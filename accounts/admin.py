from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class Admin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (("بيانات الطالب", {"fields": ("role", "phone", "stage", "grade")}),)
    list_display = ("email", "first_name", "role", "is_active")
    list_filter = ("role", "is_active")
