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
        neuron_ix = 0
        for layer_ix, layer_size in enumerate(self.topology):
            layer = []
            if layer_ix == 0:
                _type = 'input'
            elif layer_ix == len(self.topology)-1:
                _type = 'output'
            else:
                _type = 'hidden'
            for _ in range(layer_size):
                neuron = Neuron(neuron_ix, _type)
                neuron_ix += 1
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
                        
    def add_neuron(self, layer):
        self.layers[]

    def forward_prop(self, inputs):
        for ix, neuron in enumerate(self.layers[0]):

            neuron.receive(inputs[ix])
            neuron.fire()

        for hidden in self.layers[1:-1]:
            for neuron in hidden:
                neuron.fire()

        return [neuron.output_value() for neuron in self.layers[-1]]





            