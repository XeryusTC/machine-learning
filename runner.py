#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from game import GameMaster
import glob
import logging
import pickle
import sys

def main(runs):
    print('gamma, eta, width, runs, hareWins, houndWins')
    for p in glob.glob('trainedQs/*.q'):
        with open(p, 'rb') as f:
            (gamma, width, eta, oruns, hareQ, houndQ) = pickle.load(f)
            gm = GameMaster(width, gamma, eta, False)
            res = gm.run(runs, hareQ, houndQ)
            print("{}, {}, {}, {}, {}, {}"
                    .format(gamma, eta, width, oruns, res['hare'], res['hounds']))

if len(sys.argv) == 2:
    rootlog = logging.getLogger()
    rootlog.setLevel(logging.ERROR)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    rootlog.addHandler(ch)
    main(int(sys.argv[1]))
else:
    print("usage: {} runs".format(sys.argv[0]))

