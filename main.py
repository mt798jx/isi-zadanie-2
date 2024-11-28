from copy import deepcopy

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

        # 3. Kontrola: Čierne políčka tvoria súvislú cestu
        visited = [[False] * self.n for _ in range(self.n)]
        def dfs_black(x, y):
            """
            DFS na kontrolu súvislosti čiernych políčok.
            """
            stack = [(x, y)]
            connected_black_count = 0

            while stack:
                cx, cy = stack.pop()
                if visited[cx][cy]:
                    continue
                visited[cx][cy] = True
                connected_black_count += 1

                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nx, ny = cx + dx, cy + dy
                    if 0 <= nx < self.n and 0 <= ny < self.n and not visited[nx][ny]:
                        if grid[nx][ny] == -1:
                            stack.append((nx, ny))

            return connected_black_count

        # Nájdeme prvé čierne políčko a skontrolujeme súvislosť
        black_cells_count = sum(cell == -1 for row in grid for cell in row)
        for i in range(self.n):
            for j in range(self.n):
                if grid[i][j] == -1:
                    # Spustíme DFS z prvého čierneho políčka
                    if dfs_black(i, j) != black_cells_count:
                        return False
                    break
            else:
                continue
            break

        # 4. Kontrola: Počet bielych políčok je správny
        total_white_cells = sum(cell for row in self.grid for cell in row if cell > 0)
        current_white_cells = sum(cell >= 0 for row in grid for cell in row)
        if current_white_cells != total_white_cells:
            return False

        # Kontrola, že čísla z pôvodnej mriežky sa zachovali
        for i in range(self.n):
            for j in range(self.n):
                if self.grid[i][j] > 0 and self.grid[i][j] != grid[i][j]:
                    return False

        # 5. Kontrola: Každý ostrov musí byť súvislý, obsahovať správny počet políčok a políčka nesmú byť zdieľané
        visited = [[False] * self.n for _ in range(self.n)]

        def dfs(x, y, required_size):
            """
            DFS na kontrolu ostrova a kontrolu, že políčka nie sú zdieľané.
            """
            stack = [(x, y)]
            size = 0
            contains_number = False

            while stack:
                cx, cy = stack.pop()
                # Ak je políčko už navštívené, znamená to konflikt s iným ostrovom
                if visited[cx][cy]:
                    return False
                visited[cx][cy] = True
                size += 1
                if self.grid[cx][cy] > 0:
                    contains_number = True

                # Prechádzame susedov
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nx, ny = cx + dx, cy + dy
                    if 0 <= nx < self.n and 0 <= ny < self.n and not visited[nx][ny]:
                        if grid[nx][ny] >= 0:  # Len biele políčka a čísla
                            stack.append((nx, ny))

            # Ostrov musí obsahovať správny počet políčok a aspoň jedno číslo
            return size == required_size and contains_number

        for i in range(self.n):
            for j in range(self.n):
                # Začíname ostrov s číslom, ak dané políčko ešte nebolo navštívené
                if self.grid[i][j] > 0:
                    if not dfs(i, j, self.grid[i][j]):
                        return False
        return True

    def dfs(self, grid, row, col):
        # Ak sme prešli celú mriežku, overíme, či je riešenie platné
        if col == self.n:
            if self.is_valid(grid):
                self.solutions.append([row[:] for row in grid])
            return

        # Prechod na ďalšiu bunku (do hĺbky - prioritne po riadkoch v stĺpci)
        next_row, next_col = (row + 1, col) if row < self.n - 1 else (0, col + 1)

        # Skúšanie prvej možnosti, ponechať hodnotu 0
        self.dfs([row[:] for row in grid], next_row, next_col)

        # Skúšanie ďalšej možnosti, nastaviť hodnotu -1
        new_grid = [row[:] for row in grid]
        new_grid[row][col] = -1
        self.visited_states += 1
        self.dfs(new_grid, next_row, next_col)

    def solve(self):
        """
        Spustí DFS na vyriešenie hlavolamu.
        """
        self.dfs([row[:] for row in self.grid], 0, 0)
        return self.solutions

    def is_partial_valid(self, grid):
        """
        Rýchla kontrola na čiastočne platný stav mriežky.
        """
        # 1. Kontrola: Neexistencia 2x2 čiernych blokov (-1)
        for i in range(self.n - 1):
            for j in range(self.n - 1):
                if (
                        grid[i][j] == -1 and grid[i + 1][j] == -1 and
                        grid[i][j + 1] == -1 and grid[i + 1][j + 1] == -1
                ):
                    return False

        # 2. Kontrola: Každé číslo v pôvodnej mriežke musí byť stále dostupné
        for i in range(self.n):
            for j in range(self.n):
                if self.grid[i][j] > 0 and grid[i][j] != self.grid[i][j]:
                    return False

        return True

    def backtrack(self, grid, row, col):
        """
        Backtracking na riešenie mriežky.
        """

        self.visited_states += 1

        # Ak sme prešli celú mriežku, overíme, či je riešenie platné
        if row == self.n:
            if self.is_valid(grid):
                self.solutions.append(deepcopy(grid))
            return

        # Prechod na ďalšiu bunku (po riadkoch zľava doprava)
        next_row, next_col = (row, col + 1) if col < self.n - 1 else (row + 1, 0)

        # Ak je bunka pevne daná (číslo v pôvodnej mriežke), preskočíme ju
        if self.grid[row][col] > 0:
            self.backtrack(deepcopy(grid), next_row, next_col)
            return

        # Skúšanie prvej možnosti: biela bunka (0)
        grid[row][col] = 0
        if self.is_partial_valid(grid):
            self.backtrack(deepcopy(grid), next_row, next_col)

        # Skúšanie druhej možnosti: čierna bunka (-1)
        grid[row][col] = -1
        if self.is_partial_valid(grid):
            self.backtrack(deepcopy(grid), next_row, next_col)

        # Spätný krok (reset bunky)
        grid[row][col] = 0


def print_grid(grid):
    """
    Funkcia na vykreslenie mriežky do konzoly, kde hodnota -1 je zobrazená ako 'x'.
    """
    for row in grid:
        print(" ".join('x' if cell == -1 else str(cell) for cell in row))
    print()


# Príklad použitia
if __name__ == "__main__":
    initial_grid = [
        [2, 0, 0, 0, 1],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0],
        [0, 0, 0, 6, 0],
    ]

    print("Počiatočná mriežka:")
    print_grid(initial_grid)

    solver = NurikabeSolver(initial_grid)

    # Vyber metódy
    while True:
        method = input("Vyberte metódu riešenia (dfs/backtrack): ").strip().lower()
        if method in ["dfs", "backtrack"]:
            break
        print("Nesprávna voľba. Zadajte 'dfs' alebo 'backtrack'.")

    if method == "dfs":
        print("\nDFS riešenie:")
        solver.visited_states = 0
        solver.dfs(deepcopy(solver.grid), 0, 0)
    elif method == "backtrack":
        print("\nBacktracking riešenie:")
        solver.visited_states = 0
        solver.backtrack(deepcopy(solver.grid), 0, 0)

    # Výstup výsledkov
    print(f"Počet riešení: {len(solver.solutions)}")
    print(f"Počet navštívených stavov: {solver.visited_states}\n")

    for idx, solution in enumerate(solver.solutions, 1):
        print(f"Riešenie {idx}:")
        print_grid(solution)

        if solver.is_valid(solution):
            print("Riešenie je validné.")
        else:
            print("Riešenie nie je validné.")
