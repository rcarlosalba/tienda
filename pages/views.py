from django.shortcuts import render
from django.db.models import Count
from random import sample
from inventory.models import Product


def home(request):
    products_with_images = Product.objects.annotate(
        image_count=Count('images')
    ).filter(image_count__gt=0, stock__gt=0)
    products_home = Product.objects.all()[:12]

    top_products = products_with_images.order_by('-price')[:10]

    featured_products = sample(list(top_products), min(5, len(top_products)))

    context = {
        'featured_products': featured_products,
        'products': products_home,
        'is_home': True,
    }

    return render(request, 'pages/index.html', context)


def privacy_policy(request):
    return render(request, 'pages/privacy_policy.html')


def terms_of_service(request):
    return render(request, 'pages/terms_of_service.html')


def contact(request):
    return render(request, 'pages/contact.html')
