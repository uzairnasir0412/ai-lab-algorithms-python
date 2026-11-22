# =============================================================
#  AI Lab Tasks — Python Implementation
#  Tasks: Lab13-T4, Lab3-T2, Lab7-T1, Lab11-T1
# =============================================================

import heapq
from collections import deque

# =============================================================
# ── LAB 13  TASK 4 ── Encloses (Prolog-style in Python) ──────
# =============================================================
# The diagram shows nested boxes:
#   b1 directly contains: b2, b5
#   b2 directly contains: b3, b4
#   b5 directly contains: b6
#   b6 directly contains: b7
#
# FACT: directly_inside(X, Y)  — X is immediately inside Y
# RULE 1 (base):      encloses(X, Y) :- directly_inside(Y, X)
# RULE 2 (recursive): encloses(X, Y) :- directly_inside(Z, X), encloses(Z, Y)
# =============================================================

print("=" * 60)
print("LAB 13 — TASK 4 : Encloses (Recursive Logic in Python)")
print("=" * 60)

# ── Facts: directly_inside(inner, outer) ──────────────────────
directly_inside_facts = [
    ("b2", "b1"),
    ("b5", "b1"),
    ("b3", "b2"),
    ("b4", "b2"),
    ("b6", "b5"),
    ("b7", "b6"),
]

def directly_inside(x, y):
    """True if x is directly inside y (base fact)."""
    return (x, y) in directly_inside_facts

def encloses(x, y, visited=None):
    """
    True if box x encloses box y.
    RULE 1 (base case):      encloses(X,Y) :- directly_inside(Y,X)
    RULE 2 (recursive case): encloses(X,Y) :- directly_inside(Z,X), encloses(Z,Y)
    """
    if visited is None:
        visited = set()
    if (x, y) in visited:
        return False
    visited.add((x, y))

    # Rule 1 — base: Y is directly inside X
    if directly_inside(y, x):
        return True

    # Rule 2 — recursive: some Z is directly inside X, and X encloses Y via Z
    for (inner, outer) in directly_inside_facts:
        if outer == x:          # inner is directly inside x
            if encloses(inner, y, visited):
                return True

    return False

# ── Test queries ───────────────────────────────────────────────
queries = [
    ("b1", "b6"),   # expected True  — b1 > b5 > b6
    ("b1", "b7"),   # expected True  — b1 > b5 > b6 > b7
    ("b2", "b4"),   # expected True  — b2 > b4
    ("b5", "b3"),   # expected False
    ("b1", "b2"),   # expected True
    ("b6", "b1"),   # expected False
]

print("\nFacts (directly_inside):")
for fact in directly_inside_facts:
    print(f"  directly_inside({fact[0]}, {fact[1]})")

print("\nQuery Results:")
for (x, y) in queries:
    result = encloses(x, y)
    print(f"  encloses({x}, {y}) => {result}")

print("\nAll pairs where encloses(X,Y) is True:")
boxes = ["b1","b2","b3","b4","b5","b6","b7"]
for x in boxes:
    for y in boxes:
        if x != y and encloses(x, y):
            print(f"  encloses({x}, {y})")


# =============================================================
# ── LAB 3  TASK 2 ── BFS Maze Solver ─────────────────────────
# =============================================================
# Maze: 0 = free, 1 = wall
# Start = (3, 2) [row, col], Goal = (0, 4) (top row, GOAL tile)
# =============================================================

print("\n" + "=" * 60)
print("LAB 3  — TASK 2 : BFS Maze Solver")
print("=" * 60)

# Maze grid (0=open, 1=wall) — matches the lab image layout
# 8 rows × 8 cols
MAZE_BFS = [
    [1,1,1,1,1,0,1,1],
    [1,0,0,0,0,0,0,1],
    [1,0,1,1,1,1,0,1],
    [1,0,1,0,1,0,0,1],
    [1,0,1,0,1,1,0,1],
    [1,0,1,0,1,0,0,1],
    [1,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1],
]

START_BFS = (3, 3)   # 'S'
GOAL_BFS  = (0, 5)   # 'G'

ROWS_BFS  = len(MAZE_BFS)
COLS_BFS  = len(MAZE_BFS[0])
MOVES     = [(-1,0,'UP'), (1,0,'DOWN'), (0,-1,'LEFT'), (0,1,'RIGHT')]

