from organism import Organism

class Pool:
    def __init__(self, population_nb):
        self.population = []
        self.population_nb = population_nb
        self.gen = 0

        self.init_organisms()

    def init_organisms(self):
        for _ in range(self.population_nb):
            self.population.append(Organism())
