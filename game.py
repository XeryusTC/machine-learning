#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import logging
from board import HareAndHoundsBoard
import player

logger = logging.getLogger(__name__)
REWARD = 1

class GameMaster:
    def __init__(self, width=5, gamma=0.9, eta=1, training=True):
        self.width = width
        self.gamma = gamma
        self.eta = eta
        self.training = training
        self.logger = logging.getLogger(__name__ + '.GameMaster')

    def run(self, runs=1, hareQ={}, houndsQ={}):
        width = len(str(runs))
        eta = self.eta
        results = {'hare': 0, 'hounds': 0}
        if self.training:
            T = runs
        else:
            T = 1
            # TODO: load hare and hounds Qs

        for i in range(runs):
            self.logger.debug('Starting run {}'.format(i))
            board = HareAndHoundsBoard(self.width)
            hare = player.HarePlayer(board, self.gamma, eta, T, hareQ)
            hounds = player.HoundsPlayer(board, self.gamma, eta, T, houndsQ)

            for j in range(100):
                hounds.play()
                if self.winstate(board, True) == 'hounds':
                    hare.reward(-REWARD)
                    hounds.reward(REWARD)
                    results['hounds'] += 1
                    break
                else:
                    # Give the other player reward so they know what state
                    # they ended up in after doing their action
                    hare.reward(0)

                hare.play()
                if self.winstate(board) == 'hare':
                    hare.reward(REWARD)
                    hounds.reward(-REWARD)
                    results['hare'] += 1
                    break
                else:
                    hounds.reward(0)
            self.logger.info('{:{width}}/{:{width}} Winner: {}'.format(i, runs,
                self.winstate(board), width=width))
            # if there is no winner, give both players a penalty
            if self.winstate(board) == None:
                hare.reward(-REWARD * .5)
                hounds.reward(-REWARD * .5)
            if self.training:
                T = T - 1
                eta = self.eta - (self.eta/runs) * i
                # Update the Q for next time
                hareQ = hare._Q
                houndsQ = hounds._Q
        #hare.printQ()
        if self.training:
            return hareQ, houndsQ, results
        else:
            return results

    def winstate(self, board, hare_move=False):
        # Hounds win if the hare can not make any more moves
        if len(board.possible_moves(board.hare)) == 0:
            return 'hounds'
        # Hare wins if it is to the left of all hounds
        if all([board.hare[0] < h[0] for h in board.hounds]):
            return 'hare'
        # Hare wins if he reaches the left side of the board
        if board.hare == (0, 1):
            return 'hare'
        # Hare also wins if the hounds can not move
        if not hare_move and \
                sum([len(board.possible_moves(h)) for h in board.hounds]) == 0:
            return 'hare'
        return None


if __name__ == '__main__':
    rootlog = logging.getLogger()
    rootlog.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    rootlog.addHandler(ch)

    gm = GameMaster(gamma=0.9, eta=0.5)
    gm.run(100000)
