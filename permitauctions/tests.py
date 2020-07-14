from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants


class PlayerBot(Bot):

    def play_round(self):
        yield pages.Signin, dict(first_name="Bob", last_name='Jones', computing_ID='wms5f') #'first_name', 'last_name', 'computing_ID'
        yield (pages.Instructions1)
