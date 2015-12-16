#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from game import GameMaster
import json
import logging
import sys

logger = logging.getLogger(__name__ + '.trainer')

class Config:
    def __init__(self, widths, gammas, etas, runs):
        self.widths = widths
        self.gammas = gammas
        self.etas = etas
        self.runs = runs

def train(config):
    try:
        for gamma in config.gammas:
            for width in config.widths:
                for eta in config.etas:
                    logger.info("Training gamma: {} width: {} eta: {}"
                            .format(gamma, width, eta))
                    gm = GameMaster(width, gamma, eta, True)
                    gm.run(config.runs)
    except Exception as ex:
        logger.error("Exception during training:")
        logger.error(ex)

def main(fileName):
    try:
        with open(fileName, 'r') as configFile:
            configDict = json.load(configFile)
            config = Config(configDict['width'], 
                            configDict['gamma'],
                            configDict['eta'],
                            configDict['runs'])
            train(config)
    except FileNotFoundError as ex:
        print("The config file \"" + fileName + "\" does not exist")
    except KeyError as ex:
        print("The key \"" + ex.args[0] + "\" cannot be found in the config")
    except Exception as ex:
        print(ex)

if __name__ == "__main__":
    if len(sys.argv) == 2:
        rootlog = logging.getLogger()
        rootlog.setLevel(logging.INFO)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        rootlog.addHandler(ch)
        main(sys.argv[1])
    else:
        print("Usage: " + sys.argv[0] + " configfile")


