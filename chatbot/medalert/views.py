from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import User

# Create your views here.

def index(request):
    return render(request, "medalert/index.html")

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "medalert/register.html",
            {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            newuser = User.objects.create_user(username, email, password)
            return render(request, "medalert/register1.html",
            {
                "message": "Registration Successful"
            })
            newuser.save()
        except IntegrityError:
            return render(request, "medalert/register.html",
            {
                "message": "Username already taken."
            })
        login(request, newuser)
        return HttpResponseRedirect(reverse("login"))
    else:
        return render(request, 'medalert/register.html')

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication is succesful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "medalert/login.html", {
                "message": "Invalid username/password"
            })
    else:
        return render(request, "medalert/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))