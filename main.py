from copy import deepcopy
from itertools import cycle
from random import randint
from tkinter import *
from tkinter import messagebox
from functools import partial

# ---------------------- CONSTANTS ----------------------
FONT_NAME = "Courier"
BACKGROUND_COLOUR = "#011CFF"
FONT_COLOUR = "white"
BOX_WIDTH = 2
BOX_HEIGHT = 1
BOX_FONT_SIZE = 150
TOP_LABEL_FONT_SIZE = 15

# ---------------------- GAME VARIABLES ----------------------
BOARD = {}
player = cycle(range(2))


# ---------------------- GUI FUNCTIONS ----------------------
def make_move(box):
    if BOARD[box] == " ":
        player_move.set(box)
    else:
        messagebox.showwarning(title="Move invalid", message="That move is not available, please try again")


def play_game():

    reset_board()
    number_of_moves = 0
    is_game_over = False

    # randomly choose first player
    for _ in range(randint(1, 2)):
        current_player = next(player)

    if current_player == 0:
        top_label.config(text="Computer starts")
    else:
        top_label.config(text="Player starts")

    while not is_game_over:

        if current_player == 0:
            current_board = deepcopy(BOARD)
            next_move = minimax(current_board, current_player)[1]
            if BOARD[next_move] != " ":
                messagebox.showwarning(title="Computer error", message="Computer made an invalid move")
                return
        else:
            window.wait_variable(player_move)
            next_move = player_move.get()

        # update board with move
        if current_player == 0:
            BOARD[next_move] = 'x'
            all_buttons[next_move].config(text="X")
        else:
            BOARD[next_move] = 'o'
            all_buttons[next_move].config(text="O")

        if number_of_moves == 1:
            top_label.config(text="")

        # toggle to next player
        current_player = next(player)
        number_of_moves += 1

        # check for game over
        if number_of_moves >= 5:
            is_game_over = check_game_over(BOARD)

    # compute value of final board and declare winner
    final_board_value = value_board(BOARD)
    if final_board_value == 1:
        top_label.config(text="Game over: Computer is the winner!")
    elif final_board_value == -1:
        top_label.config(text="Game over: Player is the winner!")
    else:
        top_label.config(text="Game over: No winner")


# ---------------------- TIC TAC TOE FUNCTIONS ----------------------
def check_game_over(current_board):
    # TODO: improve check_game_over function
    if ((current_board[0] == current_board[1] == current_board[2] and current_board[0] != " ") or
            (current_board[3] == current_board[4] == current_board[5] and current_board[3] != " ") or
            (current_board[6] == current_board[7] == current_board[8] and current_board[6] != " ") or
            (current_board[0] == current_board[3] == current_board[6] and current_board[0] != " ") or
            (current_board[1] == current_board[4] == current_board[7] and current_board[1] != " ") or
            (current_board[2] == current_board[5] == current_board[8] and current_board[2] != " ") or
            (current_board[0] == current_board[4] == current_board[8] and current_board[0] != " ") or
            (current_board[2] == current_board[4] == current_board[6] and current_board[2] != " ") or
            # or all squares are full
            (not (" " in current_board.values()))):
        return True
    else:
        return False


def reset_board():
    for i in range(9):
        BOARD[i] = " "
    for button in all_buttons:
        button.config(text="")


def print_board():
    print(f"\n"
          f" {BOARD[0]} | {BOARD[1]} | {BOARD[2]} \n"
          f"-----------\n"
          f" {BOARD[3]} | {BOARD[4]} | {BOARD[5]} \n"
          f"-----------\n"
          f" {BOARD[6]} | {BOARD[7]} | {BOARD[8]} \n")


def print_template():
    print("\n"
          f" 1 | 2 | 3 \n"
          f"-----------\n"
          f" 4 | 5 | 6 \n"
          f"-----------\n"
          f" 7 | 8 | 9 \n")


def value_board(current_board):
    """
    Returns numerical value for terminal state of current_board
    """
    # TODO: improve the value_board function
    if ((current_board[0] == current_board[1] == current_board[2] and current_board[0] == "x") or
            (current_board[3] == current_board[4] == current_board[5] and current_board[3] == "x") or
            (current_board[6] == current_board[7] == current_board[8] and current_board[6] == "x") or
            (current_board[0] == current_board[3] == current_board[6] and current_board[0] == "x") or
            (current_board[1] == current_board[4] == current_board[7] and current_board[1] == "x") or
            (current_board[2] == current_board[5] == current_board[8] and current_board[2] == "x") or
            (current_board[0] == current_board[4] == current_board[8] and current_board[0] == "x") or
            (current_board[2] == current_board[4] == current_board[6] and current_board[2] == "x")):
        return 1
    elif ((current_board[0] == current_board[1] == current_board[2] and current_board[0] == "o") or
          (current_board[3] == current_board[4] == current_board[5] and current_board[3] == "o") or
          (current_board[6] == current_board[7] == current_board[8] and current_board[6] == "o") or
          (current_board[0] == current_board[3] == current_board[6] and current_board[0] == "o") or
          (current_board[1] == current_board[4] == current_board[7] and current_board[1] == "o") or
          (current_board[2] == current_board[5] == current_board[8] and current_board[2] == "o") or
          (current_board[0] == current_board[4] == current_board[8] and current_board[0] == "o") or
          (current_board[2] == current_board[4] == current_board[6] and current_board[2] == "o")):
        return -1
    else:
        return 0


