# Lecture 5: Graph Algorithms for Networking I
## Student Notes — SST Computer Networks (Term 5)

---

## 🎯 Learning Objectives

By the end of this lecture, you should be able to:
- Formally model arbitrary physical and logical computer networks as **weighted graphs** $G = (V, E)$.
- Translate real-world network metrics (propagation delay, transmission bandwidth, monetary cost, reliability) into quantitative edge weights.
- Implement, trace, and analyze **Breadth-First Search (BFS)** for unweighted minimum hop-count routing and broadcast tree construction.
- Implement, trace, and analyze **Depth-First Search (DFS)** for topology exploration, cycle detection, and bridge/cut-vertex identification.
- Master **Dijkstra’s Algorithm** with a Min-Heap priority queue, proving its greedy invariant and analyzing its $O((V + E) \log V)$ complexity.
- Trace step-by-step execution tables for Dijkstra on complex topologies and construct the resulting **Router Forwarding Table (FIB)**.
- Connect Dijkstra’s theoretical shortest-path tree directly to practical **Link-State Routing Protocols (OSPF and IS-IS)**.

---

## 1. Modeling Networks as Graphs

Every routing protocol on the internet fundamentally solves a graph algorithm problem. To apply computer science algorithms to physical telecommunications infrastructure, we construct an abstract graph model.

### Formal Graph Definition
A network is modeled as a graph $G = (V, E, W)$:
- **Vertices / Nodes ($V$)**: Routers, layer 3 switches, autonomous systems, or end hosts.
- **Edges / Links ($E$)**: Physical communication channels (Cat6a copper, submarine fiber optic cables, satellite radio links, or virtual MPLS tunnels).
- **Edge Weight Function ($W: E \rightarrow \mathbb{R}^+$)**: The cost metric associated with traversing a link.

```
                  [ Router B ]
                 /            \
        Cost = 2/              \ Cost = 1
               /                \
   [ Router A ] ──────────────── [ Router D ]
               \    Cost = 8    /
        Cost = 4\              / Cost = 3
                 \            /
                  [ Router C ]
```

### Directed vs. Undirected Networks
- **Undirected Graphs**: Assume symmetric properties (upload speed equals download speed, latency is identical in both directions).
- **Directed Graphs (Digraphs)**: Real-world internet routing is frequently **asymmetric**:
  - ADSL / Cable connections provide 300 Mbps download but only 20 Mbps upload.
  - Commercial BGP peering policies may allow traffic to enter via Provider X but force exit via Provider Y.

### Network Metrics: What Does "Cost" Mean in Practice?
In academic algorithms, weights are simple integers. In production computer networks, edge weight $w(e)$ is computed via sophisticated metric formulas:

1. **Hop Count**: Each link has weight $w = 1$. Minimizes intermediate switches (used in RIP).
2. **Latency / Propagation Delay**: Physical transit time $t = \frac{d}{v}$ (where $v \approx 2 \times 10^8\text{ m/s}$ in fiber). Critical for algorithmic trading and cloud gaming.
3. **Bandwidth Inversion (Cisco OSPF Metric)**:

   $$\text{Cost} = \frac{\text{Reference Bandwidth}}{\text{Interface Bandwidth}} = \frac{10^8\text{ bps (100 Mbps)}}{\text{Bandwidth in bps}}$$

   - 10 Mbps Ethernet: $\text{Cost} = 100 / 10 = 10$
   - 100 Mbps FastEthernet: $\text{Cost} = 100 / 100 = 1$
   - 1 Gbps GigabitEthernet: $\text{Cost} = 1$ (requires changing reference bandwidth to $10^{11}$ in modern 100G networks)
4. **Reliability & Packet Loss**: Edge weight penalized exponentially based on bit error rate (BER).

---

## 2. Breadth-First Search (BFS) in Networking

### Purpose & Theoretical Role
**BFS** explores a graph level by level, discovering all vertices at distance $k$ before any vertices at distance $k+1$.
- **Networking Application**:
  - Computes the **minimum hop-count path** in unweighted networks.
  - Used in P2P broadcast flooding (Gnutella, BitTorrent DHT peer discovery).
  - Used in SDN controllers to compute the shortest topological tree for broadcast packets.

### Formal Algorithm Specification

```python
from collections import deque

def bfs_shortest_path(graph, start_node):
    # graph: dict of {node: [neighbors]}
    visited = {start_node}
    queue = deque([start_node])
    
    distance = {start_node: 0}
    predecessor = {start_node: None}
    
    while queue:
        current = queue.popleft()
        
        for neighbor in graph.get(current, []):
            if neighbor not in visited:
                visited.add(neighbor)
                distance[neighbor] = distance[current] + 1
                predecessor[neighbor] = current
                queue.append(neighbor)
                
    return distance, predecessor
```

