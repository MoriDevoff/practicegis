from django.urls import path
from django.contrib.auth import views as auth_views
from game import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('solo/', views.solo_play, name='solo_play'),
    path('battle/<int:battle_id>/', views.battle_detail, name='battle_detail'),
    path('calculate_score/', views.calculate_score, name='calculate_score'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.logout_view, name='logout'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('online_matchmaking/', views.online_matchmaking, name='online_matchmaking'),
    path('online_matchmaking/check/', views.check_matchmaking, name='check_matchmaking'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)