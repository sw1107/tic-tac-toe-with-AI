from copy import deepcopy
from itertools import cycle
from random import randint

BOARD = {}
player = cycle(range(2))


def main():
    while input("Do you want to play a game of Tic Tac Toe? Type 'y' to play': ") == 'y':
        print_template()
        play_game()


def play_game():
    reset_board()
    number_of_moves = 0
    is_game_over = False

    # randomly choose first player
    for _ in range(randint(1, 2)):
        current_player = next(player)

    while not is_game_over:

        if current_player == 0:
            current_board = deepcopy(BOARD)
            next_move = minimax(current_board, current_player)[1]
            print(f"Computer move: {next_move + 1}")
        else:
            next_move = int(input(f"Player move? Type 1-9: "))
            # TODO: improve validation of inputs

        # validate move
        # TODO: improve validation so player/computer can't play in space already played in
        if current_player == 0 and BOARD[next_move] != " ":
            print(f"Computer move invalid: {next_move}")
            return

        # update board with move
        if current_player == 0:
            BOARD[next_move] = 'x'
        else:
            BOARD[next_move - 1] = 'o'

        # toggle to next player
        current_player = next(player)
        number_of_moves += 1

        print_board()

        # check for game over
        if number_of_moves >= 5:
            is_game_over = check_game_over(BOARD)

    # compute value of final board and declare winner
    final_board_value = value_board(BOARD)
    if final_board_value == 1:
        print("Game over: Computer is the winner! \n")
    elif final_board_value == -1:
        print("Game over: Player is the winner! \n")
    else:
        print("Game over: No winner\n")


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
    # TODO: improve the value_board function (find a way to sum indices?)
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


# def test():
#     BOARD = {0: 'x', 1: 'o', 2: 'x', 3: 'x', 4: ' ', 5: 'o', 6: 'o', 7: ' ', 8: ' '}
#     current_player = 0
#     current_board = deepcopy(BOARD)
#     next_move = minimax(current_board, current_player)[1]
#     print(f"Computer move: {next_move + 1}")
#
#
# test()


if __name__ == "__main__":
    main()
