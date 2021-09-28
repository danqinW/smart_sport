class ChainStateMachine(object):
    def __init__(self, states):
        self.states = states
        self.length = len(states)
        self.cur_state = None
        self.next_state = states[0] if self.length > 0 else None
        # self.done = False

    def state_change(self):
        if len(self.states) > 0:
            self.cur_state = self.next_state
            self.next_state = (self.next_state + 1) % self.length
            # if self.next_state == self.length:
            #     self.done = True

    def get_next_frame_id(self):
        return self.states[self.next_state]

    def get_cur_frame_id(self):
        return self.states[self.cur_state] if self.cur_state else None

    def reinitialize(self):
        self.cur_state = None
        self.next_state = self.states[0] if self.length > 0 else None
        # self.done = False
