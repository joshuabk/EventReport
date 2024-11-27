from django import forms
from .models import IncidentReport
from datetime import datetime


class incidentForm(forms.ModelForm):
    
    class Meta:
        model = IncidentReport
        fields= ["Name", "Location",  "IncidentDate", "PatientName", "PatientMRN","IncidentType", "IncidentDescription" ]



class editReportForm(forms.ModelForm):
    

    class Meta:
        model = IncidentReport
        fields= ["Name", "Location", "IncidentDate", "PatientName", "PatientMRN", "IncidentType", "IncidentDescription" ]