### Complexity Analysis
- **Time Complexity**: $O(|V| + |E|)$ when using an Adjacency List. Every vertex is enqueued once, and every edge is traversed once.
- **Space Complexity**: $O(|V|)$ to maintain the `visited` set and FIFO `queue`.

### Step-by-Step State Trace Example
Consider 6 routers: $A, B, C, D, E, F$:
- Edges: $(A, B), (A, C), (B, D), (C, D), (C, E), (D, F), (E, F)$
- Starting node: Router $A$

```
State Trace:
Initialization: Queue = [A], Visited = {A}, Dist = {A:0}

Step 1: Pop A. Neighbors of A: B, C.
        Enqueue B, C. Visited = {A, B, C}. Dist = {A:0, B:1, C:1}
        Queue = [B, C]

Step 2: Pop B. Neighbors of B: A (visited), D.
        Enqueue D. Visited = {A, B, C, D}. Dist = {..., D:2}
        Queue = [C, D]

Step 3: Pop C. Neighbors of C: A (visited), D (visited), E.
        Enqueue E. Visited = {A, B, C, D, E}. Dist = {..., E:2}
        Queue = [D, E]

Step 4: Pop D. Neighbors of D: B, C (visited), F.
        Enqueue F. Visited = {A, B, C, D, E, F}. Dist = {..., F:3}
        Queue = [E, F]

Step 5: Pop E. Neighbors of E: C (visited), F (already visited!).
        Queue = [F]

Step 6: Pop F. All neighbors visited. Queue empty. Termination.
```

### Why Hop-Count BFS Fails on Real Networks
BFS treats all links identically. In the topology below, BFS chooses Path $A \rightarrow B$ because it is $1$ hop. However, $A \rightarrow B$ is a congested 56 kbps dialup link ($200\text{ ms}$ delay), while $A \rightarrow C \rightarrow B$ is a 100 Gbps fiber line ($2\text{ ms}$ delay). This fatal flaw requires **weighted graph algorithms**.

```
             [ Router A ] ─── 56 kbps (Hop=1, Latency=200ms) ───► [ Router B ]
                  │                                                     ▲
                  └── 100 Gbps (Latency=1ms) ──► [ Router C ] ──────────┘
                                                  100 Gbps (Latency=1ms)
```

---

## 3. Depth-First Search (DFS) in Networking

### Purpose & Theoretical Role
**DFS** explores as deep as possible along each branch before backtracking.
- **Networking Applications**:
  - **Loop / Cycle Detection**: Detecting Layer 2 switching loops that cause destructive broadcast storms.
  - **Path Feasibility & Reachability**: Verifying if an isolated backup link can reach a disaster recovery site.
  - **Biconnected Components & Bridges**: Identifying **Single Points of Failure (SPOF)**. A link whose removal disconnects the graph is a *bridge*; a router whose failure splits the network is an *articulation point*.

### Cycle Detection Algorithm (Three-Color Method)
In a network graph, a cycle causes packets to circulate indefinitely until their TTL expires. We detect cycles using DFS node coloring:
- **WHITE**: Node unvisited.
- **GRAY**: Node currently being explored (currently on the recursion call stack).
- **BLACK**: Node and all its descendants have been fully explored.

> **Theorem**: A network graph contains a cycle if and only if a DFS traversal encounters a directed edge pointing to a **GRAY** node (a *back-edge*).

```python
def has_cycle(graph):
    color = {node: "WHITE" for node in graph}
    
    def dfs(node):
        color[node] = "GRAY"
        for neighbor in graph.get(node, []):
            if color[neighbor] == "GRAY":
                return True # Cycle detected!
            if color[neighbor] == "WHITE" and dfs(neighbor):
                return True
        color[node] = "BLACK"
        return False

    for node in graph:
        if color[node] == "WHITE":
            if dfs(node):
                return True
    return False
```

---

## 4. Dijkstra’s Shortest-Path Algorithm

Published in 1959 by Edsger W. Dijkstra, this algorithm solves the **Single-Source Shortest Path (SSSP)** problem for graphs with **strictly non-negative edge weights** ($w(e) \ge 0$).

### The Greedy Choice Property & Invariant
Dijkstra maintains two sets of vertices:
1. $S$: The set of vertices whose shortest distance from the source is **permanently finalized**.
2. $Q$: A priority queue (min-heap) of vertices whose tentative distances are still subject to improvement.

