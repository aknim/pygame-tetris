import pygame
import sys
import random

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

# Tetromino shapes
SHAPES = [
    # I-shape
    [[1, 1, 1, 1],
     [0, 0, 0, 0],
     [0, 0, 0, 0],
     [0, 0, 0, 0]],

     # O-shape
     [[1, 1],
      [1, 1]],

     # T-Shape
     [[0, 1, 0], 
      [1, 1, 1],
      [0, 0, 0]],

     # S-shape
     [[0, 1, 1], 
      [1, 1, 0],
      [0, 0, 0]],

     # Z-shape
     [[1, 1, 0],
      [0, 1, 1],
      [0, 0, 0]],

     # J-shape
     [[1, 0, 0],
      [1, 1, 1],
      [0, 0, 0]],

     # L-shape
     [[0, 0, 1],
      [1, 1, 1],
       [0, 0, 0]]
]

# Tetromino colors (optional for visual differentiation)
SHAPE_COLORS = [
    (0, 255, 255),  # Cyan for I-shape
    (255, 255, 0),  # Yellow For O-shape
    (128, 0, 128),  # Purple for T-shape
    (0, 255, 0),    # Green for S-shape
    (255, 0, 0),    # Red for Z-shape
    (0, 0, 255),    # Blue for J-shape
    (255, 165, 0)   # Orange for L-shape
]

class Tetromino:
    def __init__(self, shape_index):
        self.shape = SHAPES[shape_index] # List of all rotation states for this shape
        self.color = SHAPE_COLORS[shape_index]
        # self.rotation = 0
        self.x = COLS // 2 - len(self.shape[0]) // 2 
        self.y = 0

    def rotate(self):
        # self.rotation = (self.rotation + 1) % len(self.shapes)
        #self.shape = SHAPES[self.rotation]
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

# Function to create a new random Tetromino
def create_tetromino():
    shape_index = random.randint(0, len(SHAPES) - 1) 
    return Tetromino(shape_index)

# Initialize the current Tetromino
current_tetromino = create_tetromino()

# Main game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                current_tetromino.x -= 1 # Move left
            elif event.key == pygame.K_RIGHT:
                current_tetromino.x += 1 # Move right
            elif event.key == pygame.K_DOWN:
                current_tetromino.y += 1 # Move down
            elif event.key == pygame.K_UP:
                current_tetromino.rotate() # Rotate the piece
    
    # Render the current Tetromino
    for y, row in enumerate(current_tetromino.shape): # index, val
        # print(current_tetromino.rotation, y, row)
        for x, cell in enumerate(row): # index, val
            # print("r, x, ce",row, x, cell)
            if cell:
                pygame.draw.rect(screen, current_tetromino.color,
                ((current_tetromino.x + x) * GRID_SIZE,
                 (current_tetromino.y + y) * GRID_SIZE,
                 GRID_SIZE, GRID_SIZE))
    # input()

    # Refresh display
    pygame.display.flip()

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