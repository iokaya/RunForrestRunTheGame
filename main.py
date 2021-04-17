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
GRAY = '#B9B9B9'
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


# adding UI elements
lbl_0_0 = __make_label__(window, 2, 808, 60, 60, bg=BLACK)
lbl_1_0 = __make_label__(window, 2, 746, 60, 60, bg=WHITE, fg=BLACK, text='1', font=("Calibri", 22))
lbl_2_0 = __make_label__(window, 2, 684, 60, 60, bg=WHITE, fg=BLACK, text='2', font=("Calibri", 22))
lbl_3_0 = __make_label__(window, 2, 622, 60, 60, bg=WHITE, fg=BLACK, text='3', font=("Calibri", 22))
lbl_4_0 = __make_label__(window, 2, 560, 60, 60, bg=WHITE, fg=BLACK, text='4', font=("Calibri", 22))
lbl_5_0 = __make_label__(window, 2, 498, 60, 60, bg=WHITE, fg=BLACK, text='5', font=("Calibri", 22))
lbl_6_0 = __make_label__(window, 2, 436, 60, 60, bg=WHITE, fg=BLACK, text='6', font=("Calibri", 22))
lbl_7_0 = __make_label__(window, 2, 374, 60, 60, bg=WHITE, fg=BLACK, text='7', font=("Calibri", 22))
lbl_8_0 = __make_label__(window, 2, 312, 60, 60, bg=WHITE, fg=BLACK, text='8', font=("Calibri", 22))

# window live
window.mainloop()