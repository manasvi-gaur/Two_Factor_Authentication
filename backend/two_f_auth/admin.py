from django.contrib import admin
from .models import User
# Register your models here.
admin.site.register(User)
class User(admin.ModelAdmin):
    list_display = ['id', 'qr_otp']