from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('play/', views.play, name='play'),
    path('solo/', views.solo_play, name='solo_play'),
    path('calculate_score/', views.calculate_score, name='calculate_score'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('battle/create/', views.battle_create, name='battle_create'),
    path('battle/<int:battle_id>/', views.battle_detail, name='battle_detail'),
]