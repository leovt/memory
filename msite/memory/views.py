from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponseForbidden, JsonResponse
from django.views.generic import View
from django.core.urlresolvers import reverse
from django.views.decorators.http import last_modified
from django.utils.decorators import classonlymethod
from .models import Game, Player, Card

def get_player(request):
    """
    get the player object of the player making the request.
    the player is identified by a cookie
    """
    player_id = request.COOKIES.get('player_id', '')
    try:
        return Player.objects.get(secretid=player_id)
    except Player.DoesNotExist:
        return None

class GameViewJSON(View):
    @classonlymethod
    def as_conditional_view(cls, *args, **kwargs):
        def last_modified_func(request, urlid):
            game = get_object_or_404(Game, urlid=urlid)
            return game.last_modified
        return last_modified(last_modified_func)(cls.as_view(*args, **kwargs))

    def get(self, request, urlid):
        game = get_object_or_404(Game, urlid=urlid)
        player = get_player(request)
            
        response = {
            'status': game.get_status_display(),
            'players': {'player%d' % p.id:
                {'name': p.name,
                 'score': p.score,
                 'is_current_player': p.is_current_player()}
                for p in game.players.all()},
            'message': game.message(),
            'cards': {'card%d' % c.id:{
                 'visible': c.visible(),
                 'bgpos': (('-%dpx -%dpx' % (c.image.offset_x, c.image.offset_y))
                           if c.status == Card.STATUS_FRONTSIDE else '')}
                for c in game.cards.all()}
        }
        player = get_player(request)
        if player and player.game == game:
            response['player'] = {
                'name': player.name,
                'can_act': player.can_act(),
                'should_refresh': player.should_refresh()}
        
        return JsonResponse(response)

class GameView(View):
    def get(self, request, urlid):
        accept = request.META.get('HTTP_ACCEPT')
        if 'json' in accept:
            return HttpResponseRedirect(reverse('memory:game_json', args=(urlid,)))
        return self.get_html(request, urlid)

    def get_html(self, request, urlid):
        game = get_object_or_404(Game, urlid=urlid)

        player = get_player(request)

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
            if card_id.isdigit():
                try:
                    card = game.cards.get(id=card_id)
                except Card.DoesNotExist:
                    pass
                else:
                    game.show_card(card)
            
        accept = request.META.get('HTTP_ACCEPT')
        if 'json' in accept:
            return HttpResponseRedirect(reverse('memory:game_json', args=(urlid,)))
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
