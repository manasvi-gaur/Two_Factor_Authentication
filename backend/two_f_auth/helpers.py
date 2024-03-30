from .models import User
import random
import string
import requests, pyotp
from backend.settings import EMAIL_HOST_USER
from django.core.mail import send_mail


def backup_token_generate():
  characters = string.ascii_letters + string.digits
  backup_code = ''.join(random.choice(characters) for _ in range(10))
  return backup_code

def getUser(request):
 try:
  data = request.data
  user_id = data.get('user_id', None)
  user = User.objects.get(id = user_id)
  return user
 except:
  return None

def getQRCode(user):
 qr_otp = pyotp.random_base32()
 otp_auth_url = pyotp.totp.TOTP(qr_otp).provisioning_uri(
 name=user.username.lower(), issuer_name="localhost.com")

 user.qr_otp = qr_otp
 user.backup_code = backup_token_generate()
 user.save()
 qr_code = requests.post('http://localhost:8001/get-qr-code/', json = {'otp_auth_url': otp_auth_url}).json()
 
 return qr_code['qr_code_link']

def getLoginUser(request):
 data = request.data
 username = data.get('username', None)
 password = data.get('password', None)
 try:
  user = User.objects.get(username = username, password = password)
  return user
 except:
  return None


def getOTPValidity(user, otp):
 totp = pyotp.TOTP(user.qr_otp)
 if not totp.verify(otp):
  return False
 user.logged_in = True
 user.save()
 return True

def getUserForMail(request):
  try:
    data = request.data
    user_id = data.get('user_id', None)
    user = User.objects.get(id = user_id)
    if len(user.email)<10:
      return "invalid email"
    return user
  except:
    return None
  
  
def sendOTPmail(email):
  try:
    otp_value = random.randint(100000, 999999)
    send_mail("2FA OTP",f"Your OTP for 2 factor authentication: {otp_value}", EMAIL_HOST_USER, [email], fail_silently=False)
    return otp_value
  except Exception as e:
    return e
  