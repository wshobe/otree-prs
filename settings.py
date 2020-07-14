import os
from os import environ
import dj_database_url
#from otree.api import Currency as c, currency_range

import otree.settings

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
#print(BASE_DIR)
# the environment variable OTREE_PRODUCTION controls whether Django runs in
# DEBUG mode. If OTREE_PRODUCTION==1, then DEBUG=False
if environ.get('OTREE_PRODUCTION') not in {None, '', '0'}:
    DEBUG = False
else:
    DEBUG = True
OTREE_PRODUCTION = 0
DEBUG = True
ADMIN_USERNAME = 'admin'

# for security, best to set admin password in an environment variable
#ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')
ADMIN_PASSWORD = "pw"
# don't share this with anybody.
SECRET_KEY = 'l)2(&wh@^_l9@e04v20f#ne-*hw_z!94dz(igf$_m^ifu3g4mp'

DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3')
    )
}
# AUTH_LEVEL:
# If you are launching a study and want visitors to only be able to
# play your app if you provided them with a start link, set the
# environment variable OTREE_AUTH_LEVEL to STUDY.
# If you would like to put your site online in public demo mode where
# anybody can play a demo version of your game, set OTREE_AUTH_LEVEL
# to DEMO. This will allow people to play in demo mode, but not access
# the full admin interface.

AUTH_LEVEL = environ.get('OTREE_AUTH_LEVEL')
AUTH_LEVEL = 'STUDY'
# setting for integration with AWS Mturk
#AWS_ACCESS_KEY_ID = environ.get('AWS_ACCESS_KEY_ID')
#AWS_SECRET_ACCESS_KEY = environ.get('AWS_SECRET_ACCESS_KEY')


# e.g. EUR, CAD, GBP, CHF, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = False



SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)

LANGUAGE_CODE = 'en'


# SENTRY_DSN = ''

DEMO_PAGE_INTRO_TEXT = """
oTree: Permit Experiments
"""

#ROOM_DEFAULTS = {}

ROOMS = [
    {
        'name': 'econ_lab',
        'display_name': 'Economics Lab',
        'participant_label_file': 'participants.txt',
    },
]



SESSION_CONFIGS = [
     {
    'name': 'Permit_Auctions',
    'display_name': 'Permit Markets',
    'num_demo_participants': 12,      #12
    'app_sequence': ['permitauctions'],
    'random_start_order': True,
    'permits_persist': True,
    'initial_cap': 66,     #62
    'cap_decrement': 1,
    'initial_ecr_reserve_amount': 16,    #12
    'ecr_trigger_price': 8,
    'ecr_reserve_increment': 3,
    'num_low_emitters': 6,
    'num_high_emitters': 6,
    'supply_step': False,
    'random_seed': 113,
    'output_price_random_seed': 1283,
    'show_instructions': True,
    'last_round': 30,         #30
    'low_emitter_min_cost': 10,
    'low_emitter_max_cost': 28,
    'high_emitter_min_cost': 1,
    'high_emitter_max_cost': 28,
    'low_output_price': 30,
    'high_output_price_increment': 10,
    'payout_rate': 0.025,
    'price_containment_trigger': 12,
    'price_containment_reserve_amount': 10 ,
    'ecr_treatment':'None',
    'allow_deficit_bids': True
     },
    {
        'name': 'permitauctions_test',
        'display_name': "Permit Markets Test",
        'num_demo_participants': 2,
        'app_sequence': ['permitauctions'],
        'random_start_order': True,
        'permits_persist': True,
        'initial_cap': 10,     #62
        'cap_decrement': 1,
        'initial_ecr_reserve_amount': 4,    #12
        'ecr_trigger_price': 8,
        'ecr_reserve_increment': 2,
        'num_low_emitters': 1,
        'num_high_emitters': 1,
        'supply_step': False,
        'random_seed': 113,
        'output_price_random_seed': 1283,
        'show_instructions': True,
        'last_round': 4,         #30
        'low_emitter_min_cost': 10,
        'low_emitter_max_cost': 28,
        'high_emitter_min_cost': 1,
        'high_emitter_max_cost': 28,
        'low_output_price': 30,
        'high_output_price_increment': 10,
        'payout_rate': 0.025,
        'price_containment_trigger': 12,
        'price_containment_reserve_amount': 2 ,
        'ecr_treatment':'None',
        'allow_deficit_bids': True,
    }
]



INSTALLED_APPS = ['otree']

