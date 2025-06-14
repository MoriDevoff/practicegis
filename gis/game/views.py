import folium
import math
import random
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import login, logout, authenticate
from .forms import RegisterForm, LoginForm
from datetime import timedelta
from django.utils import timezone
from channels.generic.websocket import JsonWebsocketConsumer
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import PlayerQueue, Battle, Landmark
import logging
import random
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Настройка логгера
logger = logging.getLogger(__name__)

class BattleConsumer(JsonWebsocketConsumer):
    def connect(self):
        self.battle_id = self.scope['url_route']['kwargs']['battle_id']
        async_to_sync(self.channel_layer.group_add)(
            f"battle_{self.battle_id}",
            self.channel_name
        )
        self.accept()
        logger.info(f"WebSocket connected for battle {self.battle_id}")

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            f"battle_{self.battle_id}",
            self.channel_name
        )
        logger.info(f"WebSocket disconnected for battle {self.battle_id}")

    def receive_json(self, content):
        battle_id = content.get('battle_id')
        action = content.get('action')
        logger.info(f"Received WebSocket message: action={action}, battle_id={battle_id}")

        if action == 'update':
            async_to_sync(self.channel_layer.group_send)(
                f"battle_{battle_id}",
                {
                    'type': 'battle.update',
                    'message': 'update'
                }
            )

    def battle_update(self, event):
        self.send_json({
            'action': 'reload'
        })
        logger.info(f"Sent WebSocket reload message for battle {self.battle_id}")

# Очередь для онлайн подбора
online_queue = []
# Хранилище активных боёв
active_battles = {}

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
        battle_id = request.POST.get('battle_id', None)

        try:
            landmark = Landmark.objects.get(id=landmark_id)
            lat1, lon1 = float(lat), float(lon)
            lat2, lon2 = landmark.latitude, landmark.longitude

            distance = math.sqrt((lat1 - lat2) ** 2 + (lon1 - lon2) ** 2) * 100
            score = max(0, 1000 - int(distance * 5))

            if battle_id:
                battle = Battle.objects.get(id=battle_id)
                user = request.user
                logger.info(f"Calculating score for user {user.username} in battle {battle_id}, score: {score}")

                if battle.player1 == user:
                    battle.player1_lat = lat1
                    battle.player1_lon = lon1
                    battle.player1_score = score
                elif battle.player2 == user:
                    battle.player2_lat = lat1
                    battle.player2_lon = lon1
                    battle.player2_score = score
                battle.save()

                # Отправляем обновление через WebSocket
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(
                    f"battle_{battle_id}",
                    {
                        'type': 'battle.update',
                        'message': {
                            'action': 'update',
                            'lat': lat1,
                            'lon': lon1,
                            'score': score,
                            'battle_id': battle_id
                        }
                    }
                )

                return JsonResponse({
                    'score': score,
                    'user': user.username
                })
            else:
                return JsonResponse({
                    'score': score,
                    'correct_lat': landmark.latitude,
                    'correct_lon': landmark.longitude
                })

        except (ValueError, Landmark.DoesNotExist, Battle.DoesNotExist) as e:
            logger.error(f"Error in calculate_score: {str(e)}")
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Метод не поддерживается'}, status=400)

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
            logger.info(f"User {user.username} logged in, session: {request.session.session_key}")
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
    expired_time = timezone.now() - timedelta(minutes=5)
    Battle.objects.filter(player2__isnull=True, created_at__lt=expired_time).delete()
    Battle.objects.filter(player1_score__isnull=True, player2_score__isnull=True, created_at__lt=expired_time).delete()

    battles = Battle.objects.filter(player1=request.user) | Battle.objects.filter(player2=request.user)
    return render(request, 'game/profile.html', {'user': request.user, 'battles': battles})

@login_required
def battle_detail(request, battle_id):
    battle = get_object_or_404(Battle, id=battle_id)
    if battle.player1 != request.user and battle.player2 != request.user:
        messages.error(request, 'У вас нет доступа к этому сражению.')
        return redirect('profile')

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'is_finished': battle.player1_score is not None and battle.player2_score is not None
        })

    m = folium.Map(location=[battle.landmark.latitude, battle.landmark.longitude], zoom_start=10, tiles='OpenStreetMap')
    m.add_child(folium.LatLngPopup())

    # Добавляем маркер для правильного места (зеленый)
    folium.Marker(
        [battle.landmark.latitude, battle.landmark.longitude],
        popup='Правильное место',
        icon=folium.Icon(color='green')
    ).add_to(m)

    # Добавляем метки, если координаты доступны
    if battle.player1_lat and battle.player1_lon and battle.player1_score:
        folium.Marker(
            [battle.player1_lat, battle.player1_lon],
            popup=f'{battle.player1.username}: {battle.player1_score} очков'
        ).add_to(m)
    if battle.player2_lat and battle.player2_lon and battle.player2_score:
        folium.Marker(
            [battle.player2_lat, battle.player2_lon],
            popup=f'{battle.player2.username}: {battle.player2_score} очков'
        ).add_to(m)

    map_html = m._repr_html_()

    context = {
        'battle': battle,
        'landmark': battle.landmark,
        'map_html': map_html,
        'is_finished': battle.player1_score is not None and battle.player2_score is not None,
        'player1_lat': battle.player1_lat,
        'player1_lon': battle.player1_lon,
        'player1_score': battle.player1_score,
        'player2_lat': battle.player2_lat,
        'player2_lon': battle.player2_lon,
        'player2_score': battle.player2_score,
    }
    return render(request, 'game/battle.html', context)

