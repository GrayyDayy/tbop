import pygame
from Projectiles import Projectile
import time
import json
import random

with open("config.json") as file:
    config = json.load(file)

with open("enemies.json") as file:
    enemy_config = json.load(file)

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
timesinceshot = 0

facingleft, facingright, facingup, facingdown = False, False, False, True
player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

background_img = pygame.transform.scale(pygame.image.load("sprites/startroom.png"),
                                        (screen.get_width(), screen.get_height()))
player_sprites = {
    "left": pygame.image.load("sprites/leftp.png"),
    "right": pygame.image.load("sprites/rightp.png"),
    "up": pygame.image.load("sprites/backp.png"),
    "down": pygame.image.load("sprites/frontp.png")
}

enemy_sprite_cache = {}
for name, data in enemy_config.items():
    enemy_sprite_cache[name] = pygame.image.load(data["image"])

class Enemy:
    def __init__(self, enemyname, x, y):
        self.name = enemyname
        stats = enemy_config[enemyname]
        self.health = stats["health"]
        self.speed = stats["speed"]
        self.size = stats["size"]
        self.image = enemy_sprite_cache[enemyname]
        self.pos = pygame.Vector2(x, y)

    def update(self, player_posi, delt):
        direction = player_posi - self.pos
        distance = direction.length()
        if distance > 5:
            direction = direction.normalize()
            self.pos += direction * self.speed * delt

    def draw(self, surface):
        # Anchor transformations relative to center origins
        surface.blit(self.image, (int(self.pos.x - 230), int(self.pos.y - 144)))

waves = {
    1: ["elbooger"],
    2: ["elbooger", "elbooger"],
    3: ["elbooger", "elwebo"],
    4: ["elwebo", "hexemo"],
    5: ["sabubble"],
    6: ["eyeloco"],
    7: ["eyeloco", "hexemo"],
    8: ["squarely", "squarely", "squarely", "squarely", "squarely", "squarely", "squarely", "squarely", "squarely", "squarely", "squarely"],
    9: ["uglo", "beautifo"],
    10: ["ryazz"],
    11: ["eyeloco", "eyeloco", "elwebo", "hexemo"],
    12: ["diablonaranja"],
    13: ["diabloverde"],
    14: ["diablorosa"],
    15: ["edperor"]
}

current_wave = 1
active_enemies = []
spawn_points = [
    pygame.Vector2(100, 100),
    pygame.Vector2(screen.get_width() - 100, 100),
    pygame.Vector2(100, screen.get_height() - 100),
    pygame.Vector2(screen.get_width() - 100, screen.get_height() - 100)
]


def spawn_wave(wave_num):
    if wave_num not in waves:
        return False

    for enemy_type in waves[wave_num]:
        spawn_pt = random.choice(spawn_points)
        fuzz_x = random.randint(-30, 30)
        fuzz_y = random.randint(-30, 30)

        active_enemies.append(Enemy(enemy_type, spawn_pt.x + fuzz_x, spawn_pt.y + fuzz_y))
    return True

spawn_wave(current_wave)

while running:
    currenttime = time.time()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if len(active_enemies) == 0:
        current_wave += 1
        if not spawn_wave(current_wave):
            running = False

    for bullet in bullets[:]:
        bullet.x += bullet.vel_x
        bullet.y += bullet.vel_y

        if not (0 < bullet.x < screen.get_width() and 0 < bullet.y < screen.get_height()):
            bullets.remove(bullet)
            continue

        bullet_rect = pygame.Rect(bullet.x, bullet.y, bullet_size, bullet_size)
        for enemy in active_enemies[:]:
            enemy_rect = pygame.Rect(enemy.pos.x - (enemy.size / 2), enemy.pos.y - (enemy.size / 2), enemy.size,
                                     enemy.size)

            if bullet_rect.colliderect(enemy_rect):
                enemy.health -= 1
                if bullet in bullets:
                    bullets.remove(bullet)
                if enemy.health <= 0:
                    active_enemies.remove(enemy)
                break

    screen.blit(background_img, (0, 0))

    for enemy in active_enemies:
        enemy.update(player_pos, dt)
        enemy.draw(screen)

    if facingleft:
        screen.blit(player_sprites["left"], (player_pos.x - 75, player_pos.y - 88))
    elif facingright:
        screen.blit(player_sprites["right"], (player_pos.x - 75, player_pos.y - 88))
    elif facingup:
        screen.blit(player_sprites["up"], (player_pos.x - 75, player_pos.y - 88))
    elif facingdown:
        screen.blit(player_sprites["down"], (player_pos.x - 75, player_pos.y - 88))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        facingleft, facingright, facingup, facingdown = False, False, True, False
        player_pos.y -= int(player_speed) * dt
    if keys[pygame.K_s]:
        facingleft, facingright, facingup, facingdown = False, False, False, True
        player_pos.y += int(player_speed) * dt
    if keys[pygame.K_a]:
        facingleft, facingright, facingup, facingdown = True, False, False, False
        player_pos.x -= int(player_speed) * dt
    if keys[pygame.K_d]:
        facingleft, facingright, facingup, facingdown = False, True, False, False
        player_pos.x += int(player_speed) * dt

    if keys[pygame.K_UP]:
        facingleft, facingright, facingup, facingdown = False, False, True, False
        if currenttime - timesinceshot > cooldown:
            timesinceshot = currenttime
            if len(bullets) < 6:
                bullets.append(Projectile(player_pos.x, player_pos.y, bullet_size, bullet_color, 0, -bullet_speed))

    if keys[pygame.K_DOWN]:
        facingleft, facingright, facingup, facingdown = False, False, False, True
        if currenttime - timesinceshot > cooldown:
            timesinceshot = currenttime
            if len(bullets) < 6:
                bullets.append(Projectile(player_pos.x, player_pos.y, bullet_size, bullet_color, 0, bullet_speed))

    if keys[pygame.K_LEFT]:
        facingleft, facingright, facingup, facingdown = True, False, False, False
        if currenttime - timesinceshot > cooldown:
            timesinceshot = currenttime
            if len(bullets) < 6:
                bullets.append(Projectile(player_pos.x, player_pos.y, bullet_size, bullet_color, -bullet_speed, 0))

    if keys[pygame.K_RIGHT]:
        facingleft, facingright, facingup, facingdown = False, True, False, False
        if currenttime - timesinceshot > cooldown:
            timesinceshot = currenttime
            if len(bullets) < 6:
                bullets.append(Projectile(player_pos.x, player_pos.y, bullet_size, bullet_color, bullet_speed, 0))

    for bullet in bullets:
        bullet.draw(screen)

    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()