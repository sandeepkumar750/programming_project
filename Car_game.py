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
lane_marker_move_y = 0          # sai

#akhilash code
class Car(pygame.sprite.Sprite):

    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)

        # scale the image down. so it's not wider than the lane
        car_scale = 50 / image.get_rect().width
        nw = image.get_rect().width * car_scale
        nh = image.get_rect().height * car_scale
        self.image = pygame.transform.scale(image, (nw, nh))

        self.rect = self.image.get_rect()
        self.rect.center = [x, y]


class PlayerCar(Car):
    def __init__(self, x, y):
        image = pygame.image.load("New folder/SportCar.png")
        super().__init__(image, x, y)


# starting position
player_x = 245
player_y = 550

# creat the player car
player_group = pygame.sprite.Group()
player = PlayerCar(player_x, player_y)
player_group.add(player)

# lode the other car
image_filenames = ["car1.png", "car2.png", "car3.png", "car4.png", "car5.png", "car6.png", "car7.png"]
car_images = []
for image_filename in image_filenames:
    image = pygame.image.load('New folder/' + image_filename)
    car_images.append(image)

# sprite group for other cars
car_group = pygame.sprite.Group()

# load the crash image
crash = pygame.image.load('New folder/fire1.png')
crash_rect = crash.get_rect()

# load music
pygame.mixer.music.load("New folder/back.wav") 
pygame.mixer.music.play(-1, 0.0)
crash_sound = pygame.mixer.Sound("New folder/crash.wav")   # akhilash

#sandeep code
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
                        crash_rect.center = [player.rect.right, (player.rect.center[1]  + car.rect.center[1])/2]    # sandeep

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
    
    # sandeep code
    #draw the player car
    player_group.draw(screen)

    # add up to four cars
    if len(car_group) < 4:
        # ensure there's enough gap between vehicles
        add_car = True
        for car in car_group:
            if car.rect.top < car.rect.height *1.5:
                add_car = False 

        if add_car:

            # select a rendum lane
            lane = random.choice(lanes)

            # select an random car image
            image = random.choice(car_images)
            car = Car(image, lane - 30, screen_height / -2)
            car_group.add(car)
            
    #make the car move
    for car in car_group:
        car.rect.y += speed

        ## remove the car once it goes off screen
        if car.rect.top >= screen_height:
            car.kill()

            # add score
            score += 1

            # speed up the game after passing 10 cars
            if score > 0 and score % 10 == 0:
                speed += 1

    # draw the cars
    car_group.draw(screen)

    # # display score
    pygame.font.init()
    font = pygame.font.Font(pygame.font.get_default_font(), 16)
    text = font.render('Score: ' + str(score), True, white)
    text_rect = text.get_rect()
    text_rect.center = (600, 100)
    screen.blit(text, text_rect)

    # creat if there a head collision
    if pygame.sprite.spritecollide(player, car_group, True):
        game_over = True
        crash_rect.center = [player.rect.center[0], player.rect.top]

    # display game over
    if game_over:
        pygame.mixer.music.pause()
        crash_sound.play()

        screen.blit(crash, crash_rect)

        pygame.draw.rect(screen, red, (0, 50, screen_width, 100))

        font = pygame.font.Font(pygame.font.get_default_font(), 16)
        text = font.render(f'Game Over. Your Score: {score}. Play again? (enter Y or N)', True, white)
        text_rect = text.get_rect()
        text_rect.center = (screen_width / 2, 100)
        screen.blit(text, text_rect)


      
    
    pygame.display.update()

    # check if player want to play again
    while game_over:

        clock.tick(fps)

        for event in pygame.event.get():

            if event.type == QUIT:
                game_over = False
                running = False

            # get the player input (y or n)
            if event.type == KEYDOWN:
                if event.key == K_y:
                    pygame.mixer.music.play(-1, 0.0)
                    # reset the game
                    game_over = False
                    speed = 2
                    score = 0
                    car_group.empty()
                    player.rect.center = [player_x, player_y]
                elif event.key == K_n:
                    # exit the loop
                    game_over = False
                    running = False



pygame.quit()

