"""
8-Puzzle solver using A* search with the Misplaced Tiles heuristic.

f(n) = g(n) + h(n)
  g(n) = number of moves made so far
  h(n) = number of tiles (excluding the blank) not in their goal position
"""

import heapq
from itertools import count

# Moves expressed as the movement of the blank tile.
MOVES = {
    "Up": (-1, 0),
    "Down": (1, 0),
    "Left": (0, -1),
    "Right": (0, 1),
}


# ---------------------------------------------------------------- state utils
def parse_state(text):
    """'013 824 765' -> (0, 1, 3, 8, 2, 4, 7, 6, 5). 0 is the blank."""
    digits = [int(c) for c in text if c.isdigit()]
    if sorted(digits) != list(range(9)):
        raise ValueError("State must contain each digit 0-8 exactly once.")
    return tuple(digits)


def inversions(state):
    tiles = [t for t in state if t != 0]
    return sum(
        1
        for i in range(len(tiles))
        for j in range(i + 1, len(tiles))
        if tiles[i] > tiles[j]
    )


def is_solvable(start, goal):
    """On a 3x3 board, start can reach goal iff their inversion parities match."""
    return inversions(start) % 2 == inversions(goal) % 2


def print_state(state):
    for r in range(3):
        print(" ".join(str(x) if x else "_" for x in state[3 * r: 3 * r + 3]))
    print()


# ------------------------------------------------------------------ heuristic
def misplaced_tiles(state, goal):
    """Count tiles that are not in their goal position (blank ignored)."""
    return sum(1 for s, g in zip(state, goal) if s != 0 and s != g)


# ----------------------------------------------------------------- successors
def get_neighbors(state):
    """Yield (move_name, new_state) for every legal move of the blank."""
    blank = state.index(0)
    row, col = divmod(blank, 3)
    for name, (dr, dc) in MOVES.items():
        nr, nc = row + dr, col + dc
        if 0 <= nr < 3 and 0 <= nc < 3:
            new = list(state)
            target = nr * 3 + nc
            new[blank], new[target] = new[target], new[blank]
            yield name, tuple(new)


# ------------------------------------------------------------------- A* core
def reconstruct_path(came_from, state):
    """Walk parent links back to the start; return states and moves."""
    states, moves = [state], []
    while came_from[state] is not None:
        state, move = came_from[state]
        states.append(state)
        moves.append(move)
    return states[::-1], moves[::-1]


def a_star(start, goal, heuristic=misplaced_tiles):
    """
    Returns (states_on_path, moves, nodes_expanded) or (None, None, n)
    if no solution exists.
    """
    if not is_solvable(start, goal):
        return None, None, 0

    tie = count()  # tie-breaker so heapq never compares states
    open_heap = [(heuristic(start, goal), next(tie), 0, start)]
    came_from = {start: None}   # state -> (parent_state, move)
    best_g = {start: 0}
    closed = set()
    expanded = 0

    while open_heap:
        _, _, g, current = heapq.heappop(open_heap)

        if current in closed:
            continue
        if current == goal:
            states, moves = reconstruct_path(came_from, current)
            return states, moves, expanded

        closed.add(current)
        expanded += 1

        for move, nxt in get_neighbors(current):
            new_g = g + 1
            if nxt in closed or new_g >= best_g.get(nxt, float("inf")):
                continue
            best_g[nxt] = new_g
            came_from[nxt] = (current, move)
            f = new_g + heuristic(nxt, goal)
            heapq.heappush(open_heap, (f, next(tie), new_g, nxt))

    return None, None, expanded


# ----------------------------------------------------------------------- main
def solve(start, goal):
    print("Start state:")
    print_state(start)
    print("Goal state:")
    print_state(goal)

    states, moves, expanded = a_star(start, goal)
    if states is None:
        print("This puzzle is not solvable.")
        return

    for step, (move, state) in enumerate(zip(moves, states[1:]), 1):
        h = misplaced_tiles(state, goal)
        print(f"Step {step}: {move}  (g={step}, h={h}, f={step + h})")
        print_state(state)

    print(f"Solved in {len(moves)} moves ({expanded} nodes expanded).")
    print("Moves:", " -> ".join(moves))


if __name__ == "__main__":
    start_state = parse_state("283 164 705")
    goal_state = parse_state("123 804 765")
    solve(start_state, goal_state)