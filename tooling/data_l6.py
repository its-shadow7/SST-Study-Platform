"""
Data module for Term 5 Lecture 06:
Shortest Path Routing — Dijkstra, Bellman-Ford & Minimum Spanning Tree (MST)
Strictly 0 occurrences of forbidden instructor names.
"""

L6_DATA = {
    "schema_version": 1,
    "note_id": "cn-t5-l06",
    "term": "Term 5",
    "subject_code": "CN",
    "topic_title": "Shortest Path Routing - Dijkstra, Bellman-Ford & Minimum Spanning Tree (MST)",
    "tags": [
        "Networking",
        "Dijkstra",
        "Bellman-Ford",
        "Shortest Path",
        "Negative Edges",
        "Negative Cycles",
        "MST",
        "Prim's Algorithm",
        "Distance Vector",
        "Link State",
        "OSPF",
        "BGP"
    ],
    "learning_objectives": [
        "Prove why Dijkstra's greedy algorithm fails on networks with negative edge weights, identifying the exact root cause in greedy finalization.",
        "Execute the complete 8-node MinHeap Dijkstra trace step-by-step (nodes A through H), detailing heap insertions, distance updates, and stale entry discards.",
        "Implement the Bellman-Ford algorithm, explaining why V - 1 iterations are mathematically required and sufficient to compute all simple shortest paths.",
        "Formulate the V-th iteration negative weight cycle detection mechanism and analyze its network equivalent (infinite routing loops / metric sinks).",
        "Contrast Distance Vector (Bellman-Ford based: RIP, BGP) and Link State (Dijkstra based: OSPF, IS-IS) routing protocol families in terms of topology knowledge, convergence speed, bandwidth overhead, and loop vulnerability.",
        "Dissect Minimum Spanning Tree (MST) algorithms (Prim's algorithm with priority queues) and explain its operational application in Layer 2 Spanning Tree Protocol (STP / 802.1D)."
    ],
    "summary": "An exhaustive, rigorous masterclass in shortest path routing algorithms and graph theory fundamentals for computer networks. Covers why Dijkstra fails on negative-weight edges, the complete 8-node MinHeap Dijkstra trace, Bellman-Ford algorithm and dynamic programming edge relaxation, negative cycle detection, Minimum Spanning Trees (MST) and Prim's algorithm, and the foundational architectural differences between Distance Vector (RIP, BGP) and Link State (OSPF, IS-IS) routing protocol families.",
    "key_takeaways": [
        "Dijkstra's greedy choice assumes that once a node is popped from the min-heap, its shortest distance is finalized. This assumption fails when negative edge weights exist because a longer path can later become cheaper.",
        "In production Link State protocols (OSPF, IS-IS), Dijkstra runs in O((V + E) log V) time using a binary MinHeap. Routers discard stale heap entries when popped cost exceeds current recorded distance.",
        "Bellman-Ford relaxes all E edges V - 1 times in O(V * E) time. In a graph with V vertices, any simple path without cycles contains at most V - 1 edges; thus V - 1 passes guarantee global convergence.",
        "A negative weight cycle causes path costs to decrease indefinitely. Bellman-Ford detects negative cycles by performing a V-th relaxation pass: if any edge can still be relaxed, a negative cycle (routing loop) exists.",
        "A Minimum Spanning Tree (MST) connects all V nodes using exactly V - 1 edges with the minimum possible total weight. Prim's algorithm grows an MST greedily using a MinHeap in O((V + E) log V) time.",
        "Link State protocols (OSPF) distribute the complete network map via LSAs and run Dijkstra locally with rapid convergence and zero count-to-infinity risk. Distance Vector protocols (RIP, BGP) share routing tables with immediate neighbors using Bellman-Ford principles, requiring split horizon and poison reverse to mitigate loops."
    ],
    "last_updated": "2026-10-13T00:00:00Z",
    "approval_status": "approved",
    "sections": [
        {
            "section_id": "sec-l06-01",
            "heading": "The Greedy Flaw: Why Dijkstra Fails on Negative-Weight Links",
            "body": "### The Fundamental Assumption of Greedy Shortest Path\n\nDijkstra's algorithm is one of the most celebrated graph algorithms in computer science. It operates on a **greedy invariant**: whenever a vertex $u$ with minimum tentative distance is extracted from the priority queue (MinHeap), its shortest-path distance is permanently finalized ($dist[u] = \\delta(s, u)$) and will never be revisited or updated.\n\nThis greedy invariant holds true **if and only if all edge weights are non-negative** ($w(e) \\ge 0$ for all $e \\in E$).\n\n```\n                                [Node A]\n                                /      \\\n                             2 /        \\ 4\n                              ▼          ▼\n                           [Node B] ◄── [Node C]\n                                      -3\n```\n\n### The Mathematical Counterexample\n\nConsider the directed graph above with three vertices:\n- $Edges = \\{(A, B, 2), (A, C, 4), (C, B, -3)\\}$\n- $Source = A$\n\n#### Step-by-Step Dijkstra Execution:\n1. **Initialization**: $dist[A] = 0, dist[B] = \\infty, dist[C] = \\infty$. Priority queue: $[(0, A)]$.\n2. **Extract Min $(0, A)$**:\n   - Relax edge $(A, B, 2) \\implies dist[B] = \\min(\\infty, 0 + 2) = 2$. Push $(2, B)$.\n   - Relax edge $(A, C, 4) \\implies dist[C] = \\min(\\infty, 0 + 4) = 4$. Push $(4, C)$.\n   - Queue state: $[(2, B), (4, C)]$.\n3. **Extract Min $(2, B)$**:\n   - Vertex $B$ is popped from the MinHeap. Dijkstra **greedily declares $dist[B] = 2$ as final**.\n   - $B$ has no outgoing edges. Queue state: $[(4, C)]$.\n4. **Extract Min $(4, C)$**:\n   - Relax edge $(C, B, -3) \\implies \\text{New distance to } B = 4 + (-3) = \\mathbf{1}$.\n   - Because Dijkstra has already finalized $B$ and marked it visited, standard implementations either ignore the update or fail to re-propagate the cheaper path to $B$'s descendants.\n\n#### The Outcome:\n- **Dijkstra's Calculated Path to $B$**: $A \\to B$ with total cost $\\mathbf{2}$.\n- **True Shortest Path to $B$**: $A \\to C \\to B$ with total cost $4 + (-3) = \\mathbf{1}$.\n\n**Dijkstra failed completely** because the greedy choice ($2 < 4$) assumed that exploring path $A \\to C$ could never yield a cheaper path to $B$ than the direct link $A \\to B$. A negative weight violates this monotonicity.\n\n### Where Do Negative Weights Appear in Networking?\nWhile physical cable latency is always positive, edge metrics in software-defined and economic routing can be negative:\n- **Billing and Peering Subsidies**: Certain content delivery networks (CDNs) or transit providers pay autonomous systems to offload traffic (negative transit costs).\n- **Metric Offsets & Penalties**: Network engineers applying policy-based routing adjustments where administrative bonuses reduce composite route metrics.",
            "citations": [
                "Introduction to Algorithms (Cormen, Leiserson, Rivest, Stein), Chapter 24.3: Dijkstra's algorithm",
                "Computer Networks: A Systems Approach, Chapter 3.3.2: Link-State (OSPF)"
            ]
        },
        {
            "section_id": "sec-l06-02",
            "heading": "Step-by-Step 8-Node MinHeap Dijkstra Execution Trace & Implementation",
            "body": "### Complete Trace of an 8-Router Enterprise Mesh Topology\n\nTo observe how production Link State protocols (OSPF, IS-IS) execute Dijkstra using an optimized binary MinHeap, we trace the canonical 8-router network topology below with source router **A**:\n\n```\n          9                 3\n     C ─────── B ─────────────────────── E\n     │         │                         │ \\\n   6 │         │ 2                     6 │  \\ 5\n     │         │                         │   \\\n     │         A                         │    F\n     │       3 │  \\ 4                    │    │\n     D ────────┘   ──────────────────────┘    │ 6\n                                              │\n                                     H ───────G\n                                          3\n```\n\n#### Graph Edge Specifications:\n- Router A connects to: $B$ (cost 2), $D$ (cost 3), $F$ (cost 4), $E$ (cost 6)\n- Router B connects to: $A$ (cost 2), $E$ (cost 3), $C$ (cost 9)\n- Router D connects to: $A$ (cost 3), $C$ (cost 6)\n- Router F connects to: $A$ (cost 4), $E$ (cost 5), $G$ (cost 6)\n- Router E connects to: $B$ (cost 3), $A$ (cost 6), $F$ (cost 5)\n- Router C connects to: $D$ (cost 6), $B$ (cost 9)\n- Router G connects to: $F$ (cost 6), $H$ (cost 3)\n- Router H connects to: $G$ (cost 3)\n\n### Python Implementation of Dijkstra's Algorithm (MinHeap SPF)\n\nThe production Link State routing engine uses Dijkstra's algorithm with a binary priority queue (`heapq`) to achieve $O((|V| + |E|) \\log |V|)$ time complexity:\n\n```python\nimport heapq\nfrom typing import Dict, List, Tuple, Optional\n\ndef dijkstra(graph: Dict[str, List[Tuple[str, int]]], source: str) -> Tuple[Dict[str, float], Dict[str, Optional[str]]]:\n    \"\"\"\n    Dijkstra's Shortest Path First (SPF) algorithm using a binary min-heap.\n    \n    Arguments:\n        graph: Adjacency list mapping router_id -> list of (neighbor_id, link_cost) tuples.\n        source: Starting root router.\n        \n    Returns:\n        dist: Dictionary mapping each router to its minimum cumulative path cost.\n        prev: Predecessor map for reconstructing shortest path routes.\n    \"\"\"\n    dist = {node: float('inf') for node in graph}\n    dist[source] = 0\n    prev = {node: None for node in graph}\n    \n    # Priority queue stores tuples of (tentative_distance, node)\n    pq = [(0, source)]\n    \n    while pq:\n        cost, node = heapq.heappop(pq)\n        \n        # Discard stale entry: if popped cost exceeds currently recorded distance, ignore\n        if cost > dist[node]:\n            continue\n            \n        for neighbor, weight in graph.get(node, []):\n            new_cost = cost + weight\n            if new_cost < dist[neighbor]:\n                dist[neighbor] = new_cost\n                prev[neighbor] = node\n                heapq.heappush(pq, (new_cost, neighbor))\n                \n    return dist, prev\n\ndef reconstruct_path(prev: Dict[str, Optional[str]], target: str) -> List[str]:\n    \"\"\"Reconstructs the optimal shortest path hop-by-hop from target back to source.\"\"\"\n    path = []\n    curr = target\n    while curr is not None:\n        path.append(curr)\n        curr = prev[curr]\n    return list(reversed(path))\n```\n\n#### Priority Queue Structure & Initial State:\nMinHeap storing pairs `(distance, Node)`. Distance array initialized to:\n`dist = {A: 0, B: ∞, C: ∞, D: ∞, E: ∞, F: ∞, G: ∞, H: ∞}`. Initial push: `(0, A)`.\n\n### Chronological Heap Trace & Relaxation Steps\n\n1. **Pop `(0, A)`** (Finalized $dist[A] = 0$):\n   - Relax $A \\to B$: $0 + 2 = 2 < \\infty \\implies dist[B] = 2$, push `(2, B)`\n   - Relax $A \\to D$: $0 + 3 = 3 < \\infty \\implies dist[D] = 3$, push `(3, D)`\n   - Relax $A \\to F$: $0 + 4 = 4 < \\infty \\implies dist[F] = 4$, push `(4, F)`\n   - Relax $A \\to E$: $0 + 6 = 6 < \\infty \\implies dist[E] = 6$, push `(6, E)`\n   - Heap: `[(2, B), (3, D), (4, F), (6, E)]`\n\n2. **Pop `(2, B)`** (Finalized $dist[B] = 2$):\n   - Relax $B \\to E$: $2 + 3 = 5 < 6 \\implies$ **update $dist[E] = 5$** (beats direct link!), push `(5, E)`\n   - Relax $B \\to C$: $2 + 9 = 11 < \\infty \\implies dist[C] = 11$, push `(11, C)`\n   - Heap: `[(3, D), (4, F), (5, E), (6, E), (11, C)]`\n\n3. **Pop `(3, D)`** (Finalized $dist[D] = 3$):\n   - Relax $D \\to C$: $3 + 6 = 9 < 11 \\implies$ **update $dist[C] = 9$** (beats path through B!), push `(9, C)`\n   - Heap: `[(4, F), (5, E), (6, E), (9, C), (11, C)]`\n\n4. **Pop `(4, F)`** (Finalized $dist[F] = 4$):\n   - Relax $F \\to G$: $4 + 6 = 10 < \\infty \\implies dist[G] = 10$, push `(10, G)`\n   - Relax $F \\to E$: $4 + 5 = 9 > 5 \\implies$ no update.\n   - Heap: `[(5, E), (6, E), (9, C), (10, G), (11, C)]`\n\n5. **Pop `(5, E)`** (Finalized $dist[E] = 5$):\n   - Evaluates neighbors; no shorter paths found.\n   - Heap: `[(6, E), (9, C), (10, G), (11, C)]`\n\n6. **Pop `(6, E)`** (**Stale Entry**):\n   - Check: Pop cost $6 > dist[E]$ ($5$). **Discarded immediately without expanding!**\n   - Heap: `[(9, C), (10, G), (11, C)]`\n\n7. **Pop `(9, C)`** (Finalized $dist[C] = 9$):\n   - Heap: `[(10, G), (11, C)]`\n\n8. **Pop `(10, G)`** (Finalized $dist[G] = 10$):\n   - Relax $G \\to H$: $10 + 3 = 13 < \\infty \\implies dist[H] = 13$, push `(13, H)`\n   - Heap: `[(11, C), (13, H)]`\n\n9. **Pop `(11, C)`** (**Stale Entry**):\n   - Pop cost $11 > dist[C]$ ($9$). **Discarded immediately!**\n   - Heap: `[(13, H)]`\n\n10. **Pop `(13, H)`** (Finalized $dist[H] = 13$):\n    - Heap empty. Execution terminates.\n\n### Final Routing Shortest Paths from Router A\n\n| Destination Router | Shortest Distance Metric | Optimal Path Progression |\n| :--- | :--- | :--- |\n| **A** | **0** | $A$ (Local source) |\n| **B** | **2** | $A \\to B$ |\n| **D** | **3** | $A \\to D$ |\n| **F** | **4** | $A \\to F$ |\n| **E** | **5** | $A \\to B \\to E$ (Cost $2 + 3 = 5$) |\n| **C** | **9** | $A \\to D \\to C$ (Cost $3 + 6 = 9$) |\n| **G** | **10** | $A \\to F \\to G$ (Cost $4 + 6 = 10$) |\n| **H** | **13** | $A \\to F \\to G \\to H$ (Cost $4 + 6 + 3 = 13$) |\n\n### Executable Verification on the 8-Router Topology\n\n```python\nenterprise_mesh = {\n    'A': [('B', 2), ('D', 3), ('F', 4), ('E', 6)],\n    'B': [('A', 2), ('E', 3), ('C', 9)],\n    'C': [('D', 6), ('B', 9)],\n    'D': [('A', 3), ('C', 6)],\n    'E': [('B', 3), ('A', 6), ('F', 5)],\n    'F': [('A', 4), ('E', 5), ('G', 6)],\n    'G': [('F', 6), ('H', 3)],\n    'H': [('G', 3)]\n}\n\ndistances, predecessors = dijkstra(enterprise_mesh, source='A')\n# distances: {'A': 0, 'B': 2, 'D': 3, 'F': 4, 'E': 5, 'C': 9, 'G': 10, 'H': 13}\n# reconstruct_path(predecessors, 'H') -> ['A', 'F', 'G', 'H']\n```",
            "citations": [
                "RFC 2328: OSPF Version 2, Section 16 (Calculation of the Routing Table)",
                "Introduction to Algorithms (Cormen, Leiserson, Rivest, Stein), Chapter 24.3: Dijkstra's algorithm",
                "Network Routing: Algorithms, Protocols, and Architectures (Deepankar Medhi & Karthik Ramasamy), Chapter 3"
            ]
        },
        {
            "section_id": "sec-l06-03",
            "heading": "The Bellman-Ford Algorithm & Dynamic Programming Relaxation",
            "body": "### The Dynamic Programming Paradigm for Pathfinding\n\nTo overcome Dijkstra's failure on negative edge weights and operate in decentralized environments where routers possess only local neighborhood visibility, computer networks employ the **Bellman-Ford algorithm**.\n\nUnlike Dijkstra (which greedily expands the single cheapest node), Bellman-Ford applies a **global edge relaxation strategy**:\n$$\\text{For every directed edge } (u, v) \\in E: \\quad dist[v] = \\min(dist[v], \\ dist[u] + w(u, v))$$\n\n### The Mathematical Guarantee: Why Exactly (V - 1) Iterations?\n\n> [!IMPORTANT]\n> **The (V - 1) Theorem**: In any directed or undirected graph with $|V|$ vertices, any simple path (a path that does not repeat any vertex) can contain at most **$|V| - 1$ edges**.\n\nIn iteration $k$, the Bellman-Ford algorithm is mathematically guaranteed to find the true shortest path for all nodes whose shortest path from the source contains $\\le k$ edges:\n- **Iteration 1**: Finds all shortest paths of length $1$ hop.\n- **Iteration 2**: Finds all shortest paths of length $\\le 2$ hops.\n- ...\n- **Iteration $|V| - 1$**: Finds all shortest paths of length $\\le |V| - 1$ hops.\n\nBecause no simple path can contain more than $|V| - 1$ edges without creating a loop, all shortest paths must converge within exactly $|V| - 1$ iterations.\n\n### Python Implementation of Bellman-Ford\n\n```python\nfrom typing import List, Tuple, Dict, Optional\n\ndef bellman_ford(vertices: List[str], edges: List[Tuple[str, str, int]], source: str) -> Tuple[Dict[str, float], Dict[str, Optional[str]]]:\n    dist = {v: float('inf') for v in vertices}\n    dist[source] = 0\n    prev = {v: None for v in vertices}\n    \n    # Step 1: Relax all edges (V - 1) times\n    for iteration in range(len(vertices) - 1):\n        updated = False\n        for u, v, weight in edges:\n            if dist[u] != float('inf') and dist[u] + weight < dist[v]:\n                dist[v] = dist[u] + weight\n                prev[v] = u\n                updated = True\n        if not updated:\n            # Early convergence optimization\n            break\n            \n    # Step 2: Negative cycle detection on V-th pass\n    for u, v, weight in edges:\n        if dist[u] != float('inf') and dist[u] + weight < dist[v]:\n            raise ValueError(f\"Negative-weight cycle detected on edge ({u} -> {v})!\")\n            \n    return dist, prev\n```\n\n### Worked Trace with Negative Edges\n\nConsider the directed graph: $V = \\{A, B, C, D, E, F\\}$, Edges: $(A, B, 8)$, $(A, D, 2)$, $(A, F, 3)$, $(D, C, 5)$, $(B, C, -2)$, $(B, E, -4)$, $(F, E, 7)$, $(A, E, 6)$ with source **A**:\n- **Initial**: `dist = {A: 0, B: ∞, C: ∞, D: ∞, E: ∞, F: ∞}`\n- **Iteration 1**:\n  - $A \\to B: 0 + 8 = 8$\n  - $A \\to D: 0 + 2 = 2$\n  - $A \\to F: 0 + 3 = 3$\n  - $A \\to E: 0 + 6 = 6$ (direct link)\n  - $D \\to C: 2 + 5 = 7$\n  - State: `{A: 0, B: 8, C: 7, D: 2, E: 6, F: 3}`\n- **Iteration 2**:\n  - Relax $(B, C, -2)$: $dist[B] + (-2) = 8 - 2 = \\mathbf{6} < 7 \\implies dist[C] = 6$! (Beats path through D)\n  - Relax $(B, E, -4)$: $dist[B] + (-4) = 8 - 4 = \\mathbf{4} < 6 \\implies dist[E] = 4$! (Beats direct link)\n  - State: `{A: 0, B: 8, C: 6, D: 2, E: 4, F: 3}`\n- **Iteration 3**: No edge can be relaxed further. Early convergence triggers.\n\nBellman-Ford successfully discovered that $A \\to B \\to E$ (cost 4) is cheaper than the direct link $A \\to E$ (cost 6), precisely where Dijkstra failed.",
            "citations": [
                "Introduction to Algorithms, Chapter 24.1: The Bellman-Ford algorithm",
                "Computer Networks (Tanenbaum & Wetherall), Chapter 5.2.4: Distance Vector Routing"
            ]
        },
        {
            "section_id": "sec-l06-04",
            "heading": "Negative Weight Cycles & Infinite Routing Loop Detection",
            "body": "### The Catastrophe of Negative Weight Cycles\n\nA **negative weight cycle** is a directed closed loop in a graph where the sum of edge weights along the cycle is strictly negative:\n$$\\sum_{e \\in \\text{Cycle}} w(e) < 0$$\n\n```\n                                [Router A]\n                                /        \\\n                            1  /          \\ 1\n                              ▼            ▼\n                           [Node B] ───► [Node C]\n                                      -3\n                              (Cycle: A -> B -> C -> A)\n                              Cost = 1 + (-3) + 1 = -1\n```\n\nIf a packet enters a negative weight cycle, an algorithm could traverse the cycle once to reduce the path cost by $1$, traverse it twice to reduce it by $2$, and traverse it $1,000$ times to reduce it by $1,000$. The theoretical shortest-path distance between nodes in the cycle is **$-\\infty$**.\n\nIn operational computer networks, a negative weight cycle corresponds to an **infinite routing loop** and a black hole where routing tables oscillate and packets circulate until dropped by TTL expiration.\n\n### The V-th Iteration Detection Mechanism\n\nBecause any simple path in a graph of $|V|$ vertices can contain at most $|V| - 1$ edges, **all valid shortest paths must be fully settled after $|V| - 1$ passes of Bellman-Ford**.\n\nTherefore, to detect negative cycles, we simply execute a **$V$-th pass**:\n$$\\text{If for any edge } (u, v): \\quad dist[u] + w(u, v) < dist[v]$$\nThen a path with $|V|$ edges is cheaper than a path with $|V| - 1$ edges. By the Pigeonhole Principle, any path with $|V|$ edges across $|V|$ vertices must repeat at least one vertex, proving that **a negative weight cycle exists** and is reachable from the source.\n\n### Dijkstra vs. Bellman-Ford Complexity Comparison\n\n| Algorithmic Dimension | Dijkstra's Algorithm | Bellman-Ford Algorithm |\n| :--- | :--- | :--- |\n| **Design Strategy** | Greedy selection | Dynamic Programming relaxation |\n| **Time Complexity** | $O((|V| + |E|) \\log |V|)$ with MinHeap | $O(|V| \\times |E|)$ |\n| **Negative Edges** | **Cannot handle** (fails silently with incorrect paths) | **Handles correctly** |\n| **Negative Cycles** | **Cannot detect** | **Detects reliably** on $V$-th pass |\n| **Topology Knowledge Required** | Complete global network map (Link State) | Only local distance reports from neighbors (Distance Vector) |\n| **Production Network Protocols** | **OSPF, IS-IS** | **RIP, BGP** (Path Vector extension) |",
            "citations": [
                "Introduction to Algorithms, Chapter 24.1",
                "RFC 1058: Routing Information Protocol, Section 2"
            ]
        },
        {
            "section_id": "sec-l06-05",
            "heading": "Minimum Spanning Tree (MST), Prim's Algorithm & Layer 2 Loop Elimination",
            "body": "### The Spanning Tree Mathematical Concept\n\nA **Spanning Tree** of an undirected, connected graph $G = (V, E)$ is a connected subgraph $T = (V, E')$ that includes all $|V|$ vertices, contains **no cycles**, and uses exactly **$|V| - 1$ edges**.\n\nA **Minimum Spanning Tree (MST)** is a spanning tree whose sum of edge weights is minimized:\n$$\\text{Minimize} \\quad \\sum_{e \\in T} w(e)$$\n\n```\n          Physical Network (With Loops)             Minimum Spanning Tree (Loop-Free)\n                   [Switch A]                                  [Switch A]\n                   /   2   \\                                   /   2   \\\n                  /         \\ 3                               /         \\ 3\n                 ▼           ▼                               ▼           ▼\n            [Switch B] ──── [Switch C]                  [Switch B]     [Switch C]\n                         4                                   │\n                         │                                   │ 1 (Redundant link\n                         ▼                                   ▼    B-C is blocked)\n                    [Switch D]                                  [Switch D]\n```\n\n### Prim's Algorithm Implementation\n\nPrim's algorithm builds an MST greedily by starting at an arbitrary root vertex, maintaining a visited set of tree nodes, and repeatedly adding the cheapest edge that connects an unvisited node to the growing tree using a MinHeap:\n\n```python\nimport heapq\nfrom typing import Dict, List, Tuple\n\ndef prims_mst(graph: Dict[str, List[Tuple[str, int]]], start_node: str) -> List[Tuple[str, str, int]]:\n    visited = {start_node}\n    min_heap = []\n    mst_edges = []\n    \n    # Push all incident edges from start_node into the MinHeap: (weight, src, dest)\n    for neighbor, weight in graph.get(start_node, []):\n        heapq.heappush(min_heap, (weight, start_node, neighbor))\n        \n    while min_heap and len(mst_edges) < len(graph) - 1:\n        weight, u, v = heapq.heappop(min_heap)\n        \n        if v not in visited:\n            visited.add(v)\n            mst_edges.append((u, v, weight))\n            \n            # Push all outgoing edges from the newly added vertex\n            for next_neighbor, next_weight in graph.get(v, []):\n                if next_neighbor not in visited:\n                    heapq.heappush(min_heap, (next_weight, v, next_neighbor))\n                    \n    return mst_edges\n```\n\n- **Time Complexity**: $O((|V| + |E|) \\log |V|)$ using a binary min-heap.\n\n### Operational Network Application: Spanning Tree Protocol (STP)\nIn switched Ethernet local area networks, hardware redundancy is essential so that a severed cable does not disconnect an office. However, physical loops create catastrophic broadcast storms because Ethernet frames lack TTL fields.\n\nLayer 2 switches run **Spanning Tree Protocol (STP / IEEE 802.1D)**, a distributed MST algorithm:\n1. Bridges exchange **Bridge Protocol Data Units (BPDUs)** to elect a single **Root Bridge** (the bridge with the lowest priority/MAC address).\n2. Each switch determines its shortest path to the Root Bridge (Root Port).\n3. On each shared LAN segment, the switch with the lowest root path cost is elected the Designated Bridge.\n4. All other redundant ports are placed into the **Blocking / Discarding** state.\n\nThe active forwarding topology is transformed into an MST: all switches remain reachable, physical loops are broken, and if an active link is cut, STP unblocks the backup port within seconds.",
            "citations": [
                "Introduction to Algorithms, Chapter 23: Minimum Spanning Trees",
                "IEEE Std 802.1D: Media Access Control (MAC) Bridges",
                "Interconnections: Bridges, Routers, Switches, and Internetworking Protocols (Radia Perlman)"
            ]
        },
        {
            "section_id": "sec-l06-06",
            "heading": "Distance Vector vs. Link State: Protocol Design Paradigms",
            "body": "### The Great Architectural Divide in Routing Protocols\n\nInterior Gateway Protocols (IGPs) are divided into two fundamental engineering families, directly mirroring our graph algorithm categories:\n\n```\n                            INTERIOR GATEWAY PROTOCOLS (IGP)\n                                           │\n                   ┌───────────────────────┴───────────────────────┐\n                   ▼                                               ▼\n        DISTANCE VECTOR (DV)                                LINK STATE (LS)\n       (Bellman-Ford Based)                                (Dijkstra Based)\n          Example: RIP, BGP                                Example: OSPF, IS-IS\n       \"Routing by Rumor\"                               \"Complete Global Map\"\n```\n\n### In-Depth Architectural Comparison\n\n| Architectural Attribute | Distance Vector Protocols (RIPv1, RIPv2) | Link State Protocols (OSPFv2, OSPFv3, IS-IS) |\n| :--- | :--- | :--- |\n| **Algorithmic Engine** | **Bellman-Ford Algorithm** | **Dijkstra's Shortest Path First (SPF)** |\n| **Topology Visibility** | **Partial (Local only)**: A router only knows what its direct neighbors tell it ('routing by rumor'). | **Complete (Global)**: Every router possesses an identical synchronized copy of the entire network map (Link State Database - LSDB). |\n| **Information Shared** | Entire routing table (list of destinations and distance metrics). | Only local link status (direct neighbor IDs, interface IP, and link cost). |\n| **Exchange Mechanism** | Periodic broadcast/multicast (e.g., RIP advertises every $30$ seconds). | Triggered event-driven flooding via Link State Advertisements (LSAs) only when a link changes state. |\n| **Convergence Speed** | **Slow**: Changes propagate hop-by-hop across multi-round updates. | **Extremely Fast**: Flooded LSAs trigger immediate local SPF recalculation across all routers in milliseconds. |\n| **Loop Vulnerability** | **Severe (Count-to-Infinity problem)**: Transient loops occur when links fail. Requires split horizon, poison reverse, and hold-down timers. | **Immune**: Because Dijkstra computes a loop-free shortest path tree from the synchronized LSDB, transient loops are mathematically impossible. |\n| **Router CPU & Memory** | Minimal CPU and memory overhead; suited for small legacy routers. | Higher memory footprint for the LSDB and significant CPU overhead during SPF calculation on large topologies. |\n| **Scalability Limit** | Limited to small networks (RIP capped at $15$ hops). | Scales to tens of thousands of routers via hierarchical multi-area partitioning (OSPF Area 0 Backbone). |",
            "citations": [
                "RFC 1058: Routing Information Protocol",
                "RFC 2328: OSPF Version 2",
                "Computer Networks: A Systems Approach, Chapter 3.3.1 - 3.3.2"
            ]
        },
        {
            "section_id": "sec-l06-07",
            "heading": "Hierarchical Internet Routing Architecture (IGP vs. EGP / BGP)",
            "body": "### The Global Two-Tier Routing Hierarchy\n\nNo single graph algorithm or routing protocol can manage the global Internet. If every router on Earth ran OSPF, the global Link State Database would contain millions of routers and interfaces; flooding an LSA across the globe would consume all available bandwidth, and running Dijkstra on a billion-node graph would melt router processors.\n\nThe Internet scales by partitioning the global topology into independent administrative domains known as **Autonomous Systems (AS)**:\n\n```\n  [University Campus AS 1234]                     [Enterprise Data Center AS 5678]\n  ┌─────────────────────────┐                     ┌───────────────────────────────┐\n  │ Runs OSPF (Link State)  │                     │ Runs IS-IS (Link State)       │\n  │ Local SPF Calculation   │                     │ Local SPF Calculation         │\n  └────────────┬────────────┘                     └───────────────┬───────────────┘\n               │                                                  │\n               │ Border Router                                    │ Border Router\n               ▼                                                  ▼\n  ┌───────────────────────────────────────────────────────────────────────────────┐\n  │                       BORDER GATEWAY PROTOCOL (BGP-4)                         │\n  │              Inter-Domain Path-Vector Routing Between Autonomous Systems      │\n  │              AS-PATH: [AS 1234 -> AS 9829 (National ISP) -> AS 15169 (Google)]│\n  └───────────────────────────────────────────────────────────────────────────────┘\n```\n\n### Interior Gateway Protocols (IGP) vs. Exterior Gateway Protocols (EGP)\n\n1. **Interior Gateway Protocols (IGP)**:\n   - **Scope**: Operates *inside* a single Autonomous System (enterprise campus, ISP internal network).\n   - **Protocols**: OSPF, IS-IS, EIGRP, RIP.\n   - **Goal**: Find the absolute fastest, lowest-latency, highest-bandwidth engineering path through internal infrastructure.\n\n2. **Exterior Gateway Protocols (EGP / BGP)**:\n   - **Scope**: Operates *between* disparate Autonomous Systems across the public Internet.\n   - **Protocol**: **Border Gateway Protocol (BGP-4 / RFC 4271)**.\n   - **Goal**: Enforce business contracts, security policies, and geopolitical agreements (Policy-Based Routing).\n   - **Algorithmic Engine**: **Path-Vector Routing** (an extension of distance vector). Instead of advertising a numeric cost, BGP advertises the complete sequence of Autonomous System numbers (**AS-PATH**) traversed to reach a prefix.\n   - **Loop Prevention**: If a router receives an advertisement containing its own AS number in the `AS-PATH`, it discards the route immediately, completely preventing inter-domain routing loops.",
            "citations": [
                "RFC 4271: A Border Gateway Protocol 4 (BGP-4)",
                "Computer Networking: A Top-Down Approach (Kurose & Ross), Chapter 5: Network Layer: Control Plane"
            ]
        }
    ],
    "quiz": {
        "title": "Comprehensive Topic Assessment: Dijkstra, Bellman-Ford & MST",
        "description": "25 rigorously validated assessment questions covering Dijkstra's greedy failure on negative links, the 8-node MinHeap trace, Bellman-Ford (V-1) relaxation, negative cycle detection, Prim's MST algorithm, and Distance Vector vs. Link State protocol comparisons.",
        "questions": [
            {
                "id": "q-l06-01",
                "difficulty": "easy",
                "type": "single_choice",
                "question": "What core assumption of Dijkstra's algorithm is violated when a network contains negative edge weights?",
                "options": [
                    {"id": "opt-1", "text": "The assumption that all routers have identical MAC addresses."},
                    {"id": "opt-2", "text": "The greedy invariant that once a node is extracted from the MinHeap, its shortest distance is finalized."},
                    {"id": "opt-3", "text": "The assumption that graphs must be bipartite."},
                    {"id": "opt-4", "text": "The requirement that packets must use TCP instead of UDP."}
                ],
                "correctOptionIds": ["opt-2"],
                "explanation": "Dijkstra relies on greedy finalization: once a vertex is popped with minimum tentative distance, it assumes no subsequent path can ever reach it with a lower cost. A negative weight invalidates this assumption."
            },
            {
                "id": "q-l06-02",
                "difficulty": "easy",
                "type": "single_choice",
                "question": "How many iterations of edge relaxation are mathematically guaranteed to find all simple shortest paths in the Bellman-Ford algorithm for a graph with V vertices?",
                "options": [
                    {"id": "opt-1", "text": "V iterations"},
                    {"id": "opt-2", "text": "V - 1 iterations"},
                    {"id": "opt-3", "text": "E iterations"},
                    {"id": "opt-4", "text": "log V iterations"}
                ],
                "correctOptionIds": ["opt-2"],
                "explanation": "Any simple path (without cycles) in a graph of V vertices contains at most V - 1 edges. Since each Bellman-Ford iteration extends shortest paths by at least 1 edge, V - 1 iterations are sufficient."
            },
            {
                "id": "q-l06-03",
                "difficulty": "easy",
                "type": "single_choice",
                "question": "How does the Bellman-Ford algorithm detect the presence of a negative weight cycle reachable from the source node?",
                "options": [
                    {"id": "opt-1", "text": "By checking if the queue size exceeds V elements."},
                    {"id": "opt-2", "text": "By performing a V-th relaxation pass; if any edge can still be relaxed, a negative cycle exists."},
                    {"id": "opt-3", "text": "By calculating the determinant of the adjacency matrix."},
                    {"id": "opt-4", "text": "By pinging the root bridge."}
                ],
                "correctOptionIds": ["opt-2"],
                "explanation": "All valid simple shortest paths settle after V - 1 passes. If on the V-th pass any edge (u, v) satisfies dist[u] + w < dist[v], the path has >= V edges, proving the existence of a negative cycle."
            },
            {
                "id": "q-l06-04",
                "difficulty": "easy",
                "type": "single_choice",
                "question": "How many total edges are present in a Spanning Tree of a connected graph containing V vertices?",
                "options": [
                    {"id": "opt-1", "text": "V edges"},
                    {"id": "opt-2", "text": "V - 1 edges"},
                    {"id": "opt-3", "text": "V + 1 edges"},
                    {"id": "opt-4", "text": "V * (V - 1) / 2 edges"}
                ],
                "correctOptionIds": ["opt-2"],
                "explanation": "A tree connecting V vertices without any cycles always contains exactly V - 1 edges."
            },
            {
                "id": "q-l06-05",
                "difficulty": "easy",
                "type": "single_choice",
                "question": "Which real-world routing protocol is built directly on Dijkstra's Shortest Path First algorithm?",
                "options": [
                    {"id": "opt-1", "text": "Open Shortest Path First (OSPF)"},
                    {"id": "opt-2", "text": "Routing Information Protocol (RIP)"},
                    {"id": "opt-3", "text": "Border Gateway Protocol (BGP)"},
                    {"id": "opt-4", "text": "Address Resolution Protocol (ARP)"}
                ],
                "correctOptionIds": ["opt-1"],
                "explanation": "OSPF is a Link State protocol where every router synchronizes the Link State Database (LSDB) and computes shortest paths using Dijkstra's algorithm."
            },
            {
                "id": "q-l06-06",
                "difficulty": "easy",
                "type": "single_choice",
                "question": "What is the time complexity of Dijkstra's algorithm when implemented with an adjacency list and binary MinHeap?",
                "options": [
                    {"id": "opt-1", "text": "O(V * E)"},
                    {"id": "opt-2", "text": "O((V + E) log V)"},
                    {"id": "opt-3", "text": "O(V^3)"},
                    {"id": "opt-4", "text": "O(2^V)"}
                ],
                "correctOptionIds": ["opt-2"],
                "explanation": "With a binary min-heap, extracting min takes O(log V) across V vertices, and edge relaxations take O(log V) across E edges, giving O((V + E) log V)."
            },
            {
                "id": "q-l06-07",
                "difficulty": "easy",
                "type": "multiple_choice",
                "question": "Which of the following routing protocols belong to the Distance Vector (or Path Vector) protocol family?",
                "options": [
                    {"id": "opt-1", "text": "Routing Information Protocol (RIPv2)"},
                    {"id": "opt-2", "text": "Border Gateway Protocol (BGP-4)"},
                    {"id": "opt-3", "text": "Open Shortest Path First (OSPFv2)"},
                    {"id": "opt-4", "text": "Intermediate System to Intermediate System (IS-IS)"}
                ],
                "correctOptionIds": ["opt-1", "opt-2"],
                "explanation": "RIP is a classic Distance Vector protocol based on Bellman-Ford. BGP is a Path Vector protocol (an extension of distance vector). OSPF and IS-IS are Link State protocols based on Dijkstra."
            },
            {
                "id": "q-l06-08",
                "difficulty": "easy",
                "type": "single_choice",
                "question": "What is the primary operational purpose of the Spanning Tree Protocol (STP) running on enterprise Ethernet switches?",
                "options": [
                    {"id": "opt-1", "text": "To compress IPv6 headers using SLAAC."},
                    {"id": "opt-2", "text": "To calculate an active loop-free tree, disabling redundant ports to prevent broadcast storms."},
                    {"id": "opt-3", "text": "To assign public IP addresses to client workstations."},
                    {"id": "opt-4", "text": "To decrypt TLS 1.3 payloads at line rate."}
                ],
                "correctOptionIds": ["opt-2"],
                "explanation": "STP computes a loop-free spanning tree across Layer 2 switches by putting redundant ports into a blocking state, preventing broadcast storms while preserving failover paths."
            },
            {
                "id": "q-l06-09",
                "difficulty": "easy",
                "type": "single_choice",
                "question": "What does a router in a Link State protocol (such as OSPF) flood across the network when an interface link fails?",
                "options": [
                    {"id": "opt-1", "text": "Its entire routing table containing all global routes."},
                    {"id": "opt-2", "text": "A Link State Advertisement (LSA) detailing only the changed link status."},
                    {"id": "opt-3", "text": "A DHCP Discover broadcast packet."},
                    {"id": "opt-4", "text": "An ARP reply with an empty MAC address."}
                ],
                "correctOptionIds": ["opt-2"],
                "explanation": "Link State routers do not broadcast entire routing tables. They flood only Link State Advertisements (LSAs) containing the updated status and metric of their direct interfaces."
            },
            {
                "id": "q-l06-10",
                "difficulty": "medium",
                "type": "single_choice",
                "question": "In the 8-node MinHeap Dijkstra trace starting at router A, router A has direct links to B (cost 2) and E (cost 6), while B has a link to E (cost 3). What happens when router B is expanded?",
                "options": [
                    {"id": "opt-1", "text": "Path A -> B -> E (cost 5) beats direct link A -> E (cost 6), updating dist[E] to 5 and pushing (5, E) to the heap."},
                    {"id": "opt-2", "text": "The path is rejected because direct links always take precedence over multi-hop paths."},
                    {"id": "opt-3", "text": "The heap overflows and resets dist[E] to infinity."},
                    {"id": "opt-4", "text": "Router B is placed in a blocking state by STP."}
                ],
                "correctOptionIds": ["opt-1"],
                "explanation": "When B is popped at distance 2, it evaluates B -> E (cost 3): 2 + 3 = 5 < 6. It updates dist[E] = 5 and pushes (5, E). The older entry (6, E) remains in the heap as a stale entry to be discarded later."
            },
            {
                "id": "q-l06-11",
                "difficulty": "medium",
                "type": "single_choice",
                "question": "In an optimized MinHeap implementation of Dijkstra, how are stale heap entries (elements pushed before a shorter route was discovered) handled when popped?",
                "options": [
                    {"id": "opt-1", "text": "The algorithm crashes with a runtime KeyError."},
                    {"id": "opt-2", "text": "If the popped cost is strictly greater than dist[node], the entry is immediately discarded without evaluating neighbors."},
                    {"id": "opt-3", "text": "All previously finalized shortest paths are recalculated from scratch."},
                    {"id": "opt-4", "text": "The algorithm replaces the popped cost with zero."}
                ],
                "correctOptionIds": ["opt-2"],
                "explanation": "Because binary heaps do not support efficient decrease-key without indexed arrays, algorithms push new pairs. When popping (cost, u), if cost > dist[u], it is recognized as stale and skipped."
            },
            {
                "id": "q-l06-12",
                "difficulty": "medium",
                "type": "single_choice",
                "question": "What is the time complexity of the Bellman-Ford algorithm on a network graph with V vertices and E edges?",
                "options": [
                    {"id": "opt-1", "text": "O((V + E) log V)"},
                    {"id": "opt-2", "text": "O(V * E)"},
                    {"id": "opt-3", "text": "O(V + E)"},
                    {"id": "opt-4", "text": "O(1)"}
                ],
                "correctOptionIds": ["opt-2"],
                "explanation": "Bellman-Ford executes V - 1 outer iterations, each relaxing all E edges in the graph. Hence, its worst-case time complexity is O(V * E)."
            },
            {
                "id": "q-l06-13",
                "difficulty": "medium",
                "type": "multiple_choice",
                "question": "Which of the following statements correctly highlight architectural advantages of Link State protocols (OSPF) over Distance Vector protocols (RIP)?",
                "options": [
                    {"id": "opt-1", "text": "Link State routers possess a complete synchronized map of the global network topology."},
                    {"id": "opt-2", "text": "Link State protocols converge significantly faster when topology changes occur."},
                    {"id": "opt-3", "text": "Link State protocols are completely immune to the Count-to-Infinity problem."},
                    {"id": "opt-4", "text": "Link State protocols consume less router CPU and memory than Distance Vector protocols."}
                ],
                "correctOptionIds": ["opt-1", "opt-2", "opt-3"],
                "explanation": "Link State protocols have full topology visibility, converge in milliseconds, and avoid Count-to-Infinity. However, they consume MORE CPU and memory (running Dijkstra on full LSDB) than Distance Vector (option 4 is false)."
            },
            {
                "id": "q-l06-14",
                "difficulty": "medium",
                "type": "single_choice",
                "question": "How does Prim's algorithm choose which edge to add next when constructing a Minimum Spanning Tree from a growing tree of visited nodes?",
                "options": [
                    {"id": "opt-1", "text": "It randomly picks an edge between any two unvisited nodes."},
                    {"id": "opt-2", "text": "It greedily selects the minimum-weight edge connecting any visited node to an unvisited node."},
                    {"id": "opt-3", "text": "It selects the edge with the highest latency to maximize link buffer space."},
                    {"id": "opt-4", "text": "It selects edges in alphabetical order by vertex name."}
                ],
                "correctOptionIds": ["opt-2"],
                "explanation": "Prim's algorithm maintains a cut between visited and unvisited vertices. At each step, it greedily crosses the cut by adding the cheapest edge connecting a visited node to an unvisited node."
            },
            {
                "id": "q-l06-15",
                "difficulty": "medium",
                "type": "single_choice",
                "question": "In the Border Gateway Protocol (BGP-4), how does the Path-Vector mechanism prevent inter-domain routing loops between Autonomous Systems?",
                "options": [
                    {"id": "opt-1", "text": "By capping the maximum hop count at 15."},
                    {"id": "opt-2", "text": "By prepending its own AS number to the AS-PATH attribute and dropping any incoming route that already contains its own AS number."},
                    {"id": "opt-3", "text": "By running Dijkstra's algorithm across all world routers simultaneously."},
                    {"id": "opt-4", "text": "By converting all IPv4 packets to IPv6 before transmission."}
                ],
                "correctOptionIds": ["opt-2"],
                "explanation": "BGP is a Path-Vector protocol. As routes transit ASes, each AS prepends its AS number to the AS-PATH attribute. If a router receives an advertisement containing its own AS number, a loop is detected and the route is rejected."
            },
            {
                "id": "q-l06-16",
                "difficulty": "medium",
                "type": "multiple_choice",
                "question": "Which of the following techniques are commonly deployed in Distance Vector routing protocols to mitigate transient loops and the Count-to-Infinity problem?",
                "options": [
                    {"id": "opt-1", "text": "Split Horizon (never advertise a route back out the interface it was learned from)"},
                    {"id": "opt-2", "text": "Poison Reverse (advertise failed routes back to the neighbor with an infinite metric of 16)"},
                    {"id": "opt-3", "text": "Hold-Down Timers (refuse new updates for a route that just failed for a period of time)"},
                    {"id": "opt-4", "text": "Path MTU Discovery (PMTUD)"}
                ],
                "correctOptionIds": ["opt-1", "opt-2", "opt-3"],
                "explanation": "Split Horizon, Poison Reverse, and Hold-Down Timers are the standard loop-mitigation mechanisms in Distance Vector routing. PMTUD is an IP packet sizing mechanism, not a loop prevention tool."
            },
            {
                "id": "q-l06-17",
                "difficulty": "medium",
                "type": "single_choice",
                "question": "What is the primary difference in operational scope between an Interior Gateway Protocol (IGP) and an Exterior Gateway Protocol (EGP)?",
                "options": [
                    {"id": "opt-1", "text": "IGPs run inside a single Autonomous System; EGPs (like BGP) route traffic between different Autonomous Systems across the public Internet."},
                    {"id": "opt-2", "text": "IGPs only support wireless WiFi; EGPs only support fiber optic cables."},
                    {"id": "opt-3", "text": "IGPs run at Layer 2; EGPs run at Layer 7."},
                    {"id": "opt-4", "text": "IGPs are proprietary to Cisco; EGPs are open standard."}
                ],
                "correctOptionIds": ["opt-1"],
                "explanation": "IGPs (OSPF, IS-IS, RIP) optimize routing inside a single administrative domain (Autonomous System). EGPs (BGP-4) manage routing policies between autonomous systems globally."
            },
            {
                "id": "q-l06-18",
                "difficulty": "medium",
                "type": "single_choice",
                "question": "Consider a graph with edges: (A, B, 3), (B, C, -5), (A, C, 2). Starting from source A, what are the final shortest-path distances computed by Bellman-Ford?",
                "options": [
                    {"id": "opt-1", "text": "dist[A] = 0, dist[B] = 3, dist[C] = 2"},
                    {"id": "opt-2", "text": "dist[A] = 0, dist[B] = 3, dist[C] = -2"},
                    {"id": "opt-3", "text": "dist[A] = 0, dist[B] = -5, dist[C] = -2"},
                    {"id": "opt-4", "text": "Negative cycle error is thrown"}
                ],
                "correctOptionIds": ["opt-2"],
                "explanation": "From A: dist[A] = 0. Edge (A, B, 3) gives dist[B] = 3. Edge (A, C, 2) initially gives dist[C] = 2. Relaxing (B, C, -5) gives dist[C] = min(2, 3 + (-5)) = -2. Path A -> B -> C (cost -2) beats direct link A -> C (cost 2). Final: A:0, B:3, C:-2."
            },
            {
                "id": "q-l06-19",
                "difficulty": "hard",
                "type": "single_choice",
                "question": "In the 8-node MinHeap trace (source A), why does router C receive its final shortest path from D (cost 3 + 6 = 9) rather than from B (cost 2 + 9 = 11)?",
                "options": [
                    {"id": "opt-1", "text": "Because edge D -> C has a lower weight (6) than edge B -> C (9), and total path A -> D -> C (9) beats A -> B -> C (11)."},
                    {"id": "opt-2", "text": "Because B was marked offline by an LSA update."},
                    {"id": "opt-3", "text": "Because router D has a lower MAC address than router B."},
                    {"id": "opt-4", "text": "Because D is closer alphabetically to C."}
                ],
                "correctOptionIds": ["opt-1"],
                "explanation": "Path A -> B -> C has cost 2 + 9 = 11. When D is popped at cost 3, relaxing edge D -> C (weight 6) yields 3 + 6 = 9 < 11. The distance to C is updated to 9, beating the path via B."
            },
            {
                "id": "q-l06-20",
                "difficulty": "hard",
                "type": "single_choice",
                "question": "A network graph has 4 vertices with a directed cycle: A -> B (cost 2), B -> C (cost -6), C -> A (cost 3). What occurs when Bellman-Ford runs with source A?",
                "options": [
                    {"id": "opt-1", "text": "It computes dist[A] = 0, dist[B] = 2, dist[C] = -4."},
                    {"id": "opt-2", "text": "Cycle cost is 2 + (-6) + 3 = -1 (< 0). On the 4th (V-th) pass, distances continue decreasing, triggering a negative cycle exception."},
                    {"id": "opt-3", "text": "Dijkstra is invoked automatically as a fallback."},
                    {"id": "opt-4", "text": "All edge weights are converted to absolute values."}
                ],
                "correctOptionIds": ["opt-2"],
                "explanation": "The sum of edge weights in cycle A -> B -> C -> A is 2 - 6 + 3 = -1. Because this is negative, traversing the cycle infinitely decreases path costs. On the V-th (4th) pass, relaxation succeeds again, detecting the negative cycle."
            },
            {
                "id": "q-l06-21",
                "difficulty": "hard",
                "type": "multiple_choice",
                "question": "Why can an Internet Autonomous System NOT scale by running a single unified Link State protocol (like OSPF) across the entire global Internet?",
                "options": [
                    {"id": "opt-1", "text": "The global Link State Database (LSDB) would contain millions of routers, consuming tens of gigabytes of RAM on every router."},
                    {"id": "opt-2", "text": "Flooding LSAs globally every time a residential fiber cable is cut would saturate core Internet transit links with update traffic."},
                    {"id": "opt-3", "text": "Independent ISPs refuse to reveal internal proprietary network topologies and link metrics to commercial competitors."},
                    {"id": "opt-4", "text": "Dijkstra's algorithm cannot run on 64-bit CPU architectures."}
                ],
                "correctOptionIds": ["opt-1", "opt-2", "opt-3"],
                "explanation": "Global OSPF would fail due to LSDB memory explosion, global LSA flooding overhead, and business confidentiality (ISPs will not disclose internal topology to rivals). Dijkstra runs fine on 64-bit CPUs."
            },
            {
                "id": "q-l06-22",
                "difficulty": "hard",
                "type": "single_choice",
                "question": "What is the early termination optimization in the Bellman-Ford algorithm that allows it to finish in O(E) time under best-case scenarios?",
                "options": [
                    {"id": "opt-1", "text": "If a full pass over all E edges results in zero distance updates, terminate immediately because the paths have converged."},
                    {"id": "opt-2", "text": "Stop after expanding the node with the highest IP address."},
                    {"id": "opt-3", "text": "Skip all edges with even weights."},
                    {"id": "opt-4", "text": "Convert all negative edges to zero."}
                ],
                "correctOptionIds": ["opt-1"],
                "explanation": "If an entire iteration over all E edges produces no updates to any dist[v], no further passes will produce updates either. The algorithm can break early, achieving O(E) time for simple topologies."
            },
            {
                "id": "q-l06-23",
                "difficulty": "hard",
                "type": "single_choice",
                "question": "Suppose an undirected network graph has multiple edges with identical weights. Which statement regarding its Minimum Spanning Tree (MST) is strictly true?",
                "options": [
                    {"id": "opt-1", "text": "The graph cannot have any Spanning Tree."},
                    {"id": "opt-2", "text": "The Minimum Spanning Tree may not be unique, but the minimum total weight sum of all valid MSTs is always identical."},
                    {"id": "opt-3", "text": "Prim's algorithm will throw an infinite loop exception."},
                    {"id": "opt-4", "text": "The number of edges in the MST will exceed V - 1."}
                ],
                "correctOptionIds": ["opt-2"],
                "explanation": "When edge weights are not strictly unique, multiple distinct MST edge sets may exist, but all valid Minimum Spanning Trees have the exact same minimum total weight sum and contain exactly V - 1 edges."
            },
            {
                "id": "q-l06-24",
                "difficulty": "hard",
                "type": "single_choice",
                "question": "How does BGP enforce policy-based routing rather than purely shortest-path routing between Autonomous Systems?",
                "options": [
                    {"id": "opt-1", "text": "By evaluating BGP attributes (such as LOCAL_PREF, AS-PATH length, Origin, and MED) in a strict policy decision hierarchy before considering cost."},
                    {"id": "opt-2", "text": "By randomly flipping coins at border routers."},
                    {"id": "opt-3", "text": "By executing BFS hop count exclusively."},
                    {"id": "opt-4", "text": "By blocking all incoming TCP port 179 packets."}
                ],
                "correctOptionIds": ["opt-1"],
                "explanation": "BGP chooses routes based on administrative and economic policies using a defined attribute hierarchy (highest LOCAL_PREF first, shortest AS-PATH second, origin code third, lowest MED fourth) rather than raw physical link latency."
            },
            {
                "id": "q-l06-25",
                "difficulty": "hard",
                "type": "multiple_choice",
                "question": "Which of the following conditions must hold true for Dijkstra's algorithm to compute the mathematically correct shortest path across all nodes in a network?",
                "options": [
                    {"id": "opt-1", "text": "All edge weights in the graph must be non-negative (w(e) >= 0)."},
                    {"id": "opt-2", "text": "The graph must be a connected or weakly-connected component for reachable vertices."},
                    {"id": "opt-3", "text": "The graph must not contain any undirected edges."},
                    {"id": "opt-4", "text": "The priority queue must correctly extract the element with the minimum tentative distance."}
                ],
                "correctOptionIds": ["opt-1", "opt-2", "opt-4"],
                "explanation": "Dijkstra requires non-negative edge weights, connectivity to reach targets, and a valid priority queue extracting minimum distances. It works perfectly on undirected graphs by treating each undirected link as two bidirectional directed edges (option 3 is false)."
            }
        ]
    }
}
