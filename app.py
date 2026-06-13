import streamlit as st
import pandas as pd
import maze
from dfs import dfs
from bfs import bfs
from astar import astar

st.set_page_config(layout="wide", page_title="AI Maze Solver", page_icon="🧩")

# ── Session State ────────────────────────────────────────────────
defaults = {
    "step": 0, "explored": [], "path": [], "algorithm": "",
    "phase": "explore", "path_step": 0,
    "player_pos": list(maze.start), "player_path": [maze.start],
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

def move_player(dr, dc):
    r, c = st.session_state.player_pos
    nr, nc = r + dr, c + dc
    if 0 <= nr < len(maze.maze) and 0 <= nc < len(maze.maze[0]) and maze.maze[nr][nc] == 0:
        node = (nr, nc)
        if len(st.session_state.player_path) > 1 and node == st.session_state.player_path[-2]:
            st.session_state.player_path.pop()
        else:
            st.session_state.player_path.append(node)
        st.session_state.player_pos = [nr, nc]

def run_algo(name):
    p, e = {"DFS": dfs, "BFS": bfs, "A*": astar}[name]()
    st.session_state.update(algorithm=name, explored=e, path=p,
                            step=0, phase="explore", path_step=0)

# ── Derived state ────────────────────────────────────────────────
algo      = st.session_state.algorithm
explored  = st.session_state.explored
path      = st.session_state.path
step      = st.session_state.step
phase     = st.session_state.phase
path_step = st.session_state.path_step
total_ex  = len(explored)
total_p   = len(path)

explored_so_far = set(explored[:step + 1]) if explored else set()
current_node    = explored[step] if explored and step < total_ex else None
if phase == "path" and path:
    explored_so_far = set(explored)
    path_so_far     = set(path[:path_step + 1])
    current_node    = path[path_step]
else:
    path_so_far = set()

def astar_costs(node, idx):
    gr, gc = maze.goal
    r, c = node
    h = abs(gr - r) + abs(gc - c)
    return idx, h, idx + h

player_pos_t    = tuple(st.session_state.player_pos)
player_path_set = set(st.session_state.player_path)

# ════════════════════════════════════════════════════════════════
#  STYLING & CSS
# ════════════════════════════════════════════════════════════════
st.markdown("""
<style>
    /* Maze cells styling */
    .maze-table { width: 100%; border-collapse: collapse; table-layout: fixed; }
    .maze-table td { width: 10%; aspect-ratio: 1 / 1; text-align: center; border: 1px solid #aaa; font-size: 10px; }
    .cell-wall { background: #111; }
    .cell-explored { background: #ffd700; }
    .cell-path { background: #1a56cc; color: #fff; }
    
    /* Compact Dataframe Styles */
    [data-testid="stDataFrame"] { font-size: 10px !important; }
    [data-testid="stDataFrame"] td { padding: 2px 4px !important; }
    
    /* D-pad sizing */
    div[data-testid="stButton"] button { height: 35px; }
</style>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════
#  HEADER & CONTROLS
# ════════════════════════════════════════════════════════════════
st.title("🧩 AI Maze Solver")

b1, b2, b3, b4 = st.columns(4)
with b1:
    if st.button("🎲 New Maze"):
        maze.maze = maze.generate_maze()
        for k, v in defaults.items(): st.session_state[k] = v
        st.rerun()
with b2:
    if st.button("▶ Run DFS"): run_algo("DFS"); st.rerun()
with b3:
    if st.button("▶ Run BFS"): run_algo("BFS"); st.rerun()
with b4:
    if st.button("▶ Run A*"): run_algo("A*"); st.rerun()

st.divider()

col_left, col_center, col_right = st.columns([1, 2.5, 1])

# ── LEFT ──
with col_left:
    st.subheader("👨‍🎓 Student")
    st.dataframe(pd.DataFrame([{"#": i, "Pos": str(n)} for i, n in enumerate(st.session_state.player_path)]), use_container_width=True)

# ── CENTER ──
with col_center:
    # (Simplified D-Pad logic here)
    maze_rows = ""
    for r in range(len(maze.maze)):
        maze_rows += "<tr>"
        for c in range(len(maze.maze[0])):
            cell = (r, c)
            css = "cell-wall" if maze.maze[r][c] == 1 else ("cell-path" if phase=="path" and cell in path_so_far else ("cell-explored" if cell in explored_so_far else "cell-empty"))
            maze_rows += f'<td class="{css}"></td>'
        maze_rows += "</tr>"
    st.markdown(f'<table class="maze-table">{maze_rows}</table>', unsafe_allow_html=True)

# ── RIGHT ──
with col_right:
    st.subheader("🤖 AI Panel")
    if not algo:
        st.info("Run an algorithm to see live logic.")
    else:
        st.write(f"**Algorithm:** {algo}")
        st.markdown("**🔍 Explored Nodes**")
        df_exp = pd.DataFrame([{"#": i, "Node": str(explored[i]), "Status": "◀" if i == step else ""} for i in range(min(step + 1, total_ex))])
        st.dataframe(df_exp, use_container_width=True)

        if phase == "path" and path:
            st.markdown("**🔵 AI Path**")
            df_path = pd.DataFrame([{"#": i, "Node": str(path[i]), "Status": "◀" if i == path_step else ""} for i in range(min(path_step + 1, total_p))])
            st.dataframe(df_path, use_container_width=True)