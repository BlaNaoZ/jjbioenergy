from app.models import Reference
from django.shortcuts import get_object_or_404, redirect, render
from .models import User
from django.contrib.auth.decorators import login_required, user_passes_test

@login_required
def favourite_list(request, pk):
    user = get_object_or_404(User, pk=pk)
    references = Reference.objects.all
    favourites = user.favourites.all
    return render(request, 'accounts/favourite_list.html', {'favourites': favourites, 'references': references})

@login_required
def profile(request, pk):
    user = get_object_or_404(User, pk=pk)
    if not user.is_admin:
        return render(request, 'accounts/profile.html', {'user': user})

@login_required
def profile_list(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % ('accounts/login', request.path))
    users = User.objects.filter(admin=False).order_by('-email')
    return render(request, 'accounts/profile_list.html', {'users': users})
