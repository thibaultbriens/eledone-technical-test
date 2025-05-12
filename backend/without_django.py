import random
from time import sleep

wasteCollected = 0
wasteNumber = 0
wastePosList = []
# agentPosList a list of (x, y, w) with x,y its position and w a boolean to know if they are carrying a waste
agentPosList = []
basePos = (0, 0)

'''
Function for game start
@param n the number of cleaning agents
@param m the number of wastes
@param basPos the position of the base

@return wether the start succeeded or not
'''
def start(n, m, basePosArg):
    if n >= (32 * 32) or m >= (32 * 32):
        return False
    
    global wasteNumber, wastePosList, agentPosList, basePos, wasteCollected
    
    wasteNumber = m
    agentPosList = randList(n, thirdArg=True)
    wastePosList = randList(m, wastes=True)
    basePos = basePosArg

    game([])

    return True

'''
@return a random list of positions from (0, 0) to (31, 31)
'''
def randList(n, thirdArg = False, wastes = False):
    allPos = [(i, j) for i in range(32) for j in range(32)]
    if wastes:
        for (i, j, _) in agentPosList:
            allPos.remove((i, j))
    pos = random.sample(allPos, n)
    if thirdArg:
        return [(i, j, False) for (i, j) in pos]
    else:
        return pos


'''
Handles all the game displaying the board for each turn and returning when the game is over
'''
def game(knownWastePosList):
    global wasteNumber, wastePosList, agentPosList, basePos, wasteCollected

    newKnownWastePosList = nextTurn(knownWastePosList)
    displayBoard()
    sleep(1)

    if wasteCollected < wasteNumber:
        game(newKnownWastePosList)
    else:
        print("Game Over")


'''
Plays the next turn.
This is the main function !
This function will move agents.
@param knownWastePosList a list of all the know wastes position
'''
def nextTurn(knownWastePosList : list):
    global wasteNumber, wastePosList, agentPosList, basePos, wasteCollected

    # Move agents
    for index, (i, j, w) in enumerate(agentPosList):
        # Drop waste if agent is at base
        if (i, j) == basePos and w:
            agentPosList[index] = (i, j, False)
            wasteCollected += 1

        # If is on waste, collect it
        if (i, j) in knownWastePosList and not w:
            agentPosList[index] = (i, j, True)
            knownWastePosList.remove((i, j))
            wastePosList.remove((i, j))
        else :
            # Move to next pos
            nextpos = basePos
            if not w:
                nextpos = closestWaste(knownWastePosList, (i, j))

            d = distanceToPos((i, j), nextpos)
            if (d[0] > 0 and not any((i + 1, j) == (x, y) for x, y, _ in agentPosList)):
                agentPosList[index] = (i + 1, j, w)
            elif (d[0] < 0 and not any((i - 1, j) == (x, y) for x, y, _ in agentPosList)):
                agentPosList[index] = (i - 1, j, w)
            elif (d[1] > 0 and not any((i, j + 1) == (x, y) for x, y, _ in agentPosList)):
                agentPosList[index] = (i, j + 1, w)
            elif (d[1] < 0 and not any((i, j - 1) == (x, y) for x, y, _ in agentPosList)):
                agentPosList[index] = (i, j - 1, w)

            # Update the known waste pos list
            for di in range(-5, 6):
                for dj in range(-5, 6):
                    if (i + di, j + dj) in wastePosList and (i + di, j + dj) not in knownWastePosList:
                        knownWastePosList.append((i + di, j + dj))
        

    return knownWastePosList

'''
Return the distance between two positions
@return a tuple (x, y) with x the distance in x and y the distance in y
'''
def distanceToPos(pos1, pos2):
    return (pos2[0] - pos1[0], pos2[1] - pos1[1])


'''
Return the position of the closest waste
@param wastePosList a list of all the known waste positions
@param pos the position of the agent

@return the position of the closest waste or a strategic exploration position if there is no waste
'''
def closestWaste(knownWastePosList, pos):
    if len(knownWastePosList) == 0:
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
    
    closestWaste = knownWastePosList[0]
    minDistance = distanceToPos(pos, closestWaste)
    for waste in knownWastePosList:
        d = distanceToPos(pos, waste)
        if (abs(d[0]) + abs(d[1])) < (abs(minDistance[0]) + abs(minDistance[1])):
            closestWaste = waste
            minDistance = d

    return closestWaste

'''
Display the board with the agents and the wastes
'''
def displayBoard():
    global wasteNumber, wastePosList, agentPosList, basePos, wasteCollected
    
    # Create an empty 32x32 board
    board = [[' ' for _ in range(32)] for _ in range(32)]
    
    # Place wastes on the board
    for waste_x, waste_y in wastePosList:
        board[waste_x][waste_y] = '.'
    
    # Place agents on the board
    for agent_x, agent_y, _ in agentPosList:
        board[agent_x][agent_y] = 'X'
    
    # Place base on the board
    base_x, base_y = basePos
    board[base_x][base_y] = '$'
    
    # Print the board
    print("\n" + "-" * 66)
    for row in board:
        print("|", end=' ')
        for cell in row:
            print(cell, end=' ')
        print("|")
    print("-" * 66)
    
    # Display waste collection status
    print(f"Waste collected: {wasteCollected}/{wasteNumber}")
    print(f"Agents: {agentPosList}")
    print("-" * 66)


# Main
start(2, 10, (2, 2))
print(wasteNumber)
print(wastePosList)
print(agentPosList)
print(basePos)