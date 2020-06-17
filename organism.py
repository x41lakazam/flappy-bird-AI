import numpy as np

from config import *
from network import Network
from overview import logger


class Organism:
    def __init__(self, network=None):
        if network is None:
            network = Network(TOPOLOGY)
        self.network = network
        self.fitness = 0
        self.is_alive = 1

    def reset(self):
        self.network.reset()
        self.is_alive = 1
        self.fitness = 0

    def print_infos(self):
        self.network.print_infos()

    def decision(self, inputs):
        
        out = self.network.forward_prop(inputs)
        logger.add_var_value("network_output", out)

        if out[0] >= FLAP_THRESHOLD:
            return 1
        return 0

    def clone(self):
        return Organism(network=self.network)
    
    def mutate(self):
        options = [
            # self.network.add_random_neuron,
            self.network.del_random_neuron,
            # self.network.add_random_connection,
            self.network.del_random_connection,
            self.network.mutate_weights,
        ]

        # DEBUG
        try:
            func = np.random.choice(options)
            func()
        except ValueError:
            print("SOMETHING CRASHED HERE, DEBUG ME (organism.py line 43=, function mutate)")
            import ipdb; ipdb.set_trace()

    def get_mutant_child(self):
        child = self.clone()
        child.mutate()
        return child

    




