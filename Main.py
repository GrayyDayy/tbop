import pygame
from Projectiles import Projectile
import time
import json

with open("config.json") as file:
    config = json.load(file)

with open("enemies.json") as file:
    enemy_config = json.load(file)


enemy_data = enemy_config["enemito_one"]
enemy_health = enemy_data["health"]
enemy_speed = enemy_data["speed"]
enemy_size = enemy_data["size"]

player_health = config["player_health"]
player_speed = config["player_speed"]
bullet_speed = config["bullet_speed"]
bullet_size = config["bullet_size"]
bullet_color = config["bullet_color"]
cooldown = config["cooldown"]


pygame.init()
screen = pygame.display.set_mode()
clock = pygame.time.Clock()
running = True
dt = 0
bullets = []
cooldown = 0.5
timesinceshot = 0
facingleft = False
facingright = False
facingup = False
facingdown = True

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
enemy_pos = pygame.Vector2(200, 200)

while running:
    currenttime = time.time()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for bullet in bullets[:]:
        bullet.x += bullet.vel_x
        bullet.y += bullet.vel_y

        if not (0 < bullet.x < screen.get_width() and 0 < bullet.y < screen.get_height()):
            bullets.remove(bullet)

    screen.blit(pygame.transform.scale(pygame.image.load("sprites/startroom.png"),(screen.get_width(), screen.get_height())), (0, 0), area=screen.get_rect())

    if facingleft:
        screen.blit(pygame.image.load("sprites/leftp.png"), (player_pos.x - 75, player_pos.y - 88),
                    area=screen.get_rect())
    elif facingright:
        screen.blit(pygame.image.load("sprites/rightp.png"), (player_pos.x - 75, player_pos.y - 88),
                    area=screen.get_rect())
    elif facingup:
        screen.blit(pygame.image.load("sprites/backp.png"), (player_pos.x - 75, player_pos.y - 88),
                    area=screen.get_rect())
    elif facingdown:
        screen.blit(pygame.image.load("sprites/frontp.png"), (player_pos.x - 75, player_pos.y - 88),
                    area=screen.get_rect())

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        facingleft = False
        facingright = False
        facingup = True
        facingdown = False
        player_pos.y -= int(player_speed) * dt
    if keys[pygame.K_s]:
        facingleft = False
        facingright = False
        facingup = False
        facingdown = True
        player_pos.y += int(player_speed) * dt
    if keys[pygame.K_a]:
        facingleft = True
        facingright = False
        facingup = False
        facingdown = False
        player_pos.x -= int(player_speed) * dt
    if keys[pygame.K_d]:
        facingleft = False
        facingright = True
        facingup = False
        facingdown = False
        player_pos.x += int(player_speed) * dt
    if keys[pygame.K_UP]:
        facingleft = False
        facingright = False
        facingup = True
        facingdown = False
        if currenttime - timesinceshot > cooldown:
            timesinceshot = currenttime
            if len(bullets) < 6:
                bullets.append(Projectile(player_pos.x,player_pos.y, bullet_size, bullet_color, 0, -bullet_speed))
    if keys[pygame.K_DOWN]:
        facingleft = False
        facingright = False
        facingup = False
        facingdown = True
        if currenttime - timesinceshot > cooldown:
            timesinceshot = currenttime
            if len(bullets) < 6:
                bullets.append(Projectile(player_pos.x,player_pos.y, bullet_size, bullet_color, 0, bullet_speed))
    if keys[pygame.K_LEFT]:
        facingleft = True
        facingright = False
        facingup = False
        facingdown = False
        if currenttime - timesinceshot > cooldown:
            timesinceshot = currenttime
            if len(bullets) < 6:
                bullets.append(Projectile(player_pos.x,player_pos.y, bullet_size, bullet_color, -bullet_speed, 0))
    if keys[pygame.K_RIGHT]:
        facingleft = False
        facingright = True
        facingup = False
        facingdown = False
        if currenttime - timesinceshot > cooldown:
            timesinceshot = currenttime
            if len(bullets) < 6:
                bullets.append(Projectile(player_pos.x,player_pos.y, bullet_size, bullet_color, bullet_speed, 0))



    for bullet in bullets:
        bullet.draw(screen)

    pygame.display.flip()

    dt = clock.tick(60) / 1000

pygame.quit()