from django.db import models
from django.contrib.auth.models import User
import random

class PlayerQueue(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    @classmethod
    def add_user(cls, user):
        if not cls.objects.filter(user=user).exists():
            cls.objects.create(user=user)

    @classmethod
    def remove_user(cls, user):
        cls.objects.filter(user=user).delete()

    @classmethod
    def get_queue(cls):
        return [queue.user for queue in cls.objects.order_by('timestamp')]

    @classmethod
    def clear_queue(cls):
        cls.objects.all().delete()

class Landmark(models.Model):
    name = models.CharField(max_length=200)
    latitude = models.FloatField()
    longitude = models.FloatField()
    image = models.ImageField(upload_to='landmarks/', null=True, blank=True)
    hint_image = models.ImageField(upload_to='hints/', null=True, blank=True)

    def __str__(self):
        return self.name

class Battle(models.Model):
    player1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='battles_as_player1')
    player2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='battles_as_player2')
    landmark = models.ForeignKey(Landmark, on_delete=models.CASCADE)
    player1_lat = models.FloatField(null=True, blank=True)
    player1_lon = models.FloatField(null=True, blank=True)
    player1_score = models.IntegerField(null=True, blank=True)
    player2_lat = models.FloatField(null=True, blank=True)
    player2_lon = models.FloatField(null=True, blank=True)
    player2_score = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    def create_battle(cls, player1, player2):
        if player1 == player2:
            raise ValueError("Игроки должны быть разными")
        landmarks = Landmark.objects.all()
        if not landmarks.exists():
            raise ValueError("Нет доступных достопримечательностей")
        landmark = random.choice(landmarks)
        battle = cls.objects.create(player1=player1, player2=player2, landmark=landmark)
        return battle