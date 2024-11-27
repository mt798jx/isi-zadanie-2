import random
import copy

def generate_random_puzzle(size=5):
    grid = [[0 for _ in range(size)] for _ in range(size)]
    num_islands = random.randint(2, 4)  # Náhodný počet ostrovov
    placed_positions = set()  # Množina obsadených políčok

    for _ in range(num_islands):
        while True:
            x, y = random.randint(0, size - 1), random.randint(0, size - 1)
            if (x, y) not in placed_positions:  # Skontroluj, či nie je políčko obsadené
                grid[x][y] = random.randint(1, 4)  # Veľkosť ostrova
                placed_positions.add((x, y))  # Označ políčko ako obsadené
                break  # Ukonči cyklus pre toto políčko
    return grid

# Funkcia na kontrolu platnosti pohybu
def is_valid(grid, x, y, visited):
    size = len(grid)
    return 0 <= x < size and 0 <= y < size and grid[x][y] == 0 and (x, y) not in visited

# DFS na vytvorenie ostrova
def dfs_island(grid, x, y, target_size, visited):
    if len(visited) == target_size:
        return True

    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Smer pohybu
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if is_valid(grid, nx, ny, visited):
            visited.add((nx, ny))
            if dfs_island(grid, nx, ny, target_size, visited):
                return True
            visited.remove((nx, ny))
    return False

# DFS na riešenie celého puzzle
def dfs_solve(grid, current_grid, x, y):
    size = len(grid)
    if x == size:  # Ak sa dostaneme mimo maticu, riešenie je platné
        return True

    next_x, next_y = (x + 1, 0) if y + 1 == size else (x, y + 1)  # Prechod na ďalšie políčko

    if grid[x][y] > 0:  # Ak je na políčku číslo (ostrov)
        visited = set()
        visited.add((x, y))
        if not dfs_island(current_grid, x, y, grid[x][y], visited):  # Skús vytvoriť ostrov
            return False
        for vx, vy in visited:  # Označ ostrov ako vyplnený
            current_grid[vx][vy] = 1
        if dfs_solve(grid, current_grid, next_x, next_y):
            return True
        for vx, vy in visited:  # Vráť zmeny späť
            current_grid[vx][vy] = 0
    else:  # Ak je políčko prázdne, môže byť more alebo ostrov
        current_grid[x][y] = -1  # Skús označiť ako more
        if dfs_solve(grid, current_grid, next_x, next_y):
            return True
        current_grid[x][y] = 0  # Vráť zmeny späť
    return False

# Hlavná funkcia na riešenie puzzle
def solve_nurikabe(grid):
    size = len(grid)
    current_grid = [[0 for _ in range(size)] for _ in range(size)]  # Pracovná kópia mriežky
    if dfs_solve(grid, current_grid, 0, 0):
        return current_grid
    return None

# Výstupná funkcia na zobrazenie hracej plochy
def print_grid(grid):
    for row in grid:
        print(' '.join(f'{cell:2}' for cell in row))
    print()

# Testovanie
if __name__ == "__main__":
    random.seed(0)  # Pre reprodukovateľnosť výsledkov
    puzzles = [generate_random_puzzle() for _ in range(10)]  # Generovanie 10 štartovacích stavov

    for i, puzzle in enumerate(puzzles):
        print(f"Puzzle {i + 1}:")
        print_grid(puzzle)
        solution = solve_nurikabe(puzzle)
        if solution:
            print("Solved Puzzle:")
            print_grid(solution)
        else:
            print("No solution found.")
