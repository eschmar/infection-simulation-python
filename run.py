from simulation import Simulation
import helper
import sys

def run(args):
    params = helper.parseArguments(args)

    # default values
    size = 40
    probabilityOfInfection = 0.02
    probabilityOfDeath = 0
    infectionLength = [6, 9]

    # check size for user input
    if '-N' in params:
        val = int(params['-N'])
        if val < 1:
            raise ValueError("Size of the simulation has to be positive.")
        size = val

    # check probability of infection for user input
    if '-S' in params:
        val = float(params['-S'])
        if val < 0 or val > 1:
            raise ValueError("Probabilities have to be within [0,1].")
        probabilityOfInfection = val

    # check probability of death for user input
    if '-L' in params:
        val = float(params['-L'])
        if val < 0 or val > 1:
            raise ValueError("Probabilities have to be within [0,1].")
        probabilityOfDeath = val

    # check length of infection for user input
    if '-minDays' in params and '-maxDays' in params:
        min = int(params['-minDays'])
        max = int(params['-maxDays'])
        if min < 0 or min > max:
            raise ValueError("Infection interval has to be positive and min > max.")
        infectionLength = [min, max]

    # init simulation
    simulation = Simulation(size, probabilityOfInfection, probabilityOfDeath, infectionLength)

    #  contaminate chosen individuals
    if '-x' in params and len(params['-x']) > 0:
        for i in range(0, len(params['-x'])):
            point = params['-x'][i].split(",")
            x = int(point[0])
            y = int(point[1])

            if x < 0 or x > size or y < 0 or y > size:
                raise ValueError("One of your individuals was out of bounds.")

            simulation.contaminate(x, y)
    else:
        # contaminate one cell
        simulation.contaminate(0,0)

    if '--frames' in params and params['--frames']:
        simulation.writeFrames = True

    if '-seed' in params:
        simulation.setSeed(int(params['-seed']))

    # run simulation
    iteration, avgInfectedPerDay, avgDeathsPerDay, avgRecoveredPerDay, avgIllPerDay, sumInfectedPerDay, sumDeathsPerDay = simulation.run()

    # print output
    if '--iterations' in params or '--print' in params:
        print("Simulation took {0} iterations.".format(iteration))
    
    if '--avgInfected' in params or '--print' in params:
        print("Average infected per iteration: {0}".format(avgInfectedPerDay))
    
    if '--avgDead' in params or '--print' in params:
        print("Average deaths per iteration: {0}".format(avgDeathsPerDay))

    if '--avgRecovered' in params or '--print' in params:
        print("Average recovered per iteration: {0}".format(avgRecoveredPerDay))
    
    if '--avgIll' in params or '--print' in params:
        print("Average ill per iteration: {0}".format(avgIllPerDay))

    if '--sumInfected' in params or '--print' in params:
        print("Sum of infected: {0}".format(sumInfectedPerDay))

    if '--sumDeaths' in params or '--print' in params:
        print("Sum of deaths: {0}".format(sumDeathsPerDay))

    return sumInfectedPerDay

if __name__ == '__main__':
    run(sys.argv[1:])
