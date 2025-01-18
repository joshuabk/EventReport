from django import forms
from .models import IncidentReport
from datetime import datetime


class incidentForm(forms.ModelForm):
    
    class Meta:
        model = IncidentReport
        fields= ["Name", "TeamMember","Location",  "IncidentDate", "PatientName", "PatientMRN","IncidentType","StageOfCatch", "IncidentDescription" ]
    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['Name'].required = False



class editReportForm(forms.ModelForm):
    

    class Meta:
        model = IncidentReport
        fields= ["Name", "TeamMember", "Location", "IncidentDate", "PatientName", "PatientMRN", "IncidentType", "StageOfCatch", "IncidentDescription" ]
    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['Name'].required = False