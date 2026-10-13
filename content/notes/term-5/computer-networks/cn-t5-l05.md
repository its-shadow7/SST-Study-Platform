# Graph Theory in Networking - BFS, DFS, Adjacency Models & Cycle Detection
**Term:** Term 5 | **Subject:** CN | **Note ID:** `cn-t5-l05`
**Last Updated:** 2026-10-13T00:00:00Z

## Abstract & Summary
An exhaustive, rigorous masterclass in graph theory fundamentals applied to computer networks. Explores graph mathematical modeling G = (V, E), sparse internet topology vs. dense matrix representations, Breadth-First Search (BFS) hop-count pathfinding and path reconstruction, Depth-First Search (DFS) topology exploration, the canonical Layer 2 cycle detection algorithm, and Spanning Tree Protocol (STP / 802.1D) broadcast storm elimination.

## Learning Objectives
- Model complex network topologies as weighted graphs G = (V, E) with propagation delay, inverse bandwidth, and administrative link costs.
- Contrast Adjacency List (O(V+E) space) and Adjacency Matrix (O(V^2) space) representations, explaining why the sparse Internet topology mandates adjacency lists.
- Implement and trace Breadth-First Search (BFS) using FIFO queues to discover minimum-hop paths and reconstruct routes via parent pointers.
- Analyze the fundamental architectural limitation of BFS (hop-count minimization vs. latency/bandwidth minimization) and recognize when Dijkstra is required.
- Implement Depth-First Search (DFS) with recursion and explicit stacks for complete network topology discovery.
- Dissect the canonical parent-pointer cycle detection algorithm and explain why Layer 2 Ethernet loops cause catastrophic broadcast storms without Spanning Tree Protocol (STP).

## Key Takeaways
- Networks are formally modeled as weighted graphs G = (V, E) where routers/switches are vertices V, communication cables/channels are edges E, and edge weights represent propagation delay, financial metrics, or inverse bandwidth.
- Because real-world network router topologies are sparse (average node degree between 2 and 10), the Adjacency List is asymptotically superior to the Adjacency Matrix, requiring O(V+E) space versus O(V^2) and enabling rapid neighbor iteration.
- BFS guarantees the shortest path exclusively in terms of hop count (number of intermediate links) using a FIFO queue in O(V+E) time, tracking parent pointers for path reconstruction.
- The critical limitation of BFS in production networks is that hop count does not correlate with transmission speed or delay; a 1-hop satellite link (500ms) will be chosen by BFS over a 3-hop terrestrial fiber route (15ms). Cost-based routing requires Dijkstra.
- Layer 2 Ethernet frames lack a Time to Live (TTL) field. Consequently, a physical loop in a switched Ethernet topology causes broadcast frames to multiply and circulate infinitely, triggering a broadcast storm that saturates switch CPUs and crashes the LAN.
- Cycle detection using DFS tracking parent pointers (if neighbor is visited and neighbor != parent -> loop exists) is the algorithmic foundation for Layer 2 loop elimination via Spanning Tree Protocol (STP / 802.1D).

---

## Modeling Computer Networks as Weighted Graphs
### The Graph Abstraction of Communications Topologies

At its mathematical foundation, the global Internet is a massive, decentralized graph. Every design pattern, pathfinding mechanism, and fault-tolerance protocol in networking relies on graph theory.

A network is formally modeled as a graph:
$$G = (V, E)$$
Where:
- **Vertices ($V$)**: Represent intermediate forwarding nodes (Layer 3 routers, Layer 2 switches) and terminal endpoints (servers, hosts).
- **Edges ($E$)**: Represent bidirectional or unidirectional communication circuits (physical fiber optic cables, copper twisted-pair Ethernet, wireless radio frequency links, satellite transponders).

```
                                [Delhi]
                               /   5   \
                              /         \ 2
                             /     3     \
                         [Mumbai] ───── [Hyderabad]
                             \               \
                              \ 8             \ 2
                               \               \
                               [Chennai] ───── [Bangalore]
                                          4
```

