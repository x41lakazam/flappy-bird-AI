import random
import numpy as np 
from neuron import Connection, Neuron

class Innovation:
    
    _innov_nb = 0

    @property
    @classmethod
    def innov_nb(cls):
        cls._innov_nb += 1
        return cls._innov_nb - 1
    

class Network:
    def __init__(self, topology):
        self.topology = topology
        self.conns = []
        self.layers = []
        
        self.init_neurons()
        self.init_connections()

    def init_neurons(self):
        for layer_ix, layer_size in enumerate(self.topology):
            layer = []
            if layer_ix == 0:
                _type = 'input'
            elif layer_ix == len(self.topology)-1:
                _type = 'output'
            else:
                _type = 'hidden'
            for _ in range(layer_size):
                neuron = Neuron(_type)
                layer.append(neuron)
            self.layers.append(layer)


    def init_connections(self):
        for layer_ix, layer in enumerate(self.layers[:-1]):
            next_layer = self.layers[layer_ix + 1]
            for neuron in layer:
                for next_neuron in next_layer:
                    if np.random.uniform(0,1) <= 0.25:
                        conn = Connection(neuron, next_neuron, Innovation.innov_nb)
                        self.conns.append(conn)  
                        
    def add_random_neuron(self):
        origin_ix = np.random.randint(1, len(self.layers)-1)
        neuron = Neuron('hidden')
        new_layer = [neuron]
        before_layer = random.choice(self.layers[:origin_ix])
        after_layer = random.choice(self.layers[origin_ix:])
        before_neuron = random.choice(before_layer)
        after_neuron = random.choice(after_layer)

        for conn in before_neuron.output_conn:
            if after_neuron == conn.out_neuron:
                conn.disable() 
        
        innov_id = Innovation.innov_nb
        self.conns.append(Connection(before_neuron, neuron, innov_id))
        self.conns.append(Connection(neuron, after_neuron, innov_id))

    def del_random_neuron(self):
        random_neuron = np.random.choice(np.random.choice(self.layers))
        random_neuron.disable()
    
    def add_random_connection(self):
        layer1_ix = np.random.randint(len(self.layers)-1)
        layer2_ix = np.random.randint(len(self.layers))

        first = min(layer1_ix, layer2_ix)
        second = max(layer1_ix, layer2_ix)
        if first == second:
            second += 1

        random_neuron1 = np.random.choice(self.layers[first])
        random_neuron2 = np.random.choice(self.layers[second])

        conn = Connection(random_neuron1, random_neuron2, Innovation.innov_nb)
        self.conns.append(conn)

    def del_random_connection(self):
        conn = np.random.choice(self.conns)
        conn.disable()

    def forward_prop(self, inputs):
        for ix, neuron in enumerate(self.layers[0]):

            neuron.receive(inputs[ix])
            neuron.fire()

        for hidden in self.layers[1:-1]:
            for neuron in hidden:
                neuron.fire()

        return [neuron.output_value() for neuron in self.layers[-1]]





            