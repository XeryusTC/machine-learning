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

            for i in range(10):
                hounds.play()
                hounds.reward(0)
                hare.play()
                hare.reward(0)


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
