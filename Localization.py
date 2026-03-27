"""
CIS 479 | Introduction to Artificial Intelligence | Winter 2026
HMM Robot Localization

This program tracks where a robot might be in a maze using:
1. Sensor updates (filtering)
2. Movement updates (prediction)

By: Ghassan El Zahabi
"""

ROWS = 6
COLS = 7

# 0 = free space, 1 = obstacle
GRID = [
    [0, 0, 1, 1, 1, 1, 0],
    [0, 0, 0, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 1, 1],
    [1, 1, 0, 0, 0, 1, 1],
    [1, 1, 1, 0, 0, 0, 1],
    [0, 1, 1, 1, 0, 0, 0],
]


def is_valid(r, c):
    return 0 <= r < ROWS and 0 <= c < COLS


def is_obstacle(r, c):
    if not is_valid(r, c):
        return True
    return GRID[r][c] == 1


def get_free_cells():
    cells = []
    for r in range(ROWS):
        for c in range(COLS):
            if GRID[r][c] == 0:
                cells.append((r, c))
    return cells


FREE_CELLS = get_free_cells()


def initialize_belief():
    belief = {}
    p = 1.0 / len(FREE_CELLS)

    for cell in FREE_CELLS:
        belief[cell] = p

    return belief


def print_grid(title, belief):
    print(title)

    for r in range(ROWS):
        row = []
        for c in range(COLS):
            if GRID[r][c] == 1:
                row.append("####")
            else:
                row.append(f"{belief[(r, c)] * 100:5.2f}")
        print(" ".join(row))

    print()


def main():
    belief = initialize_belief()
    print_grid("Initial Location Probabilities", belief)


if __name__ == "__main__":
    main()