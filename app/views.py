from django.core.checks import messages
from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from .forms import ReferenceForm
from app.models import Reference

""" 
Used to check if user is authenticated before they can view any page, 
if not they're redirected to the login page.
Work in progress. 
"""

def check_supplier(user):
    return user.supplier_flag

def check_foundation_industry(user):
    return user.foundation_industry_flag

def check_heat_buyer(user):
    return user.heat_buyer_flag


@login_required
def favourite_add(request, id):
    reference = get_object_or_404(Reference, pk=id)
    if request.user.favourites.filter(id=reference.pk).exists():
        request.user.favourites.remove(reference)
    else:
        request.user.favourites.add(reference)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

@login_required
def reference_list(request):
    references = Reference.objects.filter(install_date__lte=timezone.now()).order_by('-install_date')
    return render(request, 'app/reference_list.html', {'references': references})

@login_required
def reference_detail(request, pk):
    reference = get_object_or_404(Reference, pk=pk)

    fav = bool

    if request.user.favourites.filter(pk=reference.pk).exists():
        fav = True

    return render(request, 'app/reference_detail.html', {'reference': reference, 'fav': fav})

@login_required
def category_list(request):
    categories = Reference.objects.order_by('equipment_category')
    return render(request, 'app/reference_list.html', {'categories': categories})

@login_required
def category_detail(request, pk):
    category = get_object_or_404(Reference, pk)
    return render(request, 'app/reference_detail.html', {'category': category})

@login_required
def reference_new(request):
    if request.method == "POST":
        form = ReferenceForm(request.POST)
        if form.is_valid():
            """
            Here some Reference fields are initialised using the User's (the one creating the reference) fields.
            """
            reference = form.save(commit=False)
            reference.supplier = request.user.supplier 
            reference.equipment_category = request.user.supplier.level_one
            reference.save()
            reference.reference_number = 'ref-' + str(reference.equipment_category) + '-' + str(reference.pk)
            reference.save()
            return redirect('reference_detail', pk=reference.pk)
    else:
        form = ReferenceForm()
    return render(request, 'app/reference_edit.html', {'form': form})

@login_required
def reference_edit(request, pk):
    reference = get_object_or_404(Reference, pk=pk)
    if request.method == "POST":
        form = ReferenceForm(request.POST, instance=reference)
        if form.is_valid():
            reference = form.save(commit=False)
            reference.supplier = request.user.supplier
            reference.save()
            reference.reference_number = 'ref-' + str(reference.equipment_category) + '-' + str(reference.pk)
            reference.save()
            return redirect('reference_detail', pk=reference.pk)
    else:
        form = ReferenceForm(instance=reference)
    return render(request, 'app/reference_edit.html', {'form': form})
