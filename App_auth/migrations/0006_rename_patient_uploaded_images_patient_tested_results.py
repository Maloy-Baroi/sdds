# Generated by Django 4.0.4 on 2022-09-17 18:21

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('App_auth', '0005_patient_uploaded_images_brain_tumor_result_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Patient_Uploaded_Images',
            new_name='Patient_Tested_Results',
        ),
    ]