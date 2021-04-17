# import libraries
import numpy as np
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
# define board props
BOX_WIDTH = 50
BOX_HEIGHT = 50
BOX_MARGIN = 2
BOARD_GRID_ROW_COUNT = 8
BOARD_GRID_COLUMN_COUNT = 13
BOARD_TOP_MARGIN = WINDOW_HEIGHT - (BOARD_GRID_ROW_COUNT + 1) * BOX_HEIGHT - (BOARD_GRID_ROW_COUNT + 2) * BOX_MARGIN
# define turn count - default value is 100
turn_count = 100
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
    print(event.widget['text'])
# helper methods
def row_column_to_string(row, column):
    return str(row) + '_' + str(column)
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
                                 font=("Calibri", 22), text=chr(ASCII_CAPITAL_LETTERS_START + column))
        elif column==0:
            elt = __make_label__(window, x, y, BOX_HEIGHT, BOX_WIDTH, bg=WHITE, font=("Calibri", 22), text=str(row))
        else:
            elt = __make_button__(window, x, y, BOX_HEIGHT, BOX_WIDTH,
                                  image=grass_image, text=row_column_to_string(row, column))
            elt.bind('<1>', clickedButton)
        elts[row].append(elt)

runner = elts[1][1]
chaser1 = elts[8][13]
chaser2 = elts[8][12]
runner.configure(image=runner_image)
chaser1.configure(image=chaser1_image)
chaser2.configure(image=chaser2_image)

#print(np.where(elts.text == elts[1][1].text))

print(elts)

# window live
window.mainloop()
