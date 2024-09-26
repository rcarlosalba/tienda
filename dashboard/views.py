from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Count, Sum
from inventory.models import Product, Category, ProductImage
from orders.models import Order
from .forms import ProductForm, OrderStatusForm, CategoryForm


def is_owner_or_manager(user):
    return user.is_authenticated and (user.is_superuser or user.groups.filter(name='Managers').exists())


@user_passes_test(is_owner_or_manager)
def dashboard_home(request):
    total_products = Product.objects.count()
    total_categories = Category.objects.count()
    low_stock_products = Product.objects.filter(stock__lt=5).count()
    recent_orders = Order.objects.order_by('-created_at')[:5]

    context = {
        'total_products': total_products,
        'total_categories': total_categories,
        'low_stock_products': low_stock_products,
        'recent_orders': recent_orders,
    }
    return render(request, 'dashboard/home.html', context)


@user_passes_test(is_owner_or_manager)
def product_list(request):
    products = Product.objects.all()
    low_stock_products = Product.objects.filter(stock__lt=5)
    context = {
        'products': products,
        'low_stock_products': low_stock_products,
    }
    return render(request, 'dashboard/product_list.html', context)


@user_passes_test(is_owner_or_manager)
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            for image in request.FILES.getlist('images'):
                ProductImage.objects.create(product=product, image=image)
            return redirect('dashboard_product_list')
    else:
        form = ProductForm()
    return render(request, 'dashboard/product_form.html', {'form': form})


@user_passes_test(is_owner_or_manager)
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('dashboard_products')
    else:
        form = ProductForm(instance=product)
    return render(request, 'dashboard/product_form.html', {'form': form, 'product': product})


@user_passes_test(is_owner_or_manager)
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('dashboard_products')
    return render(request, 'dashboard/product_confirm_delete.html', {'product': product})


@user_passes_test(is_owner_or_manager)
def order_list(request):
    orders = Order.objects.all().order_by('-created_at')
    context = {
        'orders': orders,
        'total_orders': orders.count(),
        'total_revenue': orders.aggregate(Sum('total_amount'))['total_amount__sum'] or 0,
        'pending_orders': orders.filter(status='pending').count(),
    }
    return render(request, 'dashboard/order_list.html', context)


@user_passes_test(is_owner_or_manager)
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        form = OrderStatusForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            messages.success(
                request, f'El estado del pedido #{order.id} ha sido actualizado.')
            return redirect('dashboard_order_list')
    else:
        form = OrderStatusForm(instance=order)

    context = {
        'order': order,
        'form': form,
        'order_items': order.items.all(),
    }
    return render(request, 'dashboard/order_detail.html', context)


@user_passes_test(is_owner_or_manager)
def product_list(request):
    products = Product.objects.all()
    return render(request, 'dashboard/product_list.html', {'products': products})


@user_passes_test(is_owner_or_manager)
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product = form.save()
            for image in request.FILES.getlist('images'):
                ProductImage.objects.create(product=product, image=image)
            return redirect('dashboard_product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'dashboard/product_form.html', {'form': form, 'product': product})


@user_passes_test(is_owner_or_manager)
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('dashboard_product_list')
    return render(request, 'dashboard/product_confirm_delete.html', {'product': product})


@user_passes_test(is_owner_or_manager)
def delete_product_image(request, image_id):
    if request.method == 'POST':
        image = get_object_or_404(ProductImage, id=image_id)
        if image.product.images.count() > 1:
            image.delete()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'message': 'No se puede eliminar la última imagen del producto.'}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Método no permitido.'}, status=405)


@user_passes_test(is_owner_or_manager)
def category_list(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
    }
    return render(request, 'dashboard/category_list.html', context)


@user_passes_test(is_owner_or_manager)
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoría creada exitosamente.')
            return redirect('dashboard_category_list')
    else:
        form = CategoryForm()
    return render(request, 'dashboard/category_form.html', {'form': form})


@user_passes_test(is_owner_or_manager)
def category_edit(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoría actualizada exitosamente.')
            return redirect('dashboard_category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'dashboard/category_form.html', {'form': form, 'category': category})


@user_passes_test(is_owner_or_manager)
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Categoría eliminada exitosamente.')
        return redirect('dashboard_category_list')
    return render(request, 'dashboard/category_confirm_delete.html', {'category': category})
