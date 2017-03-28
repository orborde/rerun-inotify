#!/usr/bin/env python

import Queue

PROCEND  = 'PROCEND'
MODIFY   = 'MODIFY'
TIMEDONE = 'TIMEDONE'
EVENTS = set([PROCEND, MODIFY, TIMEDONE])

class State:
    def modify(self):
        raise NotImplementedError()
    def timedone(self):
        raise NotImplementedError()
    def procend(self):
        raise NotImplementedError()

class IdleState(State):
    def modify(self):
        return DebounceState()

class DebounceState(State):
    def __init__(self):
        spawn_timer()

    def modify(self):
        return self

    def timedone(self):
        return TestingState()

class TestingState(State):
    def __init__(self):
        self.pid = spawn_tests()

    def modify(self):
        send_kill(self.pid)
        return KillWaitState()

    def procend(self):
        # TODO: Capture output and print it here?
        return IdleState()

class KillWaitState(State):
    def modify(self):
        return self

    def procend(self):
        return TestingState()

        
def run(self):
    events = Queue.Queue()
    spawn_inotify(self.events)
    state = IdleState()

    while True:
        event = events.get()
        assert event in EVENTS
        if event is MODIFY:
            state = state.modify()
        elif event is PROCEND:
            state = state.procend()
        elif event is TIMEDONE:
            state = state.timedone()
        # TODO: Instead of constructing the next state inside the
        # previous state, maybe call the class constructer down here?
        # That affords a good place to inject the functions states
        # will need to call to manipulate the outside world.
