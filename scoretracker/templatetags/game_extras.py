from django import template
from scoretracker.models import Game

register = template.Library()

@register.filter
def get_score(game, user):

    return game.get_score_for_user(user)


@register.inclusion_tag("scoretracker/game_overview.html")
def get_game_data(game,user):
    user_score = game.get_score_for_user(user)
    return {
        'game':game,
        'gameusers':game.users.all(),
        'user':user,
        'user_score': user_score
    }
