from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Configuration, Game
from .serializers import ConfigurationSerializer, GameStateSerializer
from .game_logic import rand_list, next_turn
import json

class GameStatusView(APIView):
    """
    Get the current game status
    """
    def get(self, request):
        try:
            game = Game.objects.select_related('configuration').first()
            if not game:
                return Response(
                    {"error": "No game found. Start a new game first."},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            game_state = {
                "waste_collected": game.waste_collected,
                "total_wastes": game.configuration.num_wastes,
                "agent_positions": game.agent_positions,
                "waste_positions": game.waste_positions,
                "base_position": [game.configuration.base_position_x, game.configuration.base_position_y],
                "turn_number": game.turn_number
            }
            
            serializer = GameStateSerializer(game_state)
            return Response(serializer.data)
            
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class GameNextRoundView(APIView):
    """
    Play the next round of the game
    """
    def post(self, request):
        try:
            game = Game.objects.select_related('configuration').first()
            if not game:
                return Response(
                    {"error": "No game found. Start a new game first."},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            if not game.is_active:
                return Response(
                    {"error": "Game is not active. Start a new game first."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            base_position = [game.configuration.base_position_x, game.configuration.base_position_y]
            
            # Run next turn logic
            waste_positions, agent_positions, known_waste_positions, waste_collected = next_turn(
                game.waste_positions,
                game.agent_positions,
                base_position,
                game.known_waste_positions,
                game.waste_collected
            )
            
            # Update game state
            game.waste_positions = waste_positions
            game.agent_positions = agent_positions
            game.known_waste_positions = known_waste_positions
            game.waste_collected = waste_collected
            game.turn_number += 1
            
            # Check if game is over
            if game.waste_collected >= game.configuration.num_wastes:
                game.is_active = False
            
            game.save()
            
            # Prepare response
            game_state = {
                "waste_collected": game.waste_collected,
                "total_wastes": game.configuration.num_wastes,
                "agent_positions": game.agent_positions,
                "waste_positions": game.waste_positions,
                "base_position": base_position,
                "turn_number": game.turn_number
            }
            
            serializer = GameStateSerializer(game_state)
            return Response(serializer.data)
            
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class GameStartView(APIView):
    """
    Start a new game
    POST Body: 'num_agents', 'num_wastes', 'base_position_x', 'base_position_y'
    """
    def post(self, request):
        try:
            # Extract configuration from request
            serializer = ConfigurationSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Check if game already exists and delete it
            if Game.objects.exists():
                Game.objects.all().delete()
            if Configuration.objects.exists():
                Configuration.objects.all().delete()
            
            # Create new configuration
            config = serializer.save()
            
            # Check if number of agents and wastes are valid
            if config.num_agents >= (32 * 32) or config.num_wastes >= (32 * 32):
                config.delete()
                return Response(
                    {"error": "Too many agents or wastes for the board size."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Initialize game state
            agent_positions = rand_list(config.num_agents, third_arg=True)
            agent_positions_list = [[i, j, w] for i, j, w in agent_positions]
            
            waste_positions = rand_list(config.num_wastes, agent_positions=agent_positions, wastes=True)
            waste_positions_list = [[i, j] for i, j in waste_positions]
            
            # Create game
            game = Game.objects.create(
                configuration=config,
                waste_collected=0,
                is_active=True,
                turn_number=0,
                waste_positions=waste_positions_list,
                agent_positions=agent_positions_list,
                known_waste_positions=[]
            )
            
            # Prepare response
            game_state = {
                "waste_collected": 0,
                "total_wastes": config.num_wastes,
                "agent_positions": game.agent_positions,
                "waste_positions": game.waste_positions,
                "base_position": [config.base_position_x, config.base_position_y],
                "turn_number": 0
            }
            
            response_serializer = GameStateSerializer(game_state)
            return Response(response_serializer.data)
            
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class GameStopView(APIView):
    """
    Stop the current game
    """
    def post(self, request):
        try:
            game = Game.objects.select_related('configuration').first()
            if not game:
                return Response(
                    {"error": "No game found."},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            if not game.is_active:
                return Response(
                    {"error": "Game is already stopped."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Prepare response
            game_state = {
                "waste_collected": game.waste_collected,
                "total_wastes": game.configuration.num_wastes,
                "agent_positions": game.agent_positions,
                "waste_positions": game.waste_positions,
                "base_position": [game.configuration.base_position_x, game.configuration.base_position_y],
                "turn_number": game.turn_number
            }

            # Stop the game
            Game.objects.all().delete()
            Configuration.objects.all().delete()
            
            serializer = GameStateSerializer(game_state)
            return Response(serializer.data)
            
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
