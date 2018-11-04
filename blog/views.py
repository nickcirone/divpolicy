from django.shortcuts import render
from django.utils import timezone
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render
from django.views.generic.base import TemplateView
from .models import Policy
from .search import search, search_suggest
import json
import ast

# Create your views here.

def search_home(request):
    return render(request, 'blog/search_home.html')

def policy_search(request):
    term = request.GET.get('search')
    policies = search(term)
    return render(request, 'blog/policy_list.html', {'policies': policies})


# Autocomplete function -- takes text as it is being typed into the search bar, runs a simple prefix search over
# just the "title" field, and returns a list of the matches which will then be displayed as suggestions from the
# search bar to the user

def autocompleteModel(request):
    if request.is_ajax():
        q = request.GET.get('search')
        search_qs = search_suggest(q)
        results = []
        for r in search_qs:
            results.append(r.title.lower())
        data = json.dumps(results)
    else:
        data = 'fail'
    data = list(set([n.strip() for n in ast.literal_eval(data)]))[:10]
    mimetype = 'application/json'
    print("Text: ", q)
    print("Suggestions: ", data)
    return HttpResponse(data, mimetype)