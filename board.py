# import libraries
import tkinter as tk
import utils as ut
from PIL import Image, ImageTk
from Enums import ButtonType, WaitingJob
from agent import Agent

class Board(tk.Frame):
    def __init__(self, boxHeight, boxWidth, boxMargin, rowCount, columnCount, master=None):
        super().__init__(master)
        self.colorBlack = '#000000'
        self.windowTitle = 'Run Forrest Run!! The RL Game'
        self.colorBlack = '#000000'
        self.colorWhite = '#FAFAFA'
        self.colorGray = '#B9B9B9'
        self.colorRunner = '#0A9F23'
        self.colorChaser = '#9F0A0A'
        self.colorRunnerPlaceConfiguration = '#B5FFB9'
        self.colorChaserPlaceConfiguration = '#FFB5B5'
        self.colorRockPlaceConfiguration = '#B5ECFF'
        self.colorRunnerBehaviourConfiguration = '#F8B5FF'
        self.colorRockCountConfiguration = '#FFFFB5'
        self.colorTurnCountConfiguration = '#B5CFFF'
        self.buttonGrassText = 'grass'
        self.buttonRockText = 'rock'
        self.buttonRunnerText = 'runner'
        self.buttonChaser1Text = 'chaser1'
        self.buttonChaser2Text = 'chaser2'
        self.boxFont = ("Calibri", 22)
        self.buttonFont = ("Calibri", 12)
        self.windowHeight = 302 + boxHeight*(rowCount+1) + boxMargin*(rowCount+2)
        self.windowWidth = boxWidth*(columnCount+1) + boxMargin*(columnCount+2)
        self.boxWidth = boxWidth
        self.boxHeight = boxHeight
        self.boxMargin = boxMargin
        self.rowCount = rowCount
        self.columnCount = columnCount
        self.boardTopMargin = self.windowHeight - (self.rowCount + 1) * self.boxHeight - (
                    self.rowCount + 2) * self.boxMargin
        self.generalHeight = (self.boardTopMargin - 8 * self.boxMargin) / 8
        self.configurationFrameHeaderWidth = (self.windowWidth - 3 * self.boxMargin) * 0.5
        self.configurationFrameHeaderX = self.boxMargin
        self.configurationFrameHeaderY = self.boxMargin
        self.configurationFrameEltWidth = (self.configurationFrameHeaderWidth - 2 * self.boxMargin) / 3
        self.window = master
        self.runnerController = tk.IntVar()
        self.runnerController.set(1)
        self.runnerPlaceController = tk.IntVar()
        self.runnerPlaceController.set(1)
        self.chaserPlaceController = tk.IntVar()
        self.chaserPlaceController.set(1)
        self.rockPlaceController = tk.IntVar()
        self.rockPlaceController.set(1)
        self.rockCount = tk.IntVar()
        self.rockCount.set(16)
        self.rockCounter = 0
        self.turnCount = tk.IntVar()
        self.turnCount.set(100)
        self.window.title(self.windowTitle)
        self.window.resizable(0, 0)
        self.window.geometry(str(self.windowWidth) + 'x' + str(self.windowHeight))
        self.window.wm_iconphoto(False, ImageTk.PhotoImage(Image.open('image/runner.png')))
        self.window.configure(bg=self.colorGray)
        self.imageGrass = tk.PhotoImage(file='image/grass.png')
        self.imageObstacle = tk.PhotoImage(file='image/obstacle.png')
        self.imageRunner = tk.PhotoImage(file='image/runner.png')
        self.imageChaser1 = tk.PhotoImage(file='image/chaser1.png')
        self.imageChaser2 = tk.PhotoImage(file='image/chaser2.png')
        self.buttonImage = {
            ButtonType.Grass: self.imageGrass,
            ButtonType.Obstacle: self.imageObstacle,
            ButtonType.Runner: self.imageRunner,
            ButtonType.Chaser1: self.imageChaser1,
            ButtonType.Chaser2: self.imageChaser2
        }
        self.state = []
        self.waitingJob = WaitingJob.SelectRunnerPlace
        self.runner = Agent(0, 0, ButtonType.Runner)
        self.chaser1 = Agent(0, 0, ButtonType.Chaser1)
        self.chaser2 = Agent(0, 0, ButtonType.Chaser2)

        counter = 0
        while counter <= self.columnCount:
            self.window.rowconfigure(counter, weight=1)
            self.window.columnconfigure(counter, weight=1)
            counter += 1

        self.configurationsHeaderLabel = self.makeLabel(self.window, self.configurationFrameHeaderX, self.configurationFrameHeaderY,
                                                        self.generalHeight, self.configurationFrameHeaderWidth,
                                                        text='Configurations',
                                                        bg=self.colorWhite)
        self.runnerPlaceConfigurationLabel = self.makeLabel(self.window, self.configurationFrameEltWidth * 0 + self.boxMargin * 1,
                                                        self.boxMargin * 2 + self.generalHeight * 1,
                                                        self.generalHeight, self.configurationFrameEltWidth,
                                                        text='Runner Place',
                                                        bg=self.colorRunnerPlaceConfiguration)
        self.runnerPlaceDefaultRB = self.makeRadioButton(self.window, self.configurationFrameEltWidth * 0 + self.boxMargin * 1,
                                                        self.boxMargin * 3 + self.generalHeight * 2,
                                                        self.generalHeight, self.configurationFrameEltWidth, text='Default',
                                                        bg=self.colorRunnerPlaceConfiguration, value=1,
                                                        variable=self.runnerPlaceController,
                                                        justify=tk.LEFT)
        self.runnerPlaceRandomRB = self.makeRadioButton(self.window, self.configurationFrameEltWidth * 0 + self.boxMargin * 1,
                                                        self.boxMargin * 4 + self.generalHeight * 3,
                                                        self.generalHeight, self.configurationFrameEltWidth, text='Random',
                                                        bg=self.colorRunnerPlaceConfiguration, value=2,
                                                        variable=self.runnerPlaceController)
        self.runnerPlaceManualRB = self.makeRadioButton(self.window, self.configurationFrameEltWidth * 0 + self.boxMargin * 1,
                                                        self.boxMargin * 5 + self.generalHeight * 4,
                                                        self.generalHeight, self.configurationFrameEltWidth, text='Manual',
                                                        bg=self.colorRunnerPlaceConfiguration, value=3,
                                                        variable=self.runnerPlaceController)
        self.chaserPlaceConfigurationLabel = self.makeLabel(self.window, self.configurationFrameEltWidth * 1 + self.boxMargin * 2,
                                                        self.boxMargin * 2 + self.generalHeight * 1,
                                                        self.generalHeight, self.configurationFrameEltWidth,
                                                        text='Chaser Place',
                                                        bg=self.colorChaserPlaceConfiguration)
        self.chaserPlaceDefaultRB = self.makeRadioButton(self.window, self.configurationFrameEltWidth * 1 + self.boxMargin * 2,
                                                        self.boxMargin * 3 + self.generalHeight * 2,
                                                        self.generalHeight, self.configurationFrameEltWidth, text='Default',
                                                        bg=self.colorChaserPlaceConfiguration, value=1,
                                                        variable=self.chaserPlaceController,
                                                        justify=tk.LEFT)
        self.chaserPlaceRandomRB = self.makeRadioButton(self.window, self.configurationFrameEltWidth * 1 + self.boxMargin * 2,
                                                        self.boxMargin * 4 + self.generalHeight * 3,
                                                        self.generalHeight, self.configurationFrameEltWidth, text='Random',
                                                        bg=self.colorChaserPlaceConfiguration, value=2,
                                                        variable=self.chaserPlaceController)
        self.chaserPlaceManualRB = self.makeRadioButton(self.window, self.configurationFrameEltWidth * 1 + self.boxMargin * 2,
                                                        self.boxMargin * 5 + self.generalHeight * 4,
                                                        self.generalHeight, self.configurationFrameEltWidth, text='Manual',
                                                        bg=self.colorChaserPlaceConfiguration, value=3,
                                                        variable=self.chaserPlaceController)
        self.rockPlaceConfigurationLabel = self.makeLabel(self.window, self.configurationFrameEltWidth * 2 + self.boxMargin * 3,
                                                        self.boxMargin * 2 + self.generalHeight * 1,
                                                        self.generalHeight, self.configurationFrameEltWidth,
                                                        text='Rock Place',
                                                        bg=self.colorRockPlaceConfiguration)
        self.rockPlaceDefaultRB = self.makeRadioButton(self.window, self.configurationFrameEltWidth * 2 + self.boxMargin * 3,
                                                        self.boxMargin * 3 + self.generalHeight * 2,
                                                        self.generalHeight, self.configurationFrameEltWidth, text='Default',
                                                        bg=self.colorRockPlaceConfiguration, value=1,
                                                        variable=self.rockPlaceController,
                                                        justify=tk.LEFT)
        self.rockPlaceRandomRB = self.makeRadioButton(self.window, self.configurationFrameEltWidth * 2 + self.boxMargin * 3,
                                                        self.boxMargin * 4 + self.generalHeight * 3,
                                                        self.generalHeight, self.configurationFrameEltWidth, text='Random',
                                                        bg=self.colorRockPlaceConfiguration, value=2,
                                                        variable=self.rockPlaceController)
        self.rockPlaceManualRB = self.makeRadioButton(self.window, self.configurationFrameEltWidth * 2 + self.boxMargin * 3,
                                                        self.boxMargin * 5 + self.generalHeight * 4,
                                                        self.generalHeight, self.configurationFrameEltWidth, text='Manual',
                                                        bg=self.colorRockPlaceConfiguration, value=3,
                                                        variable=self.rockPlaceController)
        self.runnerBehaviorConfigurationLabel = self.makeLabel(self.window, self.configurationFrameEltWidth * 0 + self.boxMargin * 1,
                                                        self.boxMargin * 6 + self.generalHeight * 5,
                                                        self.generalHeight, self.configurationFrameEltWidth,
                                                        text='Runner Behavior',
                                                        bg=self.colorRunnerBehaviourConfiguration)
        self.runnerBehaviorAutoRB = self.makeRadioButton(self.window, self.configurationFrameEltWidth * 1 + self.boxMargin * 2,
                                                        self.boxMargin * 6 + self.generalHeight * 5,
                                                        self.generalHeight, self.configurationFrameEltWidth, text='Auto',
                                                        bg=self.colorRunnerBehaviourConfiguration, value=1,
                                                        variable=self.runnerController)
        self.runnerBehaviorManualRB = self.makeRadioButton(self.window, self.configurationFrameEltWidth * 2 + self.boxMargin * 3,
                                                        self.boxMargin * 6 + self.generalHeight * 5,
                                                        self.generalHeight, self.configurationFrameEltWidth, text='Manual',
                                                        bg=self.colorRunnerBehaviourConfiguration, value=2,
                                                        variable=self.runnerController)
        self.turn_count_label = self.makeLabel(self.window, self.configurationFrameEltWidth * 0 + self.boxMargin * 1,
                                                        self.boxMargin * 7 + self.generalHeight * 6,
                                                        self.generalHeight, self.configurationFrameEltWidth, text='Turn Count',
                                                        bg=self.colorTurnCountConfiguration)
        self.turn_count_spinbox = self.makeSpinbox(self.window, self.configurationFrameEltWidth * 0 + self.boxMargin * 1,
                                                        self.boxMargin * 8 + self.generalHeight * 7,
                                                        self.generalHeight, self.configurationFrameEltWidth,
                                                        textvariable=self.turnCount, from_=10, to=1000)
        self.rock_count_label = self.makeLabel(self.window, self.configurationFrameEltWidth * 1 + self.boxMargin * 2,
                                                        self.boxMargin * 7 + self.generalHeight * 6,
                                                        self.generalHeight, self.configurationFrameEltWidth, text='Rock Count',
                                                        bg=self.colorRockCountConfiguration)
        self.rock_count_spinbox = self.makeSpinbox(self.window, self.configurationFrameEltWidth * 1 + self.boxMargin * 2,
                                                        self.boxMargin * 8 + self.generalHeight * 7,
                                                        self.generalHeight, self.configurationFrameEltWidth,
                                                        textvariable=self.rockCount, from_=1, to=50)
        self.apply_configuration_button = self.makeButton(self.window, self.configurationFrameEltWidth * 2 + self.boxMargin * 3,
                                                        self.boxMargin * 7 + self.generalHeight * 6,
                                                        self.generalHeight * 2 + self.boxMargin, self.configurationFrameEltWidth,
                                                        text='Apply\nConfiguration', bg='blue', fg=self.colorWhite, font=self.buttonFont)
        self.elts = []
        for row in range(self.rowCount + 1):
            self.elts.append([])
            for column in range(self.columnCount + 1):
                elt = 0
                x = self.boxMargin + column * (self.boxWidth + self.boxMargin)
                y = self.boardTopMargin + self.boxMargin + row * (self.boxWidth + self.boxMargin)
                if row == 0 and column == 0:
                    elt = self.makeLabel(self.window, x, y, self.boxHeight, self.boxWidth, bg=self.colorBlack)
                elif row == 0:
                    elt = self.makeLabel(self.window, x, y, self.boxHeight, self.boxWidth, bg=self.colorWhite,
                                         font=self.boxFont, text=ut.numToChar(column))
                elif column == 0:
                    elt = self.makeLabel(self.window, x, y, self.boxHeight, self.boxWidth, bg=self.colorWhite, font=self.boxFont, text=str(row))
                else:
                    button_type = 'grass'
                    elt = self.makeButton(self.window, x, y, self.boxHeight, self.boxWidth,
                                          image=self.imageGrass, text=ut.rowColumnTypeToString(row, column, button_type))
                    elt.bind('<1>', self.clickedButton)
                self.elts[row].append(elt)

        self.initializeState()
        self.window.mainloop()

    def initializeState(self):
        for row in range(self.rowCount + 1):
            self.state.append([])
            for column in range(self.columnCount + 1):
                if (row == 0 or column == 0):
                    self.state[row].append(ButtonType.Header)
                else:
                    self.state[row].append(ButtonType.Grass)

    def moveAgent(self, row, column, buttonType, oldRow=0, oldColumn=0):
        if oldRow > 0:
            self.configureButton(self.elts[oldRow][oldColumn], ButtonType.Grass)
            self.state[oldRow][oldColumn] = ButtonType.Grass
        self.configureButton(self.elts[row][column], buttonType)
        self.state[row][column] = buttonType

    def clickedButton(self, event):
        row_column = ut.stringToRowColumn(event.widget['text'])
        row = row_column[0]
        column = row_column[1]
        print('Initial Waiting Job:', self.waitingJob)
        if self.waitingJob == WaitingJob.SelectRunnerPlace:
            self.moveAgent(row, column, ButtonType.Runner)
            self.waitingJob = WaitingJob.SelectChaser1Place
            self.runner.row = row
            self.runner.column = column
        elif self.waitingJob == WaitingJob.SelectChaser1Place:
            self.moveAgent(row, column, ButtonType.Chaser1)
            self.waitingJob = WaitingJob.SelectChaser2Place
        elif self.waitingJob == WaitingJob.SelectChaser2Place:
            self.moveAgent(row, column, ButtonType.Chaser2)
            self.waitingJob = WaitingJob.SelectRockPlace
        elif self.waitingJob == WaitingJob.SelectRockPlace:
            self.moveAgent(row, column, ButtonType.Obstacle)
            self.rockCounter += 1
            if self.rockCount.get() == self.rockCounter:
                self.waitingJob = WaitingJob.NoWaitingJob
        print('Final Waiting Job:', self.waitingJob)

    def makeLabel(self, master, x, y, h, w, *args, **kwargs):
        frame = tk.Frame(master, height=h, width=w)
        frame.pack_propagate(0)
        frame.place(x=x, y=y)
        label = tk.Label(frame, *args, **kwargs)
        label.pack(fill=tk.BOTH, expand=1)
        return label

    # button maker
    def makeButton(self, master, x, y, h, w, *args, **kwargs):
        frame = tk.Frame(master, height=h, width=w)
        frame.pack_propagate(0)
        frame.place(x=x, y=y)
        button = tk.Button(frame, *args, **kwargs)
        button.pack(fill=tk.BOTH, expand=1)
        return button

    # radiobutton maker
    def makeRadioButton(self, master, x, y, h, w, *args, **kwargs):
        frame = tk.Frame(master, height=h, width=w)
        frame.pack_propagate(0)
        frame.place(x=x, y=y)
        radiobutton = tk.Radiobutton(frame, *args, **kwargs)
        radiobutton.pack(fill=tk.BOTH, expand=1)
        return radiobutton

    # spinbox maker
    def makeSpinbox(self, master, x, y, h, w, *args, **kwargs):
        frame = tk.Frame(master, height=h, width=w)
        frame.pack_propagate(0)
        frame.place(x=x, y=y)
        spinbox = tk.Spinbox(frame, *args, **kwargs)
        spinbox.pack(fill=tk.BOTH, expand=1)
        return spinbox

    def configureButton(self, button, buttonType):
        button.configure(image=self.buttonImage[buttonType])
        button.buttonType = buttonType