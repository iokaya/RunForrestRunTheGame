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
    possibleMoves.append((row, column))

    # check north
    if state[row-1][column] not in bannedTypes:
        possibleMoves.append((row-1, column))
    # check east
    if column != len(state[0])-1 and state[row][column] not in bannedTypes:
        possibleMoves.append((row, column+1))
    # check south
    if row != len(state)-1 and state[row+1][column] not in bannedTypes:
        possibleMoves.append((row+1, column))
    # check west
    if state[row][column-1] not in bannedTypes:
        possibleMoves.append((row, column-1))

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
