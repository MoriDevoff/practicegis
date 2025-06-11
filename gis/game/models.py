from django.db import models
from django.contrib.auth.models import User

class Landmark(models.Model):
    name = models.CharField(max_length=200)
    latitude = models.FloatField()
    longitude = models.FloatField()
    image = models.ImageField(upload_to='landmarks/')

    def __str__(self):
        return self.name

class Battle(models.Model):
    player1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='battle_player1')
    player2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='battle_player2', null=True)
    landmark = models.ForeignKey(Landmark, on_delete=models.CASCADE)
    player1_lat = models.FloatField(null=True)
    player1_lon = models.FloatField(null=True)
    player1_score = models.IntegerField(null=True)
    player2_lat = models.FloatField(null=True)
    player2_lon = models.FloatField(null=True)
    player2_score = models.IntegerField(null=True)
    winner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='battle_winner', null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Сражение {self.player1} vs {self.player2 if self.player2 else 'Ожидает'}"