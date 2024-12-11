import time
from copy import deepcopy

directions = [
    # (row, col)
    [(-1, 0), (-1, -1), (0, -1)],
    [(0, -1), (1, -1), (1, 0)],
    [(1, 0), (1, 1), (0, 1)],
    [(0, 1), (-1, 1), (-1, 0)]
]

class NurikabeSolver:
    def __init__(self, grid):
        self.grid = grid  # 5x5 grid (list of lists)
        self.n = len(grid)
        self.solutions = []
        self.visited_states = 0
        self.final_states = 0
        self.islands = [] # zapisuje si stavy bielych ostrovov
        self.islands_size = 0

        for row in range(self.n):
            for col in range(self.n):
                if grid[row][col] != 0:
                    self.islands.append([(row, col)])
                    self.islands_size += grid[row][col]

    def dfs(self, grid, row, col):
        """
        Riešenie pomocou hĺbkového prehľadávania (DFS).
        """
        self.refresh_grid_print(grid)
        # Ak sme prešli celú mriežku, overíme, či je riešenie platné
        if col == self.n:
            self.set_undefined_fields_to(grid, 1)
            if self.is_valid_grid(grid) and self.is_islands_connected(grid):
                self.solutions.append([row[:] for row in grid])
            return

        # Prechod na ďalšiu bunku (do hĺbky - prioritne po riadkoch v stĺpci)
        next_row, next_col = (row + 1, col) if row < self.n - 1 else (0, col + 1)

        self.visited_states += 1

        self.refresh_grid_print(grid)

        # Skúšanie prvej možnosti, ponechať hodnotu 0
        self.dfs([row[:] for row in grid], next_row, next_col)

        # Skúšanie ďalšej možnosti, nastaviť hodnotu -1
        new_grid = [row[:] for row in grid]
        new_grid[row][col] = -1
        self.dfs(new_grid, next_row, next_col)

    def is_partial_valid(self, grid, row, col):
        """
        Rýchla kontrola na čiastočne platný stav mriežky pre konkrétnu zmenu.
        """
        # 1. Kontrola: Neexistencia 2x2 čiernych blokov (-1) iba okolo bunky [row][col]
        for i in range(max(0, row - 1), min(self.n - 1, row + 1)):
            for j in range(max(0, col - 1), min(self.n - 1, col + 1)):
                if (
                        grid[i][j] == -1 and grid[i + 1][j] == -1 and
                        grid[i][j + 1] == -1 and grid[i + 1][j + 1] == -1
                ):
                    return False

        # 2. Kontrola: Pevné hodnoty v pôvodnej mriežke sa nesmú meniť
        if self.grid[row][col] > 0 and grid[row][col] != self.grid[row][col]:
            return False

        return True

    def backtrack(self, grid, row, col):
        self.refresh_grid_print(grid)
        """
        Čistý backtracking na riešenie mriežky bez deepcopy a validácie čiastočných stavov.
        """
        # Ak sme prešli celú mriežku, overíme, či je riešenie platné
        if row == self.n:
            self.set_undefined_fields_to(grid, 1)
            if self.is_valid_grid(grid) and self.is_islands_connected(grid):
                # if grid not in self.solutions:
                self.solutions.append([row[:] for row in grid])
            return

        # Prechod na ďalšiu bunku (po riadkoch zľava doprava)
        next_row, next_col = (row, col + 1) if col < self.n - 1 else (row + 1, 0)
        self.refresh_grid_print(grid)

        # Ak je bunka pevne daná (číslo v pôvodnej mriežke), preskočíme ju
        if self.grid[row][col] > 0:
            self.backtrack(grid, next_row, next_col)
            return

        # Skúšanie prvej možnosti: biela bunka (0)
        grid[row][col] = 0
        if self.is_partial_valid(grid, row, col):
            self.visited_states += 1
            self.backtrack(grid, next_row, next_col)

        # Skúšanie druhej možnosti: čierna bunka (-1)
        grid[row][col] = -1
        if self.is_partial_valid(grid, row, col):
            self.visited_states += 1
            self.backtrack(grid, next_row, next_col)

        # Spätný krok (reset bunky)
        grid[row][col] = 0

    def solve(self):
        """
        Spustí DFS na vyriešenie hlavolamu.
        """
        self.dfs([row[:] for row in self.grid], 0, 0)
        return self.solutions

    def set_undefined_fields_to(self, grid, set_to):
        for row in range(self.n):
            for col in range(self.n):
                if grid[row][col] == 0:
                    grid[row][col] = set_to

    def filter(self, grid):
        """
        Filter na riešenie mriežky.
        """
        if self.is_islands_final_sizes():
            self.set_undefined_fields_to(grid, -1)
            if self.is_valid_grid(grid):
                if grid not in self.solutions:
                    self.solutions.append([row[:] for row in grid])
            return
        grid_copy = deepcopy(grid)
        self.eliminate_island_directions(grid_copy)
        #self.refresh_grid_print(grid_copy)

        for island in self.islands:
            if len(island) == grid_copy[island[0][0]][island[0][1]]:
                continue
            for isle in island:
                for direction in directions:
                    tmp_isle = (isle[0] + direction[0][0],
                                isle[1] + direction[0][1])
                    # Je True ak je stav políčka nedefinovaný
                    if self.is_within_boundaries(tmp_isle[0], tmp_isle[1]) and grid_copy[tmp_isle[0]][tmp_isle[1]] == 0:
                        grid_copy[tmp_isle[0]][tmp_isle[1]] = 1
                        island.append(tmp_isle)
                        self.visited_states += 1
                        self.filter(grid_copy)
                        grid_copy[tmp_isle[0]][tmp_isle[1]] = 0
                        island.pop()
                        #self.refresh_grid_print(grid_copy) # Refreshne grid, funguje len pri spúšťaní cez terminál

    #Funkcia eliminuje poliíčka, ktoré vieme že nemá zmysel ďalej kontrolovať
    def eliminate_island_directions(self, grid) -> None:
        for island in self.islands:
            # Ak biely ostrov dovŕšil svoju maximálnu veľkosť, eliminujeme políčka vôkol neho (nemá zmysel tam expandovať)
            if len(island) == grid[island[0][0]][island[0][1]]:
                self.eliminate_fields_around_island(grid, island)
                continue
            for isle in island:
                for direction in directions:
                    tmp_isle = (isle[0] + direction[1][0],
                                isle[1] + direction[1][1])
                    # Kontroluje diagonaly ostrovov, ak je na diagonale cudzi ostrov -> eliminuje linie
                    if self.is_within_boundaries(tmp_isle[0], tmp_isle[1]) and 0 < grid[tmp_isle[0]][
                        tmp_isle[1]] and tmp_isle not in island:
                        grid[isle[0] + direction[0][0]][isle[1] + direction[0][1]] = -1
                        grid[isle[0] + direction[2][0]][isle[1] + direction[2][1]] = -1
                    tmp_isle = (isle[0] + direction[0][0] * 2,
                                isle[1] + direction[0][1] * 2)
                    # Kontroluje vertikaly a horizontaly, ak je tam cudzi ostrov -> eliminuje linie
                    if self.is_within_boundaries(tmp_isle[0], tmp_isle[1]) and 0 < grid[tmp_isle[0]][
                        tmp_isle[1]] and tmp_isle not in island:
                        grid[isle[0] + direction[0][0]][isle[1] + direction[0][1]] = -1

    #Funkcia eliminuje políčka na ôkol ostrova
    def eliminate_fields_around_island(self, grid, island):
        for isle in island:
            for direction in directions:
                tmp_isle = (isle[0] + direction[0][0],
                            isle[1] + direction[0][1])
                if self.is_within_boundaries(tmp_isle[0], tmp_isle[1]) and 0 == grid[tmp_isle[0]][tmp_isle[1]]:
                    grid[tmp_isle[0]][tmp_isle[1]] = -1

    def is_within_boundaries(self, col, row) -> bool:
        return 0 <= row < self.n and 0 <= col < self.n

    def is_islands_final_sizes(self) -> bool:
        islands_sizes = 0
        fin_size = 0
        for island in self.islands:
            fin_size += self.grid[island[0][0]][island[0][1]]
            islands_sizes += len(island)
        return not islands_sizes < fin_size

    def refresh_grid_print(self, grid):
        print(f"Počet navšívaných stavov: {self.visited_states}\nPočet konečných riešení: " , end="\n")
        print("\033[H\033[J", end="")
        time.sleep(0.2)
        print_grid(grid, self.islands)

    def is_valid_grid(self, grid) -> bool:
        all_black_count = sum(row.count(-1) for row in grid)
        if all_black_count != self.n * self.n - self.islands_size:
            return False

        for row in range(self.n):
            for col in range(self.n):
                if grid[row][col] == -1:
                    black_in_row = self.is_valid_grid_recursive(grid, row, col)
                    self.set_undefined_fields_to(grid, -1)
                    return all_black_count == black_in_row

    def is_valid_grid_recursive(self, grid, row, col) -> int:
        black_cnt = 0
        grid[row][col] = 0
        for direction in directions:
            is_square = True
            if not self.is_within_boundaries(row + direction[1][0], col + direction[1][1]):
                continue
            for x_i, y_i in direction:
                if grid[row + x_i][col + y_i] != -1:
                    is_square = False
                    break
            if is_square:
                return -1
        for direction in directions:
            tmp_isle = (row + direction[0][0],
                        col + direction[0][1])
            if self.is_within_boundaries(tmp_isle[0], tmp_isle[1]) and grid[tmp_isle[0]][tmp_isle[1]] == -1:
                black_cnt += self.is_valid_grid_recursive(grid, tmp_isle[0], tmp_isle[1])
        return black_cnt + 1

    def is_islands_connected(self, grid) -> bool:
        for island in self.islands:
            tmp = grid[island[0][0]][island[0][1]]
            if not self.is_island_connected_rec(grid, island[0][0], island[0][1]) == tmp:
                grid[island[0][0]][island[0][1]] = tmp
                return False
            grid[island[0][0]][island[0][1]] = tmp
        self.set_undefined_fields_to(grid, 1)
        return True

    def is_island_connected_rec(self, grid, row, col) -> int:
        white_cnt = 0
        grid[row][col] = 0
        for direction in directions:
            tmp_isle = (row + direction[0][0],
                        col + direction[0][1])

            if self.is_within_boundaries(tmp_isle[0], tmp_isle[1]) and grid[tmp_isle[0]][tmp_isle[1]] > 0:
                if tmp_isle in [x[0] for x in self.islands]:
                    return white_cnt - 1
                white_cnt += self.is_island_connected_rec(grid, tmp_isle[0], tmp_isle[1])
        return white_cnt + 1


