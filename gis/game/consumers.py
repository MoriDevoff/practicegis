from channels.generic.websocket import JsonWebsocketConsumer
from asgiref.sync import async_to_sync
import logging
from .models import Battle, PlayerQueue
from django.contrib.auth import get_user_model

logger = logging.getLogger(__name__)

User = get_user_model()

class MatchmakingConsumer(JsonWebsocketConsumer):
    def connect(self):
        self.accept()
        logger.info(f"WebSocket connected for matchmaking: {self.scope['user'].username}")
        async_to_sync(self.channel_layer.group_add)(
            f"matchmaking_{self.scope['user'].username}",  # Группа для конкретного пользователя
            self.channel_name
        )
        if self.scope['user'].is_authenticated:
            PlayerQueue.add_user(self.scope['user'])
            self.notify_queue_status()

    def disconnect(self, close_code):
        logger.info(f"WebSocket disconnected for matchmaking: {self.scope['user'].username}")
        if self.scope['user'].is_authenticated:
            PlayerQueue.remove_user(self.scope['user'])
        async_to_sync(self.channel_layer.group_discard)(
            f"matchmaking_{self.scope['user'].username}",
            self.channel_name
        )

    def notify_queue_status(self):
        queue = PlayerQueue.get_queue()
        logger.info(f"Queue status: {len(queue)} players")
        # Логика создания боя перенесена в views.py

    def matchmaking_update(self, event):
        self.send_json(event['message'])

class BattleConsumer(JsonWebsocketConsumer):
    def connect(self):
        self.battle_id = self.scope['url_route']['kwargs']['battle_id']
        async_to_sync(self.channel_layer.group_add)(
            f"battle_{self.battle_id}",
            self.channel_name
        )
        self.accept()
        logger.info(f"WebSocket connected for battle {self.battle_id}")
        self.send_json({'action': 'start', 'battle_id': self.battle_id})  # Уведомление о начале боя
        self.send_current_markers()

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
            lat = content.get('lat')
            lon = content.get('lon')
            score = content.get('score')
            user = self.scope['user'].username

            battle = Battle.objects.get(id=battle_id)
            if battle.player1.username == user:
                battle.player1_lat = lat
                battle.player1_lon = lon
                battle.player1_score = score
            elif battle.player2.username == user:
                battle.player2_lat = lat
                battle.player2_lon = lon
                battle.player2_score = score
            battle.save()

            self.send_updated_markers(battle_id)

            if battle.player1_score is not None and battle.player2_score is not None:
                async_to_sync(self.channel_layer.group_send)(
                    f"battle_{battle_id}",
                    {
                        'type': 'battle.finish',
                        'message': {
                            'action': 'finish',
                            'player1_score': battle.player1_score,
                            'player2_score': battle.player2_score,
                            'player1_lat': battle.player1_lat,
                            'player1_lon': battle.player1_lon,
                            'player2_lat': battle.player2_lat,
                            'player2_lon': battle.player2_lon
                        }
                    }
                )

    def battle_update(self, event):
        self.send_json(event['message'])

    def battle_finish(self, event):
        self.send_json(event['message'])

    def send_current_markers(self):
        battle = Battle.objects.get(id=self.battle_id)
        markers = {}
        if battle.player1_lat and battle.player1_lon:
            markers['player1'] = {
                'lat': battle.player1_lat,
                'lon': battle.player1_lon,
                'score': battle.player1_score or 0,
                'username': battle.player1.username
            }
        if battle.player2_lat and battle.player2_lon:
            markers['player2'] = {
                'lat': battle.player2_lat,
                'lon': battle.player2_lon,
                'score': battle.player2_score or 0,
                'username': battle.player2.username
            }
        self.send_json({'action': 'update_markers', 'markers': markers})

    def send_updated_markers(self, battle_id):
        battle = Battle.objects.get(id=battle_id)
        markers = {}
        if battle.player1_lat and battle.player1_lon:
            markers['player1'] = {
                'lat': battle.player1_lat,
                'lon': battle.player1_lon,
                'score': battle.player1_score or 0,
                'username': battle.player1.username
            }
        if battle.player2_lat and battle.player2_lon:
            markers['player2'] = {
                'lat': battle.player2_lat,
                'lon': battle.player2_lon,
                'score': battle.player2_score or 0,
                'username': battle.player2.username
            }
        async_to_sync(self.channel_layer.group_send)(
            f"battle_{battle_id}",
            {
                'type': 'battle.update',
                'message': {'action': 'update_markers', 'markers': markers}
            }
        )

    def battle_start(self, event):
        self.send_json(event)  # Передаём сообщение о начале боя