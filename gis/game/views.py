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
from django.contrib.auth.models import User

# Настройка логгера
logger = logging.getLogger(__name__)

def index(request):
    return render(request, 'game/index.html')

def solo_play(request):
    landmarks = list(Landmark.objects.all())
    if not landmarks:
        return render(request, 'game/solo_play.html', {'error': 'Нет доступных достопримечательностей'})

    landmark = random.choice(landmarks)

    # Центрируем карту ближе к правильному месту (случайное смещение не более 5 градусов)
    offset_lat = random.uniform(-5, 5)
    offset_lon = random.uniform(-5, 5)
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

            # Используем геодезическое расстояние (Haversine formula)
            def haversine(lat1, lon1, lat2, lon2):
                from math import radians, sin, cos, sqrt, atan2
                R = 6371  # Earth radius in km
                dlat = radians(lat2 - lat1)
                dlon = radians(lon2 - lon1)
                a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
                c = 2 * atan2(sqrt(a), sqrt(1 - a))
                return R * c

            distance_km = haversine(lat1, lon1, lat2, lon2)

            # Новая система начисления очков: более плавная и дружелюбная для городских расстояний
            if distance_km < 1:
                score = 1000
            elif distance_km < 5:
                score = int(900 + (1000 - 900) * (5 - distance_km) / 4)
            elif distance_km < 15:
                score = int(800 + (900 - 800) * (15 - distance_km) / 10)
            elif distance_km < 30:
                score = int(700 + (800 - 700) * (30 - distance_km) / 15)
            elif distance_km < 50:
                score = int(600 + (700 - 600) * (50 - distance_km) / 20)
            elif distance_km < 100:
                score = int(500 + (600 - 500) * (100 - distance_km) / 50)
            elif distance_km < 1000:
                score = int(500 * (1000 - distance_km) / 900)
            else:
                score = 0
            score = max(0, score)

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

def validate_field(request):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        field_name = request.POST.get('field_name')
        field_value = request.POST.get('field_value')
        errors = []

        if field_name == 'username':
            if len(field_value) < 3:
                errors.append('Имя пользователя должно содержать минимум 3 символа')
            if User.objects.filter(username=field_value).exists():
                errors.append('Это имя пользователя уже занято')
        elif field_name == 'email':
            if not '@' in field_value or not '.' in field_value:
                errors.append('Введите корректный email адрес')
            if User.objects.filter(email=field_value).exists():
                errors.append('Этот email уже зарегистрирован')
        elif field_name in ['password', 'password2']:
            password = request.POST.get('password', '')
            password2 = request.POST.get('password2', '')
            if field_name == 'password' and len(password) < 8:
                errors.append('Пароль должен содержать минимум 8 символов')
            if field_name == 'password2' and password != password2:
                errors.append('Пароли не совпадают')

        return JsonResponse({'errors': errors})
    return JsonResponse({'error': 'Метод не поддерживается'}, status=400)