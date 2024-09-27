from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from app.models import Ticket, add_user
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
import openpyxl




def add_user_view(request):
    if request.method == "POST":
        try:
            username = request.POST.get['username']
            fname = request.POST.get['fname']
            lname = request.POST.get['lname']
            email = request.POST.get['email']
            pwd = request.POST.get['pwd']
            new_user = add_user(
                username = username,
                fname = fname,
                lname = lname,
                email = email,
                pwd = pwd
            )
            new_user.save()
            return redirect('add_user_view')
        except Exception as e:
            # Handle any errors, log them if necessary
            print(f"Error: {e}")
            return render(request, 'home.html')

    return render(request, 'home.html')



        # myuser = User.objects.create_user(username, email, pwd)
        # myuser.first_name = fname
        # myuser.last_name = lname
        # myuser.save()
        # messages.success(request,"Successfully Created")
        # return redirect('Signin')
@never_cache
def login_view(request):
    # print(request.user.is_authenticated , "user is ")
    if request.user.is_authenticated:  
        return redirect('/home')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Attempt to authenticate the user
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            if user.is_active and user.is_superuser:
                login(request, user)
                return redirect('/collection_report')  # Redirect to home page upon successful login
            elif user.is_active and user.is_staff:
                login(request, user)
                print("staff is logined in ")
                return redirect('/home')
            # Check if the user is active and a superuser
        else:
            messages.error(request, 'Invalid Login Credentials.')
    
    response = render(request, 'login.html')
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response

def logout_view(request):
    logout(request)
    return redirect('/')

@login_required(login_url='/login')
def home_view(request):
    if request.method == 'POST':
        try:
            # Retrieve POST data
            adult_count = int(request.POST.get('adult_count') or '0')
            children_count = int(request.POST.get('children_count') or '0')
            student_count = int(request.POST.get('student_count') or '0')

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


def export_ticket_data(request):
    # Create an in-memory workbook and worksheet
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = 'Ticket Data'
    
    # Define the headers for the Excel file
    headers = ['Date', 'Adult', 'Children', 'Student', 'Total Amount', 'Payment']
    ws.append(headers)

    # Fetch data from the database (your collection_report query here)
    collection_report = Ticket.objects.all()

    # Loop through the queryset and write the rows into the Excel file
    for ticket in collection_report:
        ws.append([
            ticket.created_at.strftime('%Y-%m-%d'),  # Format the date if necessary
            ticket.adult_count,
            ticket.children_count,
            ticket.student_count,
            ticket.total_amount,
            ticket.payment_type,
        ])

    # Prepare the response with the appropriate content-type for Excel
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=ticket_data.xlsx'
    
    # Save the Excel file in the response
    wb.save(response)

    return response
def ticket_report_view(request):
    # Get the filter value from the GET request
    filter_option = request.GET.get('filter', '')

    # Get the current date
    today = timezone.now().date()

    # Initialize the queryset
    collection_report = Ticket.objects.all()

    # Apply filter based on the selected option
    if filter_option == 'today':
        collection_report = collection_report.filter(created_at__date=today)
    elif filter_option == 'yesterday':
        yesterday = today - timedelta(days=1)
        collection_report = collection_report.filter(created_at__date=yesterday)
    elif filter_option == 'day_before_yesterday':
        day_before_yesterday = today - timedelta(days=2)
        collection_report = collection_report.filter(created_at__date=day_before_yesterday)
    # Pass the filtered queryset to the template
    return render(request, 'collection_report.html', {'collection_report': collection_report})
