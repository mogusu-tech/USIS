from django.contrib import admin

from myapp.models import *

# Register your models here.
admin.site.register(User)
admin.site.register(StudentProfile)
admin.site.register(LecturerProfile)
admin.site.register(Attendance)
admin.site.register(Assignment)
admin.site.register(Submission)
admin.site.register(Marks)
admin.site.register(Timetable)
admin.site.register(Group)
admin.site.register(GroupMember)
admin.site.register(Payment)
admin.site.register(Notification)
admin.site.register(ContactMessage)