@login_required
def online_matchmaking(request):
    if request.method == 'POST':
        # Проверяем, есть ли пользователь в очереди
        if PlayerQueue.objects.filter(user=request.user).exists():
            messages.info(request, 'Вы уже в очереди на поиск соперника!')
            logger.info(f"User {request.user.username} already in queue")
            return redirect('index')

        # Добавляем пользователя в очередь
        PlayerQueue.objects.create(user=request.user)
        messages.success(request, 'Вы добавлены в очередь для онлайн-сражения!')
        logger.info(f"User {request.user.username} added to queue, total: {PlayerQueue.objects.count()}")

        # Проверяем, достаточно ли игроков для создания боя
        if PlayerQueue.objects.count() >= 2:
            players = PlayerQueue.objects.all()[:2]
            player1 = players[0].user
            player2 = players[1].user
            try:
                landmark = random.choice(Landmark.objects.all())
                battle = Battle.objects.create(
                    player1=player1,
                    player2=player2,
                    landmark=landmark,
                    created_at=timezone.now()
                )
                logger.info(f"Battle {battle.id} created with players {player1.username} vs {player2.username}")

                # Удаляем игроков из очереди
                PlayerQueue.objects.filter(user__in=[player1, player2]).delete()
                logger.info(f"Players {player1.username} and {player2.username} removed from queue")

                # Отправляем уведомление через WebSocket обоим игрокам
                channel_layer = get_channel_layer()
                for player in [player1, player2]:
                    async_to_sync(channel_layer.group_send)(
                        f"matchmaking_{player.username}",  # Группа для конкретного пользователя
                        {
                            'type': 'battle.start',
                            'battle_id': battle.id
                        }
                    )
                logger.info(f"Sent WebSocket start message for battle {battle.id} to {player1.username} and {player2.username}")

                # Перенаправляем обоих игроков на страницу боя
                return redirect('battle', battle_id=battle.id)
            except ValueError as e:
                logger.error(f"Error creating battle: {str(e)}")
                messages.error(request, f"Ошибка создания боя: {str(e)}")
                PlayerQueue.objects.filter(user=request.user).delete()

        return redirect('index')

    return redirect('index')

@login_required
def check_matchmaking(request):
    global online_queue, active_battles
    logger.info(f"Checking matchmaking for user {request.user.username}, queue size: {len(online_queue)}")
    if request.user in online_queue and len(online_queue) >= 2:
        player1 = online_queue.pop(0)
        player2 = online_queue.pop(0)
        landmark = random.choice(Landmark.objects.all())
        battle = Battle.objects.create(
            player1=player1,
            player2=player2,
            landmark=landmark,
            created_at=timezone.now()
        )
        active_battles[battle.id] = True
        logger.info(f"Battle {battle.id} created via check_matchmaking for {player1.username} vs {player2.username}")
        return JsonResponse({'battle_id': battle.id})

    # Проверяем активные бои для текущего пользователя
    for battle_id in list(active_battles.keys()):
        try:
            battle = Battle.objects.get(id=battle_id)
            if battle.player1 == request.user or battle.player2 == request.user:
                logger.info(f"Found active battle {battle_id} for user {request.user.username}")
                return JsonResponse({'battle_id': battle_id})
        except Battle.DoesNotExist:
            del active_battles[battle_id]
            logger.info(f"Removed non-existent battle {battle_id} from active_battles")

    return JsonResponse({})

def validate_field(request):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        field_name = request.POST.get('field_name')
        field_value = request.POST.get('field_value')

        form = UserCreationForm({field_name: field_value}) # Использовать базовую UserCreationForm для частичной валидации
        form.is_valid() # Запустить валидацию

        errors = []
        if field_name in form.errors:
            for error in form.errors[field_name]:
                errors.append(error)
        
        # Специальная обработка для уникальности имени пользователя и email
        if field_name == 'username':
            if User.objects.filter(username=field_value).exists():
                errors.append('Это имя пользователя уже занято.')
        elif field_name == 'email':
            if User.objects.filter(email=field_value).exists():
                errors.append('Этот email уже зарегистрирован.')

        # Обработка для PasswordMismatch при изменении одного из полей пароля
        if field_name in ['password', 'password2']:
            password = request.POST.get('password')
            password2 = request.POST.get('password2')
            if password and password2 and password != password2:
                errors.append('Пароли не совпадают.')

        return JsonResponse({'errors': errors})
    return JsonResponse({'error': 'Метод не поддерживается'}, status=400)