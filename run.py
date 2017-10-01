from simulation import Simulation

# run simulation
simulation = Simulation(50, 0.1, 0.1, [2, 6])
simulation.run()

# output
for x in range(0, 50):
    print(",".join(str(v) for v in simulation.population[x*50:x*50+50]))