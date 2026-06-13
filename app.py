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
#  HEADER
# ════════════════════════════════════════════════════════════════
st.title("🧩 AI Maze Solver & Pathfinding Visualizer")

st.markdown("""
<div style="background:linear-gradient(135deg,#1a1a2e,#0f3460);
            border-radius:10px;padding:14px 18px;margin-bottom:5px;
            border-left:5px solid #1a56a0;">
  <p style="font-size:15px;color:#e0e0e0;margin:0 0 8px 0;font-weight:600;">
    🎓 Hands-on AI learning &mdash;
    <span style="color:#4fc3f7;">Sir Syed CASE Institute of Technology</span>
  </p>
  <p style="font-size:13px;color:#bbb;margin:0 0 10px 0;line-height:1.7;">
    Solve the maze yourself first, then watch
    <b style="color:#ffd700;">DFS</b>,
    <b style="color:#4fc3f7;">BFS</b> and
    <b style="color:#69f0ae;">A*</b>
    tackle it <b>step by step</b> — every node explored, every cost calculated, fully visible.
  </p>
  <div style="display:flex;gap:10px;flex-wrap:wrap;">
    <span style="background:#ffffff18;border-radius:5px;padding:3px 10px;font-size:12px;color:#ddd;">🕹️ Play Mode</span>
    <span style="background:#ffffff18;border-radius:5px;padding:3px 10px;font-size:12px;color:#ddd;">🔍 Step-by-Step</span>
    <span style="background:#ffffff18;border-radius:5px;padding:3px 10px;font-size:12px;color:#ddd;">📊 Compare</span>
    <span style="background:#ffffff18;border-radius:5px;padding:3px 10px;font-size:12px;color:#ddd;">⭐ A* Costs</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Algorithm run buttons ────────────────────────────────────────
b1, b2, b3, b4 = st.columns(4)
with b1:
    if st.button("🎲 New Maze", use_container_width=True):
        maze.maze = maze.generate_maze()
        for k, v in defaults.items():
            st.session_state[k] = v
        st.session_state.player_pos  = list(maze.start)
        st.session_state.player_path = [maze.start]
        st.rerun()
with b2:
    if st.button("▶ Run DFS", use_container_width=True):
        run_algo("DFS"); st.rerun()
with b3:
    if st.button("▶ Run BFS", use_container_width=True):
        run_algo("BFS"); st.rerun()
with b4:
    if st.button("▶ Run A*", use_container_width=True):
        run_algo("A*"); st.rerun()

st.divider()

# ════════════════════════════════════════════════════════════════
#  THREE-COLUMN LAYOUT  left panel | center maze+controls | right panel
# ════════════════════════════════════════════════════════════════
col_left, col_center, col_right = st.columns([1, 3, 1])

# ── LEFT: Student stats only ─────────────────────────────────────
with col_left:
    st.subheader("👨‍🎓 Student")
    st.markdown(f"**Pos:** `{player_pos_t}`")
    st.markdown(f"**Moves:** `{len(st.session_state.player_path) - 1}`")
    if player_pos_t == maze.goal:
        st.success("🎉 Goal!")
    st.markdown("---")
    st.markdown("**Path log**")
    st.dataframe(
        pd.DataFrame([{"#": i, "Pos": str(n)}
                      for i, n in enumerate(st.session_state.player_path)]),
        use_container_width=True, height=340
    )

# ── CENTER: D-pad → Maze → Step controls → Legend ────────────────
with col_center:

    st.markdown("""
    <style>
      /* ── maze container — everything inherits this width ── */
      .maze-container {
        max-width: 100%;
        margin: 0 auto;
      }
      /* ── maze table wrapper — keeps the grid compact & centered ── */
      .maze-table-wrap {
        max-width: 520px;
        margin: 0 auto;
      }
      /* ── maze table ── */
      .maze-table {
        width: 100%;
        border-collapse: collapse;
        table-layout: fixed;
      }
      .maze-table td {
        width: 10%;
        aspect-ratio: 1 / 1;
        height: auto;
        text-align: center;
        vertical-align: middle;
        border: 1px solid #aaa;
        font-size: 11px;
        font-family: monospace;
        padding: 0;
        overflow: hidden;
      }
      .cell-wall     { background: #111; }
      .cell-empty    { background: #fff; }
      .cell-start    { background: #00cc44; }
      .cell-goal     { background: #ff3333; }
      .cell-player   { background: #9900cc; }
      .cell-human    { background: #6495ed; }
      .cell-explored { background: #ffd700; }
      .cell-path     { background: #1a56cc; color: #fff; }
      .coord         { font-size: 9px; color: #333; }
      .coord-w       { font-size: 9px; color: #fff; }
      /* ── legend ── */
      .legend-row {
        width: 100%;
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 10px;
        margin-top: 10px;
        font-size: 12px;
      }
      .legend-dot {
        display: inline-block;
        width: 12px; height: 12px;
        border-radius: 2px;
        margin-right: 3px;
        vertical-align: middle;
      }
      /* ── make ALL buttons in center col tall, narrow & centered ── */
      div[data-testid="stButton"] button {
        height: auto;
        min-height: 34px;
        font-size: 15px;
        padding: 6px 8px;
        line-height: 1.3;
        width: 100% !important;
        margin: 0 auto;
        display: block;
        white-space: normal;
        word-wrap: break-word;
      }
      /* remove the extra vertical gap Streamlit adds around button wrappers */
      div[data-testid="stButton"] {
        margin: 0;
        display: flex;
        justify-content: center;
      }
      div[data-testid="column"] {
        padding: 0;
        display: flex;
        justify-content: center;
      }
      /* ── column gap ── */
      div[data-testid="stHorizontalBlock"] {
        gap: 0rem;
      }
      /* ── shorter, centered progress bar ── */
      .stProgress {
        max-width: 320px;
        margin: 0 auto;
      }
      /* ── mobile ── */
      @media (max-width: 768px) {
        .maze-container { max-width: 100%; }
        .maze-table-wrap { max-width: 100%; }
        .maze-table td  { font-size: 8px; }
        .coord, .coord-w { font-size: 7px; }
        .legend-row     { font-size: 10px; gap: 6px; }
        div[data-testid="stButton"] button {
          height: auto;
          min-height: 28px;
          font-size: 12px;
          padding: 4px 6px;
          line-height: 1.2;
          white-space: normal;
          word-wrap: break-word;
        }
        div[data-testid="stHorizontalBlock"] {
          gap: 0rem;
        }
        .stProgress {
          max-width: 240px;
        }
      }
    </style>
    """, unsafe_allow_html=True)

    # Open maze-container div
    st.markdown('<div class="maze-container">', unsafe_allow_html=True)

    # ── D-PAD — large buttons, same style as step controls ───────
    st.markdown("<p style='text-align:center;font-weight:600;margin:0 0 4px 0;'>🕹️ Move Player</p>",
                unsafe_allow_html=True)

    # UP — centered, same width as the 3 bottom buttons combined
    u1, u2, u3 = st.columns([1, 2, 1])
    with u2:
        if st.button("⬆", key="up", use_container_width=True):
            move_player(-1, 0); st.rerun()

    # LEFT / DOWN / RIGHT — centered block matching UP width
    l1, l2, l3 = st.columns([1, 2, 1])
    with l2:
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("⬅", key="lft", use_container_width=True):
                move_player(0, -1); st.rerun()
        with c2:
            if st.button("⬇", key="dn", use_container_width=True):
                move_player(1, 0); st.rerun()
        with c3:
            if st.button("➡", key="rgt", use_container_width=True):
                move_player(0, 1); st.rerun()

    # Close + reopen so maze sits flush (Streamlit inserts a gap after columns)
    st.markdown('</div>', unsafe_allow_html=True)

    # ── MAZE TABLE ───────────────────────────────────────────────
    maze_rows = ""
    for r in range(len(maze.maze)):
        maze_rows += "<tr>"
        for c in range(len(maze.maze[0])):
            cell    = (r, c)
            coord   = f'<span class="coord">({r},{c})</span>'
            coord_w = f'<span class="coord-w">({r},{c})</span>'
            if cell == player_pos_t:
                maze_rows += f'<td class="cell-player">{coord}</td>'
            elif phase == "path" and cell in path_so_far:
                maze_rows += f'<td class="cell-path">{coord_w}</td>'
            elif cell in explored_so_far:
                maze_rows += f'<td class="cell-explored">{coord}</td>'
            elif cell == maze.start:
                maze_rows += f'<td class="cell-start">{coord}</td>'
            elif cell == maze.goal:
                maze_rows += f'<td class="cell-goal">{coord}</td>'
            elif cell in player_path_set:
                maze_rows += f'<td class="cell-human">{coord}</td>'
            elif maze.maze[r][c] == 1:
                maze_rows += '<td class="cell-wall"></td>'
            else:
                maze_rows += f'<td class="cell-empty">{coord}</td>'
        maze_rows += "</tr>"

    st.markdown(
        f'<div class="maze-table-wrap"><table class="maze-table">{maze_rows}</table></div>',
        unsafe_allow_html=True,
    )

    # ── STEP CONTROLS — open container ───────────────────────────
    st.markdown('<div class="maze-container">', unsafe_allow_html=True)

    st.markdown("<p style='text-align:center;font-weight:600;margin:8px 0 2px 0;'>⏩ Step-by-Step Controls</p>",
                unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    if not algo:
        st.info("Run DFS, BFS, or A* to enable step controls.")
    else:
        prog  = (step + 1) if phase == "explore" else (path_step + 1)
        total = total_ex   if phase == "explore" else total_p
        label = "🔍 Exploration" if phase == "explore" else "🔵 Path Tracing"
        st.markdown(
            f"<p style='text-align:center;margin:0;font-size:13px;'>"
            f"{label} &nbsp;—&nbsp; Step <b>{prog}</b> / <b>{total}</b></p>",
            unsafe_allow_html=True,
        )
        st.progress(prog / total if total else 0)

        # Row 1: First | Prev | Next | Last  — 4 equal cols
        s1, s2, s3, s4 = st.columns([1, 1, 1, 1], gap="small")
        with s1:
            if st.button("⏮ First", key="first", use_container_width=True):
                st.session_state["step" if phase == "explore" else "path_step"] = 0
                st.rerun()
        with s2:
            if st.button("◀ Prev", key="prev", use_container_width=True):
                if phase == "path" and path_step > 0:
                    st.session_state.path_step -= 1
                elif phase == "path" and path_step == 0:
                    st.session_state.phase = "explore"
                    st.session_state.step  = total_ex - 1
                elif phase == "explore" and step > 0:
                    st.session_state.step -= 1
                st.rerun()
        with s3:
            if st.button("Next ▶", key="nxt", use_container_width=True):
                if phase == "explore":
                    if step < total_ex - 1:
                        st.session_state.step += 1
                    else:
                        st.session_state.phase     = "path"
                        st.session_state.path_step = 0
                elif path_step < total_p - 1:
                    st.session_state.path_step += 1
                st.rerun()
        with s4:
            if st.button("Last ⏭", key="last", use_container_width=True):
                if phase == "explore":
                    st.session_state.step = total_ex - 1
                else:
                    st.session_state.path_step = total_p - 1
                st.rerun()

        # Row 2: Skip | Back — 2 equal cols
        sk1, sk2 = st.columns([1, 1], gap="small")
        with sk1:
            if st.button("⏩ Skip → Path Phase", key="skip", use_container_width=True):
                st.session_state.step      = total_ex - 1
                st.session_state.phase     = "path"
                st.session_state.path_step = 0
                st.rerun()
        with sk2:
            if st.button("↩ Back → Explore Phase", key="back", use_container_width=True):
                st.session_state.phase     = "explore"
                st.session_state.path_step = 0
                st.rerun()

    # ── LEGEND — below all controls ──────────────────────────────
    st.markdown("""
    <div class="maze-container">
      <div class="legend-row">
        <span><span class="legend-dot" style="background:#00cc44"></span>Start</span>
        <span><span class="legend-dot" style="background:#ff3333"></span>Goal</span>
        <span><span class="legend-dot" style="background:#9900cc"></span>You</span>
        <span><span class="legend-dot" style="background:#6495ed"></span>Your path</span>
        <span><span class="legend-dot" style="background:#ffd700"></span>Explored</span>
        <span><span class="legend-dot" style="background:#1a56cc"></span>AI path</span>
        <span><span class="legend-dot" style="background:#111;border:1px solid #555"></span>Wall</span>
        <span><span class="legend-dot" style="background:#ccc"></span>Open</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # ── ALGORITHM EXPLAINER below step controls ──────────────────
    algo_info = {
        "DFS": {
            "icon": "🌲", "color": "#e67e22",
            "title": "Depth-First Search (DFS)",
            "tagline": "Goes as deep as possible before backtracking.",
            "how": """DFS uses a **stack (LIFO)** to explore the maze. It always picks the most recently
added node and dives as far down one path as possible. When it hits a dead end,
it backtracks to the last junction and tries a different direction.

Think of it like exploring a cave — keep walking forward until blocked,
then retrace your steps and try another tunnel.""",
            "steps": [
                "Push the start node onto the stack.",
                "Pop the top node and mark it as visited 🟨.",
                "Push all unvisited neighbors onto the stack.",
                "Repeat until the goal is found or the stack is empty.",
                "Trace parent pointers back to get the final path 🔵.",
            ],
            "pros": ["Very low memory usage", "Fast at finding *a* path in deep mazes"],
            "cons": ["Does NOT guarantee the shortest path", "Can waste time in long dead ends"],
            "complexity": "Time: O(V+E)  |  Space: O(V)  |  Optimal: No  |  Complete: Yes",
        },
        "BFS": {
            "icon": "🌊", "color": "#2980b9",
            "title": "Breadth-First Search (BFS)",
            "tagline": "Level by level — guarantees the shortest path.",
            "how": """BFS uses a **queue (FIFO)** to explore the maze ring by ring. It visits every
node at distance 1 from the start, then distance 2, and so on. This wave expansion
guarantees the first time it reaches the goal, it took the fewest steps.

Think of dropping a stone in water — ripples spread outward equally in all directions.""",
            "steps": [
                "Enqueue the start node.",
                "Dequeue the front node and mark it as visited 🟨.",
                "Enqueue all unvisited neighbors.",
                "Repeat — each round expands one level further from the start.",
                "When the goal is dequeued, trace parent pointers for the shortest path 🔵.",
            ],
            "pros": ["Guarantees the shortest path (unweighted maze)", "Systematic and predictable"],
            "cons": ["Higher memory usage than DFS", "Slower when the goal is far in open space"],
            "complexity": "Time: O(V+E)  |  Space: O(V)  |  Optimal: Yes  |  Complete: Yes",
        },
        "A*": {
            "icon": "⭐", "color": "#27ae60",
            "title": "A* Search Algorithm",
            "tagline": "Shortest path + smart heuristic — the best of both worlds.",
            "how": """A* uses a **priority queue** ordered by **f(n) = g(n) + h(n)**. Instead of
exploring blindly, it estimates total cost through each node and always expands
the most promising one first.

- **g(n)** — exact cost paid to reach this node from the start
- **h(n)** — Manhattan Distance estimate to the goal
- **f(n)** — total estimated cost of going through this node

Like a GPS: it knows how far you've travelled *and* estimates how far you still
need to go — avoiding obviously bad detours.""",
            "steps": [
                "Add start node to the priority queue with f = h(start).",
                "Pop the node with the lowest f(n) value 🟨.",
                "For each neighbor, compute g, h, and f values.",
                "If the neighbor is new or has a better f, update and re-enqueue it.",
                "When the goal is popped, trace parent pointers for the optimal path 🔵.",
            ],
            "pros": ["Finds the shortest path efficiently",
                     "Far fewer nodes explored than BFS",
                     "Live cost values visible in the AI Panel"],
            "cons": ["More complex to implement",
                     "Performance depends on the heuristic quality"],
            "complexity": "Time: O(E log V)  |  Space: O(V)  |  Optimal: Yes (admissible h)  |  Complete: Yes",
        },
    }

    active = algo if algo in algo_info else None

    if active:
        info = algo_info[active]
        st.markdown(
            f"""<div style="border-left:5px solid {info['color']};background:#1e1e2e;
                border-radius:8px;padding:14px 18px;margin-bottom:12px;">
              <h3 style="margin:0 0 4px 0;color:{info['color']};">
                {info['icon']} {info['title']}</h3>
              <p style="margin:0;color:#aaa;font-size:13px;font-style:italic;">
                {info['tagline']}</p>
            </div>""",
            unsafe_allow_html=True,
        )
        th, ts, tt = st.tabs(["📖 How it Works", "🔢 Step-by-Step Logic", "⚖️ Trade-offs"])
        with th:
            st.markdown(info["how"])
            st.code(info["complexity"], language=None)
        with ts:
            for i, s in enumerate(info["steps"], 1):
                st.markdown(f"**{i}.** {s}")
        with tt:
            cp, cc2 = st.columns(2)
            with cp:
                st.markdown("**✅ Advantages**")
                for x in info["pros"]: st.markdown(f"- {x}")
            with cc2:
                st.markdown("**❌ Disadvantages**")
                for x in info["cons"]: st.markdown(f"- {x}")
    else:
        st.markdown("#### 📚 How Do These Algorithms Work?")
        st.caption("Run any algorithm above — this section updates to show its full explanation.")
        ca, cb, cc2 = st.columns(3)
        cards = [
            (ca, "DFS", "🌲", "#e67e22", "Stack (LIFO)",   "Dives deep, backtracks on dead ends.",  "✗ Not shortest","✓ Low memory"),
            (cb, "BFS", "🌊", "#2980b9", "Queue (FIFO)",   "Expands level by level like a ripple.", "✓ Shortest",    "✗ High memory"),
            (cc2,"A*",  "⭐", "#27ae60", "Priority Queue", "f(n)=g(n)+h(n) guides the search.",     "✓ Shortest+fast","✗ Needs heuristic"),
        ]
        for col, name, icon, color, struct, desc, opt, mem in cards:
            with col:
                st.markdown(
                    f"""<div style="border:2px solid {color};border-radius:10px;
                            padding:12px;text-align:center;">
                      <div style="font-size:26px;">{icon}</div>
                      <div style="font-size:14px;font-weight:bold;color:{color};">{name}</div>
                      <div style="font-size:11px;color:#888;margin:4px 0;">{struct}</div>
                      <div style="font-size:11px;color:#ccc;margin:6px 0;">{desc}</div>
                      <div style="font-size:11px;">
                        <span style="color:#2ecc71;">{opt}</span><br>
                        <span style="color:#e74c3c;">{mem}</span>
                      </div>
                    </div>""",
                    unsafe_allow_html=True,
                )

# ── RIGHT: AI Logic Panel ─────────────────────────────────────────
with col_right:
    st.subheader("🤖 AI Panel")

    with st.container(border=True):
        if not algo:
            st.info("Run an algorithm to see live reasoning here.")
        else:
            g_val = h_val = f_val = "-"
            message = ""
            if phase == "explore" and current_node:
                if algo == "A*":
                    g_val, h_val, f_val = astar_costs(current_node, step)
                message = "Lowest f(n) selected" if algo == "A*" else "Exploring next node"
            elif phase == "path" and current_node:
                if algo == "A*":
                    g_val, h_val, f_val = astar_costs(current_node, path_step)
                message = "Optimal path traced" if algo == "A*" else "Final path visualization"

            st.markdown(f"**Algorithm:** `{algo}`")
            st.markdown(f"**Phase:** {'🔍 Exploration' if phase == 'explore' else '🔵 Path Tracing'}")
            st.markdown(f"**Node:** `{current_node}`")
            if phase == "explore":
                st.markdown(f"**Step:** {step + 1} / {total_ex}")
            else:
                st.markdown(f"**Path step:** {path_step + 1} / {total_p}")

            st.divider()

            if algo == "A*":
                st.markdown("**Cost Breakdown**")
                m1, m2, m3 = st.columns(3)
                m1.metric("g(n)", g_val)
                m2.metric("h(n)", h_val)
                m3.metric("f(n)", f_val)
                st.caption("g = cost from start\nh = Manhattan to goal\nf = g + h")
            else:
                st.info(message)

            st.divider()

            st.markdown("**📊 Comparison**")
            human_moves = len(st.session_state.player_path)
            ai_len      = len(path) if path else None
            diff        = (human_moves - ai_len) if ai_len else None
            mc1, mc2    = st.columns(2)
            mc1.metric("👤 You", human_moves)
            mc2.metric("🤖 AI", ai_len or "—")
            if diff is not None:
                if diff > 0:    st.warning(f"+{diff} extra steps vs AI")
                elif diff == 0: st.success("Matched AI! 🎉")
                else:           st.info(f"{abs(diff)} steps shorter than AI")

            st.divider()

            st.markdown("**🔍 Explored Nodes**")
            if explored:
                up_to = step if phase == "explore" else total_ex - 1
                st.dataframe(
                    pd.DataFrame([
                        {"#": i, "Node": str(explored[i]),
                         "": "← now" if i == up_to else ""}
                        for i in range(up_to + 1)
                    ]),
                    use_container_width=True, height=200,
                )

            if phase == "path" and path:
                st.markdown("**🔵 AI Path**")
                st.dataframe(
                    pd.DataFrame([
                        {"#": i, "Node": str(path[i]),
                         "": "← now" if i == path_step else ""}
                        for i in range(path_step + 1)
                    ]),
                    use_container_width=True, height=180,
                )