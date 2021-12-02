from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q


from .models import Product, Category


def home(request):
    categories = Category.objects.all()
    latest_products = Product.objects.all().order_by("-id")[:4]
    context = {"categories":categories, "latest_products":latest_products}
    return render(request, "shop/index.html", context)

def shop(request, category_slug=None):
    products = Product.objects.all()
    categories = Category.objects.all()
    query = None
    if category_slug:
        products = Product.objects.filter(category__slug=category_slug)
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

    context = {"categories":categories, "products":products, "query":query}
    return render(request, "shop/shop.html", context)


def product_detail(request, product_slug):
    product = Product.objects.filter(slug=product_slug).first()
    related_products = Product.objects.filter(category__in=product.category.all())
    related_products = [product for product in related_products if product != product]
    categories = Category.objects.all()
    text = "Hi, I am referred from Animal Farm NG. I want to buy"
    context = {"categories":categories, "product":product, "text":text, "related_products":related_products}
    return render(request, "shop/product_detail.html", context)
