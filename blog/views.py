from django.shortcuts import render
from django.utils import timezone
#from .models import Post
from .models import Policy

# Create your views here.

def policy_list(request):
    policies = Policy.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/policy_list')
