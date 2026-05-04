import pygame

class Projectile:
    def __init__(self, x, y, radius, color, velocity):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.velocity = velocity

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)