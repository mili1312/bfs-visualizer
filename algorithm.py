from collections import deque

def bfs(grid, start, goal, ROWS, COLS):
    queue = deque()
    queue.append(start)
    visited = set()
    visited.add(start)
    came_from = {}

    while queue:
        current = queue.popleft()
        row, col = current

        if current == goal:
            path = []
            if current not in came_from:
                break
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path

        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            r, c = row + dr, col + dc
            if 0 <= r < ROWS and 0 <= c < COLS:
                if grid[r][c] != 'wall' and (r,c) not in visited:
                    queue.append((r,c))
                    visited.add((r,c))
