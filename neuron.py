import numpy as np
from config import *

class Neuron:
    def __init__(self, _id, _type):
        self.type = _type
        self.id = _id

        self.received_nb = 0
        self.reveived_val = 0
        self.input_conn = []
        self.output_conn = []

    def receive(self, val):
        self.reveived_val += val
        self.received_nb += 1

    def sigmoid(self, x):
        return 1.0 / (1.0 + np.exp(-x))

    def output_value(self):
        return self.sigmoid(self.reveived_val)

    def fire(self):
        for conn in self.output_conn:
            if conn.enabled:
                rcv_value = self.sigmoid(self.reveived_val) * conn.weight
                conn.out_neuron.receive(rcv_value)

    def ready(self):
        return self.reveived_nb == len(self.input_conn)

    def add_input_connection(self, conn):
        self.input_conn.append(conn)

    def add_output_connection(self, conn):
        self.output_conn.append(conn)


class Connection:
    def __init__(self, in_neuron, out_neuron, innov_id, enabled=True):
        self.in_neuron = in_neuron
        self.out_neuron = out_neuron
        self.innov_id = innov_id
        self.enabled = enabled

        self.weight = 0
        self.randomize_weight()
        self.connect_neurons()

    def connect_neurons(self):
        self.in_neuron.add_output_connection(self)
        self.out_neuron.add_input_connection(self)

    def mutate_weight(self):
        if np.random.uniform(0,1) <= WEIGHT_SMALL_MUTATION_PROB:
            if np.random.uniform(0,1) <= WEIGHT_BIG_MUTATION_PROB:
                self.randomize_weight() 
            else:
                self.weight += np.random.uniform(-0.1, 0.1)
            
    def randomize_weight(self):
        self.weight = np.random.uniform(0, 1)

