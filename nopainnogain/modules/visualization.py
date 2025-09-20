import pygame
import random
import math
from config import settings, constants

class Visualization:
   
    def __init__(self, environment):
        pygame.init()
        self.screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        pygame.display.set_caption("AI Ecosystem Simulator")
        self.environment = environment
        self.death_particles = []

    def render(self, agents):
        self.screen.fill(settings.COLORS["background"])
        
        # Draw the environment
        self._draw_grid()
        
        # Draw agents
        for agent in agents:
            self._draw_agent(agent)

        # Update and draw death particles
        self._update_and_draw_particles()
            
        pygame.display.flip()
        
    def visualize_birth(self, position):
       
        x, y = position
        center = (x * settings.TILE_SIZE + settings.TILE_SIZE // 2, y * settings.TILE_SIZE + settings.TILE_SIZE // 2)
        pygame.draw.circle(self.screen, (0, 255, 0), center, settings.TILE_SIZE // 4)

    def visualize_death(self, position):
     
        x, y = position
        center = (x * settings.TILE_SIZE + settings.TILE_SIZE // 2, y * settings.TILE_SIZE + settings.TILE_SIZE // 2)
        for _ in range(30):
            # Create particles with random speed and direction
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 5)
            velocity = (speed * math.cos(angle), speed * math.sin(angle))
            self.death_particles.append({
                "position": list(center),
                "velocity": velocity,
                "lifetime": 255
            })
            
    def _update_and_draw_particles(self):
        
        particles_to_keep = []
        for particle in self.death_particles:
            particle["position"][0] += particle["velocity"][0]
            particle["position"][1] += particle["velocity"][1]
            particle["lifetime"] -= 5 # Decrease opacity
            
            if particle["lifetime"] > 0:
                # Clamp the alpha value between 0 and 255
                alpha = max(0, min(255, int(particle["lifetime"])))
                color_with_alpha = settings.COLORS["death_particle"] + (alpha,)
                
                # Draw the particle as a small circle
                # We need to create a new surface with per-pixel alpha
                s = pygame.Surface((5, 5), pygame.SRCALPHA)
                pygame.draw.circle(s, color_with_alpha, (2, 2), 2)
                self.screen.blit(s, particle["position"])
                particles_to_keep.append(particle)
        self.death_particles = particles_to_keep

    def _draw_grid(self):
        
        for y in range(self.environment.height):
            for x in range(self.environment.width):
                cell = self.environment.grid[y][x]
                rect = pygame.Rect(x * settings.TILE_SIZE, y * settings.TILE_SIZE, settings.TILE_SIZE, settings.TILE_SIZE)

                # Base color for the cell
                color = settings.COLORS["ground"]

                # Override with resource color if present
                if "plant" in cell['resources'] and cell['resources']['plant'].quantity > 0:
                    color = settings.COLORS["resource_plant"]
                elif "water" in cell['resources'] and cell['resources']['water'].quantity > 0:
                    color = settings.COLORS["resource_water"]
                elif "mineral" in cell['resources'] and cell['resources']['mineral'].quantity > 0:
                    color = settings.COLORS["resource_mineral"]
                
                # Add hazard shading
                if cell['hazards'] > 0:
                    hazard_intensity = min(1, cell['hazards'] / settings.MAX_HAZARD_VALUE)
                    r = int(color[0] * (1 - hazard_intensity) + settings.COLORS["hazard"][0] * hazard_intensity)
                    g = int(color[1] * (1 - hazard_intensity) + settings.COLORS["hazard"][1] * hazard_intensity)
                    b = int(color[2] * (1 - hazard_intensity) + settings.COLORS["hazard"][2] * hazard_intensity)
                    color = (r, g, b)
                
                pygame.draw.rect(self.screen, color, rect)
                
    def _draw_agent(self, agent):
      
        x, y = agent.position
        radius = settings.TILE_SIZE // 2 - 1
        center = (x * settings.TILE_SIZE + radius, y * settings.TILE_SIZE + radius)
        
        # Draw the main agent body
        pygame.draw.circle(self.screen, agent.color, center, radius)

        # Draw horns for predators
        if agent.species_id == "predator":
            horn_color = settings.COLORS["horns"]
            horn_length = radius * 0.8
            horn_width = 2

            # Left horn
            start_pos_l = (center[0] - radius * 0.4, center[1] - radius * 0.4)
            end_pos_l = (start_pos_l[0] - horn_length * 0.5, start_pos_l[1] - horn_length)
            pygame.draw.line(self.screen, horn_color, start_pos_l, end_pos_l, horn_width)

            # Right horn
            start_pos_r = (center[0] + radius * 0.4, center[1] - radius * 0.4)
            end_pos_r = (start_pos_r[0] + horn_length * 0.5, start_pos_r[1] - horn_length)
            pygame.draw.line(self.screen, horn_color, start_pos_r, end_pos_r, horn_width)

    def quit(self):
       
        pygame.quit()

"""

# modules/visualization.py
import pygame
import random
import math
from config import settings, constants

class Visualization:
    
    def __init__(self, environment):
        pygame.init()
        self.screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        pygame.display.set_caption("AI Ecosystem Simulator")
        self.environment = environment
        self.death_particles = []

        # map species id -> drawing method
        self.agent_drawers = {
            "prey": self._draw_basic_agent,
            "predator": self._draw_predator_agent,
            # add more species keys here
        }

    def render(self, agents):
        self.screen.fill(settings.COLORS["background"])
        self._draw_grid()
        for agent in agents:
            self._draw_agent(agent)
        self._update_and_draw_particles()
        pygame.display.flip()

    def visualize_birth(self, position):
        x, y = position
        center = (x * settings.TILE_SIZE + settings.TILE_SIZE // 2, y * settings.TILE_SIZE + settings.TILE_SIZE // 2)
        pygame.draw.circle(self.screen, (0, 255, 0), center, settings.TILE_SIZE // 4)

    def visualize_death(self, position):
        x, y = position
        center = (x * settings.TILE_SIZE + settings.TILE_SIZE // 2, y * settings.TILE_SIZE + settings.TILE_SIZE // 2)
        for _ in range(30):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 5)
            velocity = (speed * math.cos(angle), speed * math.sin(angle))
            self.death_particles.append({"position": list(center), "velocity": velocity, "lifetime": 255})

    def _update_and_draw_particles(self):
        particles_to_keep = []
        for particle in self.death_particles:
            particle["position"][0] += particle["velocity"][0]
            particle["position"][1] += particle["velocity"][1]
            particle["lifetime"] -= 5
            if particle["lifetime"] > 0:
                alpha = max(0, min(255, int(particle["lifetime"])))
                color_with_alpha = settings.COLORS["death_particle"] + (alpha,)
                s = pygame.Surface((5, 5), pygame.SRCALPHA)
                pygame.draw.circle(s, color_with_alpha, (2, 2), 2)
                self.screen.blit(s, particle["position"])
                particles_to_keep.append(particle)
        self.death_particles = particles_to_keep

    def _draw_grid(self):
        for y in range(self.environment.height):
            for x in range(self.environment.width):
                cell = self.environment.grid[y][x]
                rect = pygame.Rect(x * settings.TILE_SIZE, y * settings.TILE_SIZE, settings.TILE_SIZE, settings.TILE_SIZE)
                color = settings.COLORS["ground"]
                resources = cell.get("resources", {})
                if "plant" in resources and getattr(resources["plant"], "quantity", 0) > 0:
                    color = settings.COLORS["resource_plant"]
                elif "water" in resources and getattr(resources["water"], "quantity", 0) > 0:
                    color = settings.COLORS["resource_water"]
                elif "mineral" in resources and getattr(resources["mineral"], "quantity", 0) > 0:
                    color = settings.COLORS["resource_mineral"]
                hazards = cell.get("hazards", 0)
                if hazards and hazards > 0:
                    hazard_intensity = min(1, hazards / settings.MAX_HAZARD_VALUE)
                    r = int(color[0] * (1 - hazard_intensity) + settings.COLORS["hazard"][0] * hazard_intensity)
                    g = int(color[1] * (1 - hazard_intensity) + settings.COLORS["hazard"][1] * hazard_intensity)
                    b = int(color[2] * (1 - hazard_intensity) + settings.COLORS["hazard"][2] * hazard_intensity)
                    color = (r, g, b)
                pygame.draw.rect(self.screen, color, rect)

    def _draw_agent(self, agent):
        drawer = self.agent_drawers.get(agent.species_id, self._draw_basic_agent)
        drawer(agent)

    def _draw_basic_agent(self, agent):
        x, y = agent.position
        # radius scaled with energy for quick visual feedback
        radius = max(2, int((agent.energy / constants.MAX_ENERGY) * (settings.TILE_SIZE // 2)))
        center = (x * settings.TILE_SIZE + settings.TILE_SIZE // 2, y * settings.TILE_SIZE + settings.TILE_SIZE // 2)
        pygame.draw.circle(self.screen, agent.color, center, radius)

        # small health bar
        bar_w = settings.TILE_SIZE - 4
        bar_h = 4
        bar_x = center[0] - bar_w // 2
        bar_y = center[1] + settings.TILE_SIZE // 2 - bar_h - 2
        health_pct = max(0.0, min(1.0, agent.health / constants.MAX_HEALTH))
        pygame.draw.rect(self.screen, (60, 60, 60), (bar_x, bar_y, bar_w, bar_h))
        pygame.draw.rect(self.screen, (200, 30, 30), (bar_x, bar_y, int(bar_w * health_pct), bar_h))

    def _draw_predator_agent(self, agent):
        # draw base body
        self._draw_basic_agent(agent)
        x, y = agent.position
        center = (x * settings.TILE_SIZE + settings.TILE_SIZE // 2, y * settings.TILE_SIZE + settings.TILE_SIZE // 2)
        radius = max(2, int((agent.energy / constants.MAX_ENERGY) * (settings.TILE_SIZE // 2)))
        horn_color = settings.COLORS["horns"]
        horn_length = int(radius * 0.8)
        horn_width = 2
        start_pos_l = (center[0] - int(radius * 0.4), center[1] - int(radius * 0.4))
        end_pos_l = (start_pos_l[0] - int(horn_length * 0.5), start_pos_l[1] - horn_length)
        pygame.draw.line(self.screen, horn_color, start_pos_l, end_pos_l, horn_width)
        start_pos_r = (center[0] + int(radius * 0.4), center[1] - int(radius * 0.4))
        end_pos_r = (start_pos_r[0] + int(horn_length * 0.5), start_pos_r[1] - horn_length)
        pygame.draw.line(self.screen, horn_color, start_pos_r, end_pos_r, horn_width)

    def quit(self):
        pygame.quit()
"""