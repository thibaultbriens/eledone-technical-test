from django.db import models
import json

class Configuration(models.Model):
    num_agents = models.IntegerField()
    num_wastes = models.IntegerField()
    base_position_x = models.IntegerField()
    base_position_y = models.IntegerField()
    
    @property
    def base_position(self):
        return (self.base_position_x, self.base_position_y)

class Game(models.Model):
    configuration = models.OneToOneField(Configuration, on_delete=models.CASCADE, related_name='game')
    waste_collected = models.IntegerField(default=0)
    is_active = models.BooleanField(default=False)
    turn_number = models.IntegerField(default=-1)
    
    # Serialized field for waste positions (list of tuples)
    _waste_positions = models.TextField(blank=True, default='[]')
    
    # Serialized field for agent positions (list of tuples with 3 elements)
    _agent_positions = models.TextField(blank=True, default='[]')
    
    # Serialized field for known waste positions
    _known_waste_positions = models.TextField(blank=True, default='[]')
    
    @property
    def waste_positions(self):
        return json.loads(self._waste_positions)
    
    @waste_positions.setter
    def waste_positions(self, positions):
        self._waste_positions = json.dumps(positions)
    
    @property
    def agent_positions(self):
        return json.loads(self._agent_positions)
    
    @agent_positions.setter
    def agent_positions(self, positions):
        self._agent_positions = json.dumps(positions)
    
    @property
    def known_waste_positions(self):
        return json.loads(self._known_waste_positions)
    
    @known_waste_positions.setter
    def known_waste_positions(self, positions):
        self._known_waste_positions = json.dumps(positions)
