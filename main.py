import sys
import pygame as pg
from sprites import Particle, Ray, Boundary
from settings import *
from random import randint
vec = pg.math.Vector2

class Game():
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(SCREEN_SIZE)
        pg.display.set_caption(CAPTION)
        self.clock = pg.time.Clock()
        self.pipetime = pg.time.get_ticks()
        pg.mouse.set_visible(False)

    def new(self):
        # Set up a new game by setting up sprite groups
        self.all = pg.sprite.Group()
        self.all_rays = pg.sprite.Group()
        self.all_particles = pg.sprite.Group()
        self.all_walls = pg.sprite.Group()
        self.particle = Particle(self)

        for particle in self.all_particles:
            for angle in range(0,360,5):
                self.ray = Ray(self, particle, angle)

        for i in range(3):
            self.wall = Boundary(self, \
            vec(randint(0, SCREEN_WIDTH), randint(0, SCREEN_HEIGHT)), \
            vec(randint(0, SCREEN_WIDTH), randint(0, SCREEN_HEIGHT)))

    def run(self):
        # Main game loop, set running = False to end game
        self.running = True
        while self.running:
            self.dt_ms = self.clock.tick(FPS) # Return loop duration in milliseconds, limit max framerate to 'FPS'
            self.dt_s = self.clock.tick(FPS) / 1000 # Return loop duration in seconds, limit max framerate to 'FPS'
            self.events()
            self.update()
            self.render()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()

    def update(self):
        self.all.update()

    def render(self):
        self.screen.fill((255,0,0))
        self.all_particles.draw(self.screen)
        i = 0
        for ray in self.all_rays:
            pg.draw.aaline(self.screen, (255,255,255), ray.pt1, ray.pt2)
        for wall in self.all_walls:
            pg.draw.aaline(self.screen, (0,0,0), wall.pt1, wall.pt2)
        pg.display.flip()

    def quit(self):
        pg.quit()
        sys.exit()

game = Game()
game.new()
game.run()
