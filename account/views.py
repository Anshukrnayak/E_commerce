from django.shortcuts import render,redirect
from django.views import generic
from .forms import SignupForm,LoginForm
from django.contrib.auth import  authenticate,login,logout
from django.contrib.auth.mixins import LoginRequiredMixin


class SignupView(generic.View):
    def get(self,request):
        form=SignupForm()
        return render(request,'account/signup.html',{'form':form})

    def post(self,request):
        form=SignupForm(data=request.POST)
        if form.is_valid():
            login(request,form.save())
            return redirect('create_profile')

        return render(request,'account/signup.html',{'form':form})


class LoginView(generic.View):
    def get(self,request):
        form=LoginForm()
        return render(request,'account/Login.html',{'form':form})

    def post(self,request):
        form=LoginForm(data=request.POST)
        if form.is_valid():

            email=form.data['email']
            password=form.data['password']

            user=authenticate(email=email,password=password)
            if user is not None:
                login(request, user)
                return redirect('home')

            return render(request,'account/Login.html',{'form':form})


class LogoutView(LoginRequiredMixin,generic.View):
    def get(self,request):
        logout(request)
        return redirect('login')

