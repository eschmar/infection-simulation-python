from simulation import Simulation
import helper
import sys

params = helper.parseArguments(sys.argv)

# init simulation
simulation = Simulation(40, 0.02, 0, [6, 9])
if '--silent' in params and params['--silent']:
    simulation.isSilent = True
if '--frames' in params and params['--frames']:
    simulation.writeFrames = True

# run simulation
simulation.run()
