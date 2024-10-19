from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from .forms import SignupForm
from .models import UserProfile
from store.models import Product_model

def vendor_detail(request,pk):

    vendor_profile=User.objects.get(id=pk)

    return render(request,'home/vendor.html',{'user':vendor_profile})


@login_required
def myaccount_page(request):

    product=Product_model.objects.filter(user=request.user)

    return render(request,'account/account.html',{'product_list':product})
    
    

def signup_page(request):

    if request.method=='POST':
        form=SignupForm(data=request.POST)

        if form.is_valid():
            user=form.save()
            login(request,user)
            UserProfile=UserProfile.objects.create(user=user)
            
            return redirect('home')

        return render(request,'account/signup.html',{'form':form})

    form=SignupForm()
    return render(request,'account/signup.html',{'form':form})


def Login_page(request):


    if request.method=='POST':
        form=AuthenticationForm(data=request.POST)

        if form.is_valid():

            username=form.cleaned_data['username']
            password=form.cleaned_data['password']


            user=authenticate(username=username,password=password)

            if user is not None:
                login(request,user)

                return redirect('home')

        return render(request,'account/login.html',{'form':form})


    form=AuthenticationForm()

    return render(request,'account/login.html',{'form':form})


@login_required
def logout_page(request):


    logout(request)

    return redirect('home')

