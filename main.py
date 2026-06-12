import pygame

from dfs import dfs
from bfs import bfs
from astar import astar

from visualize import (
    reset_screen,
    animate_search,
    move_player,
    reached_goal
)

pygame.init()

running = True

# Draw initial maze
reset_screen()

while running:

    for event in pygame.event.get():

        # Close Window
        if event.type == pygame.QUIT:
            running = False

        # Keyboard Input
        if event.type == pygame.KEYDOWN:

            # PLAYER MOVEMENT

            if event.key == pygame.K_UP:

                move_player(0, -1)
                reset_screen()

            elif event.key == pygame.K_DOWN:

                move_player(0, 1)
                reset_screen()

            elif event.key == pygame.K_LEFT:

                move_player(-1, 0)
                reset_screen()

            elif event.key == pygame.K_RIGHT:

                move_player(1, 0)
                reset_screen()

            # DFS

            elif event.key == pygame.K_1:

                path, explored = dfs()

                print("\n=== DFS ===")
                print("Explored Nodes:", len(explored))
                print("Path Length:", len(path))

                animate_search(
                    explored,
                    path,
                    "DFS"
                )

            # BFS

            elif event.key == pygame.K_2:

                path, explored = bfs()

                print("\n=== BFS ===")
                print("Explored Nodes:", len(explored))
                print("Path Length:", len(path))

                animate_search(
                    explored,
                    path,
                    "BFS"
                )

            # A*

            elif event.key == pygame.K_3:

                path, explored = astar()

                print("\n=== A* ===")
                print("Explored Nodes:", len(explored))
                print("Path Length:", len(path))

                animate_search(
                    explored,
                    path,
                    "A*"
                )

            # ESCAPE KEY

            elif event.key == pygame.K_ESCAPE:

                running = False

            # CHECK GOAL

            if reached_goal():

                print("\nYOU REACHED THE GOAL!")

                print(
                    "\nNow press:\n"
                    "1 = DFS\n"
                    "2 = BFS\n"
                    "3 = A*\n"
                    "to compare your solution with AI."
                )

pygame.quit()
