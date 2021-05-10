from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index,name='index'),
    path('login', views.user_login,name='login'),
    path('logout', views.user_logout,name='logout'),
    path('register', views.register,name="register"),
    path('user_dashboard', views.user_profile,name="user_profile"),
    path('librarian', views.admin_panel,name="admin_panel"),
    path('user_dashboard/<int:id>/', views.user_details,name="user_details"),
    path('user_dashboard/<int:us_id>/<int:id>/', views.update_data, name="updatedata"),
    path('delete/<int:id>/', views.delete_data, name="deletedata"),
]
