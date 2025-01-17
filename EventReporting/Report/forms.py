from django import forms
from .models import IncidentReport
from datetime import datetime


class incidentForm(forms.ModelForm):
    
    class Meta:
        model = IncidentReport
        fields= ["Name", "TeamMember","Location",  "IncidentDate", "PatientName", "PatientMRN","IncidentType","StageOfCatch", "IncidentDescription" ]



class editReportForm(forms.ModelForm):
    

    class Meta:
        model = IncidentReport
        fields= ["Name", "TeamMember", "Location", "IncidentDate", "PatientName", "PatientMRN", "IncidentType", "StageOfCatch", "IncidentDescription" ]