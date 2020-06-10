import pygame
import random
import sys
import time

import neat
from config import *
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
SPEED = 1

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

    def get_pipes_coords(self):
        """
        IMPLICITLY INCREMENT THE X COORD
        """
        self.x -= self.x_speed
        if self.x < -100:
            self.x = 400
            self.y = random.randint(-self.y_range, self.y_range)
        return [(self.x, 300+ self.y + self.space // 2), (self.x, -300 + self.y - self.space // 2) ]
    
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
        self.pos = [100,250]
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
        self.jumping = JUMP_LENGTH

    def __repr__(self):
        return "<BIRD {}>".format(self.pos)
        

pygame.init() 
 

screen = pygame.display.set_mode(WINDOW_SIZE)
pipe_coords = PipeCoords(20, x_speed=SPEED)
top_pipe = Pipe(pipe_coords, _type="top")
bottom_pipe = Pipe(pipe_coords, _type="bottom")
background = pygame.image.load('images/background.png')


def is_dead(bird, top_pipe, bottom_pipe):
    if pygame.sprite.collide_rect(bird, top_pipe):
        return True
    elif pygame.sprite.collide_rect(bird, bottom_pipe):
        return True
    if bird.pos[1] < 0 or bird.pos[1] > WINDOW_SIZE[1]:
        return True
    return False


def flappy_bird_game(pool):
    birds = [Bird() for _ in range(pool.population_nb)]
    dead_birds = 0
    points = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
                
            # if event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_SPACE:
            #         bird.jump()
            


        screen.blit(background, (0,-100))
        bottom_pipe.draw(screen)
        top_pipe.draw(screen)

        if top_pipe.coords[0] == birds[0].pos[0]:
            points += 1

        inputs = [birds[0].pos[1], top_pipe.coords[0] ,top_pipe.coords[1], bottom_pipe.coords[1]]
        for bird, organism in zip(birds, pool.population):
            print(bird.pos)
            if not organism.is_alive:
                continue

            if organism.decision(inputs) == 1:
                bird.jump()

            bird.draw(screen)

            if is_dead(bird, top_pipe, bottom_pipe):
                organism.is_alive = 0
                organism.fitness = points
                dead_birds += 1
                if len(birds) == dead_birds:
                    return birds
        

        pygame.display.flip()

pool = neat.Pool(POPULATION)

while True:

    flappy_bird_game(pool)
    time.sleep(0.5)
    pool.new_gen()


     