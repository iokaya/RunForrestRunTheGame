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
    return numToChar(column) + row