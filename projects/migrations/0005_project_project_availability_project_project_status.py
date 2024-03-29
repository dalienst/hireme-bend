# Generated by Django 5.0.2 on 2024-02-16 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0004_bid_file"),
    ]

    operations = [
        migrations.AddField(
            model_name="project",
            name="project_availability",
            field=models.CharField(
                choices=[("A", "Available"), ("N", "Not Available")],
                default="A",
                max_length=1,
            ),
        ),
        migrations.AddField(
            model_name="project",
            name="project_status",
            field=models.CharField(
                choices=[("P", "Pending"), ("A", "Active"), ("C", "Completed")],
                default="P",
                max_length=1,
            ),
        ),
    ]
