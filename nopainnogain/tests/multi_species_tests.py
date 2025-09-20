import sys
import os
import pandas as pd
import random
import pygame
import uuid
from config import settings, constants
from modules.agent import Agent
from modules.environment import Environment
from modules.decision_engine import DecisionEngine
from modules.evolution import reproduce
from modules.visualization import Visualization
from modules.utils import setup_directories, log_agent_data, log_species_data, save_logs
import time

def run_multi_species_scenario(scenario_name, initial_species_populations):
    """
    Runs a single multi-species test scenario.
    """
    print(f"--- Running Scenario: {scenario_name} ---")
    setup_directories()
    env = Environment(settings.GRID_WIDTH, settings.GRID_HEIGHT)
    rl_engine = DecisionEngine()

    # Initialize agents for multiple species
    agents = []
    for species_id, count in initial_species_populations.items():
        if species_id == "prey":
            agents.extend([Agent(name=f"Prey_{i}", species_id="prey", position=(random.randint(0, settings.GRID_WIDTH-1), random.randint(0, settings.GRID_HEIGHT-1))) for i in range(count)])
        elif species_id == "predator":
            agents.extend([Agent(name=f"Predator_{i}", species_id="predator", position=(random.randint(0, settings.GRID_WIDTH-1), random.randint(0, settings.GRID_HEIGHT-1))) for i in range(count)])
    
    agent_logs = []
    species_logs = []

    for step in range(settings.MAX_STEPS):
        new_agents = []
        for agent in agents:
            if not agent.alive:
                continue

            action = rl_engine.choose_action(rl_engine.get_state(agent, env))
            agent.act(action, env)
            agent.check_status()
            
            # Reproduction check
            if agent.energy >= settings.REPRODUCTION_ENERGY_THRESHOLD and random.random() < settings.REPRODUCTION_PROBABILITY:
                new_agents.append(reproduce(agent, agent))
                agent.energy -= settings.REPRODUCTION_ENERGY_THRESHOLD
                
            # Log agent data
            agent_log_entry = log_agent_data(agent, step, action, 0)
            agent_logs.append(agent_log_entry)
        
        agents = [agent for agent in agents if agent.alive]
        agents.extend(new_agents)

        species_populations = {s: 0 for s in initial_species_populations.keys()}
        for agent in agents:
            species_populations[agent.species_id] += 1
        for species_id, size in species_populations.items():
            species_log_entry = log_species_data(species_id, step, size)
            species_logs.append(species_log_entry)
            
        print(f"Step: {step}, Population: {len(agents)}, Species populations: {species_populations}")

        if not agents:
            print("All agents have perished.")
            break

    simulation_log_df = pd.DataFrame(agent_logs)
    species_log_df = pd.DataFrame(species_logs)
    
    save_logs(simulation_log_df, f"{constants.LOG_DIR}{scenario_name}_simulation_logs.csv")
    save_logs(species_log_df, f"{constants.LOG_DIR}{scenario_name}_species_logs.csv")
    print(f"Scenario {scenario_name} finished. Logs saved.")


if __name__ == "__main__":
    # Scenario 1: Competition between two prey species
    run_multi_species_scenario(
        scenario_name="prey_competition_test",
        initial_species_populations={
            "prey_A": 50,
            "prey_B": 50
        }
    )

    # Scenario 2: Predator-prey dynamics with a specialized predator
    run_multi_species_scenario(
        scenario_name="predator_prey_test",
        initial_species_populations={
            "prey": 100,
            "predator": 10
        }
    )