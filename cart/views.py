from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from .models import Cart, CartItem
from orders.models import Order, OrderItem
from inventory.models import Product
from .utils import send_order_emails

import logging

logger = logging.getLogger(__name__)


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, item_created = CartItem.objects.get_or_create(
        cart=cart, product=product)

    if not item_created:
        cart_item.quantity += 1
        cart_item.save()

    messages.success(request, f"{product.name} added to your cart.")
    return redirect('product_detail', product_id=product_id)


@login_required
def view_cart(request):
    try:
        cart = Cart.objects.get(user=request.user)
        cart_items = cart.items.all()
        total_price = cart.get_total_price()
    except Cart.DoesNotExist:
        cart = None
        cart_items = []
        total_price = 0

    context = {
        'cart': cart,
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(request, 'cart/view_cart.html', context)


@login_required
def empty_cart(request):
    if request.method == 'POST':
        try:
            cart = Cart.objects.get(user=request.user)
            cart.items.all().delete()
            messages.success(request, 'Tu carrito ha sido vaciado.')
        except Cart.DoesNotExist:
            messages.error(request, 'No se pudo vaciar el carrito.')
    return redirect('view_cart')


@login_required
def update_cart(request, item_id):
    if request.method == 'POST':
        try:
            cart_item = CartItem.objects.get(
                id=item_id, cart__user=request.user)
            quantity = int(request.POST.get('quantity', 1))
            if 1 <= quantity <= 4:
                cart_item.quantity = quantity
                cart_item.save()
                messages.success(request, 'Cantidad actualizada.')
            else:
                messages.error(request, 'La cantidad debe estar entre 1 y 4.')
        except CartItem.DoesNotExist:
            messages.error(request, 'No se pudo actualizar el carrito.')
    return redirect('view_cart')


@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(
        CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    messages.success(
        request, f"{cart_item.product.name} removed from your cart.")
    return redirect('view_cart')


@login_required
def confirm_purchase(request):
    if request.method == 'POST':
        metodo_pago = request.POST.get('metodoPago')
        if not metodo_pago:
            messages.error(request, 'Por favor, selecciona un método de pago.')
            return redirect('view_cart')
        try:
            with transaction.atomic():
                cart = Cart.objects.get(user=request.user)
                cart_items = cart.items.all()
                total_price = cart.get_total_price()

                # Crear un nuevo objeto Order
                order = Order.objects.create(
                    user=request.user,
                    total_amount=total_price,
                    status='pending'
                )

                # Crear OrderItems y actualizar el inventario
                product_summary = []
                for item in cart_items:
                    OrderItem.objects.create(
                        order=order,
                        product=item.product,
                        quantity=item.quantity,
                        price=item.product.price
                    )
                    # Actualizar el inventario
                    product = item.product
                    product.stock -= item.quantity
                    product.save()
                    product_summary.append(
                        f"{item.product.name} - Cantidad: {item.quantity}")

                product_summary = "\n".join(product_summary)

                # Enviar correos
                try:
                    send_order_emails(order, product_summary, metodo_pago)
                except Exception as e:
                    # Manejar el error de envío de correo
                    logger.error(
                        f"No se pudieron enviar los correos para la orden {order.id}: {str(e)}")
                    messages.warning(
                        request, "Se procesó tu orden, pero hubo un problema al enviar los correos de confirmación. Por favor, contacta con soporte.")

                # Limpiar el carrito
                cart.items.all().delete()

                context = {
                    'order': order,
                    'cart_items': cart_items,
                    'total_price': total_price,
                    'metodo_pago': metodo_pago,
                }

                # Si es una solicitud AJAX, devolver el HTML renderizado
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return render(request, 'cart/purchase_confirmation.html', context)
                else:
                    return render(request, 'cart/purchase_confirmation.html', context)

        except Cart.DoesNotExist:
            messages.error(request, 'No se pudo procesar la compra.')
            return redirect('view_cart')

    return redirect('view_cart')
