from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class SignupForm(UserCreationForm):
    full_name = forms.CharField(label="الاسم بالكامل", min_length=3, max_length=100)
    terms = forms.BooleanField(label="أوافق على الشروط والأحكام")

    class Meta:
        model = User
        fields = ("full_name", "email", "phone", "stage", "grade")

    def save(self, commit=True):
        u = super().save(commit=False)
        u.username = self.cleaned_data["email"].lower()
        u.email = u.username
        u.first_name = self.cleaned_data["full_name"]
        u.role = User.Role.STUDENT  # role is never taken from the form
        if commit:
            u.save()
        return u
