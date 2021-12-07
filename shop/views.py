from django.shortcuts import redirect, render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q


from .models import Product, Category

import os
import random
import requests


def home(request):
    categories = Category.objects.all()
    latest_products = Product.objects.all().order_by("-id")[:4]
    products = list(Product.objects.all())
    random_products = random.sample(products, len(products))[:4]
    context = {"categories":categories, "latest_products":latest_products, "random_products": random_products}
    return render(request, "shop/index.html", context)

def shop(request, category_slug=None):
    products = Product.objects.all()
    categories = Category.objects.all()
    category= None
    query = None
    if category_slug:
        products = Product.objects.filter(category__slug=category_slug)
        category = Category.objects.filter(slug=category_slug).first()
        category = category.name
    query = request.GET.get("q", None)
    if query:
        products = Product.objects.filter(Q(name__icontains=query) | \
            Q(category__name__icontains=query) \
                | Q(detail__icontains=query) \
                | Q(age__icontains=query) \
                | Q(vendor__city__icontains=query) \
                | Q(vendor__state__icontains=query))

    paginator = Paginator(products, 20)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    except:
        products = paginator.page(1)

    context = {"categories":categories, "products":products, "query":query, "category":category}
    return render(request, "shop/shop.html", context)


def product_detail(request, product_slug):
    product = Product.objects.filter(slug=product_slug).first()
    related_products = Product.objects.filter(category__in=product.category.all())
    related_products = [product for product in related_products if product != product]
    categories = Category.objects.all()
    text = "Hi, I am referred from Animal Farm NG. I want to buy"
    context = {"categories":categories, "product":product, "text":text, "related_products":related_products}
    return render(request, "shop/product_detail.html", context)


def enquire(request):
    if request.method == "POST":
        name = request.POST.get("name", None)
        email = request.POST.get("email", None)
        farm_name = request.POST.get("farm_name", None)
        category = request.POST.get("category", None)
        age = request.POST.get("age", None)
        quantity = request.POST.get("quantity", None)
        from_where = request.POST.get("from", None)
        to_where = request.POST.get("to", None)
        html_message = f"ENQUIRY\n\n\nName: {name}\nEmail: {email}\nFarm Name: {farm_name}\nCategory: {category}\nAge: {age}\nQuantity: {quantity}\n\nFrom: {from_where}\nTo: {to_where}"
        requests.post("https://api.mailgun.net/v3/animalfarm.ng/messages", auth=("api", os.environ.get("MAILGUN_API_KEY")), data={"from": "Animal Farm NG <hello@animalfarm.ng>", "to": ["peculiarmercy09@gmail.com"],  "subject": "Enquiry", "text": html_message})
        return redirect("shop:enquire")
    categories = Category.objects.all()
    context = {"categories":categories}
    return render(request, "shop/enquire.html", context)