import pygame
import time
import maze

pygame.init()

# WINDOW SETTINGS

WIDTH = 1000
HEIGHT = 750

CELL_SIZE = 60

ROWS = len(maze.maze)
COLS = len(maze.maze[0])

# COLORS

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

GREEN = (0, 255, 0)
RED = (255, 0, 0)

BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

GRAY = (180, 180, 180)

PURPLE = (160, 32, 240)

LIGHT_BLUE = (100, 149, 237)

DARK_GRAY = (40, 40, 40)

PANEL_BG = (230, 230, 230)

# SCREEN

screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption(
    "Interactive AI Pathfinding Learning System"
)

# FONTS

font = pygame.font.SysFont(None, 30)

small_font = pygame.font.SysFont(None, 18)

# PLAYER

player_pos = list(maze.start)

player_path = [tuple(player_pos)]



# DRAW GRID


def draw_grid():

    for row in range(ROWS):

        for col in range(COLS):

            rect = pygame.Rect(
                col * CELL_SIZE,
                row * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE
            )

            # WALL
            if maze.maze[row][col] == 1:

                pygame.draw.rect(
                    screen,
                    BLACK,
                    rect
                )

            # EMPTY CELL
            else:

                pygame.draw.rect(
                    screen,
                    WHITE,
                    rect
                )

            pygame.draw.rect(
                screen,
                GRAY,
                rect,
                1
            )


# DRAW PLAYER PATH


def draw_player_path():

    for node in player_path:

        row, col = node

        rect = pygame.Rect(
            col * CELL_SIZE,
            row * CELL_SIZE,
            CELL_SIZE,
            CELL_SIZE
        )

        pygame.draw.rect(
            screen,
            LIGHT_BLUE,
            rect
        )

        pygame.draw.rect(
            screen,
            GRAY,
            rect,
            1
        )

        # SHOW COORDINATES
        coord_text = small_font.render(
            f"({row},{col})",
            True,
            BLACK
        )

        screen.blit(
            coord_text,
            (
                col * CELL_SIZE + 3,
                row * CELL_SIZE + 20
            )
        )



# DRAW START & GOAL


def draw_start_goal():

    # START
    s_row, s_col = maze.start

    pygame.draw.rect(
        screen,
        GREEN,
        (
            s_col * CELL_SIZE,
            s_row * CELL_SIZE,
            CELL_SIZE,
            CELL_SIZE
        )
    )

    # GOAL
    g_row, g_col = maze.goal

    pygame.draw.rect(
        screen,
        RED,
        (
            g_col * CELL_SIZE,
            g_row * CELL_SIZE,
            CELL_SIZE,
            CELL_SIZE
        )
    )

# =========================
# DRAW PLAYER
# =========================


def draw_player():

    row, col = player_pos

    pygame.draw.rect(
        screen,
        PURPLE,
        (
            col * CELL_SIZE + 10,
            row * CELL_SIZE + 10,
            CELL_SIZE - 20,
            CELL_SIZE - 20
        )
    )

# =========================
# DRAW TEXT
# =========================


def draw_text():

    instructions = [

        "Arrow Keys = Move Player",
        "1 = DFS",
        "2 = BFS",
        "3 = A*",
        "ESC = Quit"

    ]

    y = 620

    for text in instructions:

        rendered = font.render(
            text,
            True,
            BLACK
        )

        screen.blit(
            rendered,
            (20, y)
        )

        y += 25

# =========================
# AI LOGIC PANEL
# =========================


def draw_ai_panel(
    algorithm="None",
    current=None,
    g_cost=None,
    h_cost=None,
    f_cost=None,
    message=""
):

    panel_x = 620

    panel_rect = pygame.Rect(
        panel_x,
        0,
        380,
        HEIGHT
    )

    pygame.draw.rect(
        screen,
        PANEL_BG,
        panel_rect
    )

    title = font.render(
        "AI LOGIC PANEL",
        True,
        BLACK
    )

    screen.blit(
        title,
        (panel_x + 20, 20)
    )

    info = [

        f"Algorithm: {algorithm}",
        "",
        f"Current Node: {current}",
        "",
        f"g(n): {g_cost}",
        f"h(n): {h_cost}",
        f"f(n): {f_cost}",
        "",
        "Decision:",
        message

    ]

    y = 80

    for line in info:

        rendered = font.render(
            line,
            True,
            DARK_GRAY
        )

        screen.blit(
            rendered,
            (panel_x + 20, y)
        )

        y += 40

# =========================
# RESET SCREEN
# =========================


def reset_screen():

    screen.fill(WHITE)

    draw_grid()

    draw_player_path()

    draw_start_goal()

    draw_player()

    draw_text()

    pygame.display.update()

# =========================
# MOVE PLAYER
# =========================


def move_player(dx, dy):

    new_row = player_pos[0] + dy

    new_col = player_pos[1] + dx

    if (
        0 <= new_row < ROWS
        and 0 <= new_col < COLS
    ):

        if maze.maze[new_row][new_col] == 0:

            new_position = (new_row, new_col)

            # BACKTRACKING
            if (
                len(player_path) > 1
                and new_position == player_path[-2]
            ):

                player_path.pop()

            else:

                player_path.append(
                    new_position
                )

            # UPDATE PLAYER
            player_pos[0] = new_row
            player_pos[1] = new_col

