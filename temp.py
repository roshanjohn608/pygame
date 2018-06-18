import random, sys, pygame
from pygame.locals import *

WINDOWwIDTH = 640
WINDOWHIEGHT = 480
HALF_WINWIDTH = int(WINDOWwIDTH/2)
HALF_WINHIEGHT = int(WINDOWHIEGHT/2)

#colors   R    G    B
WHITE = (255, 255, 255)

def main():

    global DISPLAYSURF, PLAYER_IMG, AI_IMG, WALL_IMG, START_SIZE

    #Set up the initial pygame values
    pygame.init()
    DISPLAYSURF = pygame.display.set_mode((WINDOWwIDTH, WINDOWHIEGHT))
    pygame.display.set_caption('My first game')

    #Load the respective image files
    PLAYER_IMG = pygame.image.load('player_1.png')
    AI_IMG = pygame.image.load('ai.png')
    WALL_IMG = pygame.image.load('wall.png')

    START_SIZE = 1000

    #PLAYER_IMG = pygame.transform.scale(PLAYER_IMG, (100, 0))

    while True:
        GameLoop()

def GameLoop():

    #Player values
    PLAYER_SIZE = START_SIZE
    P_x = HALF_WINWIDTH
    P_y = HALF_WINHIEGHT

    while True:
        print (PLAYER_SIZE)
        PLAYER_SIZE -= 1
        DISPLAYSURF.fill(WHITE)
        p_Rect = PLAYER_IMG.get_rect()
        p_Rect = p_Rect.move((P_x,P_y))
        DISPLAYSURF.blit(PLAYER_IMG, p_Rect)

        #Event handler
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                terminate()

        #Update the display surface onto the screen
        pygame.display.update()

def terminate():
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
