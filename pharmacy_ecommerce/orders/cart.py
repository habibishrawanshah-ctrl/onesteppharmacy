from django.shortcuts import get_object_or_404
from products.models import Product
from .models import Cart, CartItem


def get_or_create_cart(user):
    cart, created = Cart.objects.get_or_create(user=user)
    return cart


def add_to_cart(user, product_id, quantity=1):
    cart = get_or_create_cart(user)
    product = get_object_or_404(Product, pk=product_id)
    item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': quantity},
    )
    if not created:
        item.quantity += quantity
        item.save()
    return item


def remove_from_cart(user, product_id):
    cart = get_or_create_cart(user)
    CartItem.objects.filter(cart=cart, product_id=product_id).delete()


def update_quantity(user, product_id, quantity):
    cart = get_or_create_cart(user)
    item = CartItem.objects.filter(cart=cart, product_id=product_id).first()
    if item:
        if quantity > 0:
            item.quantity = quantity
            item.save()
        else:
            item.delete()


def cart_items(user):
    cart = get_or_create_cart(user)
    items = cart.items.select_related('product').all()
    total = sum(item.subtotal() for item in items)
    return items, total


def clear_cart(user):
    cart = get_or_create_cart(user)
    cart.items.all().delete()
