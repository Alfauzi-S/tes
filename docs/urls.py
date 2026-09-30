from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('edit/<int:pk>/', views.edit, name='edit'),
    path('cetak/<int:pk>/', views.cetak, name='cetak'),
    path('hapus/<int:pk>/', views.hapus, name='hapus'),
    path('<str:type>/', views.listing, name='list'),
    path('<str:type>/baru/', views.edit, name='new'),
]
