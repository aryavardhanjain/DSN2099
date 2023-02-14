from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import User, Contact

# Create your views here.

def index(request):
    return render(request, "medalert/index.html")

def about(request):
    return render(request, "medalert/about.html")

def services(request):
    return render(request, "medalert/services.html")

def contact(request):
    if request.method=="POST":
        contact = Contact()
        user_name = request.POST["name"]        
        email_address = request.POST["email"]
        content = request.POST["content"]
        if len(user_name)<2 or len(email_address)<3 or len(content)<5:
            return render(request, "medalert/contact.html", {
                "message": "Invalid Form Submission."
            })
        else:
            contact.name = user_name
            contact.email = email_address
            contact.content = content
            contact.save()
            return render(request, "medalert/contact.html", 
            {
                "message1": "Thank You for Contacting Us. We Will Get Back to You Shortly."
            })
    else:
        return render(request, "medalert/contact.html")

def register(request):
    if request.method == "POST":
        username = request.POST["username"]

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
            user = User.objects.create_user(username, password)
            user.save()
        except IntegrityError:
            return render(request, "medalert/register.html",
            {
                "message": "Username already taken."
            })
        login(request,user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, 'medalert/register.html')


def login_view(request):
     if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "medalert/login.html", {
                "message": "Invalid username and/or password."
            })
     
     else:
        return render(request, "medalert/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


