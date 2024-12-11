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



def addReport(request):
    
    if request.method == "POST":
        form = incidentForm(request.POST or None)

        if form.is_valid():
            incident = form.save()
            messages.success(request, ('Item has been Added to the list!'))
            print('send mail')

            connection = mail.get_connection()
            print(connection)
            '''if isinstance(connection, EmailBackend):
                connection.open()
                print("connection is open")'''
             
           
            ''' body = 'The new request from '+ request.POST.get('Name')+' is as follows: \n\n EMR System: '+  request.POST.get('EMRSystem')+'\n \n Request: '+ request.POST.get('Request')+'  \n\n Reason: '+ request.POST.get('Reason')+'\n\n Priority: '+  request.POST.get('Priority')+'\n\n Impact: '+  request.POST.get('Impact') +'\n\nHere is the link to the EMR Request page http://10.40.71.201:2000/'  
            
            print(body)
            email = EmailMessage(
                  'New EMR Change Request',
                   body,
                    settings.EMAIL_HOST_USER,
                   ['joshua.kessler@northside.com', 'RadiationOncologyEMR@northside.com',])
            

            #email.send()
            print('mail sent')'''
            
            createPDF(incident)
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
        pdf_directory = 'P:\\Outpatient Oncology\\17-INCIDENT LEARNING REPORT'
        if not os.path.exists(pdf_directory):
            os.makedirs(pdf_directory)  # Create the directory if it doesn't exist

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
        c.drawString(50, 720, f"Report Date: {incident.ReportDate.strftime('%Y-%m-%d %H:%M')}")
        c.drawString(50, 700, f"Incident Date: {incident.IncidentDate.strftime('%Y-%m-%d %H:%M')}")
        c.drawString(50, 680, f"Reporter: {incident.Name}")
        c.drawString(50, 660, f"Location: {incident.Location}")
        c.drawString(50, 640, f"Patient Initials: {incident.PatientName}")
        c.drawString(50, 620, f"Patient MRN: {incident.PatientMRN}")
        c.drawString(50, 600, f"Type: {incident.IncidentType}")
        c.drawString(50, 565, f"Description:" )
        
        c.setFont("Helvetica", 12)
        y_pos = 545
        lines =  textwrap.wrap(incident.IncidentDescription, width=95)
        for line in lines:
            c.drawString(50, y_pos, line)
            y_pos -= 15
        
        # Save the PDF
        c.save()
