"""import random
import uuid
from config import constants, settings
from modules.resources import Plant, Water, Mineral

class Agent:
   
    def _get_color_from_species_id(self):
        # Use the fixed color from settings, or a default random one for other species.
        if self.species_id == "prey":
            return settings.COLORS["prey"]
        elif self.species_id == "predator":
            return settings.COLORS["predator"]
        # A simple way to generate a unique color based on species_id
        # This ensures all agents in the same species have the same color
        random.seed(str(self.species_id))
        r = random.randint(50, 255)
        g = random.randint(50, 255)
        b = random.randint(50, 255)
        random.seed(None) # Reset the seed so other random operations aren't affected
        return (r, g, b)

    def __init__(self, name, health=constants.MAX_HEALTH, energy=constants.MAX_ENERGY, genome=None, species_id=None, position=None, generation=0):
        self.name = name
        self.id = uuid.uuid4()
        self.health = health
        self.energy = energy
        self.position = position if position else (0, 0)
        self.generation = generation
        self.alive = True
        self.age = 0
        self.species_id = species_id if species_id else self.id
        self.group_id = None
        self.state = "FORAGING"
        self.genome = genome if genome else [random.randint(0, 10) for _ in range(settings.GENOME_LENGTH)]
        self.traits = self._express_phenotype()
        self.color = self._get_color_from_species_id() # Assign color on initialization
        
    def _express_phenotype(self):
      
        traits = {
            # Simple mapping from genome to traits
            'speed': self.genome[0] / 10.0,
            'intelligence': self.genome[1] / 10.0,
            'aggression': self.genome[2] / 10.0,
            'cooperation': self.genome[3] / 10.0,
            'pollution_tolerance': self.genome[4] / 10.0,
        }
        return traits

    def decide_action(self, environment, rl_engine):
     
        # Get the current state
        state = rl_engine.get_state(self, environment)
        
        # Corrected line: Call the proper method from the decision engine
        action = rl_engine.get_action(self, state, constants.ACTIONS)
        
        return action


    def perform_action(self, action, environment):
      
        self.age += 1
        self.energy -= settings.ENERGY_LOSS_PER_MOVE
        
        if action == "move":
            self._move(random.choice(["up", "down", "left", "right"]), environment)
        elif action == "eat":
            self._eat(environment)
        # Other actions would be implemented here
    
    def _move(self, direction, environment):
      
        x, y = self.position
        dx, dy = 0, 0
        if direction == "up": dy = -1
        elif direction == "down": dy = 1
        elif direction == "left": dx = -1
        elif direction == "right": dx = 1

        new_x = max(0, min(environment.width - 1, x + dx))
        new_y = max(0, min(environment.height - 1, y + dy))
        self.position = (new_x, new_y)

    def _eat(self, environment):
        
        x, y = self.position
        # Find a suitable resource to eat
        if "plant" in environment.grid[y][x]['resources']:
            resource = environment.grid[y][x]['resources']['plant']
            # Use nutritional_value as the amount to consume
            gathered = min(self.traits['intelligence'], resource.nutritional_value)
            self.energy += gathered
            environment.deplete_resource(x, y, "plant", gathered)
            self.energy = min(self.energy, constants.MAX_ENERGY)
            return True
        return False
        
    def _eat_prey(self, prey_agent):
        
        
        if self.species_id == "predator" and prey_agent.species_id == "prey":
            self.energy += prey_agent.health / 2  # Predator gains energy
            prey_agent.health = 0
            prey_agent.alive = False
            self.energy = min(self.energy, constants.MAX_ENERGY)
            return True
        return False
        
    def check_status(self):
     
        if self.health <= 0 or self.energy <= constants.MIN_ENERGY:
            self.alive = False

    def reset(self):

        self.health = constants.MAX_HEALTH
        self.energy = constants.MAX_ENERGY
        self.position = (random.randint(0, settings.GRID_WIDTH - 1), random.randint(0, settings.GRID_HEIGHT - 1))
        self.alive = True
        self.age = 0"""
