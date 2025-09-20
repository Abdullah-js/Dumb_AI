import os

# Project paths
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
LOG_DIR = os.path.join(DATA_DIR, "logs")
REPORTS_DIR = os.path.join(DATA_DIR, "reports")

# Log files
SIMULATION_LOG = os.path.join(DATA_DIR, "simulation_logs.csv")
SPECIES_LOG = os.path.join(DATA_DIR, "species_logs.csv")
REWARDS_LOG = os.path.join(DATA_DIR, "rewards_logs.csv")

# Q-table
Q_TABLE_PATH = os.path.join(DATA_DIR, "q_table.npy")
# constants.py

# --- Core Simulation Parameters ---
# Maximum values for agent attributes
MAX_HEALTH = 100
MAX_ENERGY = 100
MIN_ENERGY = 0

# --- Agent-related Constants ---
# A list of all possible actions an agent can take.
# Used by the decision engine and action handlers.
ACTIONS = ["move", "eat", "rest"]
ACTIONS_MOVE = ["up", "down", "left", "right"]

# --- Environment Constants ---
# Types of resources and hazards that can exist in the environment.
# These are used for logic and visualization.
RESOURCE_TYPES = ["plant", "water", "mineral"]
HAZARD_TYPES = ["pollution"]

# --- Genetic Constants ---
# The total number of genes in an agent's genome.
GENOME_LENGTH = 7

# --- File Paths and Directories ---
# A centralized location for all log files and saved data.
LOG_DIR = "logs/"

# --- Visualization Constants ---
# The size of a single grid cell in pixels.
TILE_SIZE = 40

# config/settings.py

# ... other settings

COLORS = {
    # Basic colors
    "black": (0, 0, 0),
    "white": (255, 255, 255),
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "background": (20, 20, 20),
    
    # New: Add the 'ground' color
    "ground": (100, 75, 50), # A brown color for the ground
    
    # Agent colors (can be defined here or dynamically)
    "prey": (0, 200, 0),
    "predator": (200, 0, 0),
    "horns": (100, 100, 100),
    
    # Resource and hazard colors
    "resource_plant": (34, 139, 34), # Forest green
    "resource_water": (0, 191, 255), # Deep sky blue
    "resource_mineral": (169, 169, 169), # Dark gray
    "hazard": (255, 69, 0), # Red-orange for hazards
    "death_particle": (255, 0, 0),
}

# ... other settings
