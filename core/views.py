from django.shortcuts import render
from .models import Institution, Donation, Category
# Create your views here.

def landing_page(request):
    return render(request, 'core/index.html', {} )

