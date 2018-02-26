import random
from messages import Message


class WifeGlobalState:

    @staticmethod
    def execute(wife):
        if random.random() < 0.1:
            wife.state_machine.change_state(GoBathroom)

    @staticmethod
    def on_message(wife, message):
        if message.message == Message.HI_HONEY:
            wife.say('Hi Honey. Let me make you some of mah fine country stew.')
            wife.state_machine.change_state(CookStew)
            return True

        return False


class DoHouseWork:

    @staticmethod
    def enter(wife):
        pass

    @staticmethod
    def execute(wife):
        action = random.randint(0,2)
        if action == 0:
            wife.say('Making the bed')
        elif action == 1:
            wife.say('Washing the dishes')
        else:
            wife.say('Mopping the floor')

    @staticmethod
    def exit(wife):
        pass

    @staticmethod
    def on_message(wife, message):
        return False


class GoBathroom:

    @staticmethod
    def enter(wife):
        wife.say("Walkin' to the can. Need to powda mah pretty li'l nose")

    @staticmethod
    def execute(wife):
        wife.say('Ahhhhhh! Sweet relief!')
        wife.state_machine.revert_previous_state()

    @staticmethod
    def exit(wife):
        wife.say('Leaving the john')

    @staticmethod
    def on_message(wife, message):
        return False


class CookStew:

    @staticmethod
    def enter(wife):
        if not wife.cooking:
            wife.say('Putting the stew in the oven.')
            wife.game.message_dispatcher.dispatch_message(wife, wife, Message.STEW_READY, 2)
        wife.cooking = True

    @staticmethod
    def execute(wife):
        wife.say('Fussing over food.')

    @staticmethod
    def exit(wife):
        wife.say('Putting the stew on the table')

    @staticmethod
    def on_message(wife, message):
        if message.message == Message.STEW_READY:
            wife.say('Stew Ready! Lets eat')
            wife.game.message_dispatcher.dispatch_message(wife, wife.husband, Message.STEW_READY)
            wife.cooking = False
            wife.state_machine.change_state(DoHouseWork)
            return True

        return False

