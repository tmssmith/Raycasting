import pygame as pg
import pygame.gfxdraw
vec = pg.math.Vector2
from settings import *
from random import randint

class Particle(pg.sprite.Sprite):
    """
    Docstring for Particle class
    """

    def __init__(self, game):
        self.groups = game.all, game.all_particles
        super().__init__(self.groups)
        self.game = game
        self.image = pg.Surface([20,20], pg.SRCALPHA)
        self.rect = self.image.get_rect()
        pg.gfxdraw.aacircle(self.image, 10, 10, 9, (255, 255, 255))
        pg.gfxdraw.filled_circle(self.image, 10, 10, 9, (255, 255, 255))

    def update(self):
        self.pos = pg.mouse.get_pos()
        self.rect.center = self.pos

class Ray(pg.sprite.Sprite):
    """
    Docstring for Ray class
    """

    def __init__(self, game, particle, angle):
        self.groups = game.all, game.all_rays
        super().__init__(self.groups)
        self.game = game
        self.particle = particle
        self.dir = vec.rotate(vec(0,-1), angle)

    def update(self):
        x1 = int(self.particle.pos[0])
        y1 = int(self.particle.pos[1])
        x2 = int(x1 + self.dir[0]*SCREEN_WIDTH*1.5)
        y2 = int(y1 + self.dir[1]*SCREEN_WIDTH*1.5)
        self.pt1 = vec(x1, y1)
        self.pt2 = vec(x2, y2)

        shortest = SCREEN_WIDTH*1.5
        tmp_pt2 = self.pt2

        for wall in self.game.all_walls:
            if self.intersects(wall):
                t = self.t_num / self.den
                intercept = vec(int(x1+t*(x2-x1)), int(y1+t*(y2-y1)))
                if t <= shortest:
                    shortest = t
                    tmp_pt2 = intercept
        self.pt2 = tmp_pt2

    def intersects(self, wall):
        x1 = self.pt1[0]
        y1 = self.pt1[1]
        x2 = self.pt2[0]
        y2 = self.pt2[1]
        x3 = wall.pt1[0]
        y3 = wall.pt1[1]
        x4 = wall.pt2[0]
        y4 = wall.pt2[1]

        den = (x1-x2)*(y3-y4)-(y1-y2)*(x3-x4)
        t_num = (x1-x3)*(y3-y4)-(y1-y3)*(x3-x4)
        u_num = -((x1-x2)*(y1-y3)-(y1-y2)*(x1-x3))

        if (
            (den!=0) &
            (abs(t_num)<=abs(den)) &
            (abs(t_num+den)==abs(t_num)+abs(den)) &
            (abs(u_num)<=abs(den)) &
            (abs(u_num+den)==abs(u_num)+abs(den))
            ):
            self.den = den
            self.t_num = t_num
            self.u_num = u_num
            return True
        else:
            return False


class Boundary(pg.sprite.Sprite):
    """
    Docstring for Boundary class
    """

    def __init__(self, game, pt1, pt2):
        self.groups = game.all, game.all_walls
        super().__init__(self.groups)
        self.game = game
        self.pt1 = pt1
        self.pt2 = pt2

    def update(self):
        pass
