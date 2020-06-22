import pygame
import random
import sys
import time

from overview import logger
import neat
from config import *
from net_repr import NetworkRepresentation
# TODO: make it better

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
WIDTH = 70
HEIGHT = 70
MARGIN = 5
GRAVITY = 10
JUMP_STRENGTH = 5
JUMP_LENGTH = 12
WINDOW_SIZE = (400, 500)
SHRINK_RECTS = .8
SPEED = 60
BIRD_X = 100
NET_POS = (50, 50)

def convert_to_rect(sprite, pos):
    rect = sprite.get_rect()
    rect.x = pos[0]
    rect.y = pos[1]

    return rect

class Rect:
    def __init__(self, sprite, pos):
        self.rect = convert_to_rect(sprite, pos)


class PipeCoords:
    def __init__(self, space, x_speed=5, y_range=100):
        self.y = random.randint(-y_range, y_range)
        self.x = 400
        self.space = space
        self.x_speed = x_speed
        self.y_range = y_range

        self.scored = False

    def get_pipes_coords(self):
        """
        IMPLICITLY INCREMENT THE X COORD
        """
        self.x -= self.x_speed
        if self.x < -100:
            self.x = 400
            self.y = random.randint(-self.y_range, self.y_range)
            self.scored = False
        return [(self.x, 300+ self.y + self.space // 2), (self.x, -300 + self.y - self.space // 2) ]

    def score(self):
        self.scored = True

    @property
    def bot_coords(self):
        return self.get_pipes_coords()[0]

    @property
    def top_coords(self):
        return self.get_pipes_coords()[1]


class Pipe:

    def __init__(self, pipe_coords, _type="top"):
        self.pipe_coords = pipe_coords
        self.type = _type
        if _type == "top":
            self.sprite = pygame.image.load('images/top.png')
        else:
            self.sprite = pygame.image.load('images/bottom.png')

        self.scored = False

    @property
    def coords(self):
        if self.type == "top":
            coords = self.pipe_coords.top_coords
        else:
            coords = self.pipe_coords.bot_coords
        return coords

    def draw(self, screen):
        screen.blit(self.sprite, self.coords)

    @property
    def rect(self):
        return convert_to_rect(self.sprite, self.coords)

class Bird:

    def __init__(self):
        self.sprite = pygame.image.load('images/bird1.png')
        self.pos = [BIRD_X,250]
        self.jumping = 0


    @property
    def rect(self):
        rect =  convert_to_rect(self.sprite, self.pos)
        rect.width *= SHRINK_RECTS
        rect.height  *= SHRINK_RECTS
        return rect

    def draw(self, screen):
        if self.jumping != 0:
            self.jumping -= 1
            self.pos[1] -= int(JUMP_STRENGTH * self.jumping / 2)

        pygame.draw.circle(screen, (255, 0, 0), self.pos, 2)

        screen.blit(self.sprite, self.pos)
        self.pos[1] += GRAVITY

    def jump(self):
        if self.jumping != 0:
            return False
        self.jumping = JUMP_LENGTH

    def __repr__(self):
        return "<BIRD {} ({},{})>".format(self.id, self.pos[0], self.pos[1])


pygame.init()


screen = pygame.display.set_mode(WINDOW_SIZE)
font = pygame.font.Font('freesansbold.ttf', 32)


def collide_pipes(bird, top_pipe, bottom_pipe):
    if pygame.sprite.collide_rect(bird, top_pipe):
        return True
    elif pygame.sprite.collide_rect(bird, bottom_pipe):
        return True

def collide_win(bird,):
    if bird.pos[1] <= 0 or bird.pos[1] >= WINDOW_SIZE[1]:
        return True
    return False


def flappy_bird_game(pool):
    global SPEED

    pipe_coords = PipeCoords(20, x_speed=SPEED)
    top_pipe = Pipe(pipe_coords, _type="top")
    bottom_pipe = Pipe(pipe_coords, _type="bottom")
    background = pygame.image.load('images/background.png')

    pool.reset()
    birds = [Bird() for _ in range(pool.population_nb)]
    dead_birds = 0
    points = 0

    net_repr = NetworkRepresentation(pool.population[0].network, 350, 100, scale=2, margin=5)


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN:
                # if event.key == pygame.K_SPACE:
                #     bird.jump()
                if event.key == pygame.K_MINUS:
                    SPEED -= 0.5*SPEED
                if event.key == pygame.K_PLUS:
                    SPEED += 0.5*SPEED
                if event.key == pygame.K_0:
                    SPEED = 5


        screen.blit(background, (0,-100))
        bottom_pipe.draw(screen)
        top_pipe.draw(screen)


        if top_pipe.coords[0] - pipe_coords.x_speed < BIRD_X < top_pipe.coords[0] + pipe_coords.x_speed:
            points += 1

        for bird, organism in zip(birds, pool.population):
            inputs = [bird.jumping, bird.pos[1], top_pipe.coords[0] ,top_pipe.coords[1], bottom_pipe.coords[1]]

            if len(birds) == dead_birds:
                    return birds

            if not organism.is_alive:
                continue

            if organism.decision(inputs) == 1:
                bird.jump()

            bird.draw(screen)


            if collide_win(bird) or collide_pipes(bird, top_pipe, bottom_pipe):
                organism.is_alive = 0
                organism.fitness = points
                dead_birds += 1

        screen.blit(net_repr.get_surface(), NET_POS)

        text = font.render(str(points), True, (0,0,0), (255,255,255))
        screen.blit(text, (10,10))

        time.sleep(1/SPEED)

        pygame.display.flip()

pool = neat.Pool(POPULATION)

gen = 0
while True:
    flappy_bird_game(pool)
    pool.new_gen()

    logger.print_infos(pool)
    logger.print_infos(pool.population[0])
    gen += 1




