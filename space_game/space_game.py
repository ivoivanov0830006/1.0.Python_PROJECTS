import pygame  # Import the Pygame library for game development
import os  # Import the os module for operating system functions
import random  # Import the random module for generating random numbers
pygame.font.init()  # Initialize the font module in Pygame

# -------------------- game area -----------------------

width_main, height_main = 750, 650  # Set the dimensions of the game window
win = pygame.display.set_mode((width_main, height_main))  # Create the game window
pygame.display.set_caption("Space Game")  # Set the title of the game window

# -------------------loading images----------------------

# Enemy ships
red_space_ship = pygame.image.load(os.path.join("assets", "enemy_red.png"))  # Load the image for a red enemy
green_space_ship = pygame.image.load(os.path.join("assets", "enemy_green.png"))  # Load the image for a green enemy
yellow_space_ship = pygame.image.load(os.path.join("assets", "enemy_yellow.png"))  # Load the image for a yellow enemy

# Player ship
blue_space_ship = pygame.image.load(os.path.join("assets", "player_blue.png"))  # Load the image for the player's ship

# Lasers
laser_images = {  # Define a dictionary mapping laser colors to their respective image filenames
    "red": "pixel_laser_red.png",
    "green": "pixel_laser_green.png",
    "blue": "pixel_laser_blue.png",
    "yellow": "pixel_laser_yellow.png"
}

# Load laser images for each color using dictionary comprehension
laser_dict = {color: pygame.image.load(os.path.join("assets", filename)) for color, filename in laser_images.items()}

red_laser = laser_dict["red"]  # Load the red laser image
green_laser = laser_dict["green"]  # Load the green laser image
blue_laser = laser_dict["blue"]  # Load the blue laser image
yellow_laser = laser_dict["yellow"]  # Load the yellow laser image

# Background
background = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background.png")),
                                    (width_main, height_main))  # Load and scale the background image

# Buttons

# Load images for play and exit buttons
play_button = pygame.image.load(os.path.join("assets", "play_button_white.png"))
exit_button = pygame.image.load(os.path.join("assets", "exit_button_white.png"))

# Load images for hover state of play and exit buttons
play_button_hover = pygame.image.load(os.path.join("assets", "play_button.png"))
exit_button_hover = pygame.image.load(os.path.join("assets", "exit_button.png"))


class Button:
    def __init__(self, image, hover_image, pos, text_input, font, base_color):
        self.image = image  # Button image
        self.hover_image = hover_image  # Button image for hover state
        self.x_pos = pos[0]  # X-coordinate of button position
        self.y_pos = pos[1]  # Y-coordinate of button position
        self.font = font  # Font for button text
        self.base_color = base_color  # Base color for button text
        self.text_input = text_input  # Text to display on the button
        self.text = self.font.render(self.text_input, True, self.base_color)  # Render the button text
        if self.image is None:
            self.image = self.text  # If image is not provided, use text as the button image
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))  # Get rect for button image
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))  # Get rect for button text

    def update(self, screen, mouse_pos):
        # Update button appearance based on mouse position
        if self.rect.collidepoint(mouse_pos):
            screen.blit(self.hover_image, self.rect)  # Display hover image if mouse is over the button
        else:
            screen.blit(self.image, self.rect)  # Display default image
        screen.blit(self.text, self.text_rect)  # Display button text

    def check_input(self, position):
        # Check if mouse click position is within button bounds
        if position[0] in range(self.rect.left, self.rect.right) and \
                position[1] in range(self.rect.top, self.rect.bottom):
            return True  # Return True if mouse click is within button bounds
        return False  # Return False otherwise


class Laser:
    def __init__(self, x, y, img):
        self.x = x  # X-coordinate of laser position
        self.y = y  # Y-coordinate of laser position
        self.img = img  # Laser image
        self.mask = pygame.mask.from_surface(self.img)  # Create a mask for pixel-perfect collision detection

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))  # Draw the laser on the window

    def move(self, velocity):
        self.y += velocity  # Move the laser vertically by the given velocity

    def off_screen(self, height):
        return not(self.y <= height)  # Check if the laser is off-screen

    def collision(self, obj):
        return collide(self, obj)  # Check for collision between the laser and another object


