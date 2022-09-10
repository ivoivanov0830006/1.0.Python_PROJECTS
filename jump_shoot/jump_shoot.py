import pygame
pygame.init()

screen_width = 500
screen_height = 500
win = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("Jump'n'Shoot")

x = 50
y = 400
player_width = 40
player_height = 60
velocity = 15

run = True
while run:
    pygame.time.delay(50)   # miliseconds

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and x > 0:
        x -= velocity
    if keys[pygame.K_RIGHT] and x < screen_width - player_width:
        x += velocity
    if keys[pygame.K_UP] and y > 0:
        y -= velocity
    if keys[pygame.K_DOWN] and y < screen_height - player_height:
        y += velocity

    win.fill((0, 0, 0))
    pygame.draw.rect(win, (255, 0, 0), (x, y, player_width, player_height))
    pygame.display.update()

pygame.quit()

