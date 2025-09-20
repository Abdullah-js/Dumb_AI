import os
import pandas as pd
import uuid
from config import constants

def setup_directories():
    """
    Sets up the necessary data directories for the simulation logs.
    """
    os.makedirs(constants.DATA_DIR, exist_ok=True)
    os.makedirs(constants.LOG_DIR, exist_ok=True)
    os.makedirs(constants.REPORTS_DIR, exist_ok=True)

def log_agent_data(df, agent, step, action, reward):
    
    new_row = {
        'step': step,
        'agent_id': agent.id,
        'agent_name': agent.name,
        'species_id': agent.species_id,
        'health': agent.health,
        'energy': agent.energy,
        'position_x': agent.position[0],
        'position_y': agent.position[1],
        'generation': agent.generation,
        'age': agent.age,
        'speed': agent.traits['speed'],
        'intelligence': agent.traits['intelligence'],
        'aggression': agent.traits['aggression'],
        'cooperation': agent.traits['cooperation'],
        'pollution_tolerance': agent.traits['pollution_tolerance'],
        'action': action,
        'reward': reward
    }
    # Use .loc to append a single row, which is a modern and efficient approach.
    df.loc[len(df)] = new_row
    return df

def log_species_data(df, species_id, step, population_size):
    
    new_row = {
        'step': step,
        'species_id': species_id,
        'population_size': population_size
    }
    # Use .loc to append a single row, which is a modern and efficient approach.
    df.loc[len(df)] = new_row
    return df

def save_logs(df, filepath):
    """
    Saves a DataFrame to a CSV file.
    
    Args:
        df (DataFrame): The DataFrame to save.
        filepath (str): The full path to the file to save to.
    """
    df.to_csv(filepath, index=False)
    print(f"Log saved to {filepath}")

def generate_unique_id():
    """Generates a unique ID."""
    return str(uuid.uuid4())