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
    if not cart:
        return items, total
        
    product_ids = [int(pid) for pid in cart.keys() if pid.isdigit()]
    products = Product.objects.filter(pk__in=product_ids)
    
    for product in products:
        pid = str(product.pk)
        if pid in cart:
            qty = cart[pid]['qty']
            subtotal = product.price * qty
            total += subtotal
            items.append({
                'product': product,
                'quantity': qty,
                'subtotal': subtotal,
            })
            
    return items, total