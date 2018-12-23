from django.urls import path
# from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('', views.index),
    path('contracts/', views.ContractList.as_view()),
    path('contracts/<int:pk>/', views.ContractDetail.as_view()),
    path('clients/', views.ClientList.as_view()),
    path('clients/<int:pk>/', views.ClientDetail.as_view()),
    path('countersigns/', views.CountersignList.as_view()),
    path('countersigns/<int:pk>/', views.CountersignDetail.as_view()),
    path('reviews/', views.ReviewList.as_view()),
    path('reviews/<int:pk>/', views.ReviewDetail.as_view()),
    path('signs/', views.SignList.as_view()),
    path('signs/<int:pk>/', views.SignDetail.as_view()),
    path('roles/', views.RoleList.as_view()),
    path('roles/<int:pk>/', views.RoleDetail.as_view()),
    path('register/', views.Register.as_view()),
]

# urlpatterns = format_suffix_patterns(urlpatterns)
