from store.models import Product_model
from django import forms


class ProductForm(forms.ModelForm):
    class Meta:
        model=Product_model
        fields=['category','title','description','price','image']

        widgets={
            'category':forms.Select(attrs={'class':'form-control border-secondary'}),
            'title':forms.TextInput(attrs={'class':'form-control border-secondary'}),
            'description':forms.Textarea(attrs={'class':'form-control border-secondary'}),
            
        }