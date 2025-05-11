import random

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
    wastePosList = randList(n)
    basePos = basePosArg

    game([])

    return True

'''
@return a random list of positions from (0, 0) to (31, 31)
'''
def randList(n, thirdArg = False):
    allPos = [(i, j) for i in range(32) for j in range(32)]
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

    if wasteCollected < wasteNumber:
        game(newKnownWastePosList)


'''
Plays the next turn.
This is the main function !
This function will move agents.
@param knownWastePosList a list of all the know wastes position
'''
def nextTurn(knownWastePosList):
    global wasteNumber, wastePosList, agentPosList, basePos, wasteCollected

    wasteCollected = wasteNumber
    return []


# Main
start(2, 10, (2, 2))
print(wasteNumber)
print(wastePosList)
print(agentPosList)
print(basePos)