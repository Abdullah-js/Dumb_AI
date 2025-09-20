import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from config import constants

def plot_population_trends(sim_log_path, species_log_path):
    """
    Plots the total population and population of each species over time.
    
    Args:
        sim_log_path (str): Path to the main simulation log CSV.
        species_log_path (str): Path to the species population log CSV.
    """
    if not os.path.exists(sim_log_path) or not os.path.exists(species_log_path):
        print(f"Log files not found. Please run the simulation first.")
        return

    sim_df = pd.read_csv(sim_log_path)
    species_df = pd.read_csv(species_log_path)

    # Plot total population
    total_population_over_time = sim_df.groupby('step')['agent_id'].count()
    plt.figure(figsize=(12, 6))
    total_population_over_time.plot(title="Total Population Over Time", linestyle='-', marker='o')
    plt.xlabel("Time Step")
    plt.ylabel("Population Size")
    plt.grid(True)
    plt.show()

    # Plot population of each species
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=species_df, x='step', y='population_size', hue='species_id')
    plt.title("Species Population Over Time")
    plt.xlabel("Time Step")
    plt.ylabel("Population Size")
    plt.legend(title='Species')
    plt.grid(True)
    plt.show()

def plot_trait_distribution(sim_log_path, trait):
    """
    Plots the distribution of a specific trait at the final time step.
    
    Args:
        sim_log_path (str): Path to the main simulation log CSV.
        trait (str): The name of the trait to plot (e.g., 'speed', 'intelligence').
    """
    if not os.path.exists(sim_log_path):
        print(f"Log file not found. Please run the simulation first.")
        return
        
    sim_df = pd.read_csv(sim_log_path)
    
    # Get data from the final step
    final_step = sim_df['step'].max()
    final_step_df = sim_df[sim_df['step'] == final_step]
    
    if trait not in final_step_df.columns:
        print(f"Trait '{trait}' not found in the simulation logs.")
        return

    plt.figure(figsize=(12, 6))
    sns.histplot(data=final_step_df, x=trait, kde=True, hue='species_id', multiple='dodge')
    plt.title(f"Distribution of {trait.capitalize()} Trait at End of Simulation")
    plt.xlabel(trait.capitalize())
    plt.ylabel("Frequency")
    plt.show()

def main():
    """Main function to run the analysis scripts."""
    print("Starting simulation data analysis...")
    sim_log_path = os.path.join(constants.DATA_DIR, 'simulation_logs.csv')
    species_log_path = os.path.join(constants.DATA_DIR, 'species_logs.csv')
    
    # Check if logs exist
    if not os.path.exists(sim_log_path):
        print(f"Simulation log file not found at: {sim_log_path}")
        print("Please run the main simulation first to generate data.")
        return

    # Plot population trends
    plot_population_trends(sim_log_path, species_log_path)
    
    # Plot trait distributions for key traits
    plot_trait_distribution(sim_log_path, 'speed')
    plot_trait_distribution(sim_log_path, 'aggression')
    plot_trait_distribution(sim_log_path, 'cooperation')

if __name__ == "__main__":
    main()