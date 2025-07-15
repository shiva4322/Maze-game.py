
def generate_maze(rows, cols):
    """
    Generates a random maze using Depth-First Search (DFS) algorithm.
    """
    def carve_passages_from(cx, cy, grid):
        directions = [(cx + 2, cy), (cx - 2, cy), (cx, cy + 2), (cx, cy - 2)]
        random.shuffle(directions)
        for nx, ny in directions:
            if 0 <= nx < rows and 0 <= ny < cols and grid[ny][nx] == WALL:
                grid[ny][nx] = EMPTY
                grid[ny + (cy - ny) // 2][nx + (cx - nx) // 2] = EMPTY
                carve_passages_from(nx, ny, grid)

    grid = [[WALL] * cols for _ in range(rows)]
    grid[1][1] = EMPTY
    carve_passages_from(1, 1, grid)
    grid[1][1] = START
    grid[-2][-2] = EXIT
    return grid


def find_shortest_path(maze):
    """
    Finds the shortest path from start to exit using A* algorithm.
    """
    rows, cols = len(maze), len(maze[0])
    start = None
    end = None

    for y in range(rows):
        for x in range(cols):
            if maze[y][x] == START:
                start = (y, x)
            elif maze[y][x] == EXIT:
                end = (y, x)

    if not start or not end:
        return []

    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    open_set = deque([start])
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, end)}

    while open_set:
        current = min(open_set, key=lambda o: f_score.get(o, float('inf')))
        if current == end:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path

        open_set.remove(current)

        for d in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            neighbor = (current[0] + d[0], current[1] + d[1])
            if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols and maze[neighbor[0]][neighbor[1]] != WALL:
                tentative_g_score = g_score[current] + 1
                if tentative_g_score < g_score.get(neighbor, float('inf')):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic(neighbor, end)
                    if neighbor not in open_set:
                        open_set.append(neighbor)

    return []
def print_maze(maze, path=None):
    """
    Prints the maze with optional path highlighting.
    """
    path = path or []
    path_set = set(path)
    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            if (y, x) in path_set:
                print('*', end="")
            else:
                print(cell, end="")
        print()