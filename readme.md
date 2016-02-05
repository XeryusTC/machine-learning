Hare and Hounds
===============
This project aims to learn to play the game 'Hare and Hounds' using temporal 
difference learning. It consists of multiple programs, one for training the 
system, and one for running the game with the trained parameters

`trainer.py`
------------
This program reads in a configuration file and train the system using the 
parameters given in the configuration. It also requires a number of workers it 
can use to train multiple configurations at the same time. Trained Q values 
get stored in a file in the directory `trainedQs`, where the filename is the 
parameters that were used.

The configuration is a json file which should have the fields `runs`, `gamma`,
`eta` and `width`, where `runs` is a single integer and the other ones are 
arrays. The values are combined in each possible way and this is the eventual 
configuration used.

`runner.py`
-----------
This program reads in all the `.q` files in the directory `trainedQs` and 
plays a given number of games with each of the configurations. This number
of games has to be given at the command line. It will then for each 
configuration give the number of wins of the Hounds and the Hares and the 
parameters given during training.
