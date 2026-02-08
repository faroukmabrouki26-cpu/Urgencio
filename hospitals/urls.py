from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('hospitals/', views.hospital_list, name='hospital_list'),
    path('hospital/<int:pk>/', views.hospital_detail, name='hospital_detail'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
