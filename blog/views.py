from django.shortcuts import render
from django.utils import timezone
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render
from django.views.generic.base import TemplateView
from .models import Policy
from .search import search, get_search_suggestions
import json
import ast

# Create your views here.

def search_home(request):
    return render(request, 'blog/search_home.html')

def policy_search(request):
    term = request.GET.get('search')
    policies = search(term)
    return render(request, 'blog/policy_list.html', {'policies': policies})

# Old autocomplete function using elasticsearch built-in functionality--somewhat works but not very robust
# def series_autocomplete(request):
#     term = request.GET.get('search')
#     print(term)
#     suggestions = get_search_suggestions(term)
#     print("Suggestions: ", suggestions)
#     return JsonResponse({'suggestions': suggestions})

# New autocomplete--more robust, searches over title attribute data

# Problem is that it is currently case sensitive, so you need to type in same case as the actual policies that
# will be suggested. Shouldn't be hard to fix this.
def autocompleteModel(request):
    if request.is_ajax():
        q = request.GET.get('search')
        search_qs = Policy.objects.filter(title__startswith=q)
        results = []
        for r in search_qs:
            results.append(r.title)
        data = json.dumps(results)
    else:
        data = 'fail'
    data = list(set([n.strip() for n in ast.literal_eval(data)]))
    mimetype = 'application/json'
    print("Suggestions: ", data)
    return HttpResponse(data, mimetype)