from django.urls import path

from . import views
from user.views import register
app_name = 'user'

urlpatterns = [
    path('login/', views.user_login, name = 'login'),
    path('logout/', views.user_logout, name = 'logout'),
    path('register/', register.as_view(), name = 'register'), 
    path('dashboard/', views.dashboard, name = 'dashboard'),
]