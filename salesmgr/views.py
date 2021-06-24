from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import get_user_model
from django.views import generic
from django.views.generic import ListView, UpdateView, CreateView
from django.shortcuts import redirect, render
from theapp.models import *
from django.urls import reverse_lazy
from django.core.mail import send_mail
import csv
from pathlib import Path
import pdfkit
# extract the last page
from pathlib import Path
from PyPDF2 import PdfFileReader, PdfFileWriter, PdfFileMerger
from datetime import datetime, timezone
# gets html
import urllib.request
# parses html
from bs4 import BeautifulSoup
from django.db import IntegrityError
import requests
from django.http import HttpResponse



@user_passes_test(lambda u: u.is_superuser)
def delete_sponsor(request, pk):
    # get the sponsor to delete
    company = Account.objects.get(id=pk)
    sponsors = SponsorCohort.objects.get(id=5)
    sponsors.sponsors.remove(company)

    return redirect('agent-deals')



@user_passes_test(lambda u: u.is_superuser)
def admin_dashboard(request):
    accounts = Account.objects.filter(converted=True)

    tasks = AdminTask.objects.filter(user=request.user)

    return render(request, 'salesmgr/dashboard.html', {'tasks':tasks,'accounts':accounts})



@user_passes_test(lambda u: u.is_superuser)
def create_admin_task(request):
    if request.method == "POST":
        description = request.POST["description"]

        task = AdminTask.objects.create(
                    description=description,
                    user=request.user,
                )
        return redirect('admin-dash')
    return render(request, 'salesmgr/create-admin-task.html', {})



@user_passes_test(lambda u: u.is_superuser)
def delete_admin_task(request, pk):
    task = AdminTask.objects.get(id=pk).delete()

    return redirect('admin-dash')



@user_passes_test(lambda u: u.is_superuser)
def agent_deals(request):
    # needs sponsors
    active_accounts = Account.objects.filter(converted=True)
    active_accounts = active_accounts.filter(needs_sponsors=True)
    active_accounts = active_accounts.filter(is_course=True)

    # has sponsors
    closed_accounts = Account.objects.filter(converted=True)
    closed_accounts = closed_accounts.filter(needs_sponsors=False)
    closed_accounts = closed_accounts.filter(is_course=True)


    sponsors = Account.objects.filter(is_sponsor=True)

    return render(request, 'salesmgr/agent-deals.html', {'sponsors':sponsors,'closed_accounts':closed_accounts,'active_accounts':active_accounts})



@user_passes_test(lambda u: u.is_superuser)
def course_needs_sponsors(request):
    if request.method == "POST":
        posted_course = request.POST["course"]

        # toggle needs_sponsors
        course = Account.objects.get(id=posted_course)
        course.needs_sponsors = True
        course.save()

        courses = Account.objects.filter(is_course=True)
        courses = courses.filter(converted=True)

        # email the team
        User = get_user_model()
        users = User.objects.all()
        for user in users:
            send_mail(
            'A new course needs sponsors!',
            'Greetings! A new golf course needs sponsors. Check your account for details!',
            'from@team.com',
            [user.email],
            fail_silently=False,
        )

        return redirect('agent-deals')

    courses = Account.objects.filter(is_course=True)
    courses = courses.filter(converted=True)
    courses = courses.filter(needs_sponsors=False)
    return render(request, 'salesmgr/course-needs-sponsors.html', {'courses':courses})

@user_passes_test(lambda u: u.is_superuser)
def agent_pipeline(request):

    accounts = Account.objects.filter(converted=False)
    accounts = accounts.filter(agent=True)

    return render(request, 'salesmgr/agent-pipeline.html', {'accounts':accounts})



@user_passes_test(lambda u: u.is_superuser)
def update_cohort(request, pk):
    if request.method == "POST":
        sponsor = request.POST["sponsor"]

        cohort = SponsorCohort.objects.get(id=pk)
        cohort.sponsors.add(sponsor)
        cohort.save()

         # check for the max # of 20 before changing the course Account to "needs_sponsors" = False
        if cohort.sponsors.count() >= 4:
            course = Account.objects.get(id=cohort.course_id)
            course.needs_sponsors = False
            course.save()

        return redirect('create-cohort', pk=cohort.course_id)



