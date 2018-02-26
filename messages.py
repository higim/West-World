import time
from enum import Enum


class Message(Enum):
    HI_HONEY = 1
    STEW_READY = 2


class Telegram:
    """
    Telegram class only provides getter properties to get the different fields created by the
    constructor. We want to avoid internal data to be changed from outside.
    """
    def __init__(self, sender, receiver, message, dispatch_time=None, extra_info=None):
        self._sender = sender
        self._receiver = receiver
        self._message = message
        self._dispatch_time = dispatch_time
        self._extra_info = extra_info

    @property
    def sender(self):
        return self._sender

    @property
    def receiver(self):
        return self._receiver

    @property
    def message(self):
        return self._message

    @property
    def dispatch_time(self):
        return self._dispatch_time

    @dispatch_time.setter
    def dispatch_time(self, delay):
        current_time = time.time()
        self._dispatch_time += current_time + delay

    def discharge(self):
        self.receiver.handle_message(self)


class MessageDispatcher:
    _instance = None

    # Singleton
    def __new__(cls):
        if MessageDispatcher._instance is None:
            MessageDispatcher._instance = object.__new__(cls)
        return MessageDispatcher._instance

    def __init__(self):
        self._priority = list()

    def dispatch_message(self, sender, receiver, message, delay=0.0, extra_info=None):
        """
        :param delay: in seconds
        """
        telegram = Telegram(sender, receiver, message, delay, extra_info)

        if delay <= 0.0:
            print('Instant telegram dispatched at time {0} by {1} for {2}. Msg is {3}.'.format(
                time.time(),
                sender.name,
                receiver.name,
                str(message)
            ))

            telegram.discharge()

        else:
            telegram.dispatch_time = delay
            self._priority.append(telegram)
            self._priority = sorted(self._priority, key=lambda x: x.dispatch_time)

            print('Delayed telegram from {0} recorded at time {1} for {2}. Msg is {3}'.format(
                sender.name,
                time.time(),
                receiver.name,
                str(message)
            ))

    def dispatch_delayed_messages(self):
        if not self._priority:
            return

        # Search for messages with dispatch time <= current_time and discharge them
        current_time = time.time()
        while self._priority and self._priority[0].dispatch_time < current_time:
            telegram = self._priority.pop(0)

            print('Queued telegram ready for dispatch: sent to {0}. Msg is {1}'.format(
                telegram.receiver.name,
                str(telegram.message)
            ))

            telegram.discharge()