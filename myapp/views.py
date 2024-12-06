from datetime import datetime

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views import View

from myapp.forms import *
from myapp.models import *
import json
import requests
import base64
import random


# Create your views here.
def index(request):
    return render(request,'index.html')
def about(request):
    return render(request, 'about.html')
def contact(request):
    return render(request, 'contact.html')
def courses(request):
    return render(request,'courses.html')
def course(request):
    return render(request, 'course-details.html')
def events(request):
    return render(request, 'events.html')
def pricing(request):
    return render(request, 'pricing.html')
def trainers(request):
    return render(request, 'trainers.html')
def starterpage(request):
    return render(request,'starter-page.html')

#Custom Views
def register(request):
    if request.method == "POST":
        members=User(
            name=request.POST['name'],
            username=request.POST['username'],
            password=request.POST['password'],
            user_type=request.POST['user_type']


        )
        members.save()
        return redirect('/login')
    else:
        return render(request, 'registration.html')


def login(request):
    if request.method == "POST":
        # Authenticate user by matching username and password
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            # Retrieve the user from the database
            user = User.objects.get(username=username, password=password)

            # Check user type and redirect accordingly
            if user.user_type == 'Student':
                return redirect('student_dashboard')  # Ensure 'index' is defined in urls.py
            elif user.user_type == 'Lecturer':  # Ensure 'Lecturer' is correctly typed
                return redirect('lecturer_dashboard')  # Ensure 'courses' is defined in urls.py

        except User.DoesNotExist:
            # If user does not exist, show an error
            messages.error(request, "Invalid username or password. Please try again.")
            return redirect('/login')

    else:
        return render(request, 'login.html')

def student_dashboard(request):
    # Here, you can fetch the student's data from the database (e.g., assignments, grades, timetable)
    return render(request, 'student_dashboard.html')

def lecturer_dashboard(request):
    return render(request, 'lecturer_dashboard.html')

def assignment(request):
    if request.method == "POST":
        form = AssignmentForm(request.POST)
        if form.is_valid():  # Automatically checks if the data is correct
            form.save()  # Saves the form data to the database
            return redirect('/index')  # Redirect to assignments list or another page
    else:
        form = AssignmentForm()  # Initialize an empty form

    return render(request, 'create_assignment.html', {'form': form})


from django.shortcuts import render
from myapp.models import Assignment

def view_assignments(request):
    if request.method == "GET":
        # Order assignments by a valid field (e.g., 'deadline')
        assignments = Assignment.objects.all().order_by('deadline')  # Adjust based on your requirements

        # Render assignments in the template
        return render(request, 'view_assignment.html', {'assignments': assignments})

    elif request.method == "POST":
        # Example for filtered query
        title = request.POST.get('title')
        course = request.POST.get('course')

        assignments = Assignment.objects.all()
        if title:
            assignments = assignments.filter(title__icontains=title)
        if course:
            assignments = assignments.filter(course_id=course)

        assignments = assignments.order_by('deadline')  # Adjust ordering if needed
        return render(request, 'view_assignment.html', {'assignments': assignments})




def submit_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)

    if request.method == 'POST':
        # Handle file submission
        file = request.FILES.get('file')
        submission = Submission.objects.create(
            assignment_id=assignment.id,
            student_id=request.user.username,  # Assuming user.username is the student ID
            file=file
        )
        return redirect('view_assignments')  # Redirect to the assignments list after submission

    return render(request, 'submit_assignment.html', {'assignment': assignment})

from .models import Notification

def manage_groups(request):
    if request.method == "POST":
        # Handle group creation or editing if necessary
        form = GroupForm(request.POST)
        if form.is_valid():
            new_group = form.save()  # Save the new group and capture it in a variable

            # Notify relevant lecturers about the new group
            lecturers = User.objects.filter(user_type='lecturer')  # Adjust based on your user model
            for lecturer in lecturers:
                Notification.objects.create(
                    recipient_username=lecturer.username,
                    recipient_id=lecturer.id,
                    message=f"A new group '{new_group.name}' has been created."
                )

            return redirect('manage_groups')  # Redirect to the same page after saving
    else:
        # Display groups and the form to add a new one
        groups = Group.objects.all()  # Fetch all groups
        form = GroupForm()  # Empty form for creating a new group

    return render(request, 'manage_groups.html', {'groups': groups, 'form': form})


