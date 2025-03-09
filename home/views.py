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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            category = Product.objects.get(id=self.kwargs['pk']).category
            context['related_products'] = Product.objects.filter(category=category).exclude(pk=self.kwargs['pk'])
        except Product.DoesNotExist:
            context['related_products'] = Product.objects.none()
        return context


# Delete product
class ProductDeleteView(LoginRequiredMixin, generic.DeleteView):
    template_name = 'home/confirm_delete.html'
    model = Product
    success_url = reverse_lazy('profile')


# Add product
class CreateProductView(LoginRequiredMixin, generic.View):
    def get(self, request):
        return render(request, 'home/create_product.html', {'form': ProductForm()})

    def post(self, request):
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                profile = Profile.objects.get(user=request.user)
                product = form.save(commit=False)
                product.seller = profile
                product.save()
                messages.success(request, 'New Product added successfully!')
                return redirect('profile')
            except Profile.DoesNotExist:
                messages.error(request, 'You need to create a profile first.')
                return redirect('create_profile')
        return render(request, 'home/create_product.html', {'form': form})


# Manage product
class ManageProductView(LoginRequiredMixin, generic.View):
    def get(self, request, *args, **kwargs):
        try:
            pk = kwargs['pk']
            product = Product.objects.get(pk=pk)
            form = ProductForm(instance=product)
            return render(request, 'home/create_product.html', {'form': form})
        except Product.DoesNotExist:
            messages.warning(request, 'Product does not exist.')
            return redirect('profile')

    def post(self, request, *args, **kwargs):
        try:
            pk = kwargs['pk']
            product = Product.objects.get(pk=pk)
            form = ProductForm(instance=product, data=request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Product updated successfully!')
                return redirect('profile')
            return render(request, 'home/create_product.html', {'form': form})
        except Product.DoesNotExist:
            messages.warning(request, 'Product does not exist.')
            return redirect('profile')


# Remove product

class RemoveProductView(LoginRequiredMixin,generic.DeleteView):
    template_name = 'home/confirm_delete.html'
    model = Product
    success_url = 'profile'

# Profile view
class ProfileView(LoginRequiredMixin, generic.View):
    def get(self, request):
        profile = get_object_or_404(Profile, user=request.user)
        return render(request, 'home/profile.html', {'profile': profile})


# Create profile
class CreateProfileView(LoginRequiredMixin, generic.CreateView):
    template_name = 'home/create_profile.html'
    model = Profile
    form_class = ProfileForm

    def form_valid(self, form):
        if Profile.objects.filter(user=self.request.user).exists():
            messages.warning(self.request, 'You already have a profile.')
            return redirect('profile')
        form.instance.user = self.request.user
        messages.success(self.request, 'New profile created successfully.')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('profile')


# Manage profile
class ManageProfileView(LoginRequiredMixin, generic.UpdateView):
    form_class = ProfileForm
    model = Profile
    template_name = 'home/create_profile.html'

    def get_object(self, queryset=None):
        return Profile.objects.get(user=self.request.user)

    def get_success_url(self):
        return reverse_lazy('profile')