### Edge Weight Formulations: What Does Link Cost Represent?
In pure graph theory, edge weights are abstract integers. In network engineering, an edge weight $W(u, v)$ encapsulates physical and operational properties:
1. **Propagation Latency ($d_{\text{prop}}$)**: Time required for a bit to transit the physical medium at the speed of light ($s \approx 2 \times 10^8\text{ m/s}$ in optical glass). Longer geographical links incur higher weights.
2. **Inverse Bandwidth (Link Capacity)**: High-speed backbones should be preferred over slow links. For instance, in Cisco OSPF:
   $$\text{Cost} = \frac{\text{Reference Bandwidth (100 Mbps)}}{\text{Interface Bandwidth}}$$
   A $10\text{ Gbps}$ interface receives a cost of $1$, whereas a $10\text{ Mbps}$ link receives a cost of $10$.
3. **Financial Transit Cost & Peering Policies**: Autonomous Systems (AS) assign artificial high weights to transit links where they must pay upstream transit providers per gigabyte, while assigning zero or low cost to free settlement peering links.
4. **Reliability & Bit Error Rate (BER)**: Unstable wireless links with frequent packet drops can be assigned higher metrics to discourage route selection under stable conditions.

**Citations & References:**
- Introduction to Algorithms (Cormen, Leiserson, Rivest, Stein), Chapter 22: Elementary Graph Algorithms
- Computer Networks: A Systems Approach, Chapter 3: Routing
- RFC 2328: OSPF Version 2, Section 1.3 (Routing with OSPF)

---

## Adjacency List vs. Adjacency Matrix in Sparse Internet Topologies
### Graph Storage Trade-Offs at Internet Scale

To compute routing tables, a router's control plane CPU must represent the network topology in RAM. The two primary programmatic representations are the **Adjacency Matrix** and the **Adjacency List**.

#### 1. The Adjacency Matrix
A 2D array $M$ of size $|V| \times |V|$, where $M[u][v]$ stores the weight of the link between vertex $u$ and vertex $v$ (or $\infty$ if no direct link exists):

```
               Delhi     Mumbai   Hyderabad   Bangalore   Chennai
  Delhi     [    0,        5,         2,          ∞,         8    ]
  Mumbai    [    5,        0,         3,          ∞,         ∞    ]
  Hyderabad [    2,        3,         0,          2,         ∞    ]
  Bangalore [    ∞,        ∞,         2,          0,         4    ]
  Chennai   [    8,        ∞,         ∞,          4,         0    ]
```

- **Space Complexity**: $\Theta(|V|^2)$, completely independent of the number of edges $|E|$.
- **Edge Existence Lookup**: $\Theta(1)$ instantaneous array indexing.
- **Iterating All Neighbors of a Node**: $\Theta(|V|)$ operations (must scan entire row, checking for non-infinity values).

#### 2. The Adjacency List
An associative array or hash map where each vertex $u$ maps to a dynamic list of tuples `(neighbor, weight)` representing only direct, active connections:

```python
network_graph = {
    'Delhi':     [('Mumbai', 5), ('Hyderabad', 2), ('Chennai', 8)],
    'Mumbai':    [('Delhi', 5), ('Hyderabad', 3)],
    'Hyderabad': [('Delhi', 2), ('Mumbai', 3), ('Bangalore', 2)],
    'Bangalore': [('Hyderabad', 2), ('Chennai', 4)],
    'Chennai':   [('Delhi', 8), ('Bangalore', 4)]
}
```

- **Space Complexity**: $\Theta(|V| + |E|)$.
- **Iterating All Neighbors of Node $u$**: $\Theta(\text{deg}(u))$, where $\text{deg}(u)$ is the degree (number of links) of node $u$.

### Why the Internet Demands Adjacency Lists

