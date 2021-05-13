# import libraries
import enum
import tkinter as tk
from PIL import Image, ImageTk


class WaitingJob(enum.Enum):
    NoWaitingJob = 0
    SelectRunnerPlace = 1
    SelectChaser1Place = 2
    SelectChaser2Place = 3
    SelectRockPlace = 4

class Utils:
    colorBlack = '#000000'
    windowTitle = 'Run Forrest Run!! The RL Game'
    colorBlack = '#000000'
    colorWhite = '#FAFAFA'
    colorGray = '#B9B9B9'
    colorRunner = '#0A9F23'
    colorChaser = '#9F0A0A'
    colorRunnerPlaceConfiguration = '#B5FFB9'
    colorChaserPlaceConfiguration = '#FFB5B5'
    colorRockPlaceConfiguration = '#B5ECFF'
    colorRunnerBehaviourConfiguration = '#F8B5FF'
    colorRockCountConfiguration = '#FFFFB5'
    colorTurnCountConfiguration = '#B5CFFF'
    buttonGrassText = 'grass'
    buttonRockText = 'rock'
    buttonRunnerText = 'runner'
    buttonChaser1Text = 'chaser1'
    buttonChaser2Text = 'chaser2'
    boxFont = ("Calibri", 22)
    buttonFont = ("Calibri", 12)
    asciiCapitalLettersStartNum = 64
    imageGrass = tk.PhotoImage(file='image/grass.png')
    imageRock = tk.PhotoImage(file='image/rock.png')
    imageRunner = tk.PhotoImage(file='image/runner.png')
    imageChaser1 = tk.PhotoImage(file='image/chaser1.png')
    imageChaser2 = tk.PhotoImage(file='image/chaser2.png')

    def rowColumnTypeToString(row, column, button_type):
        return str(row) + '_' + str(column) + '_' + button_type

    def stringToRowColumn(rc_str):
        return int(rc_str.split('_')[0]), int(rc_str.split('_')[1])

    def numToChar(self, num):
        return chr(self.asciiCapitalLettersStartNum + num)

    def charToNum(self, char):
        return int(char.upper()) - self.asciiCapitalLettersStartNum

    def makeLabel(master, x, y, h, w, *args, **kwargs):
        frame = tk.Frame(master, height=h, width=w)
        frame.pack_propagate(0)
        frame.place(x=x, y=y)
        label = tk.Label(frame, *args, **kwargs)
        label.pack(fill=tk.BOTH, expand=1)
        return label

    # button maker
    def makeButton(master, x, y, h, w, *args, **kwargs):
        frame = tk.Frame(master, height=h, width=w)
        frame.pack_propagate(0)
        frame.place(x=x, y=y)
        button = tk.Button(frame, *args, **kwargs)
        button.pack(fill=tk.BOTH, expand=1)
        return button

    # radiobutton maker
    def makeRadioButton(master, x, y, h, w, *args, **kwargs):
        frame = tk.Frame(master, height=h, width=w)
        frame.pack_propagate(0)
        frame.place(x=x, y=y)
        radiobutton = tk.Radiobutton(frame, *args, **kwargs)
        radiobutton.pack(fill=tk.BOTH, expand=1)
        return radiobutton

    # spinbox maker
    def makeSpinbox(master, x, y, h, w, *args, **kwargs):
        frame = tk.Frame(master, height=h, width=w)
        frame.pack_propagate(0)
        frame.place(x=x, y=y)
        spinbox = tk.Spinbox(frame, *args, **kwargs)
        spinbox.pack(fill=tk.BOTH, expand=1)
        return spinbox

    def configure_button(button, image, button_type):
        button.configure(image=image)
        row_column = Utils.stringToRowColumn(button['text'])

    def to_runner(self, button):
        self.configure_button(button, self.runnerImage, self.buttonRunnerText)

    def to_chaser1(self, button):
        self.configure_button(button, self.imageChaser1, self.buttonChaser1Text)

    def to_chaser2(self, button):
        self.configure_button(button, self.imageChaser2, self.buttonChaser2Text)

    def to_rock(self, button):
        self.configure_button(button, self.imageRock, self.buttonRockText)

class Board:
    def __init__(self, windowHeight, windowWidth, boxHeight, boxWidth, boxMargin, rowCount, columnCount):
        self.windowHeight = windowHeight
        self.windowWidth = windowWidth
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
        self.window = tk.Tk()
        self.runner_controller = tk.IntVar()
        self.runner_controller.set(1)
        self.runner_place_controller = tk.IntVar()
        self.runner_place_controller.set(1)
        self.chaser_place_controller = tk.IntVar()
        self.chaser_place_controller.set(1)
        self.rock_place_controller = tk.IntVar()
        self.rock_place_controller.set(1)
        self.rock_count = tk.IntVar()
        self.rock_count.set(16)
        self.rock_counter = 0
        self.turn_count = tk.IntVar()
        self.turn_count.set(100)
        self.window.title(self.windowTitle)
        self.window.resizable(0, 0)
        self.window.geometry(str(self.windowWidth) + 'x' + str(self.windowHeight))
        self.window.wm_iconphoto(False, ImageTk.PhotoImage(Image.open('image/runner.png')))
        self.window.configure(bg=self.colorGray)
        self.waitingJob = WaitingJob.SelectRunnerPlace
        counter = 0
        while counter <= self.columnCount:
            self.window.rowconfigure(counter, weight=1)
            self.window.columnconfigure(counter, weight=1)
            counter += 1
        self.state = []
        for row in range(rowCount):
            self.state.append([])
            for column in range(columnCount):
                self.state[row].append(0)


    def clickedButton(event):
        global waitingJob
        global rock_counter
        row_column = string_to_row_column(event.widget['text'])
        print('Initial Waiting Job:', waitingJob)
        if waitingJob == WaitingJob.SelectRunnerPlace:
            to_runner(elts[row_column[0]][row_column[1]])
            waitingJob = WaitingJob.SelectChaser1Place
        elif waitingJob == WaitingJob.SelectChaser1Place:
            to_chaser1(elts[row_column[0]][row_column[1]])
            waitingJob = WaitingJob.SelectChaser2Place
        elif waitingJob == WaitingJob.SelectChaser2Place:
            to_chaser2(elts[row_column[0]][row_column[1]])
            waitingJob = WaitingJob.SelectRockPlace
        elif waitingJob == WaitingJob.SelectRockPlace:
            to_rock(elts[row_column[0]][row_column[1]])
            rock_counter += 1
            if rock_count.get() == rock_counter:
                waitingJob = WaitingJob.NoWaitingJob
        print('Final Waiting Job:', waitingJob)



