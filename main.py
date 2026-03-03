import pygame
from collections import deque
import random
import time

# Colors
WHITE = (255,255,255)
BLACK = (0,0,0)
GREY = (200,200,200)
GREEN = (0,255,0)
RED = (255,0,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
LIGHT_BLUE = (173,216,230)

# Grid settings
WIDTH, HEIGHT = 600, 600
ROWS, COLS = 20, 20
CELL_SIZE = WIDTH // COLS

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("BFS Animation with Timer")
font = pygame.font.SysFont(None, 32)

# Create grid
def create_grid():
    grid = [['empty' for _ in range(COLS)] for _ in range(ROWS)]
    start = (0,0)
    goal = (ROWS-1, COLS-1)
    grid[start[0]][start[1]] = 'start'
    grid[goal[0]][goal[1]] = 'goal'

    # Static walls
    for i in range(3,17):
        grid[5][i] = 'wall'
        grid[15][i] = 'wall'
    for i in range(2,18):
        grid[i][7] = 'wall'
        grid[i][12] = 'wall'

    # Random walls
    for _ in range(50):
        r = random.randint(0,ROWS-1)
        c = random.randint(0,COLS-1)
        if (r,c) not in [start, goal]:
            grid[r][c] = 'wall'

    return grid, start, goal

grid_data, start_pos, goal_pos = create_grid()

# Draw grid
def draw_grid():
    for r in range(ROWS):
        for c in range(COLS):
            rect = pygame.Rect(c*CELL_SIZE,r*CELL_SIZE,CELL_SIZE,CELL_SIZE)
            cell = grid_data[r][c]
            color = WHITE
            if cell=='start': color = GREEN
            elif cell=='goal': color = RED
            elif cell=='wall': color = BLUE
            elif cell=='visited': color = LIGHT_BLUE
            elif cell=='path': color = YELLOW
            pygame.draw.rect(screen,color,rect)
            pygame.draw.rect(screen,GREY,rect,1)

# Popup
def show_popup():
    popup_rect = pygame.Rect(100,200,400,200)
    while True:
        pygame.draw.rect(screen,BLACK,popup_rect)
        pygame.draw.rect(screen,WHITE,popup_rect,3)
        line1 = font.render("Βρέθηκε διαδρομή!",True,WHITE)
        line2 = font.render("Θέλεις να ξαναπαίξεις;",True,WHITE)
        line3 = font.render("Enter = Ναι | Esc = Όχι",True,WHITE)
        screen.blit(line1,(popup_rect.x+60,popup_rect.y+40))
        screen.blit(line2,(popup_rect.x+50,popup_rect.y+80))
        screen.blit(line3,(popup_rect.x+45,popup_rect.y+130))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type==pygame.QUIT: pygame.quit(); exit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_RETURN: return True
                if event.key==pygame.K_ESCAPE: return False

# BFS generator
def bfs_generator(grid,start,goal):
    queue = deque([start])
    visited = set([start])
    came_from = {}
    while queue:
        r,c = queue.popleft()
        if (r,c)==goal:
            path=[]
            curr = goal
            while curr!=start:
                path.append(curr)
                curr = came_from[curr]
            path.reverse()
            for pr,pc in path:
                if grid[pr][pc] not in ('start','goal'):
                    grid[pr][pc]='path'
                    yield
            return True
        if grid[r][c] not in ('start','goal'):
            grid[r][c]='visited'
            yield
        for dr,dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nr,nc = r+dr,c+dc
            if 0<=nr<ROWS and 0<=nc<COLS:
                if (nr,nc) not in visited and grid[nr][nc] not in ('wall','visited'):
                    queue.append((nr,nc))
                    visited.add((nr,nc))
                    came_from[(nr,nc)] = (r,c)
    return False

# Main loop
running = True
bfs_gen = None
start_time = None
elapsed_time = 0

while running:
    for event in pygame.event.get():
        if event.type==pygame.QUIT: running=False
        elif event.type==pygame.KEYDOWN:
            if event.key==pygame.K_SPACE:
                bfs_gen = bfs_generator(grid_data,start_pos,goal_pos)
                start_time = time.time()
            elif event.key==pygame.K_r:
                grid_data, start_pos, goal_pos = create_grid()
                bfs_gen = None
                start_time = None
                elapsed_time = 0

    # BFS animation
    if bfs_gen is not None:
        try:
            next(bfs_gen)
            # Update timer live
            if start_time is not None:
                elapsed_time = time.time()-start_time
        except StopIteration:
            bfs_gen=None
            if start_time is not None:
                elapsed_time = time.time()-start_time
            # Show popup
            replay = show_popup()
            if replay:
                grid_data, start_pos, goal_pos = create_grid()
                bfs_gen = None
                start_time = None
                elapsed_time = 0
            else:
                pygame.quit()
                exit()

    # Draw
    screen.fill(BLACK)
    draw_grid()
    # Draw timer live
    if start_time is not None:
        time_text = font.render(f"Time: {elapsed_time:.2f}s",True,WHITE)
        screen.blit(time_text,(WIDTH-150,10))
    pygame.display.flip()
    pygame.time.delay(40)

pygame.quit()
