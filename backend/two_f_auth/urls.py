from django.contrib import admin
from django.urls import path
from two_f_auth import views

urlpatterns = [
    path('set2fa/', views.Set2FAView.as_view()),
    path('verify2fa/', views.Verify2FAView.as_view()),
    path('sendMailOTP/', views.SendOTPMail.as_view()),
    path('verifyMailOTP/', views.VerifyMailOTP.as_view()),
    path('verifyBackup/', views.VerifyWithBackup.as_view()),
]
