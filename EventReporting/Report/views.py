from django.shortcuts import render
from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages 

from django.core.mail import send_mail, EmailMessage
from django.conf import settings

from smtplib import SMTPException
from datetime import datetime
from .forms import incidentForm, editReportForm
from .models import IncidentReport

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from io import BytesIO
import os
import textwrap

from django.core import mail
from django.core.mail.backends.smtp import EmailBackend




def selectCoordinatorEmail(incident):
    email = " "
    location = incident.Location
    print(location)
    if location == "Atlanta":
        email = "Stephanie.Draper@northside.com"
    elif location == "Cherokee":
        email = "Michelle.Orlando@northside.com"
    elif location == "Alpharetta":
        email = "Linda.Hilton@northside.com"
    elif location == "Forsyth":
        email = "Tiffany.Armour@northside.com"
    elif location == "Duluth Hwy" or location == "Phillip Blvd" or location == "Gwinnett":
        email = "Gary.Thomas@northside.com"
   
    elif location == "Preston Ridge":
        email = "Faith.Dupree@northside.com"
    elif location == "Midtown":
        email = "Keith.Turner@northside.com"
    elif location == "Macon":
        email = "MRUGESH.PATEL@northside.com"
    elif location == "Lake Oconee":
        email = "Ashley.Davis2@northside.com"

    elif location == "South Atlanta" or location == "Hawkinsville":
        email = "Eva.Turner@northside.com"
    return email

def addReport(request):
    
    if request.method == "POST":
        form = incidentForm(request.POST or None)

        if form.is_valid():
            incident = form.save()
            messages.success(request, ('Item has been Added to the list!'))
            print('send mail')

            connection = mail.get_connection()
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
            email.send()
            print('mail sent')
            createPDF(incident)
            
            
            incident.delete()
            return render(request, 'reportSuccess.html', {})
        else:
            messages.error(request, "Error")
            return render(request, 'report.html', {'errors': form.errors})

    else:
        return render(request, 'report.html', {})

def showSingleReport(request, report_id):
    if request.method == "GET":
        showReport = IncidentReport.objects.get(pk = report_id)
        return render(request, 'showSingleReport.html', {'report':showReport})


def showReports(request):
    orderBy = request.GET.get('order_by', '-ReportDate')
    reports = IncidentReport.objects.all().order_by(orderBy)
    return render(request, 'showReports.html', {'reports':reports})

def deleteReport(request, report_id):
    deleteReport = IncidentReport.objects.get(pk = report_id)
    deleteReport.delete()
    requests = IncidentReport.objects.all
    return redirect('showReports')


def editReport(request, report_id):
    if request.method == "POST":
        report = IncidentReport.objects.get(pk = report_id)
        form = editReportForm(request.POST or None, instance=report)
        print(form.errors)
        if form.is_valid():
            
            messages.success(request, ('Item has been Edited'))
           
            temReq = form.save()

            requests = list(IncidentReport.objects.all())
            
            return redirect('showReports')
        else:
           
            print("Farts")
            messages.error(request, "Error")
            requests = IncidentReport.objects.all()
            return redirect('showReports')
           
    else:
        
        report = IncidentReport.objects.get(pk = report_id)
        print(report.Name)
        return render(request, 'editReport.html', {'report':report})



def loginUser(request):
    if request.method == 'POST':
        password = request.POST.get("password")
        username = request.POST.get("username")
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            messages.success(request, ('Login Successful'))
            return redirect(showReports)
            
        else:
            storage = messages.get_messages(request)
            storage.used = True


            messages.error(request, ('Incorrect login credentials'))
            return render(request, 'login.html')

    else:
        
        return render(request, 'login.html', {})
    
def logoutUser(request):
    logout(request)
    messages.success(request, ('You have Been Logged Out'))
    return redirect('login')



def createPDF(incident):
     
        # Define the directory where PDFs will be saved

        #pdf_directory = 'C:\PDF' #'P:\\Outpatient Oncology\\DOSIMETRY-PHYSICS\\SJC\\reports'


        pdf_directory =  'P:\\Outpatient Oncology\\DOSIMETRY - PHYSICS\\SJC\\reports'

        #if not os.path.exists(pdf_directory):
           # os.makedirs(pdf_directory)  # Create the directory if it doesn't exist
        #buffer = BytesIO()
        # Create a file path for the PDF
        pdf_file_path = os.path.join(pdf_directory, f"incident_{incident.id}.pdf")
        
        # Create the PDF
        c = canvas.Canvas(pdf_file_path, pagesize=letter)
        
        # Register a custom font if desired
        #pdfmetrics.registerFont(TTFont('Roboto', 'path/to/Roboto-Regular.ttf'))
        
        # Write content to PDF (Same as before)
        c.setFont("Helvetica", 16)
        c.drawString(220, 750, f"Incident Report # {incident.id}")
        
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

        

        

