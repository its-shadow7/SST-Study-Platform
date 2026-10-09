# Lecture 8: Routing and Forwarding II
## Student Notes — SST Computer Networks (Term 5)

---

## 🎯 Learning Objectives

By the end of this lecture, you should be able to:
- Formulate the architecture of **Distance Vector Routing Protocols** and analyze the operational mechanics of **RIP (Routing Information Protocol)**.
- Dissect the **Count-to-Infinity Problem** and trace how routing loops emerge step-by-step following link failures.
- Implement and evaluate loop mitigation techniques: **Split Horizon, Poison Reverse, Hold-Down Timers**, and **Triggered Updates**.
- Master **Link-State Routing Protocols** and trace **OSPF (Open Shortest Path First)** neighbor adjacencies, LSA flooding, and LSDB synchronization.
- Explain **OSPF Area Hierarchies** (Area 0 Backbone, ABRs, ASBRs) and the role of **Designated Routers (DR/BDR)** in multi-access networks.
- Distinguish between **Interior Gateway Protocols (IGP)** and **Exterior Gateway Protocols (EGP)**.
- Analyze **BGP (Border Gateway Protocol)** as a **Path Vector** protocol, explaining how the `AS_PATH` attribute eliminates loops and enforces economic peering policies.

---

## 1. Distance Vector Routing Protocols

### The Core Paradigm: "Routing by Rumor"
In a **Distance Vector (DV)** protocol, routers do not possess a global topographical map of the entire network. Instead, each router:
1. Maintains an array (vector) of estimated distances to all known destinations.
2. Periodically transmits its **entire routing table** to its directly connected immediate neighbors.
3. Updates its local table using the **Distributed Bellman-Ford Equation**:

   $$D_x(y) = \min_{v \in \text{Neighbors}(x)} \left\{ c(x, v) + D_v(y) \right\}$$

Because routers blindly accept distance claims from neighbors without independently verifying the path, distance vector protocols are colloquially called **"routing by rumor"**.

```
  [ Router A ] ──(Shares full table every 30s)──► [ Router B ]
  "I can reach Subnet X in 1 hop"               "A says it can reach X in 1 hop,
                                                 so I can reach X via A in 2 hops!"
```

### The Canonical Implementation: RIP (RFC 1058 / RFC 2453)
**RIP (Routing Information Protocol)** is the classic distance vector protocol:
- **Metric**: Pure **Hop Count** (each router traversed = $1$ hop).
- **Maximum Metric / Infinity**: **16 hops**. Any destination with a metric of $16$ is classified as unreachable.
- **Update Frequency**: Broadcasts or multicasts (`224.0.0.9` in RIPv2) its full table every **30 seconds** via UDP port **520**.
- **Timers**:
  - **Update Timer**: $30\text{ seconds}$.
  - **Invalid / Timeout Timer**: $180\text{ seconds}$ (marks route as metric 16 if no update heard).
  - **Flush Timer**: $240\text{ seconds}$ (purges route completely from RIB).

---

## 2. The Count-to-Infinity Problem & Routing Loops

The fundamental vulnerability of distance vector routing is its **slow convergence** upon network topology degradation, leading to the **Count-to-Infinity Problem**.

### Step-by-Step Failure Scenario

```
[ Router A ] ─── 1 ─── [ Router B ] ─── 1 ─── [ Router C ] ─── 1 ─── [ Subnet X ]
```

- In steady state:
  - $C$ reaches $X$ with metric **1** (Direct).
  - $B$ reaches $X$ via $C$ with metric **2**.
  - $A$ reaches $X$ via $B$ with metric **3**.

#### The Catastrophe: Link $C \leftrightarrow X$ Fails

```
               Link FAILS!
[ A ] ─── 1 ─── [ B ] ─── 1 ─── [ C ] ─── X ─── [ Subnet X ]
```

1. **Time $t = 0$**: The link connecting Router $C$ to Subnet $X$ physically snaps.
   - Router $C$ marks Subnet $X$ as unreachable ($\text{metric} = 16$).
2. **Time $t = 1$**: Before Router $C$ can broadcast this failure, Router $B$’s routine 30-second timer expires.
   - Router $B$ sends its periodic update to Router $C$: *"I can reach Subnet X with metric 2!"*
   - Note: Router $B$ doesn't realize its path to $X$ depended entirely on $C$!
