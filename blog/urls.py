from django.urls import path
from . import views

# Added call to the new (10/28) autocomplete function instead of previous one
urlpatterns = [
    path('', views.search_home, name='index_view'),
    path('policy/', views.policy_search, name='policy-search'),
    path('policy_suggest/', views.autocompleteModel, name='policy-suggest')
]

