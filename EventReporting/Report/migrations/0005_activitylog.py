from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("Report", "0004_alter_incidentreport_stageofcatch"),
    ]

    operations = [
        migrations.CreateModel(
            name="ActivityLog",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("timestamp", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("username", models.CharField(blank=True, default="", max_length=150)),
                ("action", models.CharField(choices=[("REPORT_ADDED", "Report added"), ("REPORT_EDITED", "Report edited"), ("REPORT_DELETED", "Report deleted"), ("REPORT_VIEWED", "Report viewed"), ("LOGIN", "Login"), ("LOGIN_FAILED", "Login failed"), ("LOGOUT", "Logout")], db_index=True, max_length=30)),
                ("report_id", models.IntegerField(blank=True, null=True)),
                ("details", models.CharField(blank=True, default="", max_length=500)),
                ("ip_address", models.GenericIPAddressField(blank=True, null=True)),
                ("user", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="activity_logs", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ["-timestamp"]},
        ),
    ]
