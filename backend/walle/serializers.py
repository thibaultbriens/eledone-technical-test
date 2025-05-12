from rest_framework import serializers
from .models import Configuration, Game

class ConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Configuration
        fields = ['num_agents', 'num_wastes', 'base_position_x', 'base_position_y']

class GameStateSerializer(serializers.Serializer):
    waste_collected = serializers.IntegerField()
    total_wastes = serializers.IntegerField()
    agent_positions = serializers.ListField()
    waste_positions = serializers.ListField()
    base_position = serializers.ListField()
    turn_number = serializers.IntegerField()
