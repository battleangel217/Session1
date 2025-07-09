from django.db import models

# Create your models here.

class Room(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.IntegerField(primary_key=True)
    done_voting = models.CharField(max_length=100, default="False")
    started = models.CharField(default="Open")

class Player(models.Model):
    username = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=100, default='Not Mafia')
    vote = models.IntegerField(default=0)
    submitted = models.CharField(max_length=100, default="False")
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='room_code')

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f"{self.name}"
