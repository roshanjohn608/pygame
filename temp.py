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
                [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1]
                ]
PLAYER_SIZE = 30
BLOCK_SIZE = 35
BLOCK_SCALE = 30
PLAYER_MOVE_SPEED = 1
PLAYER_JUMP_SPEED = 1
GRAVITY = 0.01


# WINDOWwIDTH and WINDOWHIEGHT define the dimensions of th game window
# HALF_WINWIDTH and HALF_WINHIEGHT is the centre of the screen
# MAP_STRUCTURE is the initial structure of the map
# PLAYER_SIZE defines the size of the player sprite
# BLOCK_SIZE defines size of a block sprite
# BLOCK_SCALE is how much each set of MAP_STRUCTURE coordinates is scaled to fit the game screen
# PLAYER_MOVE_SPEED and PLAYER_JUMP_SPEED sets the speed for player movement
# GRAVITY defines acceleration due to gravity

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

    floorObj = {
            'surface' : WALL_IMG,
            'size' : BLOCK_SIZE,
            'rect_list' : []
    }

    initialise_game_coordinates(wallObj, floorObj)

    # Main game loop, which runs each loop/state of the game
    while True:

        DISPLAYSURF.fill(WHITE)
        player_rect = draw_rect(playerObj, DISPLAYSURF)
        wall_rects_list = update_list_of_rects(wallObj, DISPLAYSURF)
        floor_rects_list = update_list_of_rects(floorObj, DISPLAYSURF)

        key_pressed = pygame.key.get_pressed()
        if key_pressed[K_SPACE] and player_rect.collidelist(floor_rects_list) != -1 :
            playerObj['y_velocity'] = -1 * PLAYER_JUMP_SPEED

        # Handles all inputs
        for event in pygame.event.get():
            if event.type == QUIT :
                terminate()

            elif event.type == KEYDOWN :
                if event.key == K_ESCAPE :
                    terminate()
                elif event.key == K_a :
                    playerObj['x_velocity'] = -1 * PLAYER_MOVE_SPEED
                elif event.key == K_d :
                    playerObj['x_velocity'] = 1 * PLAYER_MOVE_SPEED
                elif event.key == K_w :
                    playerObj['y_velocity'] = -1 * PLAYER_MOVE_SPEED
                elif event.key == K_s :
                    playerObj['y_velocity'] = 1 * PLAYER_MOVE_SPEED

            elif event.type == KEYUP :
                if event.key == K_a and playerObj['x_velocity'] < 0 :
                    playerObj['x_velocity'] = 0
                elif event.key == K_d and playerObj['x_velocity'] > 0 :
                    playerObj['x_velocity'] = 0
                elif event.key == K_w and playerObj['y_velocity'] < 0 :
                    playerObj['y_velocity'] = 0
                elif event.key == K_s and playerObj['y_velocity'] > 0 :
                    playerObj['y_velocity'] = 0


        run_physics(playerObj)

        # Update the display surface onto the screen
        pygame.display.update()

# Handles physics of the game
def run_physics(playerObj):

    playerObj['y_acceleration'] = GRAVITY
    playerObj['x_velocity'] += playerObj['x_acceleration']
    playerObj['y_velocity'] += playerObj['y_acceleration']
    playerObj['x'] += playerObj['x_velocity']
    playerObj['y'] += playerObj['y_velocity']

    if playerObj['x'] > 575:
        playerObj['x'] = 575
    elif playerObj['x'] < 30:
        playerObj['x'] = 30
    if playerObj['y'] > 395:
        playerObj['y'] = 395
    elif playerObj['y'] < 30:
        playerObj['y'] = 30

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
    return rect

# Draw multiple surface objects on a surface
def update_list_of_rects (obj_list, display_surf):
    rect_list = []
    surface = pygame.transform.scale(obj_list['surface'], (obj_list['size'], obj_list['size']))
    for point in obj_list['rect_list']:
        rect = surface.get_rect()
        rect = rect.move(point[0], point[1])
        rect_list.append(rect)
        display_surf.blit(surface, rect)
    return rect_list

# Convert MAP_STRUCTURE into game coordinates
def initialise_game_coordinates (wall_list, floor_list):
    for x in range (len (MAP_STRUCTURE)):
        for y in range (len (MAP_STRUCTURE[x])):
            if MAP_STRUCTURE[x][y] == 1 :
                wall_list['rect_list'].append((y*BLOCK_SCALE, x*BLOCK_SCALE))
            elif MAP_STRUCTURE[x][y] == 2 :
                floor_list['rect_list'].append((y*BLOCK_SCALE, x*BLOCK_SCALE))

if __name__ == '__main__' :
    main()
