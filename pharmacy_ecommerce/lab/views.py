from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import LabTest, LabBooking

def lab_list(request):
    category = request.GET.get('category', '')
    tests = LabTest.objects.filter(is_active=True).order_by('name')
    if category:
        tests = tests.filter(category=category)
    paginator = Paginator(tests, 12)
    page = request.GET.get('page')
    tests = paginator.get_page(page)
    categories = LabTest.CATEGORY_CHOICES
    return render(request, 'lab/lab_list.html', {'tests': tests, 'categories': categories, 'active_category': category})

def lab_detail(request, pk):
    test = get_object_or_404(LabTest, pk=pk, is_active=True)
    return render(request, 'lab/lab_detail.html', {'test': test})

@login_required
def book_lab(request, pk):
    test = get_object_or_404(LabTest, pk=pk, is_active=True)
    if request.method == 'POST':
        booking_date = request.POST.get('booking_date')
        preferred_time = request.POST.get('preferred_time', '')
        address = request.POST.get('address', '')
        notes = request.POST.get('notes', '')
        if not booking_date:
            messages.error(request, 'Please select a booking date.')
        else:
            from datetime import datetime
            try:
                bd = datetime.strptime(booking_date, '%Y-%m-%dT%H:%M')
            except ValueError:
                try:
                    bd = datetime.strptime(booking_date, '%Y-%m-%d')
                except ValueError:
                    messages.error(request, 'Invalid date format.')
                    return render(request, 'lab/book_lab.html', {'test': test})
            LabBooking.objects.create(
                user=request.user,
                lab_test=test,
                booking_date=bd,
                preferred_time=preferred_time,
                address=address or request.user.userprofile.address,
                notes=notes,
            )
            messages.success(request, f'Lab test "{test.name}" booked successfully!')
            return redirect('lab:my_bookings')
    return render(request, 'lab/book_lab.html', {'test': test})

@login_required
def my_bookings(request):
    bookings = LabBooking.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'lab/my_bookings.html', {'bookings': bookings})
