from django.contrib.auth import get_user_model
from django.views import generic
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.forms import UserCreationForm

from django.core.mail import send_mail
from django.views.generic import ListView, UpdateView, CreateView

#https://data-flair.training/blogs/discussion-forum-python-django/
from .forms import *
from django.shortcuts import redirect, render
import csv
from django.db.models import Q
from django.urls import reverse_lazy
from django.contrib import messages
import requests
from datetime import datetime, timezone



# User signup / signin / signout
class PasswordsChangeView(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('agent-account')



def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.info(request,"Username or Password is not correct.")
    return render(request, 'theapp/signin.html',{})



def signout(request):
    logout(request)
    return redirect('signin')



class AgentAccountUpdate(generic.UpdateView):
    form_class = EditProfileForm
    template_name = 'theapp/agent-account.html'
    success_url = reverse_lazy('dashboard')

    def get_object(self):
        return self.request.user



def dashboard(request):
    accounts = Account.objects.filter(agent=request.user)
    accounts = accounts.filter(converted = True)

    user_tasks = Task.objects.filter(agent=request.user)
    sponsor_tasks = user_tasks.filter(is_sponsor=True)
    course_tasks = user_tasks.filter(is_course=True)
    return render(request, 'theapp/dashboard.html', {'sponsor_tasks':sponsor_tasks,'course_tasks':course_tasks,'accounts':accounts})



def create_course_task(request):
    if request.method == "POST":
        description = request.POST["description"]

        task = Task.objects.create(
                    description=description,
                    agent=request.user,
                    is_course=True
                )
        return redirect('dashboard')
    return render(request, 'theapp/create-task.html', {})




def create_sponsor_task(request):
    if request.method == "POST":
        description = request.POST["description"]

        task = Task.objects.create(
                    description=description,
                    agent=request.user,
                    is_sponsor=True
                )
        return redirect('dashboard')
    return render(request, 'theapp/create-task.html', {})




def delete_task(request, pk):
    task = Task.objects.get(id=pk).delete()

    return redirect('dashboard')



def tech_support(request):
    if request.method == "POST":
        subject = request.POST["subject"]
        body = request.POST["body"]
        user = request.user

        support = SupportTicket.objects.create(
                    subject=subject,
                    body=body,
                    agent=user
                )

        submitted = 'true'

        # email developer

        send_mail(
            'You got a support request!',
            'From ' + support.agent.username +  '. Reply to them via email at: ' + support.agent.email + '.  ---------   Subject: ' + support.subject + '.   ---------    Body: ' + support.body,
            'from@team.com',
            ['devoncodes@protonmail.com'],
            fail_silently=False,
        )

        return render(request, 'theapp/tech-support.html', {'submitted':submitted})

    return render(request, 'theapp/tech-support.html', {})



def course_prospects(request):

    prospects = Account.objects.filter(is_course=True)
    prospects_count = len(prospects)
    prospects = prospects[:10]

    return render(request, 'theapp/prospects.html', {'prospects_count':prospects_count,'prospects':prospects})



def sponsor_prospects(request):

    # needs_sponsors = SponsorCohort.objects.filter(active=True)

    prospects = Account.objects.filter(is_sponsor=True)

    return render(request, 'theapp/prospects.html', {'prospects':prospects})



class update_script(UpdateView):
    model = Script
    template_name = 'theapp/update-script.html'
    form_class = EditScriptForm
    success_url = reverse_lazy('dashboard')



class update_voicemail(UpdateView):
    model = VoicemailScript
    template_name = 'theapp/update-script.html'
    form_class = EditVoicemailForm
    success_url = reverse_lazy('dashboard')



def create_scripts(request, pk):
    # Create Golf Course Call Script
    title = 'Golf Course Call Script'
    body = 'Good Am/Pm, may I speak with whoever handles the golf scorecards? (Wait for Answer) My name is […] with Western Specialty Products, I have a scorecard program that can benefit you and your golf course. Do you have a minute to let me explain why we offer the best scorecards available?  (Wait for Answer - if OK:) Our admin team will go over the details with you. (Go over incentive PDF. Then follow up with the email below to our admin team.) '

    scripts = Script.objects.create(
                        agent=request.user,
                        title=title,
                        body=body,
                        is_course = True
                    )
    # Create Golf Course Voicemail Script
    title = 'Golf Course Voicemail Script'
    body = 'Good Am/Pm, My name is […] with Western Specialty Products, I have a scorecard program that can benefit you and your golf course. If you could give me a shout back, I would love to explain why we offer the best scorecards available. My number is...'
    scripts = VoicemailScript.objects.create(
                        agent=request.user,
                        title=title,
                        body=body,
                        is_course = True
                    )

    # Sponsor Call Script
    title = 'Sponsor Call Script'
    body = 'Good Am/Pm, may I speak with whoever handles your marketing? (Wait for Answer) My name is […] with Western Specialty Products, I have a local marketing program that can benefit you and your business. Do you have a minute to let me explain?  (Wait for Answer - if OK:) (Go over incentive PDF. Then follow up with the email below to our admin team.) '

    scripts = Script.objects.create(
                        agent=request.user,
                        title=title,
                        body=body,
                        is_sponsor = True
                    )
    # Create Sponsor Voicemail Script
    title = 'Sponsor Voicemail Script'
    body = 'Good Am/Pm, My name is […] with Western Specialty Products, I have a scorecard program that can benefit you and your golf course. If you could give me a shout back, I would love to go over a local marketing program that can benefit you and your business. My number is...'
    scripts = VoicemailScript.objects.create(
                        agent=request.user,
                        title=title,
                        body=body,
                        is_sponsor = True
                    )

    return redirect('profile', pk=pk)



def my_accounts(request):
    # get course accounts
    course_accounts = Account.objects.filter(agent=request.user)
    course_accounts = course_accounts.filter(converted=True)
    course_accounts = course_accounts.filter(is_course=True)

    # get sponsor accounts
    sponsor_accounts = Account.objects.filter(agent=request.user)
    sponsor_accounts = sponsor_accounts.filter(converted=True)
    sponsor_accounts = sponsor_accounts.filter(is_sponsor=True)


    return render(request, 'theapp/my-accounts.html', {'course_accounts':course_accounts,'sponsor_accounts':sponsor_accounts})



def my_prospects(request):
    # get course prospects
    course_accounts = Account.objects.filter(agent=request.user)
    course_accounts = course_accounts.filter(converted=False)
    course_accounts = course_accounts.filter(is_course=True)

    # get sponsor prospects
    sponsor_accounts = Account.objects.filter(agent=request.user)
    sponsor_accounts = sponsor_accounts.filter(converted=False)
    sponsor_accounts = sponsor_accounts.filter(is_sponsor=True)

    return render(request, 'theapp/my-prospects.html', {'course_accounts':course_accounts,'sponsor_accounts':sponsor_accounts})



def close_deal(request, pk):
    account = Account.objects.get(id=pk)
    # ensure decision maker and email have been created
    if account.decision_maker and account.email:

        account.converted = True
        account.save()

        # email admin to follow up (for now its developer)
        send_mail(
            'New Account Needs Follow Up!',
            'Business: ' + account.biz_name  + ' --- Decision Maker: ' + account.decision_maker + ' --- Email: ' + account.email + ' --- Phone: ' + account.phone + ' --- URL: ' + account.link,
            'from@team.com',
            ['devoncodes@protonmail.com'],
            fail_silently=False,
        )

        # email the agent a thank you note
        send_mail(
            'Congratulations on closing that deal today!',
            'Hey, I appreciate your hard work closing the ' + account.biz_name + ' account. Your efforts are noted!',
            'from@team.com',
            [request.user.email],
            fail_silently=False,
        )

        return redirect('profile', pk=pk)

    return redirect('profile', pk=pk)



def update_account(request, pk):
    if request.method == "POST":

        email = request.POST["email"]
        decision_maker = request.POST["decision-maker"]

        account = Account.objects.get(id=pk)
        account.email = email
        account.decision_maker = decision_maker
        account.save()

        return redirect('profile', pk=pk)



def create_note(request, pk):
    if request.method == "POST":
        body = request.POST["body"]
        account = Account.objects.get(id=pk)

        note = Note.objects.create(
                        account=account,
                        body=body
                    )
        return redirect('profile', pk=pk)



def profile(request, pk):

    # check for voicemail scripts and toggle button
    if request.method == "POST":
        # Claim the lead as the agents
        voicemails = VoicemailScript.objects.filter(agent=request.user)

        account = Account.objects.get(id=pk)
        account.agent = request.user
        account.save()

        # for notification
        claimed = 'true'

        #golf scripts
        golf_voicemails = VoicemailScript.objects.filter(agent=request.user)
        golf_voicemails = golf_voicemails.filter(is_course=True)
        golf_scripts = Script.objects.filter(agent=request.user)
        golf_scripts = golf_scripts.filter(is_course=True)

        #sponsor scripts
        sponsor_voicemails = VoicemailScript.objects.filter(agent=request.user)
        sponsor_voicemails = sponsor_voicemails.filter(is_sponsor=True)
        sponsor_scripts = Script.objects.filter(agent=request.user)
        sponsor_scripts = sponsor_scripts.filter(is_sponsor=True)

        profile = Account.objects.get(id=pk)

        #notes
        notes = Note.objects.filter(account=profile).order_by('-id')
        return render(request, 'theapp/profile.html', {'notes':notes,'sponsor_scripts':sponsor_scripts,'sponsor_voicemails':sponsor_voicemails,'golf_scripts':golf_scripts,'golf_voicemails':golf_voicemails,'claimed':claimed,'profile':profile})

    #golf scripts
    golf_voicemails = VoicemailScript.objects.filter(agent=request.user)
    golf_voicemails = golf_voicemails.filter(is_course=True)
    golf_scripts = Script.objects.filter(agent=request.user)
    golf_scripts = golf_scripts.filter(is_course=True)

    #sponsor scripts
    sponsor_voicemails = VoicemailScript.objects.filter(agent=request.user)
    sponsor_voicemails = sponsor_voicemails.filter(is_sponsor=True)
    sponsor_scripts = Script.objects.filter(agent=request.user)
    sponsor_scripts = sponsor_scripts.filter(is_sponsor=True)

    profile = Account.objects.get(id=pk)
    #notes
    notes = Note.objects.filter(account=profile).order_by('-id')

    ### WEATHER ###
    city = profile.address
    city = city.split(',', 1)[0]

    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid=8adeafa1da277ff64dfe8f1addfb3e36&units=imperial'.format(city)

    res = requests.get(url)

    data = res.json()

    temp = data['main']['temp']
    temp = int(temp)

    weather_description = data['weather'][0]['description']

    return render(request, 'theapp/profile.html', {'temp':temp,'weather_description':weather_description,'notes':notes,'sponsor_scripts':sponsor_scripts,'sponsor_voicemails':sponsor_voicemails,'golf_scripts':golf_scripts,'golf_voicemails':golf_voicemails,'profile':profile})



def create_prospect(request):
    if request.method == "POST":

        biz_name = request.POST["biz_name"]
        phone = request.POST["phone"]
        link = request.POST["link"]
        address = request.POST["address"]


        new_account = Account.objects.create(
                    agent=request.user,
                    biz_name=biz_name,
                    phone=phone,
                    link=link,
                    address=address,
                    is_sponsor=True
                )

        return redirect('my-prospects')

    needs_sponsors = Account.objects.filter(needs_sponsors=True)
    needs_sponsors = needs_sponsors.filter(agent=request.user)

    return render(request, 'theapp/create-prospect.html', {'needs_sponsors':needs_sponsors})



def forum(request):
    discussions = Discussion.objects.all().order_by('-id')
    count = discussions.count()

    context = {
              'count':count,
              'discussions':discussions}
    return render(request,'theapp/forum.html', context)



def discussion_details(request, pk):
    discussion = Discussion.objects.get(id=pk)
    comments = Comment.objects.filter(discussion=discussion).order_by('-id')
    context = {'comments':comments,
              'discussion':discussion}
    return render(request,'theapp/discussion.html', context)



def add_discussion(request):
    if request.method == "POST":
        username = request.POST["user"]
        topic = request.POST["topic"]
        description = request.POST["description"]

        new_forum = Discussion.objects.create(
                    username=username,
                    topic=topic,
                    description=description,
                )

        discussions = Discussion.objects.all().order_by('-id')
        count = discussions.count()

        context = {
              'count':count,
              'discussions':discussions}

        # email the team
        User = get_user_model()
        users = User.objects.all()
        for user in users:
            send_mail(
            'A new forum discussion was started',
            'The discussion is about ' + new_forum.topic +  '. Check your account for details!',
            'from@team.com',
            [user.email],
            fail_silently=False,
        )

        return render(request,'theapp/forum.html', context)

    return render(request,'theapp/add-discussion.html', {})



def add_comment(request, pk):

    if request.method == "POST":
        username = request.POST["user"]
        discussion = request.POST["discussion"]
        comment = request.POST["comment"]

        discussion = Discussion.objects.get(id=int(discussion))

        new_discussion = Comment.objects.create(
                    username=username,
                    discussion=discussion,
                    comment=comment,
                )

        # send email to post user notifying they got a comment on their discussion
        User = get_user_model()
        username = discussion.username
        user = User.objects.get(username=username)

        send_mail(
            'Your discussion got a comment!',
            'The discussion ' + discussion.topic +  ' got a comment. Check your account for details!',
            'from@team.com',
            [user.email],
            fail_silently=False,
        )

        return redirect('discussion', pk=pk)

    discussion = Discussion.objects.get(id=pk)

    return render(request,'theapp/add-comment.html', {'discussion':discussion})



class SearchResultsView(ListView):
    model = Account
    template_name = 'theapp/search_results.html'
    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Account.objects.filter(
            Q(biz_name__icontains=query) | Q(address__icontains=query)
        )
        return object_list



def documents(request):
    documents = Document.objects.all()
    return render(request,'theapp/documents.html', {'documents':documents})



def do_not_call(request, pk):
    account = Account.objects.get(id=pk)
    account.dont_call = True
    account.save()

    return redirect('dashboard')



#### ERROR PAGES ####
def custom_error_404(request, exception):
    return render(request, 'theapp/404.html', {})



def custom_error_500(request):
    return render(request, 'theapp/500.html', {})



def custom_error_403(request, exception):
    return render(request, 'theapp/403.html', {})



def time_clock(request):
    # see if agent is clocked in (template uses else: to show if clocked out)
    clocked_in = TimeRecord.objects.filter(agent=request.user)
    clocked_in = clocked_in.filter(completed=False)

    records = TimeRecord.objects.filter(agent=request.user)

    return render(request, 'theapp/time-clock.html', {'records':records,'clocked_in':clocked_in,})



def clock_in(request):
    start_time = datetime.now(timezone.utc)

    # save current datetime and agent
    entry = TimeRecord.objects.create(
        agent=request.user,
        start_time=start_time,
    )

    return redirect('time-clock')



def clock_out(request):
    # get agents latest record, change completed to true, update end_time, save total time using time delta
    time_record = TimeRecord.objects.filter(agent=request.user)
    latest_time_record = time_record.latest('id')
    latest_time_record.completed = True
    latest_time_record.end_time = datetime.now(timezone.utc)
    # todo: currently only saves total_time up to 1 hour
    seconds = (latest_time_record.start_time - latest_time_record.end_time).total_seconds()
    minutes = (seconds % 3600) // 60
    minutes = 59 - minutes
    latest_time_record.total_time = minutes
    latest_time_record.save()
    return redirect('time-clock')
