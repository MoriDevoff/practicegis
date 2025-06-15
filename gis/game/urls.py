from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from game import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),  # Добавляем маршрут для корневого пути
    path('solo/', views.solo_play, name='solo_play'),
    path('calculate_score/', views.calculate_score, name='calculate_score'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.logout_view, name='logout'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)