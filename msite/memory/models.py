from django.db import models

class Game(models.Model):
    STATUS_WAIT_FOR_PLAYERS = 0
    STATUS_NO_CARD_SHOWN = 1
    STATUS_ONE_CARD_SHOWN = 2
    STATUS_GAME_ENDED = 3
    STATUS_CHOICES = (
        (STATUS_WAIT_FOR_PLAYERS, 'wait for players'),
        (STATUS_NO_CARD_SHOWN, 'no card shown'),
        (STATUS_ONE_CARD_SHOWN, 'one_card_shown'),
        (STATUS_GAME_ENDED, 'game ended'))
    
    urlid = models.CharField(max_length=10, unique=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=STATUS_WAIT_FOR_PLAYERS)
    current_player = models.ForeignKey('Player', on_delete=models.PROTECT, related_name='+')

    def __str__(self):
        return self.urlid

class Player(models.Model):
    secretid = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=30)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='players')
    score = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Image(models.Model):
    def __str__(self):
        return 'Image%d' % self.id

class Card(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='cards')
    image = models.ForeignKey(Image, on_delete=models.PROTECT, related_name='+')
    
