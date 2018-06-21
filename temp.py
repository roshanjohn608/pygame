import random, sys, pygame
from pygame.locals import *

# Global static values
WINDOWwIDTH = 640
WINDOWHIEGHT = 480
HALF_WINWIDTH = int(WINDOWwIDTH/2)
HALF_WINHIEGHT = int(WINDOWHIEGHT/2)
MAP_STRUCTURE = [
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
                ]
PLAYER_SIZE = 30
BLOCK_SIZE = 35
BLOCK_SCALE = 30
PLAYER_MOVE_SPEED = 1

# WINDOWwIDTH and WINDOWHIEGHT define the dimensions of th game window
# HALF_WINWIDTH and HALF_WINHIEGHT is the centre of the screen
# MAP_STRUCTURE is the initial structure of the map
# PLAYER_SIZE defines the size of the player sprite
# BLOCK_SIZE defines size of a block sprite
# BLOCK_SCALE is how much each set of MAP_STRUCTURE coordinates is scaled to fit the game screen
# PLAYER_MOVE_SPEED sets the speed for player movement

# colors  R    G    B
WHITE = (255, 255, 255)

def main ():

    global DISPLAYSURF, PLAYER_IMG, AI_IMG, WALL_IMG

    # Set up the initial pygame values
    pygame.init()
    DISPLAYSURF = pygame.display.set_mode((WINDOWwIDTH, WINDOWHIEGHT))
    pygame.display.set_caption('My first game')

    # Load the respective image files
    PLAYER_IMG = pygame.image.load('player.png')
    AI_IMG = pygame.image.load('ai.png')
    WALL_IMG = pygame.image.load('wall.png')

    while True:
        GameLoop()

# Game loop, which starts the game
def GameLoop ():

    # Surface objects
    playerObj = {
                'surface' : PLAYER_IMG,
                'direction_forward' : True,
                'x' : HALF_WINWIDTH,
                'y' : HALF_WINHIEGHT,
                'size' : PLAYER_SIZE,
                'x_velocity' : 0,
                'y_velocity' : 0,
                'x_acceleration' : 0,
                'y_acceleration' : 0
    }

    wallObj = {
            'surface' : WALL_IMG,
            'size' : BLOCK_SIZE,
            'rect_list' : []
    }

    initialise_game_coordinates(wallObj)

    # Main game loop, which runs each loop/state of the game
    while True:

        DISPLAYSURF.fill(WHITE)
        draw_rect(playerObj, DISPLAYSURF)
        update_list_of_rects(wallObj, DISPLAYSURF)

        # Event handler
        for event in pygame.event.get():
            if event.type == QUIT :
                terminate()
            elif event.type == KEYDOWN :
                if event.key == K_ESCAPE :
                    terminate()

        keys_pressed =  pygame.key.get_pressed()
        if keys_pressed[K_a]:
            move_surface(playerObj, 'left', PLAYER_MOVE_SPEED)
        if keys_pressed[K_d]:
            move_surface(playerObj, 'right', PLAYER_MOVE_SPEED)
        if keys_pressed[K_w]:
            move_surface(playerObj, 'up', PLAYER_MOVE_SPEED)
        if keys_pressed[K_s]:
            move_surface(playerObj, 'down', PLAYER_MOVE_SPEED)

        # Update the display surface onto the screen
        pygame.display.update()

# Terminate the game
def terminate ():
    pygame.quit()
    sys.exit()

# Draw a surface object as a rect on a surface
def draw_rect (surf_obj, display_surf):
    surface = pygame.transform.scale(surf_obj['surface'], (surf_obj['size'], surf_obj['size']))
    rect = surface.get_rect()
    rect = rect.move((surf_obj['x'],surf_obj['y']))
    display_surf.blit(surface, rect)

# Draw multiple surface objects on a surface
def update_list_of_rects (obj_list, display_surf):
    rect_list = []
    surface = pygame.transform.scale(obj_list['surface'], (obj_list['size'], obj_list['size']))
    for point in obj_list['rect_list']:
        rect = surface.get_rect()
        rect = rect.move(point[0], point[1])
        rect_list.append(rect)
        display_surf.blit(surface, rect)

# Convert MAP_STRUCTURE into game coordinates
def initialise_game_coordinates (obj_list):
    for x in range (len (MAP_STRUCTURE)):
        for y in range (len (MAP_STRUCTURE[x])):
            if MAP_STRUCTURE[x][y] == 1 :
                obj_list['rect_list'].append((y*BLOCK_SCALE, x*BLOCK_SCALE))

# Gives a surface some speed
def move_surface (surf_obj, direction, speed):
    if direction == 'left' :
        surf_obj['x'] -= speed
    elif direction == 'right' :
        surf_obj['x'] += speed
    elif direction == 'up' :
        surf_obj['y'] -= speed
    elif direction == 'down' :
        surf_obj['y'] += speed

if __name__ == '__main__' :
    main()
