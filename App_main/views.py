import importlib
from urllib import request
from django.shortcuts import render, reverse
import pickle
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
import numpy as np
from django.contrib.auth.decorators import login_required
from App_auth.models import *
from datetime import date
import joblib
from keras.models import load_model
from PIL import Image, ImageOps
import numpy as np
from django.core.files.storage import FileSystemStorage


# Create your views here.
@login_required
def home(request):
    return render(request, 'App_main/dashboard.html')


def bmi_calculator(request):
    if request.method == 'POST':
        print(request.POST.get('height'))
        print(request.POST.get('weight'))
        ft = float(request.POST.get('height'))
        weight_in_kg = float(request.POST.get('weight'))
        height_in_meter = ft * 0.3048
        bmi = weight_in_kg / (height_in_meter ** 2)
        profile = MedicalProfile.objects.get(user=request.user)
        profile.height = height_in_meter
        profile.weight = weight_in_kg
        profile.bmi = str(bmi)[:6]
        profile.save()
        return JsonResponse({"bmi": str(bmi)[:6]})


def covid_19(request):
    return render(request, 'App_main/covid_19.html')


def covid_19_predict_by_image(request):
    patientTestedResult = Patient_Tested_Results.objects.get(user=request.user)
    content = {
        'patientTestedResult': patientTestedResult,
    }
    return render(request, 'App_main/covid_19_predict_by_image.html', context=content)


def covid_19_predict_by_image_predict(request):
    # Load the model
    model = load_model('App_main/models/converted_keras_covid_19/keras_model.h5')

    # Create the array of the right shape to feed into the keras model
    # The 'length' or number of images you can put into the array is
    # determined by the first position in the shape tuple, in this case 1.
    if request.method == 'POST':
        image_get = request.FILES.get('xray_image')
        profile = Patient_Tested_Results.objects.get(user=request.user)
        profile.covid_19 = image_get

        data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
        # Replace this with the path to your image
        fileObj = request.FILES.get('xray_image')
        print(fileObj)
        fs = FileSystemStorage()
        filePathName = fs.save(fileObj.name, fileObj)
        filePathName = fs.url(filePathName)
        testImage = '.'+filePathName
        # image_to_predict = Image.open(testImage)

        data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
        # Replace this with the path to your image
        image = Image.open(testImage).convert('RGB')
        #resize the image to a 224x224 with the same strategy as in TM2:
        #resizing the image to be at least 224x224 and then cropping from the center
        size = (224, 224)
        image = ImageOps.fit(image, size, Image.ANTIALIAS)

        #turn the image into a numpy array
        image_array = np.asarray(image)
        # Normalize the image
        normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1

        # Load the image into the array
        data[0] = normalized_image_array

        # run the inference
        prediction = model.predict(data)
        print(prediction)

        if prediction[0][1]*10 > 7.5 or int(prediction[0][1]*10) > 75:
            predicted_result = 'Positive'
        else:
            predicted_result = 'Negative'
        
        profile.covid_19_result = predicted_result
        profile.save()
        print(predicted_result)
        # return HttpResponse(prediction[0][0])
        return HttpResponseRedirect(reverse('App_main:covid-19-predict-by-image'))


# Previous versions of prediction
# def covid_19_predict(request):
#     if request.method == 'POST':
#         image_get = request.FILES.get('xray-image')
#         data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
#         # Replace this with the path to your image
#         fileObj = request.FILES.get('xray-image')
#         fs = FileSystemStorage()
#         filePathName = fs.save(fileObj.name, fileObj)
#         filePathName = fs.url(filePathName)
#         testImage = '.'+filePathName
#         image_to_predict = Image.open(testImage)
#         # resize the image to a 224x224 with the same strategy as in TM2:
#         # resizing the image to be at least 224x224 and then cropping from the center
#         size = (224, 224)
#         new_image = ImageOps.fit(image_to_predict, size, Image.ANTIALIAS)

