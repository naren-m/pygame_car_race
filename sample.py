import pygame
import random
import time
from PIL import Image

pygame.init()

display_width = 800
display_height = 600
game_window_size = (display_width, display_height)

# Color definitions
white = (255, 255, 255)
black = (0, 0, 0)

gd = pygame.display.set_mode(game_window_size)
pygame.display.set_caption('test')
clock = pygame.time.Clock()

car_img = pygame.image.load('Car.png')
im = Image.open('Car.png')
car_width, car_height = im.size

def car(x,y):
    # blit prepare the image to display in background and show once update
    # is called
    gd.blit(car_img, (x,y))

def crash():
    message_display('Crashed!!!')

def message_display(text):
    large_text = pygame.font.Font('freesansbold.ttf', 115)
    text_surface, text_rect = text_objects(text, large_text)
    text_rect.center = (display_width/2, display_height/2)
    gd.blit(text_surface, text_rect)

    pygame.display.update()
    time.sleep(2)
    game_loop()

def things_dodged(count):
    font = pygame.font.SysFont(None, 25)
    text = font.render("Dodged: "+str(count), True, black)
    gd.blit(text,(0,0))

def text_objects(text, font):
    ts = font.render(text, True, black)
    return ts, ts.get_rect()

def things(thingx, thingy, thingw, thingh, color):
    pygame.draw.rect(gd, color, [thingx, thingy, thingw, thingh])

def game_loop():
    x = display_width * 0.45
    y = display_height * 0.8

    game_exit = False
    x_change = 0
    thing_startx = random.randrange(0, display_width)
    thing_starty = -600
    thing_speed = 7
    thing_width = 100
    thing_height = 100

    thing_count = 1

    dodged = 0

    while not game_exit:
        for event in pygame.event.get():
            # Condition to quit
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -5
                elif event.key == pygame.K_RIGHT:
                    x_change = 5

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0

        x += x_change
        gd.fill(white)

        things(thing_startx, thing_starty, thing_width, thing_height, black)

        thing_starty += thing_speed
        car(x,y)
        things_dodged(dodged)

        if x > display_width - car_width or x < 0:
            crash()

        if thing_starty > display_height:
            thing_starty = 0 - thing_height
            thing_startx = random.randrange(0,display_width)
            dodged += 1
            thing_speed += 1
            thing_width += (dodged * 1.2)


        ####
        if y < thing_starty+thing_height:
            print('y crossover')

            if x > thing_startx and x < thing_startx + thing_width or x+car_width > thing_startx and x + car_width < thing_startx+thing_width:
                print('x crossover')
                crash()
        ####

        pygame.display.update()
        clock.tick(60) # Frames per second

game_loop()
pygame.quit()
quit()

