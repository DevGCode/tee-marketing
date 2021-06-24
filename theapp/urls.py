from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from .views import *
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', login_required(dashboard), name="dashboard"),
    # Logins
    path("signin/", signin, name="signin"),
    path("signout/", login_required(signout), name="signout"),
    # prospects
    path('course-prospects/', login_required(course_prospects), name="course-prospects"),
    path('sponsor-prospects/', login_required(sponsor_prospects), name="sponsor-prospects"),
    # close deal
    path('close-deal/<int:pk>', login_required(close_deal), name="close-deal"),
     # both a prospect or account profile
    path('profile/<int:pk>', login_required(profile), name="profile"),
    # all accounts for admin - my closed deals for agents
    path('my-accounts/', login_required(my_accounts), name="my-accounts"),
    # all prospects for agents
    path('my-prospects/', login_required(my_prospects), name="my-prospects"),
    # team forum
    path('forum/', login_required(forum), name="forum"),
    # documents
    path('documents/', login_required(documents), name="documents"),
    path('discussion/<int:pk>', login_required(discussion_details), name='discussion'),
    path('add-discussion/', login_required(add_discussion), name='add-discussion'),
    path('add-comment/<int:pk>', login_required(add_comment), name='add-comment'),
    # support
    path('tech-support/', login_required(tech_support), name='tech-support'),
    # search
    path('search/', login_required(SearchResultsView.as_view()), name='search-results'),
    # auto create default scripts
    path('create-scripts/<int:pk>', login_required(create_scripts), name='create-scripts'),
    # update scripts
    path('update-script/<int:pk>', login_required(update_script.as_view()), name='update-script'),
    path('update-voicemail/<int:pk>', login_required(update_voicemail.as_view()), name='update-voicemail'),
    # update prospect/lead account
    path('update-account/<int:pk>', login_required(update_account), name='update-account'),
    # create note
    path('create-note/<int:pk>', login_required(create_note), name='create-note'),
    # create prospect
    path('create-prospect/', login_required(create_prospect), name='create-prospect'),
    # delete task
    path('delete-task/<int:pk>', login_required(delete_task), name='delete-task'),
    # add tasks
    path('create-course-task/', login_required(create_course_task), name='create-course-task'),
    path('create-sponsor-task/', login_required(create_sponsor_task), name='create-sponsor-task'),
    # update password
    path('password/', login_required(PasswordsChangeView.as_view(template_name="theapp/change-password.html")), name='password'),
    # agent account settings
    path('agent-account/', login_required(AgentAccountUpdate.as_view()), name="agent-account"),
    # add account to "do not call" list
    path('do-not-call/<int:pk>/', login_required(do_not_call), name='do-not-call'),
    # timeclock
    path('time-clock/', login_required(time_clock), name="time-clock"),
    path('clock-in/', login_required(clock_in), name="clock-in"),
    path('clock-out/', login_required(clock_out), name="clock-out"),

]
