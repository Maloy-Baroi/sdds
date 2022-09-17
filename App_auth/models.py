from re import T
from django.db import models
from django.contrib.auth.models import User
from django_mysql.models import ListCharField


# Create your models here.
genders = (
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Third Gender', 'Third Gender')
)

class MedicalProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    sex = models.CharField(max_length=100, choices=genders)
    past_medical_history = ListCharField(base_field=models.CharField(max_length=50), size=7, max_length=(7 * 51))
    hyper_tension = models.BooleanField(default=False)
    diabetics = models.BooleanField(default=False)
    asthma = models.BooleanField(default=False)
    smoking = models.BooleanField(default=False)
    Alchohol = models.BooleanField(default=False)
    address = models.CharField(max_length=255)
    height = models.CharField(max_length=20, blank=True)
    weight = models.CharField(max_length=20, blank=True)
    bmi = models.CharField(max_length=10, blank=True)
    profile_picture = models.ImageField(upload_to='patient_profile_picture/')

    def __str__(self):
        return f"{self.full_name}"


class Patient_Tested_Results(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patient_uploaded_images')
    covid_19 = models.ImageField(upload_to='patient_covid_19/', blank=True, null=True)
    covid_19_result = models.CharField(max_length=20, default=False)
    heart_disease = models.BooleanField(default=False, null=True, blank=True)
    brain_tumor = models.ImageField(upload_to='brain_tumor/', blank=True, null=True)
    brain_tumor_result = models.CharField(max_length=20, default=False)

