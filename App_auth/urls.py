from django.urls import path
from App_auth.views import *


app_name = 'App_auth'


urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
]

