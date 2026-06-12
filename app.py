import streamlit as st
import pandas as pd
import maze
from dfs import dfs
from bfs import bfs
from astar import astar

st.set_page_config(layout="wide", page_title="AI Maze Solver", page_icon="🧩")

# ── Session State Init ──────────────────────────────
defaults = {
    "step": 0,
    "explored": [],
    "path": [],
    "algorithm": "",
    "phase": "explore",        # "explore" | "path"
    "path_step": 0,
    "player_pos": list(maze.start),
    "player_path": [maze.start],
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── Player Movement ─────────────────────────────────────────────
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

# ── Run Algorithm ───────────────────────────────────────────────
def run_algo(name):
    p, e = {"DFS": dfs, "BFS": bfs, "A*": astar}[name]()
    st.session_state.update(
        algorithm=name, explored=e, path=p,
        step=0, phase="explore", path_step=0
    )

# ── Derived State ────────────────────────────────────────────────
algo        = st.session_state.algorithm
explored    = st.session_state.explored
path        = st.session_state.path
step        = st.session_state.step          # index into explored
phase       = st.session_state.phase
path_step   = st.session_state.path_step    # index into path

total_explore_steps = len(explored)
total_path_steps    = len(path)

# What's visible right now
explored_so_far = set(explored[:step + 1]) if explored else set()
current_node    = explored[step] if explored and step < len(explored) else None

# During path phase, show explored fully + path up to path_step
if phase == "path" and path:
    explored_so_far = set(explored)          # all explored stays yellow
    path_so_far     = set(path[:path_step + 1])
    current_node    = path[path_step]
else:
    path_so_far = set()

# ── A* cost helper ──────────────────────────────────────────────
def astar_costs(node, index):
    gr, gc = maze.goal
    r, c = node
    h = abs(gr - r) + abs(gc - c)
    g = index
    return g, h, g + h

# ════════════════════════════════════════════════════════════════
# HEADER
# ════════════════════════════════════════════════════════════════

st.title("🧩 AI Maze Solver & Pathfinding Visualizer")

st.markdown("""
### 🚀 Learn AI Search Algorithms Step-by-Step

Explore how **Depth First Search (DFS)**, **Breadth First Search (BFS)**, and **A* Search**
solve maze problems in real time.

🎮 **Student Mode:** Navigate the maze yourself using movement controls.

🤖 **AI Mode:** Watch the algorithm explore nodes one step at a time and discover the path to the goal.

📊 **Compare Results:** Analyze your solution against AI by comparing:
- Path Length
- Nodes Explored
- Search Strategy
- Efficiency

📚 Perfect for learning:
**Artificial Intelligence, Search Algorithms, Pathfinding, Graph Traversal, Data Structures, and Heuristic Search.**
""")

c1, c2, c3, c4 = st.columns(4)

with c1:
    if st.button("🎲 Generate New Maze", use_container_width=True):
        maze.maze = maze.generate_maze()
        for k, v in defaults.items():
            st.session_state[k] = v
        st.session_state.player_pos = list(maze.start)
        st.session_state.player_path = [maze.start]
        st.rerun()

with c2:
    if st.button("▶ Run DFS", use_container_width=True):
        run_algo("DFS")
        st.rerun()

with c3:
    if st.button("▶ Run BFS", use_container_width=True):
        run_algo("BFS")
        st.rerun()

with c4:
    if st.button("▶ Run A*", use_container_width=True):
        run_algo("A*")
        st.rerun()

st.divider()

#  MAIN LAYOUT  —  left controls | maze | right controls + panel

col_left, col_maze, col_right = st.columns([1, 3, 1])

player_pos_t    = tuple(st.session_state.player_pos)
player_path_set = set(st.session_state.player_path)

# ── LEFT COLUMN: Player Controls + Student Progress ─────────────
with col_left:
    st.subheader("🎮 Player")

    # D-pad layout
    _, mu, _ = st.columns([1, 2, 1])
    with mu:
        if st.button("⬆", key="up", use_container_width=True):
            move_player(-1, 0); st.rerun()

    ml, md, mr = st.columns(3)
    with ml:
        if st.button("⬅", key="lft", use_container_width=True):
            move_player(0, -1); st.rerun()
    with md:
        if st.button("⬇", key="dn", use_container_width=True):
            move_player(1, 0); st.rerun()
    with mr:
        if st.button("➡", key="rgt", use_container_width=True):
            move_player(0, 1); st.rerun()

    st.markdown("---")

    # Student stats
    st.markdown(f"**Pos:** `{player_pos_t}`")
    st.markdown(f"**Moves:** `{len(st.session_state.player_path) - 1}`")
    if player_pos_t == maze.goal:
        st.success("🎉 Goal!")

    st.markdown("---")
    st.subheader("👨‍🎓 Path")
    st.dataframe(
        pd.DataFrame([{"#": i, "Pos": str(n)} for i, n in enumerate(st.session_state.player_path)]),
        use_container_width=True, height=300
    )

# ── CENTER COLUMN: Maze Grid ─────────────────────────────────────
with col_maze:

    # Build HTML table — matches pygame visual exactly
    table_html = """
    <style>
      .maze-table { border-collapse: collapse; margin: 0 auto; }
      .maze-table td {
        width: 42px; height: 42px;
        text-align: center; vertical-align: middle;
        font-size: 11px; font-family: monospace;
        border: 1px solid #aaa;
        padding: 0;
      }
      .cell-wall    { background: #111; }
      .cell-empty   { background: #fff; }
      .cell-start   { background: #00cc44; }
      .cell-goal    { background: #ff3333; }
      .cell-player  { background: #9900cc; }
      .cell-human   { background: #6495ed; }
      .cell-explored{ background: #ffd700; }
      .cell-path    { background: #1a56cc; color: #fff; }
      .coord  { font-size: 10px; color: #333; }
      .coord-w{ font-size: 10px; color: #fff; }
    </style>
    <table class="maze-table">
    """

    for r in range(len(maze.maze)):
        table_html += "<tr>"
        for c in range(len(maze.maze[0])):
            cell   = (r, c)
            coord  = f'<span class="coord">({r},{c})</span>'
            coord_w= f'<span class="coord-w">({r},{c})</span>'

            if cell == player_pos_t:
                table_html += f'<td class="cell-player">{coord}</td>'
            elif phase == "path" and cell in path_so_far:
                table_html += f'<td class="cell-path">{coord_w}</td>'
            elif cell in explored_so_far:
                table_html += f'<td class="cell-explored">{coord}</td>'
            elif cell == maze.start:
                table_html += f'<td class="cell-start">{coord}</td>'
            elif cell == maze.goal:
                table_html += f'<td class="cell-goal">{coord}</td>'
            elif cell in player_path_set:
                table_html += f'<td class="cell-human">{coord}</td>'
            elif maze.maze[r][c] == 1:
                table_html += '<td class="cell-wall"></td>'
            else:
                table_html += f'<td class="cell-empty">{coord}</td>'
        table_html += "</tr>"
    table_html += "</table>"

    st.markdown(table_html, unsafe_allow_html=True)

    st.markdown("---")

    # Color legend centered below maze
    st.markdown(
        """
        <div style="display:flex;gap:12px;flex-wrap:wrap;font-size:12px;justify-content:center;">
          <span>🟩 Start</span><span>🟥 Goal</span>
          <span style="color:#9900cc;">🟪 Player</span>
          <span style="color:#6495ed;">🟦 Human</span>
          <span style="color:#ffd700;">🟨 Explored</span>
          <span style="color:#1a56cc;">🟦 AI Path</span>
          <span>⬛ Wall</span><span>⬜ Open</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")

    # ── Algorithm Explainer ──────────────────────────────────────
    algo_info = {
        "DFS": {
            "icon": "🌲",
            "title": "Depth-First Search (DFS)",
            "color": "#e67e22",
            "tagline": "Goes as deep as possible before backtracking.",
            "how": """
DFS uses a **stack (LIFO)** to explore the maze. It always picks the most recently added node and dives as far down one path as it can. When it hits a dead end, it backtracks to the last junction and tries a different direction.

Think of it like exploring a cave — you keep walking forward until you are blocked, then retrace your steps and try another tunnel.
""",
            "steps": [
                "Push the start node onto the stack.",
                "Pop the top node and mark it as visited (🟨).",
                "Push all unvisited neighbors onto the stack.",
                "Repeat until the goal is found or stack is empty.",
                "Trace back the parent pointers to get the final path (🔵).",
            ],
            "pros": ["Very low memory usage", "Fast at finding *a* path in deep mazes"],
            "cons": ["Does NOT guarantee the shortest path", "Can waste time in long dead ends"],
            "complexity": "Time: O(V+E)  |  Space: O(V)  |  Optimal: No  |  Complete: Yes",
        },
        "BFS": {
            "icon": "🌊",
            "title": "Breadth-First Search (BFS)",
            "color": "#2980b9",
            "tagline": "Explores level by level — guarantees the shortest path.",
            "how": """
BFS uses a **queue (FIFO)** to explore the maze ring by ring. It visits every node at distance 1 from the start, then every node at distance 2, and so on. This wave expansion ensures the first time it reaches the goal, it has taken the fewest possible steps.

Think of it like dropping a stone in water — the ripples spread outward equally in all directions.
""",
            "steps": [
                "Enqueue the start node.",
                "Dequeue the front node and mark it as visited (🟨).",
                "Enqueue all unvisited neighbors.",
                "Repeat — each round expands one level further from the start.",
                "When the goal is dequeued, trace parent pointers for the shortest path (🔵).",
            ],
            "pros": ["Guarantees the shortest path in unweighted mazes", "Systematic and predictable"],
            "cons": ["Higher memory usage than DFS", "Slower when the goal is far away in open space"],
            "complexity": "Time: O(V+E)  |  Space: O(V)  |  Optimal: Yes  |  Complete: Yes",
        },
        "A*": {
            "icon": "⭐",
            "title": "A* Search Algorithm",
            "color": "#27ae60",
            "tagline": "Shortest path + smart heuristic — the best of both worlds.",
            "how": """
A* uses a **priority queue** ordered by **f(n) = g(n) + h(n)**. Instead of exploring blindly, it estimates the total cost through each node and always expands the most promising one first.

- **g(n)** — exact cost paid to reach this node from the start
- **h(n)** — Manhattan Distance estimate to the goal
- **f(n)** — total estimated cost of going through this node

Think of it like a GPS — it knows how far you have travelled *and* estimates how far you still need to go, so it avoids obviously bad detours.
""",
            "steps": [
                "Add start node to the priority queue with f = h(start).",
                "Pop the node with the lowest f(n) value (🟨).",
                "For each neighbor, compute g, h, and f values.",
                "If the neighbor is new or has a better f, update and re-enqueue it.",
                "When the goal is popped, trace parent pointers for the optimal path (🔵).",
            ],
            "pros": ["Finds the shortest path efficiently", "Far fewer nodes explored than BFS", "Transparent cost calculations visible in the AI Panel"],
            "cons": ["More complex to implement", "Performance depends on the quality of the heuristic"],
            "complexity": "Time: O(E log V)  |  Space: O(V)  |  Optimal: Yes (admissible h)  |  Complete: Yes",
        },
    }

    active = algo if algo in algo_info else None

    if active:
        info = algo_info[active]
        st.markdown(
            f"""<div style="border-left:5px solid {info['color']};background:#1e1e2e;
                border-radius:8px;padding:16px 20px;margin-bottom:12px;">
              <h3 style="margin:0 0 4px 0;color:{info['color']};">{info['icon']} {info['title']}</h3>
              <p style="margin:0;color:#aaa;font-size:14px;font-style:italic;">{info['tagline']}</p>
            </div>""",
            unsafe_allow_html=True,
        )
        tab_how, tab_steps, tab_tradeoff = st.tabs(["📖 How it Works", "🔢 Step-by-Step Logic", "⚖️ Trade-offs"])
        with tab_how:
            st.markdown(info["how"])
            st.code(info["complexity"], language=None)
        with tab_steps:
            for i, s in enumerate(info["steps"], 1):
                st.markdown(f"**{i}.** {s}")
        with tab_tradeoff:
            cp, cc2 = st.columns(2)
            with cp:
                st.markdown("**✅ Advantages**")
                for item in info["pros"]:
                    st.markdown(f"- {item}")
            with cc2:
                st.markdown("**❌ Disadvantages**")
                for item in info["cons"]:
                    st.markdown(f"- {item}")
    else:
        st.markdown("#### 📚 How Do These Algorithms Work?")
        st.caption("Run DFS, BFS, or A* above — this panel will show a full breakdown of the active algorithm. Here is a quick overview of all three:")
        ca, cb, cc2 = st.columns(3)
        cards = [
            (ca, "DFS", "🌲", "#e67e22", "Stack (LIFO)",     "Dives deep, backtracks on dead ends.",    "✗ Not shortest", "✓ Low memory"),
            (cb, "BFS", "🌊", "#2980b9", "Queue (FIFO)",     "Expands level by level like a ripple.",   "✓ Shortest path","✗ High memory"),
            (cc2,"A*",  "⭐", "#27ae60", "Priority Queue",   "Uses f(n)=g(n)+h(n) to guide the search.","✓ Shortest+fast","✗ Needs heuristic"),
        ]
        for col, name, icon, color, struct, desc, opt, mem in cards:
            with col:
                st.markdown(
                    f"""<div style="border:2px solid {color};border-radius:10px;
                            padding:14px;text-align:center;">
                      <div style="font-size:30px;">{icon}</div>
                      <div style="font-size:15px;font-weight:bold;color:{color};">{name}</div>
                      <div style="font-size:11px;color:#888;margin:4px 0;">Data structure:<br><b>{struct}</b></div>
                      <div style="font-size:12px;color:#ccc;margin:8px 0;">{desc}</div>
                      <div style="font-size:11px;margin-top:6px;">
                        <span style="color:#2ecc71;">{opt}</span><br>
                        <span style="color:#e74c3c;">{mem}</span>
                      </div>
                    </div>""",
                    unsafe_allow_html=True,
                )

# ── RIGHT COLUMN: Step Controls + AI Logic Panel ─────────────────
with col_right:

    # ── Step Controls ──────────────────────────────────────────
    st.subheader("⏩ Steps")

    if not algo:
        st.info("Run an algorithm first.")
    else:
        phase_label = "🔍 Explore" if phase == "explore" else "🔵 Path"
        prog  = (step + 1)      if phase == "explore" else (path_step + 1)
        total = total_explore_steps if phase == "explore" else total_path_steps

        st.markdown(f"**{phase_label}**")
        st.markdown(f"Step **{prog}** / **{total}**")
        st.progress(prog / total if total else 0)

        if st.button("⏮ First", use_container_width=True):
            st.session_state[("step" if phase == "explore" else "path_step")] = 0
            st.rerun()

        if st.button("◀ Prev", use_container_width=True):
            if phase == "path" and path_step > 0:
                st.session_state.path_step -= 1
            elif phase == "path" and path_step == 0:
                st.session_state.phase = "explore"
                st.session_state.step  = total_explore_steps - 1
            elif phase == "explore" and step > 0:
                st.session_state.step -= 1
            st.rerun()

        if st.button("Next ▶", use_container_width=True):
            if phase == "explore":
                if step < total_explore_steps - 1:
                    st.session_state.step += 1
                else:
                    st.session_state.phase     = "path"
                    st.session_state.path_step = 0
            elif phase == "path" and path_step < total_path_steps - 1:
                st.session_state.path_step += 1
            st.rerun()

        if st.button("Last ⏭", use_container_width=True):
            if phase == "explore":
                st.session_state.step = total_explore_steps - 1
            else:
                st.session_state.path_step = total_path_steps - 1
            st.rerun()

        st.markdown("---")

        if st.button("⏩ Skip→Path", use_container_width=True):
            st.session_state.step      = total_explore_steps - 1
            st.session_state.phase     = "path"
            st.session_state.path_step = 0
            st.rerun()

        if st.button("↩ Back→Explore", use_container_width=True):
            st.session_state.phase     = "explore"
            st.session_state.path_step = 0
            st.rerun()

    st.markdown("---")

    # ── AI Logic Panel ────────────────────────────────────────
    st.subheader("🤖 AI Panel")
    with st.container(border=True):

        if not algo:
            st.info("Run an algorithm to see step-by-step AI reasoning here.")
        else:
            # Current node info
            g_val = h_val = f_val = "-"
            message = ""

            if phase == "explore" and current_node:
                if algo == "A*":
                    g_val, h_val, f_val = astar_costs(current_node, step)
                message = "Lowest heuristic selected" if algo == "A*" else "Exploring next node"
            elif phase == "path" and current_node:
                if algo == "A*":
                    g_val, h_val, f_val = astar_costs(current_node, path_step)
                message = "Optimal path selected" if algo == "A*" else "Final path visualization"

            st.markdown(f"**Algorithm:** `{algo}`")
            st.markdown(f"**Phase:** {'🔍 Exploration' if phase == 'explore' else '🔵 Path Tracing'}")
            st.markdown(f"**Current Node:** `{current_node}`")

            if phase == "explore":
                st.markdown(f"**Explore Step:** {step + 1} / {total_explore_steps}")
                st.markdown(f"**Nodes Explored:** {step + 1}")
            else:
                st.markdown(f"**Path Step:** {path_step + 1} / {total_path_steps}")

            st.divider()

            # Cost display (A* specific)
            if algo == "A*":
                st.markdown("**Cost Breakdown**")
                m1, m2, m3 = st.columns(3)
                m1.metric("g(n)", g_val)
                m2.metric("h(n)", h_val)
                m3.metric("f(n)", f_val)
                st.caption("g(n) = cost from start | h(n) = Manhattan Distance to goal | f(n) = g + h")
            else:
                st.info(f"**Decision:** {message}")

            st.divider()

            # Comparison metrics
            st.subheader("📊 Comparison")
            human_moves = len(st.session_state.player_path)
            ai_path_len = len(path) if path else None
            diff = (human_moves - ai_path_len) if ai_path_len else None

            mc1, mc2 = st.columns(2)
            mc1.metric("👤 Human Moves", human_moves)
            mc2.metric("🤖 AI Path Len", ai_path_len or "-")
            if diff is not None:
                if diff > 0:
                    st.warning(f"You took {diff} extra steps compared to the AI.")
                elif diff == 0:
                    st.success("You matched the AI's path length! 🎉")
                else:
                    st.info(f"You were {abs(diff)} steps shorter (AI not yet optimal here).")

            st.divider()

            # Exploration table (scrollable)
            st.subheader("🔍 Explored Nodes")
            if explored:
                display_up_to = step if phase == "explore" else len(explored) - 1
                st.dataframe(
                    pd.DataFrame([
                        {"#": i, "Node": str(explored[i]),
                         "Status": "← current" if i == display_up_to else "visited"}
                        for i in range(display_up_to + 1)
                    ]),
                    use_container_width=True, height=200
                )

            # Final path table
            if phase == "path" and path:
                st.subheader("🔵 AI Path (so far)")
                st.dataframe(
                    pd.DataFrame([
                        {"#": i, "Node": str(path[i]),
                         "Status": "← current" if i == path_step else "traced"}
                        for i in range(path_step + 1)
                    ]),
                    use_container_width=True, height=180
                )