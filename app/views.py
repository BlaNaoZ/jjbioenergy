from django.core.checks import messages
from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from .forms import ReferenceForm
from app.models import Reference

#Used to check if the user has the permission to edit a reference.
def can_edit_reference(user, reference):
    if user.supplier_flag:
        if user == reference.supplier:
            return True
        return False
    elif user.foundation_industry_flag:
        if user == reference.customer:
            return True
        return False
    elif user.heat_buyer_flag:
        if user == reference.customer:
            return True
        return False
    elif user.admin:
        return True
    else:
        return False


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

    can_edit = can_edit_reference(user=request.user, reference=reference)

    return render(request, 'app/reference_detail.html', {'reference': reference, 'fav': fav, 'editable': can_edit})

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
            reference.supplier = request.user
            reference.equipment_category = request.user.supplier.level_one
            reference.save()
            
            if reference.customer.heat_buyer_flag:
                reference.customer_product = reference.customer.heatbuyer.level_two
            else:
                reference.customer_product = reference.customer.foundationindustry.level_two

            reference.reference_number = 'ref-' + str(reference.equipment_category) + '-' + str(reference.pk)
            reference.save()
            return redirect('reference_detail', pk=reference.pk)
    else:
        form = ReferenceForm()
    return render(request, 'app/reference_edit.html', {'form': form})

@login_required
def reference_edit(request, pk):
    reference = get_object_or_404(Reference, pk=pk)
    if not can_edit_reference(user=request.user, reference=reference):
        return redirect('error/500.html')
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


#Error handling custom views.
def error_404(request, exception):
        data = {}
        return render(request,'errors/404.html', data)

def error_500(request):
        data = {}
        return render(request,'errors/500.html', data)

def error_403(request, exception):
        data = {}
        return render(request,'errors/403.html', data)

def error_400(request, exception):
        data = {}
        return render(request,'errors/400.html', data)