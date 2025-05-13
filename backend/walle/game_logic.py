import random

def rand_list(n, agent_positions=None, third_arg=False, wastes=False):
    """
    Generate a random list of positions
    """
    all_pos = [(i, j) for i in range(32) for j in range(32)]
    
    if wastes and agent_positions:
        for position in agent_positions:
            i, j = position[0], position[1]
            if (i, j) in all_pos:
                all_pos.remove((i, j))
    
    if len(all_pos) < n:
        n = len(all_pos)
    
    pos = random.sample(all_pos, n)
    
    if third_arg:
        return [(i, j, False) for (i, j) in pos]
    else:
        return pos

def distance_to_pos(pos1, pos2):
    """
    Calculate Manhattan distance between two positions
    """
    return abs(pos2[0] - pos1[0]) + abs(pos2[1] - pos1[1])

def vector_to_pos(pos1, pos2):
    """
    Calculate direction vector between two positions
    """
    return (pos2[0] - pos1[0], pos2[1] - pos1[1])

def closest_waste(known_waste_positions, pos, agent_index, agents_count, assigned_wastes=None):
    """
    Find closest waste position to the agent with load balancing
    """
    if not assigned_wastes:
        assigned_wastes = {}
        
    if len(known_waste_positions) == 0:
        # Strategic exploration with sector division
        grid_size = 32
        sector_size = grid_size // min(4, agents_count)
        
        # Assign sectors based on agent index for better coverage
        sector_x = (agent_index % 2) * sector_size + random.randint(0, sector_size - 1)
        sector_y = ((agent_index // 2) % 2) * sector_size + random.randint(0, sector_size - 1)
        
        # Add offset to make agents explore different areas
        offset_x = random.randint(-5, 5)
        offset_y = random.randint(-5, 5)
        
        target_x = min(max(0, sector_x * (grid_size // sector_size // 2) + offset_x), grid_size - 1)
        target_y = min(max(0, sector_y * (grid_size // sector_size // 2) + offset_y), grid_size - 1)
        
        return (target_x, target_y)
    
    # Filter out wastes that are already assigned to other agents
    available_wastes = [w for w in known_waste_positions if tuple(w) not in assigned_wastes.values()]
    
    # If no available wastes, pick the closest one regardless of assignment
    if not available_wastes:
        available_wastes = known_waste_positions
    
    # Calculate distances and find closest waste using a list instead of heap
    if available_wastes:
        waste_distances = [(distance_to_pos(pos, waste), waste) for waste in available_wastes]
        closest_waste_pos = min(waste_distances, key=lambda x: x[0])[1]
        return closest_waste_pos
    
    # Fallback to original behavior
    return known_waste_positions[0]

def find_path(start, target, grid_size=32, avoid_diagonal=False, random_factor=0.2):
    """
    Find next position to move towards target with enhanced pathfinding
    to avoid gridlocks
    """
    # Calculate direction vector to target
    dx, dy = vector_to_pos(start, target)
    
    # Introduce occasional randomness to break patterns
    if random.random() < random_factor:
        # Randomly prioritize horizontal or vertical movement to break diagonal gridlocks
        if random.random() < 0.5:
            # Prioritize horizontal movement
            if dx != 0:
                next_x = start[0] + (1 if dx > 0 else -1)
                next_pos = (next_x, start[1])
            else:
                next_y = start[1] + (1 if dy > 0 else -1 if dy < 0 else 0)
                next_pos = (start[0], next_y)
        else:
            # Prioritize vertical movement
            if dy != 0:
                next_y = start[1] + (1 if dy > 0 else -1)
                next_pos = (start[0], next_y)
            else:
                next_x = start[0] + (1 if dx > 0 else -1 if dx < 0 else 0)
                next_pos = (next_x, start[1])
    else:
        # Normal pathfinding logic with better handling of diagonal situations
        if abs(dx) > abs(dy) or (abs(dx) == abs(dy) and random.random() < 0.5):
            # Move horizontally first or random choice when diagonal
            next_x = start[0] + (1 if dx > 0 else -1 if dx < 0 else 0)
            next_pos = (next_x, start[1])
        else:
            # Move vertically first or random choice when diagonal
            next_y = start[1] + (1 if dy > 0 else -1 if dy < 0 else 0)
            next_pos = (start[0], next_y)
    
    # Make sure we stay in bounds
    next_x, next_y = next_pos
    next_x = max(0, min(next_x, grid_size - 1))
    next_y = max(0, min(next_y, grid_size - 1))
    
    return (next_x, next_y)

def try_alternative_moves(current_pos, agent_positions, grid_size=32):
    """
    Try alternative moves when the primary direction is blocked
    Returns a list of possible positions ordered by priority
    """
    x, y = current_pos
    possible_moves = []
    
    # Check all four possible directions
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    random.shuffle(directions)  # Randomize to avoid patterns
    
    for dx, dy in directions:
        new_x, new_y = x + dx, y + dy
        if 0 <= new_x < grid_size and 0 <= new_y < grid_size:
            if not any((new_x, new_y) == (ax, ay) for ax, ay, _ in agent_positions):
                possible_moves.append((new_x, new_y))
    
    return possible_moves

def next_turn(waste_positions, agent_positions, base_pos, known_waste_positions, waste_collected):
    """
    Calculate the state for the next turn with agent coordination and improved
    movement logic to avoid gridlocks
    """
    # Convert positions from lists to tuples for easier processing
    waste_positions_tuples = [tuple(pos) for pos in waste_positions]
    agent_positions_tuples = [tuple(pos) for pos in agent_positions]
    known_waste_positions_tuples = [tuple(pos) for pos in known_waste_positions]
    base_pos_tuple = tuple(base_pos)
    
    # Task assignment for agents
    assigned_wastes = {}
    agents_count = len(agent_positions_tuples)
    
    # Update the known waste positions first (for all agents)
    for index, (i, j, w) in enumerate(agent_positions_tuples):
        for di in range(-5, 6):
            for dj in range(-5, 6):
                ni, nj = i + di, j + dj
                # Make sure coordinates are within bounds
                if 0 <= ni < 32 and 0 <= nj < 32:
                    if (ni, nj) in waste_positions_tuples and (ni, nj) not in known_waste_positions_tuples:
                        known_waste_positions_tuples.append((ni, nj))
    
    # Random priority order for movement to avoid gridlocks
    # Agents with higher priority get to move first
    movement_priority = list(range(len(agent_positions_tuples)))
    random.shuffle(movement_priority)
    
    # Keep track of new positions to avoid collisions
    new_positions = {}
    
    # Move agents in priority order
    for priority_idx in movement_priority:
        index = priority_idx
        i, j, w = agent_positions_tuples[index]
        
        # Drop waste if agent is at base
        if (i, j) == base_pos_tuple and w:
            agent_positions_tuples[index] = (i, j, False)
            waste_collected += 1
            if index in assigned_wastes:
                del assigned_wastes[index]
            continue

        # If is on waste, collect it
        if (i, j) in known_waste_positions_tuples and not w:
            agent_positions_tuples[index] = (i, j, True)
            known_waste_positions_tuples.remove((i, j))
            waste_positions_tuples.remove((i, j))
            if index in assigned_wastes:
                del assigned_wastes[index]
            continue
        
        # Determine target position
        if w:
            target_pos = base_pos_tuple  # Return to base if carrying waste
        else:
            if index not in assigned_wastes or tuple(assigned_wastes[index]) not in known_waste_positions_tuples:
                # Find and assign a new waste target
                target_waste = closest_waste(known_waste_positions_tuples, (i, j), index, agents_count, assigned_wastes)
                assigned_wastes[index] = target_waste
                target_pos = target_waste
            else:
                target_pos = assigned_wastes[index]
        
        # Introduce randomness based on agent index to avoid synchronized movement
        random_factor = 0.2 + (index % 5) * 0.05  # Different random factors for different agents
        
        # Find next position using improved pathfinding to reduce gridlocks
        next_pos = find_path((i, j), target_pos, random_factor=random_factor)
        next_i, next_j = next_pos
        
        # Check if the move is valid and doesn't collide with other agents
        valid_move = False
        
        # First check if the primary move is valid
        if 0 <= next_i < 32 and 0 <= next_j < 32:
            # Check for collisions with existing and new agent positions
            if not any((next_i, next_j) == (x, y) for x, y, _ in agent_positions_tuples if (x, y) != (i, j)):
                # Also check against new positions of agents that have already moved
                if not any((next_i, next_j) == new_positions.get(other_idx, (-1, -1)) for other_idx in range(len(agent_positions_tuples)) if other_idx != index and other_idx in new_positions):
                    valid_move = True
                    new_positions[index] = (next_i, next_j)
                    agent_positions_tuples[index] = (next_i, next_j, w)
        
        # If primary move is invalid, try alternative moves
        if not valid_move:
            alternative_moves = try_alternative_moves((i, j), agent_positions_tuples)
            for alt_i, alt_j in alternative_moves:
                # Check if this alternative move is valid
                if not any((alt_i, alt_j) == new_positions.get(other_idx, (-1, -1)) for other_idx in range(len(agent_positions_tuples)) if other_idx != index and other_idx in new_positions):
                    new_positions[index] = (alt_i, alt_j)
                    agent_positions_tuples[index] = (alt_i, alt_j, w)
                    valid_move = True
                    break
            
            # If still stuck, stay in place (no valid move)
            if not valid_move:
                new_positions[index] = (i, j)
    
    # Convert tuples back to lists for JSON serialization
    waste_positions = [list(pos) for pos in waste_positions_tuples]
    agent_positions = [list(pos) for pos in agent_positions_tuples]
    known_waste_positions = [list(pos) for pos in known_waste_positions_tuples]
    
    return waste_positions, agent_positions, known_waste_positions, waste_collected