3. **Time $t = 2$**: Router $C$ receives $B$'s update.
   - $C$ reasons: *"My direct link is down, but my neighbor $B$ claims it has a path to $X$ of cost 2! Therefore, I will route through $B$ with cost $2 + 1 = 3$!"*
   - Router $C$ installs: `Subnet X via B, metric = 3`.
4. **Time $t = 3$**: Router $C$ sends its next update to Router $B$: *"I can reach Subnet X with metric 3!"*
   - Router $B$ reasons: *"My path through $C$ increased to 3, so my new cost is $3 + 1 = 4$!"*
   - Router $B$ installs: `Subnet X via C, metric = 4`.
5. **Time $t = 4$ to $t = 15$**:
   - $B$ updates $C \implies C$ sets metric to **5**.
   - $C$ updates $B \implies B$ sets metric to **6**.
   - $B$ and $C$ bounce the metric back and forth in an infinite loop, slowly incrementing until the metric reaches **16 (Infinity)**!

> **Impact on Real Traffic**: While counting to 16, if a packet for Subnet $X$ arrives at Router $B$, $B$ forwards it to $C$, and $C$ forwards it right back to $B$. The packet bounces between $B$ and $C$ in a tight Layer 3 loop until its IP TTL decrements to 0, saturating the link bandwidth.

---

## 3. Loop Mitigation Mechanisms in Distance Vector

To counteract the Count-to-Infinity pathology, routing engineers developed four core defense mechanisms:

```
┌─────────────────────────┬────────────────────────────────────────────────────────┐
│ Technique               │ Architectural Defense Rule                             │
├─────────────────────────┼────────────────────────────────────────────────────────┤
│ **Split Horizon**       │ Never advertise a route back out the same interface    │
│                         │ from which it was originally learned.                  │
├─────────────────────────┼────────────────────────────────────────────────────────┤
│ **Poison Reverse**      │ Explicitly advertise the route back to the sender with │
│                         │ metric = 16 (Infinity / Poisoned).                     │
├─────────────────────────┼────────────────────────────────────────────────────────┤
│ **Hold-Down Timers**    │ When a route is marked down, freeze and ignore all new │
│                         │ updates for that route for a set stabilization window. │
├─────────────────────────┼────────────────────────────────────────────────────────┤
│ **Triggered Updates**   │ Transmit immediate update packets the microsecond a    │
│                         │ link fails, rather than waiting for the 30s timer.     │
└─────────────────────────┴────────────────────────────────────────────────────────┘
```

### 1. Split Horizon
- **Rule**: If Router $B$ learns about Subnet $X$ through Router $C$ on interface `eth1`, Router $B$ **must never advertise Subnet $X$ back out interface `eth1` to Router $C$**.
- **Effect**: In our failure scenario, Router $B$ never tells $C$ that it can reach $X$. $C$ will never mistakenly assume $B$ has an alternate path.

### 2. Split Horizon with Poison Reverse
- Rather than remaining silent, Router $B$ explicitly advertises `Subnet X: metric = 16` out interface `eth1` to $C$.
- **Advantage**: Overcomes potential timing race conditions by actively poisoning the reverse direction.

### 3. Hold-Down Timers
- When a router receives an update indicating a route is unreachable, it starts a **Hold-Down Timer** (typically 180 seconds in RIP).
- During this window, the router **refuses to accept any new path updates for that subnet** unless the update has an equal or better metric than the original pre-failure path.
- This gives the entire network sufficient time to flush stale routing loops before any router attempts to recalculate alternate routes.

---

## 4. Link-State Routing: The OSPF Architecture

Because distance vector protocols scale poorly and suffer from convergence delays, modern enterprise networks deploy **Link-State Routing Protocols**, predominantly **OSPF (Open Shortest Path First - RFC 2328)**.

### The Link-State Philosophy: "Global Map & Independent Calculation"
Unlike distance vector:
1. Routers do **NOT** exchange routing tables.
2. Routers exchange **Link-State Advertisements (LSAs)** describing only their own immediate interfaces and neighbors.
3. Every router floods these LSAs throughout the area until **every single router possesses an identical synchronized Link-State Database (LSDB)**.
4. Each router independently runs **Dijkstra’s Algorithm** on its local LSDB to compute its own shortest-path tree rooted at itself.

```
       [ Router A ]                    [ Router B ]
            │                               │
            └── Both build identical LSDB ──┘
                   (Global Network Map)
                            │
              Runs Dijkstra Locally in CPU
                            │
                            ▼
              Builds Unique Forwarding Table
```

