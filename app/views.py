from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from app.models import Transaction, PaymentDetail
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
            adult = request.POST.get('adult')
            adult_count = int(request.POST.get('adult_count', 0))
            children = request.POST.get('children')
            children_count = int(request.POST.get('children_count', 0))
            student = request.POST.get('student')
            student_count = int(request.POST.get('student_count', 0))
            payment_type = request.POST.get('payment_type')

            # Calculate the total amount based on your logic (you can adjust this)
            total_amount = (adult_count * 100) + (children_count * 50) + (student_count * 75)
            current_date = datetime.now().date()

            # Create Transaction object
            with transaction.atomic():  # Ensure atomicity
                transaction_obj = Transaction.objects.create(
                    date=current_date,
                    payment_type=payment_type,
                    total_amount=total_amount
                )
                # Create PaymentDetail objects
                if adult and adult_count > 0:
                    PaymentDetail.objects.create(
                        date=current_date,
                        type_of_user='adult',
                        amount=adult_count * 100,
                    )

                if children and children_count > 0:
                    PaymentDetail.objects.create(
                        date=current_date,
                        type_of_user='children',
                        amount=children_count * 50,
                    )

                if student and student_count > 0:
                    PaymentDetail.objects.create(
                        date=current_date,
                        type_of_user='student',
                        amount=student_count * 75,
                    )

            # Redirect or return a success message
            messages.success(request, 'Transaction and Payment Details saved successfully!')
            return redirect('home')  # Redirect to home or another page

        except Exception as e:
            # Handle errors and display a message
            messages.error(request, f'An error occurred: {str(e)}')
            return render(request, 'home.html', {})

    return render(request, "home.html", {})


@login_required(login_url='/login')
def collection_report_view(request):
    # Query the Transaction model to get the required data, sorted by date in descending order
    transactions = Transaction.objects.all().order_by('-date')

    # Prepare the data array
    report_data = [
        {
            'date': transaction.date.strftime('%d-%m-%Y'),
            'payment_type': transaction.payment_type,
            'total_amount': transaction.total_amount
        }
        for transaction in transactions
    ]

    # Pass the report_data to the template
    return render(request, 'collection_r.html', {'report_data': report_data})

from django.db.models import Sum
@login_required(login_url='/login')
def payment_detail_view(request):
    # Query the PaymentDetail model, aggregate data by date and user type
    payment_details = PaymentDetail.objects.values('date', 'type_of_user').annotate(
        count=Sum('amount') / 50,  # Assuming each "count" corresponds to a fixed amount (like 50 for children)
        total_amount=Sum('amount')
    ).order_by('date')

    # Prepare a dictionary to hold the data grouped by date
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

    # Convert report_data to a list for easy iteration in the template
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

    # Sort the list by date in descending order
    report_data_list.sort(key=lambda x: datetime.strptime(x['date'], '%d-%m-%Y'), reverse=True)

    return render(request, 'payment_detail.html', {'report_data': report_data_list})