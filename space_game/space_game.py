import pygame
import os
import random

pygame.font.init()

width_main, height_main = 750, 650
win = pygame.display.set_mode((width_main, height_main))
pygame.display.set_caption("Space Game Tutorial")

# -------------------loading images----------------------

# Enemy ships
red_space_ship = pygame.image.load(os.path.join("assets", "pixel_ship_red_small.png"))
green_space_ship = pygame.image.load(os.path.join("assets", "pixel_ship_green_small.png"))
blue_space_ship = pygame.image.load(os.path.join("assets", "pixel_ship_blue_small.png"))

# Player ship
yellow_space_ship = pygame.image.load(os.path.join("assets", "pixel_ship_yellow.png"))

# Lasers
red_laser = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))
green_laser = pygame.image.load(os.path.join("assets", "pixel_laser_green.png"))
blue_laser = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))
yellow_laser = pygame.image.load(os.path.join("assets", "pixel_laser_yellow.png"))

# Background
background = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background-black.png")),
                                    (width_main, height_main))


class Ship:
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0

    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()


# ----------------------------------------------Player Ship--------------------------------------------------------
class PlayerShip(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)     # deinitialization method
        self.ship_img = yellow_space_ship
        self.laser_img = yellow_laser
        self.mask = pygame.mask.from_surface(self.ship_img)  # to describe is there any collision with our object
        self.max_health = health


# ----------------------------------------------Enemy Ships--------------------------------------------------------
class EnemyShips(Ship):
    color_map = {
                "red": (red_space_ship, red_laser),
                "green": (green_space_ship, green_laser),
                "blue": (blue_space_ship, blue_laser)
                }

    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.color_map[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, velocity):
        self.y += velocity


def main():
    run = True
    fps = 60
    level = 0
    lives = 5
    play_font = pygame.font.SysFont("calibri", 50)

    enemies = []
    wave_length = 5       # enemies count at current wave
    enemy_velocity = 3
    player_velocity = 12

    player = PlayerShip(300, 500)

    clock = pygame.time.Clock()

    def redraw_window():
        win.blit(background, (0, 0))     # blit draws the background on coordinates 0, 0 (top left corner)
        lives_label = play_font.render(f"Lives: {lives}", True, (255, 255, 255))  # draw text
        level_label = play_font.render(f"Level: {level}", True, (255, 255, 255))

        win.blit(lives_label, (10, 10))
        win.blit(level_label, (width_main - level_label.get_width() - 10, 10))

        for every_enemy in enemies:   # we put it before player ship, because of overlapping
            every_enemy.draw(win)

        player.draw(win)

        pygame.display.update()

    while run:
        clock.tick(fps)

        if len(enemies) == 0:
            level += 1
            wave_length += 5          # add 5 more enemies
            for i in range(wave_length):
                enemy = EnemyShips(random.randrange(50, width_main-100), random.randrange(-1500, - 100),
                                   random.choice(["red", "blue", "green"]))
                enemies.append(enemy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # clicking X button will close the game
                run = False

# ----------------------------------------------key binds--------------------------------------------------------
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - player_velocity > 0 - player.get_width()/2:  # move left + limit on left
            player.x -= player_velocity
        if keys[pygame.K_RIGHT] and player.x + player_velocity < width_main - player.get_width()/2:  # move right+limit
            player.x += player_velocity
        if keys[pygame.K_UP] and player.y - player_velocity > 0:         # move up + limit on up side
            player.y -= player_velocity
        if keys[pygame.K_DOWN] and player.y + player_velocity < height_main - player.get_height():  # move down + limit
            player.y += player_velocity

        for enemy in enemies[:]:    # made copy of list, so while we are looping there will be no issues
            enemy.move(enemy_velocity)
            if enemy.y + enemy.get_height() > height_main:
                lives -= 1
                enemies.remove(enemy)

        redraw_window()


main()

