import numpy as np
from config import *

class Neuron:
    objs_n = 0
    def __init__(self, _type):
        self.type = _type
        self.id = Neuron.objs_n
        Neuron.objs_n += 1

        self.received_nb = 0
        self.received_val = 0
        self.input_conn = []
        self.output_conn = []
        self.enabled = True

    def reset(self):
        self.received_nb = 0
        self.received_val = 0

    def disable(self):
        for conn in self.input_conn:
            conn.disable()
        for conn in self.output_conn:
            conn.disable()
        self.enabled = False

    def receive(self, val):
        self.received_val += val
        self.received_nb += 1

    def sigmoid(self, x):
        return 1.0 / (1.0 + np.exp(-x, dtype=np.float128))

    def output_value(self):
        return self.sigmoid(self.received_val)

    def fire(self):
        rcv_value = None
        for conn in self.output_conn:
            if conn.enabled:
                rcv_value = self.output_value() * conn.weight
                conn.out_neuron.receive(rcv_value)

        if not self.ready():
            for in_c in self.input_conn:
                in_c.in_neuron.fire()

        return rcv_value

    def ready(self):
        enabled_in_neurons_n = len([c for c in self.input_conn if c.in_neuron.enabled])
        return self.received_nb == enabled_in_neurons_n

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

    def disable(self):
        self.enable = False

    def connect_neurons(self):
        self.in_neuron.add_output_connection(self)
        self.out_neuron.add_input_connection(self)

    def mutate_weight(self):
        if np.random.uniform(0,1) <= WEIGHT_SMALL_MUTATION_PROB:
            if np.random.uniform(0,1) <= WEIGHT_BIG_MUTATION_PROB:
                self.randomize_weight()
            else:
                self.weight += np.random.uniform(-0.3, 0.3)

        if self.weight > 1:
            self.weight = 1
        elif self.weight < 0:
            self.weight = 0

    def randomize_weight(self):
        self.weight = np.random.uniform(0, 1)