> 🔑 **THE GREEDY INVARIANT**:
> At each step, the algorithm extracts the vertex $u \in Q$ with the minimum tentative distance $dist[u]$. Because all edge weights are non-negative ($w \ge 0$), any other path reaching $u$ later would have to travel through another node in $Q$, which already has a tentative distance $\ge dist[u]$. Therefore, **$dist[u]$ can never be improved further, and is permanently optimal.**

### The Edge Relaxation Primitive
The heart of shortest path algorithms is the **Relaxation Step**:

$$\text{relax}(u, v, w): \quad \mathbf{if\ } dist[v] > dist[u] + w(u, v) \implies dist[v] = dist[u] + w(u, v), \quad pred[v] = u$$

```
Before Relaxation:                   After Relaxation:
  dist[u] = 10                         dist[u] = 10
  dist[v] = 25                         dist[v] = 14  <-- Improved!
       (u) ── weight=4 ──► (v)              (u) ── weight=4 ──► (v)
```

### Complete Python Implementation with Min-Heap

```python
import heapq

def dijkstra(graph, source):
    # graph format: {node: [(neighbor, cost), ...]}
    dist = {node: float('inf') for node in graph}
    pred = {node: None for node in graph}
    
    dist[source] = 0
    # Min-Heap stores tuples: (current_distance, node)
    pq = [(0, source)]
    
    visited = set()
    
    while pq:
        d, u = heapq.heappop(pq)
        
        if u in visited:
            continue
        visited.add(u)
        
        for neighbor, weight in graph.get(u, []):
            if neighbor in visited:
                continue
            if dist[u] + weight < dist[neighbor]:
                dist[neighbor] = dist[u] + weight
                pred[neighbor] = u
                heapq.heappush(pq, (dist[neighbor], neighbor))
                
    return dist, pred
```

### Complexity Breakdown
- **With Min-Heap / Binary Heap**:
  - Extract-Min: $O(|V| \log |V|)$
  - Decrease-Key / Push: $O(|E| \log |V|)$
  - **Total Time Complexity**: $\mathbf{O((|V| + |E|) \log |V|)}$
- **With Fibonacci Heap** (Theoretical): $O(|E| + |V| \log |V|)$
- **Naive Array Implementation**: $O(|V|^2)$ (unacceptable for massive ISP graphs).

---

## 5. End-to-End Dijkstra Trace on an ISP Network

Let us trace Dijkstra on a realistic ISP core network consisting of 6 routers: **$A, B, C, D, E, F$**.

```
                [ B ] ────── 2 ────── [ D ]
               /  │                     │  \
              4   │ 1                   │ 3  \ 5
             /    │                     │     \
       [ A ]      └──────── 6 ──────────┘      [ F ]
             \                                /
              2                              / 1
               \                            /
                [ C ] ────── 7 ────── [ E ]
```

- **Source Node**: **$A$**
- **Link Costs**:
  - $A-B: 4$, $A-C: 2$
  - $B-C: 1$, $B-D: 2$, $B-E: \infty$
  - $C-E: 7$
  - $D-E: 3$, $D-F: 5$
  - $E-F: 1$

### Step-by-Step Execution Table

| Step | Visited / Finalized ($u$) | Min $dist[u]$ | Relaxation Updates ($v: dist[u] + w < dist[v]$) | Priority Queue Contents ($dist, node$) |
| :--- | :--- | :--- | :--- | :--- |
| **0** | None (Init) | - | $dist[A] = 0$, all others $\infty$ | `[(0, A)]` |
| **1** | **A** | 0 | $B: 0 + 4 = 4$ (via A)<br>$C: 0 + 2 = 2$ (via A) | `[(2, C), (4, B)]` |
| **2** | **C** | 2 | $B: 2 + 1 = 3 < 4$ (via C) *(Updated!)*<br>$E: 2 + 7 = 9$ (via C) | `[(3, B), (4, B_stale), (9, E)]` |
| **3** | **B** | 3 | $D: 3 + 2 = 5$ (via B)<br>$D$ path via B is optimal | `[(5, D), (9, E)]` |
| **4** | **D** | 5 | $E: 5 + 3 = 8 < 9$ (via D) *(Updated!)*<br>$F: 5 + 5 = 10$ (via D) | `[(8, E), (10, F)]` |
| **5** | **E** | 8 | $F: 8 + 1 = 9 < 10$ (via E) *(Updated!)* | `[(9, F), (10, F_stale)]` |
| **6** | **F** | 9 | No unvisited neighbors. | `[]` (Empty) |

