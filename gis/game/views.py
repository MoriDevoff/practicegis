import folium
import math
import random
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import login, logout, authenticate
from .forms import RegisterForm, LoginForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Landmark, SoloGame
import logging
from django.db import models

# Настройка логгера
logger = logging.getLogger(__name__)

def index(request):
    return render(request, 'game/index.html')

def solo_play(request):
    landmarks = list(Landmark.objects.all())
    if not landmarks:
        return render(request, 'game/solo_play.html', {'error': 'Нет доступных достопримечательностей'})

    landmark = random.choice(landmarks)

    # Создаем карту с центром в случайном месте (далеко от правильного ответа)
    offset_lat = random.uniform(-20, 20)
    offset_lon = random.uniform(-20, 20)
    map_center = [landmark.latitude + offset_lat, landmark.longitude + offset_lon]

    context = {
        'landmark': landmark,
        'map_center_lat': map_center[0],
        'map_center_lon': map_center[1],
        'correct_lat': landmark.latitude,
        'correct_lon': landmark.longitude,
        'hint_image_url': landmark.hint_image.url if landmark.hint_image else None,
    }
    return render(request, 'game/solo_play.html', context)

def calculate_score(request):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        lat = request.POST.get('lat')
        lon = request.POST.get('lon')
        landmark_id = request.POST.get('landmark_id')

        try:
            landmark = Landmark.objects.get(id=landmark_id)
            lat1, lon1 = float(lat), float(lon)
            lat2, lon2 = landmark.latitude, landmark.longitude

            distance = math.sqrt((lat1 - lat2) ** 2 + (lon1 - lon2) ** 2) * 100
            score = max(0, 1000 - int(distance * 5))

            # Сохраняем результат игры, если пользователь авторизован
            if request.user.is_authenticated:
                SoloGame.objects.create(
                    player=request.user,
                    landmark=landmark,
                    player_lat=lat1,
                    player_lon=lon1,
                    score=score
                )

            return JsonResponse({
                'score': score,
                'correct_lat': landmark.latitude,
                'correct_lon': landmark.longitude
            })

        except (ValueError, Landmark.DoesNotExist) as e:
            logger.error(f"Error in calculate_score: {str(e)}")
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Метод не поддерживается'}, status=400)

@login_required
def profile(request):
    # Получаем последние 10 игр пользователя
    recent_games = SoloGame.objects.filter(player=request.user).order_by('-created_at')[:10]
    
    # Вычисляем статистику
    total_games = SoloGame.objects.filter(player=request.user).count()
    if total_games > 0:
        average_score = SoloGame.objects.filter(player=request.user).aggregate(
            avg_score=models.Avg('score'))['avg_score']
        best_score = SoloGame.objects.filter(player=request.user).order_by('-score').first()
    else:
        average_score = 0
        best_score = None

    context = {
        'user': request.user,
        'recent_games': recent_games,
        'total_games': total_games,
        'average_score': round(average_score, 1) if average_score else 0,
        'best_score': best_score.score if best_score else 0,
    }
    return render(request, 'game/profile.html', context)

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Аккаунт создан для {user.username}!')
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'game/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            logger.info(f"User {user.username} logged in")
            messages.success(request, 'Вы успешно вошли!')
            return redirect('index')
    else:
        form = LoginForm()
    return render(request, 'game/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, 'Вы вышли из аккаунта.')
    return redirect('index')