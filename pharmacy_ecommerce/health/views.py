from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import HealthRecord, HealthCondition, BlogPost
from django.core.paginator import Paginator

@login_required
def my_health_records(request):
    records = HealthRecord.objects.filter(user=request.user).order_by('-updated_at')
    return render(request, 'health/my_records.html', {'records': records})

@login_required
def add_health_record(request):
    conditions = HealthCondition.objects.all()
    if request.method == 'POST':
        condition_id = request.POST.get('condition')
        custom_condition = request.POST.get('custom_condition', '').strip()
        diagnosis_date = request.POST.get('diagnosis_date', '') or None
        notes = request.POST.get('notes', '')
        medications = request.POST.get('medications', '')
        if not condition_id and not custom_condition:
            messages.error(request, 'Please select or enter a health condition.')
        else:
            condition = None
            if condition_id:
                condition = get_object_or_404(HealthCondition, pk=condition_id)
            HealthRecord.objects.create(
                user=request.user,
                condition=condition,
                custom_condition=custom_condition,
                diagnosis_date=diagnosis_date,
                notes=notes,
                medications=medications,
            )
            messages.success(request, 'Health record added!')
            return redirect('health:my_records')
    return render(request, 'health/add_record.html', {'conditions': conditions})

@login_required
def delete_health_record(request, pk):
    record = get_object_or_404(HealthRecord, pk=pk, user=request.user)
    record.delete()
    messages.success(request, 'Health record removed.')
    return redirect('health:my_records')

def health_conditions(request):
    conditions = HealthCondition.objects.all()
    return render(request, 'health/conditions.html', {'conditions': conditions})


def blog_list(request):
    posts = BlogPost.objects.filter(is_published=True)
    category = request.GET.get('category')
    if category:
        posts = posts.filter(category__iexact=category)
    paginator = Paginator(posts, 9)
    page = paginator.get_page(request.GET.get('page'))
    categories = BlogPost.objects.filter(is_published=True).values_list('category', flat=True).distinct().exclude(category='')
    return render(request, 'health/blog_list.html', {
        'posts': page,
        'categories': categories,
        'current_category': category,
    })


def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, is_published=True)
    recent = BlogPost.objects.filter(is_published=True).exclude(pk=post.pk)[:3]
    return render(request, 'health/blog_detail.html', {'post': post, 'recent': recent})
