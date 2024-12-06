from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True, default='Anonymous')
    username = models.CharField(max_length=100, default='user')
    password = models.CharField(max_length=100, default='password')
    user_type = models.CharField(max_length=100, null=True, blank=True, default='student')
    groups = models.ManyToManyField('Group', related_name='students', blank=True)


    def __str__(self):
        return self.name


class StudentProfile(models.Model):
    student_id = models.CharField(max_length=20, null=True, blank=True, default='default_id')
    course = models.CharField(max_length=100, default='default_course')
    year_of_study = models.IntegerField(default=1)
    username = models.CharField(max_length=100, default='student_username')
    name = models.CharField(max_length=100, null=True, blank=True, default='Student Name')

    def __str__(self):
        return self.username


class LecturerProfile(models.Model):
    lecturer_id = models.CharField(max_length=20, null=True, blank=True, default='default_lecturer_id')
    department = models.CharField(max_length=100, default='default_department')
    courses_taught = models.TextField(null=True, blank=True, default='[]')
    username = models.CharField(max_length=100, default='lecturer_username')
    name = models.CharField(max_length=100, null=True, blank=True, default='Lecturer Name')

    def __str__(self):
        return self.username


class Attendance(models.Model):
    student_id = models.CharField(max_length=20, null=True, blank=True, default='default_student_id')
    course = models.CharField(max_length=100, default='default_course')
    date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=(('Present', 'Present'), ('Absent', 'Absent')), default='Present')

    def __str__(self):
        return f"{self.student_id} - {self.date}"


class Assignment(models.Model):
    title = models.CharField(max_length=200, default='default_title')
    description = models.TextField(null=True, blank=True, default='No description')
    course = models.CharField(max_length=100, default='default_course')
    lecturer_name = models.CharField(max_length=100, null=True, blank=True, default='Unknown Lecturer')
    lecturer_id = models.CharField(max_length=20, null=True, blank=True, default='default_lecturer_id')
    deadline = models.DateTimeField(null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Submission(models.Model):
    assignment_id = models.CharField(max_length=200, null=True, blank=True, default='default_assignment_id')
    student_id = models.CharField(max_length=20, null=True, blank=True, default='default_student_id')
    file = models.FileField(upload_to='submissions/', null=True, blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    grade = models.FloatField(blank=True, null=True, default=0.0)

    def __str__(self):
        return f"{self.assignment_id} - {self.student_id}"


class Marks(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to User model
    assignment = models.ForeignKey('Assignment', null=True, blank=True, on_delete=models.CASCADE)  # Make it nullable
    marks = models.FloatField(default=0.0)
    graded_by = models.ForeignKey(User, related_name='graded_by', on_delete=models.SET_NULL, null=True, blank=True)  # Link to User for grading

    def __str__(self):
        return f"{self.student_id} - {self.marks}"


class Timetable(models.Model):
    username = models.CharField(max_length=100, default='default_username')
    course = models.CharField(max_length=100, default='default_course')
    day = models.CharField(max_length=10, choices=(
        ('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Saturday', 'Saturday'), ('Sunday', 'Sunday')),
        default='Monday')
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    location = models.CharField(max_length=100, default='default_location')

    def __str__(self):
        return f"{self.username} - {self.day}"


class Group(models.Model):
    name = models.CharField(max_length=100, default='default_group')
    lecturer_name = models.CharField(max_length=100, null=True, blank=True, default='Unknown Lecturer')
    lecturer_id = models.CharField(max_length=20, null=True, blank=True, default='default_lecturer_id')
    description = models.TextField(blank=True, null=True, default='No description')
    created_at = models.DateTimeField(auto_now_add=True)
    assignment = models.ForeignKey(Assignment,null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class GroupMember(models.Model):
    group_name = models.CharField(max_length=100, default='default_group')
    user_username = models.CharField(max_length=100, default='default_user')
    user_id = models.CharField(max_length=20, null=True, blank=True, default='default_user_id')
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_username} - {self.group_name}"


class Payment(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='payments', null=True, blank=True)
    user_username = models.CharField(max_length=100, default='default_user')
    user_id = models.CharField(max_length=20, null=True, blank=True, default='default_user_id')
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    transaction_id = models.CharField(max_length=100, unique=True, default='default_transaction')
    status = models.CharField(max_length=20, choices=(('Pending', 'Pending'), ('Completed', 'Completed'), ('Failed', 'Failed')), default='Pending')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_username} - {self.transaction_id}"


class Notification(models.Model):
    recipient_username = models.CharField(max_length=100, default='default_user')
    recipient_id = models.CharField(max_length=20, null=True, blank=True, default='default_user_id')
    message = models.TextField(default='No message')
    read_status = models.BooleanField(default=False)
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"To: {self.recipient_username} - {self.message[:30]}"


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=150)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"