@user_passes_test(lambda u: u.is_superuser)
def create_cohort(request, pk):

    if request.method == "POST":
        sponsors = request.POST.getlist('sponsors')

        # create the cohort
        cohort = SponsorCohort.objects.create(
                    course_id=pk
                )

        i = 0

        for sponsor in sponsors:
            # add the sponsors
            cohort.sponsors.add(sponsor[i])
            i += 1

        cohort_sponsors = cohort.sponsors.all()

        #let template know a cohort exists
        cohort_exists = True

        course = Account.objects.get(id=pk)

        return render(request, 'salesmgr/create-cohort.html', {'cohort_sponsors':cohort_sponsors,'cohort_exists':cohort_exists,'cohort':cohort,'course':course,})

    pageid = pk

    course = Account.objects.get(id=pk)

    sponsor_accounts = Account.objects.filter(is_sponsor=True)

    # let template know whether a cohort exists
    cohort_exists = True

    try:
        cohort = SponsorCohort.objects.get(course_id=pk)
        cohort_exists = True
        cohort_sponsors = cohort.sponsors.all()
    except:
        cohort_exists = False
        cohort = False
        cohort_sponsors = False

    sponsor_accounts = Account.objects.filter(is_sponsor=True)
    return render(request, 'salesmgr/create-cohort.html', {'cohort_sponsors':cohort_sponsors,'sponsor_accounts':sponsor_accounts,'cohort':cohort,'cohort_exists':cohort_exists,'course':course,'sponsor_accounts':sponsor_accounts,'pageid':pageid})



