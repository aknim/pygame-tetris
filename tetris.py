import pygame
import sys

# Initialize Pygame
pygame.init()

# Game constants
WIDTH, HEIGHT = 300, 600 # Tetris playfield size
GRID_SIZE = 30 # Size of each square in the grid
ROWS, COLS = HEIGHT // GRID_SIZE, WIDTH // GRID_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

# Set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tetris')
running = True

# Main game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen
    screen.fill(BLACK)

    # Draw the grid
    for row in range(ROWS):
        for col in range(COLS):
            pygame.draw.rect(screen, GRAY, (col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()