#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import logging
from board import HareAndHoundsBoard
import player

logger = logging.getLogger(__name__)

class GameMaster:
    def __init__(self, width=7):
        self.width = width
        self.logger = logging.getLogger(__name__ + '.GameMaster')

    def run(self, runs=1):
        for i in range(runs):
            self.logger.debug('Starting run {}'.format(i))
            board = HareAndHoundsBoard(self.width)
            hare = player.HarePlayer(board, 0.9)
            hounds = player.HoundsPlayer(board, 0.9)
            print(board)

            for i in range(50):
                hounds.play()
                if self.winstate(board) == 'hounds':
                    hare.reward(-100)
                    hounds.reward(100)
                    break
                else:
                    hounds.reward(0)

                hare.play()
                if self.winstate(board) == 'hare':
                    hare.reward(100)
                    hounds.reward(-100)
                    break
                else:
                    hare.reward(0)
                print(board)
            self.logger.info('Winner: {}'.format(self.winstate(board)))
            print(board)

    def winstate(self, board):
        # Hare wins if he reaches the left side of the board
        if board.hare == (0, 1):
            return 'hare'
        # Hounds win if the hare can not make any more moves
        if len(board.possible_moves(board.hare)) == 0:
            return 'hounds'
        return None


if __name__ == '__main__':
    rootlog = logging.getLogger()
    rootlog.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    rootlog.addHandler(ch)

    gm = GameMaster()
    gm.run()
