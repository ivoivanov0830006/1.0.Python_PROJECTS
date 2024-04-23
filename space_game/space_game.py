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
background = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background-black.png")), (width_main,
                                                                                                        height_main))


# ----------------------------------------Adding Lasers----------------------------------------------------
class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, velocity):
        self.y += velocity

    def off_screen(self, height):
        return not(self.y <= height)       # and self.y >= 0)

    def collision(self, obj):
        return collide(self, obj)
# ---------------------------------------------------------------------------------------------------------


class Ship:
    COOLDOWN = 10     # it means 1/6 sec, because fps = 60

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
        for laser in self.lasers:
            laser.draw(window)

    def move_lasers(self, velocity, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(velocity)
            if laser.off_screen(height_main):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)

    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()


# ----------------------------------------------Player Ship--------------------------------------------------
class PlayerShip(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)     # deinitialization method
        self.ship_img = yellow_space_ship
        self.laser_img = yellow_laser
        self.mask = pygame.mask.from_surface(self.ship_img)  # to describe is there any collision with our object
        self.max_health = health

    def move_lasers(self, velocity, objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(velocity)
            if laser.off_screen(height_main):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        if laser in self.lasers:
                            self.lasers.remove(laser)

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x - 15, self.y - 40, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

    def draw(self, window):
        super().draw(window)
        self.health_bar(window)

    def health_bar(self, window):
        pygame.draw.rect(window, (255, 0, 0), (self.x, self.y + self.ship_img.get_height() + 10,
                                               self.ship_img.get_width(), 5))
        pygame.draw.rect(window, (0, 255, 0), (self.x, self.y + self.ship_img.get_height() + 10,
                                               self.ship_img.get_width() * (self.health / self.max_health), 5))


# ----------------------------------------------Enemy Ship--------------------------------------------------
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

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x - 25, self.y + 25, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1


def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y))
# -----------------------------------------------------------------------------------------------------------

# -----------------------------------------------------------------------------------------------------------


def play():
    run = True
    fps = 60
    level = 0

    play_font = pygame.font.SysFont("calibri", 50)
    lost_font = pygame.font.SysFont("calibri", 70)

    enemies = []
    wave_length = 5
    enemy_velocity = 2
    player_velocity = 12
    enemy_laser_velocity = 5
    laser_velocity = 15

    player = PlayerShip(600, 500)

    clock = pygame.time.Clock()  # clock speed , see in while loop

    lost = False
    lost_count = 0

    def redraw_window():
        win.blit(background, (0, 0))     # blit draws the background on coordinates 0, 0 (top left corner)
        lives_label = play_font.render(f"Lives: {player.lives}", True, (255, 255, 255))     # draw text
        level_label = play_font.render(f"Level: {level}", True, (255, 255, 255))
        points_label = play_font.render(f"Points: {player.points}", True, (255, 255, 255))  # Draw points label

        win.blit(lives_label, (10, 10))
        win.blit(level_label, (width_main - level_label.get_width() - 10, 10))
        win.blit(points_label, (width_main / 2 - points_label.get_width() / 2, 10))

        for every_enemy in enemies:
            every_enemy.draw(win)

        if player.lives > 0:
            player.draw(win)

        if lost:
            lost_label = lost_font.render("GAME OVER!", True, (255, 255, 255))
            win.blit(lost_label, (width_main / 2 - lost_label.get_width() / 2, 350))

        pygame.display.update()     # refresh display

    while run:
        clock.tick(fps)   # clock speed is based on FPS and that's why the game will run on every computer the same way
        redraw_window()

        if player.lives <= 0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > fps * 2:     # if we pass 3 sec timer,
                run = False              # quit the game
            else:
                continue                # go back to beginning of the loop without doing anything BELOW ! ! !

        if len(enemies) == 0:
            level += 1
            wave_length += 2
            for i in range(wave_length):
                enemy = EnemyShips(random.randrange(50, width_main - 100), random.randrange(-1500, -100), random.
                                   choice(["red", "blue", "green"]))
                enemies.append(enemy)

        for event in pygame.event.get():  # on every 60 sec if event occur -> do something
            if event.type == pygame.QUIT:  # clicking X button will close the game
                quit()      # if want to get us in main menu again it:     run = False

# ----------------------------------------------key binds--------------------------------------------------------
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - player_velocity > 0 - player.get_width()/2:  # move left + limit on left
            player.x -= player_velocity
        if keys[pygame.K_RIGHT] and player.x + player_velocity < width_main - player.get_width()/2:  # move right+limit
            player.x += player_velocity
        if keys[pygame.K_UP] and player.y - player_velocity > 0:         # move up + limit on up side
            player.y -= player_velocity
        if keys[pygame.K_DOWN] and player.y + player_velocity < height_main - player.get_height() - 15:
            player.y += player_velocity
        if keys[pygame.K_SPACE]:
            player.shoot()
# ------------------------------------------------------------------------------------------------------------------
        # Iterate over enemies
        for enemy in enemies:
            enemy.move(enemy_velocity)
            enemy.move_lasers(enemy_laser_velocity, player)  # Move enemy lasers

            # Enemy shooting logic
            if random.randrange(0, 2 * 60) == 1:
                enemy.shoot()

            # Check collisions between enemy lasers and player
            for laser in enemy.lasers:
                if laser.collision(player):
                    player.health -= 10
                    enemy.lasers.remove(laser)
                    if player.health <= 0:
                        player.lives -= 1
                        player.health = 100
                        if player.lives <= 0:
                            player.health = 0
                            lost = True  # Set lost flag to end the game

                # Check collisions between player lasers and enemy lasers
                for player_laser in player.lasers[:]:
                    if laser.collision(player_laser):
                        player.lasers.remove(player_laser)
                        enemy.lasers.remove(laser)
                        break  # Break the inner loop after destroying the enemy laser

            # Check collisions between enemy and player
            if collide(enemy, player):
                player.health -= 10
                player.points += 10
                enemies.remove(enemy)
                if player.health <= 0:
                    player.lives -= 1
                    player.health = 100
                    if player.lives <= 0:
                        player.health = 0
                        lost = True  # Set lost flag to end the game

                player.draw(win)  # Update health bar

            elif enemy.y + enemy.get_height() > height_main:
                enemies.remove(enemy)  # Add the enemy to the removal list

        player.move_lasers(-laser_velocity, enemies)  # checks if laser collides with enemies and - because of direction

# -------------------------------------------- main menu ------------------------------------------------------------


def main_menu():
    title_font = pygame.font.SysFont("verdana", 80)
    other_text_font = pygame.font.SysFont("calibri", 60)
    run = True
    while run:
        win.blit(background, (0, 0))
        menu_mouse_pos = pygame.mouse.get_pos()

        title_label = title_font.render("MAIN MENU", True, (231, 231, 231))
        win.blit(title_label, (width_main / 2 - title_label.get_width() / 2, 50))

        play_but = Button(play_button, play_button_hover, pos=(250, 270), text_input=" ", font=title_font, base_color="White")
        play_label = other_text_font.render("PLAY", True, (231, 231, 231))
        win.blit(play_label, (350, 250))

        quit_but = Button(exit_button, exit_button_hover, pos=(250, 480), text_input=" ", font=title_font, base_color="White")
        play_label = other_text_font.render("QUIT", True, (231, 231, 231))
        win.blit(play_label, (350, 460))

        for button in [play_but, quit_but]:
            button.update(win, menu_mouse_pos)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_but.check_input(menu_mouse_pos):
                    play()
                if quit_but.check_input(menu_mouse_pos):
                    pygame.quit()
                    run = False


main_menu()


