import numpy as np

from config import *
from network import Network


class Organism:
    def __init__(self, network=None):
        if network is None:
            network = Network(TOPOLOGY)
        self.network = network
        self.fitness = 0
        self.is_alive = 1

    def decision(self, inputs):
        out = self.network.forward_prop(inputs)
        if out[0] >= FLAP_THRESHOLD:
            return 1
        return 0

    def clone(self):
        return Organism(network=self.network)
    
    def mutate(self):
        options = [
            self.network.add_random_neuron,
            self.network.del_random_neuron,
            self.network.add_random_connection,
            self.network.del_random_connection
        ]
        np.random.choice(options)()

    def get_mutant_child(self):
        child = self.clone()
        child.mutate()
        return child

    




