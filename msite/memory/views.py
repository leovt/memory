from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.views.generic import View
from django.core.urlresolvers import reverse

from .models import Game, Player

class GameView(View):

    def get(self, request, urlid):
        game = get_object_or_404(Game, urlid=urlid)

        player_id = request.COOKIES.get('player_id', '')
        try:
            player = Player.objects.get(secretid=player_id)
        except Player.DoesNotExist:
            player = None

        if game.status == Game.STATUS_WAIT_FOR_PLAYERS:
            if player and player.game == game:
                return render(request, 'memory/wait.html', {
                    'game': game, 'player':player})
            else:
                return render(request, 'memory/join.html', {
                    'game': game, 'player':player})

        return render(request, 'memory/game.html', {
            'game': game, 'player':player})

    def post(self, request, urlid):
        game = get_object_or_404(Game, urlid=urlid)

        player_id = request.COOKIES.get('player_id', '')
        try:
            player = Player.objects.get(secretid=player_id)
        except Player.DoesNotExist:
            player = None

        if game.status == Game.STATUS_WAIT_FOR_PLAYERS:
            if player and player.game == game:
                return HttpResponseRedirect(game.get_absolute_url())

            name = request.POST.get("name", "")

            if not name:
                return render(request, 'memory/join.html', {'error': 'please enter a name', 'game':game})

            player = Player(name=name)

            player = Player(game=game, name=name)
            player.save()

            game.new_game()
            game.save()

            assert game.players.count() == 2, 'expected exactly two players'

            response = HttpResponseRedirect(game.get_absolute_url())
            response.set_cookie('player_id', player.secretid, path=game.get_absolute_url())
            return response
        return HttpResponseRedirect(game.get_absolute_url())


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
