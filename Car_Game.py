import pygame
from pygame.locals import *
import random

pygame.init()

screen_width = 700
screen_height = 600

# for creating game window
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Car Game")

# rgb of colors
gray = (100, 100, 100)
green = (76, 208, 56)
red = (200, 0, 0)
white = (255, 255, 255)
black = (0, 0, 0)
yellow = (255, 232, 0)

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

# lode the other cars
image_filenames = ["car1.png", "car2.png", "car3.png", "car4.png", "car5.png", "car6.png", "car7.png"]
car_images = []
for image_filename in image_filenames:
    image = pygame.image.load('New folder/' + image_filename)
    car_images.append(image)

# sprite group for other cars
car_group = pygame.sprite.Group()

# load the crash image
crash = pygame.image.load('New folder/fire.png')
crash_rect = crash.get_rect()

# load music
pygame.mixer.music.load("New folder/background_music.wav") 
pygame.mixer.music.play(-1)
crash_sound = pygame.mixer.Sound("New folder/crash.wav")

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

                    game_over = True

                    # place the player car next to other car
                    # and determine where to position the crash image
                    if event.key == K_LEFT:
                        player.rect.left = car.rect.right
                        crash_rect.center = [player.rect.left, (player.rect.center[1]  + car.rect.center[1])/2]
                    elif event.key == K_RIGHT:
                        player.rect.right = car.rect.left
                        crash_rect.center = [player.rect.right, (player.rect.center[1]  + car.rect.center[1])/2]

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

            # select one random lane
            lane = random.choice(lanes)

            # select one random car image
            image = random.choice(car_images)
            car = Car(image, lane - 30, screen_height / -2)
            car_group.add(car)
            
    #make the car move
    for car in car_group:
        car.rect.y += speed

        # remove the car once it goes off screen
        if car.rect.top >= screen_height:
            car.kill()

            # add score
            score += 1

            # speed up the game after passing 10 cars
            if score % 10 == 0:
                speed += 1

    # draw the cars
    car_group.draw(screen)

    #  display score and speed
    font1 = pygame.font.Font(pygame.font.get_default_font(), 20)
    text1 = font1.render('Score: ' + str(score), True, white)
    text1_rect = text1.get_rect()
    text1_rect.center = (600, 200)
    screen.blit(text1, text1_rect)
    font2 = pygame.font.Font(pygame.font.get_default_font(), 20)
    text2 = font2.render('Speed: ' + str(speed * 20) + 'km/h', True, white)
    text2_rect = text2.get_rect()
    text2_rect.center = (600, 400)
    screen.blit(text2, text2_rect)

    # create if there is a head collision
    if pygame.sprite.spritecollide(player, car_group, True):
        game_over = True
        crash_rect.center = [player.rect.center[0], player.rect.top]

    # display game over and score
    if game_over:
        pygame.mixer.music.pause()
        crash_sound.play()
        screen.blit(crash, crash_rect)
        pygame.draw.rect(screen, red, (0, 50, screen_width, 100))
        font3 = pygame.font.Font(pygame.font.get_default_font(), 20)
        text3 = font3.render(f'Game Over. Your Score: {score}. Play again? (enter Y or N)', True, white)
        text3_rect = text3.get_rect()
        text3_rect.center = (screen_width / 2, 100)
        screen.blit(text3, text3_rect)
        
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
                    pygame.mixer.music.play(-1)
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