@user_passes_test(lambda u: u.is_superuser)
def get_prospects(request):
    if request.method == "POST":

        def getprospects(webpage, page_number):
            # handles pagination of webpage
            next_page = webpage + str(page_number)
            response = requests.get(str(next_page))
            # get the soup and grab prospect info
            soup = BeautifulSoup(response.content,"html.parser")
            soup_biz_name = soup.findAll("a",{"class":"business-name"})
            soup_since = soup.findAll("div",{"class":"years-in-business"})
            soup_phone = soup.findAll("div",{"class":"phones phone primary"})
            soup_address = soup.findAll("div",{"class":"locality"})

            for x in range(len(soup_biz_name)):
                biz_name = soup_biz_name[x].text
                link = soup_biz_name[x]['href']
                try:
                    phone = soup_phone[x].get_text()
                except IndexError:
                    pass

                try:
                    address = soup_address[x].get_text()
                except IndexError:
                    pass

                # data source
                link = 'https://www.yellowpages.com' + link


                try:
                    prospect = Account.objects.create(
                            is_course=True,
                            biz_name=biz_name,
                            phone=phone,
                            address=address,
                            link=link
                        )
                except IntegrityError as e:
                    pass

                # the sub strings below make sure we don't grab
                # any problematic prospects (TESTED AND THIS IS A MUST)
                # todo: needs to be DRY

                if "Golf" in biz_name:
                    try:
                        prospect = Account.objects.create(
                                is_course=True,
                                biz_name=biz_name,
                                phone=phone,
                                address=address,
                                link=link
                            )
                    except IntegrityError as e:
                        pass

                elif "Team" in biz_name:

                    try:
                        prospect = Account.objects.create(
                                is_course=True,
                                biz_name=biz_name,
                                phone=phone,
                                address=address,
                                link=link
                            )
                    except IntegrityError as e:
                        pass

                elif "Pro" in biz_name:

                    try:
                        prospect = Account.objects.create(
                                is_course=True,
                                biz_name=biz_name,
                                phone=phone,
                                address=address,
                                link=link
                            )
                    except IntegrityError as e:
                        pass

                elif "Private" in biz_name:

                    try:
                        prospect = Account.objects.create(
                                is_course=True,
                                biz_name=biz_name,
                                phone=phone,
                                address=address,
                                link=link
                            )
                    except IntegrityError as e:
                        pass

                elif "Club" in biz_name:

                    try:
                        prospect = Account.objects.create(
                                is_course=True,
                                biz_name=biz_name,
                                phone=phone,
                                address=address,
                                link=link
                            )
                    except IntegrityError as e:
                        pass

                elif "Country" in biz_name:

                    try:
                        prospect = Account.objects.create(
                                is_course=True,
                                biz_name=biz_name,
                                phone=phone,
                                address=address,
                                link=link
                            )
                    except IntegrityError as e:
                        pass

                elif "Course" in biz_name:

                    try:
                        prospect = Account.objects.create(
                                is_course=True,
                                biz_name=biz_name,
                                phone=phone,
                                address=address,
                                link=link
                            )
                    except IntegrityError as e:
                        pass


                elif "Tee" in biz_name:

                    try:
                        prospect = Account.objects.create(
                                is_course=True,
                                biz_name=biz_name,
                                phone=phone,
                                address=address,
                                link=link
                            )
                    except IntegrityError as e:
                        pass


                elif "Green" in biz_name:

                    try:
                        prospect = Account.objects.create(
                                is_course=True,
                                biz_name=biz_name,
                                phone=phone,
                                address=address,
                                link=link
                            )
                    except IntegrityError as e:
                        pass

                elif "Park" in biz_name:

                    try:
                        prospect = Account.objects.create(
                                is_course=True,
                                biz_name=biz_name,
                                phone=phone,
                                address=address,
                                link=link
                            )
                    except IntegrityError as e:
                        pass

                else:

                    pass


            # Generating the next page url in the pagination
            if page_number < 20:
                page_number = page_number + 1
                getprospects(webpage, page_number)

        # check 200 major US cities via Yellow Pages
        # # todo: add to "include" file for brevity
        locales = [
            "New York City",
            "Los Angeles",
            "Chicago",
            "Houston",
            "Phoenix",
            "Philadelphia",
            "San Antonio",
            "San Diego",
            "Dallas",
            "Austin",
            "San Jose",
            "Fort Worth",
            "Jacksonville",
            "Columbus",
            "Charlotte",
            "Indianapolis",
            "San Francisco",
            "Seattle",
            "Denver",
            "Washington",
            "Boston",
            "El Paso",
            "Nashville",
            "Oklahoma City",
            "Las Vegas",
            "Detroit",
            "Portland",
            "Memphis",
            "Louisville",
            "Milwaukee",
            "Baltimore",
            "Tucson",
            "Mesa",
            "Fresno",
            "Sacramento",
            "Atlanta",
            "Kansas City",
            "Colorado Springs",
            "Raleigh",
            "Omaha",
            "Miami",
            "Long Beach",
            "Virginia Beach",
            "Oakland",
            "Minneapolis",
            "Tampa",
            "Tulsa",
            "Arlington",
            "Wichita",
            "Bakersfield",
            "Aurora",
            "New Orleans",
            "Cleveland",
            "Anaheim",
            "Henderson",
            "Honolulu",
            "Riverside",
            "Santa Ana",
            "Corpus Christi",
            "Lexington",
            "San Juan",
            "Stockton",
            "St. Paul",
            "Cincinnati",
            "Greensboro",
            "Pittsburgh",
            "Irvine",
            "St. Louis",
            "Lincoln",
            "Orlando",
            "Durham",
            "Plano",
            "Anchorage",
            "Newark",
            "Chula Vista",
            "Fort Wayne",
            "Chandler",
            "Toledo",
            "St. Petersburg",
            "Reno",
            "Laredo",
            "Scottsdale",
            "North Las Vegas",
            "Lubbock",
            "Madison",
            "Gilbert",
            "Jersey City",
            "Glendale",
            "Buffalo",
            "Winston-Salem",
            "Chesapeake",
            "Fremont",
            "Norfolk",
            "Irving",
            "Garland",
            "Paradise",
            "Arlington",
            "Richmond",
            "Hialeah",
            "Spokane",
            "Frisco",
            "Moreno Valley",
            "Tacoma",
            "Fontana",
            "Modesto",
            "Baton Rouge",
            "Port St. Lucie",
            "San Bernardino",
            "McKinney",
            "Fayetteville",
            "Santa Clarita",
            "Des Moines",
            "Oxnard",
            "Birmingham",
            "Spring Valley",
            "Huntsville",
            "Rochester",
            "Cape Coral",
            "Tempe",
            "Grand Rapids",
            "Yonkers",
            "Overland Park",
            "Salt Lake City",
            "Amarillo",
            "Augusta",
            "Columbus",
            "Tallahassee",
            "Montgomery",
            "Huntington Beach",
            "Akron",
            "Little Rock",
            "Glendale",
            "Grand Prairie",
            "Aurora",
            "Sunrise Manor",
            "Ontario",
            "Sioux Falls",
            "Knoxville",
            "Vancouver",
            "Mobile",
            "Worcester",
            "Chattanooga",
            "Brownsville",
            "Peoria",
            "Fort Lauderdale",
            "Shreveport",
            "Newport News",
            "Providence",
            "Elk Grove",
            "Rancho Cucamonga",
            "Salem",
            "Pembroke Pines",
            "Santa Rosa",
            "Eugene",
            "Oceanside",
            "Cary",
            "Fort Collins",
            "Corona",
            "Enterprise",
            "Garden Grove",
            "Springfield",
            "Clarksville",
            "Bayamon",
            "Lakewood",
            "Alexandria",
            "Hayward",
            "Murfreesboro",
            "Killeen",
            "Hollywood",
            "Lancaster",
            "Salinas",
            "Jackson",
            "Midland",
            "Macon County",
            "Kansas City",
            "Palmdale",
            "Sunnyvale",
            "Springfield",
            "Escondido",
            "Pomona",
            "Bellevue",
            "Surprise",
            "Naperville",
            "Pasadena",
            "Denton",
            "Roseville",
            "Joliet",
            "Thornton",
            "McAllen",
            "Paterson",
            "Rockford",
            "Carrollton",
            "Bridgeport",
            "Miramar",
            "Round Rock",
            "Metairie",
            "Olathe",
            "Waco",
        ]

        # find all locales and loop through them
        for locale in locales:
            # calling the function with relevant parameters
            getprospects('https://www.yellowpages.com/search?search_terms=Food%20truck&geo_location_terms=' + locale + '&page=', 0)


        return render(request, 'salesmgr/get-prospects-form.html', {})


    return render(request, 'salesmgr/get-prospects-form.html', {})



