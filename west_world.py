import time
import miner_states, wife_states

from entities import Miner, Wife
from entity_manager import EntityManager
from messages import MessageDispatcher


class Game:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not Game._instance:
            Game._instance = object.__new__(cls)
        return Game._instance

    def __init__(self):
        self.entity_manager = EntityManager()
        self.message_dispatcher = MessageDispatcher()

    def add_entity(self, entity):
        self.entity_manager.register_entity(entity)
        entity.game = self

    def update(self):
        for entity in self.entity_manager:
            entity.update()
        self.message_dispatcher.dispatch_delayed_messages()

if __name__ == '__main__':
    bob = Miner("Bob", None, miner_states.EnterMineAndDigForNugget)
    elsa = Wife("Elsa", wife_states.WifeGlobalState, wife_states.DoHouseWork)

    bob.wife = elsa
    elsa.husband = bob

    game = Game()
    game.add_entity(bob)
    game.add_entity(elsa)

    for i in range(0,100):
        game.update()
        time.sleep(1)