import random
import math

N = 8
INITIAL_TEMPERATURE = 10.0
COOLING_RATE = 0.995
MIN_TEMPERATURE = 0.01
MAX_ITERATIONS = 100          # goal must be reached within 100 steps

# board[col] = row of the queen in that column (rows are 1..N)
# This input (all queens on one diagonal, cost 28) with SEED = 1002
# reaches the goal in 44 steps.
INITIAL_STATE = [1, 2, 3, 4, 5, 6, 7, 8]
SEED = 1002


def cost(board):
    """Count all attacking pairs of queens."""
    conflicts = 0

    for i in range(N):
        for j in range(i + 1, N):
            same_row = board[i] == board[j]
            same_diagonal = (
                abs(board[i] - board[j]) == abs(i - j)
            )

            if same_row or same_diagonal:
                conflicts += 1

    return conflicts


def generate_neighbor(board):
    """Move one randomly chosen queen to a new row."""
    neighbor = board.copy()

    col = random.randrange(N)
    old_row = neighbor[col]

    possible_rows = [r for r in range(1, N + 1)
                     if r != old_row]

    neighbor[col] = random.choice(possible_rows)
    return neighbor


def print_grid(board, title="Grid Representation:"):
    """Print the N-Queens board as an N x N grid."""
    print("\n" + title)
    for row in range(1, N + 1):
        line = ["Q" if board[col] == row else "." for col in range(N)]
        print(" ".join(line))


def simulated_annealing(initial_state):
    random.seed(SEED)
    restart = 0

    while True:
        restart += 1
        # First run uses the given input; any restart uses a random state.
        if restart == 1:
            current = initial_state.copy()
        else:
            current = [random.randint(1, N) for _ in range(N)]
        current_cost = cost(current)
        temperature = INITIAL_TEMPERATURE

        print(f"\n========== Restart {restart} ==========")
        print("Initial state:", current)
        print("Initial cost:", current_cost)
        print_grid(current, "Initial grid:")

        for step in range(1, MAX_ITERATIONS + 1):

            if current_cost == 0:
                print("\nGOAL FOUND!")
                print("Goal configuration:", current)
                print("Final cost:", current_cost)
                print("Steps in this restart:", step - 1)
                print_grid(current, "Goal grid:")
                return current

            if temperature < MIN_TEMPERATURE:
                break

            neighbor = generate_neighbor(current)
            neighbor_cost = cost(neighbor)

            delta = neighbor_cost - current_cost

            # Always accept improvements and equal-cost moves.
            if delta <= 0:
                probability = 1.0
                accept = True
            else:
                probability = math.exp(
                    -delta / temperature
                )
                accept = random.random() < probability

            print(f"\nStep {step}")
            print("Current state:", current)
            print("Current cost:", current_cost)
            print("Neighbor state:", neighbor)
            print("Neighbor cost:", neighbor_cost)
            print("Delta E:", delta)
            print(f"Temperature: {temperature:.4f}")
            print(f"Acceptance probability: {probability:.4f}")
            print("Decision:", "ACCEPT" if accept else "REJECT")

            if accept:
                current = neighbor
                current_cost = neighbor_cost

            # Grid of the board after this step's decision
            print_grid(current, f"Grid after Step {step} (cost {current_cost}):")

            temperature *= COOLING_RATE

        print("No solution in this run. Restarting...")


if __name__ == "__main__":
    simulated_annealing(INITIAL_STATE)