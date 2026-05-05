import pygame

class Projectile:
    def __init__(self, x, y, radius, color, vel_x, vel_y):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.vel_x = vel_x
        self.vel_y = vel_y

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)