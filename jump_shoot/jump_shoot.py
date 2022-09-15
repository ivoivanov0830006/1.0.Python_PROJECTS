import pygame
pygame.init()

screen_width = 500
screen_height = 480
win = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("Jump'n'Shoot")

walk_right = [pygame.image.load('player_R1.png'),
              pygame.image.load('player_R2.png'),
              pygame.image.load('player_R3.png'),
              pygame.image.load('player_R4.png'),
              pygame.image.load('player_R5.png'),
              pygame.image.load('player_R6.png'),
              pygame.image.load('player_R7.png'),
              pygame.image.load('player_R8.png'),
              pygame.image.load('player_R9.png')]
walk_left = [pygame.image.load('player_L1.png'),
             pygame.image.load('player_L2.png'),
             pygame.image.load('player_L3.png'),
             pygame.image.load('player_L4.png'),
             pygame.image.load('player_L5.png'),
             pygame.image.load('player_L6.png'),
             pygame.image.load('player_L7.png'),
             pygame.image.load('player_L8.png'),
             pygame.image.load('player_L9.png')]
bg = pygame.image.load('background.png')
char = pygame.image.load('player_0.png')

clock = pygame.time.Clock()


class Player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.velocity = 5
        self.is_jump = False
        self.jump_count = 10
        self.left = False
        self.right = False
        self.walk_count = 0

    def draw(self, win):
        if self.walk_count + 1 >= 27:
            self.walk_count = 0

        if left:
            win.blit(walk_left[self.walk_count // 3], (self.x, self.y))
            self.walk_count += 1
        elif right:
            win.blit(walk_right[self.walk_count // 3], (self.x, self.y))
            self.walk_count += 1
        else:
            win.blit(char, (self.x, self.y))


def redraw_game_window():
    win.blit(bg, (0, 0))
    man.draw(win)
    pygame.display.update()


man = Player(300, 420, 64, 64)
run = True
while run:
    clock.tick(27)   # milliseconds

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and man.x > man.velocity:
        man.x -= man.velocity
        left = True
        right = False
    elif keys[pygame.K_RIGHT] and man.x < screen_width - man.width - man.velocity:
        man.x += man.velocity
        right = True
        left = False
    else:
        right = False
        left = False
        walk_count = 0

    if not man.is_jump:
        if keys[pygame.K_SPACE]:
            man.is_jump = True
            man.right = False
            man.left = False
            man.walk_count = 0
    else:
        if man.jump_count >= -10:
            negative = 1
            if man.jump_count < 0:
                negative = - 1
            man.y -= (man.jump_count ** 2) * 0.5 * negative
            man.jump_count -= 1
        else:
            man.is_jump = False
            man.jump_count = 10

    redraw_game_window()

pygame.quit()
