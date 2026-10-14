"""
Data module for Term 5 Lecture 05:
Graph Theory in Networking — BFS, DFS, Adjacency Models & Cycle Detection
Strictly 0 occurrences of forbidden instructor names.
"""

L5_DATA = {
    "schema_version": 1,
    "note_id": "cn-t5-l05",
    "term": "Term 5",
    "subject_code": "CN",
    "topic_title": "Graph Theory in Networking - BFS, DFS, Adjacency Models & Cycle Detection",
    "tags": [
        "Networking",
        "Graph Theory",
        "BFS",
        "DFS",
        "Adjacency List",
        "Adjacency Matrix",
        "Cycle Detection",
        "Broadcast Storm",
        "STP",
        "Hop Count"
    ],
    "learning_objectives": [
        "Model complex network topologies as weighted graphs G = (V, E) with propagation delay, inverse bandwidth, and administrative link costs.",
        "Contrast Adjacency List (O(V+E) space) and Adjacency Matrix (O(V^2) space) representations, explaining why the sparse Internet topology mandates adjacency lists.",
        "Implement and trace Breadth-First Search (BFS) using FIFO queues to discover minimum-hop paths and reconstruct routes via parent pointers.",
        "Analyze the fundamental architectural limitation of BFS (hop-count minimization vs. latency/bandwidth minimization) and recognize when Dijkstra is required.",
        "Implement Depth-First Search (DFS) with recursion and explicit stacks for complete network topology discovery.",
        "Dissect the canonical parent-pointer cycle detection algorithm and explain why Layer 2 Ethernet loops cause catastrophic broadcast storms without Spanning Tree Protocol (STP)."
    ],
    "summary": "An exhaustive, rigorous masterclass in graph theory fundamentals applied to computer networks. Explores graph mathematical modeling G = (V, E), sparse internet topology vs. dense matrix representations, Breadth-First Search (BFS) hop-count pathfinding and path reconstruction, Depth-First Search (DFS) topology exploration, the canonical Layer 2 cycle detection algorithm, and Spanning Tree Protocol (STP / 802.1D) broadcast storm elimination.",
    "key_takeaways": [
        "Networks are formally modeled as weighted graphs G = (V, E) where routers/switches are vertices V, communication cables/channels are edges E, and edge weights represent propagation delay, financial metrics, or inverse bandwidth.",
        "Because real-world network router topologies are sparse (average node degree between 2 and 10), the Adjacency List is asymptotically superior to the Adjacency Matrix, requiring O(V+E) space versus O(V^2) and enabling rapid neighbor iteration.",
        "BFS guarantees the shortest path exclusively in terms of hop count (number of intermediate links) using a FIFO queue in O(V+E) time, tracking parent pointers for path reconstruction.",
        "The critical limitation of BFS in production networks is that hop count does not correlate with transmission speed or delay; a 1-hop satellite link (500ms) will be chosen by BFS over a 3-hop terrestrial fiber route (15ms). Cost-based routing requires Dijkstra.",
        "Layer 2 Ethernet frames lack a Time to Live (TTL) field. Consequently, a physical loop in a switched Ethernet topology causes broadcast frames to multiply and circulate infinitely, triggering a broadcast storm that saturates switch CPUs and crashes the LAN.",
        "Cycle detection using DFS tracking parent pointers (if neighbor is visited and neighbor != parent -> loop exists) is the algorithmic foundation for Layer 2 loop elimination via Spanning Tree Protocol (STP / 802.1D)."
    ],
    "last_updated": "2026-10-13T00:00:00Z",
    "approval_status": "approved",
    "sections": [
        {
            "section_id": "sec-l05-01",
            "heading": "Modeling Computer Networks as Weighted Graphs",
            "body": "### The Graph Abstraction of Communications Topologies\n\nAt its mathematical foundation, the global Internet is a massive, decentralized graph. Every design pattern, pathfinding mechanism, and fault-tolerance protocol in networking relies on graph theory.\n\nA network is formally modeled as a graph:\n$$G = (V, E)$$\nWhere:\n- **Vertices ($V$)**: Represent intermediate forwarding nodes (Layer 3 routers, Layer 2 switches) and terminal endpoints (servers, hosts).\n- **Edges ($E$)**: Represent bidirectional or unidirectional communication circuits (physical fiber optic cables, copper twisted-pair Ethernet, wireless radio frequency links, satellite transponders).\n\n```\n                                [Delhi]\n                               /   5   \\\n                              /         \\ 2\n                             /     3     \\\n                         [Mumbai] ───── [Hyderabad]\n                             \\               \\\n                              \\ 8             \\ 2\n                               \\               \\\n                               [Chennai] ───── [Bangalore]\n                                          4\n```\n\n### Edge Weight Formulations: What Does Link Cost Represent?\nIn pure graph theory, edge weights are abstract integers. In network engineering, an edge weight $W(u, v)$ encapsulates physical and operational properties:\n1. **Propagation Latency ($d_{\\text{prop}}$)**: Time required for a bit to transit the physical medium at the speed of light ($s \\approx 2 \\times 10^8\\text{ m/s}$ in optical glass). Longer geographical links incur higher weights.\n2. **Inverse Bandwidth (Link Capacity)**: High-speed backbones should be preferred over slow links. For instance, in Cisco OSPF:\n   $$\\text{Cost} = \\frac{\\text{Reference Bandwidth (100 Mbps)}}{\\text{Interface Bandwidth}}$$\n   A $10\\text{ Gbps}$ interface receives a cost of $1$, whereas a $10\\text{ Mbps}$ link receives a cost of $10$.\n3. **Financial Transit Cost & Peering Policies**: Autonomous Systems (AS) assign artificial high weights to transit links where they must pay upstream transit providers per gigabyte, while assigning zero or low cost to free settlement peering links.\n4. **Reliability & Bit Error Rate (BER)**: Unstable wireless links with frequent packet drops can be assigned higher metrics to discourage route selection under stable conditions.",
            "citations": [
                "Introduction to Algorithms (Cormen, Leiserson, Rivest, Stein), Chapter 22: Elementary Graph Algorithms",
                "Computer Networks: A Systems Approach, Chapter 3: Routing",
                "RFC 2328: OSPF Version 2, Section 1.3 (Routing with OSPF)"
            ]
        },
        {
            "section_id": "sec-l05-02",
            "heading": "Adjacency List vs. Adjacency Matrix in Sparse Internet Topologies",
            "body": "### Graph Storage Trade-Offs at Internet Scale\n\nTo compute routing tables, a router's control plane CPU must represent the network topology in RAM. The two primary programmatic representations are the **Adjacency Matrix** and the **Adjacency List**.\n\n#### 1. The Adjacency Matrix\nA 2D array $M$ of size $|V| \\times |V|$, where $M[u][v]$ stores the weight of the link between vertex $u$ and vertex $v$ (or $\\infty$ if no direct link exists):\n\n```\n               Delhi     Mumbai   Hyderabad   Bangalore   Chennai\n  Delhi     [    0,        5,         2,          ∞,         8    ]\n  Mumbai    [    5,        0,         3,          ∞,         ∞    ]\n  Hyderabad [    2,        3,         0,          2,         ∞    ]\n  Bangalore [    ∞,        ∞,         2,          0,         4    ]\n  Chennai   [    8,        ∞,         ∞,          4,         0    ]\n```\n\n- **Space Complexity**: $\\Theta(|V|^2)$, completely independent of the number of edges $|E|$.\n- **Edge Existence Lookup**: $\\Theta(1)$ instantaneous array indexing.\n- **Iterating All Neighbors of a Node**: $\\Theta(|V|)$ operations (must scan entire row, checking for non-infinity values).\n\n#### 2. The Adjacency List\nAn associative array or hash map where each vertex $u$ maps to a dynamic list of tuples `(neighbor, weight)` representing only direct, active connections:\n\n```python\nnetwork_graph = {\n    'Delhi':     [('Mumbai', 5), ('Hyderabad', 2), ('Chennai', 8)],\n    'Mumbai':    [('Delhi', 5), ('Hyderabad', 3)],\n    'Hyderabad': [('Delhi', 2), ('Mumbai', 3), ('Bangalore', 2)],\n    'Bangalore': [('Hyderabad', 2), ('Chennai', 4)],\n    'Chennai':   [('Delhi', 8), ('Bangalore', 4)]\n}\n```\n\n- **Space Complexity**: $\\Theta(|V| + |E|)$.\n- **Iterating All Neighbors of Node $u$**: $\\Theta(\\text{deg}(u))$, where $\\text{deg}(u)$ is the degree (number of links) of node $u$.\n\n### Why the Internet Demands Adjacency Lists\n\n> [!IMPORTANT]\n> **The Sparsity of Communications Topologies**: Real-world communication networks are fundamentally **sparse graphs** ($|E| \\ll |V|^2$). A core router in an ISP typically has between $4$ and $16$ high-speed line cards, not $100,000$.\n\nConsider an Autonomous System topology with $|V| = 50,000$ routers:\n- **Adjacency Matrix Memory Footprint**:\n  $$50,000 \\times 50,000 = 2,500,000,000 \\text{ elements} \\times 4\\text{ bytes} = \\mathbf{10\\text{ Gigabytes of RAM}}$$\n  Scanning neighbors during SPF recalculation requires iterating through $50,000$ elements for every single node.\n- **Adjacency List Memory Footprint** (assuming average degree $\\text{deg}(u) = 8 \\implies |E| = 200,000$ edges):\n  $$50,000 \\text{ pointers} + 400,000 \\text{ edge records} \\approx \\mathbf{4.8\\text{ Megabytes of RAM}}$$\n\nBecause router memory and convergence speed are critical, routing protocols (such as OSPF and IS-IS) model topologies exclusively using adjacency lists.",
            "citations": [
                "Algorithms, 4th Edition (Robert Sedgewick & Kevin Wayne), Chapter 4: Graphs",
                "RFC 2328: OSPF Version 2, Appendix C (Configurable Constants)"
            ]
        },
        {
            "section_id": "sec-l05-03",
            "heading": "Breadth-First Search (BFS) & Minimum-Hop Path Reconstruction",
            "body": "### Discovering Routes Layer-by-Layer\n\nBreadth-First Search (BFS) is the fundamental graph traversal algorithm for discovering the **minimum-hop path** from a designated source vertex to all reachable destinations.\n\n### Core Invariants of BFS\n1. **Queue Discipline (FIFO)**: Explores vertices in strictly increasing order of their distance (hop count) from the source.\n2. **Visited Guard Set**: Prevents infinite loops and redundant reprocessing by marking nodes when they are first discovered.\n3. **Hop Minimization**: Guarantees that the first time vertex $v$ is dequeued from the queue, the path discovered from source $s$ to $v$ contains the absolute minimum number of intermediate edges.\n\n```python\nfrom collections import deque\nfrom typing import Dict, List, Tuple, Optional\n\ndef bfs_shortest_hop_path(graph: Dict[str, List[Tuple[str, int]]], start: str, target: str) -> Optional[List[str]]:\n    \"\"\"\n    Computes the path with the minimum number of link hops between start and target.\n    Maintains a parent pointer dictionary to reconstruct the route.\n    \"\"\"\n    visited = {start}\n    queue = deque([start])\n    parent = {start: None}\n    \n    while queue:\n        curr = queue.popleft()\n        \n        if curr == target:\n            # Reconstruct path from target back to start via parent pointers\n            path = []\n            node = target\n            while node is not None:\n                path.append(node)\n                node = parent[node]\n            return list(reversed(path))\n            \n        for neighbor, _ in graph.get(curr, []):\n            if neighbor not in visited:\n                visited.add(neighbor)\n                parent[neighbor] = curr\n                queue.append(neighbor)\n                \n    return None  # Target unreachable\n```\n\n### Step-by-Step Execution Trace: Mumbai to Bangalore\n\nLet us trace `bfs_shortest_hop_path` on our 5-city topology to route from **Mumbai** to **Bangalore**:\n\n```\nInitial State:\n  Queue = [Mumbai]\n  Visited = {Mumbai}\n  Parent = {Mumbai: None}\n\nStep 1: Pop Mumbai\n  Neighbors of Mumbai: Delhi, Hyderabad\n  Add Delhi: Visited={Mumbai, Delhi}, Parent[Delhi]=Mumbai, Queue=[Delhi]\n  Add Hyderabad: Visited={Mumbai, Delhi, Hyderabad}, Parent[Hyderabad]=Mumbai, Queue=[Delhi, Hyderabad]\n\nStep 2: Pop Delhi (Distance = 1 hop)\n  Neighbors of Delhi: Mumbai (visited), Hyderabad (visited), Chennai (unvisited)\n  Add Chennai: Visited={..., Chennai}, Parent[Chennai]=Delhi, Queue=[Hyderabad, Chennai]\n\nStep 3: Pop Hyderabad (Distance = 1 hop)\n  Neighbors of Hyderabad: Delhi (visited), Mumbai (visited), Bangalore (unvisited)\n  Add Bangalore: Visited={..., Bangalore}, Parent[Bangalore]=Hyderabad, Queue=[Chennai, Bangalore]\n\nStep 4: Pop Chennai (Distance = 2 hops)\n  Neighbors of Chennai: Delhi (visited), Bangalore (already visited/queued)\n\nStep 5: Pop Bangalore (Distance = 2 hops)\n  Target 'Bangalore' reached!\n  Reconstruct path: Bangalore -> Parent[Bangalore]=Hyderabad -> Parent[Hyderabad]=Mumbai -> None\n  Final Reconstructed Route: Mumbai -> Hyderabad -> Bangalore (2 hops)\n```",
            "citations": [
                "Introduction to Algorithms, Chapter 22.2: Breadth-first search",
                "Computer Networks (Andrew S. Tanenbaum & David J. Wetherall), Chapter 5: The Network Layer"
            ]
        },
        {
            "section_id": "sec-l05-04",
            "heading": "The Fundamental Architectural Limitation of Hop-Based Routing & Dijkstra's Algorithm",
            "body": "### The Fatal Flaw of Hop Minimization\n\nWhile BFS provides an elegant, optimal solution for minimizing edge counts, **hop count is a disastrous metric for real-world production networks**.\n\nConsider the following real-world scenario:\n\n```\n                                  Satellite Link\n                         [Router A] ──────────────► [Router B]\n                              │       1 Hop (500ms)      ▲\n                              │                          │\n                              │ 3 Hops                   │\n                              │ Terrestrial Fiber        │\n                              ▼ (5ms each = 15ms total)  │\n                         [Router C] ──► [Router D] ──────┘\n```\n\n- **Route 1 (Satellite)**: $A \\to B$. Hop count: **1 hop**. Total delay: **$500\\text{ ms}$**.\n- **Route 2 (Terrestrial Fiber)**: $A \\to C \\to D \\to B$. Hop count: **3 hops**. Total delay: **$15\\text{ ms}$**.\n\n#### What Does BFS Choose?\nBecause BFS minimizes the number of edges, it chooses the **1-hop Satellite path** ($500\\text{ ms}$ latency), completely ignoring the fact that the 3-hop fiber path is **33 times faster**!\n\n### Historical Legacy: RIP Hop Count Ceiling\nThe original **Routing Information Protocol (RIP / RFC 1058)** used pure hop count as its metric, derived directly from Bellman-Ford/BFS principles. This led to notorious operational problems:\n1. **High-Speed Link Bypass**: A $10\\text{ Mbps}$ Ethernet link of 1 hop was preferred over a $10\\text{ Gbps}$ fiber path of 2 hops.\n2. **The 15-Hop Diameter Limit**: To contain the count-to-infinity problem, RIP defined $16$ as infinity (unreachable). Consequently, RIP cannot be deployed on any network with a diameter greater than 15 routers.\n\nFor enterprise and internet-scale routing, hop-count algorithms were superseded by cost-based link-state routing (**Dijkstra's Algorithm in OSPF/IS-IS**).\n\n---\n\n### Dijkstra's Shortest Path First (SPF) Algorithm\n\nTo solve the fundamental failure of unweighted BFS, modern Interior Gateway Protocols (such as OSPF and IS-IS) deploy **Dijkstra's Algorithm** to compute the **minimum cumulative cost path** from a source router to all reachable destinations in the network.\n\n#### Key Architectural Properties\n- **Data Structure**: Min-Priority Queue (**MinHeap**) storing tuples of `(distance, node)`.\n- **Greedy Invariant**: At each step, Dijkstra extracts the unfinished node with the absolute lowest tentative distance and finalizes its shortest path.\n- **Weight Constraint**: Requires **strictly non-negative edge weights** ($w(e) \\ge 0$).\n- **Time Complexity**: $O((|V| + |E|) \\log |V|)$ using a binary min-heap.\n\n### Production Python Implementation\n\n```python\nimport heapq\nfrom typing import Dict, List, Tuple, Optional\n\ndef dijkstra(graph: Dict[str, List[Tuple[str, int]]], source: str) -> Tuple[Dict[str, float], Dict[str, Optional[str]]]:\n    \"\"\"\n    Computes minimum cost paths from source to all nodes using a binary min-heap.\n    Returns:\n      dist: Mapping of node -> shortest distance metric\n      prev: Mapping of node -> predecessor pointer for route reconstruction\n    \"\"\"\n    # Step 1: Initialize all distances to infinity\n    dist = {node: float('inf') for node in graph}\n    dist[source] = 0\n    prev = {node: None for node in graph}\n    \n    # Min-heap stores (tentative_cost, node)\n    pq = [(0, source)]\n    \n    while pq:\n        cost, node = heapq.heappop(pq)\n        \n        # Skip stale entries if a cheaper path was already finalized\n        if cost > dist[node]:\n            continue\n            \n        # Relax all outgoing edges\n        for neighbor, weight in graph.get(node, []):\n            new_cost = cost + weight\n            if new_cost < dist[neighbor]:\n                dist[neighbor] = new_cost\n                prev[neighbor] = node\n                heapq.heappush(pq, (new_cost, neighbor))\n                \n    return dist, prev\n\ndef reconstruct_path(prev: Dict[str, Optional[str]], target: str) -> List[str]:\n    \"\"\"Reconstructs the optimal shortest path hop-by-hop from target back to source.\"\"\"\n    path = []\n    node = target\n    while node is not None:\n        path.append(node)\n        node = prev[node]\n    return list(reversed(path))\n```\n\n### Dijkstra Execution Trace: Mumbai to All Destination Cities\n\nApplying Dijkstra on our 5-city network topology with source **Mumbai**:\n\n```python\nnetwork_graph = {\n    'Delhi':     [('Mumbai', 5), ('Hyderabad', 2), ('Chennai', 8)],\n    'Mumbai':    [('Delhi', 5), ('Hyderabad', 3)],\n    'Hyderabad': [('Delhi', 2), ('Mumbai', 3), ('Bangalore', 2)],\n    'Bangalore': [('Hyderabad', 2), ('Chennai', 4)],\n    'Chennai':   [('Delhi', 8), ('Bangalore', 4)]\n}\n```\n\n| Step | Expanded Node | dist[Mumbai] | dist[Delhi] | dist[Hyderabad] | dist[Chennai] | dist[Bangalore] |\n| :--- | :--- | :--- | :--- | :--- | :--- | :--- |\n| **Init** | — | **0** | $\\infty$ | $\\infty$ | $\\infty$ | $\\infty$ |\n| **1** | **Mumbai** | **0** | 5 | 3 | $\\infty$ | $\\infty$ |\n| **2** | **Hyderabad** | **0** | 5 | **3** | $\\infty$ | 5 |\n| **3** | **Delhi** | **0** | **5** | **3** | 13 | 5 |\n| **4** | **Bangalore** | **0** | **5** | **3** | 9 | **5** |\n| **5** | **Chennai** | **0** | **5** | **3** | **9** | **5** |\n\n#### Final Routing Table Computed from Mumbai:\n- **Mumbai $\\to$ Delhi**: Minimum Cost **5** (Direct link: `Mumbai -> Delhi`)\n- **Mumbai $\\to$ Hyderabad**: Minimum Cost **3** (Direct link: `Mumbai -> Hyderabad`)\n- **Mumbai $\\to$ Bangalore**: Minimum Cost **5** (`Mumbai -> Hyderabad -> Bangalore`)\n- **Mumbai $\\to$ Chennai**: Minimum Cost **9** (`Mumbai -> Hyderabad -> Bangalore -> Chennai`)\n\n### Comprehensive Algorithm Comparison: BFS vs. DFS vs. Dijkstra\n\n| Algorithmic Dimension | Breadth-First Search (BFS) | Depth-First Search (DFS) | Dijkstra's Algorithm |\n| :--- | :--- | :--- | :--- |\n| **Primary Data Structure** | Queue (FIFO) | Stack / System Recursion | Priority Queue (MinHeap) |\n| **Optimization Goal** | Minimum hop count (unweighted) | Any path / Deep exploration | Minimum cumulative metric cost |\n| **Asymptotic Complexity** | $O(|V| + |E|)$ | $O(|V| + |E|)$ | $O((|V| + |E|) \\log |V|)$ |\n| **Weighted Graphs** | No (ignores weights, treats all as 1) | No (ignores weights) | **Yes** (accumulates weights) |\n| **Negative Edge Weights** | Not applicable | Not applicable | **No** (fails on negative links) |\n| **Operational Protocol** | **RIP** (hop-count vectors) | **STP** (cycle detection) | **OSPF, IS-IS** (link-state SPF) |",
            "citations": [
                "RFC 1058: Routing Information Protocol",
                "RFC 2453: RIP Version 2",
                "RFC 2328: OSPF Version 2, Section 16 (Calculation of the Routing Table)",
                "Introduction to Algorithms (Cormen et al.), Chapter 24.3: Dijkstra's Algorithm",
                "Computer Networks: A Systems Approach, Chapter 3.3: Routing Algorithms"
            ]
        },
        {
            "section_id": "sec-l05-05",
            "heading": "Depth-First Search (DFS) & Topological Exploration",
            "body": "### Deep Branch Exploration & Recursion Mechanics\n\nDepth-First Search (DFS) explores a graph by traversing as deeply as possible along each branch before backtracking. Unlike BFS (which discovers shortest paths in concentric circles), DFS is designed for **exhaustive topological exploration**:\n- Finding connected components.\n- Topological sorting of dependency networks.\n- Spanning tree generation.\n- **Cycle and loop detection** in physical topologies.\n\n### Recursive vs. Iterative Implementations\n\n```python\ndef dfs_recursive(graph: dict, node: str, visited: set = None) -> list:\n    if visited is None:\n        visited = set()\n    visited.add(node)\n    traversal = [node]\n    \n    for neighbor, _ in graph.get(node, []):\n        if neighbor not in visited:\n            traversal.extend(dfs_recursive(graph, neighbor, visited))\n            \n    return traversal\n\ndef dfs_iterative(graph: dict, start: str) -> list:\n    \"\"\"Iterative DFS using an explicit LIFO Stack to prevent recursion depth overflow.\"\"\"\n    visited = set()\n    stack = [start]\n    traversal = []\n    \n    while stack:\n        curr = stack.pop()\n        if curr not in visited:\n            visited.add(curr)\n            traversal.append(curr)\n            # Push neighbors in reverse order to preserve canonical iteration\n            for neighbor, _ in reversed(graph.get(curr, [])):\n                if neighbor not in visited:\n                    stack.append(neighbor)\n                    \n    return traversal\n```\n\n### Complexity Comparison: BFS vs. DFS\n\n| Property | Breadth-First Search (BFS) | Depth-First Search (DFS) |\n| :--- | :--- | :--- |\n| **Underlying Data Structure** | Queue (FIFO) | Stack (LIFO) / Call Stack |\n| **Memory Footprint** | $O(|V|)$ (stores entire current frontier level) | $O(\\text{depth})$ (proportional to tree depth) |\n| **Time Complexity** | $\\Theta(|V| + |E|)$ | $\\Theta(|V| + |E|)$ |\n| **Path Guarantees** | Minimum hop-count shortest path | Any reachable path (not shortest) |\n| **Primary Network Roles** | Hop pathfinding, distance broadcasting | Cycle detection, topology maps, reachability verification |",
            "citations": [
                "Introduction to Algorithms, Chapter 22.3: Depth-first search",
                "The Design and Analysis of Computer Algorithms (Aho, Hopcroft, Ullman)"
            ]
        },
        {
            "section_id": "sec-l05-06",
            "heading": "Layer 2 Cycle Detection & Broadcast Storm Catastrophe",
            "body": "### Why Loops Are Fatal at Layer 2: The Missing TTL\n\nIn Layer 3 (IP), every packet contains a Time to Live (IPv4 TTL) or Hop Limit (IPv6) field. If a routing loop occurs, each router decrements the TTL by 1. When TTL reaches 0, the packet is discarded and an ICMP Time Exceeded message is generated.\n\n> [!CAUTION]\n> **The Ethernet Vulnerability**: Layer 2 Ethernet frames **do not have a TTL field**! Once an Ethernet frame enters a switched network, it has no native mechanism to expire.\n\nIf physical switches are wired in a loop (e.g., Switch A $\\leftrightarrow$ Switch B $\\leftrightarrow$ Switch C $\\leftrightarrow$ Switch A) for hardware redundancy, a catastrophic phenomenon occurs:\n\n```\n                                  Switch A\n                                 ┌─────────┐\n                        ┌───────►│ Broadcast│◄───────┐\n                        │        │ Copies  │        │\n                        │        └────┬────┘        │\n                        │             │             │\n                        │ Frame loops │ Frame loops │ Infinite\n                        │ clockwise   │ counter-CW  │ Replication\n                        │             ▼             │\n                   ┌────┴────┐                 ┌────┴────┐\n                   │ Switch B│────────────────►│ Switch C│\n                   └─────────┘                 └─────────┘\n```\n\n1. Host $X$ broadcasts an ARP request (`ff:ff:ff:ff:ff:ff`).\n2. Switch A floods the frame out all ports to Switch B and Switch C.\n3. Switch B and Switch C flood the frame out all ports back to each other and back to Switch A.\n4. The frame multiplies exponentially. Within hundreds of milliseconds, the network experiences a **Broadcast Storm**: link bandwidth hits $100\\%$, switch MAC forwarding tables thrash continuously (MAC flapping), and switch CPUs collapse.\n\n### The Canonical Parent-Pointer Cycle Detection Algorithm\n\nTo detect physical and logical cycles in an undirected topology, network software executes a modified DFS tracking the `parent` vertex from which each node was reached:\n\n```python\ndef is_cycle_present(graph: dict, curr: str, parent: Optional[str], visited: set) -> bool:\n    \"\"\"\n    Detects loops in an undirected network graph.\n    In an undirected link between u and v, returning to parent (the node we just arrived from)\n    is normal. But encountering ANY OTHER previously visited node confirms a CYCLE!\n    \"\"\"\n    visited.add(curr)\n    \n    for neighbor, _ in graph.get(curr, []):\n        if neighbor not in visited:\n            if is_cycle_present(graph, neighbor, curr, visited):\n                return True\n        elif neighbor != parent:\n            # The neighbor was already visited AND is NOT the parent we came from!\n            return True\n            \n    return False\n\n# Execution on enterprise topology:\nvisited = set()\nhas_loop = is_cycle_present(network_graph, curr=\"Mumbai\", parent=None, visited=visited)\nif has_loop:\n    print(\"CRITICAL: Layer 2 Loop Detected! Spanning Tree Protocol required.\")\n```\n\n### Network Remediation: Spanning Tree Protocol (STP / IEEE 802.1D)\nWhen `is_cycle_present` is true, switches run the distributed **Spanning Tree Protocol (STP)**:\n1. Elect a single **Root Bridge** (the switch with lowest Bridge ID).\n2. Calculate shortest paths from all switches to the Root Bridge.\n3. Transition redundant backup ports into an alternate/discarding (**Blocking**) state.\n4. Frames flow across a loop-free tree. If an active link is physically severed, the blocked port transitions to Forwarding within seconds, restoring redundancy without broadcast storms.",
            "citations": [
                "IEEE Std 802.1D-2004: IEEE Standard for Local and Metropolitan Area Networks: Media Access Control (MAC) Bridges",
                "Interconnections: Bridges, Routers, Switches, and Internetworking Protocols (Radia Perlman), Chapter 3: Spanning Tree Algorithm"
            ]
        },
        {
            "section_id": "sec-l05-07",
            "heading": "Mapping Graph Algorithms to Internet Protocols (BFS, DFS, Dijkstra, STP)",
            "body": "### From Academic Graph Theory to Production Internet Architecture\n\nThe fundamental graph algorithms studied in computer science form the exact algorithmic core of modern networking protocols:\n\n```\n      GRAPH ALGORITHM                      INTERNET PROTOCOL EQUIVALENT\n   ─────────────────────                  ──────────────────────────────\n   Breadth-First Search (BFS)   ══════►   RIP (Routing Information Protocol)\n   Depth-First Search (DFS)     ══════►   STP Loop Detection & Topology Auditing\n   Dijkstra's Algorithm         ══════►   OSPF / IS-IS (Link State Routing)\n   Bellman-Ford Algorithm       ══════►   BGP / Distance Vector Routing\n   Minimum Spanning Tree (MST)  ══════►   IEEE 802.1D Spanning Tree Protocol\n```\n\n### Comprehensive Protocol Architecture Taxonomy\n\n| Graph Algorithm | Protocol Name | Operational Tier | Algorithmic Mechanism in Protocol |\n| :--- | :--- | :--- | :--- |\n| **BFS** (Hop count) | **RIPv1 / RIPv2** | Layer 3 (Interior Routing) | Discovers shortest path by minimizing total hop count. Advertises vectors every $30$ seconds. Maximum metric capped at $15$ hops. |\n| **DFS** (Loop detection) | **STP Engine / Network Audit** | Layer 2 (Switching Fabric) | Analyzes network adjacency state to identify cycles and compute non-cyclic active forwarding graphs. |\n| **Dijkstra** (Least Cost) | **OSPFv2 / OSPFv3 / IS-IS** | Layer 3 (Interior Routing) | Routers flood Link State Advertisements (LSAs) so every router builds an identical Link State Database (LSDB). Each router runs Dijkstra locally to build its routing table. |\n| **Bellman-Ford** (Vector relaxation) | **RIP / EIGRP / BGP** | Layer 3 / Layer 4 (Inter-AS) | Neighbors exchange distance vectors. Relaxes metrics iteratively without needing global topology maps. BGP augments this with `AS-PATH` attributes to avoid loops. |\n| **Prim / Kruskal** (MST) | **STP (802.1D) / RSTP (802.1w)** | Layer 2 (Bridging / Switching) | Bridges exchange Bridge Protocol Data Units (BPDUs) to compute a single spanning tree, pruning cycles by disabling redundant switch interfaces. |",
            "citations": [
                "RFC 2328: OSPF Version 2",
                "IEEE 802.1D: Media Access Control (MAC) Bridges",
                "Computer Networks: A Systems Approach, Chapter 3.3"
            ]
        }
    ],
    "quiz": {
        "title": "Comprehensive Topic Assessment: Graph Theory, BFS, DFS & Cycle Detection",
        "description": "25 rigorously validated assessment questions covering network graph modeling, adjacency list vs. matrix complexities, BFS hop pathfinding, DFS exploration, Layer 2 loop mechanics, broadcast storms, and protocol algorithm mapping.",
        "questions": [
            {
                "id": "q-l05-01",
                "difficulty": "easy",
                "type": "single_choice",
                "question": "In the formal graph model of a computer network G = (V, E), what do the vertices V and edges E represent?",
                "options": [
                    {"id": "opt-1", "text": "V represents IP addresses; E represents MAC addresses."},
                    {"id": "opt-2", "text": "V represents forwarding devices/hosts; E represents physical or logical communication links."},
                    {"id": "opt-3", "text": "V represents TCP ports; E represents application sockets."},
                    {"id": "opt-4", "text": "V represents packets; E represents routing tables."}
                ],
                "correctOptionIds": ["opt-2"],
                "explanation": "In network graph theory, vertices V correspond to network nodes (routers, switches, endpoints), and edges E correspond to communication channels/links interconnecting them."
            },
            {
                "id": "q-l05-02",
                "difficulty": "easy",
                "type": "single_choice",
                "question": "Which data structure is fundamentally utilized by Breadth-First Search (BFS) to maintain its traversal frontier?",
                "options": [
                    {"id": "opt-1", "text": "Stack (LIFO)"},
                    {"id": "opt-2", "text": "Queue (FIFO)"},
                    {"id": "opt-3", "text": "Binary Search Tree"},
                    {"id": "opt-4", "text": "Priority Queue (MinHeap)"}
                ],
                "correctOptionIds": ["opt-2"],
                "explanation": "BFS uses a First-In, First-Out (FIFO) queue to explore vertices layer-by-layer in increasing order of hop distance from the source."
            },
            {
                "id": "q-l05-03",
                "difficulty": "easy",
                "type": "single_choice",
                "question": "What is the space complexity of an Adjacency Matrix representing a network graph with V routers?",
                "options": [
                    {"id": "opt-1", "text": "O(V)"},
                    {"id": "opt-2", "text": "O(V + E)"},
                    {"id": "opt-3", "text": "O(V^2)"},
                    {"id": "opt-4", "text": "O(E log V)"}
                ],
                "correctOptionIds": ["opt-3"],
                "explanation": "An Adjacency Matrix requires a 2D array of size V x V, consuming Theta(V^2) memory regardless of whether edges are present."
            },
            {
                "id": "q-l05-04",
                "difficulty": "easy",
                "type": "single_choice",
                "question": "Why are Ethernet switches vulnerable to catastrophic broadcast storms when wired in a physical loop, whereas IP routers are not?",
                "options": [
                    {"id": "opt-1", "text": "Ethernet switches operate at 100 Mbps, which is too fast for packet filters."},
                    {"id": "opt-2", "text": "Ethernet frames lack a Time to Live (TTL) field, so frames never expire natively."},
                    {"id": "opt-3", "text": "Ethernet switches do not support copper cables."},
                    {"id": "opt-4", "text": "IP routers disable ARP requests automatically."}
                ],
                "correctOptionIds": ["opt-2"],
                "explanation": "Layer 2 Ethernet frames contain no TTL or hop-limit field. When a broadcast frame enters a physical loop, switches forward copies indefinitely, creating a network-paralyzing broadcast storm."
            },
            {
                "id": "q-l05-05",
                "difficulty": "easy",
                "type": "single_choice",
                "question": "What metric does Breadth-First Search (BFS) guarantee to minimize between source and destination in an unweighted graph?",
                "options": [
                    {"id": "opt-1", "text": "Total link propagation latency"},
                    {"id": "opt-2", "text": "Maximum transmission throughput"},
                    {"id": "opt-3", "text": "Number of link hops (edges)"},
                    {"id": "opt-4", "text": "Financial peering transit cost"}
                ],
                "correctOptionIds": ["opt-3"],
                "explanation": "BFS treats all edges uniformly and guarantees finding the path with the minimum number of edges (hop count). It cannot optimize for weighted latency or bandwidth."
            },
            {
                "id": "q-l05-06",
                "difficulty": "easy",
                "type": "single_choice",
                "question": "Which real-world Layer 2 protocol was engineered to eliminate loops and broadcast storms in switched Ethernet networks?",
                "options": [
                    {"id": "opt-1", "text": "Spanning Tree Protocol (STP / IEEE 802.1D)"},
                    {"id": "opt-2", "text": "Open Shortest Path First (OSPF)"},
                    {"id": "opt-3", "text": "Border Gateway Protocol (BGP)"},
                    {"id": "opt-4", "text": "Address Resolution Protocol (ARP)"}
                ],
                "correctOptionIds": ["opt-1"],
                "explanation": "Spanning Tree Protocol (STP / 802.1D) computes a loop-free tree across Layer 2 switches by placing redundant switch ports into a blocking state."
            },
            {
                "id": "q-l05-07",
                "difficulty": "easy",
                "type": "multiple_choice",
                "question": "Which of the following physical or operational network attributes can be encapsulated into edge weights in a routing graph?",
                "options": [
                    {"id": "opt-1", "text": "Propagation delay across physical transmission media"},
                    {"id": "opt-2", "text": "Inverse bandwidth (interface link capacity)"},
                    {"id": "opt-3", "text": "Financial administrative peering transit cost"},
                    {"id": "opt-4", "text": "The operating system version running on client laptops"}
                ],
                "correctOptionIds": ["opt-1", "opt-2", "opt-3"],
                "explanation": "Network link metrics frequently incorporate latency, inverse bandwidth (e.g. OSPF cost = reference / bandwidth), and financial/administrative policy. Client laptop OS is irrelevant to network link costs."
            },
            {
                "id": "q-l05-08",
                "difficulty": "easy",
                "type": "single_choice",
                "question": "What is the time complexity of Depth-First Search (DFS) on a graph represented with an adjacency list?",
                "options": [
                    {"id": "opt-1", "text": "O(V * E)"},
                    {"id": "opt-2", "text": "O(V + E)"},
                    {"id": "opt-3", "text": "O(V^2)"},
                    {"id": "opt-4", "text": "O(E log V)"}
                ],
                "correctOptionIds": ["opt-2"],
                "explanation": "DFS visits every vertex once and explores every edge once in an adjacency list representation, yielding a time complexity of Theta(V + E)."
            },
            {
                "id": "q-l05-09",
                "difficulty": "easy",
                "type": "single_choice",
                "question": "Which legacy Layer 3 routing protocol used pure hop count as its metric, derived directly from BFS pathfinding principles?",
                "options": [
                    {"id": "opt-1", "text": "Routing Information Protocol (RIP)"},
                    {"id": "opt-2", "text": "Open Shortest Path First (OSPF)"},
                    {"id": "opt-3", "text": "Intermediate System to Intermediate System (IS-IS)"},
                    {"id": "opt-4", "text": "Multiprotocol BGP"}
                ],
                "correctOptionIds": ["opt-1"],
                "explanation": "RIP (RFC 1058) measured all routes purely in hop count (maximum 15 hops), behaving identically to BFS hop minimization."
            },
            {
                "id": "q-l05-10",
                "difficulty": "medium",
                "type": "single_choice",
                "question": "Why is an Adjacency List asymptotically superior to an Adjacency Matrix for storing an Internet Autonomous System topology containing 50,000 routers?",
                "options": [
                    {"id": "opt-1", "text": "Real networks are dense cliques where every router connects to all 49,999 others."},
                    {"id": "opt-2", "text": "Real networks are sparse graphs where each router connects to only a few neighbors, saving gigabytes of memory."},
                    {"id": "opt-3", "text": "Adjacency lists do not require pointers or dynamic memory."},
                    {"id": "opt-4", "text": "Adjacency matrices cannot store directed edges."}
                ],
                "correctOptionIds": ["opt-2"],
                "explanation": "Internet topologies are sparse (average node degree between 2 and 10). An adjacency matrix would allocate 50,000 x 50,000 = 2.5 billion cells (10 GB RAM), whereas an adjacency list requires only O(V + E) (~5 MB RAM)."
            },
            {
                "id": "q-l05-11",
                "difficulty": "medium",
                "type": "single_choice",
                "question": "In the India 5-city topology (Delhi-Mumbai: 5, Delhi-Hyderabad: 2, Mumbai-Hyderabad: 3, Hyderabad-Bangalore: 2, Delhi-Chennai: 8, Chennai-Bangalore: 4), what path does BFS select from Mumbai to Bangalore, and what is its hop count?",
                "options": [
                    {"id": "opt-1", "text": "Mumbai -> Delhi -> Bangalore (2 hops)"},
                    {"id": "opt-2", "text": "Mumbai -> Hyderabad -> Bangalore (2 hops)"},
                    {"id": "opt-3", "text": "Mumbai -> Chennai -> Bangalore (2 hops)"},
                    {"id": "opt-4", "text": "Mumbai -> Delhi -> Chennai -> Bangalore (3 hops)"}
                ],
                "correctOptionIds": ["opt-2"],
                "explanation": "From Mumbai, neighbors are Delhi and Hyderabad (hop 1). From Hyderabad, neighbor Bangalore is reached (hop 2). Thus BFS selects Mumbai -> Hyderabad -> Bangalore in 2 hops."
            },
            {
                "id": "q-l05-12",
                "difficulty": "medium",
                "type": "single_choice",
                "question": "In undirected graph cycle detection using DFS, what condition conclusively confirms that a cycle exists when visiting neighbor 'v' from current node 'u'?",
                "options": [
                    {"id": "opt-1", "text": "Neighbor 'v' is visited AND 'v' is equal to 'parent' of 'u'."},
                    {"id": "opt-2", "text": "Neighbor 'v' is visited AND 'v' is NOT equal to 'parent' of 'u'."},
                    {"id": "opt-3", "text": "Neighbor 'v' has an edge weight strictly greater than 10."},
                    {"id": "opt-4", "text": "Neighbor 'v' has zero outgoing edges."}
                ],
                "correctOptionIds": ["opt-2"],
                "explanation": "In an undirected graph, encountering the node you just arrived from (parent) is simply traversing the same bidirectional link backward. Encountering ANY OTHER previously visited node confirms an alternate path back, proving a cycle exists."
            },
            {
                "id": "q-l05-13",
                "difficulty": "medium",
                "type": "multiple_choice",
                "question": "Which of the following illustrate why minimizing hop count via BFS can lead to suboptimal performance in real-world networking?",
                "options": [
                    {"id": "opt-1", "text": "A 1-hop satellite link with 500ms latency is chosen over a 3-hop terrestrial fiber link with 15ms total latency."},
                    {"id": "opt-2", "text": "A 1-hop 10 Mbps legacy copper cable is chosen over a 2-hop 100 Gbps optical fiber path."},
                    {"id": "opt-3", "text": "BFS cannot find any path if the destination is more than 3 hops away."},
                    {"id": "opt-4", "text": "BFS ignores link bandwidth bottlenecks and packet loss rates."}
                ],
                "correctOptionIds": ["opt-1", "opt-2", "opt-4"],
                "explanation": "BFS optimizes only edge count. It prefers high-latency satellite and low-bandwidth copper links if they have fewer hops than superior multi-hop fiber routes. BFS can discover arbitrarily long paths (option 3 is false)."
            },
            {
                "id": "q-l05-14",
                "difficulty": "medium",
                "type": "single_choice",
                "question": "How does a BFS pathfinding implementation reconstruct the full sequence of intermediate routers from source to destination upon reaching the target node?",
                "options": [
                    {"id": "opt-1", "text": "By re-running DFS from the destination backward."},
                    {"id": "opt-2", "text": "By tracing back through a parent pointer dictionary recorded during node discovery."},
                    {"id": "opt-3", "text": "By sorting the queue in alphabetical order."},
                    {"id": "opt-4", "text": "By checking the switch CAM table on the target router."}
                ],
                "correctOptionIds": ["opt-2"],
                "explanation": "When an unvisited node is queued, the algorithm records parent[neighbor] = current. Upon reaching the target, it traverses parent pointers back to the source and reverses the collected list."
            },
            {
                "id": "q-l05-15",
                "difficulty": "medium",
                "type": "single_choice",
                "question": "What is the maximum hop count allowed in RIP routing tables before a destination is declared unreachable, and why was this ceiling chosen?",
                "options": [
                    {"id": "opt-1", "text": "10 hops; to fit in an IP packet."},
                    {"id": "opt-2", "text": "15 hops (16 is infinity); to bound the Count-to-Infinity convergence problem."},
                    {"id": "opt-3", "text": "64 hops; to match the default Linux TTL."},
                    {"id": "opt-4", "text": "255 hops; to match the maximum value of an 8-bit integer."}
                ],
                "correctOptionIds": ["opt-2"],
                "explanation": "RIP caps valid paths at 15 hops; 16 represents infinity. This limit was chosen to guarantee that routing loops during Count-to-Infinity terminate within a bounded number of update cycles."
            },
            {
                "id": "q-l05-16",
                "difficulty": "medium",
                "type": "multiple_choice",
                "question": "Which of the following symptoms directly manifest across a local area network during an active Layer 2 Broadcast Storm?",
                "options": [
                    {"id": "opt-1", "text": "Switch link utilization quickly saturates to 100% capacity."},
                    {"id": "opt-2", "text": "Switch forwarding tables experience MAC address flapping as frames arrive on alternating ports."},
                    {"id": "opt-3", "text": "Switch control plane CPUs spike to maximum load processing broadcast interrupts."},
                    {"id": "opt-4", "text": "IPv4 TTL fields decrement automatically on switches, stopping the storm within 64 hops."}
                ],
                "correctOptionIds": ["opt-1", "opt-2", "opt-3"],
                "explanation": "Broadcast storms saturate link bandwidth, thrash switch MAC tables (MAC flapping), and overwhelm switch CPUs. Layer 2 switches do not touch or decrement IP TTL (option 4 is false)."
            },
            {
                "id": "q-l05-17",
                "difficulty": "medium",
                "type": "single_choice",
                "question": "In an iterative implementation of Depth-First Search, what explicit data structure is utilized to avoid runtime call-stack overflow on deep graphs?",
                "options": [
                    {"id": "opt-1", "text": "FIFO Queue"},
                    {"id": "opt-2", "text": "LIFO Stack"},
                    {"id": "opt-3", "text": "Circular Buffer"},
                    {"id": "opt-4", "text": "Min-Heap"}
                ],
                "correctOptionIds": ["opt-2"],
                "explanation": "Iterative DFS replaces compiler recursion with an explicit LIFO (Last-In, First-Out) stack allocated on the heap, preventing call-stack exhaustion."
            },
            {
                "id": "q-l05-18",
                "difficulty": "medium",
                "type": "single_choice",
                "question": "How does Spanning Tree Protocol (STP) resolve redundant physical links between Ethernet switches without physically unplugging cables?",
                "options": [
                    {"id": "opt-1", "text": "It turns off the power to the redundant switches."},
                    {"id": "opt-2", "text": "It places redundant backup ports into a logically blocked/discarding state while keeping them ready for failover."},
                    {"id": "opt-3", "text": "It assigns distinct IPv6 link-local addresses to every switch port."},
                    {"id": "opt-4", "text": "It executes NAT on all Layer 2 frames."}
                ],
                "correctOptionIds": ["opt-2"],
                "explanation": "STP maintains physical redundancy while preventing loops by logically blocking redundant switch ports. If an active link fails, the blocked port transitions to forwarding."
            },
            {
                "id": "q-l05-19",
                "difficulty": "hard",
                "type": "single_choice",
                "question": "Suppose a connected enterprise network contains V = 100 switches and E = 120 links. How many physical links must Spanning Tree Protocol (STP) place into a blocking state to produce a loop-free spanning tree?",
                "options": [
                    {"id": "opt-1", "text": "19"},
                    {"id": "opt-2", "text": "20"},
                    {"id": "opt-3", "text": "21"},
                    {"id": "opt-4", "text": "99"}
                ],
                "correctOptionIds": ["opt-3"],
                "explanation": "A spanning tree on V vertices always contains exactly V - 1 active edges. For 100 switches, the active tree requires 100 - 1 = 99 links. Since there are 120 physical links, STP must block 120 - 99 = 21 links."
            },
            {
                "id": "q-l05-20",
                "difficulty": "hard",
                "type": "single_choice",
                "question": "Consider an undirected ring topology of 5 routers: R1-R2-R3-R4-R5-R1. If DFS starts at R1 with parent=None, which edge evaluation triggers the cycle detection condition (neighbor in visited and neighbor != parent)?",
                "options": [
                    {"id": "opt-1", "text": "R2 inspecting R1"},
                    {"id": "opt-2", "text": "R3 inspecting R2"},
                    {"id": "opt-3", "text": "R5 inspecting R1"},
                    {"id": "opt-4", "text": "R4 inspecting R3"}
                ],
                "correctOptionIds": ["opt-3"],
                "explanation": "Traversing R1 -> R2 -> R3 -> R4 -> R5: When at R5 (parent=R4), neighbors are R4 and R1. R4 is visited and is parent. R1 is already in visited AND R1 != parent (R4)! This triggers cycle detection."
            },
            {
                "id": "q-l05-21",
                "difficulty": "hard",
                "type": "multiple_choice",
                "question": "Which of the following statements correctly compare graph algorithm behavior on Adjacency Matrix vs. Adjacency List representations during network analysis?",
                "options": [
                    {"id": "opt-1", "text": "Finding if an edge exists between two routers takes O(1) in a matrix, but O(deg(u)) in an adjacency list."},
                    {"id": "opt-2", "text": "Iterating all immediate neighbors of a node takes O(V) in an adjacency matrix, but O(deg(u)) in an adjacency list."},
                    {"id": "opt-3", "text": "BFS runs in O(V^2) time on an adjacency matrix, but O(V + E) on an adjacency list."},
                    {"id": "opt-4", "text": "An adjacency matrix consumes less memory than an adjacency list when the graph is sparse."}
                ],
                "correctOptionIds": ["opt-1", "opt-2", "opt-3"],
                "explanation": "Options 1, 2, and 3 are standard algorithmic complexities. Option 4 is false because an adjacency matrix always allocates V^2 memory, which is vastly larger than O(V+E) for sparse graphs."
            },
            {
                "id": "q-l05-22",
                "difficulty": "hard",
                "type": "single_choice",
                "question": "What is the primary reason why Open Shortest Path First (OSPF) executes Dijkstra's algorithm rather than Breadth-First Search (BFS)?",
                "options": [
                    {"id": "opt-1", "text": "Dijkstra handles weighted link costs (inverse bandwidth/latency) whereas BFS only minimizes unweighted hop counts."},
                    {"id": "opt-2", "text": "BFS is too computationally expensive for graphs with more than 10 routers."},
                    {"id": "opt-3", "text": "Dijkstra can only run over UDP datagrams."},
                    {"id": "opt-4", "text": "BFS cannot find routes on directed graphs."}
                ],
                "correctOptionIds": ["opt-1"],
                "explanation": "OSPF requires calculating the lowest-cost path based on interface bandwidth metrics (cost = reference / bandwidth). BFS ignores weights entirely and only minimizes hop count, making Dijkstra essential."
            },
            {
                "id": "q-l05-23",
                "difficulty": "hard",
                "type": "single_choice",
                "question": "Suppose a network engineer runs BFS on a graph where all edge weights are strictly positive and identical (weight = 10ms for all links). How does the resulting path compare to Dijkstra's algorithm?",
                "options": [
                    {"id": "opt-1", "text": "Dijkstra finds a shorter path because it uses dynamic programming."},
                    {"id": "opt-2", "text": "BFS and Dijkstra find the exact same optimal shortest path."},
                    {"id": "opt-3", "text": "BFS fails because weights are present."},
                    {"id": "opt-4", "text": "Dijkstra takes O(V!) time on uniform weight graphs."}
                ],
                "correctOptionIds": ["opt-2"],
                "explanation": "When all edge weights are uniform positive constants (c > 0), the path with the minimum number of hops is identical to the path with the minimum total weight. BFS and Dijkstra produce identical shortest paths."
            },
            {
                "id": "q-l05-24",
                "difficulty": "hard",
                "type": "single_choice",
                "question": "In a broadcast storm, why do switch MAC address tables thrash continuously (a condition known as MAC flapping)?",
                "options": [
                    {"id": "opt-1", "text": "Because client hosts change their MAC addresses every 5 seconds."},
                    {"id": "opt-2", "text": "Because identical looped broadcast frames from source X arrive alternately on different switch ingress ports, causing the switch to repeatedly overwrite X's port mapping."},
                    {"id": "opt-3", "text": "Because DHCP servers revoke leases during high traffic."},
                    {"id": "opt-4", "text": "Because the switch CAM table runs out of electricity."}
                ],
                "correctOptionIds": ["opt-2"],
                "explanation": "When a broadcast frame from host X circulates clockwise and counter-clockwise around a physical switch loop, the switch receives frames with source MAC X on port 1, then port 2, then port 1 again, endlessly overwriting its CAM table entry (MAC flapping)."
            },
            {
                "id": "q-l05-25",
                "difficulty": "hard",
                "type": "multiple_choice",
                "question": "Which of the following algorithmic pairings accurately describe production network protocols and their foundational graph algorithms?",
                "options": [
                    {"id": "opt-1", "text": "OSPF Link State Routing <---> Dijkstra's Shortest Path Algorithm"},
                    {"id": "opt-2", "text": "IEEE 802.1D Spanning Tree Protocol <---> Minimum Spanning Tree (MST)"},
                    {"id": "opt-3", "text": "RIP Hop Count Pathfinding <---> Breadth-First Search (BFS)"},
                    {"id": "opt-4", "text": "BGP Inter-Domain Routing <---> Unweighted Depth-First Search exclusively"}
                ],
                "correctOptionIds": ["opt-1", "opt-2", "opt-3"],
                "explanation": "OSPF runs Dijkstra on its link state database; STP computes a spanning tree on bridges; RIP minimizes hop counts using Bellman-Ford/BFS principles. BGP is a path-vector protocol using policies and AS-PATH, not unweighted DFS."
            }
        ]
    }
}
