from django.contrib.auth import get_user_model
# from django.urls import reverse
from django.db import models
# from django.db.models.signals import post_save
# from django.dispatch import receiver
from ckeditor.fields import RichTextField
# from django.utils import timezone
# from datetime import datetime, date



User = get_user_model()



class Account(models.Model):
    needs_sponsors = models.BooleanField(default=False)
    is_course = models.BooleanField(default=False)
    is_sponsor = models.BooleanField(default=False)
    converted = models.BooleanField(default=False)
    converted_date = models.DateTimeField(auto_now_add=False, null=True)
    agent = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    dont_call = models.BooleanField(default=False)
    biz_name = models.CharField(max_length=100, null=True, unique=True)
    decision_maker = models.CharField(max_length=100, null=True)
    email = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=100, null=True)
    link = models.CharField(max_length=1000, null=True)

    def __str__(self):
        return self.biz_name


# Reference a course Account
# Reference the sponsor Accounts
# In a view, count > 20 loads the course Account and toggles "needs_sponsors"
# create the course_id by loading the actual course, copying the id, and then reversing that to edit
class SponsorCohort(models.Model):
    course_id = models.CharField(max_length=100, null=True)
    sponsors = models.ManyToManyField(Account)

    def __str__(self):
        return self.course_id




class Note(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    body = models.CharField(max_length=8500)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
            return self.account.biz_name





class EmailTemplate(models.Model):
    title = models.CharField(max_length=30)
    subject = models.CharField(max_length=300)
    body = models.CharField(max_length=2000)
    recipient = models.CharField(max_length=100)

    def __str__(self):
            return self.user.username



class SupportTicket(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    agent = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=300)
    body = models.CharField(max_length=2000)

    def __str__(self):
            return self.subject


class Script(models.Model):
    agent = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    body = RichTextField(default=False)
    is_sponsor = models.BooleanField(default=False)
    is_course = models.BooleanField(default=False)

    def __str__(self):
            return self.title


class VoicemailScript(models.Model):
    agent = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    body = RichTextField(default=False)
    is_sponsor = models.BooleanField(default=False)
    is_course = models.BooleanField(default=False)

    def __str__(self):
            return self.title



# FORUM #

class Discussion(models.Model):
    username = models.CharField(max_length=200)
    topic = models.CharField(max_length=300)
    description = models.CharField(max_length=1000, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    current = models.BooleanField(default=False)

    def __str__(self):
        return str(self.topic)


class Comment(models.Model):
    username = models.CharField(max_length=200)
    discussion = models.ForeignKey(Discussion, blank=True, on_delete=models.CASCADE)
    comment = models.CharField(max_length=2000)
    date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.discussion)








class Task(models.Model):
    agent = models.ForeignKey(User, blank=True, on_delete=models.CASCADE)
    is_course = models.BooleanField(default=False)
    is_sponsor = models.BooleanField(default=False)
    description = models.CharField(max_length=900)

    def __str__(self):
        return self.description

# redundancy is for security purposes
class AdminTask(models.Model):
    user = models.ForeignKey(User, blank=True, on_delete=models.CASCADE)
    description = models.CharField(max_length=900)

    def __str__(self):
        return self.description



class Document(models.Model):
    title = models.CharField(max_length=100)
    upload = models.FileField(upload_to ='team-documents/')

    def __str__(self):
            return self.title





# PDF
class LeadPDF(models.Model):
    generated = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    full_name = models.CharField(max_length=100, null=True)
    first_name = models.CharField(max_length=100, null=True)
    biz_name = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.biz_name


# Time
class TimeRecord(models.Model):
    agent = models.ForeignKey(User, blank=True, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=False, blank=True, null=True)
    end_time = models.DateTimeField(auto_now_add=False, blank=True, null=True)
    completed = models.BooleanField(default=False)
    total_time = models.IntegerField(null=True)
    date = models.DateField(auto_now_add=True)


    def __str__(self):
        return self.agent.username
