from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from app.models import Transaction, PaymentDetail
from app.models import Ticket
from django.db import transaction
from datetime import datetime
from django.contrib.auth.decorators import login_required

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Attempt to authenticate the user
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            # Check if the user is active and a superuser
            if user.is_active and user.is_superuser:
                login(request, user)
                return redirect('/home')  # Redirect to home page upon successful login
            else:
                messages.error(request, 'User is not active or not a superuser.')
        else:
            messages.error(request, 'Invalid Login Credentials.')

    return render(request, 'login.html')


@login_required(login_url='/login')
def home_view(request):
    if request.method == 'POST':
        try:
            # Retrieve POST data
            adult_count = int(request.POST.get('adult_count', 0))
            children_count = int(request.POST.get('children_count', 0))
            student_count = int(request.POST.get('student_count', 0))
            payment_type = request.POST.get('payment_type')
            total_amount = (adult_count * 500) + (children_count * 250) + (student_count * 75)

            # Save data in the database
            ticket = Ticket(
                adult_count=adult_count,
                children_count=children_count,
                student_count=student_count,
                total_amount=total_amount,
                payment_type=payment_type,
            )
            ticket.save()

            return redirect('home')  # Redirect to a success page or wherever needed

        except Exception as e:
            # Handle any errors, log them if necessary
            print(f"Error: {e}")
            return render(request, 'home.html')

    return render(request, 'home.html')

@login_required(login_url='/login')
def collection_report_view(request):
    transactions = Transaction.objects.all().order_by('-date')

    report_data = [
        {
            'date': transaction.date.strftime('%d-%m-%Y'),
            'payment_type': transaction.payment_type,
            'total_amount': transaction.total_amount
        }
        for transaction in transactions
    ]

    return render(request, 'collection_r.html', {'report_data': report_data})

@login_required(login_url='/login')
def payment_detail_view(request):
    payment_details = PaymentDetail.objects.values('date', 'type_of_user').annotate(
        count=Sum('amount') / 50,  
        total_amount=Sum('amount')
    ).order_by('date')
    report_data = {}

    for detail in payment_details:
        date = detail['date'].strftime('%d-%m-%Y')
        user_type = detail['type_of_user']
        count = int(detail['count'])
        total_amount = detail['total_amount']

        if date not in report_data:
            report_data[date] = {
                'child_count': 0,
                'child_total_amount': 0,
                'student_count': 0,
                'student_total_amount': 0,
                'children_count': 0,
                'children_total_amount': 0,
            }

        if user_type == 'child':
            report_data[date]['child_count'] = count
            report_data[date]['child_total_amount'] = total_amount
        elif user_type == 'student':
            report_data[date]['student_count'] = count
            report_data[date]['student_total_amount'] = total_amount
        elif user_type == 'children':
            report_data[date]['children_count'] = count
            report_data[date]['children_total_amount'] = total_amount

    report_data_list = [
        {
            'date': date,
            'child_count': data['child_count'],
            'child_total_amount': data['child_total_amount'],
            'student_count': data['student_count'],
            'student_total_amount': data['student_total_amount'],
            'children_count': data['children_count'],
            'children_total_amount': data['children_total_amount'],
        }
        for date, data in report_data.items()
    ]

    report_data_list.sort(key=lambda x: datetime.strptime(x['date'], '%d-%m-%Y'), reverse=True)

    return render(request, 'payment_detail.html', {'report_data': report_data_list})
