from organism import Organism

class Pool:
    def __init__(self, init_population_nb):
        self.population = []
        self.init_population_nb = init_population_nb
        self.gen = 0

        self.init_organisms()

    @property
    def population_nb(self):
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



