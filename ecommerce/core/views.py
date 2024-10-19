from django.shortcuts import render,redirect
from store.models import Product_model,Category_model
from django.db.models import Q
from core.forms import ProductForm
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required

# Home page 
def home_page(request):

    newest_product=Product_model.objects.all()
    product_category=Category_model.objects.all()

    return render(request,'home/index.html',{'product_list':newest_product,'category_list':product_category})



# About 
def about_page(request): return render(request,'home/about.html')


# search for products 
def search_page(request):

    query=request.GET['query']
    print(query)

    products=Product_model.objects.filter(
        Q(title__icontains=query) 
        | 
        Q(description__icontains=query) 
        | 
        Q(slug__icontains=query)
     )


    return render(request,'home/search.html',{'query':query,'product_list':products})

@login_required
def product_detail(request,pk):

    product=Product_model.objects.get(id=pk)


    return render(request,'store/product_detail.html',{'product':product})


# Edit product 

@login_required
def product_edit(request,pk):

    product=Product_model.objects.get(id=pk)

    if request.method=='POST':
        form=ProductForm(request.POST,request.FILES,instance=product)

        if form.is_valid():
            form.save()

            return redirect('account')


    form=ProductForm(instance=product)
    return render(request,'home/add_product.html',{'form':form})



# Delete product 

@login_required
def delete_product(request,pk):

    product=Product_model.objects.get(id=pk)
    product.delete()

    return redirect('account')
    


# Category list 
def product_category(request,pk):

    category=Category_model.objects.get(id=pk)
    product_list=Product_model.objects.filter(category=category)

    return render(request,'home/category.html',{'product_list':product_list,'category_list':Category_model.objects.all()})



# Vendor can add products 
def add_product(request):
    
    if request.method=='POST':
        form=ProductForm(request.POST,request.FILES)

        if form.is_valid():
            title=request.POST['title']
            product=form.save(commit=False)
            product.user=request.user
            product.slug=slugify(title)
            product.save()
            
            print('product save successfully ')
            return redirect('account')
        
        
        return render(request,'home/add_product.html',{'form':form})

    
    form=ProductForm()
    return render(request,'home/add_product.html',{'form':form})

