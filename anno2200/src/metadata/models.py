from django.db import models
from django.utils.text import slugify

class Player(models.Model):
    name = models.CharField(max_length=128)
    photo = models.ImageField(blank=True, null=True)
    fide_number = models.CharField(max_length=32, blank=True, null=True)
    chesscom_account = models.CharField(max_length=32, blank=True, null=True)

class EventManager(models.Manager):
    pass

class Event(models.Model):
    objects = EventManager()
    name = models.CharField(max_length=128)
    location = models.CharField(max_length=128, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    
class MatchManager(models.Manager):
    pass

class Match(models.Model):
    objects = MatchManager()
    date = models.DateField(blank=True, null=True)
    round = models.CharField(max_length=64, blank=True, null=True)
    board = models.CharField(max_length=64, blank=True, null=True)
    event = models.ForeignKey('Event', blank=True, null=True, on_delete=models.CASCADE)
    white = models.ForeignKey('Player', on_delete=models.CASCADE, related_name='white')
    white_elo = models.IntegerField(blank=True, null=True)
    black = models.ForeignKey('Player', on_delete=models.CASCADE, related_name='black')
    black_elo = models.IntegerField(blank=True, null=True)
    result = models.IntegerField(blank=True, null=True)
    book = models.ForeignKey('positions.OpeningBook', blank=True, null=True, on_delete=models.SET_NULL)

    @property
    def date_header(self):
        if self.date:
            return self.date.strftime("%Y.%m.%d")
        return "????.??.??"

    @property
    def result_header(self):
        if self.result == -1:
            return "0-1"
        elif self.result == 0:
            return "1/2-1/2"
        elif self.result == 1:
            return "1-0"
        else:
            return "*"

    @property
    def result_human(self):
        if self.result == -1:
            return "Black"
        elif self.result == 0:
            return "Draw"
        elif self.result == 1:
            return "White"
        else:
            return "No Result"
            
    @property
    def exportName(self):
        return slugify(f"{ self.event.name }.{ self.date_header }.{ self.round }.{ self.white.name }.{ self.black.name }.{ self.result_human }")
    
class MoveManager(models.Manager):
    pass

class Move(models.Model):
    objects = MoveManager()
    match = models.ForeignKey('Match', on_delete=models.CASCADE)
    player = models.ForeignKey('Player', on_delete=models.CASCADE)
    move = models.CharField(max_length=6)
    position = models.ForeignKey('positions.FenPosition', on_delete=models.CASCADE)