> [!IMPORTANT]
> **The Sparsity of Communications Topologies**: Real-world communication networks are fundamentally **sparse graphs** ($|E| \ll |V|^2$). A core router in an ISP typically has between $4$ and $16$ high-speed line cards, not $100,000$.

Consider an Autonomous System topology with $|V| = 50,000$ routers:
- **Adjacency Matrix Memory Footprint**:
  $$50,000 \times 50,000 = 2,500,000,000 \text{ elements} \times 4\text{ bytes} = \mathbf{10\text{ Gigabytes of RAM}}$$
  Scanning neighbors during SPF recalculation requires iterating through $50,000$ elements for every single node.
- **Adjacency List Memory Footprint** (assuming average degree $\text{deg}(u) = 8 \implies |E| = 200,000$ edges):
  $$50,000 \text{ pointers} + 400,000 \text{ edge records} \approx \mathbf{4.8\text{ Megabytes of RAM}}$$

Because router memory and convergence speed are critical, routing protocols (such as OSPF and IS-IS) model topologies exclusively using adjacency lists.

**Citations & References:**
- Algorithms, 4th Edition (Robert Sedgewick & Kevin Wayne), Chapter 4: Graphs
- RFC 2328: OSPF Version 2, Appendix C (Configurable Constants)

---

## Breadth-First Search (BFS) & Minimum-Hop Path Reconstruction
### Discovering Routes Layer-by-Layer

Breadth-First Search (BFS) is the fundamental graph traversal algorithm for discovering the **minimum-hop path** from a designated source vertex to all reachable destinations.

### Core Invariants of BFS
1. **Queue Discipline (FIFO)**: Explores vertices in strictly increasing order of their distance (hop count) from the source.
2. **Visited Guard Set**: Prevents infinite loops and redundant reprocessing by marking nodes when they are first discovered.
3. **Hop Minimization**: Guarantees that the first time vertex $v$ is dequeued from the queue, the path discovered from source $s$ to $v$ contains the absolute minimum number of intermediate edges.

```python
from collections import deque
from typing import Dict, List, Tuple, Optional

def bfs_shortest_hop_path(graph: Dict[str, List[Tuple[str, int]]], start: str, target: str) -> Optional[List[str]]:
    """
    Computes the path with the minimum number of link hops between start and target.
    Maintains a parent pointer dictionary to reconstruct the route.
    """
    visited = {start}
    queue = deque([start])
    parent = {start: None}
    
    while queue:
        curr = queue.popleft()
        
        if curr == target:
            # Reconstruct path from target back to start via parent pointers
            path = []
            node = target
            while node is not None:
                path.append(node)
                node = parent[node]
            return list(reversed(path))
            
        for neighbor, _ in graph.get(curr, []):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = curr
                queue.append(neighbor)
                
    return None  # Target unreachable
```

### Step-by-Step Execution Trace: Mumbai to Bangalore

Let us trace `bfs_shortest_hop_path` on our 5-city topology to route from **Mumbai** to **Bangalore**:

```
Initial State:
  Queue = [Mumbai]
  Visited = {Mumbai}
  Parent = {Mumbai: None}

Step 1: Pop Mumbai
  Neighbors of Mumbai: Delhi, Hyderabad
  Add Delhi: Visited={Mumbai, Delhi}, Parent[Delhi]=Mumbai, Queue=[Delhi]
  Add Hyderabad: Visited={Mumbai, Delhi, Hyderabad}, Parent[Hyderabad]=Mumbai, Queue=[Delhi, Hyderabad]

Step 2: Pop Delhi (Distance = 1 hop)
  Neighbors of Delhi: Mumbai (visited), Hyderabad (visited), Chennai (unvisited)
  Add Chennai: Visited={..., Chennai}, Parent[Chennai]=Delhi, Queue=[Hyderabad, Chennai]

Step 3: Pop Hyderabad (Distance = 1 hop)
  Neighbors of Hyderabad: Delhi (visited), Mumbai (visited), Bangalore (unvisited)
  Add Bangalore: Visited={..., Bangalore}, Parent[Bangalore]=Hyderabad, Queue=[Chennai, Bangalore]

Step 4: Pop Chennai (Distance = 2 hops)
  Neighbors of Chennai: Delhi (visited), Bangalore (already visited/queued)

Step 5: Pop Bangalore (Distance = 2 hops)
  Target 'Bangalore' reached!
  Reconstruct path: Bangalore -> Parent[Bangalore]=Hyderabad -> Parent[Hyderabad]=Mumbai -> None
  Final Reconstructed Route: Mumbai -> Hyderabad -> Bangalore (2 hops)
```

