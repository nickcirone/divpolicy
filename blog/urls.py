from django.urls import path
from . import views

urlpatterns = [
    path('', views.search_home, name='index_view'),
    path('policy/', views.policy_search, name='policy-search'),
    path('policy/', views.series_autocomplete, name='policy-search')

]

