# 🧩 Intelligent Maze Solver AI

### An Interactive Educational Tool for Learning DFS, BFS, and A\* Search Algorithms

🌐 **Live Demo:** [ai-maze-solver.streamlit.app](https://ai-maze-solver.streamlit.app/)

---

## 📖 Overview

Navigate a maze manually first, then watch three classic AI search algorithms — **DFS**, **BFS**, and **A\*** — solve the exact same maze step by step, with every node explored, every decision made, and every cost calculated fully visible.

The project comes in two versions:
- 🖥️ **Pygame Desktop App** — real-time animated visualization with Space-bar step control
- 🌐 **Streamlit Web App** — browser-based interactive tool, works on mobile too

> **"Learn by doing, then learn by watching."**

---

## ✨ Features

| Feature | Description |
|---|---|
| 🕹️ **Play Mode** | Navigate the maze yourself using arrow keys (Pygame) or on-screen D-pad (Streamlit) |
| 🔍 **Step-by-Step AI** | Watch DFS, BFS, or A\* explore node by node — not all at once |
| 🟨 **Live Exploration** | Every visited node highlighted in yellow as the algorithm discovers it |
| 🔵 **Path Tracing** | After exploration, the shortest path is traced in blue step by step |
| 📊 **AI Logic Panel** | Real-time display of current node, g(n), h(n), f(n) values for A\* |
| 📈 **Comparison** | Compare your path length vs AI path length side by side |
| 🎲 **Random Mazes** | Generate new random mazes to test different scenarios |
| 📚 **Algorithm Explainer** | Built-in tab-based explanation of how each algorithm works |

---

---

## 🗂️ Project Structure

```
intelligent-maze-solver/
│
├── 📄 main.py              # Entry point — Pygame desktop app
├── 📄 app.py               # Streamlit web app
├── 📄 maze.py              # Maze definition & random maze generator
├── 📄 dfs.py               # Depth-First Search implementation
├── 📄 bfs.py               # Breadth-First Search implementation
├── 📄 astar.py             # A* Search implementation
├── 📄 heuristics.py        # Manhattan Distance heuristic function
├── 📄 visualize.py         # Pygame rendering & animation engine
│
├── 📁 screenshots/         # App screenshots (for README)
└── 📄 README.md
```

---

## ⚙️ Installation

### Prerequisites

- Python 3.8 or higher
- pip

### 1. Clone the Repository

```bash
git clone https://github.com/umairkaleem/intelligent-maze-solver.git
cd intelligent-maze-solver
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install pygame streamlit pandas
```

### 3. Run the App

**Pygame Desktop Version:**
```bash
python main.py
```

**Streamlit Web Version:**
```bash
streamlit run app.py
```

Then open your browser at `http://localhost:8501`

---

## 🎮 How to Use

### Pygame Version

| Key | Action |
|---|---|
| `↑ ↓ ← →` | Move player through the maze |
| `1` | Run Depth-First Search (DFS) |
| `2` | Run Breadth-First Search (BFS) |
| `3` | Run A\* Search |
| `Space` | Advance one step in the algorithm |
| `ESC` | Quit the application |

### Streamlit Version

1. **Move yourself** — Use the ⬆ ⬅ ⬇ ➡ buttons above the maze
2. **Run an algorithm** — Click **▶ Run DFS**, **▶ Run BFS**, or **▶ Run A\***
3. **Step through it** — Use **◀ Prev** and **Next ▶** to go one node at a time
4. **Skip phases** — Jump straight to path tracing with **⏩ Skip → Path Phase**
5. **Compare** — Check the AI Panel on the right to see your moves vs AI path length

---

## 🎨 Color Guide

| Color | Meaning |
|---|---|
| 🟩 Green | Start node |
| 🟥 Red | Goal node |
| 🟪 Purple | Your current position |
| 🟦 Light Blue | Your path (human navigation trail) |
| 🟨 Yellow | Nodes explored by the AI algorithm |
| 🔵 Dark Blue | Final shortest path found by AI |
| ⬛ Black | Wall (impassable) |
| ⬜ White | Open cell (passable) |

---

## 📚 Algorithms

### 🌲 Depth-First Search (DFS)

Uses a **stack (LIFO)** — dives as deep as possible before backtracking.

```
Start → Push to stack → Pop & explore deepest node → Backtrack on dead ends
```

- ✅ Low memory usage
- ✅ Simple to implement
- ❌ Does **not** guarantee shortest path
- ❌ Can get stuck in long dead ends

**Complexity:** Time `O(V+E)` | Space `O(V)` | Optimal: No

---

### 🌊 Breadth-First Search (BFS)

Uses a **queue (FIFO)** — expands level by level like ripples in water.

```
Start → Enqueue → Visit all nodes at distance 1 → then distance 2 → ...
```

- ✅ Guarantees the **shortest path** (unweighted graph)
- ✅ Systematic and predictable
- ❌ Higher memory usage than DFS
- ❌ Slower on large open spaces

**Complexity:** Time `O(V+E)` | Space `O(V)` | Optimal: **Yes**

---

### ⭐ A\* Search Algorithm

Uses a **priority queue** ordered by `f(n) = g(n) + h(n)`.

| Term | Meaning |
|---|---|
| `g(n)` | Exact cost from start to node n |
| `h(n)` | Manhattan Distance estimate from n to goal |
| `f(n)` | Total estimated cost through n |

```
Manhattan Distance: h(n) = |row_goal - row_n| + |col_goal - col_n|
```

- ✅ Finds the **optimal path efficiently**
- ✅ Far fewer nodes explored than BFS
- ✅ Live cost values visible in the AI Panel
- ❌ More complex to implement
- ❌ Performance depends on heuristic quality

**Complexity:** Time `O(E log V)` | Space `O(V)` | Optimal: **Yes** *(with admissible heuristic)*

---

## 🧪 Algorithm Comparison

| Property | DFS | BFS | A\* |
|---|:---:|:---:|:---:|
| Guarantees shortest path | ❌ | ✅ | ✅ |
| Memory efficient | ✅ | ❌ | ⚠️ |
| Uses heuristic | ❌ | ❌ | ✅ |
| Speed on large mazes | ⚠️ | ❌ | ✅ |
| Implementation complexity | Simple | Simple | Moderate |

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| **Python 3.x** | Core language — algorithm logic and program flow |
| **Pygame** | Desktop graphics, animation, keyboard input |
| **Streamlit** | Web-based interactive UI |
| **heapq** | Priority queue for A\* (always expands lowest f(n) first) |
| **collections.deque** | FIFO queue for BFS |
| **Pandas** | Data display in Streamlit tables |

---

## 🚀 Future Enhancements

- [ ] Random maze generation (Recursive Backtracker, Prim's algorithm)
- [ ] Multiple difficulty levels (maze size & wall density)
- [ ] Dijkstra's Algorithm and Greedy Best-First Search
- [ ] Custom maze editor — draw your own walls
- [ ] Performance graphs (nodes explored, path length, execution time)
- [ ] Timer and scoring system for Play Mode
