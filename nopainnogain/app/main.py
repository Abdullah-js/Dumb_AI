"""
import sys
import os
import random
import uuid
import pygame
import pandas as pd
from datetime import datetime

# This is a critical line. We need to set the project root
# so we can import our modules correctly.
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import settings, constants
from modules.agent import Agent
from modules.environment import Environment
from modules.genetics import reproduce
from modules.decision_engine import DecisionEngine
from modules.evolution import reproduce, genetic_distance
from modules.visualization import Visualization
from modules.utils import setup_directories, log_agent_data, log_species_data, save_logs
from modules.navigation import Pathfinder


def run_simulation():
    
    print("Starting the NOPAİNNOGAİN AI Ecosystem Simulator...")

    # 1. Setup
    setup_directories()
    env = Environment(settings.GRID_WIDTH, settings.GRID_HEIGHT)
    rl_engine = DecisionEngine()
    pathfinder = Pathfinder(env)

    # Initialize Pygame and the visualization module
    # The Visualization class now handles Pygame initialization internally
    vis = Visualization(env)
    clock = pygame.time.Clock()

    # Initialize the first generation of agents
    agents = [
        Agent(
            name=f"Agent_{i}",
            species_id=f"prey_{i}",
            position=(random.randint(0, settings.GRID_WIDTH - 1), random.randint(0, settings.GRID_HEIGHT - 1))
        ) for i in range(settings.INITIAL_PREY_POPULATION)
    ]

    # Initialize log files
    simulation_log_df = pd.DataFrame(columns=['step', 'agent_id', 'agent_name', 'species_id', 'health', 'energy', 'position_x', 'position_y', 'generation', 'age', 'speed', 'intelligence', 'aggression', 'cooperation', 'pollution_tolerance', 'action', 'reward'])
    species_log_df = pd.DataFrame(columns=['step', 'species_id', 'population_size'])

    # 2. Main Simulation Loop
    running = True
    step = 0
    while running and step < settings.MAX_STEPS:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Create a new list for the next generation of agents
        new_agents = []

        # Process each agent
        for agent in agents:
            if not agent.alive:
                continue

            # Get the current state
            current_state = rl_engine.get_state(agent, env)

            # Get the action from the decision engine
            # FIX: The DecisionEngine's method is `choose_action`, not `get_action`.
            # It also requires the list of possible actions.
            action = rl_engine.choose_action(agent, env, constants.ACTIONS)

            # Execute the action and get the reward
            agent.perform_action(action, env)
            reward = rl_engine.get_reward(agent, env, action)

            # Update Q-table
            next_state = rl_engine.get_state(agent, env)
            rl_engine.update_q_table(current_state, action, reward, next_state)

            # Log agent data
            simulation_log_df = log_agent_data(simulation_log_df, agent, step, action, reward)

            # Handle reproduction and check status
            if agent.energy > settings.REPRODUCTION_ENERGY_THRESHOLD:
                if random.random() < agent.traits['reproduction_rate']:
                    child = reproduce(agent, random.choice(agents))
                    new_agents.append(child)
            agent.check_status()
            agent.age += 1

        # Remove dead agents and add new ones
        agents = [agent for agent in agents if agent.alive]
        agents.extend(new_agents)

        # Log species populations
        species_populations = {}
        for agent in agents:
            species_populations[agent.species_id] = species_populations.get(agent.species_id, 0) + 1
        for species_id, size in species_populations.items():
            species_log_df = log_species_data(species_log_df, species_id, step, size)

        # Update environment
        env.update_state()

        # --- The Key Fix: Render and update the display ---
        vis.render(agents)

        # Decay exploration rate
        rl_engine.exploration_rate = max(settings.MIN_EXPLORATION_RATE, rl_engine.exploration_rate * settings.EXPLORATION_DECAY)

        # Check for victory or extinction
        if len(agents) >= settings.VICTORY_POPULATION:
            print("VICTORY! The population has reached the target goal.")
            running = False

        print(f"Step: {step}, Population: {len(agents)}, Exploration Rate: {rl_engine.exploration_rate:.2f}")
        if not agents:
            print("All agents have perished.")
            running = False

        # Control the simulation speed
        clock.tick(settings.FPS)

        step += 1

    # 3. Cleanup and Analysis
    save_logs(simulation_log_df, f"{constants.LOG_DIR}simulation_logs.csv")
    save_logs(species_log_df, f"{constants.LOG_DIR}species_logs.csv")
    vis.quit()
    print("Simulation finished. Logs saved to the data/logs directory.")

if __name__ == "__main__":
    run_simulation()
    import sys"""
