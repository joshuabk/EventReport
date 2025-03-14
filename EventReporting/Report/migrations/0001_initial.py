# Generated by Django 5.0.3 on 2024-11-25 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="IncidentReport",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("Name", models.CharField(max_length=25, null=True)),
                ("Location", models.CharField(max_length=300, null=True)),
                ("ReportDate", models.DateTimeField(auto_now_add=True)),
                ("IncidentDate", models.DateTimeField()),
                ("PatientName", models.CharField(default="", max_length=30)),
                ("PatientMRN", models.CharField(default="", max_length=30)),
                ("IncidentType", models.CharField(default="", max_length=30)),
                ("IncidentDescription", models.CharField(default="", max_length=300)),
            ],
        ),
    ]
