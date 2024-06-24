import random
import heapq

def get_neighbors(x, y, maze, d = 2, offset = 1):
    neighbors = []
    directions = [(-d, 0), (d, 0), (0, -d), (0, d)]
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0+offset <= nx < len(maze)-offset and 0+offset <= ny < len(maze[0])-offset:
            neighbors.append((nx, ny))
    return neighbors

def remove_wall(x1, y1, x2, y2, maze):
    maze[(x1 + x2) // 2][(y1 + y2) // 2] = 0

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def randomized_dfs_maze(start, w, h):
    """
    Generate a maze using randomized depth-first search starting from a given cell.
    
    :param maze: A 2D list representing the maze where 0 is an empty space and 1 is a wall.
    :param start: A tuple (x, y) representing the starting cell for the DFS.
    """
    maze = [[1] * w for i in range(h)]
    stack = [start]
    maze[start[0]][start[1]] = 0  # Mark the starting cell as empty

    while stack:
        x, y = stack[-1]
        neighbors = get_neighbors(x, y, maze)
        unvisited_neighbors = [(nx, ny) for nx, ny in neighbors if maze[nx][ny] == 1]

        if unvisited_neighbors:
            nx, ny = random.choice(unvisited_neighbors)
            remove_wall(x, y, nx, ny, maze)
            maze[nx][ny] = 0  # Mark the neighbor cell as empty
            stack.append((nx, ny))
        else:
            stack.pop()
    return maze

def a_star(maze, start, end):
    """
    Find the shortest path in a maze using the A* algorithm from start to end.
    
    :param maze: A 2D list representing the maze where 0 is an empty space and 1 is a wall.
    :param start: A tuple (x, y) representing the starting cell.
    :param end: A tuple (x, y) representing the goal cell.
    :return: A list of cells in the path from start to end if a path exists, otherwise None.
    """
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, end)}
    
    while open_set:
        _, current = heapq.heappop(open_set)
        
        if current == end:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path
        
        for neighbor in get_neighbors(*current, maze, 1, 0):
            if maze[neighbor[0]][neighbor[1]] == 1:
                continue
            
            tentative_g_score = g_score[current] + 1
            
            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, end)
                if neighbor not in [i[1] for i in open_set]:
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))
    
    return None
