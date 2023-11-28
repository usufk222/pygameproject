import pygame
from sys import exit

pygame.init()
screen = pygame.display.set_mode((1000, 700))
pygame.display.set_caption("Block Place")
clock = pygame.time.Clock()

# Block Selection 
block_colors = [(255, 255, 0, 255), (255, 0, 0, 255), (0, 255, 0, 255), (0, 0, 255, 255)]
block_hover_colors = [(255, 255, 0, 64), (255, 0, 0, 64), (0, 255, 0, 64), (0, 0, 255, 64)]
block_index = 0

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Player Placeholder
        self.width = 40
        self.image = pygame.Surface((self.width, self.width), pygame.SRCALPHA)
        pygame.draw.rect(self.image, block_colors[block_index], (0, 0, self.width, self.width))
        self.rect = self.image.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))

        # Player placeable radius indicator
        self.usable_width = self.width * 3
        self.indicator = pygame.Surface((self.usable_width * 3, self.usable_width * 3), pygame.SRCALPHA)
        pygame.draw.rect(self.indicator, block_hover_colors[block_index], self.indicator.get_rect(), 5)
        self.indicator_rect = self.indicator.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))

        # Block Hover
        cursor = self.mouse_block()
        self.block_hover = pygame.Surface((self.width//2, self.width//2), pygame.SRCALPHA)
        pygame.draw.rect(self.block_hover, block_hover_colors[block_index], self.block_hover.get_rect())
        self.block_hover_rect = self.block_hover.get_rect(center=(cursor))

        self.update_colors()

    def mouse_block(self):
        cursor = pygame.mouse.get_pos()
        return cursor
    
    def update_colors(self):
        self.image = pygame.Surface((self.width, self.width), pygame.SRCALPHA)
        pygame.draw.rect(self.image, block_colors[block_index], (0, 0, self.width, self.width))

        self.indicator = pygame.Surface((self.usable_width * 3, self.usable_width * 3), pygame.SRCALPHA)
        pygame.draw.rect(self.indicator, block_hover_colors[block_index], self.indicator.get_rect(), 5)

        self.block_hover = pygame.Surface((self.width//2, self.width//2), pygame.SRCALPHA)
        pygame.draw.rect(self.block_hover, block_hover_colors[block_index], self.block_hover.get_rect())

    def update(self):
        cursor = self.mouse_block()
        self.block_hover_rect.center = cursor

        # Checking if color of the indicator is not matched with chosen color
        if self.image.get_at((0, 0)) != block_colors[block_index]:
            self.update_colors()

class Block(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.width = 40
        # Placed block
        self.block_placed = pygame.Surface((self.width//2, self.width//2), pygame.SRCALPHA)
        pygame.draw.rect(self.block_placed, block_colors[block_index], self.block_placed.get_rect())
        self.block_placed_rect = self.block_placed.get_rect(center=position)

# Groups
player = Player()
blocks = []

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if player.block_hover_rect.colliderect(player.indicator_rect):
                print("Block Placed")
                # Create a new block with the current position of the block_hover_rect
                new_block = Block(player.block_hover_rect.center)
                blocks.append(new_block)
        elif event.type == pygame.KEYDOWN:
            # Block Deleting key
            if event.key == pygame.K_SPACE:
                for block in blocks:
                    if block.block_placed_rect.colliderect(player.block_hover_rect):
                        print("Block Deleted")
                        blocks.remove(block)
            # Block changing keys
            elif event.key == pygame.K_1:
                block_index = 0
                print("Block changed")
            elif event.key == pygame.K_2:
                print("Block changed")
                block_index = 1
            elif event.key == pygame.K_3:
                print("Block changed")
                block_index = 2
            elif event.key == pygame.K_4:
                print("Block changed")
                block_index = 3
    screen.fill("Grey")

    screen.blit(player.image, player.rect.topleft)
    screen.blit(player.indicator, player.indicator_rect.topleft)
    if player.block_hover_rect.colliderect(player.indicator_rect):
        screen.blit(player.block_hover, player.block_hover_rect)
    for block in blocks:
        screen.blit(block.block_placed, block.block_placed_rect.topleft)
    player.update()

    pygame.display.update()
    clock.tick(60)
