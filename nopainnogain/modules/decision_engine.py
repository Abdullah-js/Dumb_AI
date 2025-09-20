import random
import numpy as np
from config import settings, constants
from modules.agent import Agent 
class DecisionEngine:
    """
    A reinforcement learning-based decision engine for agents.
    Uses a simple Q-learning algorithm.
    """
    def __init__(self):
        # Q-table: a dictionary mapping states to a dictionary of Q-values for actions.
        self.q_table = {}
        # The exploration rate (epsilon) for the epsilon-greedy strategy.
        self.exploration_rate = settings.MAX_EXPLORATION_RATE

    def get_state(self, agent, environment):
        """
        Converts the agent's and environment's state into a hashable format for the Q-table.
        This simplified state includes agent health and energy, and local environmental data.
        
        Args:
            agent (Agent): The agent whose state is being observed.
            environment (Environment): The current simulation environment.
            
        Returns:
            tuple: A hashable representation of the state.
        """
        x, y = agent.position
        
        # Get local environmental data (e.g., resources and hazards in the current cell)
        current_cell_resources = environment.grid[y][x]['resources']
        current_cell_hazards = environment.grid[y][x]['hazards']
        
        # Sum the nutritional values of all resources in the cell to get a single state value
        total_resources_value = sum(res.nutritional_value for res in current_cell_resources.values())

        # Simplify agent's state
        simplified_health = int(agent.health / 25) # Bin health into 4 categories
        simplified_energy = int(agent.energy / 25) # Bin energy into 4 categories
        simplified_resources = int(total_resources_value / 25)
        
        return (simplified_health, simplified_energy, simplified_resources, current_cell_hazards)

    def choose_action(self, agent, environment, actions):
        """
        Chooses an action based on the epsilon-greedy strategy.
        
        Args:
            agent (Agent): The agent choosing the action.
            environment (Environment): The current simulation environment.
            actions (list): A list of all possible actions.
            
        Returns:
            str: The chosen action.
        """
        # Get the current state
        state = self.get_state(agent, environment)

        # Exploration vs. Exploitation
        if random.uniform(0, 1) < self.exploration_rate:
            # Explore: choose a random action
            return random.choice(actions)
        else:
            # Exploit: choose the best action from the Q-table
            if state not in self.q_table:
                # If the state is new, initialize it with a default Q-value of 0 for all actions
                self.q_table[state] = {action: 0 for action in actions}
            
            q_values = self.q_table[state]
            # Find the action with the highest Q-value
            max_q_value = max(q_values.values())
            
            # Handle multiple actions with the same max Q-value
            best_actions = [action for action, q_value in q_values.items() if q_value == max_q_value]
            
            return random.choice(best_actions)

    def update_q_table(self, state, action, reward, next_state):
        """
        Updates the Q-value for a state-action pair using the Q-learning formula.
        """
        # Ensure the state and next_state exist in the Q-table
        if state not in self.q_table:
            self.q_table[state] = {a: 0 for a in constants.ACTIONS}
        if next_state not in self.q_table:
            self.q_table[next_state] = {a: 0 for a in constants.ACTIONS}

        # Get the old Q-value
        old_q_value = self.q_table[state][action]
        
        # Find the max Q-value for the next state
        next_max_q = max(self.q_table[next_state].values())

        # Q-learning formula
        new_q_value = old_q_value + settings.LEARNING_RATE * (reward + settings.DISCOUNT_FACTOR * next_max_q - old_q_value)
        
        self.q_table[state][action] = new_q_value
    
    def get_reward(self, agent, environment, action):
        """
        Calculates the reward for a given action.
        
        Args:
            agent (Agent): The agent performing the action.
            environment (Environment): The current simulation environment.
            action (str): The action taken.
            
        Returns:
            float: The calculated reward.
        """
        reward = 0
        x, y = agent.position
        
        # Positive rewards
        if action == "gather":
            # Check if there are any resources in the current cell with a positive value
            if any(res.nutritional_value > 0 for res in environment.grid[y][x]['resources'].values()):
                reward += settings.REWARD_GATHER
            else:
                reward -= settings.PENALTY_FAILED_ACTION
        
        if action == "move":
            # Encourage moving towards resources and away from hazards
            total_resources_value = sum(res.nutritional_value for res in environment.grid[y][x]['resources'].values())
            if total_resources_value > 0:
                reward += settings.REWARD_MOVE_TO_RESOURCE
            if environment.grid[y][x]['hazards'] > 0:
                reward -= settings.PENALTY_MOVE_TO_HAZARD

        if not agent.alive:
            reward = settings.PENALTY_DEATH
            
        return reward