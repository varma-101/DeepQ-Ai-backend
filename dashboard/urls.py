from django.urls import path
from .views import sample_data, worldbank_data, login, register
from rest_framework.authtoken.views import obtain_auth_token
urlpatterns = [
    path('sample/', sample_data, name='sample-data'),
    path('stats/', worldbank_data, name='stats'),
    path('login/', obtain_auth_token, name='login'),
   
    path('register/', register, name='register'),
]

