import numpy as np

from organism import Organism
from overview import logger

class Pool:
    def __init__(self, init_population_nb):
        self.population = []
        self.init_population_nb = init_population_nb
        self.gen = 0

        self.init_organisms()
        logger.add_var("network_output")

    @property
    def population_nb(self):
        return len(self.population)

    def print_infos(self):
        print("----------------------")

        print("Fitness infos:")
        fitnesses = sorted([o.fitness for o in self.population])
        print("MAX:", fitnesses[-1])
        print("MIN:", fitnesses[0])
        print("MEAN:", np.mean(fitnesses))
        logger.print_var_mean("network_output")

        print("----------------------")


    def __len__(self):
        return len(self.population)

    def init_organisms(self):
        for _ in range(self.init_population_nb):
            self.population.append(Organism())

    def new_gen(self):
        self.gen += 1

        # Sort by fitness
        self.population.sort(key=lambda o: o.fitness)

        best = self.population[-10:]
        new_pop = best + [c.get_mutant_child() for c in best]

        self.population = new_pop

    def reset(self):
        for org in self.population:
            org.reset()



