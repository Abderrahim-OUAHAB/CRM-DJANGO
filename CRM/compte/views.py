from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import CreerUser
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
# Create your views here.
def inscriptionPage(request):
    form=CreerUser()
    if request.method == "POST":
        form=CreerUser(request.POST)
        if form.is_valid():
            form.save()
            user=form.cleaned_data.get('username')
            messages.success(request,"Creation avec succes")
            return redirect('acces')
    context={'form':form}
    return render(request,'compte/inscription.html',context)

def accesPage(request):
    if request.method =="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect("home")
        else:
            messages.info(request,"Mot de passe ou nom d'utilisateur non valide")
    context={}
    return render(request,'compte/acces.html',context)

def logoutPage(request):
    logout(request)
    return redirect("acces")