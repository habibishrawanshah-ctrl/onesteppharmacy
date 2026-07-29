from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Delivery, DeliveryZone

@login_required
def my_deliveries(request):
    deliveries = Delivery.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'delivery/my_deliveries.html', {'deliveries': deliveries})

@login_required
def delivery_tracking(request, pk):
    delivery = get_object_or_404(Delivery, pk=pk, user=request.user)
    return render(request, 'delivery/tracking.html', {'delivery': delivery})

def delivery_zones(request):
    zones = DeliveryZone.objects.all()
    return render(request, 'delivery/zones.html', {'zones': zones})
