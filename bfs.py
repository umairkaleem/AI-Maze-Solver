from collections import deque
import maze

directions = [
    (-1, 0),  
    (1, 0),   
    (0, -1),  
    (0, 1)    
]

def bfs():

    queue = deque([(maze.start, [maze.start])])

    visited = set()

    explored_order = []

    step = 0

    while queue:

        current, path = queue.popleft()

        if current in visited:
            continue

        step += 1

        print(f"Step {step}: BFS Exploring {current}")

        visited.add(current)

        explored_order.append(current)

        if current == maze.goal:

            print("\nGOAL FOUND!")

            print("\nShortest Path:")
            print(path)

            print("\nPath Length:", len(path))

            return path, explored_order

        row, col = current

        for dr, dc in directions:

            new_row = row + dr
            new_col = col + dc

            neighbor = (new_row, new_col)

            if (
                0 <= new_row < len(maze.maze) and 0 <= new_col < len(maze.maze[0]) and maze.maze[new_row][new_col] == 0 and neighbor not in visited
            ):

                queue.append(
                    (
                        neighbor,
                        path + [neighbor]
                    )
                )

    return None, explored_order