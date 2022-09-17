from django.urls import path
from App_main.views import *


app_name = 'App_main'


urlpatterns = [
    path('', home, name='home'),
    path('bmi-calculator/', bmi_calculator, name='bmi-calculator'),
    path('covid-19/', covid_19, name='covid-19'),
    path('covid-19-predict-by-image/', covid_19_predict_by_image, name='covid-19-predict-by-image'),
    path('covid-19-predict-by-image-prediction/', covid_19_predict_by_image_predict, name='covid-19-predict-by-image-prediction'),
    # path('covid-19-predict/', covid_19_predict, name='covid-19-predict'),
    path('brain-tumor/', brain_tumor, name='brain-tumor'),
    path('brain-tumor-more-specifically/', brain_tumor_more_specifically, name='brain-tumor-more-specifically'),
    path('brain-tumor-more-specifically-predictions/', brain_tumor_more_specifically_predictions, name='brain-tumor-more-specifically-predictions'),
    path('heart-disease/', heart_disease, name='heart-disease'),
    path('heart-disease-detector-better-page/', heart_disease_detector_better_page, name='heart-disease-detector-better-page'),
    path('heart-disease-detector/', heartDiseaseDetection, name='heart-disease-detector'),
    path('heart-disease-detector-better/', heart_disease_detector_better, name='heart-disease-detector-better'),
    path('kidney-disease/', kidney_disease_detect, name='kidney-disease'),

    # Profile setup
    path('profile-setup', profile_setup, name='profile-setup'),
    path('profile/', profile_, name='profile'),
]

