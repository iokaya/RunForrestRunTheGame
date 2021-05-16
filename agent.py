import utils as ut
from Enums import ButtonType


class Agent:
    def __init__(self, row, column, buttonType):
        self.row = row
        self.column = column
        self.buttonType = buttonType
        self.isRunner = buttonType == ButtonType.Runner
        self.moveList = []
        self.score = 0

    def changeAgentState(self, row, column):
        oldRow = self.row
        oldColumn = self.column
        self.row = row
        self.column = column
        self.appendMoveToList
        return oldRow, oldColumn

    def appendMoveToList(self):
        self.moveList.append(self.buttonType.value + ' ' + ut.stateStringFromRowColumn(self.row, self.column))
