import pygame
import sys
import time
import os

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

class Level:
    def __init__(self):
        self.display=pygame.display.get_surface()

        self.allSprites=pygame.sprite.Group()

        self.setup()
    
    def setup(self):
        self.player = Player((640,360), self.allSprites)
    def run(self, delta_time):
        self.display.fill((0, 0, 0))  # Fill the display with black color
        self.allSprites.draw(self.display)
        self.allSprites.update(delta_time)
class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group):
  
        super().__init__(group)
        # super helps access stuff in parent class
        self.import_animations()
        self.status = 'front'
        self.frame_index = 0

        # coding image
        self.image= self.animations[self.status][0]
        self.scale_factor = 4.0
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * self.scale_factor), int(self.image.get_height() * self.scale_factor)))
        self.rect = self.image.get_rect(center=pos)
		
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 200
		
    def import_animations(self):
        self.animations={'front': [], 'back': [], 'left': [], 'right': [],
                          'front left': [], 'front right': [], 'front idle': [],
                          'back idle': [], 'back right': [], 'back left': [], 
                          'left right': [],  'left left': [], 'right left': [],
                          'right right': []}
        for animation in self.animations.keys():
            path_1 = 'Graphics/'
            print(path_1)
            self.animations[animation] = import_folder(path_1, animation)
        print(self.animations)

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            self.status = 'back'
            self.direction.y -= 5
            
        elif keys[pygame.K_DOWN]:
            self.status = 'front'
            self.direction.y += 5
        else:
            self.direction.y = 0

        if keys[pygame.K_RIGHT]:
            self.status = 'right'
            self.direction.x += 5
        elif keys[pygame.K_LEFT]:
            self.status = 'left'
            self.direction.x -=5
        else:
            self.direction.x = 0
	
    def move(self, delta_time):

		# normalizing a vector 
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()

		# horizontal movement
        self.pos.x += self.direction.x * self.speed * delta_time
        self.rect.centerx = self.pos.x

		# vertical movement
        self.pos.y += self.direction.y * self.speed * delta_time
        self.rect.centery = self.pos.y
    def update(self, delta_time):
        self.input()
        self.move(delta_time)
        # Update player's image based on animation and frame index
        self.image = self.animations[self.status][self.frame_index]

        # Update player's image size
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * self.scale_factor), int(self.image.get_height() * self.scale_factor)))

def import_folder(path, animation):
    surface_list = []

    img_files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    
    for image in img_files:
        full_path = os.path.join(path, image)
        img_path = full_path.split("/")[1][:-4]
        print(img_path)
        image_surf = pygame.image.load(full_path).convert_alpha()
        if img_path == animation:
            surface_list.append(image_surf)

    return surface_list

if __name__ == '__main__':
    # ask yousuf what main does
    game = Game()
    game.run()