**Citations & References:**
- Introduction to Algorithms, Chapter 22.2: Breadth-first search
- Computer Networks (Andrew S. Tanenbaum & David J. Wetherall), Chapter 5: The Network Layer

---

## The Fundamental Architectural Limitation of Hop-Based Routing
### The Fatal Flaw of Hop Minimization

While BFS provides an elegant, optimal solution for minimizing edge counts, **hop count is a disastrous metric for real-world production networks**.

Consider the following real-world scenario:

```
                                  Satellite Link
                         [Router A] ──────────────► [Router B]
                              │       1 Hop (500ms)      ▲
                              │                          │
                              │ 3 Hops                   │
                              │ Terrestrial Fiber        │
                              ▼ (5ms each = 15ms total)  │
                         [Router C] ──► [Router D] ──────┘
```

- **Route 1 (Satellite)**: $A \to B$. Hop count: **1 hop**. Total delay: **$500\text{ ms}$**.
- **Route 2 (Terrestrial Fiber)**: $A \to C \to D \to B$. Hop count: **3 hops**. Total delay: **$15\text{ ms}$**.

#### What Does BFS Choose?
Because BFS minimizes the number of edges, it chooses the **1-hop Satellite path** ($500\text{ ms}$ latency), completely ignoring the fact that the 3-hop fiber path is **33 times faster**!

### Historical Legacy: RIP Hop Count Ceiling
The original **Routing Information Protocol (RIP / RFC 1058)** used pure hop count as its metric, derived directly from Bellman-Ford/BFS principles. This led to notorious operational problems:
1. **High-Speed Link Bypass**: A $10\text{ Mbps}$ Ethernet link of 1 hop was preferred over a $10\text{ Gbps}$ fiber path of 2 hops.
2. **The 15-Hop Diameter Limit**: To contain the count-to-infinity problem, RIP defined $16$ as infinity (unreachable). Consequently, RIP cannot be deployed on any network with a diameter greater than 15 routers.