def available_moves(current_board):
    """
    Returns list of actions available from state of current_board
    """
    return [square for square in current_board if current_board[square] == " "]


def result(current_board, action, current_player):
    """
    Returns board after action taken in state of current_board
    """
    result_board = deepcopy(current_board)
    if current_player == 0:
        result_board[action] = "x"
    else:
        result_board[action] = "o"
    return result_board


def minimax(current_board, current_player):
    """
    Returns value of state of current_board and best move
    """
    if check_game_over(current_board):
        return value_board(current_board), None

    best_move = None
    if current_player == 0:
        value = -100
        for action in available_moves(current_board):
            new_value = minimax(result(current_board, action, 0), 1)[0]
            if new_value > value:
                value = new_value
                best_move = action
        # return value, best_move
    else:
        value = 100
        for action in available_moves(current_board):
            new_value = minimax(result(current_board, action, 1), 0)[0]
            if new_value < value:
                value = new_value
                best_move = action
        # return value, best_move
    return value, best_move


# ---------------------- GUI ----------------------
window = Tk()
window.title("Tic Tac Toe")
window.config(padx=50, pady=50)

top_label = Label(text="Press start to play!", fg=BACKGROUND_COLOUR, font=(FONT_NAME, TOP_LABEL_FONT_SIZE))
top_label.grid(column=0, row=0, columnspan=2)

start_button = Button(text="Start", width=10, height=2, highlightbackground=BACKGROUND_COLOUR, fg=FONT_COLOUR,
                      font=FONT_NAME, command=play_game)
start_button.grid(column=2, row=0, padx=10, pady=10)

player_move = IntVar()

all_buttons = []
b0 = Button(text="", width=BOX_WIDTH, height=BOX_HEIGHT, highlightbackground=BACKGROUND_COLOUR, fg=FONT_COLOUR,
            font=(FONT_NAME, BOX_FONT_SIZE), command=partial(make_move, 0))
b0.grid(column=0, row=1)
all_buttons.append(b0)
b1 = Button(text="", width=BOX_WIDTH, height=BOX_HEIGHT, highlightbackground=BACKGROUND_COLOUR, fg=FONT_COLOUR,
            font=(FONT_NAME, BOX_FONT_SIZE), command=partial(make_move, 1))
b1.grid(column=1, row=1)
all_buttons.append(b1)
b2 = Button(text="", width=BOX_WIDTH, height=BOX_HEIGHT, highlightbackground=BACKGROUND_COLOUR, fg=FONT_COLOUR,
            font=(FONT_NAME, BOX_FONT_SIZE), command=partial(make_move, 2))
b2.grid(column=2, row=1)
all_buttons.append(b2)
b3 = Button(text="", width=BOX_WIDTH, height=BOX_HEIGHT, highlightbackground=BACKGROUND_COLOUR, fg=FONT_COLOUR,
            font=(FONT_NAME, BOX_FONT_SIZE), command=partial(make_move, 3))
b3.grid(column=0, row=2)
all_buttons.append(b3)
b4 = Button(text="", width=BOX_WIDTH, height=BOX_HEIGHT, highlightbackground=BACKGROUND_COLOUR, fg=FONT_COLOUR,
            font=(FONT_NAME, BOX_FONT_SIZE), command=partial(make_move, 4))
b4.grid(column=1, row=2)
all_buttons.append(b4)
b5 = Button(text="", width=BOX_WIDTH, height=BOX_HEIGHT, highlightbackground=BACKGROUND_COLOUR, fg=FONT_COLOUR,
            font=(FONT_NAME, BOX_FONT_SIZE), command=partial(make_move, 5))
b5.grid(column=2, row=2)
all_buttons.append(b5)
b6 = Button(text="", width=BOX_WIDTH, height=BOX_HEIGHT, highlightbackground=BACKGROUND_COLOUR, fg=FONT_COLOUR,
            font=(FONT_NAME, BOX_FONT_SIZE), command=partial(make_move, 6))
b6.grid(column=0, row=3)
all_buttons.append(b6)
b7 = Button(text="", width=BOX_WIDTH, height=BOX_HEIGHT, highlightbackground=BACKGROUND_COLOUR, fg=FONT_COLOUR,
            font=(FONT_NAME, BOX_FONT_SIZE), command=partial(make_move, 7))
b7.grid(column=1, row=3)
all_buttons.append(b7)
b8 = Button(text="", width=BOX_WIDTH, height=BOX_HEIGHT, highlightbackground=BACKGROUND_COLOUR, fg=FONT_COLOUR,
            font=(FONT_NAME, BOX_FONT_SIZE), command=partial(make_move, 8))
b8.grid(column=2, row=3)
all_buttons.append(b8)

window.mainloop()