# CHECK GOAL


def reached_goal():

    return tuple(player_pos) == maze.goal

# =========================
# ANIMATE SEARCH
# =========================


def animate_search(
    explored_order,
    path,
    algorithm="Unknown"
):

    reset_screen()

    explored_nodes = []
    step_mode = True # manual step-by-step exploration

    # =========================
    # EXPLORE STEP-BY-STEP
    # =========================

    for node in explored_order:

        pygame.event.pump()

        explored_nodes.append(node)

        screen.fill(WHITE)

        draw_grid()

        draw_player_path()

        # DRAW EXPLORED NODES
        for explored in explored_nodes:

            row, col = explored

            rect = pygame.Rect(
                col * CELL_SIZE,
                row * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE
            )

            pygame.draw.rect(
                screen,
                YELLOW,
                rect
            )

            pygame.draw.rect(
                screen,
                GRAY,
                rect,
                1
            )

            coord_text = small_font.render(
                f"({row},{col})",
                True,
                BLACK
            )

            screen.blit(
                coord_text,
                (
                    col * CELL_SIZE + 3,
                    row * CELL_SIZE + 20
                )
            )

        draw_start_goal()

        draw_player()

        draw_text()

        # =========================
        # AI LOGIC PANEL
        # =========================

        row, col = node

        # A*
        if algorithm == "A*":

            row_goal, col_goal = maze.goal

            # Manhattan Distance
            h = abs(row_goal - row) + abs(col_goal - col)

            # Cost from start
            g = explored_nodes.index(node)

            # Total cost
            f = g + h

            draw_ai_panel(
                algorithm="A*",
                current=(row, col),
                g_cost=g,
                h_cost=h,
                f_cost=f,
                message="Lowest heuristic selected"
            )

        # DFS/BFS
        else:

            draw_ai_panel(
                algorithm=algorithm,
                current=(row, col),
                message="Exploring next node"
            )

        pygame.display.update()

        # time.sleep(0.05)
        # =========================
# STEP MODE
# =========================

        if step_mode:
        
            waiting = True
        
            while waiting:
        
                for event in pygame.event.get():
        
                    # CLOSE WINDOW
                    if event.type == pygame.QUIT:
        
                        pygame.quit()
                        return
        
                    # PRESS SPACE FOR NEXT STEP
                    if event.type == pygame.KEYDOWN:
        
                        if event.key == pygame.K_SPACE:
        
                            waiting = False

    # =========================
    # FINAL PATH ANIMATION
    # =========================

    if path:

        final_nodes = []

        for node in path:

            pygame.event.pump()

            final_nodes.append(node)

            screen.fill(WHITE)

            draw_grid()

            draw_player_path()

            # KEEP EXPLORED NODES
            for explored in explored_nodes:

                row, col = explored

                rect = pygame.Rect(
                    col * CELL_SIZE,
                    row * CELL_SIZE,
                    CELL_SIZE,
                    CELL_SIZE
                )

                pygame.draw.rect(
                    screen,
                    YELLOW,
                    rect
                )

            # DRAW FINAL PATH
            for final in final_nodes:

                row, col = final

                rect = pygame.Rect(
                    col * CELL_SIZE,
                    row * CELL_SIZE,
                    CELL_SIZE,
                    CELL_SIZE
                )

                pygame.draw.rect(
                    screen,
                    BLUE,
                    rect
                )

                coord_text = small_font.render(
                    f"({row},{col})",
                    True,
                    WHITE
                )

                screen.blit(
                    coord_text,
                    (
                        col * CELL_SIZE + 3,
                        row * CELL_SIZE + 20
                    )
                )

            draw_start_goal()

            draw_player()

            draw_text()

            # =========================
            # AI PANEL DURING FINAL PATH
            # =========================

            row, col = node

            if algorithm == "A*":

                row_goal, col_goal = maze.goal

                h = abs(row_goal - row) + abs(col_goal - col)

                g = final_nodes.index(node)

                f = g + h

                draw_ai_panel(
                    algorithm="A*",
                    current=(row, col),
                    g_cost=g,
                    h_cost=h,
                    f_cost=f,
                    message="Optimal path selected"
                )

            else:

                draw_ai_panel(
                    algorithm=algorithm,
                    current=(row, col),
                    message="Final path visualization"
                )

            pygame.display.update()
            

            # time.sleep(0.08)
            # =========================
# STEP MODE
# =========================

            if step_mode:
            
                waiting = True
            
                while waiting:
            
                    for event in pygame.event.get():
            
                        # CLOSE WINDOW
                        if event.type == pygame.QUIT:
            
                            pygame.quit()
                            return
            
                        # PRESS SPACE FOR NEXT STEP
                        if event.type == pygame.KEYDOWN:
            
                            if event.key == pygame.K_SPACE:
            
                                waiting = False