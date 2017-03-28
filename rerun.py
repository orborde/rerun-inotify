#!/usr/bin/env python

import collections
import Queue

PROCEND  = 'PROCEND'
MODIFY   = 'MODIFY'
TIMEDONE = 'TIMEDONE'
EVENTS   = set([PROCEND, MODIFY, TIMEDONE])

Ops = collections.namedtuple(
    'Ops',
    ['start_timer',
     'start_tests',
     'send_kill'])

class State:
    def __init__(self, ops):
        self.ops = ops
    def modify(self):
        raise NotImplementedError()
    def timedone(self):
        raise NotImplementedError()
    def procend(self):
        raise NotImplementedError()

class IdleState(State):
    def modify(self):
        return DebounceState(self.ops)

class DebounceState(State):
    def __init__(self, ops):
        # TODO: Derp, how do I inherit?
        State.__init__(self, ops)

        self.ops.start_timer()

    def modify(self):
        return self

    def timedone(self):
        return TestingState(self.ops)

class TestingState(State):
    def __init__(self):
        # TODO: Derp, how do I inherit?
        State.__init__(self, ops)

        self.pid = self.ops.start_tests()

    def modify(self):
        self.ops.send_kill(self.pid)
        return KillWaitState(self.ops)

    def procend(self):
        # TODO: Capture output and print it here?
        return IdleState(self.ops)

class KillWaitState(State):
    def modify(self):
        return self

    def procend(self):
        return TestingState(self.ops)

        
def run(self):
    events = Queue.Queue()
    spawn_inotify(events)
    state = IdleState(ops)

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
