from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
from otree.db.models import Model, ForeignKey
from .generate_random_costs import costs1, assign_costs, generate_output_prices
import operator
import numpy as np
import logging

author = 'Bill Shobe (shobe@virginia.edu)'

doc = """
Permit trading with an emission containment reserve
"""

class Constants(BaseConstants):
    ### App metadata
    name_in_url = 'permit_trading'
    players_per_group = None  # Puts all players in one group
    num_rounds = 30

    ### Production constants
    emission_intensity_high = 2  # permits required per plant ***Change this at your peril!!!
    emission_intensity_low = 1
    production_capacity_high = 4  # number of plants per player
    production_capacity_low = 4
    must_run = 0  # number of plants each player is required to produce from

    high_price_probability = 0.5
    initial_cash_endowment_high = c(150)
    initial_cash_endowment_low = c(50)

    ### Auction details
    #ecr_trigger_price = c(7)  # Price to start removing permits from the pool
    #ecr_reserve_increment = 2
    reserve_price = c(5)  # absolutely no bids below reserve price; don't even let them try
    maximum_bid = c(30)
    bid_price_increment = c(0.5)
    num_bids_high = 5
    num_bids_low = 5

    penalty_amount = c(35)  # Cost of running a plant without necessary permits

    ### Misc
#    payout_rate = 0.01  # Conversion rate from player.money to real-life payout

