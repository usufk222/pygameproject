import pygame
import sys
import time
import os
from random import randint


class Game:
    
    screen = pygame.display.set_mode((1280,670))
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
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.level.player.block_hover_rect.colliderect(self.level.player.indicator_rect):
                        print("Block Placed")
                        # Create a new block with the current position of the block_hover_rect
                        new_block = Block(self.level.player.block_hover_rect.center)
                        self.level.blocks.append(new_block)    
                elif event.type == pygame.KEYDOWN:
                    # Block Deleting Keys
                    if event.key == pygame.K_SPACE:
                        for block in self.level.blocks:
                            if block.block_placed_rect.colliderect(self.level.player.block_hover_rect) and block.block_placed_rect.colliderect(self.level.player.indicator_rect):
                                print("Block Deleted")
                                self.level.blocks.remove(block)
                    # Block changing keys
                    elif event.key == pygame.K_1:
                        self.level.player.block_index = 0
                        Player.block_index = 0
                        print("Block changed")
                    elif event.key == pygame.K_2:
                        print("Block changed")
                        self.level.player.block_index = 1
                        Player.block_index = 1
                    elif event.key == pygame.K_3:
                        print("Block changed")
                        self.level.player.block_index = 2
                        Player.block_index = 2
                    elif event.key == pygame.K_4:
                        print("Block changed")
                        self.level.player.block_index = 3
                        Player.block_index = 3
                    elif event.key == pygame.K_5:
                        self.random_color(self.level.player, 2)
                    elif event.key == pygame.K_6:
                        self.level.player.block_index = 4
                        Player.block_index = 4
            delta_time = self.clock.tick()/1000
            self.level.run(delta_time) 
            pygame.display.update()
            
    def random_color(self, player, n):
        if n > 0:
            pygame.time.delay(200)
            Player.block_index = randint(0,3)
            player.block_index = Player.block_index
            print("Random block selected")
            self.random_color(self.level.player, n-1)
        else:
            Player.block_index = randint(0,3)
            player.block_index = Player.block_index
            print("Random block selected")
            


class Level:

    def __init__(self):
        self.display=pygame.display.get_surface()

        self.allSprites=pygame.sprite.Group()

        self.setup()
    
        self.blocks = []

    def setup(self):
        self.player = Player((640,360), self.allSprites)
    def run(self, delta_time):
        self.display.fill((0, 0, 0))  # Fill the display with black color
        self.allSprites.draw(self.display)
        self.allSprites.update(delta_time)
        self.display.blit(self.player.indicator, self.player.indicator_rect.topleft)
        if self.player.block_hover_rect.colliderect(self.player.indicator_rect):
            self.display.blit(self.player.block_hover, self.player.block_hover_rect)
        for block in self.blocks:
            self.display.blit(block.block_placed, block.block_placed_rect.topleft)
        self.player.update_colors()

class Block(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.width = 60
        # Placed block
        self.block_placed = pygame.Surface((self.width//2, self.width//2), pygame.SRCALPHA)
        pygame.draw.rect(self.block_placed, Player.block_colors[Player.block_index], self.block_placed.get_rect())
        self.block_placed_rect = self.block_placed.get_rect(center=position)

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

class Player(pygame.sprite.Sprite):

    block_colors = [(255, 255, 0, 255), (255, 0, 0, 255), (0, 255, 0, 255), (0, 0, 255, 255), import_folder("Assets/", "basic tree")[0]]
    block_hover_colors = [(255, 255, 0, 64), (255, 0, 0, 64), (0, 255, 0, 64), (0, 0, 255, 64)]
    block_index = 0

    def __init__(self, pos, group, level=Level):
  
        super().__init__(group)
        # super helps access stuff in parent class
        self.level = level
        self.import_animations()
        self.status = 'front'
        self.frame_index = 0


        self.block_colors = [(255, 255, 0, 255), (255, 0, 0, 255), (0, 255, 0, 255), (0, 0, 255, 255), import_folder("Assets/", "basic tree")[0]]
        self.block_hover_colors = [(255, 255, 0, 64), (255, 0, 0, 64), (0, 255, 0, 64), (0, 0, 255, 64)]
        self.block_index = 0

        # coding image
        self.image= self.animations[self.status][0]
        self.scale_factor = 3.0
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * self.scale_factor), int(self.image.get_height() * self.scale_factor)))
        self.rect = self.image.get_rect(center=pos)
		
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 200

        self.width = 60
        # coding block placing visuals
        self.usable_width = self.width * 2
        self.indicator = pygame.Surface((self.usable_width * 3, self.usable_width * 3), pygame.SRCALPHA)
        if isinstance(self.block_colors[self.block_index], tuple) == True:
            pygame.draw.rect(self.indicator, self.block_hover_colors[self.block_index], self.indicator.get_rect(), 3)
        else:
            self.block_image = self.block_colors[self.block_index]
            pygame.draw.rect(self.indicator, self.block_image.get_at((0,0)), self.indicator.get_rect(), 3)
        self.indicator_rect = self.indicator.get_rect(center=(self.pos))

        # Block Hover
        cursor = self.mouse_block()
        self.block_hover = pygame.Surface((self.width//2, self.width//2), pygame.SRCALPHA)
        if isinstance(self.block_colors[self.block_index], tuple) == True:
            pygame.draw.rect(self.block_hover, self.block_hover_colors[self.block_index], self.block_hover.get_rect())
        else:
            self.block_image = self.block_colors[self.block_index]
            pygame.draw.rect(self.block_hover, self.block_colors[self.block_index], self.block_hover.get_rect())
        self.block_hover_rect = self.block_hover.get_rect(center=(cursor))
		
        self.update_colors()
    
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
    
    def mouse_block(self):
        cursor = pygame.mouse.get_pos()
        return cursor
    
    def update_colors(self):
        self.indicator = pygame.Surface((self.usable_width * 3, self.usable_width * 3), pygame.SRCALPHA)
        if isinstance(self.block_colors[self.block_index], tuple) == True:
            pygame.draw.rect(self.indicator, self.block_hover_colors[self.block_index], self.indicator.get_rect(), 3)
        else:
            self.block_image = self.block_colors[self.block_index]
            pygame.draw.rect(self.indicator, self.block_image.get_at((0,0)), self.indicator.get_rect(), 3)

        # Block Hover
        self.block_hover = pygame.Surface((self.width//2, self.width//2), pygame.SRCALPHA)
        if isinstance(self.block_colors[self.block_index], tuple) == True:
            pygame.draw.rect(self.block_hover, self.block_hover_colors[self.block_index], self.block_hover.get_rect())
        else:
            self.block_image = self.block_colors[self.block_index]
            pygame.draw.rect(self.block_hover, self.block_image.get_at((0,0)), self.block_hover.get_rect())

        


    def update(self, delta_time):
        self.input()
        self.move(delta_time)
        # Update player's image based on animation and frame index
        self.image = self.animations[self.status][self.frame_index]


        self.indicator_rect = self.indicator.get_rect(center=(self.pos))
        # Update player's image size
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * self.scale_factor), int(self.image.get_height() * self.scale_factor)))

        # cursor to block
        cursor = self.mouse_block()
        self.block_hover_rect.center = cursor

        # Checking if color of the indicator is not matched with chosen color
        if self.image.get_at((0, 0)) != self.block_colors[self.block_index]:
            self.update_colors()


if __name__ == '__main__':
    # ask yousuf what main does
    game = Game()
    game.run()