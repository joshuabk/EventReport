from django.db import models
from django.conf import settings

# Create your models here.


class IncidentReport(models.Model):
    Name = models.CharField(max_length=25, null = True)
    TeamMember = models.CharField(max_length=25, null = True)
    
   
    Location = models.CharField(max_length=300, null = False, default = " ")
    ReportDate = models.DateTimeField(auto_now_add=True)
    
    IncidentDate = models.DateTimeField(auto_now_add=False)
    PatientName = models.CharField(max_length=30, default = '')
    PatientMRN = models.CharField(max_length=30, default = '')
    IncidentType = models.CharField(max_length=30, default = '')
    StageOfCatch = models.CharField(max_length=35, null = True, blank = True)
    IncidentDescription  =  models.CharField(max_length=300)

    def __str__(self):
        return self.IncidentReport


class ActivityLog(models.Model):
    """One row per notable action on the site (add/edit/delete/view a report, login/logout)."""
    ACTIONS = [
        ("REPORT_ADDED", "Report added"),
        ("REPORT_EDITED", "Report edited"),
        ("REPORT_DELETED", "Report deleted"),
        ("REPORT_VIEWED", "Report viewed"),
        ("LOGIN", "Login"),
        ("LOGIN_FAILED", "Login failed"),
        ("LOGOUT", "Logout"),
    ]

    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True,
                             on_delete=models.SET_NULL, related_name="activity_logs")
    username = models.CharField(max_length=150, blank=True, default="")  # kept even if the user is deleted / login failed
    action = models.CharField(max_length=30, choices=ACTIONS, db_index=True)
    report_id = models.IntegerField(null=True, blank=True)  # not a FK so the row survives report deletion
    details = models.CharField(max_length=500, blank=True, default="")
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return f"{self.timestamp:%Y-%m-%d %H:%M} {self.username or 'anonymous'} {self.action}"
