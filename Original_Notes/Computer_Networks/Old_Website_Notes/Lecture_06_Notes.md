# Lecture 6: Graph Algorithms for Networking II
## Student Notes — SST Computer Networks (Term 5)

---

## 🎯 Learning Objectives

By the end of this lecture, you should be able to:
- Formally demonstrate with counterexamples why **Dijkstra’s algorithm fails** in the presence of negative edge weights.
- Understand what a **negative-weight cycle** is and why shortest paths become mathematically undefined ($-\infty$).
- Implement and trace the **Bellman-Ford Algorithm**, deriving its dynamic programming recurrence relation.
- Prove why Bellman-Ford requires exactly **$|V| - 1$ relaxation passes**, and use the $|V|$-th pass to detect negative cycles.
- Connect Bellman-Ford’s distributed formulation directly to **Distance Vector Routing Protocols (RIP, BGP)**.
- Formulate the **Minimum Spanning Tree (MST)** problem and implement **Kruskal’s algorithm** with Disjoint Set Union (DSU) and **Prim’s algorithm**.
- Analyze the operational mechanics of the **Spanning Tree Protocol (STP - IEEE 802.1D)** used in Layer 2 switched Ethernet networks to prevent broadcast storms.
- Evaluate the computational trade-offs among BFS, Dijkstra, Bellman-Ford, Floyd-Warshall, and MST algorithms in telecommunications design.

---

## 1. Why Dijkstra Fails on Negative-Weight Edges

In Lecture 5, we proved that Dijkstra’s algorithm relies on a **greedy invariant**:
> *"Once a vertex $u$ is popped from the priority queue, its recorded shortest distance $dist[u]$ is permanently finalized and optimal."*

This invariant holds **if and only if all edge weights are non-negative ($w(e) \ge 0$)**. When negative edge weights exist, a longer multi-hop path can later emerge whose cumulative sum is cheaper than a direct link.

### The Concrete Counterexample

```
           [ S ] ──────── 2 ────────► [ A ]
             │                          ▲
             │                          │ -4
             5                          │
             │                          │
             ▼                          │
           [ B ] ───────────────────────┘
```

- Source node: **$S$**
- Links:
  - $S \rightarrow A$ with cost $+2$
  - $S \rightarrow B$ with cost $+5$
  - $B \rightarrow A$ with cost $-4$

#### How Dijkstra Executes (Incorrectly):
1. **Initialization**: $dist[S] = 0, dist[A] = \infty, dist[B] = \infty$.
2. **Step 1**: Pop $S$. Relax neighbors:
   - $dist[A] = 0 + 2 = 2$
   - $dist[B] = 0 + 5 = 5$
   - Min-heap contents: `[(2, A), (5, B)]`.
3. **Step 2**: Dijkstra greedily extracts the minimum element: **Node $A$ with distance $2$**.
   - **Dijkstra marks $A$ as permanently finalized ($dist[A] = 2$)**.
4. **Step 3**: Extract Node $B$ with distance $5$.
   - Relax neighbor $A$: $dist[B] + w(B, A) = 5 + (-4) = \mathbf{1}$.
   - But Node $A$ has already been finalized! Dijkstra cannot update it.

**Result**: Dijkstra outputs shortest path to $A$ as **$2$**. The true shortest path is $S \rightarrow B \rightarrow A$ with cost **$1$**. **Dijkstra fails completely.**

### Why Do Negative Weights Exist in Computer Networks?
While physical latency cannot be negative, logical costs in routing algorithms can be negative:
- **Commercial Peering Agreements**: An ISP may be paid transit revenue by a customer to carry traffic, represented as a negative cost or rebate.
- **Energy-Harvesting Networks**: A solar-powered wireless node generating surplus energy can provide a net energy gain to the network.

### Negative Cycles: The Mathematical Undecidability
If a directed cycle $C = (v_1, v_2, \dots, v_k, v_1)$ has a cumulative negative weight:

$$\sum_{e \in C} w(e) < 0$$

```
              [ A ] ─── 3 ───► [ B ]
                ▲                │
                │                │ 2
               -7                │
                │                ▼
              [ D ] ◄─── 1 ─── [ C ]
       Cycle Sum: 3 + 2 + 1 + (-7) = -1
```

A packet traversing this loop repeatedly decreases its path cost by $-1$ on each revolution.

$$\text{Cost after } 1\text{ loop} = -1, \quad \text{after } 100\text{ loops} = -100, \quad \text{after } \infty\text{ loops} = -\infty$$

**The shortest path problem on a negative cycle is ill-defined and mathematically unbounded.**

---

## 2. The Bellman-Ford Algorithm