@user_passes_test(lambda u: u.is_superuser)
def get_course_prospects(request):
    if request.method == "POST":
        csv_file = request.FILES["csv_file"]
        proposal_type = request.POST["proposal-type"]

        return redirect('get-prospects')

    return render(request, 'mainapp/get-prospects-form.html', {})



@user_passes_test(lambda u: u.is_superuser)
def sponsor_pdf(request, pk):
    lead_pdf = LeadPDF.objects.get(id=pk)
    return render(request, 'salesmgr/sponsor-proposal-object.html', {'lead_pdf':lead_pdf})



@user_passes_test(lambda u: u.is_superuser)
def scorecard_pdf(request, pk):
    lead_pdf = LeadPDF.objects.get(id=pk)
    return render(request, 'salesmgr/scorecard-proposal-object.html', {'lead_pdf':lead_pdf})



@user_passes_test(lambda u: u.is_superuser)
def make_proposals(request):
    if request.method == "POST":
        full_name = request.POST["name"]
        biz_name = request.POST["biz"]
        prospect_type = request.POST["prospect-type"]


        # CHECK FOR DR
        if "Dr" in full_name or "Dr." in full_name:
            first_name = full_name.split(' ', 2)
            first_name = first_name[0] + ' ' + first_name[2]
        else:
            first_name = full_name.split(' ', 1)
            first_name = first_name[0]
        # get date
        date = datetime.now()

        generated = True

        # create an object of the POST input
        new_lead = LeadPDF.objects.create(
                    generated=generated,
                    date=date,
                    full_name=full_name,
                    first_name=first_name,
                    biz_name=biz_name
                )

        if prospect_type == 'scorecard':
            pdfkit.from_url('http://127.0.0.1:8000/scorecard-pdf/' + str(new_lead.id),  'pdfs/test.pdf')
        elif prospect_type == 'sponsor':
            pdfkit.from_url('http://127.0.0.1:8000/sponsor-pdf/' + str(new_lead.id),  'pdfs/test.pdf')

        input_pdf = PdfFileReader('pdfs/test.pdf')
        last_page = input_pdf.getPage(0)

        # CROP TO SIZE
        last_page.mediaBox.lowerRight = (611, 400)
        last_page.mediaBox.lowerLeft = (0, 100)
        last_page.mediaBox.upperRight = (611, 700)
        last_page.mediaBox.upperLeft = (0, 850)


        pdf_writer = PdfFileWriter()
        pdf_writer.addPage(last_page)

        with Path("pdfs/last_page.pdf").open(mode="wb") as output_file:
            pdf_writer.write(output_file)

        # merge pdfs
        report_dir = (
            Path.home()
            / "Desktop"
            / "ScorecardsCRM"
            )

        if prospect_type == 'scorecard':
            report_path = report_dir / "scorecard-media-kit.pdf"
        elif prospect_type == 'sponsor':
            report_path = report_dir / "sponsor-media-kit.pdf"

        toc_path = report_dir / "pdfs/last_page.pdf"

        pdf_merger = PdfFileMerger()
        pdf_merger.append(str(report_path))

        pdf_merger.merge(0, str(toc_path))

        with Path("pdfs/" + new_lead.biz_name + ".pdf").open(mode="wb") as output_file:
            pdf_merger.write(output_file)

        return render(request, 'salesmgr/proposal-form.html', {})

    return render(request, 'salesmgr/proposal-form.html', {})



