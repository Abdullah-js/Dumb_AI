import sys
import os
import pandas as pd
import random
import pygame
from config import settings, constants
from modules.agent import Agent
from modules.environment import Environment
from modules.decision_engine import DecisionEngine
from modules.utils import setup_directories, log_agent_data, log_species_data, save_logs
import time

def train_agent_in_scenario(scenario_name, num_episodes):
    """
    Trains a single agent in a simplified environment using Q-learning.
    
    Args:
        scenario_name (str): The name of the training scenario for logging.
        num_episodes (int): The number of training episodes to run.
    """
    print(f"--- Running RL Training Scenario: {scenario_name} ---")
    setup_directories()
    env = Environment(settings.GRID_WIDTH, settings.GRID_HEIGHT)
    rl_engine = DecisionEngine()
    agent = Agent(name="RL_Agent", species_id="training_species")
    
    simulation_log_df = pd.DataFrame(columns=['step', 'agent_id', 'agent_name', 'species_id', 'health', 'energy', 'position_x', 'position_y', 'generation', 'age', 'speed', 'intelligence', 'aggression', 'cooperation', 'pollution_tolerance', 'action', 'reward'])
    rewards_log = []

    for episode in range(num_episodes):
        agent.reset()
        env.reset()
        total_reward = 0
        
        for step in range(settings.MAX_STEPS):
            if not agent.alive:
                break
            
            # RL Decision-making
            current_state = rl_engine.get_state(agent, env)
            action = rl_engine.choose_action(current_state)
            
            # Take action
            if action == "move":
                move_action = random.choice(["move_up", "move_down", "move_left", "move_right"])
                agent.perform_action(move_action, env)
            elif action == "eat":
                agent.perform_action("eat", env)

            # Get reward and next state
            reward = rl_engine.get_reward(agent, env, action)
            total_reward += reward
            
            # Update Q-table
            next_state = rl_engine.get_state(agent, env)
            rl_engine.update_q_table(current_state, action, reward, next_state)

            # Log data
            simulation_log_df = log_agent_data(simulation_log_df, agent, step, action, reward)
        
        rewards_log.append({'episode': episode, 'total_reward': total_reward, 'exploration_rate': rl_engine.exploration_rate})
        
        # Decay exploration rate
        rl_engine.exploration_rate = max(settings.MIN_EXPLORATION_RATE, rl_engine.exploration_rate * settings.EXPLORATION_DECAY)

        print(f"Episode: {episode+1}/{num_episodes}, Total Reward: {total_reward}, Exploration Rate: {rl_engine.exploration_rate:.2f}")

    # Save logs and the trained Q-table
    save_logs(simulation_log_df, f"{constants.LOG_DIR}{scenario_name}_simulation_logs.csv")
    rewards_df = pd.DataFrame(rewards_log)
    save_logs(rewards_df, f"{constants.LOG_DIR}{scenario_name}_rewards_logs.csv")
    rl_engine.save_q_table()
    print(f"Scenario {scenario_name} finished. Logs and Q-table saved.")


if __name__ == "__main__":
    # Test 1: Train a single agent for 100 episodes
    train_agent_in_scenario(
        scenario_name="single_agent_training",
        num_episodes=100
    )

    # Test 2: Train a single agent in a resource-rich environment
    # Note: This would require modifying the Environment class to create a resource-rich map
    # For now, we'll just run another training session with a different name
    train_agent_in_scenario(
        scenario_name="resource_rich_training",
        num_episodes=100
    )
