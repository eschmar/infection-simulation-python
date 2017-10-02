from simulation import Simulation
import helper
import sys

params = helper.parseArguments(sys.argv)

# default values
size = 40
probabilityOfInfection = 0.02
probabilityOfDeath = 0
infectionLength = [6, 9]

if '-N' in params and params['-N']:
    size = params['-N']

if '-S' in params and params['-S']:
    probabilityOfInfection = params['-S']

if '-L' in params and params['-L']:
    probabilityOfDeath = params['-L']

if '-minDays' in params and params['-minDays'] and '-maxDays' in params and params['-maxDays']:
    infectionLength = [params['-minDays'], params['-maxDays']]

# init simulation
simulation = Simulation(size, probabilityOfInfection, probabilityOfDeath, infectionLength)
if '--silent' in params and params['--silent']:
    simulation.isSilent = True
if '--frames' in params and params['--frames']:
    simulation.writeFrames = True

# run simulation
simulation.run()
