from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import Product, Profile
from .forms import ProductForm, ProfileForm

# Indexing view
class IndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'home/index.html'
    model = Product
    context_object_name = 'products'

# Product Details
class ProductDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = 'home/detail.html'
    model = Product
    context_object_name = 'product'


# Delete product
class ProductDeleteView(LoginRequiredMixin, generic.DeleteView):
    template_name = 'home/confirm_delete.html'
    model = Product
    success_url = reverse_lazy('profile')  # ✅ Fix

# Add product
class CreateProductView(LoginRequiredMixin, generic.View):
    def get(self, request):
        return render(request, 'home/create_product.html', {'form': ProductForm()})

    def post(self, request):
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            print('user profile ',Profile.objects.get(user=request.user))
            product.seller = Profile.objects.get(user=request.user)
            product.save()
            messages.success(request, 'New Product added successfully!')
            return redirect('profile')  # ✅ Fix
        print(form.errors)
        return render(request, 'home/create_product.html', {'form': form})

# Profile view
class ProfileView(LoginRequiredMixin, generic.View):
    def get(self, request):
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:  # ✅ Fix
            return redirect('create_profile')

        return render(request, 'home/profile.html', {'profile': profile})


# create profile 
class CreateProfileView(LoginRequiredMixin,generic.CreateView):
    template_name = 'home/create_profile.html'
    model = Profile
    form_class = ProfileForm
    
    def form_valid(self, form):
        form.instance.user=self.request.user
        messages.success(self.request,'new profile created successfully.... ')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('profile')

