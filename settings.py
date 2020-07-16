import os
from os import environ
import dj_database_url
#from otree.api import Currency as c, currency_range

import otree.settings

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

#BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']
DEBUG = True
#ADMIN_USERNAME = 'admin'

# for security, best to set admin password in an environment variable
#ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')
#ADMIN_PASSWORD = "pw"
# don't share this with anybody.
#SECRET_KEY = 'l)2(&wh@^_l9@e04v20f#ne-*hw_z!94dz(igf$_m^ifu3g4mp'



SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)


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

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = False

ROOMS = [
    dict(
        name='econ101',
        display_name='Econ 101 class',
        participant_label_file='_rooms/econ101.txt',
    ),
    dict(name='live_demo', display_name='Room for live demo (no participant labels)'),
]

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')
OTREE_PRODUCTION = 1
DEBUG = False
OTREE_AUTH_LEVEL="STUDY"
# for security, best to set admin password in an environment variable
#ADMIN_PASSWORD = "pw"

DEMO_PAGE_INTRO_HTML = """
oTree: Permit Experiments
"""

# don't share this with anybody.
SECRET_KEY = 'p95@c5f=^b3z55a+-ra67(-hj=_a9@fixrdj)n!v03p+goe+xd'

INSTALLED_APPS = ['otree']