def print_grid(grid, islands):
    """
    Funkcia na vykreslenie mriežky do konzoly, kde hodnota -1 je zobrazená ako 'x'.
    """
    print("+---+---+---+---+---+")
    for row in range(len(grid)):
        print("|", end="")
        for col in range(len(grid)):
            if grid[row][col] == -1:
                #  Black field
                print(' x', end=' |')
            elif grid[row][col] == 0:
                # Undefined field
                print('  ', end=' |')
            else:
                # Island
                tmp_tuple = (row, col)
                if tmp_tuple in [row_i[0] for row_i in islands]:
                    if grid[row][col] > 9:
                        print(grid[row][col], end=' |')
                    else:
                        print(" ", end="")
                        print(grid[row][col], end=' |')
                else:
                    print(' o', end=' |')
        print(

        )
    print("+---+---+---+---+---+")

def format_times(end_time, start_time):
    seconds = end_time - start_time
    minutes = int((seconds % 3600) // 60)
    seconds = round(seconds % 60, 3)
    return str(minutes) + " minúty, " + str(seconds) + " sekundy"

# Príklad použitia
if __name__ == "__main__":
    initial_grids = [
        [
            [2, 0, 0, 0, 1],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0],
            [0, 0, 0, 6, 0],
        ],
        [
            [0, 0, 3, 0, 0],
            [0, 3, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [2, 0, 0, 0, 4]
        ],
        [
            [0, 0, 0, 0, 0],
            [0, 12, 0, 1, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]
        ],
        [
            [1, 0, 0, 0, 2],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 3, 0, 0, 0],
            [0, 0, 0, 3, 0]
        ],
        [
            [0, 0, 3, 0, 0],
            [0, 3, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [2, 0, 0, 0, 4]
        ],
        [
            [0, 0, 3, 0, 0],
            [0, 3, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [2, 0, 0, 0, 4]
        ],
        [
            [0, 0, 0, 2, 0],
            [3, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 5],
            [0, 0, 1, 0, 0]
        ],
        [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 3, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 4, 0],
            [0, 0, 0, 0, 0]
        ],
        [
            [1, 0, 0, 0, 0],
            [0, 3, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 4, 0],
            [4, 0, 0, 0, 0]
        ],
        [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 10],
            [0, 0, 0, 2, 0],
            [0, 0, 0, 0, 0],
            [0, 2, 0, 0, 0]
        ]
    ]

    initial_grid = initial_grids[9]

    solver = NurikabeSolver(initial_grid)

    print("Počiatočná mriežka:")
    print_grid(initial_grid, solver.islands)

    # Vyber metódy
    while True:
        method = input("Vyberte metódu riešenia (dfs/backtrack/filter): ").strip().lower()
        if method in ["dfs", "backtrack", "filter"]:
            break
        print("Nesprávna voľba. Zadajte 'dfs' alebo 'backtrack' alebo 'filter'.")

    start_time = time.time()
    if method == "dfs":
        print("\nDFS riešenie:")
        solver.visited_states = 0
        solver.dfs(deepcopy(solver.grid), 0, 0)
    elif method == "backtrack":
        print("\nBacktracking riešenie:")
        solver.visited_states = 0
        solver.backtrack(deepcopy(solver.grid), 0, 0)
    elif method == "filter":
        print("\nForward filter riešenie:")
        solver.visited_states = 0
        solver.filter(deepcopy(solver.grid))
    end_time = time.time()

    # Výstup výsledkov
    print(f"Počet riešení: {len(solver.solutions)}")
    print(f"Počet navštívených stavov: {solver.visited_states}")
    print(f"Dĺžka výpočtu: {format_times(end_time, start_time)}\n")

    for idx, solution in enumerate(solver.solutions, 1):
        print(f"Riešenie {idx}:")
        print_grid(solution, solver.islands)