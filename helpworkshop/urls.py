# helpworkshop/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.help_home, name='help_home'),
    path('faq/', views.faq_view, name='faq'),
    path('contact/', views.contact_support, name='contact_support'),
]
