from state_machine import StateMachine


class BaseGameEntity:

    _next_id = 0

    def __init__(self):
        BaseGameEntity._next_id += 1
        self._id = BaseGameEntity._next_id

        # Entities has a "pointer" to the game containing it.
        # This allows to use missage_dispatcher in the game avoiding
        # global variables or cross modules.
        self.game = None

    @property
    def id(self):
        return self._id

    def update(self):
        raise NotImplementedError('Entity does not implement update function')

    def handle_message(self, t):
        raise NotImplementedError('Entity does not implement message handling')

# A superclass "Character" could be valuable to group data and functions common
# to Miner and Wife, and make easier to add new characters to the game.
class Miner(BaseGameEntity):

    max_fatigue = 10
    max_thirst = 10
    max_gold = 10
    comfort_level = 20

    def __init__(self, name, global_state=None, current_state=None):
        BaseGameEntity.__init__(self)

        self._name = name
        self.state_machine = StateMachine(self)
        self.location = None

        self._gold_carried = 0
        self._money_in_bank = 0
        self._thirst = 0
        self._fatigue = 0

        # Relations
        self.wife = None

        # Initial states
        self.state_machine.global_state = global_state
        self.state_machine.current_state = current_state

    @property
    def name(self):
        return self._name

    @property
    def money_in_bank(self):
        return self._money_in_bank

    def update(self):
        self._thirst += 1
        self.state_machine.update()

    def handle_message(self, t):
        self.state_machine.handle_message(t)

    def change_location(self, new_location):
        self.location = new_location

    def add_to_gold_carried(self, value):
        self._gold_carried += value

        # Assuming you can add negative amount of gold...
        if self._gold_carried < 0:
            self._gold_carried = 0

    def add_to_wealth(self):
        self._money_in_bank += self._gold_carried
        self._gold_carried = 0

    def increase_fatigue(self):
        self._fatigue += 1

    def decrease_fatigue(self):
        self._fatigue -= 1

    def buy_and_drink_wiskey(self):
        self._thirst = 0
        self._money_in_bank -= 2

    def pockets_full(self):
        return self._gold_carried >= Miner.max_gold

    def thirsty(self):
        return self._thirst >= Miner.max_thirst

    def wealthy(self):
        return self._money_in_bank >= Miner.comfort_level

    def fatigued(self):
        return self._fatigue >=  Miner.max_fatigue

    def say(self, s):
        print('\x1b[0;32;40m' + '{0} : '.format(self.name) + s + '\x1b[0m')


class Wife(BaseGameEntity):
    def __init__(self, name, global_state=None, current_state=None):
        BaseGameEntity.__init__(self)

        self._name = name
        self.state_machine = StateMachine(self)
        self.location = None

        self.cooking = False
        self.husband = None

        self.state_machine.global_state = global_state
        self.state_machine.current_state = current_state

    @property
    def name(self):
        return self._name

    def update(self):
        self.state_machine.update()

    def handle_message(self, t):
        self.state_machine.handle_message(t)

    def change_location(self, new_location):
        self.location = new_location

    def say(self, s):
        print('\x1b[0;31;40m' + '{0} : '.format(self.name) + s + '\x1b[0m')
