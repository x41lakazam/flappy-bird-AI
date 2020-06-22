import pygame

class NeuronRepresentation:

    def __init__(self, coords, size=3, color=(255,255,255)):
        self.coords = coords
        self.size = size
        self.color = color

    def draw(self, surface):
        pygame.draw.circle(surface,
                           self.color,
                           self.coords,
                           self.size,
                          )

class ConnectionRepresentation:

    def __init__(self, in_neuron, out_neuron, width=1, color=(100, 100 ,100)):
        self.start_pos  = in_neuron.coords
        self.end_pos    = out_neuron.coords
        self.width      = width
        self.color      = color

    def draw(self, surface):
        pygame.draw.line(surface,
                         self.color,
                         self.start_pos,
                         self.end_pos,
                         self.width
                          )


class NetworkRepresentation:

    def __init__(self, network, width, height, scale, margin):
        self.scale = scale
        self.margin = margin
        self.network = network
        self.surface = pygame.surface.Surface((width, height))

        self.neuron_id_inc  = 0
        self.conn_id_inc    = 0

    def draw(self):

        neurons        = {}

        for x, layer in enumerate(self.network.layers):
            for y, neuron in enumerate(layer):
                x = int(x*self.scale + self.margin)
                y = int(y * 8 *self.scale + self.margin)
                self.neuron_id_inc += 1
                neuron_repr = NeuronRepresentation(coords=(x, y))
                neurons[neuron.id] = neuron_repr
                neuron_repr.draw(self.surface)

        for connection in self.network.conns:
            in_neuron = neurons[connection.in_neuron.id]
            out_neuron = neurons[connection.out_neuron.id]

            opacity = int(255 * connection.weight)

            representation = ConnectionRepresentation(in_neuron, out_neuron, color=(opacity, opacity, opacity))
            representation.draw(self.surface)

    def get_surface(self):
        self.draw()
        return self.surface




