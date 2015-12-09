#!/usr/bin/env python3

import logging
import math as m
import random
from board import HareAndHoundsBoard

logger = logging.getLogger(__name__)
random.seed()

class Player:
    def __init__(self, board, gamma):
        self.board = board
        self.gamma = gamma
        self._Q = {}
        self.last_action = None
        self.last_state = None
        self.logger = logging.getLogger(__name__ + '.Player')

    def play(self):
        raise NotImplementedError()

    def reward(self, r):
        pass

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

    def updateQ(self, state, action, value):
        pass

    def pick_action(self, actions, temp=1000):
        # Calculate the probabilities (18.11)
        probs = {}
        for a in actions:
            d = sum([m.exp(self.getQ(self.state, b) / temp) for b in actions])
            probs[a] = m.exp(self.getQ(self.state, a) / temp) / d
        self.logger.debug(probs)

        # Pick the action with the highest probability
        best = random.choice(actions)
        p_best = probs[best]
        for a, p in probs.items():
            if p > p_best:
                best = a
                p_best = p
        return best


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
    p = HarePlayer(b, .9)
    p.play()

    p2 = HoundsPlayer(b, .9)
    p2.play()
