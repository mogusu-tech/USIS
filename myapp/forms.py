from django import forms
from myapp.models import*
class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['title', 'description', 'course', 'lecturer_name']

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'lecturer_name', 'lecturer_id', 'description']

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['file']

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['group', 'user_username', 'user_id', 'amount', 'transaction_id', 'status']

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']

