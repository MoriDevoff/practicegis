from django.db import models
from django.contrib.auth.models import User

class Landmark(models.Model):
    name = models.CharField(max_length=200)
    latitude = models.FloatField()
    longitude = models.FloatField()
    image = models.ImageField(upload_to='landmarks/', null=True, blank=True)
    hint_image = models.ImageField(upload_to='hints/', null=True, blank=True)

    def __str__(self):
        return self.name

class SoloGame(models.Model):
    player = models.ForeignKey(User, on_delete=models.CASCADE)
    landmark = models.ForeignKey(Landmark, on_delete=models.CASCADE)
    player_lat = models.FloatField()
    player_lon = models.FloatField()
    score = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.player.username} - {self.landmark.name} - {self.score} points"