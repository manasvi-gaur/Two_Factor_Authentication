from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions, status
from rest_framework.decorators import api_view
from .helpers import getQRCode, getUser, getLoginUser, getOTPValidity, sendOTPmail
from .models import User
from two_f_auth.serializer import UserSerializer

class RegisterView(APIView):
 serializer_class = UserSerializer
 queryset = User.objects.all()
 def post(self, request):
  serializer = self.serializer_class(data = request.data)
  if serializer.is_valid():
   serializer.save()
   return Response({ "user_id": serializer.data['id'], "status": "Registration successful", "message": "Registered successfully, please login" }, 
    status=status.HTTP_201_CREATED)
  else:
   return Response({ "status": "Registration failed", "message": str(serializer.errors) }, 
    status=status.HTTP_400_BAD_REQUEST)

class Set2FAView(APIView):
 def post(self, request):
  user = getUser(request)
  if user == None:
   return Response({"status": "fail", "message": f"No user with the corresponding username and password exists" }, 
    status=status.HTTP_404_NOT_FOUND)
  
  qr_code = getQRCode(user)
  return Response({"qr_code": qr_code, "backup_token":user.backup_code})

class LoginView(APIView):
 def post(self, request, *args, **kwargs):
  user = getLoginUser(request)
  if user == None:
   return Response({
    "status": "Login failed", 
    "message": f"No user with the corresponding username and password exists"
    }, 
    status=status.HTTP_404_NOT_FOUND)
  return Response({ "status": "Logined In successfully", 'user_id': user.id })

class Verify2FAView(APIView):
 serializer_class = UserSerializer
 queryset = User.objects.all()

 def post(self, request):
  user = getUser(request)
  if user == None:
   return Response({ "status": "Verification failed", "message": f"No user with the corresponding username and password exists"}, 
    status=status.HTTP_404_NOT_FOUND)

  valid_otp = getOTPValidity(user, request.data.get('otp', None))
  if not valid_otp:
   return Response({ "status": "Verification failed", "message": "OTP is invalid" }, 
    status=status.HTTP_400_BAD_REQUEST)
  return Response({ "status": "Verified", 'otp_verified': "true" })

  
class SendOTPMail(APIView):
  def post(self, request):
    user = getUser(request)
    if user == None:
      return Response({ "status": "Verification failed", "message": f"No user with the corresponding username and password exists"}, 
      status=status.HTTP_404_NOT_FOUND)
    otp = sendOTPmail(user.email)
    user.mail_otp = otp
    user.save()
    return Response({"status":"ok", "message":"otp sent"})

class VerifyMailOTP(APIView):
  def post(self, request):
    user = getUser(request)
    if user == None:
      return Response({ "status": "Verification failed", "message": f"No user with the corresponding username and password exists"}, 
      status=status.HTTP_404_NOT_FOUND)
    if(str(user.mail_otp) == request.data['otp']):
      return Response({"status":"ok"})
    return Response({"status":"verification failed","message":"Invalid OTP"})

class VerifyWithBackup(APIView):
  def post(self, request):
    user = getUser(request)
    if user == None:
      return Response({ "status": "Verification failed", "message": f"No user with the corresponding username and password exists"}, 
      status=status.HTTP_404_NOT_FOUND)
    if(user.backup_code == request.data['backup_otp']):
      return Response({"status":"ok"})
    return Response({"status":"verification failed","message":"Invalid Backup token"})
    
