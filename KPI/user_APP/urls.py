from django.urls import path

from user_APP import views

urlpatterns = [
    path('sign-up/', views.register_view, name='register_page'),
    path('sign-in/', views.login_view, name='login_page'),
    path('logout/', views.logout_view, name='logout_page'),
]
