from django.shortcuts import render
from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.utils.http import url_has_allowed_host_and_scheme

from django.contrib import messages 

from django.core.mail import send_mail, EmailMessage
from django.conf import settings

from smtplib import SMTPException
from datetime import datetime
from .forms import incidentForm, editReportForm
from .models import IncidentReport, ActivityLog

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from io import BytesIO
import os
import textwrap
from django.contrib.auth.models import User
from django.core import mail
from django.core.mail.backends.smtp import EmailBackend

#admin user: nowthsideadmin  pass:R3port2!
# user: northside   pass:R3port2!


def selectCoordinatorEmail(incident):
    email = " "
    location = incident.Location
    print(location)
    
    if location == "Atlanta":
        email = "Stephanie.Draper@northside.com"
    elif location == "Cherokee":
        email = "Michelle.Orlando@northside.com"
    elif location == "Alpharetta":
        email = "Darlene.Ritarita@northside.com"
    elif location == "Forsyth":
        email = "Tiffany.Armour@northside.com"
    elif location == "Duluth Hwy" or location == "Phillip Blvd" or location == "Gwinnett":
        email = "Gary.Thomas@northside.com"
   
    elif location == "Preston Ridge":
        email = "Darlene.Ritarita@northside.com"
    elif location == "Midtown":
        email = "Keith.Turner@northside.com"
    elif location == "Macon":
        email = "MRUGESH.PATEL@northside.com"
    elif location == "South Atlanta" or location == "Lake Oconee":
        email = "Ashley.Davis2@northside.com"

    elif location == "Hawkinsville":
        email = "Eva.Turner@northside.com"
    
    elif location == "Blairsville":
        email = "Chandra.Dockery@northside.com"
    elif location == "Conyers":
        email = "Chiquita.White@northside.com"
    elif location == "Covington":
        email = "Jane.Burgos@northside.com"
    elif location == "Decatur":
        email = "Amy.Cantrell2@northside.com"
    elif location == "Snellville":
        email = "Cynthia.Nixon@northside.com"

    return email


def _client_ip(request):
    forwarded = request.META.get("HTTP_X_FORWARDED_FOR")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")


def _comparable(value):
    """Normalise a field value so before/after comparisons ignore date-vs-datetime and None-vs-'' noise."""
    if hasattr(value, "date") and callable(value.date):
        return value.date()
    return value if value not in (None, "") else ""


def log_activity(request, action, report=None, details="", username=None):
    """Write one ActivityLog row. Never lets a logging failure break the page."""
    try:
        user = request.user if request.user.is_authenticated else None
        ActivityLog.objects.create(
            user=user,
            username=username if username is not None else (user.get_username() if user else ""),
            action=action,
            report_id=report.pk if report is not None else None,
            details=details[:500],
            ip_address=_client_ip(request),
        )
    except Exception as exc:  # pragma: no cover
        print(f"activity log failed: {exc}")


def addReport(request):
    
    if request.method == "POST":
        form = incidentForm(request.POST or None)

        if form.is_valid():
            incident = form.save()
            log_activity(request, "REPORT_ADDED", report=incident,
                         details=f"Location={incident.Location}; Reporter={incident.Name}; Type={incident.IncidentType}")
            print('send mail')

            '''connection = mail.get_connection()
            print(connection)
            if isinstance(connection, EmailBackend):
                connection.open()
                print("connection is open")
             
            

            Cemail = selectCoordinatorEmail(incident)

            body = 'A new event report has been submitted for '+ incident.Location 
            

            print(body)
            email = EmailMessage(
                  'New Event Report',
                   body,
                    settings.EMAIL_HOST_USER,
                   ['Chante.Frazier@northside.com','Sarah.Castillo@northside.com', Cemail])
            
            #email.attach(f"Incident_{incident.id}.pdf", pdf_content, 'application/pdf')
            #email.send()
            print('mail sent')'''
            #createPDF(incident)
            
            
            #incident.delete()
            return render(request, 'reportSuccess.html', {})
        else:
            return render(request, 'report.html', {'errors': form.errors})

    else:
        return render(request, 'report.html', {})

@login_required
def showSingleReport(request, report_id):
    if request.method == "GET":
        showReport = IncidentReport.objects.get(pk = report_id)
        log_activity(request, "REPORT_VIEWED", report=showReport)
        return render(request, 'showSingleReport.html', {'report':showReport})


SORT_COLUMNS = [
    ("id", "ID"),
    ("Name", "Reporter"),
    ("TeamMember", "Role"),
    ("Location", "Location"),
    ("IncidentDate", "Event Date"),
    ("ReportDate", "Submitted"),
    ("IncidentType", "Type"),
]


@login_required
def showReports(request):
    orderBy = request.GET.get('order_by', '-ReportDate')
    allowed = {k for k, _ in SORT_COLUMNS}
    if orderBy.lstrip('-') not in allowed:   # ignore anything that is not a real sortable column
        orderBy = '-ReportDate'
    reports = IncidentReport.objects.all().order_by(orderBy)
    return render(request, 'showReports.html', {
        'reports': reports,
        'order_by': orderBy,
        'sort_columns': SORT_COLUMNS,
    })

