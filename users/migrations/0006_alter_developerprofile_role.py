# Generated by Django 5.0.2 on 2024-03-02 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_developerprofile_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='developerprofile',
            name='role',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
