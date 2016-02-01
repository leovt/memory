from django.db import models
from django.core.urlresolvers import reverse
import random

def random_id(length):
    """return a random string of given length

    the string is composed of numbers and lowercase letters
    """
    CHARACTERS = 'abcdefghijklmnopqrstuvwxyz0123456789'
    return ''.join(random.choice(CHARACTERS) for _ in range(length))

def _default_urlid():
    """provides the default for Game.urlid"""
    return random_id(Game._meta.get_field('urlid').max_length)

def _default_secretid():
    """provides the default for Player.secretid"""
    return random_id(Player._meta.get_field('secretid').max_length)

class Game(models.Model):
    """represent a game"""
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
    """the id of the game used in urls, should be only known to the players"""

    status = models.IntegerField(choices=STATUS_CHOICES, default=STATUS_WAIT_FOR_PLAYERS)
    """the status of the game"""

    current_player = models.ForeignKey('Player', on_delete=models.PROTECT, related_name='+', null=True, blank=True)
    """the current player, i.e. the player who is currently allowed to perform actions"""

    def __str__(self):
        return self.urlid
    
    def new_game(self):
        """reset the cards used in the game

        clears the cards used for the game and sets up random cards in pairs
        """
        images = 2 * random.sample(list(Image.objects.all()), Game.NUMBER_OF_PAIRS)
        random.shuffle(images)
        self.status = Game.STATUS_NO_CARD_SHOWN
        self.save()
        self.cards.set((Card(image=image) for image in images), bulk=False)

    def get_absolute_url(self):
        return reverse('memory:game', args=[self.urlid])

class Player(models.Model):
    secretid = models.CharField(max_length=10, unique=True, default=_default_secretid)
    """the secret id for identifying the player"""

    name = models.CharField(max_length=30)
    """name or nickname of the player"""

    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='players')
    """the game in which this player is participating"""

    score = models.IntegerField(default=0)
    """the score in the current game"""

    def __str__(self):
        return self.name
    
class Image(models.Model):
    """represent an image which appears on the front of the card"""
    def __str__(self):
        return 'Image%d' % self.id

class Card(models.Model):
    """represent a card in a game"""

    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='cards')
    """the game in which this card is used"""

    image = models.ForeignKey(Image, on_delete=models.PROTECT, related_name='+')
    """the image on the front of the card"""
    
    shown = models.BooleanField(default=False)

