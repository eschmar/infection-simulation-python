from simulation import Simulation
import helper
import sys

params = helper.parseArguments(sys.argv)

# default values
size = 40
probabilityOfInfection = 0.02
probabilityOfDeath = 0
infectionLength = [6, 9]

if '-N' in params:
    val = int(params['-N'])
    if val < 1:
        raise ValueError("Size of the simulation has to be positive.")
    size = val

if '-S' in params:
    val = float(params['-S'])
    if val < 0 or val > 1:
        raise ValueError("Probabilities have to be within [0,1].")
    probabilityOfInfection = val

if '-L' in params:
    val = float(params['-L'])
    if val < 0 or val > 1:
        raise ValueError("Probabilities have to be within [0,1].")
    probabilityOfDeath = val

if '-minDays' in params and '-maxDays' in params:
    min = int(params['-minDays'])
    max = int(params['-maxDays'])
    if min < 0 or min > max:
        raise ValueError("Infection interval has to be positive and min > max.")
    infectionLength = [min, max]

# init simulation
simulation = Simulation(size, probabilityOfInfection, probabilityOfDeath, infectionLength)

if '--silent' in params and params['--silent']:
    simulation.isSilent = True

if '--frames' in params and params['--frames']:
    simulation.writeFrames = True

if '-seed' in params:
    simulation.setSeed(int(params['-seed']))
    simulation.writeFrames = True

# contaminate one cell
simulation.contaminate(0,3)

# run simulation
simulation.run()
