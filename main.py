# import libraries
import tkinter as tk
from PIL import Image, ImageTk
# define window props
WINDOW_TITLE = 'Run Forrest Run!!'
WINDOW_HEIGHT = 870
WINDOW_WIDTH = 870
# define colors
BLACK = '#000000'
WHITE = '#FAFAFA'
GREY = '#B9B9B9'
RUNNER = '#0A9F23'
CHASER = '#9F0A0A'
# define board props
BOX_WIDTH = 60
BOX_HEIGHT = 60
BOX_MARGIN = 2
BOARD_GRID_ROW_COUNT = 8
BOARD_GRID_COLUMN_COUNT = 13
BOARD_TOP_MARGIN = WINDOW_HEIGHT - BOARD_GRID_ROW_COUNT * BOX_HEIGHT - (BOARD_GRID_ROW_COUNT + 1) * BOX_MARGIN
# define turn count - default value is 100
turn_count = 100
# initialize window
window = tk.Tk()
# set window props
window.title(WINDOW_TITLE)
window.resizable(0,0)
window.geometry(str(WINDOW_HEIGHT) + 'x' + str(WINDOW_WIDTH))
window.wm_iconphoto(False, ImageTk.PhotoImage(Image.open('image/rfr_icon.png')))
# creating whole grid for once
counter = 0
while counter <= BOARD_GRID_COLUMN_COUNT:
    window.rowconfigure(counter, weight=1)
    window.columnconfigure(counter, weight=1)
    counter+=1
# adding UI elements
lbl_0_0 = tk.Label(window, bg=BLACK)
lbl_0_0.grid(row=13, column=0)
lbl_0_0.pack(fill=tk.BOTH, expand=1)
# window live
window.mainloop()