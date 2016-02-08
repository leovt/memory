from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponseForbidden, JsonResponse
from django.views.generic import View
from django.core.urlresolvers import reverse

from .models import Game, Player, Card

class GameView(View):

    def get(self, request, urlid):
        accept = request.META.get('HTTP_ACCEPT')
        if 'json' in accept:
            return self.get_json(request, urlid)
        return self.get_html(request, urlid)

    def get_json(self, request, urlid):
        game = get_object_or_404(Game, urlid=urlid)
        return JsonResponse({
            'status': game.get_status_display(),
            'players': {'player%d' % p.id:
                {'name': p.name,
                 'score': p.score,
                 'is_current_player': p.is_current_player()}
                for p in game.players.all()},
            'cards': {'card%d' % c.id:{
                 'visible': c.visible(),
                 'bgpos': (('-%dpx -%dpx' % (c.image.offset_x, c.image.offset_y))
                           if c.status == Card.STATUS_FRONTSIDE else '')}
                for c in game.cards.all()}
        })

    def get_html(self, request, urlid):
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

        response = render(request, 'memory/game.html', {
            'game': game, 'player':player})
        # response.setdefault('refresh', '2')
        return response

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

        elif game.status == Game.STATUS_GAME_ENDED:
            game.new_game()
            game.save()

        elif game.current_player == player:
            card_id = request.POST.get("card", "")
            try:
                card = game.cards.get(id=card_id)
            except Card.DoesNotExist:
                return HttpResponseForbidden()
            game.show_card(card)
            
        return HttpResponseRedirect(game.get_absolute_url())


class Welcome(View):
    def post(self, request):
        '''create a new game and redict to it'''
        name = request.POST.get("name", "")

        if not name:
            return render(request, 'memory/newgame.html', {'error': 'please enter a name'})

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
