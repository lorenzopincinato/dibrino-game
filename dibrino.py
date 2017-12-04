# -*- coding: utf-8 -*-
import sys
import pygame
import random
import pyganim


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

    imagesAndDurations = [('./images/fireball/down_fall.%s.png' % (
        str(num).rjust(3, '0')), 0.15) for num in range(3)]
    animObjs['fireball_down_fall'] = pyganim.PygAnimation(imagesAndDurations)


class Fireball():
    def __init__(self):
        if random.randrange(0, 75, 1) == 1:
            self.x = random.randrange(0, 640, 32)
            self.y = 0

            self.spawned = True
        else:
            self.spawned = False

    def fall(self, fall_rate):
        if self.y > 415:
            self.spawned = False
            return 1

        self.y += fall_rate
        return 0

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getSpawned(self):
        return self.spawned


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
FALL_RATE = 10

score = 0

sys_font = pygame.font.SysFont("None", 60)

running = moveLeft = moveRight = False

over = False

fireballs = [Fireball() for i in range(10)]

for fireball in fireballs:
    fireball.__init__()

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

        # for fireball in fireballs:
        for fireball in fireballs:
            if not fireball.getSpawned():
                fireball.__init__()

            else:
                score += fireball.fall(FALL_RATE)
                animObjs['fireball_down_fall'].blit(windowSurface, (
                    fireball.getX(), fireball.getY()))

                if fireball.getX() < (x + 62) and (fireball.getX() + 20) > x:
                    if fireball.getY() > 350:
                        over = True

        # make sure the player does move off the screen
        if x < 0 - (96 - playerWidth):
            x = 0 - (96 - playerWidth)
        if x > WINDOWWIDTH - playerWidth:
            x = WINDOWWIDTH - playerWidth
        if y < 0:
            y = 0
        if y > WINDOWHEIGHT - playerHeight:
            y = WINDOWHEIGHT - playerHeight

        FALL_RATE = 10 + score // 10

        score_rendered = sys_font.render(str(score), 0, (255, 255, 255))
        windowSurface.blit(score_rendered, (20, 20))

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
                if event.key == pygame.K_SPACE:
                    over = False
                    score = 0

        game_over = sys_font.render("GAME OVER", 0, (255, 255, 255))
        windowSurface.blit(game_over, (200, 200))

        final_score = sys_font.render(str(score), 0, (255, 255, 255))
        windowSurface.blit(final_score, (310, 300))

        for fireball in fireballs:
            fireball.spawned = False
        x = 270  # x and y are the player's position
        y = 370

        running = moveLeft = moveRight = False

        pygame.display.update()
        mainClock.tick(24)  # Feel free to experiment with any FPS setting

# https://ansimuz.itch.io/magic-cliffs-environment/download/eyJleHBpcmVzIjoxNTExNzc5NjAyLCJpZCI6NjQ4Mjh9.gUCycjafYUVjsTu8Ze96gBCN2SM%3d
