import random
import math
from config import constants
from modules.agent import Agent

def reproduce(parent1, parent2):
    """
    Creates a new agent by combining traits from two parents.
    
    Args:
        parent1 (Agent): The first parent agent.
        parent2 (Agent): The second parent agent.
        
    Returns:
        Agent: A new child agent.
    """
    # Create child traits by averaging parents' traits
    child_traits = {}
    for trait in parent1.traits:
        parent_avg = (parent1.traits[trait] + parent2.traits[trait]) / 2
        child_traits[trait] = max(1, min(10, parent_avg))
    
    # Introduce mutation
    child_traits = _mutate_traits(child_traits)
    
    # Inherit species ID or create a new one if speciation occurs
    if _get_genetic_distance(parent1, parent2) > constants.SPECIATION_THRESHOLD:
        child_species_id = f"{parent1.species_id}_mutant_{str(random.randint(1000, 9999))}"
    else:
        child_species_id = parent1.species_id
        
    child_name = f"{parent1.species_id}_child_{random.randint(1, 100)}"
    child_is_predator = parent1.is_predator # Predation is currently a fixed trait
    
    # Create and return the new child agent
    child = Agent(
        name=child_name, 
        species_id=child_species_id, 
        is_predator=child_is_predator, 
        health=constants.MAX_HEALTH, 
        energy=constants.MAX_ENERGY, 
        position=parent1.position, 
        traits=child_traits, 
        generation=parent1.generation + 1
    )
    return child

def _mutate_traits(traits):
    """
    Applies random mutations to an agent's traits.
    
    Args:
        traits (dict): The dictionary of traits to mutate.
        
    Returns:
        dict: The mutated traits.
    """
    for trait in traits:
        if random.random() < constants.MUTATION_RATE:
            # Randomly adjust the trait value within bounds
            mutation_amount = random.uniform(-constants.MUTATION_STRENGTH, constants.MUTATION_STRENGTH)
            traits[trait] = max(1, min(10, traits[trait] + mutation_amount))
            
    return traits

def _get_genetic_distance(agent1, agent2):
    """
    Calculates the genetic distance between two agents based on their traits.
    
    Args:
        agent1 (Agent): The first agent.
        agent2 (Agent): The second agent.
        
    Returns:
        float: The Euclidean distance between the trait vectors.
    """
    distance_sq = 0
    for trait in agent1.traits:
        distance_sq += (agent1.traits[trait] - agent2.traits[trait]) ** 2
    
    return math.sqrt(distance_sq)
