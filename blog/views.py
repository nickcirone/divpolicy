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
from django.core.paginator import Paginator, Page

class DSEPaginator(Paginator):
    """
    Override Django's built-in Paginator class to take in a count/total number of items;
    Elasticsearch provides the total as a part of the query results, so we can minimize hits.
    """
    def __init__(self, *args, **kwargs):
        super(DSEPaginator, self).__init__(*args, **kwargs)
        self._count = self.object_list.hits.total

    def page(self, number):
        # this is overridden to prevent any slicing of the object_list - Elasticsearch has
        # returned the sliced data already.
        number = self.validate_number(number)
        return Page(self.object_list, number, self)

def search_home(request):
    return render(request, 'blog/search_home.html')

def policy_search(request):
    term = request.GET.get('search')
    policies = search(term)

    page = int(request.GET.get('page', '1'))
    start = (page - 1) * 10
    end = start + 10


    paginator = DSEPaginator(policies, 10)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

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
    print("Text: ", q)
    query_length = len(q)
    print("Suggestions: ", data)

    # check for 'part' and numbers and maybe skip over ones with commas and limit the length of suggestions
    for i in range(len(data)):
        new_list = data[i].split(" ")
        if query_length < 3:
            #Allow suggestions up to length 2
            if len(new_list) > 1:
                data[i] = ""
                continue
        elif query_length >= 3 and query_length <= 10:
            #Allow suggestions up to length 6
            if len(new_list) > 8:
                data[i] = ""
                continue
        else:
            #Allow suggestions up to length 9
            if len(new_list) > 11:
                data[i] = ""
                continue
        for j in range(len(new_list)):
            if new_list[j] == "part":
                data[i] = " ".join(new_list[:j])
                break
            if not new_list[j].isalpha() and new_list[j] != " ":
                data[i] = " ".join(new_list[:j])
                break
    data = list(set(data))
    data = list(filter(None, data))
    data.sort(key=lambda s: len(s))

    return JsonResponse({ 'suggestions': data })