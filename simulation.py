import random

random.seed(5)

class Simulation:
    """Infection Simulation."""
    CELL_STATE_HEALTHY = "_"
    CELL_STATE_DEAD = "X"
    CELL_STATE_IMMUNE = "I"

    isSilent = False
    writeFrames = False

    def __init__(self, size, probabilityOfInfection, probabilityOfDeath, lengthOfInfection):
        # settings
        self.size = size
        self.probabilityOfInfection = probabilityOfInfection
        self.probabilityOfDeath = probabilityOfDeath
        self.lengthOfInfection = lengthOfInfection
        self.iteration = 0

        # statistics
        self.infectedPerDay = []
        self.deathsPerDay = []
        self.recoveredPerDay = []
        self.illPerDay = []
        self.currentlyIll = 0

        # prepare population
        self.populate()
        self.contaminate(0,3)
    
    def run(self):
        """Run the simulation"""
        self.isRunning = True

        # run simulation
        while self.isRunning:
            self.isRunning = False
            self.writeFrameToFile()
            self.iteration = self.iteration + 1
            self.advance()

        if self.currentlyIll != 0:
            raise ValueError("Simulation has finished, but there are still infected cells active.")

        if self.isSilent:
            return

        # print results
        print("Average infected per iteration: {0}".format(self.average(self.infectedPerDay)))
        print("Average deaths per iteration: {0}".format(self.average(self.deathsPerDay)))
        print("Average recovered per iteration: {0}".format(self.average(self.recoveredPerDay)))
        print("Average ill per iteration: {0}".format(self.average(self.illPerDay)))

        print("Sum of infected: {0}".format(sum(self.infectedPerDay)))
        print("Sum of deaths: {0}".format(sum(self.deathsPerDay)))

    def contaminate(self, x, y):
        """Contaminate a specific cell"""
        self.population[self.getPos(x, y)] = self.getRandomInfectionLength()
        self.currentlyIll += 1

    def average(self, l):
        return sum(l) / float(len(l))
    
    def writeFrameToFile(self):
        """Write current population to file."""
        if not self.writeFrames:
            return

        file = open("out/frame{0}.txt".format(self.iteration), "w")
        for x in range(0, self.size):
            file.write(" ".join(str(v) for v in self.population[x*self.size:x*self.size+self.size]))
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

        # statistics
        self.infectedToday = 0
        self.deadToday = 0
        self.recoveredToday = 0

        # update each cell
        for x in range(0, self.size):
            for y in range(0, self.size):
                self.live(x, y)
        
        # update statistics with new data
        self.infectedPerDay.append(self.infectedToday)
        self.deathsPerDay.append(self.deadToday)
        self.recoveredPerDay.append(self.recoveredToday)
        self.illPerDay.append(self.currentlyIll)

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
            self.recoveredToday += 1
            self.currentlyIll -= 1
        elif remainingDaysInfected > 0 and self.getRandomBoolean(self.probabilityOfDeath):
            self.future[pos] = self.CELL_STATE_DEAD
            self.deadToday += 1
            self.currentlyIll -= 1
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
                        self.infectedToday += 1
                        self.currentlyIll += 1

    def getRandomNumber(self):
        """Returns random float x, 0.0 <= x < 1.0."""
        return random.random()

    def getRandomInfectionLength(self):
        """Returns a random integer between min and max."""
        return random.randint(self.lengthOfInfection[0], self.lengthOfInfection[1])
    
    def getRandomBoolean(self, probability):
        """Returns true or false depending on a given probability."""
        return self.getRandomNumber() < probability
