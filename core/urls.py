from django.urls import path
from core import views

urlpatterns = [
    path('',views.index,name="index"),
    path('register',views.register,name='register'),
    path('login',views.login,name='login'),
    path('logout',views.logout,name='logout'),
    path('blog',views.blog,name='blog'),
]