For enterprise and internet-scale routing, hop-count algorithms were superseded by cost-based link-state routing (**Dijkstra's Algorithm in OSPF/IS-IS**).

**Citations & References:**
- RFC 1058: Routing Information Protocol
- RFC 2453: RIP Version 2
- Computer Networks: A Systems Approach, Chapter 3.3: Routing Algorithms

---

## Depth-First Search (DFS) & Topological Exploration
### Deep Branch Exploration & Recursion Mechanics

Depth-First Search (DFS) explores a graph by traversing as deeply as possible along each branch before backtracking. Unlike BFS (which discovers shortest paths in concentric circles), DFS is designed for **exhaustive topological exploration**:
- Finding connected components.
- Topological sorting of dependency networks.
- Spanning tree generation.
- **Cycle and loop detection** in physical topologies.

### Recursive vs. Iterative Implementations

```python
def dfs_recursive(graph: dict, node: str, visited: set = None) -> list:
    if visited is None:
        visited = set()
    visited.add(node)
    traversal = [node]
    
    for neighbor, _ in graph.get(node, []):
        if neighbor not in visited:
            traversal.extend(dfs_recursive(graph, neighbor, visited))
            
    return traversal

def dfs_iterative(graph: dict, start: str) -> list:
    """Iterative DFS using an explicit LIFO Stack to prevent recursion depth overflow."""
    visited = set()
    stack = [start]
    traversal = []
    
    while stack:
        curr = stack.pop()
        if curr not in visited:
            visited.add(curr)
            traversal.append(curr)
            # Push neighbors in reverse order to preserve canonical iteration
            for neighbor, _ in reversed(graph.get(curr, [])):
                if neighbor not in visited:
                    stack.append(neighbor)
                    
    return traversal
```

### Complexity Comparison: BFS vs. DFS

| Property | Breadth-First Search (BFS) | Depth-First Search (DFS) |
| :--- | :--- | :--- |
| **Underlying Data Structure** | Queue (FIFO) | Stack (LIFO) / Call Stack |
| **Memory Footprint** | $O(|V|)$ (stores entire current frontier level) | $O(\text{depth})$ (proportional to tree depth) |
| **Time Complexity** | $\Theta(|V| + |E|)$ | $\Theta(|V| + |E|)$ |
| **Path Guarantees** | Minimum hop-count shortest path | Any reachable path (not shortest) |
| **Primary Network Roles** | Hop pathfinding, distance broadcasting | Cycle detection, topology maps, reachability verification |

**Citations & References:**
- Introduction to Algorithms, Chapter 22.3: Depth-first search
- The Design and Analysis of Computer Algorithms (Aho, Hopcroft, Ullman)

---

## Layer 2 Cycle Detection & Broadcast Storm Catastrophe
### Why Loops Are Fatal at Layer 2: The Missing TTL

In Layer 3 (IP), every packet contains a Time to Live (IPv4 TTL) or Hop Limit (IPv6) field. If a routing loop occurs, each router decrements the TTL by 1. When TTL reaches 0, the packet is discarded and an ICMP Time Exceeded message is generated.

> [!CAUTION]
> **The Ethernet Vulnerability**: Layer 2 Ethernet frames **do not have a TTL field**! Once an Ethernet frame enters a switched network, it has no native mechanism to expire.

If physical switches are wired in a loop (e.g., Switch A $\leftrightarrow$ Switch B $\leftrightarrow$ Switch C $\leftrightarrow$ Switch A) for hardware redundancy, a catastrophic phenomenon occurs:

```
                                  Switch A
                                 ┌─────────┐
                        ┌───────►│ Broadcast│◄───────┐
                        │        │ Copies  │        │
                        │        └────┬────┘        │
                        │             │             │
                        │ Frame loops │ Frame loops │ Infinite
                        │ clockwise   │ counter-CW  │ Replication
                        │             ▼             │
                   ┌────┴────┐                 ┌────┴────┐
                   │ Switch B│────────────────►│ Switch C│
                   └─────────┘                 └─────────┘
```

1. Host $X$ broadcasts an ARP request (`ff:ff:ff:ff:ff:ff`).
2. Switch A floods the frame out all ports to Switch B and Switch C.
3. Switch B and Switch C flood the frame out all ports back to each other and back to Switch A.
4. The frame multiplies exponentially. Within hundreds of milliseconds, the network experiences a **Broadcast Storm**: link bandwidth hits $100\%$, switch MAC forwarding tables thrash continuously (MAC flapping), and switch CPUs collapse.

### The Canonical Parent-Pointer Cycle Detection Algorithm

To detect physical and logical cycles in an undirected topology, network software executes a modified DFS tracking the `parent` vertex from which each node was reached:

```python
def is_cycle_present(graph: dict, curr: str, parent: Optional[str], visited: set) -> bool:
    """
    Detects loops in an undirected network graph.
    In an undirected link between u and v, returning to parent (the node we just arrived from)
    is normal. But encountering ANY OTHER previously visited node confirms a CYCLE!
    """
    visited.add(curr)
    
    for neighbor, _ in graph.get(curr, []):
        if neighbor not in visited:
            if is_cycle_present(graph, neighbor, curr, visited):
                return True
        elif neighbor != parent:
            # The neighbor was already visited AND is NOT the parent we came from!
            return True
            
    return False

# Execution on enterprise topology:
visited = set()
has_loop = is_cycle_present(network_graph, curr="Mumbai", parent=None, visited=visited)
if has_loop:
    print("CRITICAL: Layer 2 Loop Detected! Spanning Tree Protocol required.")
```

### Network Remediation: Spanning Tree Protocol (STP / IEEE 802.1D)
When `is_cycle_present` is true, switches run the distributed **Spanning Tree Protocol (STP)**:
1. Elect a single **Root Bridge** (the switch with lowest Bridge ID).
2. Calculate shortest paths from all switches to the Root Bridge.
3. Transition redundant backup ports into an alternate/discarding (**Blocking**) state.
4. Frames flow across a loop-free tree. If an active link is physically severed, the blocked port transitions to Forwarding within seconds, restoring redundancy without broadcast storms.

**Citations & References:**
- IEEE Std 802.1D-2004: IEEE Standard for Local and Metropolitan Area Networks: Media Access Control (MAC) Bridges
- Interconnections: Bridges, Routers, Switches, and Internetworking Protocols (Radia Perlman), Chapter 3: Spanning Tree Algorithm

---

## Mapping Graph Algorithms to Internet Protocols (BFS, DFS, Dijkstra, STP)
### From Academic Graph Theory to Production Internet Architecture

The fundamental graph algorithms studied in computer science form the exact algorithmic core of modern networking protocols:

```
      GRAPH ALGORITHM                      INTERNET PROTOCOL EQUIVALENT
   ─────────────────────                  ──────────────────────────────
   Breadth-First Search (BFS)   ══════►   RIP (Routing Information Protocol)
   Depth-First Search (DFS)     ══════►   STP Loop Detection & Topology Auditing
   Dijkstra's Algorithm         ══════►   OSPF / IS-IS (Link State Routing)
   Bellman-Ford Algorithm       ══════►   BGP / Distance Vector Routing
   Minimum Spanning Tree (MST)  ══════►   IEEE 802.1D Spanning Tree Protocol
```

### Comprehensive Protocol Architecture Taxonomy

| Graph Algorithm | Protocol Name | Operational Tier | Algorithmic Mechanism in Protocol |
| :--- | :--- | :--- | :--- |
| **BFS** (Hop count) | **RIPv1 / RIPv2** | Layer 3 (Interior Routing) | Discovers shortest path by minimizing total hop count. Advertises vectors every $30$ seconds. Maximum metric capped at $15$ hops. |
| **DFS** (Loop detection) | **STP Engine / Network Audit** | Layer 2 (Switching Fabric) | Analyzes network adjacency state to identify cycles and compute non-cyclic active forwarding graphs. |
| **Dijkstra** (Least Cost) | **OSPFv2 / OSPFv3 / IS-IS** | Layer 3 (Interior Routing) | Routers flood Link State Advertisements (LSAs) so every router builds an identical Link State Database (LSDB). Each router runs Dijkstra locally to build its routing table. |
| **Bellman-Ford** (Vector relaxation) | **RIP / EIGRP / BGP** | Layer 3 / Layer 4 (Inter-AS) | Neighbors exchange distance vectors. Relaxes metrics iteratively without needing global topology maps. BGP augments this with `AS-PATH` attributes to avoid loops. |
| **Prim / Kruskal** (MST) | **STP (802.1D) / RSTP (802.1w)** | Layer 2 (Bridging / Switching) | Bridges exchange Bridge Protocol Data Units (BPDUs) to compute a single spanning tree, pruning cycles by disabling redundant switch interfaces. |

**Citations & References:**
- RFC 2328: OSPF Version 2
- IEEE 802.1D: Media Access Control (MAC) Bridges
- Computer Networks: A Systems Approach, Chapter 3.3

---
