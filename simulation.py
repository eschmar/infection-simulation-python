import random

random.seed(5)

class Simulation:
    """Infection Simulation."""
    CELL_STATE_HEALTHY = "_"
    CELL_STATE_DEAD = "X"
    CELL_STATE_IMMUNE = "I"

    def __init__(self, size, probabilityOfInfection, probabilityOfDeath, lengthOfInfection):
        self.size = size
        self.probabilityOfInfection = probabilityOfInfection
        self.probabilityOfDeath = probabilityOfDeath
        self.lengthOfInfection = lengthOfInfection
        self.iteration = 0

        self.populate()
        self.population[3] = self.getRandomInfectionLength()
    
    def run(self):
        """Run the simulation"""
        self.isRunning = True

        while self.isRunning:
            self.isRunning = False
            self.writeFrameToFile()
            self.iteration = self.iteration + 1
            self.advance()
    
    def writeFrameToFile(self):
        """Write current population to file."""
        file = open("out/frame{0}.txt".format(self.iteration), "w")
        for x in range(0, self.size):
            file.write(",".join(str(v) for v in self.population[x*self.size:x*self.size+self.size]))
            file.write("\n")
        file.close()

    def populate(self):
        """What is this"""
        self.population = []
        for i in range(0, self.size * self.size):
            self.population.append(self.CELL_STATE_HEALTHY)

    def getPos(self, x, y):
        return x * self.size + y
    
    def advance(self):
        """Advance one iteration in the simulation"""
        self.future = self.population[:]

        # update each cell
        for x in range(0, self.size):
            for y in range(0, self.size):
                self.live(x, y)
        
        self.population = self.future
    
    def live(self, x, y):
        """Update a cell's state for one iteration."""
        pos = self.getPos(x, y)

        if not isinstance(self.population[pos], int):
            return

        self.isRunning = True
        remainingDaysInfected = self.population[pos]

        if remainingDaysInfected <= 0:
            self.future[pos] = self.CELL_STATE_IMMUNE
        elif remainingDaysInfected > 0 and self.getRandomBoolean(self.probabilityOfDeath):
            self.future[pos] = self.CELL_STATE_DEAD
        else:
            self.future[pos] = remainingDaysInfected - 1
        
        self.infectNeighboursOf(x, y)
    
    def infectNeighboursOf(self, x, y):
        """Try to infect all cell's neighbours."""
        pos = self.getPos(x, y)

        for i in range(-1, 2):
            for j in range(-1, 2):
                t = (x + i + self.size) % self.size
                s = (y + j + self.size) % self.size

                # skip the cell itself
                if x == t and y == s:
                    continue

                neighbourPos = self.getPos(t, s)

                # try to infect
                if self.population[neighbourPos] == self.CELL_STATE_HEALTHY and self.future[neighbourPos] == self.CELL_STATE_HEALTHY:
                    if self.getRandomBoolean(self.probabilityOfInfection):
                        self.future[neighbourPos] = self.getRandomInfectionLength()

    def getRandomNumber(self):
        """Returns random float x, 0.0 <= x < 1.0."""
        return random.random()

    def getRandomInfectionLength(self):
        """Returns a random integer between min and max."""
        return random.randint(self.lengthOfInfection[0], self.lengthOfInfection[1])
    
    def getRandomBoolean(self, probability):
        """Returns true or false depending on a given probability."""
        return self.getRandomNumber() < probability