@login_required
@require_POST
def deleteReport(request, report_id):
    deleteReport = IncidentReport.objects.get(pk = report_id)
    log_activity(request, "REPORT_DELETED", report=deleteReport,
                 details=f"Location={deleteReport.Location}; Reporter={deleteReport.Name}; "
                         f"EventDate={deleteReport.IncidentDate:%m-%d-%Y}; Type={deleteReport.IncidentType}")
    deleteReport.delete()
    requests = IncidentReport.objects.all
    return redirect('showReports')


@login_required
def editReport(request, report_id):
    if request.method == "POST":
        report = IncidentReport.objects.get(pk = report_id)
        before = {f: _comparable(getattr(report, f)) for f in editReportForm.Meta.fields}
        form = editReportForm(request.POST or None, instance=report)
        if form.is_valid():
            temReq = form.save()
            changed = [f for f in editReportForm.Meta.fields if _comparable(getattr(temReq, f)) != before[f]]
            log_activity(request, "REPORT_EDITED", report=temReq,
                         details=("Changed: " + ", ".join(changed)) if changed else "No field changes")
            messages.success(request, f'Report #{report_id} has been updated.')
            return redirect('showReports')
        else:
           
            messages.error(request, "The report could not be saved. Please check the highlighted fields.")
            return render(request, 'editReport.html', {'report': report, 'errors': form.errors})
           
    else:
        
        report = IncidentReport.objects.get(pk = report_id)
        return render(request, 'editReport.html', {'report':report})



def loginUser(request):
    if request.method == 'POST':
        password = request.POST.get("password")
        username = request.POST.get("username")
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            log_activity(request, "LOGIN")
            messages.success(request, 'Signed in successfully.')
            next_url = request.GET.get('next') or request.POST.get('next')
            if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
                return redirect(next_url)
            return redirect('showReports')
            
        else:
            storage = messages.get_messages(request)
            storage.used = True

            log_activity(request, "LOGIN_FAILED", username=username or "", details="Incorrect credentials")
            messages.error(request, 'Incorrect username or password.')
            return render(request, 'login.html')

    else:
        
        return render(request, 'login.html', {})
    
def logoutUser(request):
    log_activity(request, "LOGOUT")
    logout(request)
    messages.success(request, 'You have been signed out.')
    return redirect('login')



@login_required
def activityLog(request):
    logs = ActivityLog.objects.select_related("user")[:500]
    return render(request, 'activityLog.html', {'logs': logs})


def createPDF(incident):
     
        # Define the directory where PDFs will be saved

        #pdf_directory = 'C:\PDF' #'P:\\Outpatient Oncology\\DOSIMETRY-PHYSICS\\SJC\\reports'


        pdf_directory =  'P:\\Outpatient Oncology\\DOSIMETRY - PHYSICS\\SJC\\reports'

        #if not os.path.exists(pdf_directory):
           # os.makedirs(pdf_directory)  # Create the directory if it doesn't exist
        #buffer = BytesIO()
        # Create a file path for the PDF
        pdf_file_path = os.path.join(pdf_directory, f"Event_Report_{incident.id}.pdf")
        
        # Create the PDF
        c = canvas.Canvas(pdf_file_path, pagesize=letter)
        
        # Register a custom font if desired
        #pdfmetrics.registerFont(TTFont('Roboto', 'path/to/Roboto-Regular.ttf'))
        
        # Write content to PDF (Same as before)
        c.setFont("Helvetica", 16)
        c.drawString(220, 750, f"Event Report # {incident.id}")
        
        c.setFont("Helvetica", 12)
        c.drawString(50, 720, f"Report Date: {incident.ReportDate.strftime('%m-%d-%Y %H:%M')}")
        c.drawString(50, 700, f"Event Date: {incident.IncidentDate.strftime('%m-%d-%Y')}")
        c.drawString(50, 680, f"Reporter: {incident.Name}")
        c.drawString(50, 660, f"Team Member: {incident.TeamMember}")
        c.drawString(50, 640, f"Location: {incident.Location}")
        c.drawString(50, 620, f"Patient Initials: {incident.PatientName}")
        c.drawString(50, 600, f"Patient MRN: {incident.PatientMRN}")
        c.drawString(50, 580, f"Type: {incident.IncidentType}")
        c.drawString(50, 560, f"Stage Caught: {incident.StageOfCatch}")
        c.drawString(50, 525, f"Description:" )
        
        c.setFont("Helvetica", 12)
        y_pos = 505
        lines =  textwrap.wrap(incident.IncidentDescription, width=95)
        for line in lines:
            c.drawString(50, y_pos, line)
            y_pos -= 15
        
        # Save the PDF
        c.save()

        

        

