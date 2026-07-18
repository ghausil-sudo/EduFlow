from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('tentang/', views.about, name='about'),
    path('kontak/', views.contact, name='contact'),
]
