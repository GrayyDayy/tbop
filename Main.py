from distutils.command.config import config

import pygame
import json

with open ("config.json") as file:
    config = json.load(file)

player_speed = config["player_speed"]

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("white")

    pygame.draw.circle(screen, "green", player_pos, 40)
    pygame.draw.circle(screen, "blue", player_pos, 20)
    pygame.draw.circle(screen, "black", player_pos, 10)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_pos.y -= int(player_speed) * dt
    if keys[pygame.K_s]:
        player_pos.y += int(player_speed) * dt
    if keys[pygame.K_a]:
        player_pos.x -= int(player_speed) * dt
    if keys[pygame.K_d]:
        player_pos.x += int(player_speed) * dt
    if keys[pygame.K_UP]:
        pygame.draw.circle(screen, "blue", player_pos, 10)
    if keys[pygame.K_DOWN]:
        pygame.draw.circle(screen, "blue", player_pos, 10)
    if keys[pygame.K_LEFT]:
        pygame.draw.circle(screen, "blue", player_pos, 10)
    if keys[pygame.K_RIGHT]:
        pygame.draw.circle(screen, "blue", player_pos, 10)

    pygame.display.flip()

    dt = clock.tick(60) / 1000



pygame.quit()
