from django.db import models

# Create your models here.


class IncidentReport(models.Model):
    Name = models.CharField(max_length=25, null = True)
   
    Location = models.CharField(max_length=300, null = True)
    ReportDate = models.DateTimeField(auto_now_add=True)
    
    IncidentDate = models.DateTimeField(auto_now_add=False)
    PatientName = models.CharField(max_length=30, default = '')
    PatientMRN = models.CharField(max_length=30, default = '')
    IncidentType = models.CharField(max_length=30, default = '')
    IncidentDescription  =  models.CharField(max_length=300, default = 'wrong patient')

    def __str__(self):
        return self.IncidentReport