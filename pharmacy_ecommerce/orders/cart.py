from products.models import Product


def get_cart(request):
    return request.session.get('cart', {})


def save_cart(request, cart):
    request.session['cart'] = cart
    request.session.modified = True


def add_to_cart(request, product_id, quantity=1):
    cart = get_cart(request)
    pid = str(product_id)
    if pid in cart:
        cart[pid]['qty'] += quantity
    else:
        cart[pid] = {'qty': quantity}
    save_cart(request, cart)


def remove_from_cart(request, product_id):
    cart = get_cart(request)
    cart.pop(str(product_id), None)
    save_cart(request, cart)


def update_quantity(request, product_id, quantity):
    cart = get_cart(request)
    pid = str(product_id)
    if pid in cart:
        if quantity > 0:
            cart[pid]['qty'] = quantity
        else:
            del cart[pid]
    save_cart(request, cart)


def cart_items(request):
    cart = get_cart(request)
    items = []
    total = 0
    for pid, data in cart.items():
        try:
            product = Product.objects.get(pk=int(pid))
            subtotal = product.price * data['qty']
            total += subtotal
            items.append({
                'product': product,
                'quantity': data['qty'],
                'subtotal': subtotal,
            })
        except Product.DoesNotExist:
            pass
    return items, total