from django.db import models
from django.contrib.auth.models import AbstractUser
import stripe
from django.conf import settings


# Custom User Model
class CustomUser(AbstractUser):
    username = models.CharField(max_length=50)  # Remove username field
    email = models.EmailField(max_length=50, unique=True)

    USERNAME_FIELD = 'email'  # Login using email
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email


# Abstract Base Model
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# Profile Model (Linked to CustomUser)
class Profile(BaseModel):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    profile_pic = models.ImageField(upload_to='profile_pics/')
    contact = models.CharField(max_length=50)
    location = models.TextField()

    def __str__(self):
        return self.user.email


# Category Model
class Category(BaseModel):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


# Product Model
class Product(BaseModel):
    product_pic = models.ImageField(upload_to='product_pics/')
    seller = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=5, decimal_places=2)  # Increased max_digits for better pricing
    content=models.TextField()
    quantity = models.PositiveIntegerField()  # Prevent negative quantities
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='categories')

    def __str__(self):
        return self.name


# Order Model
class Order(BaseModel):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Delivered', 'Delivered'),
    ]

    customer = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2,default=0)  # Increased precision

    def calculate_total_amount(self):
        """Calculates total price based on all OrderItems."""
        self.total_amount = sum(item.subtotal for item in self.items.all())  # Sum of all subtotals
        self.save()


    def __str__(self):
        return f"Order {self.id} - {self.customer.user.email}"


# OrderItem Model
class OrderItem(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
    quantity = models.PositiveIntegerField(default=1)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)  # Increased precision


    def save(self, *args, **kwargs):
        """Automatically update subtotal when quantity changes."""
        self.subtotal = self.product.price * self.quantity
        super().save(*args, **kwargs)  # Call the original save() method


    def __str__(self):
        return f"{self.quantity} x {self.product.name} for {self.order}"



class Payment(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    stripe_charge_id = models.CharField(max_length=50, blank=True, null=True)  # Store Stripe Transaction ID
    status = models.CharField(
        max_length=20,
        choices=[('Pending', 'Pending'), ('Completed', 'Completed'), ('Failed', 'Failed')],
        default='Pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.id} - {self.status}"


