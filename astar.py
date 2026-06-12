import heapq
import maze

from heuristics import manhattan

directions = [
    (-1, 0),
    (1, 0),
    (0, -1),
    (0, 1)
]

def astar():

    open_list = []

    heapq.heappush(
        open_list,
        (0, maze.start, [maze.start])
    )

    visited = set()

    explored_order = []

    while open_list:

        cost, current, path = heapq.heappop(open_list)

        if current == maze.goal:
            return path, explored_order

        if current in visited:
            continue

        visited.add(current)

        explored_order.append(current)

        row, col = current

        for dr, dc in directions:

            new_row = row + dr
            new_col = col + dc

            neighbor = (new_row, new_col)

            if (
                0 <= new_row < len(maze.maze)
                and 0 <= new_col < len(maze.maze[0])
                and maze.maze[new_row][new_col] == 0
                and neighbor not in visited
            ):

                g_cost = len(path)

                h_cost = manhattan(neighbor,maze.goal)

                f_cost = g_cost + h_cost

                heapq.heappush(
                    open_list,
                    (
                        f_cost,
                        neighbor,
                        path + [neighbor]
                    )
                )

    return None, explored_order