from django.db import models
import random

def random_id(length):
    CHARACTERS = 'abcdefghijklmnopqrstuvwxyz0123456789'
    return ''.join(random.choice(CHARACTERS) for _ in range(length))

def _default_urlid():
    return random_id(Game._meta.get_field('urlid').max_length)

def _default_secretid():
    return random_id(Player._meta.get_field('secretid').max_length)

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
    NUMBER_OF_PAIRS = 18
    
    urlid = models.CharField(max_length=10, unique=True, default=_default_urlid)
    status = models.IntegerField(choices=STATUS_CHOICES, default=STATUS_WAIT_FOR_PLAYERS)
    current_player = models.ForeignKey('Player', on_delete=models.PROTECT, related_name='+', null=True, blank=True)

    def __str__(self):
        return self.urlid
    
    def new_game(self):
        images = 2 * random.sample(list(Image.objects.all()), Game.NUMBER_OF_PAIRS)
        random.shuffle(images)
        self.save()
        self.cards.set((Card(image=image) for image in images), bulk=False)


class Player(models.Model):
    secretid = models.CharField(max_length=10, unique=True, default=_default_secretid)
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
    
