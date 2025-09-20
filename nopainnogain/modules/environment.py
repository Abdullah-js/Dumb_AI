
"""import random
from typing import Dict, Tuple, List, Optional

from config import settings
from modules.utils import setup_directories
from modules.resources import Plant, Water, Mineral


class Environment:
    

    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height

        # Each cell contains resources, hazards, pollution, and agents
        self.grid: List[List[Dict]] = [
            [
                {"resources": {}, "hazards": 0, "pollution": 0.0, "agents": []}
                for _ in range(width)
            ]
            for _ in range(height)
        ]

        self.weather: str = "normal"  # could expand into a WeatherSystem later
        self._generate_terrain()

    # ──────────────────────────────────────────────
    # TERRAIN GENERATION
    # ──────────────────────────────────────────────
    def _generate_terrain(self) -> None:
        
        all_positions = [(x, y) for y in range(self.height) for x in range(self.width)]
        resource_positions = random.sample(all_positions, k=settings.INITIAL_RESOURCE_COUNT)

        for x, y in resource_positions:
            resource_type = random.choice(["plant", "water", "mineral"])
            if resource_type == "plant":
                self.grid[y][x]["resources"]["plant"] = Plant(position=(x, y))
            elif resource_type == "water":
                self.grid[y][x]["resources"]["water"] = Water(position=(x, y))
            elif resource_type == "mineral":
                self.grid[y][x]["resources"]["mineral"] = Mineral(position=(x, y))

        # Base hazards everywhere
        for y in range(self.height):
            for x in range(self.width):
                self.grid[y][x]["hazards"] = random.randint(0, settings.HAZARD_BASE_LEVEL)

    # ──────────────────────────────────────────────
    # WORLD STATE UPDATES
    # ──────────────────────────────────────────────
    def update_state(self) -> None:
        for y in range(self.height):
            for x in range(self.width):
                cell = self.grid[y][x]

                # Resource regeneration
                for resource in cell["resources"].values():
                    resource.quantity = min(
                        settings.MAX_RESOURCE_CAPACITY,
                        resource.quantity + resource.regeneration_rate,
                    )

                # Hazards increase with pollution
                cell["hazards"] = min(
                    10, cell["hazards"] + cell["pollution"] * 0.1
                )

                # Pollution naturally decays
                cell["pollution"] = max(0, cell["pollution"] - 0.5)

    # ──────────────────────────────────────────────
    # RESOURCE INTERACTIONS
    # ──────────────────────────────────────────────
    def deplete_resource(
        self, x: int, y: int, resource_type: str, amount: int
    ) -> None:
        cell = self.grid[y][x]
        if resource_type in cell["resources"]:
            resource = cell["resources"][resource_type]
            resource.quantity = max(0, resource.quantity - amount)

    def get_resource(
        self, x: int, y: int, resource_type: str
    ) -> Optional[int]:
        return (
            self.grid[y][x]["resources"][resource_type].quantity
            if resource_type in self.grid[y][x]["resources"]
            else None
        )

    def add_pollution(self, x: int, y: int, amount: float) -> None:
        self.grid[y][x]["pollution"] += amount

    # ──────────────────────────────────────────────
    # AGENT INTERACTIONS
    # ──────────────────────────────────────────────
    def place_agent(self, x: int, y: int, agent) -> None:
        self.grid[y][x]["agents"].append(agent)

    def move_agent(self, agent, old_pos: Tuple[int, int], new_pos: Tuple[int, int]) -> None:
        ox, oy = old_pos
        nx, ny = new_pos

        if agent in self.grid[oy][ox]["agents"]:
            self.grid[oy][ox]["agents"].remove(agent)
        self.grid[ny][nx]["agents"].append(agent)
"""
import random
from config import settings
from modules.utils import setup_directories
from modules.resources import Plant, Water, Mineral

class Environment:
    """
    Manages the grid-based world with multiple resource types, hazards, and pollution.
    """
    def __init__(self, width, height):
        self.width = width
        self.height = height
        # Grid cell can now contain multiple resource types
        self.grid = [[{'resources': {}, 'hazards': 0, 'pollution': 0, 'agents': []} for _ in range(width)] for _ in range(height)]
        self.weather = "normal"
        self._generate_terrain()

    def _generate_terrain(self):
        """Initializes the grid with various resources and hazards."""
        for y in range(self.height):
            for x in range(self.width):
                # Distribute resources randomly
                if random.random() < 0.3:
                    self.grid[y][x]['resources']['plant'] = Plant(position=(x, y))
                if random.random() < 0.2:
                    self.grid[y][x]['resources']['water'] = Water(position=(x, y))
                if random.random() < 0.15:
                    self.grid[y][x]['resources']['mineral'] = Mineral(position=(x, y))
                self.grid[y][x]['hazards'] = random.randint(0, 3)

    def update_state(self):
        """Updates resources and hazards based on regeneration and pollution."""
        for y in range(self.height):
            for x in range(self.width):
                # Regenerate resources
                for r_type, resource in self.grid[y][x]['resources'].items():
                    resource.quantity = min(settings.MAX_RESOURCE_CAPACITY, resource.quantity + resource.regeneration_rate)
                
                # Pollution increases hazards
                self.grid[y][x]['hazards'] = min(10, self.grid[y][x]['hazards'] + self.grid[y][x]['pollution'] * 0.1)
                
                # Decay pollution over time
                self.grid[y][x]['pollution'] = max(0, self.grid[y][x]['pollution'] - 0.5)

    def deplete_resource(self, x, y, resource_type, amount):
        """Depletes a specific resource at a cell."""
        if resource_type in self.grid[y][x]['resources']:
            self.grid[y][x]['resources'][resource_type].quantity = max(0, self.grid[y][x]['resources'][resource_type].quantity - amount)
            self.grid[y][x]['pollution'] += 1 # Action generates waste
