import random
from Enums import ButtonType

asciiCapitalLettersStartNum = 64

def rowColumnTypeToString(row, column, button_type):
    return str(row) + '_' + str(column) + '_' + button_type

def stringToRowColumn(rc_str):
    return int(rc_str.split('_')[0]), int(rc_str.split('_')[1])

def numToChar(num):
    return chr(asciiCapitalLettersStartNum + num)

def charToNum(char):
    return int(char.upper()) - asciiCapitalLettersStartNum

def stateStringFromRowColumn(row, column):
    return numToChar(column) + str(row)

def detectPossibleMoves(row, column, buttonType, state):
    possibleMoves = []
    bannedTypes = [ButtonType.Obstacle, ButtonType.Header]

    if buttonType == ButtonType.Runner:
        bannedTypes.append(ButtonType.Chaser1)
        bannedTypes.append(ButtonType.Chaser2)

    # append current location
    possibleMoves.append('NO MOVE')

    # check north
    if state[row-1][column] not in bannedTypes:
        possibleMoves.append('NORTH')
    # check east
    if column != len(state[0])-1 and state[row][column+1] not in bannedTypes:
        possibleMoves.append('EAST')
    # check south
    if row != len(state)-1 and state[row+1][column] not in bannedTypes:
        possibleMoves.append('SOUTH')
    # check west
    if state[row][column-1] not in bannedTypes:
        possibleMoves.append('WEST')

    return possibleMoves

def getRandomNumberBetween(num1, num2):
    return random.randint(num1, num2)

def getRandomPlace(state):
    grassCount = getElementCount(state, ButtonType.Grass)
    randomPlaceNumber = getRandomNumberBetween(1, grassCount)
    counter = 0

    for i in range(0, len(state)):
        for j in range(0, len(state[i])):
            if state[i][j] == ButtonType.Grass:
                counter += 1
            if counter == randomPlaceNumber:
                return i, j

def getElementCount(state, buttonType):
    return sum([row.count(buttonType) for row in state])

def getManhattanDistance(coor1, coor2):
    return abs(coor1[0] - coor2[0]) + abs(coor1[1] - coor2[1])

def getChaserReward(runner, chaser):
    reward = 0
    md = getManhattanDistance(chaser, runner)
    if md in [1, 2]:
        reward = 3 - md
    elif isRunnerCaught(runner, chaser):
        reward = 10000
    return reward

def getRunnerReward(runner, chaser1, chaser2):
    reward = 0
    md1 = getManhattanDistance(chaser1, runner)
    md2 = getManhattanDistance(chaser2, runner)
    md = min(md1, md2)
    if md == 0:
        reward = -10000
    else:
        reward = md - 10
    return reward

def isRunnerCaught(runner, chaser):
    if runner == chaser:
        return True
    else:
        return False

def nextState(current_state, action):
    next_state = current_state
    if action == 'NORTH':
        next_state = current_state[0]-1, current_state[1]
    elif action == 'EAST':
        next_state = current_state[0], current_state[1]+1
    elif action == 'SOUTH':
        next_state = current_state[0]+1, current_state[1]
    elif action == 'WEST':
        next_state = current_state[0], current_state[1]-1
    return next_state
