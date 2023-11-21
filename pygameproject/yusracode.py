import pygame
import sys
import time
from level import Level

class Game:
    def __init__(self):
        # setting up the display screen and the clock to control the framerate and speed
        pygame.init()
        self.screen = pygame.display.set_mode((1280,670))
        pygame.display.set_caption('APS Project')
        self.clock = pygame.time.Clock()
        self.level = Level()
    def run(self):
        # this program runs the game
        # previous_time=time.time()
        # previous time declared before while loop as it needs to update outside loop
        while True:
            # delta_time=previous_time-time.time()
            # previous_time=time.time()
            # delta time ensures smooth movement regardless of computer upto some level. different ways to get delta time
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # so we can quit by pressing x button on display screen
                    pygame.display.quit()
                    pygame.quit()
                    sys.exit()
            delta_time = self.clock.tick()/1000
            self.level.run(delta_time) 
            pygame.display.update()

if __name__ == '__main__':
    # ask yousuf what main does
    game = Game()
    game.run()
