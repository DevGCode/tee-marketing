from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('admin-dash', admin_dashboard, name="admin-dash"),
    # create cohort
    path('create-cohort/<int:pk>', create_cohort, name="create-cohort"),
    # update cohort
    path('update-cohort/<int:pk>', update_cohort, name="update-cohort"),
    # deletes a cohort sponsor
    path('delete-sponsor/<int:pk>', delete_sponsor, name="delete-sponsor"),
    path('agent-deals', agent_deals, name="agent-deals"),
    path('agent-pipeline', agent_pipeline, name="agent-pipeline"),
    path('course-needs-sponsors', course_needs_sponsors, name="course-needs-sponsors"),
    # admin tasks
    path('create-admin-task', create_admin_task, name="create-admin-task"),
    path('delete-admin-task/<int:pk>', delete_admin_task, name="delete-admin-task"),
    # proposals
    path('make-proposals/', make_proposals, name="make-proposals"),
    path('csv-proposals/', csv_proposals, name="csv-proposals"),
    path('sponsor-pdf/<int:pk>/', sponsor_pdf, name="sponsor-pdf"),
    path('scorecard-pdf/<int:pk>/', scorecard_pdf, name="scorecard-pdf"),
    # get prospects
    path('get-prospects/', get_prospects, name="get-prospects"),

]
