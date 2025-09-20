import heapq
import math

class Pathfinder:
    """
    Implements the A* pathfinding algorithm to find the most efficient path
    for an agent to a target destination, considering environmental factors.
    """
    def __init__(self, environment):
        self.env = environment

    def find_path(self, start, end):
        """
        Finds the shortest path from a start point to an end point using A*.
        
        Args:
            start (tuple): The starting (x, y) coordinates.
            end (tuple): The target (x, y) coordinates.
            
        Returns:
            list or None: The path as a list of (x, y) coordinates, or None if no path exists.
        """
        # Priority queue: stores tuples of (f_score, g_score, coordinates)
        open_set = [(self._heuristic(start, end), 0, start)]
        
        # Dictionaries to store scores and path reconstruction
        came_from = {}
        g_score = {start: 0}
        f_score = {start: self._heuristic(start, end)}

        while open_set:
            current_f, current_g, current = heapq.heappop(open_set)

            if current == end:
                return self._reconstruct_path(came_from, current)

            for neighbor in self._get_neighbors(current):
                x, y = neighbor
                # A* cost combines travel cost (1) and hazard cost. Hazards penalize a path.
                tentative_g_score = current_g + 1 + self.env.grid[y][x]['hazards']

                if tentative_g_score < g_score.get(neighbor, float('inf')):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self._heuristic(neighbor, end)
                    heapq.heappush(open_set, (f_score[neighbor], tentative_g_score, neighbor))
                    
        return None # No path found

    def _get_neighbors(self, node):
        """Returns the valid neighbors of a given node (including diagonals)."""
        x, y = node
        neighbors = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.env.width and 0 <= ny < self.env.height:
                    neighbors.append((nx, ny))
        return neighbors

    def _heuristic(self, a, b):
        """Calculates the Manhattan distance heuristic."""
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
        
    def _reconstruct_path(self, came_from, current):
        """Reconstructs the path from the came_from dictionary."""
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        return path[::-1] # Reverse the path to get it from start to end
