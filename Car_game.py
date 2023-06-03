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
        pygame.draw.rect(screen, white, (lane4, y + lane_marker_move_y, marker_width, marker_height))
