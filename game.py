import pygame
import random
import sys

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


class Bird:
    def __init__(self):
        self.sprite = pygame.image.load('images/bird1.png')
        self.pos = [100,250]
        self.jumping = 0
        self.rect = convert_to_rect(self.sprite, self.pos)

    def draw(self, screen):
        if self.jumping != 0:
            self.jumping -= 1
            self.pos[1] -= JUMP_STRENGTH * self.jumping / 2

        screen.blit(self.sprite, self.pos)
        self.pos[1] += GRAVITY
    
    def jump(self):
        self.jumping = JUMP_LENGTH
        

pygame.init()
 

screen = pygame.display.set_mode(WINDOW_SIZE)
pipe_coords = PipeCoords(25)
bird = Bird()
top_pipe = pygame.image.load('images/top.png')
bottom_pipe = pygame.image.load('images/bottom.png')
background = pygame.image.load('images/background.png')


while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird.jump()

        if pygame.sprite.collide_rect(bird, Rect(bottom_pipe, pipe_coords.get_pipes_coords()[0])):
            print("bottom pipe killed you")
            sys.exit()

        if pygame.sprite.collide_rect(bird, Rect(top_pipe, pipe_coords.get_pipes_coords()[1])):
            print("top pipe killed you")
            sys.exit()
            

    screen.blit(background, (0,-100))
    screen.blit(bottom_pipe, Rect(bottom_pipe, pipe_coords.get_pipes_coords()[0]).rect)
    screen.blit(top_pipe, Rect(top_pipe, pipe_coords.get_pipes_coords()[1]).rect)
    bird.draw(screen)
    
    pygame.display.flip()

    