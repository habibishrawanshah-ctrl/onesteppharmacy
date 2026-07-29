from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import InsuranceProvider, UserInsurance

@login_required
def my_insurance(request):
    policies = UserInsurance.objects.filter(user=request.user)
    return render(request, 'insurance/my_insurance.html', {'policies': policies})

@login_required
def add_insurance(request):
    providers = InsuranceProvider.objects.filter(is_active=True)
    if request.method == 'POST':
        provider_id = request.POST.get('provider')
        policy_number = request.POST.get('policy_number', '').strip()
        coverage_type = request.POST.get('coverage_type', 'basic')
        if not provider_id or not policy_number:
            messages.error(request, 'Please select a provider and enter policy number.')
        else:
            provider = get_object_or_404(InsuranceProvider, pk=provider_id)
            UserInsurance.objects.create(
                user=request.user,
                provider=provider,
                policy_number=policy_number,
                coverage_type=coverage_type,
            )
            messages.success(request, 'Insurance policy added!')
            return redirect('insurance:my_insurance')
    return render(request, 'insurance/add_insurance.html', {'providers': providers})

@login_required
def delete_insurance(request, pk):
    policy = get_object_or_404(UserInsurance, pk=pk, user=request.user)
    policy.delete()
    messages.success(request, 'Insurance policy removed.')
    return redirect('insurance:my_insurance')

def provider_list(request):
    providers = InsuranceProvider.objects.filter(is_active=True)
    return render(request, 'insurance/providers.html', {'providers': providers})
