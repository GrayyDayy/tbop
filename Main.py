import pygame
from Projectiles import Projectile
import time
import json

with open("config.json") as file:
    config = json.load(file)

player_health = config["player_health"]
player_speed = config["player_speed"]
bullet_speed = config["bullet_speed"]
bullet_size = config["bullet_size"]
bullet_color = config["bullet_color"]
cooldown = config["cooldown"]


pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0
bullets = []
cooldown = 0.5
timesinceshot = 0

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

while running:
    currenttime = time.time()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for bullet in bullets[:]:
        bullet.x += bullet.vel_x
        bullet.y += bullet.vel_y

        if not (0 < bullet.x < 1280 and 0 < bullet.y < 720):
            bullets.remove(bullet)

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
        if currenttime - timesinceshot > cooldown:
            timesinceshot = currenttime
            if len(bullets) < 6:
                bullets.append(Projectile(player_pos.x,player_pos.y, bullet_size, bullet_color, 0, -bullet_speed))
    if keys[pygame.K_DOWN]:
        if currenttime - timesinceshot > cooldown:
            timesinceshot = currenttime
            if len(bullets) < 6:
                bullets.append(Projectile(player_pos.x,player_pos.y, bullet_size, bullet_color, 0, -bullet_speed))
    if keys[pygame.K_LEFT]:
        if currenttime - timesinceshot > cooldown:
            timesinceshot = currenttime
            if len(bullets) < 6:
                bullets.append(Projectile(player_pos.x,player_pos.y, bullet_size, bullet_color, 0, -bullet_speed))
    if keys[pygame.K_RIGHT]:
        if currenttime - timesinceshot > cooldown:
            timesinceshot = currenttime
            if len(bullets) < 6:
                bullets.append(Projectile(player_pos.x,player_pos.y, bullet_size, bullet_color, 0, -bullet_speed))



    for bullet in bullets:
        bullet.draw(screen)

    pygame.display.flip()

    dt = clock.tick(60) / 1000

pygame.quit()