### Final Shortest-Path Tree (Rooted at A):
- $A \rightarrow A$: Cost = **0**
- $A \rightarrow C$: Cost = **2** (Path: $A \rightarrow C$)
- $A \rightarrow B$: Cost = **3** (Path: $A \rightarrow C \rightarrow B$)
- $A \rightarrow D$: Cost = **5** (Path: $A \rightarrow C \rightarrow B \rightarrow D$)
- $A \rightarrow E$: Cost = **8** (Path: $A \rightarrow C \rightarrow B \rightarrow D \rightarrow E$)
- $A \rightarrow F$: Cost = **9** (Path: $A \rightarrow C \rightarrow B \rightarrow D \rightarrow E \rightarrow F$)

---

## 6. From Graph Tree to Router Forwarding Table (FIB)

How does Router $A$ convert this mathematical tree into hardware forwarding logic? Router $A$ only has physical interfaces attached to its immediate neighbors:
- Interface `eth0`: Connected to Router $B$
- Interface `eth1`: Connected to Router $C$

When a packet arrives at Router $A$ destined for Router $F$, Router $A$ inspects the predecessor chain:

$$F \leftarrow E \leftarrow D \leftarrow B \leftarrow \mathbf{C} \leftarrow A$$

The first hop out of Router $A$ is **Router $C$** via interface `eth1`.

### Router A's Forwarding Table:

| Destination IP / Subnet | Optimal Cost | Next-Hop Router | Outgoing Physical Interface |
| :--- | :--- | :--- | :--- |
| Subnet B (`10.0.2.0/24`) | 3 | `10.0.1.2` (Router C) | `eth1` |
| Subnet C (`10.0.1.0/24`) | 2 | Direct (`10.0.1.2`) | `eth1` |
| Subnet D (`10.0.3.0/24`) | 5 | `10.0.1.2` (Router C) | `eth1` |
| Subnet E (`10.0.4.0/24`) | 8 | `10.0.1.2` (Router C) | `eth1` |
| Subnet F (`10.0.5.0/24`) | 9 | `10.0.1.2` (Router C) | `eth1` |

> **Crucial Observation**: Even though Router $B$ is a direct physical neighbor of $A$ via `eth0`, Router $A$ forwards traffic for $B$ through Router $C$ because the path $A \rightarrow C \rightarrow B$ (cost $3$) is cheaper than direct link $A \rightarrow B$ (cost $4$)!

---

## 📌 Summary Checklist & Exam Cram Notes

1. **Network Modeling**: $V = \text{Routers}$, $E = \text{Links}$, $w = \text{Cost metric (latency, inverse bandwidth)}$.
2. **BFS Invariant**: Explores by hop-count; solves unweighted shortest path in $O(V + E)$. Fails when links have differing capacities.
3. **DFS Invariant**: Explores branch depth first; used for cycle detection via 3-color back-edges (Gray-to-Gray) and finding bridges.
4. **Dijkstra Invariant**: Solves non-negative single-source shortest path ($w \ge 0$). Greedily finalizes the minimum tentative node.
5. **Dijkstra Complexity**: $O((V + E) \log V)$ with adjacency list and binary min-heap.
6. **Relaxation Formula**: If $dist[u] + w(u,v) < dist[v] \implies dist[v] = dist[u] + w(u,v)$.
7. **Next-Hop Derivation**: Router traces predecessor pointers back to the source to find which local physical interface exits toward the destination.
8. **Real-World Protocol**: Link-State routing (OSPF, IS-IS) runs Dijkstra independently inside every router.

---

## 🧠 Practice Problems & Self-Check Questions

1. In a directed graph representing internet routing, suppose link $A \rightarrow B$ has cost 5 and link $B \rightarrow A$ has cost 20. Why does this asymmetry occur in real telecom networks?
2. If all edge weights in a network graph are identical constants ($w = 7$), which algorithm is asymptotically faster to compute shortest paths: BFS or Dijkstra? Why?
3. What happens if Dijkstra’s algorithm is executed on a graph with negative edge weights? Does it always produce an incorrect answer, or can it fail? (Preview for Lecture 6).
4. Given 5 routers in a complete ring topology ($A-B-C-D-E-A$) where each link has cost 2. Trace the shortest path from $A$ to $D$. How many paths have equal minimum cost?
5. How does an SDN (Software-Defined Networking) controller use graph algorithms differently than traditional distributed routers running OSPF?
