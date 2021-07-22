from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from app.models import Reference


def reference_list(request):
    references = Reference.objects.filter(install_date__lte=timezone.now()).order_by('-install_date')
    return render(request, 'app/reference_list.html', {'references': references})


def reference_detail(request, pk):
    reference = get_object_or_404(Reference, pk=pk)
    return render(request, 'app/reference_detail.html', {'reference': reference})


def category_list(request):
    categories = Reference.objects.order_by('equipment_category')
    return render(request, 'app/reference_list.html', {'categories': categories})


def category_detail(request, pk):
    category = get_object_or_404(Reference, pk)
    return render(request, 'app/reference_detail.html', {'category': category})