def edit_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    if request.method == "POST":
        form = GroupForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            return redirect('manage_groups')
    else:
        form = GroupForm(instance=group)

    return render(request, 'edit_group.html', {'form': form})

def delete_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    group.delete()
    return redirect('manage_groups')

def view_group(request):
    groups = Group.objects.all()  # Fetch all groups
    user = request.user  # Get the logged-in user
    joined_groups = GroupMember.objects.filter(user_username=user.username)  # Get all group members that the user has joined
    joined_group_names = [gm.group_name for gm in joined_groups]  # Prepare a list of group names the user has joined
    return render(request, 'view_group.html', {'groups': groups, 'joined_group_names': joined_group_names})

def view_group_members(request, group_id):
    # Fetch the group by ID
    group = get_object_or_404(Group, id=group_id)

    # Fetch the members of this group
    group_members = GroupMember.objects.filter(group_name=group.name)

    # Render the group and its members in the template
    return render(request, 'view_group_members.html', {'group': group, 'group_members': group_members})


def join_group(request, group_id):
    group = Group.objects.get(id=group_id)
    user = request.user

    # Check if the user has already joined a group
    if GroupMember.objects.filter(user_username=user.username).exists():
        messages.error(request, "You can only join one group.")
        return redirect('view_group')

    # If not already in a group, add the user to the selected group
    if not GroupMember.objects.filter(group_name=group.name, user_username=user.username).exists():
        GroupMember.objects.create(group_name=group.name, user_username=user.username, user_id=user.id)

    return redirect('view_group')

def leave_group(request, group_id):
    group = Group.objects.get(id=group_id)
    user = request.user  # Get the logged-in user
    GroupMember.objects.filter(group_name=group.name, user_username=user.username).delete()  # Remove user from the group
    return redirect('view_group')


def add_timetable(request):
    if request.method == "POST":
        username = request.user.username  # Get the logged-in user's username
        course = request.POST['course']
        day = request.POST['day']
        start_time = request.POST['start_time']
        end_time = request.POST['end_time']
        location = request.POST['location']

        # Create a new timetable entry
        Timetable.objects.create(
            username=username,
            course=course,
            day=day,
            start_time=start_time,
            end_time=end_time,
            location=location
        )

        return redirect('view_timetable')  # Redirect to the page where timetables are displayed

    return render(request, 'add_timetable.html')

def view_timetable(request):
    # Fetch all timetables for the logged-in user
    timetables = Timetable.objects.filter(username=request.user.username)
    return render(request, 'view_timetable.html', {'timetables': timetables})


def edit_timetable(request, id):
    timetable = get_object_or_404(Timetable, id=id)

    if request.method == "POST":
        timetable.course = request.POST['course']
        timetable.day = request.POST['day']
        timetable.start_time = request.POST['start_time']
        timetable.end_time = request.POST['end_time']
        timetable.location = request.POST['location']
        timetable.save()
        return redirect('view_timetable')

    return render(request, 'edit_timetable.html', {'timetable': timetable})

def delete_timetable(request, id):
    timetable = get_object_or_404(Timetable, id=id)
    timetable.delete()
    return redirect('view_timetable')
def sview_timetable(request):
    # Get all timetables for the logged-in student
    timetables = Timetable.objects.filter(username=request.user.username).order_by('day', 'start_time')
    return render(request, 'sview_timetable.html', {'timetables': timetables})


def ssubmit_assignment(request, assignment_id):
    # Get the assignment by ID
    assignment = get_object_or_404(Assignment, id=assignment_id)

    # Handle the form submission for assignment (if POST request)
    if request.method == 'POST':
        file = request.FILES['file']
        student_id = request.user.id  # Assuming student is logged in

        # Create a new Submission object
        submission = Submission.objects.create(
            assignment_id=assignment_id,
            student_id=student_id,
            file=file,
        )
        submission.save()

        return render(request, 'assignment_submitted.html', {'assignment': assignment})

    return render(request, 'ssubmit_assignment.html', {'assignment': assignment})


