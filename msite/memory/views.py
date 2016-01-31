from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.views.generic import View
from django.core.urlresolvers import reverse

from .models import Game, Player

def game(request, urlid):
    game = get_object_or_404(Game, urlid=urlid)

    player_id = request.COOKIES.get('player_id', '')
    try:
        player = game.players.get(secretid=player_id)
    except Player.DoesNotExist:
        player = None


    return render(request, 'memory/game.html', {
        'game': game, 'player':player})

class Welcome(View):
    def post(self, request):
        '''create a new game and redict to it'''
        name = request.POST.get("name", "")

        if not name:
            return render(request, 'memory/newgame.html', {'error': 'please enter a name'})

        player = Player(name=name)

        game = Game()
        game.save()
        player = Player(game=game, name=name)
        player.save()

        response = HttpResponseRedirect(game.get_absolute_url())
        response.set_cookie('player_id', player.secretid, path=game.get_absolute_url())
        return response

    def get(self, request):
        '''show a form to enable a user to create a new game'''
        return render(request, 'memory/newgame.html')