#         # turn the image into a numpy array
#         image_array = np.asarray(new_image)
#         # image_array = np.array(new_image)
#         # Normalize the image
#         normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
#         report = str(" ")
#         percentage = float(0)
#         # Load the image into the array
#         try:
#             data[0] = normalized_image_array
#             # run the inference
#             prediction = covid_19_model.predict(data)
#             if float(prediction[0][0]) >= float(prediction[0][1]):
#                 report = "Covid-19 Negative"
#                 percentage = float(prediction[0][0])
#             else:
#                 report = "Covid-19 Positive"
#                 percentage = float(prediction[0][1])
#             return zip([report], [percentage])
#         except Exception as e:
#             report = "Result is not so sure, due to your image quality."
#             percentage = 0.00
#         print(report)
#         return HttpResponse({zip([report], [percentage])})


def brain_tumor(request):
    return render(request, 'App_main/brain-tumor.html')

def brain_tumor_more_specifically(request):
    patientTestedResult = Patient_Tested_Results.objects.get(user=request.user)
    content = {
        'patientTestedResult': patientTestedResult
    }
    return render(request, 'App_main/brain-tumor-more-specifically.html', context=content)


def brain_tumor_more_specifically_predictions(request):
    # Load the model
    model = load_model('App_main/models/converted_keras_brain_tumor/keras_model.h5')

    # Create the array of the right shape to feed into the keras model
    # The 'length' or number of images you can put into the array is
    # determined by the first position in the shape tuple, in this case 1.
    if request.method == 'POST':
        image_get = request.FILES.get('mri_image')
        profile = Patient_Tested_Results.objects.get(user=request.user)
        profile.brain_tumor = image_get

        data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
        # Replace this with the path to your image
        fileObj = request.FILES.get('mri_image')
        print(fileObj)
        fs = FileSystemStorage()
        filePathName = fs.save(fileObj.name, fileObj)
        filePathName = fs.url(filePathName)
        testImage = '.'+filePathName
        # image_to_predict = Image.open(testImage)

        data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
        # Replace this with the path to your image
        image = Image.open(testImage).convert('RGB')
        #resize the image to a 224x224 with the same strategy as in TM2:
        #resizing the image to be at least 224x224 and then cropping from the center
        size = (224, 224)
        image = ImageOps.fit(image, size, Image.ANTIALIAS)

        #turn the image into a numpy array
        image_array = np.asarray(image)
        # Normalize the image
        normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1

        # Load the image into the array
        data[0] = normalized_image_array

        # run the inference
        prediction = model.predict(data)
        print(prediction)

        if prediction[0][1]*10 > 7.5 or int(prediction[0][1]*10) > 75:
            predicted_result = 'Positive'
        else:
            predicted_result = 'Negative'
        
        profile.brain_tumor_result = predicted_result
        profile.save()
        print(predicted_result)
        # return HttpResponse(prediction[0][0])
        return HttpResponseRedirect(reverse('App_main:brain-tumor-more-specifically'))



def heart_disease(request):
    return render(request, 'App_main/heart_disease.html')


def heart_disease_detector_better_page(request):
    return render(request, 'App_main/heart-disease-detector-upper.html')


def heart_disease_detector_better(request):
    with open('App_main/models/heart_disease_model', 'rb') as f:
        heart_model = pickle.load(f)
    # with open('App_main/models/heart_disease_detector_model', 'rb') as f:
    #     heart_model = pickle.load(f) 
    # heart_model = joblib.load("App_main/models/heart_disease_detector_model.joblib")
    if request.method == 'POST':
        age = int(request.POST.get('age'))
        sex = int(request.POST.get('gender'))
        cp = int(request.POST.get('chest_pain'))
        trestbps = float(request.POST.get('blood_pressure'))
        chol = float(request.POST.get('cholesterol'))
        fbs = int(request.POST.get('fasting_bp'))
        restecg = int(request.POST.get('restecg'))
        thalach = float(request.POST.get('maximum_heart_rate'))
        exang = int(request.POST.get('exang'))
        oldpeak = float(request.POST.get('oldpeak'))
        slop = int(request.POST.get('slop'))
        ca = int(request.POST.get('ca'))
        thal = int(request.POST.get('thalassemia'))
        input_data = (age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slop, ca, thal)
        input_data_array = np.asarray(input_data)
        input_shape = input_data_array.reshape(1, -1)
        predict = heart_model.predict(input_shape)
        if predict[0] == 0:
            res = 'Negative'
        elif predict[0] == 1:
            res = "Positive"
        
        profile = Patient_Tested_Results.objects.get(user=request.user)
        profile.heart_disease = res
        profile.save()
        
        return JsonResponse({'result': res})


