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

SCREEN = pygame.display.set_mode(game_window_size)
pygame.display.set_caption('test')
clock = pygame.time.Clock()

car_img = pygame.image.load('Car.png')
im = Image.open('Car.png')
car_width, car_height = im.size

class Game:
    def __init__(self):
        self.score = 0
        self.playerx = display_width * 0.45
        self.playery = display_height * 0.8
        self.playerx_displacement = 0
        self.PLAYER_LEFT_MOVE = 0
        self.PLAYER_RIGHT_MOVE = 1
        self.VALID_ACTIONS = 2
        self.actions = list([0, 0])

        self.FPS = 60
        self.obstacle_startx = random.randrange(0, display_width)
        self.obstacle_starty = -600
        self.obstacle_speed = 10
        self.obstacle_width = 100
        self.obstacle_height = 100
        self.score = 0

    def draw_car(self, x ,y):
        # blit prepare the image to display in background and show once update
        # is called
        SCREEN.blit(car_img, (x,y))

    def show_crash_msg(self):
        def text_objects(text, font):
            ts = font.render(text, True, black)
            return ts, ts.get_rect()
        
        text = 'Crashed!!!'
        large_text = pygame.font.Font('freesansbold.ttf', 115)
        text_surface, text_rect = text_objects(text, large_text)
        text_rect.center = (display_width/2, display_height/2)
        SCREEN.blit(text_surface, text_rect)

        pygame.display.update()
        time.sleep(2)
        self.game_loop()

    def things_dodged(self, count):
        font = pygame.font.SysFont(None, 25)
        text = font.render("Dodged: "+str(count), True, black)
        SCREEN.blit(text,(0,0))

    def draw_things(self, thingx, thingy, thingw, thingh, color):
        pygame.draw.rect(SCREEN, color, [thingx, thingy, thingw, thingh])

    def _is_crash(self):
        if self.playerx  > display_width - car_width or self.playerx  < 0:
            return True

        if self.playery < self.obstacle_starty+self.obstacle_height:
            if self.playerx  > self.obstacle_startx and self.playerx  < self.obstacle_startx + self.obstacle_width or self.playerx + car_width > self.obstacle_startx and self.playerx + car_width < self.obstacle_startx+self.obstacle_width:
                return True

        return False
        
    def game_loop(self):
        game_exit = False

        self.__init__()

        while not game_exit:
            for event in pygame.event.get():
                # Condition to quit
                if event.type == pygame.QUIT:
                    # pygame.quit()
                    # quit()
                    game_exit = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        # Move left
                        self.actions[self.PLAYER_LEFT_MOVE] = 1
                        self.actions[self.PLAYER_RIGHT_MOVE] = 0
                        self.playerx_displacement = -5
                    elif event.key == pygame.K_RIGHT:
                        # Move right
                        self.actions[self.PLAYER_LEFT_MOVE] = 0
                        self.actions[self.PLAYER_RIGHT_MOVE] = 1
                        self.playerx_displacement = 5

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        # Dont move
                        self.actions[self.PLAYER_LEFT_MOVE] = 0
                        self.actions[self.PLAYER_RIGHT_MOVE] = 0
                        self.playerx_displacement = 0
            self.frame(1)
        pygame.quit()
        quit()

    def frame(self, input_actions):
        self.playerx += self.playerx_displacement
        
        SCREEN.fill(white)

        self.draw_things(self.obstacle_startx, self.obstacle_starty, self.obstacle_width, self.obstacle_height, black)
        self.draw_car(self.playerx,self.playery)
        self.things_dodged(self.score)

        self.obstacle_starty += self.obstacle_speed

        if self.obstacle_starty > display_height:
            self.obstacle_starty = 0 - self.obstacle_height
            self.obstacle_startx = random.randrange(0,display_width)
            self.score += 1
            # to increase obstacle speed
            self.obstacle_speed += 0.5
            # to increase the width of obstacle
            # self.obstacle_width += (self.score * 1.2)
        
        if self._is_crash():
            self.show_crash_msg()
            self.__init__()

        pygame.display.update()
        clock.tick(self.FPS) # Frames per second


g = Game()
g.game_loop()

