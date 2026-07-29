from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from products.models import Product
from .models import Review

@login_required
def add_review(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    existing = Review.objects.filter(user=request.user, product=product).first()
    if request.method == 'POST':
        rating = int(request.POST.get('rating', 0))
        comment = request.POST.get('comment', '').strip()
        if rating < 1 or rating > 5:
            messages.error(request, 'Please select a rating between 1 and 5.')
        else:
            if existing:
                existing.rating = rating
                existing.comment = comment
                existing.save()
                messages.success(request, 'Review updated!')
            else:
                Review.objects.create(user=request.user, product=product, rating=rating, comment=comment)
                messages.success(request, 'Review submitted!')
            return redirect('products:detail', pk=product_id)
    return render(request, 'reviews/add_review.html', {'product': product, 'existing': existing})
