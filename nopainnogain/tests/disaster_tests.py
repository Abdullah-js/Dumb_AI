import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import pandas as pd
import random
import pygame
from config import settings, constants
from modules.agent import Agent
from modules.environment import Environment
from modules.decision_engine import DecisionEngine
from modules.evolution import reproduce
from modules.visualization import Visualization
from modules.utils import setup_directories, log_agent_data, log_species_data, save_logs
import time

def run_disaster_scenario(scenario_name, initial_prey, initial_predators, disaster_step, disaster_type, hazard_increase):
    """
    Runs a single disaster test scenario.
    """
    print(f"--- Running Scenario: {scenario_name} ---")
    setup_directories()
    env = Environment(settings.GRID_WIDTH, settings.GRID_HEIGHT)
    rl_engine = DecisionEngine()
    
    # Initialize agents
    agents = [Agent(name=f"Prey_{i}", species_id="prey", position=(random.randint(0, settings.GRID_WIDTH-1), random.randint(0, settings.GRID_HEIGHT-1))) for i in range(initial_prey)]
    agents.extend([Agent(name=f"Predator_{i}", species_id="predator", position=(random.randint(0, settings.GRID_WIDTH-1), random.randint(0, settings.GRID_HEIGHT-1))) for i in range(initial_predators)])
    
    agent_logs = []
    species_logs = []

    for step in range(settings.MAX_STEPS):
        # Trigger disaster
        if step == disaster_step:
            print(f"Disaster '{disaster_type}' triggered at step {step}!")
            if disaster_type == "drought":
                for y in range(env.height):
                    for x in range(env.width):
                        if "water" in env.grid[y][x]['resources']:
                            env.grid[y][x]['resources']['water'].quantity = 0
            elif disaster_type == "pollution":
                for y in range(env.height):
                    for x in range(env.width):
                        env.grid[y][x]['hazards'] += hazard_increase
        
        new_agents = []
        for agent in agents:
            if not agent.alive:
                continue
            
            action = rl_engine.choose_action(rl_engine.get_state(agent, env))
            agent.act(action, env)
            agent.check_status()
            
            # Log agent data
            agent_log_entry = log_agent_data(agent, step, action, 0)
            agent_logs.append(agent_log_entry)

        agents = [agent for agent in agents if agent.alive]
        agents.extend(new_agents)

        species_populations = {s: 0 for s in ["prey", "predator"]}
        for agent in agents:
            species_populations[agent.species_id] += 1
        for species_id, size in species_populations.items():
            species_log_entry = log_species_data(species_id, step, size)
            species_logs.append(species_log_entry)
            
        print(f"Step: {step}, Population: {len(agents)}, Prey: {species_populations['prey']}, Predator: {species_populations['predator']}")

        if not agents:
            print("All agents have perished.")
            break
            
    simulation_log_df = pd.DataFrame(agent_logs)
    species_log_df = pd.DataFrame(species_logs)

    save_logs(simulation_log_df, f"{constants.LOG_DIR}{scenario_name}_simulation_logs.csv")
    save_logs(species_log_df, f"{constants.LOG_DIR}{scenario_name}_species_logs.csv")
    print(f"Scenario {scenario_name} finished. Logs saved.")


if __name__ == "__main__":
    # Scenario 1: Sudden Drought at step 200
    run_disaster_scenario(
        scenario_name="drought_test",
        initial_prey=settings.INITIAL_PREY_POPULATION,
        initial_predators=settings.INITIAL_PREDATOR_POPULATION,
        disaster_step=200,
        disaster_type="drought",
        hazard_increase=50
    )

    # Scenario 2: Severe Pollution at step 400
    run_disaster_scenario(
        scenario_name="pollution_test",
        initial_prey=settings.INITIAL_PREY_POPULATION,
        initial_predators=settings.INITIAL_PREDATOR_POPULATION,
        disaster_step=400,
        disaster_type="pollution",
        hazard_increase=100
    )