def grades_dashboard(request):
    return render(request, 'grades_dashboard.html')


def upload_individual_grades(request, assignment_id):
    # Get the assignment
    assignment = get_object_or_404(Assignment, id=assignment_id)

    # Get all students for the specific assignment (you could use a ManyToMany relation or fetch students manually)
    students = User.objects.filter(groups__name=assignment.course)  # Assuming students are part of groups for courses

    if request.method == 'POST':
        # Process the form submission
        for student in students:
            grade = request.POST.get(f'grade_{student.id}')  # Get the grade for each student
            if grade:
                grade = float(grade)
                # Check if a grade already exists for this student and assignment
                mark, created = Marks.objects.get_or_create(
                    student=student,
                    assignment=assignment,
                    defaults={'grade': grade, 'graded_by': request.user.username, 'graded_by_id': request.user.id}
                )
                if not created:
                    mark.grade = grade  # Update existing grade
                    mark.save()

        return redirect('view_assignments')  # Redirect to a page that lists assignments

    return render(request, 'upload_individual_grades.html', {
        'assignment': assignment,
        'students': students,
    })

# views.py

# views.py
from django.shortcuts import render, get_object_or_404
from .models import Assignment, Group, Marks

def upload_group_grades(request, assignment_id):
    # Get the assignment based on the assignment_id
    assignment = get_object_or_404(Assignment, id=assignment_id)

    # Get all groups associated with this assignment
    groups = Group.objects.filter(assignment=assignment)

    if request.method == 'POST':
        # Loop through all groups and get the marks entered for each group
        for group in groups:
            marks = request.POST.get(f'marks_{group.id}')
            if marks:
                # Update or create marks for all students in the group
                for student in group.students.all():
                    Marks.objects.update_or_create(
                        student_id=student.id,
                        assignment_id=assignment.id,
                        defaults={
                            'marks': marks,
                            'graded_by_name': request.user.username,
                            'graded_by_id': request.user.id
                        }
                    )
        return HttpResponse("Group grades uploaded successfully!")

    # Render the template and pass the assignment and groups to it
    return render(request, 'upload_group_grades.html', {'assignment': assignment, 'groups': groups})

def notifications_view(request):
    # Get notifications for the logged-in user (assuming 'username' is unique)
    notifications = Notification.objects.filter(recipient_username=request.user.username).order_by('-sent_at')[:5]  # Limit to the most recent 5 notifications

    # Pass the notifications to the template
    return render(request, 'student_dashboard.html', {'notifications': notifications})

# views.py
from django.shortcuts import render
from .models import Notification

def lecturer_notifications_view(request):
    # Fetch notifications for the logged-in lecturer
    notifications = Notification.objects.filter(recipient_username=request.user.username).order_by('-sent_at')[:5]  # Limit to the most recent 5 notifications

    # Pass notifications to the template
    return render(request, 'lecturer_dashboard.html', {'notifications': notifications})



# MPESA INFORMATION
CONSUMER_KEY = 'T0uT3rh3UcZQQAAqmMNRP8m6R8BePsJRlzbgt1CsGdLIGAe0'
CONSUMER_SECRET = '50W0GBBcz0IerjbI6TLnmI1acw2Sg6UFnNLyNAVmfPsR6G5C48bGIvjNtE9FYMru'
BUSINESS_SHORT_CODE = '174379'  # Lipa Na M-Pesa Short Code
PASSKEY = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'
CALLBACK_URL = 'https://yourdomain.com/mpesa/callback'

#Generate access token
def get_mpesa_access_token():
    url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    response = requests.get(url, auth=(CONSUMER_KEY, CONSUMER_SECRET))
    if response.status_code == 200:
        return response.json()['access_token']
    else:
        raise Exception("Failed to fetch access token")


# List Payments
def payment_list(request):
    payments = Payment.objects.all()
    return render(request, 'payment_list.html', {'payments': payments})

