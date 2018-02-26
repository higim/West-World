from location import Location
from messages import Message


class EnterMineAndDigForNugget:

    @staticmethod
    def enter(miner):
        if miner.location != Location.GOLDMINE:
            miner.say('Walking to the goldmine.')

        miner.change_location(Location.GOLDMINE)

    @staticmethod
    def execute(miner):
        miner.add_to_gold_carried(1)
        miner.increase_fatigue()

        miner.say('Picking up a nugget')

        """
        Original code has two if conditions to test gold and thirst, this
        provokes strange behaviour if both conditions are true. To avoid
        it, and elif clause has been added to select behaviour: go to
        the bank is more important than go to the saloon.
        """
        if miner.pockets_full():
            miner.state_machine.change_state(VisitBankAndDepositGold)
        elif miner.thirsty():
            miner.state_machine.change_state(QuenchThirst)

    @staticmethod
    def exit(miner):
        miner.say("Ah'm leavin' the gold mine with mah pockets full o' sweet gold")

    @staticmethod
    def on_message(miner, message):
        return False


class VisitBankAndDepositGold:

    @staticmethod
    def enter(miner):
        if miner.location != Location.BANK:
            miner.say('Walking to the bank. Yes sireee.')

        miner.change_location(Location.BANK)

    @staticmethod
    def execute(miner):
        miner.add_to_wealth()

        miner.say('Depositing gold. Total savings now: {0}'.format(miner.money_in_bank))

        if miner.wealthy():
            miner.say("WooHoo! Rich enough for now. Back home to mah li'lle lady.")
            miner.state_machine.change_state(GoHomeAndSleepTilRested)
        else:
            miner.state_machine.change_state(EnterMineAndDigForNugget)

    @staticmethod
    def exit(miner):
        miner.say('Leaving the bank')

    @staticmethod
    def on_message(miner, message):
        return False


class QuenchThirst:

    @staticmethod
    def enter(miner):
        if miner.location != Location.SALOON:
            miner.say('Boy, ah sure is thusty! Walking to the saloon')

        miner.change_location(Location.SALOON)

    @staticmethod
    def execute(miner):
        if miner.thirsty():
            miner.buy_and_drink_wiskey()
            miner.say("That's mighty fine sippin liquer")
            miner.state_machine.change_state(EnterMineAndDigForNugget)
        else:
            miner.say('ERROR! ERROR! ERROR!')

    @staticmethod
    def exit(miner):
        miner.say('Leaving the saloon, feeling good')

    @staticmethod
    def on_message(miner, message):
        return False


class GoHomeAndSleepTilRested:

    @staticmethod
    def enter(miner):
        if miner.location != Location.SHACK:
            miner.say('Walking home.')
            miner.change_location(Location.SHACK)
            miner.game.message_dispatcher.dispatch_message(miner, miner.wife, Message.HI_HONEY)

    @staticmethod
    def execute(miner):
        if not miner.fatigued():
            miner.say('What a God darn fantastic nap! Time to find more gold.')
            miner.state_machine.change_state(EnterMineAndDigForNugget)
        else:
            miner.decrease_fatigue()
            miner.say('ZZZ...')

    @staticmethod
    def exit(miner):
        miner.say('Leaving the house.')

    @staticmethod
    def on_message(miner, message):
        if message.message == Message.STEW_READY:
            miner.say('Ok hun, ahm a-comin!')
            miner.state_machine.change_state(EatStew)


class EatStew:

    @staticmethod
    def enter(miner):
        miner.say('Smells Real Goood Elsa!')

    @staticmethod
    def execute(miner):
        miner.say('Tastes Real Goood too!')
        miner.state_machine.revert_previous_state()

    @staticmethod
    def exit(miner):
        miner.say('Thank you! gAh better get back to whatever ah wuz doing')

    @staticmethod
    def on_message(miner, message):
        return False
