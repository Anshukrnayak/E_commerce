from django.db import models

from django.contrib.auth.models import User



# Category model 
class Category_model(models.Model):
    title=models.CharField(max_length=50)
    slug=models.SlugField(max_length=50)

    def __str__(self): return self.title



# Product model 


class Product_model(models.Model):
    
    category=models.ForeignKey(Category_model,on_delete=models.CASCADE,related_name='category')
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='products')
    title=models.CharField(max_length=50)
    description=models.TextField()
    price=models.IntegerField()
    created_at=models.DateField(auto_now_add=True)
    update_at=models.DateField(auto_now=True)
    image=models.ImageField(upload_to='upload/product_images/')
    slug=models.SlugField(max_length=50)

    def __str__(self): return self.title

    # Thirty percent descount price.
    def get_descount_price(self): return self.price*0.3





