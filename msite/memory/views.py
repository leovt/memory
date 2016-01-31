from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect

from .models import Game

def game(request, urlid):
    game = get_object_or_404(Game, urlid=urlid)
    return render(request, 'memory/game.html', {
        'game': game})

def welcome(request):
    if request.method == 'POST':
        game = Game()
        game.save()
        return HttpResponseRedirect(game.get_absolute_url())
    else:
        return render(request, 'memory/newgame.html')
