import pygame
import sys
import random

# Initialize Pygame
pygame.init()
pygame.font.init()
font = pygame.font.Font(None, 36)

# Game constants
WIDTH, HEIGHT = 300, 600 # Tetris playfield size
GRID_SIZE = 30 # Size of each square in the grid
ROWS, COLS = HEIGHT // GRID_SIZE, WIDTH // GRID_SIZE
grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

# Set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tetris')
running = True

# Intialize the clock
clock = pygame.time.Clock()
fall_speed = 500 # Speed in milliseconds for piece to move down

# Keep track of time elapsed
last_fall_time = pygame.time.get_ticks()

score = 0
add_score = 0

# Tetromino shapes
SHAPES = [
    # Empty
    [],
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
COLORS = [
    (128, 128, 128),# Gray for empty (not used)
    (0, 255, 255),  # Cyan for I-shape
    (255, 255, 0),  # Yellow For O-shape
    (128, 0, 128),  # Purple for T-shape
    (0, 255, 0),    # Green for S-shape
    (255, 0, 0),    # Red for Z-shape
    (0, 0, 255),    # Blue for J-shape
    (255, 165, 0),   # Orange for L-shape
    (255, 255, 255), # White
    (0, 0, 0)       # Black
]

class Tetromino:
    def __init__(self, shape_index):
        self.index = shape_index
        self.shape = SHAPES[shape_index] # List of all rotation states for this shape
        self.color = COLORS[shape_index]
        # self.rotation = 0
        self.x = COLS // 2 - len(self.shape[0]) // 2 
        self.y = 0

    def rotate(self, dxn=1):
        # self.rotation = (self.rotation + 1) % len(self.shapes)
        #self.shape = SHAPES[self.rotation]
        if dxn:
            self.shape = [list(row) for row in zip(*self.shape[::-1])]
        else:
            self.shape = [list(row) for row in zip(*self.shape)][::-1]

    
def calculate_score(lines_cleared):
    global score, add_score
    if lines_cleared == 1:
        add_score = 40
    elif lines_cleared == 2:
        add_score = 100
    elif lines_cleared == 3:
        add_score = 300
    elif lines_cleared == 4: # "Tetris"
        add_score = 1200
    score += add_score


def draw_score(screen, score):
    score_surface = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_surface, (10, 10))



# Function to create a new random Tetromino
def create_tetromino():
    shape_index = random.randint(1, len(SHAPES) - 1) 
    return Tetromino(shape_index)

def check_collision(tetromino, grid, offset=(0, 0)):
    offset_x, offset_y = offset
    for y, row in enumerate(tetromino.shape):
        for x, cell in enumerate(row):
            if cell:
                grid_x = tetromino.x + x + offset_x
                grid_y = tetromino.y + y + offset_y
                # Check boundaries (left, right, bottom)
                if grid_x < 0 or grid_x >= COLS or grid_y >= ROWS:
                    return True
                # Check if the tetromino overlaps with any locked cells
                if grid_y >= 0 and grid[grid_y][grid_x]:
                    return True
    return False

def lock_piece(tetromino, grid):
    for y, row in enumerate(tetromino.shape):
        for x, cell in enumerate(row):
            if cell:
                grid[tetromino.y + y][tetromino.x + x] = tetromino.index
    # After locking, check for line clears
    return clear_lines(grid)

def clear_lines(grid):
    new_grid = [row for row in grid if any(cell == 0 for cell in row)]
    ones = [y for y in range(ROWS) if not any(cell == 0 for cell in grid[y])]
    calculate_score(len(ones))
    if ones:
        blink_lines(grid, ones)
    cleared_lines = ROWS - len(new_grid)

    # Add empty rows at the top to fill the cleared space
    for _ in range(cleared_lines):
        new_grid.insert(0, [0] * COLS)

    return new_grid, cleared_lines

def blink_lines(grid, ones, color=len(COLORS)-2):
    """Temporarily highlight full lines before clearing them."""
    global add_score, font
    for _ in range(3): # Number of blinks
        for y in ones:
            score_y = y
            grid[y] = [color] * COLS # Set the full line to the blinking color
        for row in range(ROWS):
            for col in range(COLS):
                pygame.draw.rect(screen, GRAY, (col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)
                if grid[row][col]:
                    pygame.draw.rect(screen, COLORS[grid[row][col]],
                    ((col) * GRID_SIZE,
                    (row) * GRID_SIZE,
                    GRID_SIZE, GRID_SIZE))
        score_surface = font.render(f"+{add_score}", True, (255, 255, 255))
        screen.blit(score_surface, (score_y, 50))
        pygame.display.update()
        pygame.time.delay(150) # Delay in milliseconds
        

        for y in ones:
            grid[y] = [color+1] * COLS # Set the full line to the blinking color
        for row in range(ROWS):
            for col in range(COLS):
                pygame.draw.rect(screen, GRAY, (col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)
                if grid[row][col]:
                    pygame.draw.rect(screen, COLORS[grid[row][col]],
                    ((col) * GRID_SIZE,
                    (row) * GRID_SIZE,
                    GRID_SIZE, GRID_SIZE))
        pygame.display.update()
        pygame.time.delay(150) # Delay in milliseconds

    add_score = 0



# Initialize the current Tetromino
current_tetromino = create_tetromino()

# Main game loop
while running:
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                input()
            if event.key == pygame.K_LEFT and not check_collision(current_tetromino, grid, offset=(-1, 0)):
                current_tetromino.x -= 1 # Move left
            elif event.key == pygame.K_RIGHT and not check_collision(current_tetromino, grid, offset=(1, 0)):
                current_tetromino.x += 1 # Move right
            elif event.key == pygame.K_DOWN and not check_collision(current_tetromino, grid, offset=(0, 1)):
                current_tetromino.y += 1 # Move down
            elif event.key == pygame.K_UP:
                current_tetromino.rotate() # Rotate the piece
                if check_collision(current_tetromino, grid, offset=(0, 0)):
                    current_tetromino.rotate(dxn=0)
    
    # Render the current Tetromino
    for y, row in enumerate(current_tetromino.shape): # index, val
        for x, cell in enumerate(row): # index, val
            if cell:
                pygame.draw.rect(screen, current_tetromino.color,
                ((current_tetromino.x + x) * GRID_SIZE,
                 (current_tetromino.y + y) * GRID_SIZE,
                 GRID_SIZE, GRID_SIZE))
    
    # Check if it's time to move the piece down
    if current_time - last_fall_time > fall_speed:
        if not check_collision(current_tetromino, grid, offset=(0, 1)):
            current_tetromino.y += 1 # Move piece down if no collision
        else:
            # Lock if collision detected
            grid, lines_cleared = lock_piece(current_tetromino, grid)
            
            # Spawn a new piece
            current_tetromino = create_tetromino()
            # End game condition
            if check_collision(current_tetromino, grid):
                running = False
        last_fall_time = current_time

    draw_score(screen, score)
    # Refresh display
    pygame.display.flip()
    clock.tick(60) 

    # Fill the screen
    screen.fill(BLACK)

    # Draw the grid
    for row in range(ROWS):
        for col in range(COLS):
            pygame.draw.rect(screen, GRAY, (col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)
            if grid[row][col]:
                pygame.draw.rect(screen, COLORS[grid[row][col]],
                ((col) * GRID_SIZE,
                 (row) * GRID_SIZE,
                 GRID_SIZE, GRID_SIZE))

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()