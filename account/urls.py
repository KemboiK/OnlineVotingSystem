from django.urls import path
from . import views


urlpatterns = [
    path('', views.account_login, name="account_login"),
    path('register/', views.account_register, name="account_register"),
    path('logout/', views.account_logout, name="account_logout"),

    # Password reset flow
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('reset-password/', views.reset_password, name='reset_password'),
]
