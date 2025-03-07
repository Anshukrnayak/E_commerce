# E-commerce Platform (Django + DRF + React.js)

## Overview
This is a full-stack e-commerce platform built using **Django** and **Django REST Framework (DRF)** for the backend and **React.js** for the frontend. It includes authentication, product listings, cart functionality, order processing, and payment integration.

## Features
- User authentication (JWT-based login/logout/register)
- Product management (CRUD operations for products)
- Shopping cart functionality
- Order management
- Payment integration (Stripe/PayPal)
- API-based backend (Django + DRF)
- Responsive UI (React.js + Tailwind CSS)

## Tech Stack
- **Backend:** Django, Django REST Framework (DRF), PostgreSQL/MySQL
- **Frontend:** React.js, React Router, Redux (for state management)
- **Authentication:** JWT-based authentication
- **Payments:** Stripe/PayPal
- **Deployment:** Docker, Nginx, Gunicorn

---

## Step-by-Step Implementation

### 1. Backend (Django + DRF Setup)
#### Install Dependencies:
```bash
pip install django djangorestframework django-cors-headers django-rest-framework-simplejwt stripe
```

#### Create Django Project:
```bash
django-admin startproject ecommerce_backend
cd ecommerce_backend
python manage.py startapp store
```

#### Configure `settings.py`:
```python
INSTALLED_APPS = [
    'django.contrib.admin', 'django.contrib.auth', 'django.contrib.contenttypes',
    'django.contrib.sessions', 'django.contrib.messages', 'django.contrib.staticfiles',
    'rest_framework', 'store', 'corsheaders',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}
```

#### Create Models (`store/models.py`):
```python
from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='products/')
    created_at = models.DateTimeField(auto_now_add=True)
```

#### Migrate and Create Superuser:
```bash
python manage.py makemigrations store
python manage.py migrate
python manage.py createsuperuser
```

#### API Views (`store/views.py`):
```python
from rest_framework import generics
from .models import Product
from .serializers import ProductSerializer

class ProductListView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
```

#### Setup URLs (`store/urls.py`):
```python
from django.urls import path
from .views import ProductListView

urlpatterns = [
    path('products/', ProductListView.as_view(), name='product-list')
]
```

#### Run Server:
```bash
python manage.py runserver
```

---

### 2. Frontend (React.js Setup)
#### Install Dependencies:
```bash
npx create-react-app ecommerce_frontend
cd ecommerce_frontend
npm install axios react-router-dom redux react-redux @reduxjs/toolkit
```

#### Setup Redux Store:
Create `store.js`:
```javascript
import { configureStore } from '@reduxjs/toolkit';
export const store = configureStore({ reducer: {} });
```

#### Fetch Products (`ProductList.js`):
```javascript
import React, { useEffect, useState } from 'react';
import axios from 'axios';

const ProductList = () => {
    const [products, setProducts] = useState([]);
    useEffect(() => {
        axios.get('http://127.0.0.1:8000/api/products/')
            .then(response => setProducts(response.data));
    }, []);
    return (
        <div>
            {products.map(product => (
                <div key={product.id}>{product.name} - ${product.price}</div>
            ))}
        </div>
    );
};
export default ProductList;
```

#### Start Frontend:
```bash
npm start
```

---

### 3. Payment Integration (Stripe Example)
#### Install Stripe:
```bash
pip install stripe
```

#### Create Payment View (`store/views.py`):
```python
import stripe
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response

stripe.api_key = settings.STRIPE_SECRET_KEY

class CreateCheckoutSession(APIView):
    def post(self, request):
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {'name': 'Test Product'},
                    'unit_amount': 1000,
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url='http://localhost:3000/success',
            cancel_url='http://localhost:3000/cancel',
        )
        return Response({'url': session.url})
```

---

### 4. Deployment
#### Dockerize Backend:
Create `Dockerfile`:
```dockerfile
FROM python:3.9
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

#### Run Backend with Docker:
```bash
docker build -t ecommerce_backend .
docker run -p 8000:8000 ecommerce_backend
```

#### Deploy Frontend to Vercel/Netlify:
```bash
npm run build
```

---
