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
    Calculate distance between two positions
    """
    return (pos2[0] - pos1[0], pos2[1] - pos1[1])

def closest_waste(known_waste_positions, pos):
    """
    Find closest waste position to the agent
    """
    if len(known_waste_positions) == 0:
        # Strategic exploration instead of pure randomness
        x, y = pos
        
        # Create sectors and assign a target position based on current position
        if x < 10:
            target_x = 25 
        elif x > 21:
            target_x = 6
        else:
            target_x = x
            
        if y < 10:
            target_y = 25 
        elif y > 21:
            target_y = 6
        else:
            target_y = y
        
        # Randomness to avoid same paths for every agents
        target_x += random.randint(-3, 3)
        target_y += random.randint(-3, 3)
        
        # Ensure within bounds
        target_x = max(0, min(31, target_x))
        target_y = max(0, min(31, target_y))
        
        return (target_x, target_y)
    
    closest_waste = known_waste_positions[0]
    min_distance = distance_to_pos(pos, closest_waste)
    for waste in known_waste_positions:
        d = distance_to_pos(pos, waste)
        if (abs(d[0]) + abs(d[1])) < (abs(min_distance[0]) + abs(min_distance[1])):
            closest_waste = waste
            min_distance = d

    return closest_waste

def next_turn(waste_positions, agent_positions, base_pos, known_waste_positions, waste_collected):
    """
    Calculate the state for the next turn
    """
    # Convert positions from lists to tuples for easier processing
    waste_positions_tuples = [tuple(pos) for pos in waste_positions]
    agent_positions_tuples = [tuple(pos) for pos in agent_positions]
    known_waste_positions_tuples = [tuple(pos) for pos in known_waste_positions]
    base_pos_tuple = tuple(base_pos)
    
    # Move agents
    for index, (i, j, w) in enumerate(agent_positions_tuples):
        # Drop waste if agent is at base
        if (i, j) == base_pos_tuple and w:
            agent_positions_tuples[index] = (i, j, False)
            waste_collected += 1

        # If is on waste, collect it
        elif (i, j) in known_waste_positions_tuples and not w:
            agent_positions_tuples[index] = (i, j, True)
            known_waste_positions_tuples.remove((i, j))
            waste_positions_tuples.remove((i, j))
        else:
            # Move to next pos
            nextpos = base_pos_tuple
            if not w:
                nextpos = closest_waste(known_waste_positions_tuples, (i, j))

            d = distance_to_pos((i, j), nextpos)
            
            # Check for potential moves in priority order
            moved = False
            
            if d[0] > 0 and not any((i + 1, j) == (x, y) for x, y, _ in agent_positions_tuples):
                agent_positions_tuples[index] = (i + 1, j, w)
                moved = True
            elif d[0] < 0 and not any((i - 1, j) == (x, y) for x, y, _ in agent_positions_tuples):
                agent_positions_tuples[index] = (i - 1, j, w)
                moved = True
            elif d[1] > 0 and not any((i, j + 1) == (x, y) for x, y, _ in agent_positions_tuples):
                agent_positions_tuples[index] = (i, j + 1, w)
                moved = True
            elif d[1] < 0 and not any((i, j - 1) == (x, y) for x, y, _ in agent_positions_tuples):
                agent_positions_tuples[index] = (i, j - 1, w)
                moved = True
            
            if moved:
                # Update position for scanning
                i, j, w = agent_positions_tuples[index]

            # Update the known waste pos list
            for di in range(-5, 6):
                for dj in range(-5, 6):
                    ni, nj = i + di, j + dj
                    # Make sure coordinates are within bounds
                    if 0 <= ni < 32 and 0 <= nj < 32:
                        if (ni, nj) in waste_positions_tuples and (ni, nj) not in known_waste_positions_tuples:
                            known_waste_positions_tuples.append((ni, nj))
    
    # Convert tuples back to lists for JSON serialization
    waste_positions = [list(pos) for pos in waste_positions_tuples]
    agent_positions = [list(pos) for pos in agent_positions_tuples]
    known_waste_positions = [list(pos) for pos in known_waste_positions_tuples]
    
    return waste_positions, agent_positions, known_waste_positions, waste_collected