Published independently by Alfonso Shimbel (1955), Richard Bellman (1958), and Lester Ford Jr. (1956), this algorithm computes single-source shortest paths in graphs with **arbitrary edge weights (both positive and negative)** and detects negative cycles.

### Dynamic Programming Formulation
Let $d^{(k)}(v)$ represent the shortest path distance from source $S$ to vertex $v$ using **at most $k$ edges**.

The Bellman-Ford recurrence relation:

$$d^{(k)}(v) = \min \left( d^{(k-1)}(v), \min_{u \in \text{In}(v)} \left( d^{(k-1)}(u) + w(u, v) \right) \right)$$

### Why Exactly $|V| - 1$ Relaxation Passes?
> **Fundamental Theorem**:
> In any graph with $|V|$ vertices and no negative cycles, the shortest path between any two vertices is a **simple path** (contains no cycles).
> A simple path connecting $|V|$ vertices can contain at most **$|V| - 1$ edges**.

Therefore, if we iterate through and relax **all edges** in the graph $|V| - 1$ times, every shortest path of length $1, 2, \dots, |V|-1$ edges is guaranteed to be fully discovered!

### Negative Cycle Detection at the $|V|$-th Pass
If we execute an extra **$|V|$-th relaxation pass** across all edges:
- **If no distance decreases**: The graph contains no reachable negative-weight cycles, and all distances are mathematically optimal.
- **If any distance $dist[v]$ decreases**: A negative cycle exists! The algorithm reports an error.

---

## 3. Bellman-Ford Implementation & Trace

```python
def bellman_ford(vertices, edges, source):
    # vertices: list of nodes, e.g. ['A', 'B', 'C', 'D']
    # edges: list of tuples (u, v, weight)
    
    dist = {v: float('inf') for v in vertices}
    pred = {v: None for v in vertices}
    dist[source] = 0
    
    # Relax all edges |V| - 1 times
    for pass_num in range(len(vertices) - 1):
        updated = False
        for u, v, w in edges:
            if dist[u] != float('inf') and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                pred[v] = u
                updated = True
        # Early stopping optimization
        if not updated:
            break
            
    # Step |V|: Negative Cycle Verification
    for u, v, w in edges:
        if dist[u] != float('inf') and dist[u] + w < dist[v]:
            raise ValueError("Graph contains a negative-weight cycle!")
            
    return dist, pred
```

### Complexity Breakdown
- **Time Complexity**:
  - In each pass, we iterate over all $|E|$ edges.
  - We execute at most $|V| - 1$ passes.
  - **Total Time Complexity**: $\mathbf{O(|V| \cdot |E|)}$.
- **Space Complexity**: $O(|V|)$ to store distance and predecessor arrays.

### Numerical Trace Table
- Vertices: $S, A, B, C$ ($|V| = 4 \implies |V| - 1 = 3\text{ passes}$).
- Directed Edges:
  1. $(S, A, 4)$
  2. $(S, B, 5)$
  3. $(A, C, 3)$
  4. $(B, C, -6)$
  5. $(C, A, 2)$
- Source: $S$

| Pass # | Edge Relaxed | Calculation ($dist[u] + w < dist[v]$) | Distance Array $[dist[S], dist[A], dist[B], dist[C]]$ | Updated? |
| :--- | :--- | :--- | :--- | :--- |
| **Init** | - | - | $[0, \infty, \infty, \infty]$ | - |
| **Pass 1** | $(S, A, 4)$<br>$(S, B, 5)$<br>$(A, C, 3)$<br>$(B, C, -6)$<br>$(C, A, 2)$ | $0 + 4 < \infty \implies dist[A] = 4$<br>$0 + 5 < \infty \implies dist[B] = 5$<br>$4 + 3 = 7 \implies dist[C] = 7$<br>$5 + (-6) = -1 < 7 \implies dist[C] = -1$<br>$-1 + 2 = 1 < 4 \implies dist[A] = 1$ | $[0, \mathbf{1}, \mathbf{5}, \mathbf{-1}]$ | Yes |
| **Pass 2** | All edges | $(A, C): 1 + 3 = 4 \nless -1$<br>$(B, C): 5 - 6 = -1 \nless -1$<br>$(C, A): -1 + 2 = 1 \nless 1$ | $[0, 1, 5, -1]$ | **No updates** |
| **Pass 3** | All edges | Early stopping triggered (no changes in Pass 2). | $[0, 1, 5, -1]$ | Terminated |

---

## 4. The Distributed Bellman-Ford Equation & Distance Vector Routing

Why does Bellman-Ford matter so much in networking?
Because **routers on the internet do not possess global knowledge of all topology links**.

