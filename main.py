class NurikabeSolver:
    def __init__(self, grid):
        self.grid = grid  # 5x5 grid (list of lists)
        self.n = len(grid)
        self.solutions = []
        self.visited_states = 0

    def is_valid(self, grid):
        """
        Funkcia na overenie, či je stav mriežky validný.
        """
        # 1. Kontrola: Neexistencia 2x2 čiernych blokov (-1)
        for i in range(self.n - 1):
            for j in range(self.n - 1):
                if (
                    grid[i][j] == -1 and grid[i + 1][j] == -1 and
                    grid[i][j + 1] == -1 and grid[i + 1][j + 1] == -1
                ):
                    return False

        # 2. Kontrola: Každé čierne políčko má aspoň jedného suseda s hodnotou -1
        for i in range(self.n):
            for j in range(self.n):
                if grid[i][j] == -1:
                    has_black_neighbor = False
                    for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        ni, nj = i + di, j + dj
                        if 0 <= ni < self.n and 0 <= nj < self.n and grid[ni][nj] == -1:
                            has_black_neighbor = True
                            break
                    if not has_black_neighbor:
                        return False

        # 3. Kontrola: Počet bielych políčok je správny
        total_white_cells = sum(cell for row in self.grid for cell in row if cell > 0)
        current_white_cells = sum(cell >= 0 for row in grid for cell in row)
        if current_white_cells != total_white_cells:
            return False

        return True

    def dfs(self, grid, row, col):
        # Ak sme prešli celú mriežku, overíme, či je riešenie platné
        if col == self.n:
            if self.is_valid(grid):
                self.solutions.append([row[:] for row in grid])  # Uloženie riešenia
            return

        # Prechod na ďalšiu bunku (do hĺbky - prioritne po riadkoch v stĺpci)
        next_row, next_col = (row + 1, col) if row < self.n - 1 else (0, col + 1)

        # Skúšanie prvej možnosti, ponechať hodnotu 0
        self.dfs([row[:] for row in grid], next_row, next_col)

        # Skúšanie ďalšej možnosti, nastaviť hodnotu -1
        new_grid = [row[:] for row in grid]  # Vytvorenie kópie mriežky
        new_grid[row][col] = -1
        self.visited_states += 1
        self.dfs(new_grid, next_row, next_col)

    def solve(self):
        """
        Spustí DFS na vyriešenie hlavolamu.
        """
        self.dfs([row[:] for row in self.grid], 0, 0)
        return self.solutions


def print_grid(grid):
    """
    Funkcia na vykreslenie mriežky do konzoly.
    """
    for row in grid:
        print(" ".join(map(str, row)))
    print()


# Príklad použitia
if __name__ == "__main__":
    initial_grid = [
        [0, 0, 3, 0, 0],
        [0, 3, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [2, 0, 0, 0, 4],
    ]

    print("Počiatočná mriežka:")
    print_grid(initial_grid)

    solver = NurikabeSolver(initial_grid)
    solutions = solver.solve()

    print(f"Počet navštívených stavov: {solver.visited_states}")
    print(f"Nájdené riešenia: {len(solutions)}\n")

    for idx, solution in enumerate(solutions, 1):
        print(f"Riešenie {idx}:")
        print_grid(solution)

        if solver.is_valid(solution):
            print("Riešenie je validné.")
        else:
            print("Riešenie nie je validné.")

        if idx > 10: break
