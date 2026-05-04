import pygame
from Projectiles import Projectile
import time

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0
bullets = []
cooldown = 1
timesinceshot = 0
shootingleft = False
shootingright = False
shootingup = False
shootingdown = False

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

while running:
    currenttime = time.time()
    print(currenttime)
    print(timesinceshot)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for bullet in bullets:
        if shootingleft or shootingright:
            if 1280 > bullet.x > 0:
                bullet.x += bullet.velocity
            else:
                bullets.pop(bullets.index(bullet))
        if shootingup or shootingdown:
            if 720 > bullet.y > 0:
                bullet.y += bullet.velocity
            else:
                bullets.pop(bullets.index(bullet))


    screen.fill("white")

    pygame.draw.circle(screen, "green", player_pos, 40)
    pygame.draw.circle(screen, "blue", player_pos, 20)
    pygame.draw.circle(screen, "black", player_pos, 10)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_pos.y -= 300 * dt
    if keys[pygame.K_s]:
        player_pos.y += 300 * dt
    if keys[pygame.K_a]:
        player_pos.x -= 300 * dt
    if keys[pygame.K_d]:
        player_pos.x += 300 * dt
    if keys[pygame.K_UP]:
        if currenttime - timesinceshot > cooldown:
            timesinceshot = currenttime
            shootingleft = False
            shootingright = False
            shootingup = True
            shootingdown = False
            if len(bullets) < 6:
                bullets.append(Projectile(player_pos.x,player_pos.y,12,"blue",-5))
    if keys[pygame.K_DOWN]:
        if currenttime - timesinceshot > cooldown:
            timesinceshot = currenttime
            shootingleft = False
            shootingright = False
            shootingup = False
            shootingdown = True
            if len(bullets) < 6:
                bullets.append(Projectile(player_pos.x,player_pos.y,12,"blue",5))
    if keys[pygame.K_LEFT]:
        if currenttime - timesinceshot > cooldown:
            timesinceshot = currenttime
            shootingleft = True
            shootingright = False
            shootingup = False
            shootingdown = False
            if len(bullets) < 6:
                bullets.append(Projectile(player_pos.x,player_pos.y,12,"blue",-5))
    if keys[pygame.K_RIGHT]:
        if currenttime - timesinceshot > cooldown:
            timesinceshot = currenttime
            shootingleft = False
            shootingright = True
            shootingup = False
            shootingdown = False
            if len(bullets) < 6:
                bullets.append(Projectile(player_pos.x,player_pos.y,12,"blue",5))



    for bullet in bullets:
        bullet.draw(screen)

    pygame.display.flip()

    dt = clock.tick(60) / 1000

pygame.quit()