# -*- coding: utf-8 -*-
import sys
import pygame
import random
from scripts import pyganim


# define some functions
def loadImages():
    imagesAndDurations = [('./images/vita/right_stand.%s.png' % (
        str(num).rjust(3, '0')), 0.1) for num in range(4)]
    animObjs['vita_right_stand'] = pyganim.PygAnimation(imagesAndDurations)

    animObjs['vita_left_stand'] = animObjs['vita_right_stand'].getCopy()
    animObjs['vita_left_stand'].flip(True, False)
    animObjs['vita_left_stand'].makeTransformsPermanent()

    imagesAndDurations = [('./images/vita/right_walk.%s.png' % (
        str(num).rjust(3, '0')), 0.1) for num in range(6)]
    animObjs['vita_right_walk'] = pyganim.PygAnimation(imagesAndDurations)

    animObjs['vita_left_walk'] = animObjs['vita_right_walk'].getCopy()
    animObjs['vita_left_walk'].flip(True, False)
    animObjs['vita_left_walk'].makeTransformsPermanent()

    imagesAndDurations = [('./images/vita/right_damage.%s.png' % (
        str(num).rjust(3, '0')), 0.1) for num in range(4)]
    animObjs['vita_right_damage'] = pyganim.PygAnimation(imagesAndDurations)

    animObjs['vita_left_damage'] = animObjs['vita_right_damage'].getCopy()
    animObjs['vita_left_damage'].flip(True, False)
    animObjs['vita_left_damage'].makeTransformsPermanent()

    imagesAndDurations = [('./images/vita/right_run.%s.png' % (
        str(num).rjust(3, '0')), 0.1) for num in range(6)]
    animObjs['vita_right_run'] = pyganim.PygAnimation(imagesAndDurations)

    animObjs['vita_left_run'] = animObjs['vita_right_run'].getCopy()
    animObjs['vita_left_run'].flip(True, False)
    animObjs['vita_left_run'].makeTransformsPermanent()


pygame.init()

# define some constants
LEFT = 'left'
RIGHT = 'right'

# set up the window
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
pygame.display.set_caption('Dibrino Alpha')

# set player size
playerWidth = 76
playerHeight = 96

# creating the PygAnimation objects for player actions
animObjs = {}
# loading all game images, including PygAnimation files
loadImages()
fireball = pygame.image.load('./images/fireball.png')

moveConductor = pyganim.PygConductor(animObjs)

direction = LEFT  # player starts off facing left

bg_color = (128, 255, 0)

mainClock = pygame.time.Clock()
x = 270  # x and y are the player's position
y = 370

x_fireball = 0
y_fireball = 416

WALK_RATE = 6
RUN_RATE = 10
FALL_RATE = 6

mortes = 0

sys_font = pygame.font.SysFont("None", 60)


# se YFireball > 400 gera novo random e seta o Y pra 0

running = moveLeft = moveRight = False

over = False

while True:
    # main game loop
    while not over:
        windowSurface.fill(bg_color)
        for event in pygame.event.get():  # event handling loop
            # handle ending the program
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_LSHIFT, pygame.K_RSHIFT):
                    running = True

                elif event.key == pygame.K_LEFT:
                    moveLeft = True
                    moveRight = False

                    direction = LEFT

                elif event.key == pygame.K_RIGHT:
                    moveRight = True
                    moveLeft = False

                    direction = RIGHT

            elif event.type == pygame.KEYUP:
                if event.key in (pygame.K_LSHIFT, pygame.K_RSHIFT):
                    running = False

                elif event.key == pygame.K_LEFT:
                    moveLeft = False

                elif event.key == pygame.K_RIGHT:
                    moveRight = False

        if moveLeft or moveRight:
            # draw the correct walking/running sprite from the animation object
            if running:
                rate = RUN_RATE
                playerWidth = 96

                if direction == LEFT:
                    animObjs['vita_left_run'].blit(windowSurface, (x, y))
                elif direction == RIGHT:
                    animObjs['vita_right_run'].blit(windowSurface, (x, y))
            else:
                # walking
                rate = WALK_RATE
                playerWidth = 76

                if direction == LEFT:
                    animObjs['vita_left_walk'].blit(windowSurface, (x, y))
                elif direction == RIGHT:
                    animObjs['vita_right_walk'].blit(windowSurface, (x, y))

            if moveLeft:
                x -= rate
            if moveRight:
                x += rate
        else:
            # standing still
            moveConductor.play()
            if direction == LEFT:
                animObjs['vita_left_stand'].blit(windowSurface, (x, y))

            elif direction == RIGHT:
                animObjs['vita_right_stand'].blit(windowSurface, (x, y))

        if y_fireball > 415:
            x_fireball = random.randrange(0, 640, 32)
            y_fireball = 0

        y_fireball += FALL_RATE
        windowSurface.blit(fireball, (x_fireball, y_fireball))

        # make sure the player does move off the screen
        if x < 0 - (96 - playerWidth):
            x = 0 - (96 - playerWidth)
        if x > WINDOWWIDTH - playerWidth:
            x = WINDOWWIDTH - playerWidth
        if y < 0:
            y = 0
        if y > WINDOWHEIGHT - playerHeight:
            y = WINDOWHEIGHT - playerHeight

        if x_fireball < (x + 76) and (x_fireball + 32) > x:
            if y_fireball > 350:
                over = True

        pygame.display.update()
        mainClock.tick(24)  # Feel free to experiment with any FPS setting

    while over:
        windowSurface.fill(bg_color)
        for event in pygame.event.get():  # event handling loop
            # handle ending the program
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                over = False

        mortes_rendered = sys_font.render("GAME OVER", 0, (255, 255, 255))
        windowSurface.blit(mortes_rendered, (200, 200))

        y_fireball = 416
        x = 270  # x and y are the player's position
        y = 370

        running = moveLeft = moveRight = False

        pygame.display.update()
        mainClock.tick(24)  # Feel free to experiment with any FPS setting