def bfs_solve(maze, start, goal, rows, cols):
    """
    BFS on the maze.
    Returns (path, visited_order) where path is list of (row,col) nodes.
    """
    queue   = deque()
    visited = set()
    parent  = {}          # node -> parent node (to reconstruct path)

    queue.append(start)
    visited.add(start)
    parent[start] = None
    visited_order = [start]

    while queue:
        current = queue.popleft()
        if current == goal:
            break
        r, c = current
        for dr, dc, _ in MOVES:
            nr, nc = r + dr, c + dc
            neighbor = (nr, nc)
            if 0 <= nr < rows and 0 <= nc < cols \
               and maze[nr][nc] == 0 \
               and neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                queue.append(neighbor)
                visited_order.append(neighbor)

    # Reconstruct path
    if goal not in parent:
        return None, visited_order

    path = []
    node = goal
    while node is not None:
        path.append(node)
        node = parent[node]
    path.reverse()
    return path, visited_order

def print_maze_with_path(maze, path, start, goal):
    symbols = {}
    for node in path:
        symbols[node] = '*'
    symbols[start] = 'S'
    symbols[goal]  = 'G'
    for r, row in enumerate(maze):
        line = ""
        for c, cell in enumerate(row):
            if (r, c) in symbols:
                line += f" {symbols[(r,c)]} "
            elif cell == 1:
                line += " █ "
            else:
                line += " . "
        print(line)

path_bfs, visited_bfs = bfs_solve(MAZE_BFS, START_BFS, GOAL_BFS, ROWS_BFS, COLS_BFS)

print(f"\nStart: {START_BFS}   Goal: {GOAL_BFS}")
print(f"Nodes explored (BFS): {len(visited_bfs)}")

if path_bfs:
    print(f"Path length: {len(path_bfs)} steps")
    print(f"Path (row,col): {path_bfs}")
    print("\nMaze with BFS path (* = path, S = start, G = goal, █ = wall):")
    print_maze_with_path(MAZE_BFS, path_bfs, START_BFS, GOAL_BFS)
else:
    print("No path found.")


# =============================================================
# ── LAB 7  TASK 1 ── A* Maze Solver ──────────────────────────
# =============================================================
# Same kind of maze but larger (matches lab image: red start
# top-left corner, green goal bottom-right corner).
# Heuristic: Manhattan distance to goal.
# =============================================================

print("\n" + "=" * 60)
print("LAB 7  — TASK 1 : A* Maze Solver")
print("=" * 60)

# 9×9 maze grid — 0=open, 1=wall
# Red  start = (0,0)   top-left
# Green goal = (8,8)   bottom-right
MAZE_ASTAR = [
    [0,0,0,0,1,0,0,0,0,0],
    [0,0,1,0,0,0,1,1,0,0],
    [0,0,0,1,0,0,1,1,0,1],
    [0,1,0,0,1,0,0,0,1,1],
    [0,1,1,0,0,0,0,0,0,0],
    [0,1,0,0,1,1,1,0,1,1],
    [1,0,0,1,1,1,0,0,0,0],
    [0,1,1,1,0,0,0,0,0,0],
    [0,0,0,1,0,0,0,0,0,0],
    [1,0,1,1,1,0,0,0,1,0],
]
 
START_ASTAR = (0, 0)   # 'S'
GOAL_ASTAR  = (9, 9)   # 'G'

ROWS_ASTAR  = len(MAZE_ASTAR)
COLS_ASTAR  = len(MAZE_ASTAR[0])

def heuristic(node, goal):
    """Manhattan distance heuristic — admissible for grid movement."""
    return abs(node[0] - goal[0]) + abs(node[1] - goal[1])

def astar_solve(maze, start, goal, rows, cols):
    """
    A* search.
    Each move costs 1. Heuristic = Manhattan distance.
    Returns (path, nodes_expanded).
    """
    # Priority queue entries: (f, g, node)
    open_heap = []
    heapq.heappush(open_heap, (heuristic(start, goal), 0, start))

    came_from = {start: None}
    g_score   = {start: 0}
    expanded  = []

    while open_heap:
        f, g, current = heapq.heappop(open_heap)

        if current == goal:
            break

        expanded.append(current)
        r, c = current

        for dr, dc, _ in MOVES:
            nr, nc   = r + dr, c + dc
            neighbor = (nr, nc)

            if not (0 <= nr < rows and 0 <= nc < cols):
                continue
            if maze[nr][nc] == 1:
                continue

            tentative_g = g + 1
            if tentative_g < g_score.get(neighbor, float('inf')):
                g_score[neighbor]   = tentative_g
                came_from[neighbor] = current
                f_new = tentative_g + heuristic(neighbor, goal)
                heapq.heappush(open_heap, (f_new, tentative_g, neighbor))

    if goal not in came_from:
        return None, expanded

    path = []
    node = goal
    while node is not None:
        path.append(node)
        node = came_from[node]
    path.reverse()
    return path, expanded

path_astar, expanded_astar = astar_solve(
    MAZE_ASTAR, START_ASTAR, GOAL_ASTAR, ROWS_ASTAR, COLS_ASTAR)

print(f"\nStart: {START_ASTAR}   Goal: {GOAL_ASTAR}")
print(f"Nodes expanded (A*): {len(expanded_astar)}")