class Ship:
    COOL_DOWN = 10  # Cool-down period for shooting lasers

    def __init__(self, x, y, health=100):
        self.x = x  # X-coordinate of ship position
        self.y = y  # Y-coordinate of ship position
        self.health = health  # Ship health
        self.ship_img = None  # Ship image
        self.laser_img = None  # Laser image
        self.lasers = []  # List to store lasers fired by the ship
        self.cool_down_counter = 0  # Counter for cool-down period

    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))  # Draw the ship on the window
        for laser in self.lasers:
            laser.draw(window)  # Draw lasers fired by the ship

    def move_lasers(self, velocity, obj):
        self.cool_down()  # Handle cool-down for shooting
        for laser in self.lasers:
            laser.move(velocity)  # Move lasers
            if laser.off_screen(height_main):
                self.lasers.remove(laser)  # Remove lasers that go off-screen
            elif laser.collision(obj):
                obj.health -= 10  # Decrease health of collided object
                self.lasers.remove(laser)  # Remove laser after collision
                if obj.health <= 0:
                    obj.lives -= 1  # Decrease lives of collided object
                    obj.health = 100  # Reset health
                    if obj.lives <= 0:
                        obj.health = 0  # Set health to zero if lives run out

    def cool_down(self):
        if self.cool_down_counter >= self.COOL_DOWN:
            self.cool_down_counter = 0  # Reset cool-down counter
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1  # Increment cool-down counter

    def get_width(self):
        return self.ship_img.get_width()  # Get width of ship image

    def get_height(self):
        return self.ship_img.get_height()  # Get height of ship image


class PlayerShip(Ship):
    def __init__(self, x, y, health=100, lives=2):
        super().__init__(x, y, health)  # Call superclass constructor
        self.ship_img = blue_space_ship  # Set the ship image for the player
        self.laser_img = blue_laser  # Set the laser image for the player
        self.mask = pygame.mask.from_surface(self.ship_img)  # Create a mask for pixel-perfect collision detection
        self.max_health = health  # Maximum health of the player ship
        self.lives = lives  # Number of lives
        self.points = 0  # Player points

    def move_lasers(self, velocity, objs):
        self.cool_down()  # Handle cool-down for shooting
        for laser in self.lasers:
            laser.move(velocity)  # Move lasers
            if laser.off_screen(height_main):
                self.lasers.remove(laser)  # Remove lasers that go off-screen
            else:
                for obj in objs:
                    if laser.collision(obj):
                        if laser in self.lasers:
                            self.lasers.remove(laser)  # Remove laser after collision
                            print("Enemy ship hit!")  # Print a message when enemy ship is hit
                            obj.health -= 20  # Decrease enemy ship's health
                            print(f"Enemy ship's health: {obj.health}")  # Print updated health
                            if obj.health == 0:
                                objs.remove(obj)  # Remove destroyed enemy ship
                                print("Enemy ship destroyed!")  # Print a message when enemy ship is destroyed
                                self.points += 10  # Increase points when an enemy ship is destroyed
                                print(f"Points: {self.points}")  # Print updated points

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x - 15, self.y - 40, self.laser_img)  # Create a new laser object
            self.lasers.append(laser)  # Add the laser to the list of lasers fired by the player
            self.cool_down_counter = 7  # Set cool-down counter

    def draw(self, window):
        super().draw(window)  # Call superclass draw method
        self.health_bar(window)  # Draw health bar for player ship

    def health_bar(self, window):
        pygame.draw.rect(window, (255, 0, 0), (self.x, self.y + self.ship_img.get_height() + 10,
                                               self.ship_img.get_width(), 5))  # Draw red health bar
        pygame.draw.rect(window, (0, 255, 0), (self.x, self.y + self.ship_img.get_height() + 10,
                                               self.ship_img.get_width() * (self.health / self.max_health), 5))
        # Draw green health bar


