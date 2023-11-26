import pygame
from sys import exit

from pygame.sprite import Group

pygame.init()
screen = pygame.display.set_mode((1000, 700))
pygame.display.set_caption("Block Place")
clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Player PLaceholder
        self.width = 40
        self.image = pygame.Surface((self.width, self.width), pygame.SRCALPHA)
        pygame.draw.rect(self.image, (255, 255, 0, 255), (0, 0, self.width, self.width))
        self.rect = self.image.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))

        # Player placeable radius indicator
        self.usable_width = self.width * 3
        self.indicator = pygame.Surface((self.usable_width * 3, self.usable_width * 3), pygame.SRCALPHA)
        pygame.draw.rect(self.indicator, (255, 255, 0, 64), self.indicator.get_rect(), 5)
        self.indicator_rect = self.indicator.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))

        # Block Hover
        cursor = self.mouse_block()
        self.block_hover = pygame.Surface((self.width//2, self.width//2), pygame.SRCALPHA)
        pygame.draw.rect(self.block_hover, (255, 255, 0, 64), self.block_hover.get_rect())
        self.block_hover_rect = self.block_hover.get_rect(center=(cursor))

        # Placed block
        self.block_placed = pygame.Surface((self.width//2, self.width//2), pygame.SRCALPHA)
        pygame.draw.rect(self.block_placed, (255, 255, 0), self.block_placed.get_rect())
        self.block_placed_rect = self.block_placed.get_rect(center=(cursor))
    def mouse_block(self):
        cursor = pygame.mouse.get_pos()
        return cursor

    def update(self):
        cursor = self.mouse_block()
        self.block_hover_rect.center = cursor
# Groups
player = Player()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if player.block_hover_rect.colliderect(player.indicator_rect):
                print("Block Placed")
                player.block_placed_rect = player.block_hover_rect.copy()

    screen.fill("Grey")

    screen.blit(player.image, player.rect.topleft)
    screen.blit(player.indicator, player.indicator_rect.topleft)
    if player.block_hover_rect in player.indicator_rect:
        screen.blit(player.block_hover, player.block_hover_rect)
    if player.block_placed_rect.colliderect(player.indicator_rect):
        screen.blit(player.block_placed, player.block_placed_rect.topleft)
    player.update()

    pygame.display.update()
    clock.tick(60)