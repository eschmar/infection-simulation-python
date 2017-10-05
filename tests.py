from simulation import Simulation
import helper
import sys, random

def run():
    """Runs all test cases."""
    testInstantiation()
    testRandomSeeding()
    testGetPos()
    testContaminate()
    testAverage()
    testInitialAdvance()
    testInfectNeighboursOf()

    testLiveInfected()
    testLiveDead()
    testLiveImmune()

    testRunInstantDeath()
    testRunAllInfected()

def testInstantiation():
    """Verify that the simulation was instantiated correctly and that the population is ready."""
    size = 16
    probabilityOfInfection = 1
    probabilityOfDeath = 1
    lengthOfInfection = [1, 2]

    simulation = Simulation(size, probabilityOfInfection, probabilityOfDeath, lengthOfInfection)
    if not len(simulation.population) > 0 or len(simulation.population) != size * size:
        raise Exception("Population was not initialised correctly.")
    
    for cell in simulation.population:
        if cell != simulation.CELL_STATE_HEALTHY:
            raise Exception("Population contains non healthy individuals before simulation.")
    
    if simulation.size != size or simulation.probabilityOfInfection != probabilityOfInfection or simulation.probabilityOfDeath != probabilityOfDeath or simulation.lengthOfInfection != lengthOfInfection:
        raise Exception("Parameters incorrect.")


def testRandomSeeding():
    """Verify that the same seed produces the same random numbers."""
    simulation = Simulation()

    simulation.setSeed(100)
    first = random.random()

    simulation.setSeed(100)
    second = random.random()

    if first != second:
        raise Exception("Same seed produced different results!")

def testGetPos():
    """Verify that the coordinates to array position translation is correct."""
    simulation = Simulation()
    if simulation.getPos(0, 0) != 0:
        raise Exception("Wrong position detected!")
    
    try:
        simulation.getPos(-1, -500)
    except Exception as error:
        return
    
    raise Exception("Invalid input succeeded!")

def testContaminate():
    """Verify that only the correct individual gets contaminated."""
    simulation = Simulation()
    simulation.contaminate(20, 20)

    count = 0
    for cell in simulation.population:
        if cell == simulation.CELL_STATE_INFECTED:
            count += 1
    
    if count != 1:
        raise Exception("Wrong number of individuals were contaminated.")
    
    if simulation.population[simulation.getPos(20, 20)] != simulation.CELL_STATE_INFECTED:
        raise Exception("Expected cell was not contaminated.")

def testAverage():
    """Verify that the average of list is calculated."""
    simulation = Simulation()
    if simulation.average([1, 1, 1]) != 1 or simulation.average([0, 1, 2]) != 1:
        raise Exception("Incorrect average detected.")

def testInitialAdvance():
    """Verify that the future population is intantiated correctly after an empty advance."""
    simulation = Simulation()
    simulation.advance()

    for pos in range(0, len(simulation.population)):
        if simulation.population[pos] != simulation.future[pos]:
            raise Exception("Population and future are not equal after empty advance.")

    if simulation.currentlyIll != 0 or simulation.deadToday != 0:
        raise Exception("Wrong amount of infected and dead individuals!")

def testInfectNeighboursOf():
    """Verify that neighbours get infected when they should."""
    simulation = Simulation(40, probabilityOfInfection=1)
    simulation.advance()

    simulation.contaminate(20, 20)
    simulation.infectNeighboursOf(20, 20)

    for coord in [[19,19], [19,20], [19,21], [20,19], [20,21], [21,19], [21,20], [21,21]]:
        if simulation.future[simulation.getPos(coord[0], coord[1])] != simulation.CELL_STATE_INFECTED:
            raise Exception("Neighbours were not infected!")
    
    if simulation.currentlyIll != 9 or simulation.deadToday != 0:
        raise Exception("Wrong amount of infected and dead individuals!")
    
    simulation = Simulation(40, probabilityOfInfection=0)
    simulation.advance()

    simulation.contaminate(20, 20)
    simulation.infectNeighboursOf(20, 20)

    for coord in [[19,19], [19,20], [19,21], [20,19], [20,21], [21,19], [21,20], [21,21]]:
        if simulation.future[simulation.getPos(coord[0], coord[1])] != simulation.CELL_STATE_HEALTHY:
            raise Exception("Neighbours were infected when they shouldn't!")
    
    if simulation.currentlyIll != 1 or simulation.deadToday != 0:
        raise Exception("Wrong amount of infected and dead individuals!")

