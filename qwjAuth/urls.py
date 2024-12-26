from django.urls import path
from . import views

app_name = 'qwjAuth'

urlpatterns = [
    path('login/', views.qwjlogin, name='login'),
    path('register/', views.register, name='register'),
    path('captcha/', views.send_eamil_captcha, name='captcha'),
    path('logout/', views.qwjlogout, name='logout')
]
