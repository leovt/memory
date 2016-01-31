from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.views.generic import View

from .models import Game

def game(request, urlid):
    game = get_object_or_404(Game, urlid=urlid)
    return render(request, 'memory/game.html', {
        'game': game})

class Welcome(View):
    def post(self, request):
        '''create a new game and redict to it'''
        game = Game()
        game.save()
        return HttpResponseRedirect(game.get_absolute_url())

    def get(self, request):
        '''show a form to enable a user to create a new game'''
        return render(request, 'memory/newgame.html')
