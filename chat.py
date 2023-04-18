import pygame
import random

# Set up Pygame
pygame.init()

# Set up window
WINDOW_SIZE = (400, 400)
window = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption('Circle Collector')

# Set up colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

colors = [RED, GREEN, BLUE]

# Set up font
font = pygame.font.Font(None, 36)

# Set up grid
GRID_SIZE = 8
grid = []
for i in range(GRID_SIZE):
  grid.append([])
  for j in range(GRID_SIZE):
    grid[i].append(0)

# Place circles randomly on the grid
print('place circles on grid')
num_circles = 5
for i in range(num_circles):
  circle_placed = False
  while not circle_placed:
    x = random.randint(0, GRID_SIZE - 1)
    y = random.randint(0, GRID_SIZE - 1)
    if grid[x][y] == 0:
      grid[x][y] = random.randint(1, 3)
      circle_placed = True

# Set up player
player_x = 0
player_y = 0
score = 0

# Set time limit
time_limit = 10
start_time = pygame.time.get_ticks()

print('main game loop')
# Main game loop
running = True
while running:
# Calculate time remaining
  time_remaining = time_limit - (pygame.time.get_ticks() - start_time) / 1000
  if time_remaining < 0:
     time_remaining = 0
    

  for event in pygame.event.get():
       if event.type == pygame.QUIT:
          running = False
       elif event.type == pygame.KEYDOWN:
        # Check if player has moved
         if event.key == pygame.K_LEFT and player_x > 0:
            player_x -= 1
         elif event.key == pygame.K_RIGHT and player_x < GRID_SIZE - 1:
            player_x += 1
         elif event.key == pygame.K_UP and player_y > 0:
            player_y -= 1
         elif event.key == pygame.K_DOWN and player_y < GRID_SIZE - 1:
            player_y += 1
        


    # Check if player has picked up a circle
  if grid[player_x][player_y] != 0:
        value = grid[player_x][player_y]
        score += value
        grid[player_x][player_y] = 0

  # Check if time is up
  if pygame.time.get_ticks() - start_time > time_limit * 1000:
        running = False

    # Draw grid and score
  window.fill(BLACK)
  for i in range(GRID_SIZE):
      for j in range(GRID_SIZE):
        if i == player_x and j == player_y:
           pygame.draw.circle(window, WHITE, (i * 50 + 25, j * 50 + 25), 25)
        elif grid[i][j] != 0:
           value = grid[i][j]
           pygame.draw.circle(window, colors[value-1], (i * 50 + 25, j * 50 + 25), 25)
           
  score_text = font.render(f'Score: {score}', True, WHITE)
  window.blit(score_text, (0, 0))    
  time_text = font.render(f'Time: {time_remaining:.1f}', True, WHITE)
  window.blit(time_text, (200, 0))
  pygame.display.flip()