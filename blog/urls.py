from django.urls import path
from . import views

urlpatterns = [
    path('', views.search_home, name='index_view'),
    path('policy/', views.policy_search, name='policy-search'),
    path('policy_suggest/', views.series_autocomplete, name='policy-suggest')

]

