import heapq

def a_star_pathfinding(start, end, grid):
    """
    Finds the shortest path from start to end using the A* algorithm.
    The cost is based on movement and hazard values.
    """
    open_list = []
    heapq.heappush(open_list, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: _heuristic(start, end)}

    while open_list:
        current = heapq.heappop(open_list)[1]

        if current == end:
            return _reconstruct_path(came_from, end)

        for neighbor in _get_neighbors(current, grid):
            tentative_g_score = g_score[current] + _cost(current, neighbor, grid)
            
            if tentative_g_score < g_score.get(neighbor, float('inf')):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + _heuristic(neighbor, end)
                heapq.heappush(open_list, (f_score[neighbor], neighbor))
    return None

def _heuristic(a, b):
    """Calculates Manhattan distance as a heuristic."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def _cost(current, neighbor, grid):
    """Calculates the cost to move to a neighbor, including hazard penalties."""
    x, y = neighbor
    hazard_penalty = grid[y][x]['hazards'] * 5
    return 1 + hazard_penalty

def _get_neighbors(position, grid):
    """Gets valid neighbors for a given position on the grid."""
    x, y = position
    neighbors = []
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < len(grid[0]) and 0 <= ny < len(grid):
            neighbors.append((nx, ny))
    return neighbors

def _reconstruct_path(came_from, current):
    """Reconstructs the path from the came_from dictionary."""
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path