In a decentralized network, router $x$ only talks to its direct physical neighbors $v \in \text{Neighbors}(x)$. Each neighbor shares its estimated distance vector $D_v$.

Router $x$ calculates its shortest path to any destination $y$ via the **Distributed Bellman-Ford Equation**:

$$D_x(y) = \min_{v \in \text{Neighbors}(x)} \left\{ c(x, v) + D_v(y) \right\}$$

Where:
- $c(x, v)$ is the physical link cost between router $x$ and neighbor $v$.
- $D_v(y)$ is neighbor $v$'s advertised distance to destination $y$.

This formula is the direct mathematical engine driving the **Routing Information Protocol (RIP)** and the **Border Gateway Protocol (BGP)**!

---

## 5. Minimum Spanning Trees (MST) in Networking

### What is a Minimum Spanning Tree?
Given an undirected, connected, weighted graph $G = (V, E)$, an **MST** is a subgraph $T = (V, E')$ such that:
1. It spans all vertices ($|V|$ nodes).
2. It contains **no cycles** (it is a tree, with exactly $|E'| = |V| - 1$ edges).
3. The sum of edge weights $\sum_{e \in E'} w(e)$ is **minimized**.

```
    Original Graph (With Loops)             Minimum Spanning Tree (Loop-Free)
         [ A ] ─── 1 ─── [ B ]                    [ A ] ─── 1 ─── [ B ]
           │   \       /   │                        │               │
           4     3   2     5                        │               2
           │       \       │                        │               │
         [ C ] ─── 6 ─── [ D ]                    [ C ]           [ D ]
```

### MST vs. Shortest Path Tree (Crucial Distinction!)

| Feature | Shortest Path Tree (Dijkstra) | Minimum Spanning Tree (Kruskal/Prim) |
| :--- | :--- | :--- |
| **Goal** | Minimize distance from **one source** to all nodes | Minimize the **total cable/infrastructure cost** |
| **Root Dependency** | Dependent on the choice of source root $S$ | Global property of the graph (no source node needed) |
| **Link Weight Sum** | May have higher total sum of edge weights | Guaranteed lowest possible sum of edge weights |

---

## 6. Kruskal's vs. Prim's Algorithm

### Kruskal’s Algorithm (Edge-Centric Greedy)
1. Sort all edges in non-decreasing order of weight: $w(e_1) \le w(e_2) \le \dots \le w(e_m)$.
2. Initialize an empty forest where every node is in its own disjoint set.
3. For each edge $(u, v)$:
   - Check if $u$ and $v$ belong to the same set using **Disjoint Set Union (DSU / Union-Find)**.
   - If in different sets: Add $(u, v)$ to MST and merge their sets (`union(u, v)`).
   - If in the same set: Discard edge (adding it would create a cycle).
4. Stop when $|V| - 1$ edges are added.

- **Time Complexity**: $O(|E| \log |E|) = O(|E| \log |V|)$ due to edge sorting.

### Prim’s Algorithm (Vertex-Centric Greedy)
1. Pick an arbitrary starting node and add it to the visited tree set $S$.
2. Maintain a min-heap of all edges crossing the cut from $S$ to $V \setminus S$.
3. Greedily extract the cheapest edge $(u, v)$ where $u \in S$ and $v \notin S$.
4. Add $v$ to $S$, add edge to MST, and push $v$'s adjacent edges to the heap.
5. Repeat until all vertices are in $S$.

- **Time Complexity**: $O((|V| + |E|) \log |V|)$ with a binary min-heap.

---

## 7. Spanning Tree Protocol (STP - IEEE 802.1D)

In local area networks (LANs), network engineers install redundant physical links between Ethernet switches to survive cable cuts.
However, **redundant links create physical Layer 2 loops**.

### Why Layer 2 Loops Are Catastrophic
1. **Broadcast Storms**: When a PC sends an ARP request (`FF:FF:FF:FF:FF:FF`), switches flood it out all ports. In a loop, the broadcast multiplies exponentially, consuming 100% of network bandwidth within seconds.
2. **MAC Table Thrashing / Flapping**: A switch learns MAC addresses by inspecting the source MAC of incoming frames. When duplicate frames arrive alternately on Port 1 and Port 2, the switch repeatedly overwrites its MAC table, locking up the CPU.
3. **Duplicate Frame Delivery**: Applications receive multiple copies of identical unicast frames, corrupting state.

> **Why L3 Routers Don't Have Broadcast Storms**: IP packets have a **TTL (Time to Live)** header field decremented at every hop. When TTL reaches 0, the packet is destroyed. **Ethernet Layer 2 frames have NO TTL!** A looping frame circles the wire forever until a switch is rebooted.

```
                  [ Root Bridge Switch A ]
                       /            \
           Designated /              \ Designated
              Port   /                \   Port
                    ▼                  ▼
             [ Switch B ] ──────── [ Switch C ]
                          (BLOCKING)
                    One redundant port is logically
                    blocked to break the loop!
```

### How STP Works: 4 Sequential Steps
Every 2 seconds, switches exchange **Bridge Protocol Data Units (BPDUs)**:

1. **Elect One Root Bridge**:
   - The switch with the lowest **Bridge ID (BID)** wins.
   - $\text{Bridge ID} = \text{Bridge Priority (default 32768)} + \text{MAC Address}$.
   - Lowest MAC address wins tiebreakers.
2. **Elect One Root Port (RP) per Non-Root Switch**:
   - The single port on each switch with the lowest cumulative path cost to the Root Bridge.
3. **Elect One Designated Port (DP) per Link Segment**:
   - The switch port on a segment that advertises the lowest cost to the Root Bridge. (All active ports on the Root Bridge are DPs).
4. **Block All Remaining Ports (Alternate / Blocking Ports)**:
   - Any port that is neither an RP nor a DP is put into the **BLOCKING State**.
   - A blocking port listens for BPDUs to detect link failures, but **drops all data frames**, cleanly breaking the loop!

---

## 8. Master Algorithm Comparison Matrix

| Algorithm | Problem Solved | Weights Allowed | Time Complexity | Real-World Network Use Case |
| :--- | :--- | :--- | :--- | :--- |
| **BFS** | Shortest Path (Unweighted) | Uniform ($w = 1$) | $O(V + E)$ | Minimum-hop routing, P2P peer discovery |
| **Dijkstra** | Single-Source Shortest Path | Non-negative ($w \ge 0$) | $O((V + E) \log V)$ | **OSPF**, **IS-IS** Link-State routing |
| **Bellman-Ford** | Single-Source Shortest Path | Arbitrary (Negatives OK) | $O(V \cdot E)$ | **RIP**, **BGP** Distance Vector routing |
| **Floyd-Warshall**| All-Pairs Shortest Path | Arbitrary (No neg cycles) | $O(V^3)$ | Centralized SDN global traffic matrix computation |
| **Kruskal / Prim**| Minimum Spanning Tree | Arbitrary undirected | $O(E \log V)$ | Multicast tree construction, physical WAN design |
| **STP (802.1D)** | Distributed MST on Switches | Port cost weights | Distributed | **Layer 2 loop prevention & redundancy** |

---

## 📌 Summary Checklist & Exam Cram Notes

1. **Dijkstra Failure**: Fails on negative weights because its greedy choice assumes finalized distances can never decrease.
2. **Negative Cycle**: A cycle whose edge sum is negative, causing shortest path costs to plunge toward $-\infty$.
3. **Bellman-Ford Invariant**: Relaxes all $|E|$ edges $|V|-1$ times; dynamic programming guarantees finding all simple shortest paths.
4. **Negative Cycle Test**: If any edge relaxes during pass $|V|$, a negative cycle is present.
5. **Distributed Bellman-Ford**: $D_x(y) = \min_v \{ c(x, v) + D_v(y) \}$, basis of Distance Vector protocols.
6. **MST Property**: Connects all $|V|$ nodes using $|V|-1$ edges with minimum cumulative weight without cycles.
7. **Kruskal’s**: Sorts edges; adds cheapest non-cycle edge using DSU ($O(E \log V)$).
8. **Prim’s**: Grows tree vertex by vertex using a min-heap ($O(E \log V)$).
9. **Layer 2 Loops**: Fatal because Ethernet frames have no TTL, resulting in catastrophic broadcast storms.
10. **STP Core Mechanics**: Elects Root Bridge (lowest BID), elects Root Ports and Designated Ports, blocks alternate ports.

---

## 🧠 Practice Problems & Self-Check Questions

1. In a network with 5 routers and 7 links, what is the maximum number of edge relaxations Bellman-Ford will perform in the worst case?
2. Why is Dijkstra's algorithm preferred over Bellman-Ford in OSPF routers, given that Bellman-Ford can handle more general edge weights?
3. A switch has MAC `00:1A:2B:3C:4D:5E` and priority `32768`. Another switch has MAC `00:1A:2B:3C:4D:5F` and priority `4096`. Which switch becomes the STP Root Bridge? Why?
4. Can an MST have multiple different topologies for the same graph? Under what condition is the MST guaranteed to be strictly unique?
5. What would happen on a modern enterprise campus network if an administrator disabled Spanning Tree Protocol on all access switches?
