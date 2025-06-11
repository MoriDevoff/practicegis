import folium
import math
import random
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Landmark, Battle
from .forms import RegisterForm, LoginForm

def index(request):
    return render(request, 'game/index.html')

def play(request):
    landmarks = list(Landmark.objects.all())
    if not landmarks:
        return render(request, 'game/play.html', {'error': 'Нет доступных достопримечательностей'})

    landmark = random.choice(landmarks)
    m = folium.Map(location=[landmark.latitude, landmark.longitude], zoom_start=10, tiles='OpenStreetMap')
    m.add_child(folium.LatLngPopup())
    map_html = m._repr_html_()

    context = {
        'landmark': landmark,
        'map_html': map_html,
    }
    return render(request, 'game/play.html', context)

def solo_play(request):
    landmarks = list(Landmark.objects.all())
    if not landmarks:
        return render(request, 'game/solo_play.html', {'error': 'Нет доступных достопримечательностей'})

    landmark = random.choice(landmarks)
    m = folium.Map(location=[0, 0], zoom_start=2, tiles='OpenStreetMap')  # Глобальный вид
    m.add_child(folium.LatLngPopup())
    map_html = m._repr_html_()

    context = {
        'landmark': landmark,
        'map_html': map_html,
    }
    return render(request, 'game/solo_play.html', context)

def calculate_score(request):
    if request.method == 'POST':
        user_lat = float(request.POST.get('lat'))
        user_lon = float(request.POST.get('lon'))
        landmark_id = request.POST.get('landmark_id')
        battle_id = request.POST.get('battle_id', None)

        landmark = Landmark.objects.get(id=landmark_id)
        correct_lat = landmark.latitude
        correct_lon = landmark.longitude

        R = 6371
        dlat = math.radians(correct_lat - user_lat)
        dlon = math.radians(correct_lon - user_lon)
        a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(user_lat)) * math.cos(math.radians(correct_lat)) * math.sin(dlon / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = R * c

        max_distance = 20000
        score = max(0, 5000 * (1 - distance / max_distance))

        if battle_id:
            battle = Battle.objects.get(id=battle_id)
            if battle.player1 == request.user and not battle.player1_score:
                battle.player1_lat = user_lat
                battle.player1_lon = user_lon
                battle.player1_score = score
                battle.save()
            elif battle.player2 == request.user and not battle.player2_score:
                battle.player2_lat = user_lat
                battle.player2_lon = user_lon
                battle.player2_score = score
                battle.save()
                if battle.player1_score and battle.player2_score:
                    battle.winner = battle.player1 if battle.player1_score > battle.player2_score else battle.player2
                    battle.save()

        return JsonResponse({
            'distance': round(distance, 2),
            'score': round(score),
            'correct_lat': correct_lat,
            'correct_lon': correct_lon,
        })
    return JsonResponse({'error': 'Invalid request'}, status=400)

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Аккаунт создан для {username}!')
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
            messages.success(request, 'Вы успешно вошли!')
            return redirect('profile')
    else:
        form = LoginForm()
    return render(request, 'game/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, 'Вы вышли из аккаунта.')
    return redirect('index')

@login_required
def profile(request):
    battles = Battle.objects.filter(player1=request.user) | Battle.objects.filter(player2=request.user)
    return render(request, 'game/profile.html', {'user': request.user, 'battles': battles})

@login_required
def battle_create(request):
    landmark = random.choice(Landmark.objects.all())
    battle = Battle.objects.create(player1=request.user, landmark=landmark)
    return redirect('battle_detail', battle_id=battle.id)

@login_required
def battle_detail(request, battle_id):
    battle = get_object_or_404(Battle, id=battle_id)
    if battle.player1 != request.user and battle.player2 != request.user:
        if not battle.player2:
            battle.player2 = request.user
            battle.save()
        else:
            messages.error(request, 'Это сражение уже занято.')
            return redirect('profile')

    m = folium.Map(location=[battle.landmark.latitude, battle.landmark.longitude], zoom_start=10, tiles='OpenStreetMap')
    m.add_child(folium.LatLngPopup())
    map_html = m._repr_html_()

    context = {
        'battle': battle,
        'landmark': battle.landmark,
        'map_html': map_html,
    }
    return render(request, 'game/battle.html', context)