import os
import random
import uuid
import pygame
import pandas as pd
from datetime import datetime

# This is a critical line. We need to set the project root
# so we can import our modules correctly.
os.sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import settings, constants
from modules.agent import Agent
from modules.environment import Environment
from modules.genetics import reproduce
from modules.decision_engine import DecisionEngine
from modules.evolution import reproduce, genetic_distance
from modules.visualization import Visualization
from modules.utils import setup_directories, log_agent_data, log_species_data, save_logs
from modules.navigation import Pathfinder


def run_simulation():
    """
    Main function to run the entire simulation, now using the advanced NOPAİNNOGAİN modules.
    """
    print("Starting the NOPAİNNOGAİN AI Ecosystem Simulator...")

    # 1. Setup
    setup_directories()
    env = Environment(settings.GRID_WIDTH, settings.GRID_HEIGHT)
    rl_engine = DecisionEngine()
    pathfinder = Pathfinder(env)

    # Initialize Pygame and the visualization module
    # The Visualization class now handles Pygame initialization internally
    vis = Visualization(env)
    clock = pygame.time.Clock()

    # Initialize the first generation of agents
    agents = [
        Agent(
            name=f"Agent_{i}",
            species_id=f"prey_{i}",
            position=(random.randint(0, settings.GRID_WIDTH - 1), random.randint(0, settings.GRID_HEIGHT - 1))
        ) for i in range(settings.INITIAL_PREY_POPULATION)
    ]

    # Initialize log files
    simulation_log_df = pd.DataFrame(columns=['step', 'agent_id', 'agent_name', 'species_id', 'health', 'energy', 'position_x', 'position_y', 'generation', 'age', 'speed', 'intelligence', 'aggression', 'cooperation', 'pollution_tolerance', 'action', 'reward'])
    species_log_df = pd.DataFrame(columns=['step', 'species_id', 'population_size'])

    # 2. Main Simulation Loop
    running = True
    step = 0
    while running and step < settings.MAX_STEPS:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Create a new list for the next generation of agents
        new_agents = []

        # Process each agent
        for agent in agents:
            if not agent.alive:
                continue

            # Get the current state
            current_state = rl_engine.get_state(agent, env)

            # Get the action from the decision engine
            # FIX: The DecisionEngine's method is `choose_action`, not `get_action`.
            # It also requires the list of possible actions.
            action = rl_engine.choose_action(agent, env, constants.ACTIONS)

            # Execute the action and get the reward
            agent.perform_action(action, env)
            reward = rl_engine.get_reward(agent, env, action)

            # Update Q-table
            next_state = rl_engine.get_state(agent, env)
            rl_engine.update_q_table(current_state, action, reward, next_state)

            # Log agent data
            simulation_log_df = log_agent_data(simulation_log_df, agent, step, action, reward)

            # Handle reproduction and check status
            if agent.energy > settings.REPRODUCTION_ENERGY_THRESHOLD:
                if random.random() < agent.traits['reproduction_rate']:
                    child = reproduce(agent, random.choice(agents))
                    new_agents.append(child)
            agent.check_status()
            agent.age += 1

        # Remove dead agents and add new ones
        agents = [agent for agent in agents if agent.alive]
        agents.extend(new_agents)

        # Log species populations
        species_populations = {}
        for agent in agents:
            species_populations[agent.species_id] = species_populations.get(agent.species_id, 0) + 1
        for species_id, size in species_populations.items():
            species_log_df = log_species_data(species_log_df, species_id, step, size)

        # Update environment
        env.update_state()

        # --- The Key Fix: Render and update the display ---
        vis.render(agents)

        # Decay exploration rate
        rl_engine.exploration_rate = max(settings.MIN_EXPLORATION_RATE, rl_engine.exploration_rate * settings.EXPLORATION_DECAY)

        # Check for victory or extinction
        if len(agents) >= settings.VICTORY_POPULATION:
            print("VICTORY! The population has reached the target goal.")
            running = False

        print(f"Step: {step}, Population: {len(agents)}, Exploration Rate: {rl_engine.exploration_rate:.2f}")
        if not agents:
            print("All agents have perished.")
            running = False

        # Control the simulation speed
        clock.tick(settings.FPS)

        step += 1

    # 3. Cleanup and Analysis
    save_logs(simulation_log_df, f"{constants.LOG_DIR}simulation_logs.csv")
    save_logs(species_log_df, f"{constants.LOG_DIR}species_logs.csv")
    vis.quit()
    print("Simulation finished. Logs saved to the data/logs directory.")

