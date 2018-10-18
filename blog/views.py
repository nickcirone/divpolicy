from django.shortcuts import render
from django.utils import timezone
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from django.views.generic.base import TemplateView
from .models import Policy
from .search import search, get_search_suggestions

# Create your views here.

def search_home(request):
    return render(request, 'blog/search_home.html')

def policy_search(request):
    term = request.GET.get('search')
    policies = search(term)
    return render(request, 'blog/policy_list.html', {'policies': policies})

# current problem is that this function is not being properly called in url.py -- if you swap the order between this
# and policy_search, it works, so I'm not sure how to make it so that both functions will get called, not just the
# first one. Could combine the two functions, but the issue is that series_autocomplete must be called as the user
# is typing, while policy_search should only be called when the user clicks search.

def series_autocomplete(request):
    term = request.GET.get('search')
    suggestions = get_search_suggestions(term)
    print("Suggestions: ", suggestions)
    return render(request, 'blog/policy_list.html', {'suggestions': suggestions})
