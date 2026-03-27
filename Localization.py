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

DIRS = {
    "N": (-1, 0),
    "S": (1, 0),
    "W": (0, -1),
    "E": (0, 1),
}

LEFT = {
    "N": "W",
    "W": "S",
    "S": "E",
    "E": "N",
}

RIGHT = {
    "N": "E",
    "E": "S",
    "S": "W",
    "W": "N",
}


def move(r, c, direction):
    dr, dc = DIRS[direction]
    nr, nc = r + dr, c + dc

    # If blocked by a wall or obstacle, stay in place
    if is_obstacle(nr, nc):
        return (r, c)

    return (nr, nc)


def initialize_belief():
    belief = {}
    p = 1.0 / len(FREE_CELLS)

    for cell in FREE_CELLS:
        belief[cell] = p

    return belief

def sense_probability(cell, evidence):
    """
    Returns P(evidence | cell)
    Evidence order: [W, N, E, S]
    """
    r, c = cell
    directions = ["W", "N", "E", "S"]

    prob = 1.0

    for i in range(4):
        d = directions[i]
        obs = evidence[i]

        dr, dc = DIRS[d]
        has_wall = is_obstacle(r + dr, c + dc)

        if has_wall:
            prob *= 0.9 if obs == 1 else 0.1
        else:
            prob *= 0.05 if obs == 1 else 0.95

    return prob

def normalize(belief):
    total = sum(belief.values())

    for cell in belief:
        belief[cell] /= total

    return belief


def filtering(belief, evidence):
    updated = {}

    for cell in FREE_CELLS:
        likelihood = sense_probability(cell, evidence)
        updated[cell] = belief[cell] * likelihood

    return normalize(updated)

def prediction(belief, action):
    new_belief = {cell: 0.0 for cell in FREE_CELLS}

    for cell in FREE_CELLS:
        r, c = cell
        current_prob = belief[cell]

        forward = move(r, c, action)
        left = move(r, c, LEFT[action])
        right = move(r, c, RIGHT[action])

        new_belief[forward] += current_prob * 0.75
        new_belief[left] += current_prob * 0.15
        new_belief[right] += current_prob * 0.10

    return new_belief

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

    evidence = [0, 0, 0, 0]
    belief = filtering(belief, evidence)
    print_grid(f"Filtering after Evidence {evidence}", belief)

    action = "N"
    belief = prediction(belief, action)
    print_grid(f"Prediction after Action {action}", belief)

if __name__ == "__main__":
    main()