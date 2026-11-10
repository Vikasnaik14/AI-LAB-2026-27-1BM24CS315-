import random

def calculate_cost(board):
    """Calculates the number of attacking pairs of queens."""
    cost = 0
    n = len(board)
    for i in range(n):
        for j in range(i + 1, n):
            # Check for row collision (won't happen in swap approach, but kept for safety)
            if board[i] == board[j]:
                cost += 1
            # Check for diagonal collision
            elif abs(board[i] - board[j]) == abs(i - j):
                cost += 1
    return cost

def get_neighbors_by_swapping(board):
    """Generates all neighbors by swapping row values of two different columns."""
    neighbors = []
    n = len(board)

    # Iterate through all unique pairs of columns
    for i in range(n - 1):
        for j in range(i + 1, n):
            neighbor = list(board)
            # Swap the rows for column i and column j
            neighbor[i], neighbor[j] = neighbor[j], neighbor[i]

            neighbors.append((neighbor, calculate_cost(neighbor)))

    return neighbors

def format_state(board):
    """Formats the board state to match the requested output style."""
    return f"x0 = {board[0]}, x1 = {board[1]}, x2 = {board[2]}, x3 = {board[3]}"

def print_grid(board, title="Grid:"):
    """Prints the chessboard in grid representation."""
    n = len(board)
    print(title)

    for row in range(n):
        for col in range(n):
            if board[col] == row:
                print(" Q ", end="")
            else:
                print(" . ", end="")
        print()

def solve_4_queens_swap():
    # Initialize with a permutation state (0, 1, 2, 3) so each row/col has exactly one queen
    current_board = [0, 1, 2, 3]
    random.shuffle(current_board) # Start randomly
    step = 0

    while True:
        step += 1
        current_cost = calculate_cost(current_board)

        print(f"\n===== Step {step} =====")
        print_grid(current_board, f"Current grid (cost {current_cost}):")

        if current_cost == 0:
            print(f"\nGoal Configuration Reached! {format_state(current_board)} (cost is 0)")
            print_grid(current_board, "Goal grid:")
            break

        print(f"\nNeighbours of {format_state(current_board)} (cost is {current_cost})")

        # Use the swapping neighbor function
        neighbors = get_neighbors_by_swapping(current_board)

        best_neighbor = None
        best_cost = float('inf')

        for neighbor, cost in neighbors:
            if cost < best_cost:
                best_cost = cost
                best_neighbor = neighbor

        for neighbor, cost in neighbors:
            output_line = f" * {format_state(neighbor)} cost is {cost}."
            if neighbor == best_neighbor:
                output_line += " Choose this neighbour."
            print(output_line)

        if best_cost >= current_cost:
            print(f"\nStuck in local minimum at {format_state(current_board)}. Restarting...")
            current_board = [0, 1, 2, 3]
            random.shuffle(current_board)
        else:
            current_board = best_neighbor


if __name__ == "__main__":
    solve_4_queens_swap()
    
