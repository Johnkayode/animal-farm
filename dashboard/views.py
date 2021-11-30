from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.contrib.auth.decorators import login_required
from accounts.decorators import is_vendor

from shop.models import Category, Product
from shop.forms import ProductForm, slugify

@login_required
@is_vendor
def home(request):
    vendor = request.user.vendor
    products = Product.objects.filter(vendor=vendor)
    paginator = Paginator(products, 20)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    except:
        products = paginator.page(1)
    return render(request, "dashboard/home.html", context={"products":products})


@login_required
@is_vendor
def add_product(request):
    form = ProductForm(request.POST or None, request.FILES or None)
    if request.method == "POST":
        if form.is_valid():
            categories = request.POST.getlist("categories")
            product =  form.save(commit=False)
            product.vendor = request.user.vendor
            product.save()
            for category in categories:
                category = Category.objects.filter(slug=category).first()
                product.category.add(category)
                product.save()
                messages.success(request, 'Product succesfully created.')
                return redirect("dashboard:home")
    all_categories = Category.objects.all()
    context = {"form": form, "all_categories": all_categories}
    return render(request, "dashboard/add_product.html", context)

@login_required
@is_vendor
def add_category(request):
    if request.method == "POST":
        category_name = request.POST.get("name")
        category_name = category_name.title()
        category, created = Category.objects.get_or_create(name=category_name)
        if created:
            category.slug = slugify(category.name)
            category.save()
        messages.success(request, 'Category succesfully created.')
        return redirect("dashboard:home")
    return render(request, "dashboard/add_category.html")

@login_required
@is_vendor
def delete_product(request, slug):
    product = Product.objects.filter(slug=slug).first()
    if request.user.vendor == product.vendor:
        product.delete()
        messages.info(request, 'Product deleted.')
        return redirect("dashboard:home")



@login_required
@is_vendor
def edit_product(request, slug):
    product = Product.objects.filter(slug=slug).first()
    form = ProductForm(request.POST or None, request.FILES or None, instance=product)
    if request.method=="POST":
        if form.is_valid():
            if request.user.vendor == product.vendor:
                product = form.save(commit=False)
                categories = request.POST.getlist("categories")
                categories = [Category.objects.filter(slug=category).first() for category in categories]
                product.category.set(categories)
                product.save()
                messages.info(request, 'Product successfully updated.')
                return redirect("dashboard:home")
    all_categories = Category.objects.all()
    context = {"form": form, "all_categories": all_categories}
    return render(request, "dashboard/edit_product.html", context)
            