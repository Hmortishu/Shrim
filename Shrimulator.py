"""
    Project developed by Pedro Rôlo, started on 08/2016, and still developing.
    Project developed in Python 3, using the randomPyGame module
    Version 1.0
    This project aims to analize basic shrimp activity and help me cultivate my skills as a programmer.
    I hope to eventually implement some kind of AI.

    You can contact me at Hmortishu@gmail.com
"""

import pygame
import random
from math import hypot


pygame.init()  #
#   Window width
displayWidth = 800
#   Window height
displayHeight = 600
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)

gameDisplay = pygame.display.set_mode((displayWidth, displayHeight))
#   program name
pygame.display.set_caption('Shrim')
#   Clock object, witch allows us to track an amount of time
clock = pygame.time.Clock()


#  this function shall create a shtimp at a ramdom location and return that location
def createShrimp():
    x = random.randrange(20, 780)
    y = random.randrange(20, 580)
    pygame.draw.circle(gameDisplay, red, (x, y), 5)

    return [[x, y], 5]

#  this function shall create a food patch at a ramdom location and return that location
def createFood():
    x = random.randrange(20, 780)
    y = random.randrange(20, 580)
    r = random.randrange(3, 8)
    pygame.draw.circle(gameDisplay, green, (x, y), r)

    return [[x, y], r]

'''
def textObjects(text, font):
    textsurface = font.render(text, True, black)
    return textsurface, textsurface.get_rect()


def counter(pontos):
    largeText = pygame.font.Font('freesansbold.ttf', 15)
    textSurf, textRect = textObjects(pontos, largeText)
    textRect.center = (30, 15)
    gameDisplay.blit(textSurf, textRect)
    pygame.display.update()
'''


#   this function find the nearest food patch to a shrimp(princ) and
#   return how much this shrimp should move in a X an Y plane
def tracking(princ, dataFood):
    posX = princ[0]
    posY = princ[1]
    comida = []

    for z in range(0, len(dataFood)):
        X = dataFood[z][0][0]
        Y = dataFood[z][0][1]
        dist = hypot(posX - X, posY - Y)
        comida.append(dist)

    lowest = comida.index(min(comida))
    speedX = 0
    speedY = 0
    foodX = dataFood[lowest][0][0]
    foodY = dataFood[lowest][0][1]

    if posX < foodX:
        speedX += 4
    elif posX > foodX:
        speedX -= 4
    else:
        speedX = 0

    if posY < foodY:
        speedY += 4
    elif posY > foodY:
        speedY -= 4
    else:
        speedY = 0

    return speedX, speedY


def gameloop():
    sec = 0
    acabar = False
    shrimpPos = []
    foodData = []

    while not acabar:
        #   Reset the second counter so the variable sec doesn't get out of hand.
        if sec == 6000:
            sec = 0

        #   fill the background white.
        gameDisplay.fill(white)

        #   this permits to stay on alert to key strokes or other tipes of events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # if user presses the close button(the X on a window)
                pygame.quit()
                quit()

        #   create a shrimp every 10 seconds and if there isn't already 20 shrimps
        if sec % 600 == 0 and len(shrimpPos) != 20:
            shrimpPos.append(createShrimp())

        #   create 4 food every 1.5 second
        if sec % 90 == 0:
            foodData.append(createFood())
            foodData.append(createFood())
            foodData.append(createFood())
            foodData.append(createFood())
            foodData.append(createFood())

        #   increase food radious every 5 seconds
        if sec % 300 == 0:
            for z in range(0, len(foodData)):
                if foodData[z][1] < 15:
                    foodData[z][1] += 1

        #   redraw the food patches
        for z in range(0, len(foodData)):
            posX = foodData[z][0][0]
            posY = foodData[z][0][1]
            r = foodData[z][1]
            pygame.draw.circle(gameDisplay, green, (posX, posY), r)

        #   redraw the shrimp patches
        for x in range(0, len(shrimpPos)):
            pygame.draw.circle(gameDisplay, red, shrimpPos[x][0], shrimpPos[x][1])
        #    d = sqrt(((-)*(-))+((-)*(-)))
        #  i, l = shrimpPos[0]
        #  i+=1
        #  l+=1
        # shrimpPos[0] = (i,l)
        #  pygame.draw.circle(gameDisplay, black, shrimpPos[0], 10)
        #  for x in range(0, len(shrimpPos)):
        #    print(x)
        #   print(shrimpPos[x])

        #   move shrimps following the data returned from the tracking function
        for z in range(0, len(shrimpPos)):
            moveX, moveY = tracking(shrimpPos[z][0], foodData)
            shrimpPos[z][0][0] += moveX
            shrimpPos[z][0][1] += moveY

        #   verify if the shrimps are over the food patches
        #   if they are, the food will disapear
        for x in range(0, len(shrimpPos)):
            posSx = shrimpPos[x][0][0]
            posSy = shrimpPos[x][0][1]
            for z in range(0, len(foodData)):
                posFx = foodData[z][0][0]
                posFy = foodData[z][0][1]
                dist = hypot(posFx - posSx, posFy - posSy)
                if dist < (10 + foodData[z][1]):
                    shrimpPos[x][1] += 1
                    del foodData[z]
                    break

        #   verify if there are any shrimps coliding,
        #   if there are, delete one
        partir = False
        for x in range(0, len(shrimpPos)):
            posSx = shrimpPos[x][0][0]
            posSy = shrimpPos[x][0][1]
            for z in range(0, len(shrimpPos)):
                if x == z:
                    break
                posFx = shrimpPos[z][0][0]
                posFy = shrimpPos[z][0][1]
                dist = hypot(posFx - posSx, posFy - posSy)
                if dist < 20:
                    del shrimpPos[z]
                    partir = True
            if partir:
                break

        #   fazer update a imagem da janea
        pygame.display.update()
        clock.tick(60)
        sec += 1


gameloop()
