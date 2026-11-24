from django.contrib.auth import login
from django.shortcuts import redirect, render
from .forms import SignupForm

def signup(request):
    form = SignupForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        login(request, form.save())
        return redirect("dashboard")
    return render(request, "registration/signup.html", {"form": form})
