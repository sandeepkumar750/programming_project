# sai code
import pygame
from pygame.locals import *
import random

pygame.init()

screen_width = 700
screen_height = 600

# for creating game window
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Car Driving Game")

# grb of colors
gray = (100, 100, 100)
green = (76, 208, 56)
red = (200, 0, 0)
white = (255, 255, 255)
yellow = (255, 232, 0)
black = (0, 0, 0)
# Game setting
game_over = False
speed = 2
score = 0

# marker size
marker_height = 50
marker_width = 10

# score board
score_board = (500, 0, 200, screen_height)

# road and marker edge
road = (70, 0, 350, screen_height)
left_edge_marker = (65, 0, marker_width, screen_height)
right_edge_marker = (415, 0, marker_width, screen_height)

# x coordinate of Lanes
lane1 = 135
lane2 = 205
lane3 = 275
lane4 = 345
lane5 = 415
lanes = [lane1, lane2, lane3, lane4, lane5]

# for animating movement of lane marker
lane_marker_move_y = 0

#sandeep
# game loop
clock = pygame.time.Clock()
fps = 120
running = True

while running:

    clock.tick(fps)

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        # move the player car left right aro key
        if event.type == KEYDOWN:
            if event.key == K_LEFT and player.rect.center[0] > lane1:
                player.rect.x -= 70
            elif event.key == K_RIGHT and player.rect.center[0] < lane4:
                player.rect.x += 70

            # check if there's a side swipe cillision after changing lnes
            for car in car_group:
                if pygame.sprite.collide_rect(player, car):

                    gameover = True

                    # place the player car next to other car
                    # and determine where to position the crash image
                    if event.key == K_LEFT:
                        player.rect.left = car.rect.right -1
                        crash_rect.center = [player.rect.left, (player.rect.center[1]  + car.rect.center[1])/2]
                    elif event.key == K_RIGHT:
                        player.rect.right = car.rect.left  + 1
                        crash_rect.center = [player.rect.right, (player.rect.center[1]  + car.rect.center[1])/2]

# sai code
    # draw the grass
    screen.fill(green)

    # draw the score bord
    pygame.draw.rect(screen, black, score_board)

    # dra road
    pygame.draw.rect(screen, gray, road)

    # draw edge marker
    pygame.draw.rect(screen, yellow, left_edge_marker)
    pygame.draw.rect(screen, yellow, right_edge_marker)

    # draw lane markers
    lane_marker_move_y += (speed * 2)
    if lane_marker_move_y >= (marker_height * 2):
        lane_marker_move_y = 0
    for y in range(marker_height * -2, screen_height, marker_height * 2):
        pygame.draw.rect(screen, white, (lane1, y + lane_marker_move_y, marker_width, marker_height))
        pygame.draw.rect(screen, white, (lane2, y + lane_marker_move_y, marker_width, marker_height))
        pygame.draw.rect(screen, white, (lane3, y + lane_marker_move_y, marker_width, marker_height))
        pygame.draw.rect(screen, white, (lane4, y + lane_marker_move_y, marker_width, marker_height))    #sai