if __name__ == "__main__":
    run_simulation()

"""
# main.py
import sys
import os
import random
import pygame
import pandas as pd

# allow imports when running from project root (ok for dev; package later for prod)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import settings, constants
from modules.agent import Agent
from modules.environment import Environment
from modules.genetics import reproduce  # single source for reproduction
from modules.decision_engine import DecisionEngine
from modules.visualization import Visualization
from modules.utils import setup_directories, save_logs

# ---------- adapters for RL API flexibility ----------
def _choose_action_adapter(rl_engine, agent, env):
   
    try:
        return rl_engine.choose_action(agent, env, constants.ACTIONS)
    except Exception:
        pass
    try:
        state = rl_engine.get_state(agent, env)
        return rl_engine.choose_action(state, constants.ACTIONS)
    except Exception:
        pass
    try:
        state = rl_engine.get_state(agent, env)
        return rl_engine.get_action(agent, state, constants.ACTIONS)
    except Exception:
        pass
    return random.choice(constants.ACTIONS)

def _decay_exploration_adapter(rl_engine, step):
   plicative decay with floor.
    
    if hasattr(rl_engine, "decay_exploration"):
        try:
            rl_engine.decay_exploration(step)
            return
        except Exception:
            pass

    # fallback multiplicative decay
    if hasattr(rl_engine, "exploration_rate"):
        rl_engine.exploration_rate = max(
            settings.MIN_EXPLORATION_RATE,
            rl_engine.exploration_rate * getattr(settings, "EXPLORATION_DECAY", 0.995),
        )

# ----------------------------------------------------

def run_simulation():
    print("Starting NOPAİN NOGAİN AI Ecosystem Simulator...")

    # setup
    setup_directories()
    env = Environment(settings.GRID_WIDTH, settings.GRID_HEIGHT)
    rl_engine = DecisionEngine()
    vis = Visualization(env)
    clock = pygame.time.Clock()

    # seed initial population (same species id = "prey")
    agents = [
        Agent(
            name=f"Agent_{i}",
            species_id="prey",
            position=(
                random.randint(0, settings.GRID_WIDTH - 1),
                random.randint(0, settings.GRID_HEIGHT - 1),
            ),
        )
        for i in range(settings.INITIAL_PREY_POPULATION)
    ]

    # list-based logs for performance
    simulation_log_list = []
    species_log_list = []

    running = True
    step = 0
    while running and step < settings.MAX_STEPS:
        # handle events (so window stays responsive)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        new_agents = []

        # agent loop
        for agent in agents:
            if not agent.alive:
                continue

            # get action
            try:
                action = _choose_action_adapter(rl_engine, agent, env)
            except Exception:
                action = random.choice(constants.ACTIONS)

            # perform and get reward (gracefully handle RL missing methods)
            try:
                agent.perform_action(action, env)
            except Exception as e:
                # keep running even if an agent action fails
                # print(f"Agent action error: {e}")
                pass

            try:
                reward = rl_engine.get_reward(agent, env, action)
            except Exception:
                reward = 0.0

            # update RL if possible
            try:
                current_state = rl_engine.get_state(agent, env)
                next_state = rl_engine.get_state(agent, env)
                rl_engine.update_q_table(current_state, action, reward, next_state)
            except Exception:
                pass

            # append log entry (list-based)
            simulation_log_list.append({
                "step": step,
                "agent_id": str(agent.id),
                "agent_name": agent.name,
                "species_id": agent.species_id,
                "health": agent.health,
                "energy": agent.energy,
                "position_x": agent.position[0],
                "position_y": agent.position[1],
                "generation": agent.generation,
                "age": agent.age,
                "speed": agent.traits.get("speed"),
                "intelligence": agent.traits.get("intelligence"),
                "aggression": agent.traits.get("aggression"),
                "cooperation": agent.traits.get("cooperation"),
                "pollution_tolerance": agent.traits.get("pollution_tolerance"),
                "action": action,
                "reward": reward,
            })

            # reproduction: require same-species partner and energy threshold
            if agent.energy > getattr(settings, "REPRODUCTION_ENERGY_THRESHOLD", 0):
                partners = [
                    a for a in agents
                    if a is not agent and a.alive and a.species_id == agent.species_id
                ]
                if partners and random.random() < agent.traits.get("reproduction_rate", 0.02):
                    partner = random.choice(partners)
                    try:
                        child = reproduce(agent, partner)
                        if child:
                            # place child near parent (if child has position attribute)
                            new_agents.append(child)
                            cost = getattr(settings, "REPRODUCTION_ENERGY_COST", 0)
                            if cost:
                                agent.energy = max(0, agent.energy - cost)
                                partner.energy = max(0, partner.energy - cost)
                    except Exception:
                        pass

            # life updates
            agent.age += 1
            agent.check_status()

        # remove dead agents and add newborns
        agents = [a for a in agents if a.alive]
        agents.extend(new_agents)

        # species log (list)
        species_counts = {}
        for a in agents:
            species_counts[a.species_id] = species_counts.get(a.species_id, 0) + 1
        for sid, size in species_counts.items():
            species_log_list.append({"step": step, "species_id": sid, "population_size": size})

        # environment update + render
        try:
            env.update_state()
        except Exception:
            pass
        vis.render(agents)

        # exploration decay
        _decay_exploration_adapter(rl_engine, step)

        # stop conditions
        if len(agents) >= getattr(settings, "VICTORY_POPULATION", float("inf")):
            print("VICTORY! population reached goal.")
            running = False
        if not agents:
            print("All agents perished.")
            running = False

        # info output
        print(
            f"Step: {step}, Population: {len(agents)}, "
            f"Exploration Rate: {getattr(rl_engine, 'exploration_rate', 'n/a')}"
        )

        clock.tick(settings.FPS)
        step += 1

    # finalize logs -> DataFrame and save once
    try:
        simulation_log_df = pd.DataFrame(simulation_log_list)
        species_log_df = pd.DataFrame(species_log_list)

        save_logs(simulation_log_df, os.path.join(constants.LOG_DIR, "simulation_logs.csv"))
        save_logs(species_log_df, os.path.join(constants.LOG_DIR, "species_logs.csv"))
    except Exception as e:
        print(f"Failed to save logs: {e}")

    vis.quit()
    pygame.quit()
    print("Simulation finished. Logs saved.")

if __name__ == "__main__":
    run_simulation()
"""