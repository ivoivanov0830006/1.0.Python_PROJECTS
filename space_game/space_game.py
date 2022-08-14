import pygame
import os

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


def main():
    run = True
    fps = 60

    clock = pygame.time.Clock()

    while run:
        clock.tick(fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # clicking X button will close the game
                run = False


main()
