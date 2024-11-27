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

from django.core import mail
from django.core.mail.backends.smtp import EmailBackend





def addReport(request):
    
    if request.method == "POST":
        form = incidentForm(request.POST or None)

        if form.is_valid():
            form.save()
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

            
            return render(request, 'reportSuccess.html', {})
        else:
            messages.error(request, "Error")
            return render(request, 'report.html', {'errors': form.errors})

    else:
        return render(request, 'report.html', {})

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
            messages.success(request, ('Error, please try again'))
            return redirect('login')

    else:
        
        return render(request, 'login.html', {})
    
def logoutUser(request):
    logout(request)
    messages.success(request, ('You have Been Logged Out'))
    return redirect('login')