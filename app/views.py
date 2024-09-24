from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from app.models import Ticket
from datetime import datetime
from django.contrib.auth.decorators import login_required

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Attempt to authenticate the user
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            if user.is_active and user.is_staff:
                login(request, user)
                return redirect('/home2')
            # Check if the user is active and a superuser
            elif user.is_active and user.is_superuser:
                login(request, user)
                return redirect('/home')  # Redirect to home page upon successful login
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
def collection_report(request):
    collection_report = Ticket.objects.all()
    return render(request, 'collection_report.html', {'collection_report': collection_report})


