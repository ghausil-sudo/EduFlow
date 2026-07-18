from django.urls import path
from . import views

urlpatterns = [
    path('', views.package_list, name='package_list'),
    path('pilih/<int:package_id>/', views.purchase_confirm, name='purchase_confirm'),
    path('pilih/kursus/<slug:course_slug>/', views.purchase_confirm, name='purchase_confirm_course'),
    path('bayar/', views.process_payment, name='process_payment'),
    path('instruksi/<str:invoice>/', views.payment_instructions, name='payment_instructions'),
    path('sukses/<str:invoice>/', views.payment_success, name='payment_success'),
]
