from django import forms
from .models import IncidentReport

# Fields that may be left blank: anonymous reports, and events that are not
# tied to a specific patient (e.g. Unsafe Condition, Process Improvement).
OPTIONAL_FIELDS = ["Name", "TeamMember", "PatientName", "PatientMRN", "StageOfCatch"]


class incidentForm(forms.ModelForm):
    class Meta:
        model = IncidentReport
        fields = ["Name", "TeamMember", "Location", "IncidentDate", "PatientName", "PatientMRN",
                  "IncidentType", "StageOfCatch", "IncidentDescription"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in OPTIONAL_FIELDS:
            self.fields[f].required = False


class editReportForm(forms.ModelForm):
    class Meta:
        model = IncidentReport
        fields = ["Name", "TeamMember", "Location", "IncidentDate", "PatientName", "PatientMRN",
                  "IncidentType", "StageOfCatch", "IncidentDescription"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in OPTIONAL_FIELDS:
            self.fields[f].required = False
