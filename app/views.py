from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .forms import ReferenceForm
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


def reference_new(request):
    if request.method == "POST":
        form = ReferenceForm(request.POST)
        if form.is_valid():
            reference = form.save(commit=False)
            reference.supplier = request.user
            reference.save()
            reference.reference_number = 'ref-' + str(reference.equipment_category) + '-' + str(reference.pk)
            reference.save()
            return redirect('reference_detail', pk=reference.pk)
    else:
        form = ReferenceForm()
    return render(request, 'app/reference_edit.html', {'form': form})


def reference_edit(request, pk):
    reference = get_object_or_404(Reference, pk=pk)
    if request.method == "POST":
        form = ReferenceForm(request.POST, instance=reference)
        if form.is_valid():
            reference = form.save(commit=False)
            reference.supplier = request.user
            reference.save()
            reference.reference_number = 'ref-' + str(reference.equipment_category) + '-' + str(reference.pk)
            reference.save()
            return redirect('reference_detail', pk=reference.pk)
    else:
        form = ReferenceForm(instance=reference)
    return render(request, 'app/reference_edit.html', {'form': form})