def testLiveInfected():
    """Verify that a contaminated individual starts his infection timer."""
    simulation = Simulation(3, probabilityOfInfection=1)
    simulation.advance()
    simulation.contaminate(1, 1)
    simulation.live(1, 1)

    future = simulation.future[simulation.getPos(1, 1)]
    if not isinstance(future, int):
        raise Exception("Individual that was infected didn't start its infection timer!")
    
    if future < simulation.lengthOfInfection[0] or future > simulation.lengthOfInfection[1]:
        raise Exception("Invalid infection length detected!")

def testLiveDead():
    """Verify that dead individuals have no effect on the population."""
    simulation = Simulation(3, probabilityOfInfection=1)
    simulation.advance()

    simulation.population[simulation.getPos(1, 1)] = simulation.CELL_STATE_DEAD
    simulation.deadToday += 1

    simulation.live(1, 1)

    future = simulation.future[simulation.getPos(1, 1)]
    if future != simulation.CELL_STATE_DEAD:
        raise Exception("Dead individual is supposed to stay dead!")
    
    for i in range(0, len(simulation.future)):
        if i == simulation.getPos(1, 1):
            continue
        if simulation.future[i] != simulation.CELL_STATE_HEALTHY:
            raise Exception("Dead individuals should not affect neighbours!")

def testLiveImmune():
    """Verify that immune individuals have no effect on the population."""
    simulation = Simulation(3, probabilityOfInfection=1)
    simulation.advance()

    simulation.population[simulation.getPos(1, 1)] = simulation.CELL_STATE_IMMUNE
    simulation.live(1, 1)

    future = simulation.future[simulation.getPos(1, 1)]
    if future != simulation.CELL_STATE_IMMUNE:
        raise Exception("Immune individual is supposed to stay immune!")
    
    for i in range(0, len(simulation.future)):
        if i == simulation.getPos(1, 1):
            continue
        if simulation.future[i] != simulation.CELL_STATE_HEALTHY:
            raise Exception("Immune individuals should not affect neighbours!")

def testRunInstantDeath():
    """Verify that a deadly infection instantly kills."""
    simulation = Simulation(3, probabilityOfInfection=1, probabilityOfDeath=1)
    simulation.contaminate(1, 1)
    simulation.run()

    if simulation.future[simulation.getPos(1, 1)] != simulation.CELL_STATE_DEAD:
        raise Exception("Individual should die!")

    for i in range(0, len(simulation.future)):
        if i == simulation.getPos(1, 1):
            continue
        if simulation.future[i] != simulation.CELL_STATE_HEALTHY:
            raise Exception("Dead individuals should not infect neighbours!")

def testRunAllInfected():
    """Verify that the whole population is infected, if the probably is 1. That is the case, if everyone turns immune."""
    simulation = Simulation(3, probabilityOfInfection=1, probabilityOfDeath=0)
    simulation.contaminate(1, 1)
    simulation.run()

    for i in range(0, len(simulation.future)):
        if simulation.future[i] != simulation.CELL_STATE_IMMUNE:
            raise Exception("Dead individuals should not infect neighbours!")

if __name__ == '__main__':
    try:
        run()
        print(" > SUCCESS. Tests complete and successful.")
    except Exception as error:
        print(" > ERROR: {0}.".format(error))
