import pygame

pygame.init()

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Moving Rectangle")

rect_2 = pygame.Rect(200, 200, 50, 50)  # Create a rectangle

clock = pygame.time.Clock()

run = True
while run:
    clock.tick(60)

    # Fill the background white
    screen.fill((255, 255, 255))

    # Player controls
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        rect_2.x -= 5
    if keys[pygame.K_d]:
        rect_2.x += 5
    if keys[pygame.K_w]:
        rect_2.y -= 5
    if keys[pygame.K_s]:
        rect_2.y += 5

    # Draw the rectangle
    pygame.draw.rect(screen, (0, 255, 255), rect_2)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.flip()

pygame.quit()
