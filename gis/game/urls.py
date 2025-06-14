from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from game import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),  # Добавляем маршрут для корневого пути
    path('solo/', views.solo_play, name='solo_play'),
    # path('play/', views.play, name='play'), # Закомментирована строка, ссылающаяся на views.play
    path('battle/<int:battle_id>/', views.battle_detail, name='battle_detail'),
    path('calculate_score/', views.calculate_score, name='calculate_score'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.logout_view, name='logout'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('online_matchmaking/', views.online_matchmaking, name='online_matchmaking'),
    path('online_matchmaking/check/', views.check_matchmaking, name='check_matchmaking'),
    path('validate_field/', views.validate_field, name='validate_field'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)