class Subsession(BaseSubsession):
    number_sold_auction = models.PositiveIntegerField()
    auction_price = models.CurrencyField()
    ecr_reserve_amount_used = models.PositiveIntegerField(initial=0)
    pcr_amount_added = models.PositiveIntegerField(initial=0)
    output_price = models.CurrencyField()
    permits_available = models.IntegerField()
    initial_auction_price = models.CurrencyField()
    show_instructions = models.BooleanField()

    def creating_session(self):
        # This occurs num_rounds times, but all at session start - not for initializing between rounds
        # All random draws must take place once at the start of the process.
        this_session  = self.session
        this_session_config = this_session.config
        self.ecr_reserve_amount_used = this_session_config['initial_ecr_reserve_amount']
        self.permits_available = this_session_config['initial_cap'] - (self.round_number - 1) * this_session_config['cap_decrement']
        num_low_emitters = this_session_config['num_low_emitters']
        num_high_emitters = this_session_config['num_high_emitters']

        if self.round_number == 1:
            # Make initial assignements that only need to be done once
            print('### Creating subsessions')
            #self.group_randomly()
            self.show_instructions = this_session_config['show_instructions']
            for player in self.get_players():
               # Assign high emitter role to those with higher participant numbers (assigned randomly)
               # Participants with lower id's in session are low emitters, others are high emitters
               player.high_emitter = (player.id_in_subsession > num_low_emitters)
               this_participant = player.participant
               # Name information is only stored in the first round and is not propagated
               #this_participant.vars['first_name'] = player.first_name
               #print('### First name:',player.first_name)
               #this_participant.vars['last_name'] = player.last_name
               #this_participant.vars['computing_ID'] = player.computing_ID
               this_participant.vars['high_emitter'] = player.high_emitter
               if player.high_emitter:
                  player.money = Constants.initial_cash_endowment_high
               else:
                  player.money = Constants.initial_cash_endowment_low
            initial_cap = this_session_config['initial_cap']
            cap_decrement = this_session_config['cap_decrement']
            num_rounds = this_session_config['last_round']
            round_numbers = np.arange(1,num_rounds+1)
            max_low_emitter_demand = Constants.production_capacity_low * Constants.emission_intensity_low * num_low_emitters
            max_high_emitter_demand = Constants.production_capacity_high * Constants.emission_intensity_high * num_high_emitters
            #log = logging.getLogger('permitauctionsapp')
            #log.info('creating_session: {}'.format(max_high_emitter_demand))
            #log.info('creating_session: {}'.format(max_low_emitter_demand))
            this_session.vars['costs'] = costs1(self.session,Constants)
            this_session.vars['output_prices'] = generate_output_prices(self.session,Constants)
            this_session.vars['max_low_emitter_demand'] = max_low_emitter_demand
            this_session.vars['max_high_emitter_demand'] = max_high_emitter_demand
            this_session.vars['full_capacity_permit_demand'] = [max_low_emitter_demand + max_high_emitter_demand] * num_rounds
            this_session.vars['period_caps'] = [initial_cap - (round-1)*cap_decrement for round in round_numbers]
            this_session.vars['output_prices_for_table'] = list(map(c,this_session.vars['output_prices']))[:num_rounds]
            this_session.vars['round_numbers'] = np.arange(1,num_rounds+1)
        else:
            self.show_instructions = False
            
        """ 
        The new cost function draws all costs for the entire session. 
        Costs change in each round
        Pass only the session and Constants objects to the cost function 
        """
        all_costs = this_session.vars['costs']
        self.output_price = this_session.vars['output_prices'][self.round_number - 1]
        high_index = -1
        low_index = -1
        for player in self.get_players():
            player.high_emitter = player.participant.vars['high_emitter']
            if self.round_number > 1:
               player.money = 0
            if player.high_emitter:
                high_index += 1
                player.capacity = Constants.production_capacity_high
                player.emission_intensity = Constants.emission_intensity_high
                # TODO: Is this doing what you think it is
                player_index = ((self.round_number - 1) * num_high_emitters) - 1 + high_index
                #log.info('High: player_index: {0}'.format(player_index))
                costs = assign_costs(player,all_costs['high_emitters'],player_index)
            else:
                low_index += 1
                player.capacity = Constants.production_capacity_low
                player.emission_intensity = Constants.emission_intensity_low
                player_index = ((self.round_number - 1) * num_low_emitters) - 1 + low_index
                #log.info('Low: player_index: {0}'.format(player_index))
                costs = assign_costs(player,all_costs['low_emitters'],player_index)
            player.generate_bid_stubs()
            player.generate_unit_stubs(costs)
            # Costs need to be sorted by player
            #player.generate_unit_stubs(self.session.vars['costs'][player.role()][player_index])

    def vars_for_admin_report(self):
        #for p in self.get_players():
        #    bids = p.bid_set.all().filter(bid__isnull=False).order_by('-bid').values('bid', 'accepted','pid_in_group')
        #    'bids': [(index, bid['accepted'], bid['bid']) for index, bid in enumerate(bids)],
        #config = {key: value for key, value in self.session.config.items()}
        #assert False
        players = []
        payoffs = []
        payout_rate = self.session.config['payout_rate']
        for p in self.get_players():
            payoffs.append(p.money * payout_rate)
            players.append(p)
        #payoffs = [p.money * self.session.config['payout_rate'] for p in self.get_players()]
        #players = [p for p in self.get_players()]
        mean = np.mean(payoffs)
        #if self.round_number == 1:
        #    all_costs = self.session.vars['costs']
        #    output_prices = repeat(self.session.vars['output_prices'],48)
        #    net_value = sort(list(map(operator.sub,output_prices, all_costs)), reverse=True)
        return {'payoffs':payoffs,
                'players': players,
                'mean':mean}

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    first_name = models.StringField()
    last_name = models.StringField()
    computing_ID = models.StringField()
    money = models.CurrencyField(initial=0)
    permits = models.PositiveIntegerField(initial=0)
    starting_permits = models.PositiveIntegerField(initial=0)
    capacity = models.PositiveIntegerField()
    emission_intensity = models.PositiveIntegerField()
    permits_purchased_auction = models.PositiveIntegerField()
    penalty = models.CurrencyField()
    high_emitter = models.BooleanField()
    # Need to make the choices array dynamic 
    production_amount = models.PositiveIntegerField(min=Constants.must_run, max=4, choices=range(Constants.must_run,Constants.production_capacity_low+1))
    min_production = models.PositiveIntegerField(initial=0)

    def role(self):
        if self.id_in_subsession > self.session.config['num_low_emitters']:
            return 'high_emitter'
        else:
            return 'low_emitter'

    # Helper function to retrieve bids
    def get_bids(self):
        bid_qs = Bid.objects.filter(player__exact=self).filter(bid__isnull=False)
        return [bids.bid for bids in bid_qs]

    # Helper function to retreive plant costs
    def get_costs(self):
        unit_qs = Unit.objects.filter(player__exact=self).order_by('cost')
        return [unit.cost for unit in unit_qs]

    def generate_bid_stubs(self):
        """
        Create a fixed number of "bid stubs", i.e. bid objects that have places for bids and
        may contain values needed later.
        """
        this_subsession = self.subsession
        if self.high_emitter:
            num_bids = Constants.num_bids_high
        else:
            num_bids = Constants.num_bids_low
        for _ in range(num_bids):
            bid = self.bid_set.create() # create a new bid object as part of the player's bid set
            bid.round = this_subsession.round_number
            bid.pid_in_group = self.id_in_group
            bid.subsession_id = this_subsession.id
            bid.save()   # important: save to DB!
            if self.high_emitter:
                bid2 = self.bid_set.create() # Double the bids for high emitters
                bid2.round = this_subsession.round_number
                bid2.pid_in_group = self.id_in_group
                bid2.subsession_id = this_subsession.id
                bid2.save()

    def generate_unit_stubs(self, player_costs):
        """
        Create a fixed number of production unit stubs.
        """
        this_subsession_id = self.subsession.id
        player_costs = sorted(player_costs)
        if self.high_emitter:
            capacity = Constants.production_capacity_high
        else:
            capacity = Constants.production_capacity_low
        for i in range(capacity):
            unit = self.unit_set.create() # add new production unit to set
            unit.unit_num = i
            unit.cost = player_costs[i]
            unit.subsession_id = this_subsession_id
            unit.save() # important: save to DB!


class Bid(Model):  # inherits from Django's base "Model"
    BID_CHOICES = currency_range(c(Constants.reserve_price), c(Constants.maximum_bid), c(Constants.bid_price_increment))
    round = models.PositiveIntegerField()
    bid = models.CurrencyField(choices=BID_CHOICES)
    accepted = models.PositiveIntegerField()
    pid_in_group = models.PositiveIntegerField()
    subsession_id = models.PositiveIntegerField()
    player = ForeignKey(Player, on_delete=models.CASCADE)    # creates 1:m relation -> this bid was made by a certain player


class Unit(Model):  # inherits from Django's base "Model"
    unit_num = models.IntegerField()
    cost = models.CurrencyField()
    unit_used = models.PositiveIntegerField()
    subsession_id = models.PositiveIntegerField()
    player = ForeignKey(Player, on_delete=models.CASCADE)
    
