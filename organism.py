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




