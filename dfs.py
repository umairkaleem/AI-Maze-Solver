import maze

directions = [
    (1, 0),    
    (0, 1),    
    (-1, 0),   
    (0, -1)   
]

def dfs():

    stack = [(maze.start, [maze.start])]

    visited = set()

    explored_order = []

    step = 0

    while stack:

        current, path = stack.pop()

        if current in visited:
            continue

        step += 1

        print(f"Step {step}: DFS Exploring {current}")

        visited.add(current)

        explored_order.append(current)

        if current == maze.goal:

            print("GOAL FOUND!")

            return path, explored_order

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

                stack.append(
                    (
                        neighbor,
                        path + [neighbor]
                    )
                )

    return None, explored_order