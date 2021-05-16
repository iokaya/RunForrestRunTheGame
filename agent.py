import utils as ut
from Enums import ButtonType


class Agent:
    def __init__(self, row, column, buttonType):
        self.row = row
        self.column = column
        self.buttonType = buttonType
        self.isRunner = buttonType == ButtonType.Runner
        self.moveLog = []
        self.possibleMoves = []
        self.score = 0

    def changeAgentState(self, row, column):
        oldRow = self.row
        oldColumn = self.column
        self.row = row
        self.column = column
        self.appendMoveToLog()
        return oldRow, oldColumn

    def appendMoveToLog(self):
        self.moveLog.append(self.buttonType.value + ' ' + ut.stateStringFromRowColumn(self.row, self.column))

    def detectPossibleMoves(self, state):
        self.possibleMoves = ut.detectPossibleMoves(self.row, self.column, state)