# Add Payment
def add_payment(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('payment_list')
    else:
        form = PaymentForm()
    return render(request, 'add_payment.html', {'form': form})

#For Students
class PaymentListView(View):
    def get(self, request):
        # Get all payments for the logged-in user
        payments = Payment.objects.filter(user_id=request.user.id)

        # Get all groups for the logged-in user
        groups = Group.objects.all()

        return render(request, 'payment_list.html', {'payments': payments, 'groups': groups})


# Initiate new payment
class PaymentInitiateView(View):
    def get(self, request, group_id):
        group = get_object_or_404(Group, id=group_id)  # Fetch the specific group
        return render(request, 'payment_initiate.html', {'group': group})  # Pass the group to the template

    def post(self, request, group_id):
        # Get the data from the form submission
        phone_number = request.POST.get('phone_number')
        amount = float(request.POST.get('amount'))

        group = get_object_or_404(Group, id=group_id)  # Get the selected group again

        # Initiate the M-Pesa payment
        transaction_id, success = initiate_mpesa_payment(phone_number=phone_number, amount=amount)

        if success:
            return redirect('pricing')  # Redirect to the success page
        else:
            return redirect('pricing')
# Initiate STK Push
from django.shortcuts import redirect

from django.shortcuts import redirect
from datetime import datetime
import base64
import requests
from myapp.models import Payment  # Adjust to your app's models


from django.shortcuts import redirect

def initiate_mpesa_payment(phone_number, amount):
    try:
        access_token = get_mpesa_access_token()
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        password = base64.b64encode(f"{BUSINESS_SHORT_CODE}{PASSKEY}{timestamp}".encode()).decode()

        headers = {"Authorization": f"Bearer {access_token}"}
        payload = {
            "BusinessShortCode": BUSINESS_SHORT_CODE,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone_number,
            "PartyB": BUSINESS_SHORT_CODE,
            "PhoneNumber": phone_number,
            "CallBackURL": CALLBACK_URL,
            "AccountReference": "Payment for Group",
            "TransactionDesc": "Group Payment",
        }

        response = requests.post(
            "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest",
            json=payload,
            headers=headers,
        )

        if response.status_code == 200:
            data = response.json()
            if data.get('ResponseCode') == '0':  # Success code
                payment = Payment.objects.filter(transaction_id=data['CheckoutRequestID']).first()
                if payment:
                    payment.status = 'Completed'
                    payment.save()
                    return payment.transaction_id, True
        # Redirect to error page if initiation fails
        return None, False

    except Exception as e:
        # Log the error for debugging
        print(f"Error occurred: {e}")
        return None, False


def mpesa_callback(request):
    if request.method == 'POST':
        data = request.body.decode('utf-8')
        payment_info = json.loads(data)

        # Extract required fields
        checkout_request_id = payment_info.get('Body', {}).get('stkCallback', {}).get('CheckoutRequestID')
        result_code = payment_info.get('Body', {}).get('stkCallback', {}).get('ResultCode')
        result_desc = payment_info.get('Body', {}).get('stkCallback', {}).get('ResultDesc')

        # Handle success
        if result_code == 0:
            metadata = payment_info['Body']['stkCallback']['CallbackMetadata']['Item']
            phone_number = metadata[4]['Value']
            amount = metadata[0]['Value']

            # Update payment record
            Payment.objects.filter(transaction_id=checkout_request_id).update(
                status='Completed',
                amount=amount,
            )
            return JsonResponse({'status': 'Payment completed successfully'})

        # Handle failure
        else:
            Payment.objects.filter(transaction_id=checkout_request_id).update(
                status='Failed',
            )
            return JsonResponse({'status': 'Payment failed', 'description': result_desc})


def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()  # Save the data into the ContactMessage model
            print("Form saved successfully!")
            return redirect('contact_form')  # Redirect to the same page after successful submission
        else:
            print("Form is not valid. Errors:", form.errors)  # This will help you debug if the form is invalid
    else:
        form = ContactForm()

    return render(request, 'index.html', {'form': form})




