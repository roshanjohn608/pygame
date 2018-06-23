import random, sys, pygame
from pygame.locals import *

# Global static values
FPS = 30
WINDOWwIDTH = 640
WINDOWHIEGHT = 480
HALF_WINWIDTH = int(WINDOWwIDTH/2)
HALF_WINHIEGHT = int(WINDOWHIEGHT/2)
MAP_STRUCTURE = [
                [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1]
                ]
PLAYER_SIZE = 30
BLOCK_SIZE = 30
BLOCK_SCALE = 30
PLAYER_MOVE_SPEED = 1
PLAYER_JUMP_SPEED = 1.75
GRAVITY = 0.01
COLLISION_SIZE = 28.5


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

    global DISPLAYSURF, PLAYER_IMG, AI_IMG, WALL_IMG, FPSCLOCK

    # Set up the initial pygame values
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWwIDTH, WINDOWHIEGHT))
    pygame.display.set_caption('My first game')

    # Load the respective image files
    PLAYER_IMG = pygame.image.load('player.png')
    AI_IMG = pygame.image.load('ai.png')
    WALL_IMG = pygame.image.load('wall_1.png')

    while True:
        GameLoop()


# Game loop, which starts the game
def GameLoop ():

    # Surface objects
    playerObj = {
                'rect' : None,
                'surface' : WALL_IMG,
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
            'rect_list' : [],
            'surface' : WALL_IMG,
            'size' : BLOCK_SIZE,
            'point_list' : []
    }

    floorObj = {
            'rect_list' : [],
            'surface' : WALL_IMG,
            'size' : BLOCK_SIZE,
            'point_list' : []
    }

    initialise_game_coordinates(wallObj, floorObj)

    # Main game loop, which runs each loop/state of the game
    while True:

        DISPLAYSURF.fill(WHITE)

        playerObj['rect'] = None
        del wallObj['rect_list'][:]
        del floorObj['rect_list'][:]
        draw_rect(playerObj, DISPLAYSURF)
        update_list_of_rects(wallObj, DISPLAYSURF)
        update_list_of_rects(floorObj, DISPLAYSURF)

        # Handles jumping
        key_pressed = pygame.key.get_pressed()
        floor_collide = playerObj['rect'].collidelist(floorObj['rect_list'])
        if key_pressed[K_SPACE] and floor_collide != -1 :
            if floorObj['point_list'][floor_collide][1] > playerObj['y'] :
                playerObj['y_velocity'] = -1 * PLAYER_JUMP_SPEED
                print('test')

        # Handles all inputs
        for event in pygame.event.get() :
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

        run_physics(playerObj, wallObj, floorObj)

        # Update the display surface onto the screen
        pygame.display.update()
        FPSCLOCK.tick(FPS)


# Handles physics of the game
def run_physics (playerObj, wallObj, floorObj):

    #playerObj['y_acceleration'] = GRAVITY

    floor_collide_direction = detect_collisions(playerObj, floorObj)[0]
    wall_collide_direction = detect_collisions(playerObj, wallObj)[0]
    floor_collide_element = detect_collisions(playerObj, floorObj)[1]
    wall_collide_element = detect_collisions(playerObj, wallObj)[1]

    #if floor_collide_direction == 'above' :
    #    playerObj['y'] = floorObj['point_list'][floor_collide_element][1] - COLLISION_SIZE
    #    playerObj['y_acceleration'] = 0
    #    if playerObj['y_velocity'] > 0 :
    #        playerObj['y_velocity'] = 0
    print(floor_collide_direction, floor_collide_element)

    # Handles the collisions
    #floor_collide = playerObj['rect'].collidelist(floorObj['rect_list'])
    #wall_collide = playerObj['rect'].collidelist(wallObj['rect_list'])

    #if floor_collide != -1 :
    #    if floorObj['point_list'][floor_collide][1]  > playerObj['y'] and playerObj['x'] floorObj['point_list]'][floor_collide][0] :
    #        playerObj['y'] = floorObj['point_list'][floor_collide][1] - 28.5
    #        playerObj['y_acceleration'] = 0
    #        if playerObj['y_velocity'] > 0 :
    #            playerObj['y_velocity'] = 0
    #    else :
    #        playerObj['y'] = floorObj['point_list'][floor_collide][1] + 30
        #if floorObj['point_list'][floor_collide][0] < playerObj['x'] :
        #    playerObj['x'] = floorObj['point_list'][floor_collide][0] + 30
        #else :
        #    playerObj['x'] = floorObj['point_list'][floor_collide][0] - 30

    #if wall_collide != -1 :
    #    if wallObj['point_list'][wall_collide][0] < playerObj['x'] :
    #        playerObj['x'] = wallObj['point_list'][wall_collide][0] + 30
    #    else :
    #        playerObj['x'] = wallObj['point_list'][wall_collide][0] - 30

    playerObj['x_velocity'] += playerObj['x_acceleration']
    playerObj['y_velocity'] += playerObj['y_acceleration']
    playerObj['x'] += playerObj['x_velocity']
    playerObj['y'] += playerObj['y_velocity']
    #print(playerObj['y_velocity'])


# Terminate the game
def terminate ():
    pygame.quit()
    sys.exit()


# Returns a tuple of the direction and the index
def detect_collisions (obj, obj_list) :

    half_dist_obj = (obj['size']/2)
    half_dist_obj_list = (obj_list['size']/2)
    collide = obj['rect'].collidelist(obj_list['rect_list'])
    obj_mid = (obj['x'] + half_dist_obj, obj['y'] + half_dist_obj)
    obj_list_mid = (obj_list['point_list'][collide][0] + half_dist_obj_list, obj_list['point_list'][collide][1] + half_dist_obj_list)
    mid_x_difference = obj_mid[0] - obj_list_mid[0]
    mid_y_difference = obj_mid[1] - obj_list_mid[1]

    if collide == -1 :
        return ('nope', collide)
    else :
        if abs(mid_y_difference) > abs(mid_x_difference) :
            if mid_y_difference < 0 :
                return ('above', collide)
            else :
                return ('below', collide)
        else :
            if mid_x_difference < 0 :
                return ('left-to', collide)
            else :
                return ('right-to', collide)


# Draw a surface object as a rect on a surface
def draw_rect (obj, display_surf):

    surface = pygame.transform.scale(obj['surface'], (obj['size'], obj['size']))
    rect = surface.get_rect()
    rect = rect.move((obj['x'], obj['y']))
    display_surf.blit(surface, rect)
    obj['rect'] = rect


# Draw multiple surface objects on a surface
def update_list_of_rects (obj_list, display_surf):

    rect_list = []
    surface = pygame.transform.scale(obj_list['surface'], (obj_list['size'], obj_list['size']))
    for point in obj_list['point_list']:
        rect = surface.get_rect()
        rect = rect.move(point[0], point[1])
        rect_list.append(rect)
        display_surf.blit(surface, rect)
    obj_list['rect_list'] = rect_list


# Convert MAP_STRUCTURE into game coordinates
def initialise_game_coordinates (wall_list, floor_list):

    for x in range (len (MAP_STRUCTURE)):
        for y in range (len (MAP_STRUCTURE[x])):
            if MAP_STRUCTURE[x][y] == 1 :
                wall_list['point_list'].append((y*BLOCK_SCALE, x*BLOCK_SCALE))
            elif MAP_STRUCTURE[x][y] == 2 :
                floor_list['point_list'].append((y*BLOCK_SCALE, x*BLOCK_SCALE))


if __name__ == '__main__' :
    main()
