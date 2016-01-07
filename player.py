#!/usr/bin/env python3

import logging
import math as m
import random
from board import HareAndHoundsBoard

logger = logging.getLogger(__name__)
random.seed()

class Player:
    def __init__(self, board, gamma, eta, T=1000, Q={}):
        self.board = board
        self.gamma = gamma
        self.eta = eta
        self.temp = T
        self._Q = Q
        self.last_action = None
        self.last_state = None
        self.logger = logging.getLogger(__name__ + '.Player')

    def play(self):
        raise NotImplementedError()

    def reward(self, r):
        # Updating doesn't work without having at least some action on the
        # next state, so use this trick to create it
        self.getQ(self.state, 'dummy')
        self.updateQ(self.last_state, self.last_action, self.state, r)

    @property
    def state(self):
        return (tuple(self.board.hounds), self.board.hare)

    def getQ(self, state, action):
        try:
            self._Q[state]
            return self._Q[state][action]
        except KeyError:
            if state not in self._Q.keys():
                self._Q[state] = {}
            if action not in self._Q[state].keys():
                self._Q[state][action] = 0
            return self._Q[state][action]

    def updateQ(self, s, a, sprime, reward):
        # Don't update if we don't know anything about sprime
        if sprime not in self._Q.keys():
            return

        # Q learing
        Q = self.getQ(s, a)
        m = 0
        m = self.getQ(sprime, max(self._Q[sprime],
            key=lambda k: self._Q[sprime][k]))
        update = self.eta * (reward + self.gamma * m - Q)
        self._Q[s][a] = Q + update
        self.logger.debug('Q({},{}) update, was {}, becomes {}'.format(s, a,
            Q, update))

    def pick_action(self, actions):
        # Calculate the probabilities (18.11)
        probs = {}
        d = sum([m.exp(self.getQ(self.state, b) / self.temp)
            for b in actions])
        for a in actions:
            probs[a] = m.exp(self.getQ(self.state, a) / self.temp) / d

        # Pick the action with the highest probability
        pick = random.random()
        total = 0
        for a, p in probs.items():
            total += p
            if total >= pick:
                return a
        print(total)
        return a

    def printQ(self):
        """Prints only significant values from Q"""
        for s in self._Q:
            for a in self._Q[s]:
                if self.getQ(s, a) != 0:
                    print(s, '\t', a, '\t', self.getQ(s, a))


class HarePlayer(Player):
    def __init__(self, *args, **kwargs):
        super(HarePlayer, self).__init__(*args, **kwargs)
        self.logger = logging.getLogger(__name__ + '.HarePlayer')

    def play(self):
        actions = self.board.possible_moves(self.board.hare)
        action = self.pick_action(actions)
        self.logger.debug('Best action: {}'.format(action))

        self.last_state = self.state
        self.last_action = action

        self.board.move(self.board.hare, action)


class HoundsPlayer(Player):
    def __init__(self, *args, **kwargs):
        super(HoundsPlayer, self).__init__(*args, **kwargs)
        self.logger = logging.getLogger(__name__ + '.HoundsPlayer')

    def play(self):
        actions = [(hound, m) for hound in self.board.hounds
            for m in self.board.possible_moves(hound)]
        action = self.pick_action(actions)
        self.logger.debug('Best action: {}'.format(action))

        self.last_state = self.state
        self.last_action = action

        self.board.move(action[0], action[1])


if __name__ == '__main__':
    print("You should not start this module directly")
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    b = HareAndHoundsBoard(7)
    p = HarePlayer(b, .9, .1)
    p.play()

    p2 = HoundsPlayer(b, .9, .1)
    p2.play()
    p.reward(100)