class EnemyShips(Ship):
    color_map = {
        "red": (red_space_ship, red_laser, 120),  # Map color to ship image, laser image, and initial health
        "yellow": (yellow_space_ship, yellow_laser, 60),
        "green": (green_space_ship, green_laser, 20),
    }

    def __init__(self, x, y, color, health=None):
        super().__init__(x, y, health)  # Call superclass constructor
        self.ship_img, self.laser_img, self.health = self.color_map[color]  # Set ship image, laser image, and health
        self.mask = pygame.mask.from_surface(self.ship_img)  # Create a mask for pixel-perfect collision detection

    def move(self, velocity):
        self.y += velocity  # Move the enemy ship vertically

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x - 25, self.y + 25, self.laser_img)  # Create a new laser object
            self.lasers.append(laser)  # Add the laser to the list of lasers fired by the enemy
            self.cool_down_counter = 1  # Set cool-down counter


# -----------------------------------------------------------------------------------------------------------
def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x  # Calculate offset in x direction
    offset_y = obj2.y - obj1.y  # Calculate offset in y direction
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y))  # Check for collision between two objects
# -----------------------------------------------------------------------------------------------------------


def play():
    # Function to start the game
    run = True  # Flag to control the game loop
    fps = 90  # Frames per second
    wave = 0  # Starting wave

    play_font = pygame.font.SysFont("calibri", 50)  # Font for in-game text
    lost_font = pygame.font.SysFont("calibri", 70)  # Font for "Game Over" text

    enemies = []  # List to store enemy ships
    wave_length = 5  # Initial number of enemy ships
    enemy_velocity = 5  # Velocity of enemy ships
    player_velocity = 25  # Velocity of player ship
    enemy_laser_velocity = 15  # Velocity of enemy lasers
    laser_velocity = 35  # Velocity of player lasers

    player = PlayerShip(600, 500)  # Create player ship

    clock = pygame.time.Clock()  # Clock object to control frame rate

    lost = False  # Flag to indicate if the player has lost
    lost_count = 0  # Counter for displaying "Game Over" text

    background_y = 0  # Initial background position
    background_scroll_speed = 1  # Speed of background scrolling

    def redraw_window():
        # Function to redraw the game window
        win.blit(background, (0, background_y))  # Draw the background with scrolling effect
        win.blit(background, (0, background_y - background.get_height()))
        lives_label = play_font.render(f"Lives: {player.lives}", True, (255, 255, 255))  # Draw lives label
        wave_label = play_font.render(f"Wave: {wave}", True, (255, 255, 255))  # Draw wave label
        points_label = play_font.render(f"Points: {player.points}", True, (255, 255, 255))  # Draw points label

        win.blit(lives_label, (10, 10))  # Display lives label
        win.blit(wave_label, (width_main - wave_label.get_width() - 10, 10))  # Display wave label
        win.blit(points_label, (width_main / 2 - points_label.get_width() / 2, 10))  # Display points label

        for every_enemy in enemies:
            every_enemy.draw(win)  # Draw each enemy ship

        if player.lives > 0:
            player.draw(win)  # Draw player ship

        if lost:
            lost_label = lost_font.render("GAME OVER!", True, (255, 255, 255))  # Draw "Game Over" text
            win.blit(lost_label, (width_main / 2 - lost_label.get_width() / 2, 350))  # Display "Game Over" text

        pygame.display.update()  # Update the display

    while run:
        clock.tick(fps)  # Limit frame rate
        redraw_window()  # Redraw the game window

        # Background scrolling
        background_y += background_scroll_speed
        if background_y >= background.get_height():
            background_y = 0

        if player.lives <= 0:
            lost = True  # Set lost flag if player has no lives left
            lost_count += 1  # Increment lost counter

        if lost:
            if lost_count > fps * 2:  # Display "Game Over" text for 2 seconds
                run = False  # End the game loop
            else:
                continue  # Skip the rest of the loop if the game is lost

        if len(enemies) == 0:  # Check if all enemies are destroyed
            wave += 1  # Increment level
            wave_length += 2  # Increase wave length
            for i in range(wave_length):
                # Spawn new enemies
                enemy = EnemyShips(random.randrange(50, width_main - 100), random.randrange(-1500, -100),
                                   random.choice(["red", "yellow", "green"]))  # Randomly select enemy color
                enemies.append(enemy)  # Add enemy to the list

        for event in pygame.event.get():  # Event handling loop
            if event.type == pygame.QUIT:  # Check if the user wants to quit
                quit()  # Quit the game

