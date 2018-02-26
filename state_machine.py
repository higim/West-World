class StateMachine:

    def __init__(self, owner):
        self._owner = owner

        self.global_state = None
        self.current_state = None
        self.previous_state = None

    def update(self):

        if self.global_state:
            self.global_state.execute(self._owner)

        if self.current_state:
            self.current_state.execute(self._owner)

    def handle_message(self, t):
        if self.current_state and self.current_state.on_message(self._owner, t):
            return True

        if self.global_state and self.global_state.on_message(self._owner, t):
            return True

        return False

    def change_state(self, new_state):

        # assert states != null
        self.previous_state = self.current_state

        self.current_state.exit(self._owner)
        self.current_state = new_state
        self.current_state.enter(self._owner)

    def revert_previous_state(self):
        self.change_state(self.previous_state)
