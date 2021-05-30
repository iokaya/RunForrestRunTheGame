# import libraries
import time
import tkinter as tk
import utils as ut
import pandas as pd
import numpy as np
import pickle
from PIL import Image, ImageTk
from Enums import ButtonType, WaitingJob, PlaceConfig, BehaviorConfig
from agent import Agent

class Board(tk.Frame):
    def __init__(self, boxHeight, boxWidth, boxMargin, rowCount, columnCount, master=None, alpha=0.1, gamma=0.9, epsilon=0.1, episode_count=500, game_sleep=0.1, training_sleep=0.0001):
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
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.game_sleep = game_sleep
        self.training_sleep = training_sleep
        self.boardTopMargin = self.windowHeight - (self.rowCount + 1) * self.boxHeight - (
                    self.rowCount + 2) * self.boxMargin
        self.generalHeight = (self.boardTopMargin - 8 * self.boxMargin) / 8
        self.configurationFrameHeaderWidth = (self.windowWidth - 3 * self.boxMargin) * 0.5
        self.configurationFrameHeaderX = self.boxMargin
        self.configurationFrameHeaderY = self.boxMargin
        self.consoleHeaderX = self.boxMargin * 2 + self.configurationFrameHeaderWidth
        self.consoleHeaderY = self.boxMargin
        self.configurationFrameEltWidth = (self.configurationFrameHeaderWidth - 2 * self.boxMargin) / 3
        self.window = master
        self.runnerController = tk.IntVar()
        self.runnerController.set(BehaviorConfig.Auto.value)
        self.runnerPlaceController = tk.IntVar()
        self.runnerPlaceController.set(PlaceConfig.Random.value)
        self.chaserPlaceController = tk.IntVar()
        self.chaserPlaceController.set(PlaceConfig.Random.value)
        self.obstaclePlaceController = tk.IntVar()
        self.obstaclePlaceController.set(PlaceConfig.Random.value)
        self.obstacleCount = tk.IntVar()
        self.obstacleCount.set(20)
        self.obstacleCounter = 0
        self.turnCount = tk.IntVar()
        self.turnCount.set(100)
        self.turnCounter = 0
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
        self.original_agent_states = {}
        self.waitingJob = WaitingJob.ApplyConfiguration

        self.isRunnerCaught = False

        self.default_q_table = pd.DataFrame(
            0,
            index=pd.MultiIndex.from_product([list(range(1, rowCount+1)), list(range(1, columnCount+1))]),
            columns=['NO MOVE', 'NORTH', 'EAST', 'SOUTH', 'WEST']
        )

        self.runner = Agent(0, 0, ButtonType.Runner, self.default_q_table.copy())
        self.chaser1 = Agent(0, 0, ButtonType.Chaser1, self.default_q_table.copy())
        self.chaser2 = Agent(0, 0, ButtonType.Chaser2, self.default_q_table.copy())
        #self.runner = Agent(0, 0, ButtonType.Runner, pd.read_pickle('pickle/runner_' + str(self.rowCount) + '_' + str(self.columnCount) + '.pkl'))
        #self.chaser1 = Agent(0, 0, ButtonType.Chaser1, pd.read_pickle('pickle/chaser1_' + str(self.rowCount) + '_' + str(self.columnCount) + '.pkl'))
        #self.chaser2 = Agent(0, 0, ButtonType.Chaser2, pd.read_pickle('pickle/chaser2_' + str(self.rowCount) + '_' + str(self.columnCount) + '.pkl'))

        self.runnerDefaultPlace = (1, 1)
        self.chaser1DefaultPlace = (self.rowCount, self.columnCount)
        self.chaser2DefaultPlace = (self.rowCount, self.columnCount-1)

        self.applyConfigButtonList = []

        self.isTraining = False
        self.episode_count = episode_count
        self.episode_counter = 0

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
                                                        bg=self.colorRunnerPlaceConfiguration, value=PlaceConfig.Default.value,
                                                        variable=self.runnerPlaceController,
                                                        justify=tk.LEFT)
        self.runnerPlaceRandomRB = self.makeRadioButton(self.window, self.configurationFrameEltWidth * 0 + self.boxMargin * 1,
                                                        self.boxMargin * 4 + self.generalHeight * 3,
                                                        self.generalHeight, self.configurationFrameEltWidth, text='Random',
                                                        bg=self.colorRunnerPlaceConfiguration, value=PlaceConfig.Random.value,
                                                        variable=self.runnerPlaceController)
        self.runnerPlaceManualRB = self.makeRadioButton(self.window, self.configurationFrameEltWidth * 0 + self.boxMargin * 1,
                                                        self.boxMargin * 5 + self.generalHeight * 4,
                                                        self.generalHeight, self.configurationFrameEltWidth, text='Manual',
                                                        bg=self.colorRunnerPlaceConfiguration, value=PlaceConfig.Manual.value,
                                                        variable=self.runnerPlaceController)
        self.chaserPlaceConfigurationLabel = self.makeLabel(self.window, self.configurationFrameEltWidth * 1 + self.boxMargin * 2,
                                                        self.boxMargin * 2 + self.generalHeight * 1,
                                                        self.generalHeight, self.configurationFrameEltWidth,
                                                        text='Chaser Place',
                                                        bg=self.colorChaserPlaceConfiguration)
        self.chaserPlaceDefaultRB = self.makeRadioButton(self.window, self.configurationFrameEltWidth * 1 + self.boxMargin * 2,
                                                        self.boxMargin * 3 + self.generalHeight * 2,
                                                        self.generalHeight, self.configurationFrameEltWidth, text='Default',
                                                        bg=self.colorChaserPlaceConfiguration, value=PlaceConfig.Default.value,
                                                        variable=self.chaserPlaceController,
                                                        justify=tk.LEFT)
        self.chaserPlaceRandomRB = self.makeRadioButton(self.window, self.configurationFrameEltWidth * 1 + self.boxMargin * 2,
                                                        self.boxMargin * 4 + self.generalHeight * 3,
                                                        self.generalHeight, self.configurationFrameEltWidth, text='Random',
                                                        bg=self.colorChaserPlaceConfiguration, value=PlaceConfig.Random.value,
                                                        variable=self.chaserPlaceController)
        self.chaserPlaceManualRB = self.makeRadioButton(self.window, self.configurationFrameEltWidth * 1 + self.boxMargin * 2,
                                                        self.boxMargin * 5 + self.generalHeight * 4,
                                                        self.generalHeight, self.configurationFrameEltWidth, text='Manual',
                                                        bg=self.colorChaserPlaceConfiguration, value=PlaceConfig.Manual.value,
                                                        variable=self.chaserPlaceController)
        self.rockPlaceConfigurationLabel = self.makeLabel(self.window, self.configurationFrameEltWidth * 2 + self.boxMargin * 3,
                                                        self.boxMargin * 2 + self.generalHeight * 1,
                                                        self.generalHeight, self.configurationFrameEltWidth,
                                                        text='Rock Place',
                                                        bg=self.colorRockPlaceConfiguration)
        self.rockPlaceDefaultRB = self.makeRadioButton(self.window, self.configurationFrameEltWidth * 2 + self.boxMargin * 3,
                                                        self.boxMargin * 3 + self.generalHeight * 2,
                                                        self.generalHeight, self.configurationFrameEltWidth, text='Default',
                                                        bg=self.colorRockPlaceConfiguration, value=PlaceConfig.Default.value,
                                                        variable=self.obstaclePlaceController,
                                                        justify=tk.LEFT)
        self.rockPlaceRandomRB = self.makeRadioButton(self.window, self.configurationFrameEltWidth * 2 + self.boxMargin * 3,
                                                        self.boxMargin * 4 + self.generalHeight * 3,
                                                        self.generalHeight, self.configurationFrameEltWidth, text='Random',
                                                        bg=self.colorRockPlaceConfiguration, value=PlaceConfig.Random.value,
                                                        variable=self.obstaclePlaceController)
        self.rockPlaceManualRB = self.makeRadioButton(self.window, self.configurationFrameEltWidth * 2 + self.boxMargin * 3,
                                                        self.boxMargin * 5 + self.generalHeight * 4,
                                                        self.generalHeight, self.configurationFrameEltWidth, text='Manual',
                                                        bg=self.colorRockPlaceConfiguration, value=PlaceConfig.Manual.value,
                                                        variable=self.obstaclePlaceController)
        self.runnerBehaviorConfigurationLabel = self.makeLabel(self.window, self.configurationFrameEltWidth * 0 + self.boxMargin * 1,
                                                        self.boxMargin * 6 + self.generalHeight * 5,
                                                        self.generalHeight, self.configurationFrameEltWidth,
                                                        text='Runner Behavior',
                                                        bg=self.colorRunnerBehaviourConfiguration)
        self.runnerBehaviorAutoRB = self.makeRadioButton(self.window, self.configurationFrameEltWidth * 1 + self.boxMargin * 2,
                                                        self.boxMargin * 6 + self.generalHeight * 5,
                                                        self.generalHeight, self.configurationFrameEltWidth, text='Auto',
                                                        bg=self.colorRunnerBehaviourConfiguration, value=BehaviorConfig.Auto.value,
                                                        variable=self.runnerController)
        self.runnerBehaviorManualRB = self.makeRadioButton(self.window, self.configurationFrameEltWidth * 2 + self.boxMargin * 3,
                                                        self.boxMargin * 6 + self.generalHeight * 5,
                                                        self.generalHeight, self.configurationFrameEltWidth, text='Manual',
                                                        bg=self.colorRunnerBehaviourConfiguration, value=BehaviorConfig.Manual.value,
                                                        variable=self.runnerController)
        self.turnCountLabel = self.makeLabel(self.window, self.configurationFrameEltWidth * 0 + self.boxMargin * 1,
                                                        self.boxMargin * 7 + self.generalHeight * 6,
                                                        self.generalHeight, self.configurationFrameEltWidth, text='Turn Count',
                                                        bg=self.colorTurnCountConfiguration)
        self.turnCountSpinbox = self.makeSpinbox(self.window, self.configurationFrameEltWidth * 0 + self.boxMargin * 1,
                                                        self.boxMargin * 8 + self.generalHeight * 7,
                                                        self.generalHeight, self.configurationFrameEltWidth,
                                                        textvariable=self.turnCount, from_=10, to=1000)
        self.obstacleCountLabel = self.makeLabel(self.window, self.configurationFrameEltWidth * 1 + self.boxMargin * 2,
                                                        self.boxMargin * 7 + self.generalHeight * 6,
                                                        self.generalHeight, self.configurationFrameEltWidth, text='Obstacle Count',
                                                        bg=self.colorRockCountConfiguration)
        self.obstacleCountSpinbox = self.makeSpinbox(self.window, self.configurationFrameEltWidth * 1 + self.boxMargin * 2,
                                                        self.boxMargin * 8 + self.generalHeight * 7,
                                                        self.generalHeight, self.configurationFrameEltWidth,
                                                        textvariable=self.obstacleCount, from_=1, to=50)
        self.applyConfigurationButton = self.makeButton(self.window, self.configurationFrameEltWidth * 2 + self.boxMargin * 3,
                                                        self.boxMargin * 7 + self.generalHeight * 6,
                                                        self.generalHeight * 2 + self.boxMargin, self.configurationFrameEltWidth,
                                                        ButtonType.ApplyConfig, text='Apply\nConfiguration', bg='blue',
                                                        fg=self.colorWhite, font=self.buttonFont)
        self.console = self.makeTextbox(self.window, self.consoleHeaderX,
                                                        self.consoleHeaderY,
                                                        self.windowHeight - (self.rowCount + 6)*self.boxMargin - (self.rowCount + 1) * self.boxHeight - self.generalHeight * 3,
                                                        self.configurationFrameHeaderWidth, bg='light yellow')
        self.runnerScoreLabel = self.makeLabel(self.window, self.configurationFrameEltWidth * 3 + self.boxMargin * 4,
                                                        self.boxMargin * 6 + self.generalHeight * 5,
                                                        self.generalHeight, self.configurationFrameEltWidth,
                                                        text='Runner Score',
                                                        bg=self.colorWhite)
        self.runnerScoreBoard = self.makeLabel(self.window, self.configurationFrameEltWidth * 3 + self.boxMargin * 4,
                                                        self.boxMargin * 7 + self.generalHeight * 6,
                                                        self.generalHeight, self.configurationFrameEltWidth,
                                                        text='0',
                                                        bg=self.colorWhite)
        self.chaser1ScoreLabel = self.makeLabel(self.window, self.configurationFrameEltWidth * 4 + self.boxMargin * 5,
                                                        self.boxMargin * 6 + self.generalHeight * 5,
                                                        self.generalHeight, self.configurationFrameEltWidth,
                                                        text='Chaser 1 Score',
                                                        bg=self.colorWhite)
        self.chaser1ScoreBoard = self.makeLabel(self.window, self.configurationFrameEltWidth * 4 + self.boxMargin * 5,
                                                        self.boxMargin * 7 + self.generalHeight * 6,
                                                        self.generalHeight, self.configurationFrameEltWidth,
                                                        text='0',
                                                        bg=self.colorWhite)
        self.chaser2ScoreLabel = self.makeLabel(self.window, self.configurationFrameEltWidth * 5 + self.boxMargin * 6,
                                                        self.boxMargin * 6 + self.generalHeight * 5,
                                                        self.generalHeight, self.configurationFrameEltWidth,
                                                        text='Chaser 2 Score',
                                                        bg=self.colorWhite)
        self.chaser2ScoreBoard = self.makeLabel(self.window, self.configurationFrameEltWidth * 5 + self.boxMargin * 6,
                                                        self.boxMargin * 7 + self.generalHeight * 6,
                                                        self.generalHeight, self.configurationFrameEltWidth,
                                                        text='0',
                                                        bg=self.colorWhite)
        self.startGameButton = self.makeButton(self.window, self.configurationFrameEltWidth * 3 + self.boxMargin * 4,
                                                        self.boxMargin * 8 + self.generalHeight * 7,
                                                        self.generalHeight, self.configurationFrameEltWidth * 1.5 + self.boxMargin * 1,
                                                        ButtonType.StartGame, text='Start Game', bg='blue',
                                                        fg=self.colorWhite, font=self.buttonFont, state='disabled')
        self.trainAgentsButton = self.makeButton(self.window, self.configurationFrameEltWidth * 4.5 + self.boxMargin * 5,
                                                        self.boxMargin * 8 + self.generalHeight * 7,
                                                        self.generalHeight,
                                                        self.configurationFrameEltWidth * 1.5 + self.boxMargin * 1,
                                                        ButtonType.StartGame, text='Train Agents', bg='yellow',
                                                        fg=self.colorWhite, font=self.buttonFont, state='disabled')

        self.applyConfigurationButton.bind('<1>', self.handleEvent)
        self.startGameButton.bind('<1>', self.handleEvent)
        self.trainAgentsButton.bind('<1>', self.trainAgents)

        self.applyConfigButtonList.append(self.runnerPlaceDefaultRB)
        self.applyConfigButtonList.append(self.runnerPlaceRandomRB)
        self.applyConfigButtonList.append(self.runnerPlaceManualRB)
        self.applyConfigButtonList.append(self.chaserPlaceDefaultRB)
        self.applyConfigButtonList.append(self.chaserPlaceRandomRB)
        self.applyConfigButtonList.append(self.chaserPlaceManualRB)
        self.applyConfigButtonList.append(self.rockPlaceDefaultRB)
        self.applyConfigButtonList.append(self.rockPlaceRandomRB)
        self.applyConfigButtonList.append(self.rockPlaceManualRB)
        self.applyConfigButtonList.append(self.runnerBehaviorAutoRB)
        self.applyConfigButtonList.append(self.runnerBehaviorManualRB)
        self.applyConfigButtonList.append(self.turnCountSpinbox)
        self.applyConfigButtonList.append(self.obstacleCountSpinbox)
        self.applyConfigButtonList.append(self.applyConfigurationButton)

        self.elts = []

        self.appendToConsole('Welcome to the RL Game - Run Forrest Run!!')
        self.appendToConsole('Waiting for configuration...')
        self.initializeElts()
        self.initializeState()
        self.window.mainloop()

    def resetGame(self):
        self.isRunnerCaught = False
        self.waitingJob = WaitingJob.StartGame
        self.startGameButton['state'] = 'normal'
        self.turnCounter = 0
        self.runnerScoreBoard['text'] = 0
        self.chaser1ScoreBoard['text'] = 0
        self.chaser2ScoreBoard['text'] = 0
        self.moveAgent(
            self.original_agent_states[self.runner.buttonType.value][0],
            self.original_agent_states[self.runner.buttonType.value][1],
            self.runner
        )
        self.moveAgent(
            self.original_agent_states[self.chaser1.buttonType.value][0],
            self.original_agent_states[self.chaser1.buttonType.value][1],
            self.chaser1
        )
        self.moveAgent(
            self.original_agent_states[self.chaser2.buttonType.value][0],
            self.original_agent_states[self.chaser2.buttonType.value][1],
            self.chaser2
        )
        self.runner.score = 0
        self.chaser1.score = 0
        self.chaser2.score = 0

    def trainAgents(self, event):
        for i in range(self.episode_count):
            self.handleEvent(event)

    def setWaitingJob(self):
        if self.waitingJob == WaitingJob.ApplyConfiguration:
            self.waitingJob = WaitingJob.SelectRunnerPlace
        elif self.waitingJob == WaitingJob.SelectRunnerPlace:
            self.waitingJob = WaitingJob.SelectChaser1Place
        elif self.waitingJob == WaitingJob.SelectChaser1Place:
            self.waitingJob = WaitingJob.SelectChaser2Place
        elif self.waitingJob == WaitingJob.SelectChaser2Place:
            self.waitingJob = WaitingJob.SelectObstaclePlace
        elif self.waitingJob == WaitingJob.SelectObstaclePlace:
            if ut.getElementCount(self.state, ButtonType.Obstacle) == self.obstacleCount.get():
                self.waitingJob = WaitingJob.StartGame
                self.startGameButton['state'] = 'normal'
                self.trainAgentsButton['state'] = 'normal'
        elif self.waitingJob == WaitingJob.StartGame:
            self.waitingJob = WaitingJob.PlayRunner
        elif self.waitingJob == WaitingJob.PlayRunner:
            self.waitingJob = WaitingJob.PlayChaser1
        elif self.waitingJob == WaitingJob.PlayChaser1:
            self.waitingJob = WaitingJob.PlayChaser2
        elif self.waitingJob == WaitingJob.PlayChaser2:
            if self.turnCounter <= self.turnCount.get() and not self.isRunnerCaught:
                self.waitingJob = WaitingJob.PlayRunner
            else:
                self.resetGame()
                self.runner.q_table.to_csv('csv/runner.csv')
                self.chaser1.q_table.to_csv('csv/chaser1.csv')
                self.chaser2.q_table.to_csv('csv/chaser2.csv')
                self.runner.q_table.to_pickle('pickle/runner_' + str(self.rowCount) + '_' + str(self.columnCount) + '.pkl')
                self.chaser1.q_table.to_pickle('pickle/chaser1_' + str(self.rowCount) + '_' + str(self.columnCount) + '.pkl')
                self.chaser2.q_table.to_pickle('pickle/chaser2_' + str(self.rowCount) + '_' + str(self.columnCount) + '.pkl')
        else:
            self.waitingJob = WaitingJob.NoWaitingJob

    def initializeElts(self):
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
                    elt = self.makeButton(self.window, x, y, self.boxHeight, self.boxWidth, ButtonType.Grass,
                                          image=self.imageGrass, text=ut.rowColumnTypeToString(row, column, button_type))
                    #elt.bind('<1>', self.clickedButton)
                    elt.bind('<1>', self.handleEvent)
                self.elts[row].append(elt)

    def initializeState(self):
        for row in range(self.rowCount + 1):
            self.state.append([])
            for column in range(self.columnCount + 1):
                if (row == 0 or column == 0):
                    self.state[row].append(ButtonType.Header)
                else:
                    self.state[row].append(ButtonType.Grass)

    def moveAgent(self, row, column, agent, action='NO ACTION'):
        oldState = agent.changeAgentState(row, column)

        if oldState == (0, 0):
            self.original_agent_states[agent.buttonType.value] = row, column

        self.configureButton(self.elts[row][column], agent.buttonType)
        self.state[row][column] = agent.buttonType
        if oldState[0] > 0 and action != 'NO MOVE':
            self.configureButton(self.elts[oldState[0]][oldState[1]], ButtonType.Grass)
            self.state[oldState[0]][oldState[1]] = ButtonType.Grass

    def placeObstacle(self, row, column):
        if self.state[row][column] == ButtonType.Grass:
            self.configureButton(self.elts[row][column], ButtonType.Obstacle)
            self.state[row][column] = ButtonType.Obstacle

    def clickedButton(self, event):
        row_column = ut.stringToRowColumn(event.widget['text'])
        row = row_column[0]
        column = row_column[1]
        if self.waitingJob == WaitingJob.SelectRunnerPlace:
            self.moveAgent(row, column, self.runner)
            self.setWaitingJob()
        elif self.waitingJob == WaitingJob.SelectChaser1Place:
            self.moveAgent(row, column, self.chaser1)
            self.setWaitingJob()
        elif self.waitingJob == WaitingJob.SelectChaser2Place:
            self.moveAgent(row, column, self.chaser2)
            self.setWaitingJob()
        elif self.waitingJob == WaitingJob.SelectObstaclePlace:
            self.placeObstacle(row, column)
            self.setWaitingJob()

    def handleEvent(self, event):
        actionTaken = False
        actionStr = ''
        buttonType = event.widget.buttonType
        if buttonType == ButtonType.ApplyConfig:
            self.disableButtons()
            actionTaken = True
        elif buttonType == ButtonType.StartGame:
            self.startGameButton['state'] = 'disabled'
            actionStr = 'Game Started!! Enjoy!!'
            actionTaken = True
        else:
            row = ut.stringToRowColumn(event.widget['text'])[0]
            column = ut.stringToRowColumn(event.widget['text'])[1]
            if self.waitingJob == WaitingJob.SelectRunnerPlace and self.runnerPlaceController.get() == PlaceConfig.Manual.value:
                self.moveAgent(row, column, self.runner)
                actionTaken = True
                actionStr = 'Waiting for Chaser 1 Place...'
            elif self.waitingJob == WaitingJob.SelectChaser1Place and self.chaserPlaceController.get() == PlaceConfig.Manual.value:
                self.moveAgent(row, column, self.chaser1)
                actionTaken = True
                actionStr = 'Waiting for Chaser 2 Place...'
            elif self.waitingJob == WaitingJob.SelectChaser2Place and self.chaserPlaceController.get() == PlaceConfig.Manual.value:
                self.moveAgent(row, column, self.chaser2)
                actionTaken = True
                actionStr = 'Waiting for Obstacle Places...'
            elif self.waitingJob == WaitingJob.SelectObstaclePlace and self.obstaclePlaceController.get() == PlaceConfig.Manual.value:
                self.placeObstacle(row, column)
                #actionStr = 'Waiting for game to start...\nConfiguration Applied!'
                actionTaken = True
            elif self.waitingJob == WaitingJob.PlayRunner and self.runnerController.get() == BehaviorConfig.Manual.value:
                actionTaken = True

        if actionTaken:
            self.afterActionHandler(actionStr)

    def afterActionHandler(self, logStr):
        if logStr != '':
            self.appendToConsole(logStr)
        self.window.update()
        if self.isTraining:
            time.sleep(self.training_sleep)
        else:
            time.sleep(self.game_sleep)
        self.setWaitingJob()
        self.actionDecider()

    def actionDecider(self):
        actionTaken = False
        if self.waitingJob == WaitingJob.SelectRunnerPlace:
            if self.runnerPlaceController.get() == PlaceConfig.Random.value:
                row, column = ut.getRandomPlace(self.state)
                self.moveAgent(row, column, self.runner)
                actionTaken = True
            elif self.runnerPlaceController.get() == PlaceConfig.Default.value:
                self.moveAgent(self.runnerDefaultPlace[0], self.runnerDefaultPlace[1], self.runner)
                actionTaken = True
        elif self.waitingJob == WaitingJob.SelectChaser1Place:
            if self.chaserPlaceController.get() == PlaceConfig.Random.value:
                row, column = ut.getRandomPlace(self.state)
                self.moveAgent(row, column, self.chaser1)
                actionTaken = True
            elif self.chaserPlaceController.get() == PlaceConfig.Default.value:
                self.moveAgent(self.chaser1DefaultPlace[0], self.chaser1DefaultPlace[1], self.chaser1)
                actionTaken = True
        elif self.waitingJob == WaitingJob.SelectChaser2Place:
            if self.chaserPlaceController.get() == PlaceConfig.Random.value:
                row, column = ut.getRandomPlace(self.state)
                self.moveAgent(row, column, self.chaser2)
                actionTaken = True
            elif self.chaserPlaceController.get() == PlaceConfig.Default.value:
                self.moveAgent(self.chaser2DefaultPlace[0], self.chaser2DefaultPlace[1], self.chaser2)
                actionTaken = True
        elif self.waitingJob == WaitingJob.SelectObstaclePlace:
            if self.obstaclePlaceController.get() in [PlaceConfig.Random.value, PlaceConfig.Default.value]:
                row, column = ut.getRandomPlace(self.state)
                self.placeObstacle(row, column)
                actionTaken = True
        elif self.waitingJob == WaitingJob.PlayRunner:
            self.step(self.runner)
            actionTaken = True
        elif self.waitingJob == WaitingJob.PlayChaser1:
            self.step(self.chaser1)
            actionTaken = True
        elif self.waitingJob == WaitingJob.PlayChaser2:
            self.step(self.chaser2)
            self.turnCounter += 1
            actionTaken = True
        elif self.isTraining:
            self.trainAgentsButton.invoke()


        if actionTaken:
            self.afterActionHandler('')

    def makeLabel(self, master, x, y, h, w, *args, **kwargs):
        frame = tk.Frame(master, height=h, width=w)
        frame.pack_propagate(0)
        frame.place(x=x, y=y)
        label = tk.Label(frame, *args, **kwargs)
        label.pack(fill=tk.BOTH, expand=1)
        return label

    # button maker
    def makeButton(self, master, x, y, h, w, buttonType, *args, **kwargs):
        frame = tk.Frame(master, height=h, width=w)
        frame.pack_propagate(0)
        frame.place(x=x, y=y)
        button = tk.Button(frame, *args, **kwargs)
        button.pack(fill=tk.BOTH, expand=1)
        button.buttonType = buttonType
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

    # textbox maker
    def makeTextbox(self, master, x, y, h, w, *args, **kwargs):
        frame = tk.Frame(master, height=h, width=w)
        frame.pack_propagate(0)
        frame.place(x=x, y=y)
        textbox = tk.Text(frame, *args, **kwargs)
        textbox.pack(fill=tk.BOTH, expand=1)
        return textbox

    def configureButton(self, button, buttonType):
        button.configure(image=self.buttonImage[buttonType])
        button.buttonType = buttonType

    def disableButtons(self):
        for elt in self.applyConfigButtonList:
            elt['state'] = 'disabled'

    def enableButtons(self):
        for elt in self.applyConfigButtonList:
            elt['state'] = 'normal'

    def appendToConsole(self, str):
        self.console.insert('1.0', str + '\n')

    def step(self, agent):
        state = agent.position()
        agent.detectPossibleMoves(self.state)
        possibleMoves = agent.possibleMoves
        q_table = agent.q_table
        reward = 0
        if np.random.uniform() <= self.epsilon or (q_table.loc[state, possibleMoves] == 0).all():
            action = np.random.choice(possibleMoves)
        else:
            action = q_table.loc[state, possibleMoves].index[q_table.loc[state, possibleMoves].values.argmax()]
        next_state = ut.nextState(state, action)
        if agent.buttonType == ButtonType.Runner:
            #reward = ut.getRunnerReward(self.runner.position(), self.chaser1.position(), self.chaser2.position())
            reward = ut.getRunnerReward(next_state, self.chaser1.position(), self.chaser2.position())
        elif agent.buttonType == ButtonType.Chaser1:
            #reward = ut.getChaserReward(self.runner.position(), self.chaser1.position())
            reward = ut.getChaserReward(self.runner.position(), next_state)
        else:
            #reward = ut.getChaserReward(self.runner.position(), self.chaser2.position())
            reward = ut.getChaserReward(self.runner.position(), next_state)
        current_q = agent.q_table.loc[state, action]
        next_q = agent.q_table.loc[next_state, :].max()
        agent.q_table.loc[state, action] += self.alpha * (reward + self.gamma * next_q - current_q)
        agent.score += reward
        if agent.buttonType == ButtonType.Runner:
            self.runnerScoreBoard['text'] = int(agent.score)
        elif agent.buttonType == ButtonType.Chaser1:
            self.chaser1ScoreBoard['text'] = int(agent.score)
        else:
            self.chaser2ScoreBoard['text'] = int(agent.score)

        self.moveAgent(next_state[0], next_state[1], agent, action)

        if self.runner.position() in [self.chaser1.position(), self.chaser2.position()]:
            self.isRunnerCaught = True
