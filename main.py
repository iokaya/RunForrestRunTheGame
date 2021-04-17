# import libraries
import enum
import tkinter as tk
from PIL import Image, ImageTk
# define constant variables
ASCII_CAPITAL_LETTERS_START = 64
# define window props
WINDOW_TITLE = 'Run Forrest Run!!'
WINDOW_HEIGHT = 730
WINDOW_WIDTH = 730
# define colors
BLACK = '#000000'
WHITE = '#FAFAFA'
GRAY = '#B9B9B9'
RUNNER = '#0A9F23'
CHASER = '#9F0A0A'
# define button types
BUTTON_GRASS = 'grass'
BUTTON_ROCK = 'rock'
BUTTON_RUNNER = 'runner'
BUTTON_CHASER1 = 'chaser1'
BUTTON_CHASER2 = 'chaser2'
# define board props
BOX_WIDTH = 50
BOX_HEIGHT = 50
BOX_MARGIN = 2
BOX_FONT = ("Calibri", 22)
BOARD_GRID_ROW_COUNT = 8
BOARD_GRID_COLUMN_COUNT = 13
BOARD_TOP_MARGIN = WINDOW_HEIGHT - (BOARD_GRID_ROW_COUNT + 1) * BOX_HEIGHT - (BOARD_GRID_ROW_COUNT + 2) * BOX_MARGIN
# define turn count - default value is 100
turn_count = 100
#define rock count - default is 16
rock_count = 16
rock_counter = 0
# initialize window
window = tk.Tk()
# set window props
window.title(WINDOW_TITLE)
window.resizable(0,0)
window.geometry(str(WINDOW_HEIGHT) + 'x' + str(WINDOW_WIDTH))
window.wm_iconphoto(False, ImageTk.PhotoImage(Image.open('image/runner.png')))
window.configure(bg=GRAY)
# creating whole grid for once
counter = 0
while counter <= BOARD_GRID_COLUMN_COUNT:
    window.rowconfigure(counter, weight=1)
    window.columnconfigure(counter, weight=1)
    counter += 1
# helper classes
class WaitingJob(enum.Enum):
    NoWaitingJob = 0
    SelectRunnerPlace = 1
    SelectChaser1Place = 2
    SelectChaser2Place = 3
    SelectRockPlace = 4
waitingJob = WaitingJob.SelectRunnerPlace
# layout element makers
# label maker
def __make_label__(master, x, y, h, w, *args, **kwargs):
    frame = tk.Frame(master, height=h, width=w)
    frame.pack_propagate(0)
    frame.place(x=x, y=y)
    label = tk.Label(frame, *args, **kwargs)
    label.pack(fill=tk.BOTH, expand=1)
    return label
# button maker
def __make_button__(master, x, y, h, w, *args, **kwargs):
    frame = tk.Frame(master, height=h, width=w)
    frame.pack_propagate(0)
    frame.place(x=x, y=y)
    button = tk.Button(frame, *args, **kwargs)
    button.pack(fill=tk.BOTH, expand=1)
    return button
# on click methods
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
        if rock_count == rock_counter:
            waitingJob = WaitingJob.NoWaitingJob
    print('Final Waiting Job:', waitingJob)
# helper methods
def row_column_type_to_string(row, column, button_type):
    return str(row) + '_' + str(column) + '_' + button_type
def string_to_row_column(rc_str):
    return int(rc_str.split('_')[0]), int(rc_str.split('_')[1])
def num_to_char(num):
    return chr(ASCII_CAPITAL_LETTERS_START + column)
def char_to_num(char):
    return int(char.upper()) - ASCII_CAPITAL_LETTERS_START
def configure_button(button, image, button_type):
    button.configure(image=image)
    row_column = string_to_row_column(button['text'])
    new_text = row_column_type_to_string(row_column[0], row_column[1], button_type)
def to_runner(button):
    configure_button(button, runner_image, BUTTON_RUNNER)
def to_chaser1(button):
    configure_button(button, chaser1_image, BUTTON_CHASER1)
def to_chaser2(button):
    configure_button(button, chaser2_image, BUTTON_CHASER2)
def to_rock(button):
    configure_button(button, rock_image, BUTTON_ROCK)
# adding UI elements
grass_image = tk.PhotoImage(file='image/grass.png')
rock_image = tk.PhotoImage(file='image/rock.png')
runner_image = tk.PhotoImage(file='image/runner.png')
chaser1_image = tk.PhotoImage(file='image/chaser1.png')
chaser2_image = tk.PhotoImage(file='image/chaser2.png')
elts = []
for row in range(BOARD_GRID_ROW_COUNT+1):
    elts.append([])
    for column in range(BOARD_GRID_COLUMN_COUNT + 1):
        elt = 0
        x = BOX_MARGIN + column * (BOX_WIDTH + BOX_MARGIN)
        y = BOARD_TOP_MARGIN + BOX_MARGIN + row * (BOX_WIDTH + BOX_MARGIN)
        if row==0 and column==0:
            elt = __make_label__(window, x, y, BOX_HEIGHT, BOX_WIDTH, bg=BLACK)
        elif row==0:
            elt = __make_label__(window, x, y, BOX_HEIGHT, BOX_WIDTH, bg=WHITE,
                                 font=BOX_FONT, text=chr(ASCII_CAPITAL_LETTERS_START + column))
        elif column==0:
            elt = __make_label__(window, x, y, BOX_HEIGHT, BOX_WIDTH, bg=WHITE, font=BOX_FONT, text=str(row))
        else:
            button_type = 'grass'
            elt = __make_button__(window, x, y, BOX_HEIGHT, BOX_WIDTH,
                                  image=grass_image, text=row_column_type_to_string(row, column, button_type))
            elt.bind('<1>', clickedButton)
        elts[row].append(elt)

# window live
window.mainloop()
