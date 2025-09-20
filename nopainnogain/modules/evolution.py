import random
import uuid
from modules.agent import Agent
from config import settings

def genetic_distance(genome1, genome2):
    """
    Calculates the genetic distance between two genomes.
    """
    distance = sum(abs(g1 - g2) for g1, g2 in zip(genome1, genome2))
    return distance

def reproduce(parent1, parent2):
    """
    Performs sexual reproduction with crossover and mutation.
    """
    child_genome = []
    crossover_point = random.randint(1, len(parent1.genome) - 1)
    child_genome.extend(parent1.genome[:crossover_point])
    child_genome.extend(parent2.genome[crossover_point:])
    
    child_genome = mutate(child_genome)
    
    # Speciation check: if genetic distance is too high, it's a new species
    if genetic_distance(parent1.genome, parent2.genome) > settings.GENETIC_DISTANCE_THRESHOLD:
        child_species_id = uuid.uuid4()
    else:
        child_species_id = parent1.species_id

    child = Agent(
        name=f"Child_{random.randint(1, 1000)}",
        genome=child_genome,
        species_id=child_species_id,
        position=parent1.position,
        generation=max(parent1.generation, parent2.generation) + 1
    )
    return child

def mutate(genome):
    """
    Randomly mutates an agent's genes.
    """
    mutated_genome = genome[:]
    for i in range(len(mutated_genome)):
        if random.random() < settings.MUTATION_RATE:
            change = random.choice([-2, -1, 1, 2])
            mutated_genome[i] = max(0, min(10, mutated_genome[i] + change))
    return mutated_genome
