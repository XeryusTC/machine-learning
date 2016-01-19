#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from game import GameMaster
import json
import logging
import pickle
import sys
import traceback
import multiprocessing as mp
import queue

logger = logging.getLogger(__name__ + '.trainer')

class Config:
    def __init__(self, widths, gammas, etas, runs):
        self.widths = widths
        self.gammas = gammas
        self.etas = etas
        self.runs = runs

def train_worker(q):
    while 1:
        try:
            task = q.get(True, 1)
        except queue.Empty:
            break
        width, gamma, eta, runs = task
        logger.warning('Training with gamma {} eta {} width {} runs {}'.format(
            gamma, eta, width, runs))
        gm = GameMaster(width, gamma, eta, True)
        Qs = gm.run(runs)
        with open('trainedQs/g{}_w{}_e{}_r{}.q'.format(gamma, width,
                eta, runs), 'wb') as f:
            pickle.dump((gamma, width, eta, runs, Qs[0], Qs[1]), f)
        q.task_done()

def train(config, num_workers):
    excepts = []
    queue = mp.JoinableQueue()
    for gamma in config.gammas:
        for width in config.widths:
            for eta in config.etas:
                queue.put((width, gamma, eta, config.runs))
    # stop signals
    workers = [mp.Process(target=train_worker, args=(queue,))
        for i in range(num_workers)]
    [w.start() for w in workers]

    # Wait for work to complete
    queue.join()
    queue.close()
    [w.join() for w in workers]

def main(fileName, workers):
    try:
        with open(fileName, 'r') as configFile:
            configDict = json.load(configFile)
            config = Config(configDict['width'],
                            configDict['gamma'],
                            configDict['eta'],
                            configDict['runs'])
            train(config, workers)
    except FileNotFoundError as ex:
        logger.fatal("The config file \"" + fileName + "\" does not exist")
    except KeyError as ex:
        logger.fatal("The key \"" + ex.args[0] + "\" cannot be found in the config")
    except Exception as ex:
        logger.fatal(ex)
        traceback.print_exc()

if __name__ == "__main__":
    if len(sys.argv) == 3:
        rootlog = logging.getLogger()
        rootlog.setLevel(logging.WARNING)
        ch = logging.StreamHandler()
        ch.setLevel(logging.WARNING)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        rootlog.addHandler(ch)
        main(sys.argv[1], int(sys.argv[2]))
    else:
        print("Usage: " + sys.argv[0] + " configfile num_workers")

