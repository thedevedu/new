from django.conf.urls import include
from django.urls import path
from . import views

urlpatterns = [
    path('', views.networks, name="networks"),
    path('<str:pk>/', views.network, name="network"),
    path('i18n/', include('django.conf.urls.i18n')),
    path('gift/create/', views.createNetwork, name="create-network"),
    path('gift/update/<str:pk>/', views.updateNetwork, name="update-network"),
    path('gift/delete/<str:pk>/', views.deleteNetwork, name="delete-network"),
    path('gift/test/', views.rate_limiting),
]
