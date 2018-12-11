from django.urls import path
# from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('', views.index),
    path('contracts/', views.ContractList.as_view()),
    path('contracts/<int:pk>/', views.ContractDetail.as_view()),
    path('clients/', views.ClientList.as_view()),
    path('clients/<int:pk>/', views.ClientDetail.as_view()),
]

# urlpatterns = format_suffix_patterns(urlpatterns)
