# Simulation Parameters
GRID_WIDTH = 50
GRID_HEIGHT = 100
MAX_STEPS = 1000

# Agent starting populations
INITIAL_PREY_POPULATION = 100
INITIAL_PREDATOR_POPULATION = 10
INITIAL_RESOURCE_COUNT = 500

# Reinforcement Learning Settings
LEARNING_RATE = 0.1
DISCOUNT_FACTOR = 0.95
MAX_EXPLORATION_RATE = 1.0
MIN_EXPLORATION_RATE = 0.01
EXPLORATION_DECAY = 0.995

# Resource Attributes
MAX_RESOURCE_CAPACITY = 1000
REWARD_MOVE_TO_RESOURCE = 2
REWARD_GATHER = 5
PENALTY_FAILED_ACTION = 2               
PLANT_NUTRITIONAL_VALUE = 25
WATER_NUTRITIONAL_VALUE = 15
MINERAL_NUTRITIONAL_VALUE = 5
PLANT_REGEN_RATE = 2
WATER_REGEN_RATE = 5
MINERAL_REGEN_RATE = 1
# Genetic and Evolutionary Parameters
GENOME_LENGTH = 10 
MAX_AGE = 100
REPRODUCTION_ENERGY_THRESHOLD = 75
GENETIC_DISTANCE_THRESHOLD = 3.0
MUTATION_PROBABILITY = 0.1  
MUTATION_RATE = 0.05
MUTATION_STRENGTH = 1.0
VICTORY_POPULATION = 10000000000000
SPECIATION_THRESHOLD = 5.0
REPRODUCTION_RATE = 0.1
HAZARD_BASE_LEVEL = 5  
# Default starting hazards on grid cells

# Actions for agents (to match your Agent._move)
ACTIONS = ["move", "reproduce", "eat", "fight"]
ACTIONS_MOVE = ["up", "down", "left", "right"]

# Core Agent Attributes (already mostly in your file)
MAX_HEALTH = 19000
MAX_ENERGY = 100
MIN_ENERGY = 0

# Visualization
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
TILE_SIZE = 20
FPS = 60 # Slower for better visibility

# Color Palette
COLORS = {
    "background": (20, 20, 30), # Dark blue-grey
    "grid_line": (50, 50, 70), # Slightly lighter grid lines
    "resource_plant": (30, 150, 60), # Lush green
    "resource_water": (60, 100, 200), # Deep blue
    "resource_mineral": (150, 150, 150), # Grey
    "hazard": (200, 50, 50), # Red for danger
    "agent_prey": (255, 255, 100), # Yellow-ish for prey
    "agent_predator": (255, 100, 100), # Red-ish for predators
    "energy_bar_full": (0, 255, 0), # Green
    "energy_bar_low": (255, 0, 0), # Red
}

# Agent Status
MIN_ENERGY = 0
# Base hazard level for terrain initializationp
PENALTY_MOVE_TO_HAZARD = 5
PENALTY_FAILED_ACTION = 2   
# config/settings.py

# ... other settings

COLORS = {
    # Existing colors
    "black": (0, 0, 0),
    "white": (255, 255, 255),
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "background": (20, 20, 20),
    
    # Add this line to fix the error
    "ground": (100, 75, 50), 
    
    # Other colors
    "prey": (0, 200, 0),
    "predator": (200, 0, 0),
    "horns": (100, 100, 100),
    "resource_plant": (34, 139, 34),
    "resource_water": (0, 191, 255),
    "resource_mineral": (169, 169, 169),
    "hazard": (255, 69, 0),
    "death_particle": (255, 0, 0),
}
# config/settings.py

# ... other settings

# --- Environment & Hazard Settings ---
MAX_HAZARD_VALUE = 100 # Add this line
HAZARD_DECAY_RATE = 0.95

