from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from app.models import Reference


def index(request):
    return render(request, 'index.html')