@user_passes_test(lambda u: u.is_superuser)
def csv_proposals(request):
    if request.method == "POST":
        csv_file = request.FILES["csv_file"]
        prospect_type = request.POST["prospect-type"]

        file_data = csv_file.read().decode("utf-8")
        lines = file_data.split("\n")
        # loop over the lines and save them in db. If error , store as string and then display
        for line in lines:
            fields = line.split(",")
            if line:
                full_name = fields[0]
                biz_name = fields[1]

                # CHECK FOR DR
                if "Dr" in full_name or "Dr." in full_name:
                    first_name = full_name.split(' ', 2)
                    first_name = first_name[0] + ' ' + first_name[2]
                else:
                    first_name = full_name.split(' ', 1)
                    first_name = first_name[0]

                # get date
                date = datetime.now()

                generated = True

                # create an object of the POST input
                new_lead = LeadPDF.objects.create(
                            generated=generated,
                            date=date,
                            full_name=full_name,
                            first_name=first_name,
                            biz_name=biz_name
                        )

                if prospect_type == 'scorecard':
                    pdfkit.from_url('http://127.0.0.1:8000/scorecard-pdf/' + str(new_lead.id),  'pdfs/test.pdf')
                elif prospect_type == 'sponsor':
                    pdfkit.from_url('http://127.0.0.1:8000/sponsor-pdf/' + str(new_lead.id),  'pdfs/test.pdf')

                input_pdf = PdfFileReader('pdfs/test.pdf')
                last_page = input_pdf.getPage(0)

                # CROP TO SIZE
                last_page.mediaBox.lowerRight = (611, 400)
                last_page.mediaBox.lowerLeft = (0, 100)
                last_page.mediaBox.upperRight = (611, 700)
                last_page.mediaBox.upperLeft = (0, 850)


                pdf_writer = PdfFileWriter()
                pdf_writer.addPage(last_page)

                with Path("pdfs/last_page.pdf").open(mode="wb") as output_file:
                    pdf_writer.write(output_file)

                # merge pdfs
                report_dir = (
                    Path.home()
                    / "Desktop"
                    / "ScorecardsCRM"
                    )

                if prospect_type == 'scorecard':
                    report_path = report_dir / "scorecard-media-kit.pdf"
                elif prospect_type == 'sponsor':
                    report_path = report_dir / "sponsor-media-kit.pdf"

                toc_path = report_dir / "pdfs/last_page.pdf"

                pdf_merger = PdfFileMerger()
                pdf_merger.append(str(report_path))

                pdf_merger.merge(0, str(toc_path))

                name = new_lead.biz_name

                with Path("pdfs/" + name + ".pdf").open(mode="wb") as output_file:
                    pdf_merger.write(output_file)

        return render(request, 'salesmgr/proposal-form.html', {})

    return render(request, 'salesmgr/proposal-form.html', {})
