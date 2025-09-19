from mimetypes import init
from ssl import SSL_ERROR_INVALID_ERROR_CODE
from django.contrib.auth import authenticate, login , logout
from django.shortcuts import render, redirect 
# redirect helps to push back to url as arg
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

#importing forms
from users.forms import RegistrationForm

#for messages
from django.contrib import messages
#------------------------------------------------------------

def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    return render(request, "users/user.html")
        #homepage or maybe profile

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:   #if authentication works
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:                     #if authentication fails              
            return render(request, "users/login.html", {

                "message" : "invalid credentials"
                
            } )
    else:
        return render(request, "users/login.html")

def signup_view(request, *args, **kwargs):
    user = request.user
    if user.is_authenticated:
        return HttpResponse(f"You are already authenticated as {user.email}")
    context = {}

    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email').lower()
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_password)
            
            #this login is predefined
            login(request, account)

            destination = kwargs.get("next")
            if destination:
                return redirect(destination)
            return redirect('/users')
        else:
            context ['registration_form'] = form
    else:
        form = RegistrationForm()
        context['registration_form'] = form  # use it for validation errors
    return render(request, "users/signup.html",context)
    
def logout_view(request):
    logout(request)
    messages.success(request, 'You have successfully logged out!')
    return render(request, "home/index.html" , 
    {
        "message" : "Logged out."
    }
    )