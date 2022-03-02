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
            current_board = {key: value for (key, value) in BOARD.items()}
            next_move = minimax(current_board, current_player)[1]
            print(f"Computer move: {next_move}")
            # TODO: computer shouldn't be able to move in space already played in
        else:
            # TODO: player shouldn't be able to move in space already played in
            next_move = int(input(f"Player move? Type 1-9: "))

        # validate move
        if BOARD[next_move - 1] != " ":
            print(f"Computer move invalid: {next_move}")
            return

        # update board with move
        if current_player == 0:
            BOARD[next_move - 1] = 'x'
        else:
            BOARD[next_move - 1] = 'o'

        # toggle to next player
        current_player = next(player)
        number_of_moves += 1

        print_board()

        # check for game over
        if number_of_moves >= 5:
            is_game_over = check_game_over()
        if number_of_moves == 9 and is_game_over is False:
            is_game_over = True
            print_board()
            print(f"Game over: No winner\n")
            return

    # print final board and announce winner
    print_board()
    winner = next(player)
    if winner == 0:
        print(f"Game over: Computer is the winner! \n")
    else:
        print(f"Game over: Player is the winner! \n")


def check_game_over(current_board):
    if ((current_board[0] == current_board[1] == current_board[2] and current_board[0] != " ") or
            (current_board[3] == current_board[4] == current_board[5] and current_board[3] != " ") or
            (current_board[6] == current_board[7] == current_board[8] and current_board[6] != " ") or
            (current_board[0] == current_board[3] == current_board[6] and current_board[0] != " ") or
            (current_board[1] == current_board[4] == current_board[7] and current_board[1] != " ") or
            (current_board[2] == current_board[5] == current_board[8] and current_board[2] != " ") or
            (current_board[0] == current_board[4] == current_board[8] and current_board[0] != " ") or
            (current_board[2] == current_board[4] == current_board[6] and current_board[2] != " ")):
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
    if current_player == 0:
        current_board[action] = "x"
    else:
        current_board[action] = "o"
    return current_board


def minimax(current_board, current_player):
    """
    Returns value of state of current_board and best move
    """
    # TODO: current_board doesn't reset through iterations of the recursion
    best_move = None
    if check_game_over(current_board):
        return value_board(current_board), best_move
    elif current_player == 0:
        value = -100
        for action in available_moves(current_board):
            new_value = minimax(result(current_board, action, 0), 1)[0]
            if new_value > value:
                value = new_value
                best_move = action
        return value, best_move
    else:
        value = 100
        for action in available_moves(current_board):
            new_value = minimax(result(current_board, action, 1), 0)[0]
            if new_value < value:
                value = new_value
                best_move = action
        return value, best_move


# def max_value(current_board):
#     if check_game_over():
#         return value_board(current_board)
#     else:
#         value = -100
#         for action in available_moves(current_board):
#             value = max(value, min_value(result(current_board, action)))
#         return value
#
#
# def min_value(current_board):
#     if check_game_over():
#         return value_board(current_board)
#     else:
#         value = 100
#         for action in available_moves(current_board):
#             value = min(max_value(result(current_board, action)))
#         return value


# def test():
#     reset_board()
#
#     current_player = next(player)
#     current_player = next(player)
#
#     BOARD[1] = "x"
#     BOARD[2] = "o"
#     current_board = BOARD
#     next_move = minimax(current_board, current_player)
#     print(next_move)
#
#
# test()

if __name__ == "__main__":
    main()