### The 5 OSPF Packet Types & Neighbor Adjacency
OSPF runs directly on top of raw IP using **Protocol Number 89** (no TCP/UDP overhead).

1. **Hello Packet (Type 1)**: Sent every 10 seconds to multicast `224.0.0.5`. Discovers neighbors and verifies bidirectional connectivity.
2. **Database Description / DBD (Type 2)**: Summary list of the router’s LSDB contents.
3. **Link State Request / LSR (Type 3)**: Requests specific missing LSAs from a neighbor.
4. **Link State Update / LSU (Type 4)**: Carries the actual full LSAs across the wire.
5. **Link State Acknowledgment / LSAck (Type 5)**: Guarantees reliable transport across links.

### The OSPF Adjacency State Machine:

$$\text{Down} \rightarrow \text{Init} \rightarrow \text{2-Way} \rightarrow \text{ExStart} \rightarrow \text{Exchange} \rightarrow \text{Loading} \rightarrow \mathbf{Full}$$

- **Full State**: Routers have completely synchronized their databases and are fully functional.

---

## 5. Scalability: OSPF Areas & DR/BDR Election

### OSPF Two-Tier Hierarchical Areas
If a network contains 5,000 routers, running Dijkstra across the entire topology would consume massive CPU power, and a single flapping link would trigger continuous network-wide SPF recalculations.
OSPF solves this through **Hierarchical Areas**:

```
                         [ Area 0 (Backbone) ]
                        /                     \
             [ ABR Router 1 ]             [ ABR Router 2 ]
                   /                               \
        [ Area 1 (Engineering) ]          [ Area 2 (Sales) ]
```

- **Area 0 (Backbone Area)**: The mandatory core of the network. All other areas must physically connect to Area 0.
- **Area Border Router (ABR)**: A router with interfaces in Area 0 and a non-backbone area. ABRs summarize internal area routes and contain SPF calculations strictly within the originating area.
- **Autonomous System Boundary Router (ASBR)**: A router that connects the OSPF domain to external networks (e.g., redistributing BGP or static routes).

### DR and BDR in Broadcast Multi-Access Networks
On a shared Ethernet segment with $N$ routers, establishing direct neighbor adjacencies between every pair would produce:

$$\text{Total Adjacencies} = \frac{N(N - 1)}{2} = O(N^2)$$

For 10 routers, that is 45 redundant adjacencies flooding duplicate LSAs.

OSPF elects:
- **Designated Router (DR)**: Central hub router that receives all LSAs and redistributes them.
- **Backup Designated Router (BDR)**: Standby router that immediately assumes DR duties if the DR fails.
- All other routers (**DROthers**) form adjacencies **ONLY with the DR and BDR** using multicast address `224.0.0.6`:

$$\text{Total Adjacencies Reduced to: } 2N - 3 = O(N)$$

---

## 6. Inter-Domain Routing & BGP (Border Gateway Protocol)

### Interior Gateway Protocols (IGP) vs. Exterior Gateway Protocols (EGP)
- **IGP (OSPF, IS-IS, RIP)**: Operates inside a single organization or **Autonomous System (AS)**. Goal: Find the mathematically fastest, lowest-cost path.
- **EGP (BGP)**: Connects different Autonomous Systems across the global internet. Goal: Enforce **commercial routing policies, legal jurisdictions, and financial contracts**.

### What is an Autonomous System (AS)?
An **Autonomous System** is a collection of connected IP routing networks under the control of a single administrative entity (e.g., Google is `AS15169`, Cloudflare is `AS13335`, MIT is `AS3`).
- Identified by an **ASN (Autonomous System Number)**: 16-bit ($1 - 65,535$) or 32-bit ($1 - 4,294,967,295$).

```
   [ AS 15169: Google ] ◄──── eBGP Peering ────► [ AS 13335: Cloudflare ]
            │                                              │
       (Runs OSPF)                                    (Runs IS-IS)
```

### BGP as a Path Vector Protocol
BGP (RFC 4271) runs over **TCP Port 179**. It is neither pure Distance Vector nor Link State; it is a **Path Vector Protocol**.

Instead of advertising hop counts, BGP advertises the **complete sequence of Autonomous System Numbers** traversed to reach a destination prefix via the **`AS_PATH`** attribute:

$$\text{Route Advertisement for } 142.250.0.0/15: \quad \mathbf{AS\_PATH = [7018, 1299, 15169]}$$