# agent.py
"""
import random
import uuid
from config import constants, settings
from modules.resources import Plant, Water, Mineral

class Agent:

    def __init__(self, name, health=constants.MAX_HEALTH, energy=constants.MAX_ENERGY,
                 genome=None, species_id=None, position=None, generation=0):
        self.name = name
        self.id = uuid.uuid4()
        self.health = health
        self.energy = energy
        self.position = position if position else (random.randint(0, settings.GRID_WIDTH-1),
                                                   random.randint(0, settings.GRID_HEIGHT-1))
        self.generation = generation
        self.alive = True
        self.age = 0
        self.species_id = species_id if species_id else "prey"
        self.group_id = None
        self.state = "FORAGING"

        # Genome & traits
        gl = getattr(settings, "GENOME_LENGTH", 7)
        self.genome = genome if genome else [random.randint(0, 10) for _ in range(gl)]
        self.traits = self._express_phenotype()

        # Visuals
        self.color = self._get_color_from_species_id()

    # -------------------- internal helpers --------------------

    def _get_color_from_species_id(self):
        if self.species_id == "prey":
            return settings.COLORS["prey"]
        if self.species_id == "predator":
            return settings.COLORS["predator"]
        random.seed(str(self.species_id))
        r, g, b = random.randint(50, 255), random.randint(50, 255), random.randint(50, 255)
        random.seed(None)
        return (r, g, b)

    def _gene(self, idx, default=5):
        try:
            return self.genome[idx]
        except Exception:
            return default

    def _express_phenotype(self):
        speed = self._gene(0) / 10.0
        intelligence = self._gene(1) / 10.0
        aggression = self._gene(2) / 10.0
        cooperation = self._gene(3) / 10.0
        pollution_tolerance = self._gene(4) / 10.0
        raw_rep = self._gene(5, 3) / 10.0
        reproduction_rate = max(0.01, min(0.6, 0.02 + raw_rep))
        lifespan = 80 + self._gene(6, 5) * 20
        return {
            "speed": speed,
            "intelligence": intelligence,
            "aggression": aggression,
            "cooperation": cooperation,
            "pollution_tolerance": pollution_tolerance,
            "reproduction_rate": reproduction_rate,
            "lifespan": lifespan,
        }

    # -------------------- behavior --------------------

    def decide_action(self, environment, rl_engine):
    
        if not self.alive:
            return None

        x, y = self.position
        cell = environment.grid[y][x]

        # Avoid deadly hazards
        if cell['hazards'] > self.traits['pollution_tolerance'] * 10:
            return "move"

        # Predator-prey logic
        if self.species_id == "predator":
            prey = [a for a in cell.get('agents', []) if a.species_id == "prey" and a.alive]
            if prey:
                return "hunt"

        # Check for resources
        best_resource = None
        max_value = -1
        for r_type, res in cell['resources'].items():
            if getattr(res, "quantity", 0) > max_value:
                max_value = getattr(res, "quantity", 0)
                best_resource = r_type

        if best_resource == "plant":
            return "eat"
        elif best_resource == "water":
            return "drink"
        elif best_resource == "mineral":
            return "mine"

        # Otherwise: move randomly
        return random.choice(constants.ACTIONS_MOVE)

    def perform_action(self, action, environment):
        if not self.alive or action is None:
            return

        # Base metabolic cost
        self.energy -= getattr(settings, "ENERGY_LOSS_PER_MOVE", 1)
        if self.energy <= constants.MIN_ENERGY:
            self.alive = False
            return

        # Action handling
        if action == "move":
            self._move(random.choice(constants.ACTIONS_MOVE), environment)
        elif action == "eat":
            self._eat(environment)
        elif action == "drink":
            self._drink(environment)
        elif action == "mine":
            self._mine(environment)
        elif action == "hunt":
            self._hunt(environment)
        elif action == "rest":
            self.energy = min(constants.MAX_ENERGY, self.energy + 1)

    # -------------------- action helpers --------------------

    def _move(self, direction, environment):
        x, y = self.position
        dx, dy = 0, 0
        if direction == "up": dy = -1
        if direction == "down": dy = 1
        if direction == "left": dx = -1
        if direction == "right": dx = 1
        new_x = max(0, min(environment.width - 1, x + dx))
        new_y = max(0, min(environment.height - 1, y + dy))
        self.position = (new_x, new_y)

    def _eat(self, environment):
        x, y = self.position
        cell = environment.grid[y][x]
        plant = cell['resources'].get('plant')
        if plant and getattr(plant, "quantity", 0) > 0:
            gathered = min(self.traits["intelligence"]*2.0, plant.nutritional_value)
            self.energy = min(constants.MAX_ENERGY, self.energy + gathered)
            environment.deplete_resource(x, y, "plant", gathered)
            return True
        return False

    def _drink(self, environment):
        x, y = self.position
        cell = environment.grid[y][x]
        water = cell['resources'].get('water')
        if water and getattr(water, "quantity", 0) > 0:
            self.energy = min(constants.MAX_ENERGY, self.energy + 5)
            environment.deplete_resource(x, y, "water", 1)
            return True
        return False

    def _mine(self, environment):
        x, y = self.position
        cell = environment.grid[y][x]
        mineral = cell['resources'].get('mineral')
        if mineral and getattr(mineral, "quantity", 0) > 0:
            self.energy = min(constants.MAX_ENERGY, self.energy + 2)
            environment.deplete_resource(x, y, "mineral", 1)
            return True
        return False

    def _hunt(self, environment):
        x, y = self.position
        cell = environment.grid[y][x]
        prey_list = [a for a in cell.get('agents', []) if a.species_id == "prey" and a.alive]
        if prey_list:
            prey = random.choice(prey_list)
            self.energy = min(constants.MAX_ENERGY, self.energy + prey.health/2.0)
            prey.alive = False
            prey.health = 0
            return True
        return False

    # -------------------- status & lifecycle --------------------

    def check_status(self):
        if self.health <= 0 or self.energy <= constants.MIN_ENERGY or self.age >= self.traits.get("lifespan", 200):
            self.alive = False

    def reset(self):
        self.health = constants.MAX_HEALTH
        self.energy = constants.MAX_ENERGY
        self.position = (random.randint(0, settings.GRID_WIDTH-1),
                         random.randint(0, settings.GRID_HEIGHT-1))
        self.alive = True
        self.age = 0
"""
import random
import uuid
from config import constants, settings

