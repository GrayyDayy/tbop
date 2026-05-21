import pygame
from Projectiles import Projectile
import time
import json
import random
from trivia import get_trivia_question

with open("config.json") as file:
    config = json.load(file)

with open("enemies.json") as file:
    enemy_config = json.load(file)

player_health = config["player_health"]
player_speed = config["player_speed"]
bullet_speed = config["bullet_speed"]
bullet_size = config["bullet_size"]
bullet_color = config["bullet_color"]
player_damage = config["player_damage"]
cooldown = config["cooldown"]

pygame.init()
screen = pygame.display.set_mode()
clock = pygame.time.Clock()
running = True
dt = 0
bullets = []
timesinceshot = 0
timesincehit = 0
trivia_active = False
trivia_data = {}
selected_answer = 0
trivia_done = False
wave_transition = False

health_bar_width = 200
health_bar_height = 20
maxhp = player_health

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
        surface.blit(self.image, (int(self.pos.x - 230), int(self.pos.y - 144)))

waves = {
    1: ["elbooger"],
    2: ["elbooger", "elbooger"],
    3: ["elbooger", "elwebo"],
    4: ["elwebo", "hexemo"],
    5: ["sabubble"],
    6: ["eyeloco"],
    7: ["eyeloco", "hexemo"],
    8: ["squarely", "squarely", "squarely"],
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


def draw_health_bar(surface, x, y, current_health, max_health):
    if current_health < 0:
        current_health = 0
    health_ratio = current_health / max_health
    fill_width = int(health_bar_width * health_ratio)
    background_rect = pygame.Rect(x, y, health_bar_width, health_bar_height)
    foreground_rect = pygame.Rect(x, y, fill_width, health_bar_height)
    pygame.draw.rect(surface, (200, 0, 0), background_rect)
    pygame.draw.rect(surface, (0, 200, 0), foreground_rect)

spawn_wave(current_wave)

while running:
    currenttime = time.time()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if trivia_active and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                selected_answer = (
                                          selected_answer - 1
                                  ) % len(trivia_data["options"])
            if event.key == pygame.K_DOWN:
                selected_answer = (
                                          selected_answer + 1
                                  ) % len(trivia_data["options"])
            if event.key == pygame.K_RETURN:
                chosen = trivia_data["options"][selected_answer]
                if chosen == trivia_data["correct"]:
                    rand = random.randint(1,3)
                    print("Correct!")
                    if rand == 1:
                        player_health += 2
                    elif rand == 2:
                        player_speed += 100
                    elif rand == 3:
                        player_damage += 2
                else:
                    print("Wrong!")
                    player_health -= 2
                trivia_active = False
                trivia_done = True
                spawn_wave(current_wave)
                wave_transition = False
    if trivia_active:
        screen.fill((15, 15, 15))
        title_font = pygame.font.SysFont(None, 60)
        answer_font = pygame.font.SysFont(None, 40)
        title = title_font.render(
            "TRIVIA CHALLENGE",
            True,
            (255, 255, 0)
        )
        screen.blit(title, (100, 80))
        question = answer_font.render(
            trivia_data["question"],
            True,
            (255, 255, 255)
        )
        screen.blit(question, (100, 200))
        for i, option in enumerate(trivia_data["options"]):
            color = (
                (0, 255, 0)
                if i == selected_answer
                else (255, 255, 255)
            )
            text = answer_font.render(
                option,
                True,
                color
            )
            screen.blit(text, (120, 300 + i * 60))
        pygame.display.flip()
        continue

    if len(active_enemies) == 0 and not wave_transition:
        wave_transition = True
        current_wave += 1
        if current_wave == 6 and not trivia_done:
            trivia_data = get_trivia_question()
            if trivia_data:
                trivia_active = True
        else:
            if spawn_wave(current_wave):
                wave_transition = False
            else:
                running = False
                print("You Win!")

    if player_health <= 0:
        running = False
        print("You Died!")

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

    for enemy in active_enemies[:]:
        player_rect = pygame.Rect(player_pos.x - 75, player_pos.y - 88, 150, 176)
        enemy_rect = pygame.Rect(enemy.pos.x - (enemy.size / 2), enemy.pos.y - (enemy.size / 2), enemy.size,
                             enemy.size)
        if player_rect.colliderect(enemy_rect):
            if currenttime - timesincehit > 1:
                player_health -= player_damage
                timesincehit = currenttime

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

    draw_health_bar(screen, 20, 20, player_health, maxhp)

    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()