### How `AS_PATH` Guarantees Instant Loop Elimination:
> When router $R$ in `AS 7018` receives a BGP advertisement:
> It inspects the `AS_PATH` array.
> **If its own ASN (`7018`) appears anywhere inside the list, the router INSTANTLY DISCARDS THE ROUTE!**
> Because it sees its own identity, accepting the route would create a routing loop between Autonomous Systems.

### Key BGP Path Attributes

| Attribute | Category | Description & Purpose |
| :--- | :--- | :--- |
| **`AS_PATH`** | Well-Known Mandatory | Sequence of ASNs traversed. Used for loop detection and shortest AS-hop selection. |
| **`NEXT_HOP`** | Well-Known Mandatory | IP address of the gateway router to use to reach the next AS. |
| **`LOCAL_PREF`** | Well-Known Discretionary | Inbound preference configured internally within an AS (Higher = Preferred). Used to prefer customer routes over peer routes. |
| **`MED`** | Optional Non-Transitive | Multi-Exit Discriminator ("Metric"): Informs an adjacent AS which of multiple ingress points to choose (Lower = Preferred). |

---

## 7. Master Routing Protocol Comparison Matrix

| Dimension | RIPv2 | OSPFv2 | BGP-4 |
| :--- | :--- | :--- | :--- |
| **Type** | Distance Vector | Link-State | Path Vector |
| **Algorithm** | Bellman-Ford | Dijkstra (SPF) | Policy-based Path Vector |
| **Scope** | Small IGP ($< 15$ hops) | Enterprise / Data Center IGP | Global Internet EGP |
| **Transport Layer** | UDP Port 520 | Raw IP (Protocol 89) | **TCP Port 179** |
| **Metric** | Hop Count (Max 15) | Cost (Inverse Bandwidth) | Policy Attributes (`LOCAL_PREF`, `AS_PATH`, `MED`) |
| **Convergence** | Very Slow (Minutes) | Fast (Milliseconds to Seconds) | Moderate (Dampened to prevent global flap) |
| **Loop Prevention** | Split Horizon, Poison Reverse | Loop-free Dijkstra Tree | `AS_PATH` Self-Detection |
| **Hierarchy** | Flat | Two-Tier (Area 0 + Sub-Areas) | Autonomous Systems (eBGP vs. iBGP) |

---

## 📌 Summary Checklist & Exam Cram Notes

1. **Distance Vector Principle**: "Routing by rumor"; routers periodically share entire tables with direct neighbors.
2. **RIP Constants**: Max metric 15 hops; 16 is infinity; periodic updates every 30 seconds over UDP 520.
3. **Count-to-Infinity**: Occurs when routers create mutual loops following link failure, incrementing costs up to 16.
4. **Loop Solutions**: Split Horizon (don't advertise back), Poison Reverse (advertise back as 16), Hold-down timer (freeze route updates).
5. **Link-State Principle**: Synchronize identical LSDB across all routers; run Dijkstra locally to generate shortest-path tree.
6. **OSPF Packets**: Hello (1), DBD (2), LSR (3), LSU (4), LSAck (5). Runs over IP protocol 89.
7. **OSPF Areas**: Area 0 (Backbone) is mandatory; ABR connects Area 0 to standard areas to contain LSA flooding.
8. **DR/BDR Election**: Reduces $O(N^2)$ neighbor adjacencies to $O(N)$ on shared Ethernet broadcast networks.
9. **Path Vector & BGP**: Routes internet traffic between Autonomous Systems using TCP 179; `AS_PATH` prevents loops.
10. **BGP Decision Priority**: `LOCAL_PREF` (highest) $\rightarrow$ Shortest `AS_PATH` $\rightarrow$ `MED` (lowest).

---

## 🧠 Practice Problems & Self-Check Questions

1. In a 3-router line topology ($A - B - C$), Router $C$’s connection to Subnet $Z$ fails. If Split Horizon is disabled, explain what Router $B$ advertises to $C$ and how long it takes for RIP to converge if timers are standard.
2. Why does OSPF consume more CPU RAM and processing power than RIP? Why is this trade-off acceptable in modern networks?
3. On an Ethernet switch connecting 8 OSPF routers, how many total neighbor adjacencies would form if DR/BDR were not elected? How many form with a DR and BDR?
4. How does BGP prevent routing loops across the internet without running Dijkstra’s algorithm?
5. A network engineer wants to force all outbound internet traffic from their university to exit through ISP 1 rather than ISP 2. Which BGP attribute should they configure on their border routers?