# ----------------------------------------------key binds--------------------------------------------------------
        keys = pygame.key.get_pressed()  # Get currently pressed keys
        if keys[pygame.K_LEFT] and player.x - player_velocity > 0 - player.get_width()/2:
            player.x -= player_velocity / 2  # Move left
        if keys[pygame.K_RIGHT] and player.x + player_velocity < width_main - player.get_width()/2:
            player.x += player_velocity / 2  # Move right
        if keys[pygame.K_UP] and player.y - player_velocity > 0:
            player.y -= player_velocity / 2  # Move up
        if keys[pygame.K_DOWN] and player.y + player_velocity < height_main - player.get_height() - 15:
            player.y += player_velocity / 2  # Move down
        if keys[pygame.K_SPACE]:
            player.shoot()  # Shoot laser
# ------------------------------------------------------------------------------------------------------------------
        # Iterate over enemies
        for enemy in enemies:
            enemy.move(enemy_velocity)  # Move enemy ship
            enemy.move_lasers(enemy_laser_velocity, player)  # Move enemy lasers

            # Enemy shooting logic
            if random.randrange(0, 2 * 60) == 1:
                enemy.shoot()  # Enemy ship fires laser

            # Check collisions between enemy lasers and player
            for laser in enemy.lasers:
                if laser.collision(player):
                    player.health -= 10  # Decrease player health
                    enemy.lasers.remove(laser)  # Remove enemy laser
                    if player.health <= 0:
                        player.lives -= 1  # Decrease player lives
                        player.health = 100  # Reset player health
                        if player.lives <= 0:
                            player.health = 0  # Set player health to zero if lives run out
                            lost = True  # Set lost flag

                # Check collisions between player lasers and enemy lasers
                for player_laser in player.lasers[:]:
                    if laser.collision(player_laser):
                        player.lasers.remove(player_laser)  # Remove player laser
                        enemy.lasers.remove(laser)  # Remove enemy laser
                        break  # Break the loop after destroying the enemy laser

            # Check collisions between enemy and player
            if collide(enemy, player):
                player.health -= 10  # Decrease player health
                player.points += 10  # Increase player points
                enemies.remove(enemy)  # Remove enemy ship
                if player.health <= 0:
                    player.lives -= 1  # Decrease player lives
                    player.health = 100  # Reset player health
                    if player.lives <= 0:
                        player.health = 0  # Set player health to zero if lives run out
                        lost = True  # Set lost flag

                player.draw(win)  # Update health bar

            elif enemy.y + enemy.get_height() > height_main:
                enemies.remove(enemy)  # Remove enemy ship if it goes off-screen

        player.move_lasers(-laser_velocity, enemies)  # Move player lasers and check for collisions with enemies

# -------------------------------------------- main menu ------------------------------------------------------------


def main_menu():
    # Function to display the main menu
    title_font = pygame.font.SysFont("Calibri", 80)  # Font for title
    other_text_font = pygame.font.SysFont("Calibri", 60)  # Font for other text
    run = True  # Flag to control the main menu loop
    while run:
        win.blit(background, (0, 0))  # Display background
        menu_mouse_pos = pygame.mouse.get_pos()  # Get mouse position

        title_label = title_font.render("SPACE RUNNER", True, (231, 231, 231))  # Render title text
        win.blit(title_label, (width_main / 2 - title_label.get_width() / 2, 50))  # Display title text

        play_but = Button(play_button, play_button_hover,
                          pos=(250, 270), text_input=" ", font=title_font, base_color="White")
        play_label = other_text_font.render("PLAY", True, (231, 231, 231))
        win.blit(play_label, (350, 250))

        quit_but = Button(exit_button, exit_button_hover,
                          pos=(250, 480), text_input=" ", font=title_font, base_color="White")
        play_label = other_text_font.render("QUIT", True, (231, 231, 231))
        win.blit(play_label, (350, 460))

        for button in [play_but, quit_but]:
            button.update(win, menu_mouse_pos)  # Update button appearance

        pygame.display.update()  # Update the display

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_but.check_input(menu_mouse_pos):
                    play()  # Start the game if "Play" button is clicked
                if quit_but.check_input(menu_mouse_pos):
                    pygame.quit()
                    run = False


main_menu()  # Display the main menu
