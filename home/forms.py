from .models import Profile,Product
from django import forms

# Product form
class ProductForm(forms.ModelForm):
    class Meta:
        model=Product
        fields=['product_pic','name','price','quantity','category']


        widgets = {
            'product_pic': forms.ClearableFileInput(attrs={
                'class': 'block w-full text-sm text-gray-300 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-green-500 file:text-white hover:file:bg-green-600'}),
            'name': forms.TextInput(attrs={'class': 'w-full p-2 border rounded-lg bg-gray-700 text-white',
                                           'placeholder': 'Enter product name'}),
            'price': forms.NumberInput(
                attrs={'class': 'w-full p-2 border rounded-lg bg-gray-700 text-white', 'placeholder': 'Enter price'}),
            'quantity': forms.NumberInput(attrs={'class': 'w-full p-2 border rounded-lg bg-gray-700 text-white',
                                                 'placeholder': 'Enter quantity'}),
            'category': forms.Select(attrs={'class': 'w-full p-2 border rounded-lg bg-gray-700 text-white'}),
        }


# Profile Form
class ProfileForm(forms.ModelForm):
    class Meta:
        model=Profile
        exclude=['user']


