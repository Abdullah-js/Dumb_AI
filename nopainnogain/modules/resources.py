import uuid
import random
from config import settings

class Resource:
    """
    A base class for all resources in the simulation.
    """
    def __init__(self, resource_type, nutritional_value, position):
        self.id = uuid.uuid4()
        self.type = resource_type
        self.nutritional_value = nutritional_value
        self.position = position
        self.is_depleted = False
        self.regeneration_rate = 0

    def regenerate(self):
        """Regenerates the resource's nutritional value over time."""
        self.nutritional_value = min(self.nutritional_value, self.nutritional_value + self.regeneration_rate)
        self.is_depleted = self.nutritional_value <= 0

    def __repr__(self):
        return f"Resource(type={self.type}, value={self.nutritional_value}, pos={self.position})"

class Plant(Resource):
    """
    A specific type of resource with high nutritional value.
    """
    def __init__(self, position, quantity=100):
        self.quantity = quantity
        super().__init__("plant", settings.PLANT_NUTRITIONAL_VALUE, position)
        self.regeneration_rate = settings.PLANT_REGEN_RATE

class Water(Resource):
    """
    A specific type of resource that provides hydration.
    """
    def __init__(self, position, quantity=100):
        self.quantity = quantity
        super().__init__("water", settings.WATER_NUTRITIONAL_VALUE, position)
        self.regeneration_rate = settings.WATER_REGEN_RATE
        
class Mineral(Resource):
    """
    A specific type of resource with low nutritional value but high endurance.
    """
    def __init__(self, position, quantity=100):
        self.quantity = quantity
        super().__init__("mineral", settings.MINERAL_NUTRITIONAL_VALUE, position)
        self.regeneration_rate = settings.MINERAL_REGEN_RATE