class Agent:
    """
    Represents an autonomous agent with a genome, phenotype, and social state.
    """
    def _get_color_from_species_id(self):
        # A simple way to generate a unique color based on species_id
        # This ensures all agents in the same species have the same color
        random.seed(str(self.species_id))
        r = random.randint(50, 255)
        g = random.randint(50, 255)
        b = random.randint(50, 255)
        random.seed(None) # Reset the seed so other random operations aren't affected
        return (r, g, b)

    def __init__(self, name, health=constants.MAX_HEALTH, energy=constants.MAX_ENERGY, genome=None, species_id=None, position=None, generation=0):
        self.name = name
        self.id = uuid.uuid4()
        self.health = health
        self.energy = energy
        self.position = position if position else (0, 0)
        self.generation = generation
        self.alive = True
        self.age = 0
        self.species_id = species_id if species_id else self.id
        self.group_id = None
        self.state = "FORAGING"
        self.genome = genome if genome else [random.uniform(1.0, 10.0) for _ in range(settings.GENOME_LENGTH)]
        self.traits = self._express_phenotype()
        self.color = self._get_color_from_species_id()

    def _express_phenotype(self):
        """
        Maps the agent's genetic code (genome) to a set of expressible traits (phenotype).
        This is a simple linear mapping for demonstration.
        """
        # Ensure the genome is long enough to express all traits
        if len(self.genome) < 6:
            # Handle cases where genome is too short, perhaps from initial creation
            # or legacy data. A simple solution is to extend it with random values.
            self.genome.extend([random.uniform(1.0, 10.0) for _ in range(6 - len(self.genome))])

        return {
            'speed': self.genome[0],
            'intelligence': self.genome[1],
            'aggression': self.genome[2],
            'cooperation': self.genome[3],
            'pollution_tolerance': self.genome[4],
            'reproduction_rate': self.genome[5],  # Mapped to a specific gene
        }
    
    def perform_action(self, action, environment):
        """Performs an action, modifying the agent's state."""
        if action == "move":
            self._move(random.choice(["move_up", "move_down", "move_left", "move_right"]), environment)
        elif action == "eat":
            self._eat(environment)
        # Other actions would be implemented here
    
    def _move(self, direction, environment):
        """Moves the agent in a specified direction."""
        x, y = self.position
        dx, dy = 0, 0
        if direction == "move_up": dy = -1
        elif direction == "move_down": dy = 1
        elif direction == "move_left": dx = -1
        elif direction == "move_right": dx = 1

        new_x = max(0, min(environment.width - 1, x + dx))
        new_y = max(0, min(environment.height - 1, y + dy))
        self.position = (new_x, new_y)
        self.energy -= self.traits['speed'] / 10

    def _eat(self, environment):
        """Consumes a resource at the current location."""
        x, y = self.position
        # Find a suitable resource to eat
        if "plant" in environment.grid[y][x]['resources']:
            resource = environment.grid[y][x]['resources']['plant']
            # Use nutritional_value as the amount to consume
            gathered = min(self.traits['intelligence'], resource.nutritional_value)
            self.energy += gathered
            environment.deplete_resource(x, y, "plant", gathered)
            self.energy = min(self.energy, constants.MAX_ENERGY)
            return True
        return False
    
    def check_status(self):
        """Checks agent health and energy."""
        if self.energy <= settings.MIN_ENERGY:
            self.alive = False
            self.state = "DEAD"
        if self.age >= settings.MAX_AGE:
            self.alive = False
            self.state = "DEAD"