if path_astar:
    print(f"Path length: {len(path_astar)} steps")
    print(f"Path cost  : {len(path_astar) - 1}")
    print("\nPath coordinates (row, col):")
    for step, node in enumerate(path_astar):
        print(f"  Step {step:2d}: {node}")
    print("\nMaze with A* path (* = path, S = start, G = goal, █ = wall):")
    print_maze_with_path(MAZE_ASTAR, path_astar, START_ASTAR, GOAL_ASTAR)
else:
    print("No path found.")


# =============================================================
# ── LAB 11  TASK 1 ── 4-Queens CSP Solver ────────────────────
# =============================================================
# Place 4 queens on a 4×4 chessboard so no two queens
# attack each other (same row, column, or diagonal).
#
# CSP formulation:
#   Variables  : Q1, Q2, Q3, Q4  (one queen per column)
#   Domain     : {0,1,2,3}       (row index for each queen)
#   Constraints: no two queens share same row or diagonal
# =============================================================

print("\n" + "=" * 60)
print("LAB 11 — TASK 1 : 4-Queens CSP Solver")
print("=" * 60)

def count_conflicts(assignment):
    """Count the number of attacking pairs in a (partial) assignment."""
    conflicts = 0
    cols = list(assignment.keys())
    for i in range(len(cols)):
        for j in range(i + 1, len(cols)):
            c1, c2 = cols[i], cols[j]
            r1, r2 = assignment[c1], assignment[c2]
            # Same row or same diagonal
            if r1 == r2 or abs(r1 - r2) == abs(c1 - c2):
                conflicts += 1
    return conflicts

def is_consistent(col, row, assignment):
    """Check if placing a queen at (row, col) is consistent with assignment."""
    for c, r in assignment.items():
        if r == row:                        # same row
            return False
        if abs(r - row) == abs(c - col):    # same diagonal
            return False
    return True

def backtrack_4queens(assignment, domains, n=4):
    """
    Backtracking CSP solver.
    assignment: dict {col: row} for placed queens
    domains   : dict {col: [possible rows]}
    """
    if len(assignment) == n:
        return assignment  # complete solution

    # Select next unassigned column (MRV heuristic: smallest domain)
    unassigned = [c for c in range(n) if c not in assignment]
    col = min(unassigned, key=lambda c: len(domains[c]))

    for row in domains[col]:
        if is_consistent(col, row, assignment):
            assignment[col] = row
            # Forward checking: prune domains of remaining columns
            pruned = {}
            for other_col in unassigned:
                if other_col == col:
                    continue
                pruned[other_col] = []
                new_domain = [r for r in domains[other_col]
                              if is_consistent(other_col, r, {**assignment})]
                pruned[other_col] = domains[other_col]
                domains[other_col] = new_domain

            result = backtrack_4queens(assignment, domains, n)
            if result is not None:
                return result

            # Undo
            del assignment[col]
            for other_col, old_domain in pruned.items():
                domains[other_col] = old_domain

    return None  # backtrack

def find_all_solutions(n=4):
    """Find all solutions by brute force + constraint checking."""
    solutions = []
    def bt(assignment):
        if len(assignment) == n:
            if count_conflicts(assignment) == 0:
                solutions.append(dict(assignment))
            return
        col = len(assignment)
        for row in range(n):
            if is_consistent(col, row, assignment):
                assignment[col] = row
                bt(assignment)
                del assignment[col]
    bt({})
    return solutions

def print_board(assignment, n=4):
    """Pretty-print an n×n chessboard with queens."""
    for row in range(n):
        line = ""
        for col in range(n):
            if assignment.get(col) == row:
                line += " Q "
            else:
                shade = "░░░" if (row + col) % 2 == 0 else "███"
                line += shade
        print(line)

# Solve
domains_init = {col: list(range(4)) for col in range(4)}
solution = backtrack_4queens({}, domains_init)

print("\nCSP Variables  : Q0, Q1, Q2, Q3  (one queen per column)")
print("Domain         : {0, 1, 2, 3}  (row placement)")
print("Constraints    : no two queens in same row or diagonal")

if solution:
    conflicts = count_conflicts(solution)
    print(f"\nSolution found (conflicts = {conflicts}):")
    print("  Column → Row:", {f"Q{c}": r for c, r in sorted(solution.items())})
    print("\nBoard:")
    print_board(solution)
else:
    print("No solution found.")

all_sols = find_all_solutions()
print(f"\nAll valid solutions ({len(all_sols)} total):")
for idx, sol in enumerate(all_sols):
    print(f"\n  Solution {idx+1}: {[sol[c] for c in range(4)]}")
    print_board(sol)


print("\n" + "=" * 60)
print("All tasks completed.")
print("=" * 60)
