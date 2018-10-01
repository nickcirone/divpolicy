from django.shortcuts import render
from django.utils import timezone
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from django.views.generic.base import TemplateView
from .models import Policy
from .search import search

# Create your views here.

def search_home(request):
    return render(request, 'blog/search_home.html')

def policy_search(request):
    print("Trying to search")
    term = request.GET.get('search')
    policies = search(term)
    print(policies)
    return render(request, 'blog/policy_list.html', {'policies': policies})

