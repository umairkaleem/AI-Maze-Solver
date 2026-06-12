import streamlit as st
import pandas as pd
import maze
from dfs import dfs
from bfs import bfs
from astar import astar

st.set_page_config(layout="centered", page_title="AI Maze Solver")

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
st.markdown("""
<h1 style="margin-bottom:4px;">🧩 AI Maze Solver</h1>
""", unsafe_allow_html=True)

st.markdown("""
<div style="background:linear-gradient(135deg,#1a1a2e,#0f3460);
            border-radius:10px;padding:14px 18px;margin-bottom:14px;
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

# ── Algorithm buttons ────────────────────────────────────────────
b1, b2, b3, b4 = st.columns(4)
with b1:
    if st.button("🎲 New", use_container_width=True):
        maze.maze = maze.generate_maze()
        for k, v in defaults.items():
            st.session_state[k] = v
        st.session_state.player_pos  = list(maze.start)
        st.session_state.player_path = [maze.start]
        st.rerun()
with b2:
    if st.button("DFS", use_container_width=True):
        run_algo("DFS"); st.rerun()
with b3:
    if st.button("BFS", use_container_width=True):
        run_algo("BFS"); st.rerun()
with b4:
    if st.button("A*", use_container_width=True):
        run_algo("A*"); st.rerun()

st.divider()

# ════════════════════════════════════════════════════════════════
#  MAZE  (centered, full width, compact cell size)
# ════════════════════════════════════════════════════════════════
table_html = """
<style>
  .mz{border-collapse:collapse;margin:0 auto;width:100%;}
  .mz td{
    width:9.5%;height:0;padding-bottom:9.5%;
    position:relative;text-align:center;vertical-align:middle;
    font-size:9px;font-family:monospace;border:1px solid #555;box-sizing:border-box;
  }
  .mz td span{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);}
  .cW{background:#111;} .cE{background:#fff;}
  .cS{background:#00cc44;} .cG{background:#ff3333;}
  .cP{background:#9900cc;} .cH{background:#6495ed;}
  .cX{background:#ffd700;} .cA{background:#1a56cc;}
  .cW span,.cA span{color:#fff!important;}
</style>
<table class="mz">
"""
for r in range(len(maze.maze)):
    table_html += "<tr>"
    for c in range(len(maze.maze[0])):
        cell = (r, c)
        coord = f"<span>{r},{c}</span>"
        if cell == player_pos_t:          cls = "cP"
        elif phase=="path" and cell in path_so_far: cls = "cA"
        elif cell in explored_so_far:     cls = "cX"
        elif cell == maze.start:          cls = "cS"
        elif cell == maze.goal:           cls = "cG"
        elif cell in player_path_set:     cls = "cH"
        elif maze.maze[r][c] == 1:        cls = "cW"; coord = "<span></span>"
        else:                             cls = "cE"
        table_html += f'<td class="{cls}">{coord}</td>'
    table_html += "</tr>"
table_html += "</table>"

st.markdown(table_html, unsafe_allow_html=True)

# Color legend
st.markdown("""
<div style="display:flex;gap:10px;flex-wrap:wrap;font-size:12px;
            justify-content:center;margin:8px 0;">
  <span>🟩 Start</span><span>🟥 Goal</span>
  <span style="color:#9900cc;">🟪 You</span>
  <span style="color:#6495ed;">🟦 Your path</span>
  <span style="color:#ffd700;">🟨 Explored</span>
  <span style="color:#1a56cc;">🟦 AI path</span>
  <span>⬛ Wall</span>
</div>
""", unsafe_allow_html=True)

st.divider()

# ════════════════════════════════════════════════════════════════
#  CONTROLS ROW  —  player D-pad LEFT  |  step buttons RIGHT
# ════════════════════════════════════════════════════════════════
col_dpad, col_steps = st.columns(2)

# ── D-pad ────────────────────────────────────────────────────────
with col_dpad:
    st.markdown("**🕹️ Move Player**")
    _, cu, _ = st.columns([1, 2, 1])
    with cu:
        if st.button("⬆", key="up", use_container_width=True):
            move_player(-1, 0); st.rerun()
    cl2, cd, cr2 = st.columns(3)
    with cl2:
        if st.button("⬅", key="lft", use_container_width=True):
            move_player(0, -1); st.rerun()
    with cd:
        if st.button("⬇", key="dn", use_container_width=True):
            move_player(1, 0); st.rerun()
    with cr2:
        if st.button("➡", key="rgt", use_container_width=True):
            move_player(0, 1); st.rerun()

    st.markdown(f"**Pos:** `{player_pos_t}` &nbsp; **Moves:** `{len(st.session_state.player_path)-1}`")
    if player_pos_t == maze.goal:
        st.success("🎉 Goal reached!")

# ── Step controls ────────────────────────────────────────────────
with col_steps:
    st.markdown("**⏩ AI Steps**")
    if not algo:
        st.info("Run DFS / BFS / A* first.")
    else:
        prog  = (step + 1)  if phase == "explore" else (path_step + 1)
        total = total_ex    if phase == "explore" else total_p
        label = "🔍 Explore" if phase == "explore" else "🔵 Path"
        st.markdown(f"{label} &nbsp; **{prog}/{total}**")
        st.progress(prog / total if total else 0)

        sa, sb = st.columns(2)
        with sa:
            if st.button("⏮", key="first", use_container_width=True):
                st.session_state["step" if phase=="explore" else "path_step"] = 0
                st.rerun()
        with sb:
            if st.button("⏭", key="last", use_container_width=True):
                if phase == "explore": st.session_state.step = total_ex - 1
                else: st.session_state.path_step = total_p - 1
                st.rerun()
        sc, sd = st.columns(2)
        with sc:
            if st.button("◀ Prev", key="prev", use_container_width=True):
                if phase == "path" and path_step > 0:
                    st.session_state.path_step -= 1
                elif phase == "path" and path_step == 0:
                    st.session_state.phase = "explore"
                    st.session_state.step  = total_ex - 1
                elif phase == "explore" and step > 0:
                    st.session_state.step -= 1
                st.rerun()
        with sd:
            if st.button("Next ▶", key="nxt", use_container_width=True):
                if phase == "explore":
                    if step < total_ex - 1: st.session_state.step += 1
                    else:
                        st.session_state.phase     = "path"
                        st.session_state.path_step = 0
                elif path_step < total_p - 1:
                    st.session_state.path_step += 1
                st.rerun()

        se, sf = st.columns(2)
        with se:
            if st.button("⏩ Path", key="skip", use_container_width=True):
                st.session_state.step      = total_ex - 1
                st.session_state.phase     = "path"
                st.session_state.path_step = 0
                st.rerun()
        with sf:
            if st.button("↩ Explore", key="back", use_container_width=True):
                st.session_state.phase     = "explore"
                st.session_state.path_step = 0
                st.rerun()

st.divider()

# ════════════════════════════════════════════════════════════════
#  AI LOGIC PANEL  (full width, tabbed)
# ════════════════════════════════════════════════════════════════
st.markdown("### 🤖 AI Logic Panel")

if not algo:
    st.info("Run an algorithm above to see live reasoning, cost breakdown, and comparison here.")
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

    # Status bar
    st.markdown(f"""
    <div style="background:#1e1e2e;border-radius:8px;padding:10px 16px;margin-bottom:10px;
                display:flex;gap:20px;flex-wrap:wrap;align-items:center;">
      <span style="color:#aaa;font-size:13px;"><b style="color:#fff;">Algorithm:</b>
        <code style="color:#ffd700;">{algo}</code></span>
      <span style="color:#aaa;font-size:13px;"><b style="color:#fff;">Phase:</b>
        {'🔍 Exploration' if phase=='explore' else '🔵 Path Tracing'}</span>
      <span style="color:#aaa;font-size:13px;"><b style="color:#fff;">Node:</b>
        <code style="color:#69f0ae;">{current_node}</code></span>
      <span style="color:#aaa;font-size:13px;"><b style="color:#fff;">Step:</b>
        {(step+1) if phase=='explore' else (path_step+1)} /
        {total_ex if phase=='explore' else total_p}</span>
    </div>
    """, unsafe_allow_html=True)

    tab_cost, tab_compare, tab_nodes = st.tabs(["💰 Cost Breakdown", "📊 Comparison", "🔍 Node Log"])

    with tab_cost:
        if algo == "A*":
            m1, m2, m3 = st.columns(3)
            m1.metric("g(n) — cost from start", g_val)
            m2.metric("h(n) — distance to goal", h_val)
            m3.metric("f(n) = g + h", f_val)
            st.caption("Manhattan Distance: h(n) = |row_goal − row| + |col_goal − col|")
        else:
            st.info(f"**Decision:** {message}")
            st.caption(f"{algo} does not use a cost heuristic — it explores based on structure alone.")

    with tab_compare:
        human_moves = len(st.session_state.player_path)
        ai_len      = len(path) if path else None
        diff        = (human_moves - ai_len) if ai_len else None
        mc1, mc2 = st.columns(2)
        mc1.metric("👤 Your Moves", human_moves)
        mc2.metric("🤖 AI Path", ai_len or "—")
        if diff is not None:
            if diff > 0:   st.warning(f"You took **{diff}** extra steps vs the AI.")
            elif diff == 0: st.success("You matched the AI exactly! 🎉")
            else:           st.info(f"You were {abs(diff)} steps shorter than the AI.")

    with tab_nodes:
        if explored:
            up_to = step if phase == "explore" else total_ex - 1
            st.dataframe(
                pd.DataFrame([{"#": i, "Node": str(explored[i]),
                               "": "← current" if i == up_to else ""}
                              for i in range(up_to + 1)]),
                use_container_width=True, height=220,
            )
        if phase == "path" and path:
            st.markdown("**🔵 AI Path traced so far**")
            st.dataframe(
                pd.DataFrame([{"#": i, "Node": str(path[i]),
                               "": "← current" if i == path_step else ""}
                              for i in range(path_step + 1)]),
                use_container_width=True, height=180,
            )

st.divider()

# ════════════════════════════════════════════════════════════════
#  ALGORITHM EXPLAINER
# ════════════════════════════════════════════════════════════════
st.markdown("### 📚 How These Algorithms Work")

algo_info = {
    "DFS": {
        "icon": "🌲", "color": "#e67e22",
        "title": "Depth-First Search (DFS)",
        "tagline": "Goes as deep as possible before backtracking.",
        "how": """DFS uses a **stack (LIFO)** — it always picks the most recently added node
and dives as far down one path as possible. When it hits a dead end, it backtracks
to the last junction and tries a different direction.

Think of it like exploring a cave: keep walking forward until blocked,
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
        "how": """BFS uses a **queue (FIFO)** — it visits every node at distance 1 from the start,
then distance 2, then 3, and so on. This wave-like expansion guarantees that
the first time it reaches the goal, it took the fewest possible steps.

Think of dropping a stone in water — ripples spread equally in all directions.""",
        "steps": [
            "Enqueue the start node.",
            "Dequeue the front node and mark it as visited 🟨.",
            "Enqueue all unvisited neighbors.",
            "Repeat — each round is one level further from the start.",
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
        "how": """A* uses a **priority queue** ordered by **f(n) = g(n) + h(n)**.
Instead of exploring blindly, it estimates total cost through each node and
always expands the most promising one first.

- **g(n)** — exact cost paid to reach this node from the start
- **h(n)** — Manhattan Distance estimate to the goal
- **f(n)** — total estimated cost through this node

Think of it as a GPS: it knows how far you've travelled *and* estimates
how far you still need to go — avoiding obviously bad detours.""",
        "steps": [
            "Add start node to the priority queue with f = h(start).",
            "Pop the node with the lowest f(n) value 🟨.",
            "For each neighbor, compute g, h, and f.",
            "If the neighbor is new or has a better f, update and re-enqueue it.",
            "When the goal is popped, trace parent pointers for the optimal path 🔵.",
        ],
        "pros": ["Finds the shortest path efficiently", "Explores far fewer nodes than BFS",
                 "Live cost values visible in the AI Panel above"],
        "cons": ["More complex to implement", "Quality depends on the heuristic chosen"],
        "complexity": "Time: O(E log V)  |  Space: O(V)  |  Optimal: Yes (admissible h)  |  Complete: Yes",
    },
}

active = algo if algo in algo_info else None

if active:
    info = algo_info[active]
    st.markdown(f"""
    <div style="border-left:5px solid {info['color']};background:#1e1e2e;
                border-radius:8px;padding:14px 18px;margin-bottom:12px;">
      <h3 style="margin:0 0 4px 0;color:{info['color']};">{info['icon']} {info['title']}</h3>
      <p style="margin:0;color:#aaa;font-size:13px;font-style:italic;">{info['tagline']}</p>
    </div>""", unsafe_allow_html=True)

    th, ts, tt = st.tabs(["📖 How it Works", "🔢 Step-by-Step Logic", "⚖️ Trade-offs"])
    with th:
        st.markdown(info["how"])
        st.code(info["complexity"], language=None)
    with ts:
        for i, s in enumerate(info["steps"], 1):
            st.markdown(f"**{i}.** {s}")
    with tt:
        cp, cc = st.columns(2)
        with cp:
            st.markdown("**✅ Advantages**")
            for x in info["pros"]: st.markdown(f"- {x}")
        with cc:
            st.markdown("**❌ Disadvantages**")
            for x in info["cons"]: st.markdown(f"- {x}")
else:
    # Show all three cards side by side
    st.caption("Run any algorithm above — this section updates to show its full explanation.")
    ca, cb, cc = st.columns(3)
    cards = [
        (ca, "DFS", "🌲", "#e67e22", "Stack (LIFO)",   "Dives deep, backtracks on dead ends.",   "✗ Not shortest", "✓ Low memory"),
        (cb, "BFS", "🌊", "#2980b9", "Queue (FIFO)",   "Expands level by level like a ripple.",  "✓ Shortest",     "✗ High memory"),
        (cc, "A*",  "⭐", "#27ae60", "Priority Queue", "f(n)=g(n)+h(n) guides the search.",      "✓ Shortest+fast","✗ Needs heuristic"),
    ]
    for col, name, icon, color, struct, desc, opt, mem in cards:
        with col:
            st.markdown(f"""
            <div style="border:2px solid {color};border-radius:10px;
                        padding:12px;text-align:center;">
              <div style="font-size:26px;">{icon}</div>
              <div style="font-size:14px;font-weight:bold;color:{color};">{name}</div>
              <div style="font-size:11px;color:#888;margin:4px 0;">{struct}</div>
              <div style="font-size:11px;color:#ccc;margin:6px 0;">{desc}</div>
              <div style="font-size:11px;">
                <span style="color:#2ecc71;">{opt}</span><br>
                <span style="color:#e74c3c;">{mem}</span>
              </div>
            </div>""", unsafe_allow_html=True)

st.divider()

# ── Student path log (collapsed) ────────────────────────────────
with st.expander("👨‍🎓 Your Full Path Log"):
    st.dataframe(
        pd.DataFrame([{"#": i, "Position": str(n)}
                      for i, n in enumerate(st.session_state.player_path)]),
        use_container_width=True, height=200,
    )