def heartDiseaseDetection(request):
    heart_model = joblib.load("App_main/models/cardio.joblib")
    if request.method == 'POST':
        gender = int(request.POST.get('gender'))
        height	 = int(request.POST.get('height'))
        weight = float(request.POST.get('weight'))
        ap_hi = int(request.POST.get('ap_hi'))
        ap_lo = int(request.POST.get('ap_lo'))
        cholesterol	 = int(request.POST.get('cholesterol'))
        gluc = int(request.POST.get('gluc'))
        smoke = int(request.POST.get('smoke'))
        alco = int(request.POST.get('alco'))
        active_excercise = int(request.POST.get('active'))
        age = int(request.POST.get('yr'))

        prediction = heart_model.predict([[
            height, weight, gender, ap_hi, ap_lo, cholesterol, gluc, smoke, alco, active_excercise, age
        ]])
        print(prediction[0])

        if prediction[0] == 0:
            res = 'Negative'
        elif prediction[0] == 1:
            res = "Positive"
        
        return JsonResponse({'result': res})


def kidney_disease(request):
    return render(request, 'App_main/kidney_disease.html')


def kidney_disease_detect(request):
    with open('App_main/models/ckd.model/saved_model.pb', 'rb') as f:
        kidney_model = pickle.load(f)
    content = {}
    if request.method == 'POST':
        sg = int(request.POST.get('sg'))
        al = int(request.POST.get('al'))
        sc = int(request.POST.get('sc'))
        hemo = int(request.POST.get('hemo'))
        pcv = int(request.POST.get('pcv'))
        htn = int(request.POST.get('htn'))
        input_data = (sg, al, sc, hemo, pcv, htn)
        input_data_array = np.asarray(input_data)
        input_shape = input_data_array.reshape(1, -1)
        predict = kidney_model.predict(input_shape)
        if predict[0] == 0:
            result = 'Negative'
        elif predict[0] == 1:
            result = 'Positive'
        return JsonResponse({'result': result})


def profile_setup(request):
    user = User.objects.get(username=request.user)
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        dob = request.POST.get('dob')
        sex = request.POST.get('sex')
        hyper_tension = request.POST.get('hyper_tension')
        diabetics = request.POST.get('diabetics')
        asthma = request.POST.get('asthma')
        Smoking = request.POST.get('Smoking')
        alchohol = request.POST.get('alchohol')
        address = request.POST.get('address')
        profile_picture = request.FILES.get('profile_picture')
        profile = MedicalProfile(user=user, 
                                full_name=full_name, 
                                date_of_birth=dob,
                                sex= sex,
                                past_medical_history= hyper_tension,
                                hyper_tension= hyper_tension,
                                diabetics=diabetics,
                                asthma=asthma,
                                smoking=Smoking,
                                Alchohol=alchohol,
                                address=address,
                                profile_picture=profile_picture)
        profile.save()
    return render(request, 'App_main/profile_setup.html')



def profile_(request):
    profile = MedicalProfile.objects.get(user=request.user)
    age = date.today() - profile.date_of_birth
    age_in_year = age.days // 365
    print(age_in_year)
    content = {
        'profile': profile,
        'age': age_in_year,
    }
    return render(request, 'App_main/profile.html', context=content)