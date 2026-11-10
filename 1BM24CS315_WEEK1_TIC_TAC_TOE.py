"""
Tic Tac Toe - Human vs Computer
--------------------------------
Simple console game. The computer does NOT use minimax or any
standard search algorithm - just plain priority rules:

    1. Win if possible
    2. Block the human's winning move
    3. Take the center
    4. Take a corner
    5. Take any remaining side

Board positions are numbered 1-9 like a phone keypad, top-left to
bottom-right:

     1 | 2 | 3
    -----------
     4 | 5 | 6
    -----------
     7 | 8 | 9
"""

import random

WIN_LINES = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
    (0, 3, 6), (1, 4, 7), (2, 5, 8),  # columns
    (0, 4, 8), (2, 4, 6),             # diagonals
]

HUMAN = "X"
COMPUTER = "O"


def print_board(board):
    def cell(i):
        return board[i] if board[i] else str(i + 1)

    print()
    print(f" {cell(0)} | {cell(1)} | {cell(2)} ")
    print("---+---+---")
    print(f" {cell(3)} | {cell(4)} | {cell(5)} ")
    print("---+---+---")
    print(f" {cell(6)} | {cell(7)} | {cell(8)} ")
    print()


def check_winner(board):
    for a, b, c in WIN_LINES:
        if board[a] and board[a] == board[b] == board[c]:
            return board[a]
    if all(board):
        return "draw"
    return None


def find_winning_move(board, mark):
    """Return an index that completes 3-in-a-row for `mark`, or -1."""
    for line in WIN_LINES:
        values = [board[i] for i in line]
        if values.count(mark) == 2 and values.count(None) == 1:
            empty_index = line[values.index(None)]
            return empty_index
    return -1


def computer_move(board):
    # 1. Win if possible
    move = find_winning_move(board, COMPUTER)
    # 2. Otherwise block the human
    if move == -1:
        move = find_winning_move(board, HUMAN)
    # 3. Otherwise take the center
    if move == -1 and board[4] is None:
        move = 4
    # 4. Otherwise take a random free corner
    if move == -1:
        corners = [i for i in (0, 2, 6, 8) if board[i] is None]
        if corners:
            move = random.choice(corners)
    # 5. Otherwise take a random free side
    if move == -1:
        sides = [i for i in (1, 3, 5, 7) if board[i] is None]
        if sides:
            move = random.choice(sides)

    board[move] = COMPUTER


def human_move(board):
    while True:
        raw = input("Your move (1-9): ").strip()
        if not raw.isdigit():
            print("Please enter a number from 1 to 9.")
            continue
        pos = int(raw) - 1
        if pos < 0 or pos > 8:
            print("Please enter a number from 1 to 9.")
            continue
        if board[pos] is not None:
            print("That square is already taken.")
            continue
        board[pos] = HUMAN
        return


def play_game():
    board = [None] * 9
    print("Tic Tac Toe - you are X, the computer is O.")
    print_board(board)

    while True:
        human_move(board)
        print_board(board)
        result = check_winner(board)
        if result:
            announce(result)
            return

        print("Computer is thinking...")
        computer_move(board)
        print_board(board)
        result = check_winner(board)
        if result:
            announce(result)
            return


def announce(result):
    if result == "draw":
        print("It's a draw!")
    elif result == HUMAN:
        print("You win! ")
    else:
        print("Computer wins!")


def main():
    while True:
        play_game()
        again = input("Play again? (y/n): ").strip().lower()
        if again != "y":
            print("Thanks for playing!")
            break


if __name__ == "__main__":
    main()