# Generated by Django 4.0.4 on 2022-09-02 10:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_mysql.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MedicalProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=100)),
                ('date_of_birth', models.DateField()),
                ('sex', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Third Gender', 'Third Gender')], max_length=100)),
                ('past_medical_history', django_mysql.models.ListCharField(models.CharField(max_length=50), max_length=357, size=7)),
                ('hyper_tension', models.BooleanField(default=False)),
                ('diabetics', models.BooleanField(default=False)),
                ('asthma', models.BooleanField(default=False)),
                ('smoking', models.BooleanField(default=False)),
                ('Alchohol', models.BooleanField(default=False)),
                ('address', models.CharField(max_length=255)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
