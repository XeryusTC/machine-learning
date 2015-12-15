#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from game import GameMaster
import json
import logging
import sys

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
                    print("Training gamma: {} width: {} eta: {}"
                            .format(gamma, width, eta))
                    gm = GameMaster(width, gamma, eta, True)
                    gm.run(config.runs)
    except Exception as ex:
        print("Exception during training:")
        print(ex)

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
        main(sys.argv[1])
    else:
        print("Usage: " + sys.argv[0] + " configfile")


