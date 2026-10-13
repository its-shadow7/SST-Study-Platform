# Intra-Domain and Inter-Domain Routing Protocols (RIP, OSPF, BGP)
**Term:** Term 5 | **Subject:** CN | **Note ID:** `cn-t5-l08`
**Last Updated:** 2026-10-13T00:00:00Z

## Abstract & Summary
An exhaustive, rigorous masterclass on dynamic routing algorithms and protocols that power global telecommunications. Covers Distance Vector protocols and RIP convergence, the Count-to-Infinity pathology and its mathematical remedies, Link State routing and multi-area OSPF hierarchical engineering, and Border Gateway Protocol (BGP) path-vector mechanics, route selection policy hierarchies, and prefix hijacking defenses.

## Learning Objectives
- Classify dynamic routing protocols into Interior Gateway Protocols (IGP) and Exterior Gateway Protocols (EGP).
- Explain Distance Vector routing mechanics and trace distributed Bellman-Ford table updates in RIP.
- Diagnose the Count-to-Infinity routing loop pathology and evaluate engineering fixes: Split Horizon, Poison Reverse, Triggered Updates, and Holddown Timers.
- Analyze Link State routing and OSPF operation: Hello neighbor discovery, LSA flooding, LSDB synchronization, and Dijkstra SPF calculation.
- Compute OSPF link costs using reference bandwidth formulas and design hierarchical multi-area OSPF topologies with Area 0 backbones and ABRs.
- Evaluate Border Gateway Protocol (BGP) as a path-vector inter-domain protocol: Autonomous Systems (ASNs), AS-PATH loop prevention, peering vs. transit economics, and the BGP best-path decision algorithm.
- Examine Internet security vulnerabilities including BGP prefix hijacking and cryptographic defenses via Resource Public Key Infrastructure (RPKI).

## Key Takeaways
- Routing protocols are divided into IGPs (operating within a single Autonomous System: RIP, OSPF, IS-IS) and EGPs (operating between independent Autonomous Systems: BGP).
- Distance Vector protocols (RIP) share entire routing vectors with direct neighbors using distributed Bellman-Ford; they suffer from slow convergence and Count-to-Infinity upon link failure.
- Split Horizon ('never advertise a route back to the neighbor from whom it was learned') and Poison Reverse ('advertise the route back with metric infinity = 16') mitigate two-node Count-to-Infinity loops.
- Link State protocols (OSPF) flood Link State Advertisements (LSAs) so every router builds an identical Link State Database (LSDB) of the network topology, then independently runs Dijkstra's algorithm to compute loop-free shortest paths.
- OSPF scales to massive enterprise topologies using hierarchical areas connected to Area 0 (Backbone); Area Border Routers (ABRs) summarize routes and restrict LSA flooding domains.
- BGP is a Path-Vector EGP where policy, business relationships, and economics dictate routing decisions; the AS-PATH attribute guarantees inter-domain loop prevention by dropping any announcement containing the receiving router's own ASN.
- BGP prefix hijacking exploits the Longest Prefix Match rule when an attacker maliciously announces a more specific prefix (/24); RPKI cryptographic Route Origin Authorizations (ROAs) provide mathematical origin authentication.

---

## Taxonomy of Routing Protocols: IGP vs. EGP
### The Global Routing Architecture

The global Internet cannot function as a single monolithic flat network running a uniform routing protocol. Millions of routers would exhaust their memory processing link state advertisements, and independent commercial organizations (ISPs, governments, universities) refuse to disclose their internal network topologies to competitors.

To solve scalability and administrative sovereignty, the Internet is structured as a two-tier hierarchy of **Autonomous Systems (ASes)**:

```
┌────────────────────────────────────────────────────────────────────────┐
│                     GLOBAL INTERNET HIERARCHY                          │
│                                                                        │
│      [ AS 15169: Google ]                     [ AS 13335: Cloudflare ]  │
│      (Interior: OSPF / IS-IS)                 (Interior: OSPF / IS-IS) │
│               │                                        │               │
│               └──────────────────┬─────────────────────┘               │
│                                  ▼                                     │
│                    INTER-DOMAIN: BGP-4 (EGP)                           │
│                                  ▲                                     │
│               ┌──────────────────┴─────────────────────┐               │
│               │                                        │               │
│      [ AS 55836: Reliance Jio ]               [ AS 9498: Bharti Airtel]│
│      (Interior: OSPF / IS-IS)                 (Interior: OSPF / IS-IS) │
└────────────────────────────────────────────────────────────────────────┘
```

#### Protocol Classification Matrix

| Classification | Protocol Family | Primary Protocols | Algorithmic Basis | Scope & Objective |
| :--- | :--- | :--- | :--- | :--- |
| **Interior Gateway Protocol (IGP)** | **Distance Vector** | RIPv1, RIPv2, IGRP | Distributed Bellman-Ford | Within a single AS; optimizes for minimum hop count; simple, low CPU overhead. |
| **Interior Gateway Protocol (IGP)** | **Link State** | OSPFv2, OSPFv3, IS-IS | Dijkstra's Shortest Path First (SPF) | Within a single AS; optimizes for bandwidth/latency; rapid sub-second convergence, full topology visibility. |
| **Interior Gateway Protocol (IGP)** | **Advanced Distance Vector** | EIGRP | DUAL (Diffusing Update Algorithm) | Cisco proprietary (later informational); combines distance vector simplicity with link state speed. |
| **Exterior Gateway Protocol (EGP)** | **Path Vector** | BGP-4 (Border Gateway Protocol) | Policy-Driven Path Vector | Between autonomous systems; optimizes for commercial transit agreements, peering policies, and path vector security. |

### What is an Autonomous System (AS)?
An **Autonomous System (AS)** is a collection of connected IP routing prefixes under the control of a single administrative entity (e.g., an Internet Service Provider, a multinational enterprise, or a university campus) that presents a clearly defined, unified routing policy to the Internet.
- Every public AS is assigned a globally unique **Autonomous System Number (ASN)** by regional internet registries (ARIN, RIPE NCC, APNIC).
- **2-Byte ASNs**: Range $1$ to $65,535$ (RFC 1930; exhausted).
- **4-Byte ASNs**: Range $65,536$ to $4,294,967,295$ (RFC 6793).
- **Examples**: Google is `AS15169`, Cloudflare is `AS13335`, Microsoft is `AS8075`, Reliance Jio is `AS55836`.

**Citations & References:**
- RFC 1930: Guidelines for Creation, Selection, and Registration of an Autonomous System (AS)
- RFC 6793: BGP Support for Four-Octet Autonomous System (AS) Number Space
- Computer Networks: A Systems Approach (Larry Peterson & Bruce Davie), Chapter 4 (Global Internetworking)

---

## Distance Vector Routing & RIP (Routing Information Protocol)
### The Principle of Distance Vector Routing

In Distance Vector (DV) routing, routers operate according to a decentralized, distributed implementation of the **Bellman-Ford algorithm**:
1. Each router knows only the cost to its directly attached physical neighbors.
2. Periodically, each router broadcasts or multicasts its **entire routing table** (its distance vector) to its immediate neighbors.
3. Upon receiving a distance vector from neighbor $v$, router $x$ updates its shortest distance to destination $y$ via the Bellman-Ford optimality equation:
   $$D_x(y) = \min_{v \in \text{Neighbors}(x)} \big( c(x, v) + D_v(y) \big)$$

```
         Router A ──────(cost=1)────── Router B ──────(cost=1)────── Router C
  Distance Vector:               Distance Vector:               Distance Vector:
  {A:0, B:1, C:∞}                {A:1, B:0, C:1}                {A:∞, B:1, C:0}
```

### RIP Architecture & Specifications

The **Routing Information Protocol (RIP)** is the classic textbook implementation of Distance Vector routing defined in RFC 1058 (RIPv1) and RFC 2453 (RIPv2).

#### RIP Architectural Parameters
- **Metric**: Hop count exclusively (every link has a static cost of $1$).
- **Maximum Hop Count**: $15$ hops. A hop count of $\mathbf{16}$ represents **infinity** (unreachable destination). This deliberately limits the diameter of RIP networks.
- **Periodic Update Timer**: Broadcasts or multicasts its complete routing table every **30 seconds**.
- **Route Invalid Timer**: $180$ seconds. If no update is heard for a route within $180$s, its metric is set to $16$.
- **Flush Timer**: $240$ seconds. The route is permanently purged from the routing table.
- **Transport Protocol**: Operates at Layer 7 using UDP port **520**.

#### Evolution: RIPv1 vs. RIPv2

| Specification | RIP Version 1 (RFC 1058) | RIP Version 2 (RFC 2453) |
| :--- | :--- | :--- |
| **Addressing Paradigm** | Strictly Classful (Class A, B, C) | Classless Inter-Domain Routing (CIDR) & VLSM |
| **Subnet Mask Inclusion** | Omits subnet mask in updates | Explicitly carries 32-bit subnet mask |
| **Transmission Mode** | Layer 2/3 Broadcast (`255.255.255.255`) | Layer 3 Multicast (`224.0.0.9`) |
| **Authentication** | None (insecure) | Plaintext and MD5 cryptographic authentication |
| **Route Tagging** | Not supported | Supports external route tags (for redistribution) |

**Citations & References:**
- RFC 1058: Routing Information Protocol (RIPv1)
- RFC 2453: RIP Version 2 (RIPv2)
- Computer Networking: A Top-Down Approach (Kurose & Ross), Chapter 5.2 (Distance-Vector Routing)

---

## The Count-to-Infinity Pathology & Engineering Remedies
### The Slow Convergence Dilemma

While Distance Vector protocols converge smoothly when link costs improve ('good news travels fast'), they suffer from catastrophic routing loops and prolonged convergence delays when links degrade or fail ('bad news travels slowly'). This breakdown is known as the **Count-to-Infinity problem**.

### Detailed 3-Node Failure Trace

Consider three linear routers interconnected with link costs equal to $1$:
```
   Router A ────────(1)──────── Router B ────────(1)──────── Router C (10.1.1.0/24)
```

**Steady-State Convergence**:
- Router B: Destination C has metric $1$, Next Hop = Direct (Interface to C).
- Router A: Destination C has metric $2$, Next Hop = B.

**Link B–C Severed**:
1. Link B–C drops physically. Router B detects the break and sets its internal distance to C as $\infty$ ($16$).
2. **The Race Condition**: Before Router B can send an update to Router A, Router A's periodic 30-second timer expires. Router A sends its regular distance vector to B: `Destination C = 2 hops`.
3. **Router B's Fallacy**: Router B examines A's advertisement: *"Router A claims it can reach C in 2 hops! If I route through A, I can reach C in $1 + 2 = 3$ hops!"*
4. Router B updates its routing table: `Destination C = 3 hops, Next Hop = A`.
5. Router B sends its updated table to Router A: `Destination C = 3 hops`.
6. **Router A's Fallacy**: Router A sees B's update: *"My next hop B says the cost to C increased to 3. Therefore, my cost to C is now $1 + 3 = 4$ hops!"*
7. Routers A and B bounce packets for C between each other in a persistent Layer 3 loop. With each 30-second timer interval, the metric increments: $3, 4, 5, 6, 7 \dots$
8. The loop persists until the metric finally increments to **16** (infinity in RIP), taking up to $16 \times 30 = 480$ seconds (8 minutes) during which network bandwidth is saturated!

```
Time 0:   B-C Link Fails. B sets C=16.
Time 1:   A advertises C=2 to B.
Time 2:   B updates: C = 1 + 2 = 3, Next Hop = A.
Time 3:   B advertises C=3 to A.
Time 4:   A updates: C = 1 + 3 = 4, Next Hop = B.
... Bounces repeatedly until C reaches 16 (Infinity) ...
```

### The Four Engineering Solutions

#### 1. Split Horizon Rule
**Rule**: *A router must NEVER advertise a route back out the same interface through which it learned that route.*
- Router A learned its path to C through Router B. Under Split Horizon, when Router A sends its routing updates out the interface toward B, it **omits destination C entirely**.
- When link B–C fails, B never hears a bogus advertisement from A claiming A can reach C. B keeps $C = \infty$, preventing the loop from forming.

#### 2. Poison Reverse
**Rule**: *Instead of omitting the route, a router explicitly advertises the route back to the source with a metric of INFINITY (16).*
- When Router A sends its update to B, it explicitly advertises: `Destination C = 16`.
- This actively informs B: *"You are my gateway to C; do not attempt to use me as a backup path to C!"*
- Poison reverse consumes slightly more bandwidth than split horizon but immediately breaks two-node loops.

#### 3. Triggered Updates (Route Poisoning)
- Standard updates occur every 30 seconds. With **Triggered Updates**, the moment Router B detects link B–C failure, it **immediately** transmits an unsolicited update to all neighbors with `Destination C = 16` without waiting for the 30-second timer.
- This drastically reduces the timing window during which stale updates can trigger Count-to-Infinity.

#### 4. Holddown Timers
- When a router receives an update indicating a destination has become unreachable (metric 16), it initiates a **Holddown Timer** (typically 180 seconds in RIP).
- During this holddown window, the router **refuses to accept any new route advertisements** for that destination unless the new route has a better metric than the original pre-failure metric.
- This allows bad news to fully propagate across the entire autonomous system before any router accepts new routing announcements.

**Citations & References:**
- RFC 1058: Routing Information Protocol, Section 2.2.2 (Split Horizon and Poisoned Reverse)
- Computer Networks: A Systems Approach, Chapter 4.2 (Distance-Vector / RIP)
- Interconnections: Bridges, Routers, Switches, and Internetworking Protocols (Radia Perlman), Chapter 9

---

## Link State Routing & Open Shortest Path First (OSPF)
### The Link State Philosophy: Complete Global Awareness

Distance Vector routers have 'routing by rumor'—they know only what their neighbors tell them, with zero visibility into the broader network graph. In contrast, **Link State** protocols give every router a complete, identical mathematical map of the entire network topology.

```
┌────────────────────────────────────────────────────────────────────────┐
│                      THE 5-STEP OSPF LIFECYCLE                         │
│                                                                        │
│  Step 1: Neighbor Discovery ──► Hello packets exchange on link        │
│  Step 2: Adjacency Formation ──► Exchange DBD, LSR, LSU packets        │
│  Step 3: LSA Flooding ───────► Flood Link State Advertisements to area│
│  Step 4: LSDB Synchronization ─► All routers build identical LSDB      │
│  Step 5: Dijkstra SPF Run ─────► Compute shortest-path tree & install   │
└────────────────────────────────────────────────────────────────────────┘
```

### OSPF Operation: The 5 Lifecycle Steps

1. **Step 1: Neighbor Discovery via Hello Packets**:
   - Transmitted every **10 seconds** on broadcast/point-to-point links (multicast `224.0.0.5`).
   - Routers verify matching parameters: Area ID, Subnet Mask, Hello/Dead intervals (Dead = $4 \times \text{Hello} = 40\text{s}$), and Authentication.
   - Transitions through states: `Down` $\to$ `Init` $\to$ `2-Way` (neighbors have established bidirectional communication).
2. **Step 2: Adjacency Formation & Database Exchange**:
   - On multi-access Ethernet segments, routers elect a **Designated Router (DR)** and **Backup Designated Router (BDR)** using priority and highest Router ID (RID) to prevent $O(N^2)$ flooding meshes.
   - Neighbors transition: `ExStart` $\to$ `Exchange` (sharing Database Description - DBD summaries) $\to$ `Loading` (requesting full link states with Link State Requests - LSR and Link State Updates - LSU).
   - Reach `Full` state: link state databases are fully synchronized.
3. **Step 3: LSA Flooding**:
   - Every router originates a **Link State Advertisement (LSA)** detailing its identity, attached interfaces, link states, and bandwidth costs.
   - LSAs are flooded reliably across the area via multicast (`224.0.0.5` and `224.0.0.6` for DR/BDR). Every router retransmits LSAs out all interfaces except the one on which it arrived.
4. **Step 4: Link State Database (LSDB) Building**:
   - Every router in an OSPF area stores all received LSAs in its local LSDB.
   - **Fundamental Invariant**: Within a given OSPF area, **every router's LSDB is mathematically identical**.
5. **Step 5: Dijkstra SPF Calculation**:
   - Each router places itself at the root of the graph and executes **Dijkstra's Shortest Path First (SPF) algorithm** on its LSDB.
   - Derives a loop-free Shortest Path Tree (SPT) to all destination subnets and installs the optimal next hops into the active IP routing table.

### OSPF Metric Calculation: Bandwidth Cost
Unlike RIP's simplistic hop count, OSPF computes cost based inversely on link bandwidth:
$$\text{Cost} = \frac{\text{Reference Bandwidth}}{\text{Interface Bandwidth}}$$

By default in Cisco IOS and standard OSPF implementations, $\text{Reference Bandwidth} = 100\text{ Mbps}$ ($10^8\text{ bps}$):
- **10 Mbps Ethernet**: $\text{Cost} = 100 / 10 = \mathbf{10}$
- **100 Mbps FastEthernet**: $\text{Cost} = 100 / 100 = \mathbf{1}$
- **1 Gbps GigabitEthernet**: $\text{Cost} = 100 / 1000 = 0.1 \implies \mathbf{1}$ (Cost cannot be fractional; clamped to minimum 1!)

> [!IMPORTANT]
> Because 1 Gbps and 10 Gbps links both yield a default cost of 1, modern network engineers **must adjust the reference bandwidth** to 100 Gbps ($100,000\text{ Mbps}$) using `auto-cost reference-bandwidth 100000` so that 10 Gbps (cost 10) is prioritized over 1 Gbps (cost 100)!

### Hierarchical Multi-Area OSPF Architecture
To scale to thousands of routers without running out of CPU memory during SPF recalculations, OSPF divides networks into **Areas**:

```
     [ Area 1: Branch ]               [ Area 0: BACKBONE ]               [ Area 2: Campus ]
     ┌──────────────┐                 ┌──────────────────┐                 ┌──────────────┐
     │ R1 ─── R2    │                 │  R4 ─── R5 ─── R6│                 │  R8 ─── R9   │
     │   └─── R3 ───┼──[ ABR 1 ]──────┤                  ├──────[ ABR 2 ]──┼─── R10       │
     └──────────────┘                 └──────────────────┘                 └──────────────┘
```

- **Area 0 (Backbone Area)**: The core transit hub. **All other non-backbone areas must physically or logically connect directly to Area 0**.
- **Area Border Router (ABR)**: A router with interfaces in multiple areas (one in Area 0, one in a non-backbone area). ABRs summarize internal subnet routes and prevent LSA flooding from crossing area boundaries.
- **Autonomous System Boundary Router (ASBR)**: A router connected to external networks running BGP or static routes, redistributing external routes into OSPF via Type 5 External LSAs.

**Citations & References:**
- RFC 2328: OSPF Version 2 (John Moy)
- Routing TCP/IP, Volume 1 (Jeff Doyle & Jennifer Carroll), Chapter 8 (OSPFv2)
- Cisco Systems: OSPF Design Guide (Document ID 7039)

---

## Border Gateway Protocol (BGP): The Glue of the Global Internet
### The Path-Vector Philosophy of Inter-Domain Routing

While OSPF and RIP calculate mathematically shortest paths using metrics like cost or hop count, the global Internet cannot be routed on technical optimality alone. Commercial contracts, international geopolitical borders, and financial peering agreements dictate where traffic flows. A Tier-1 ISP will never carry transit traffic between two competitor ISPs for free simply because it happens to be the 'shortest link'.

The **Border Gateway Protocol (BGP-4)** is a **Path-Vector protocol** operating at Layer 7 over reliable **TCP port 179**. Rather than advertising simple hop counts or link costs, BGP advertises the **complete sequence of Autonomous Systems** traversed to reach a destination network prefix.

```
 Google (AS15169) advertises: 8.8.8.0/24  ──►  AS_PATH: [15169]
 Tata Communications (AS6453) prepends:    ──►  AS_PATH: [6453, 15169]
 Bharti Airtel (AS9498) prepends:          ──►  AS_PATH: [9498, 6453, 15169]
 End User Router receives:                 ──►  AS_PATH: [9498, 6453, 15169]
```

### The AS-PATH Attribute: Loop Prevention at Global Scale
How does BGP prevent inter-domain routing loops without running Dijkstra over the entire global Internet?

**The BGP Loop Prevention Invariant**:
*When a BGP router receives an update, it examines the `AS_PATH` attribute list. If the router detects its OWN Autonomous System Number (ASN) anywhere inside the list, it **immediately discards the route announcement**!*

If AS9498 advertises `8.8.8.0/24` with `AS_PATH: [9498, 6453, 15169]` back to Google (AS15169), Google's edge router inspects the list, identifies `15169`, realizes the route has circled back to its origin, and drops it on the spot.

### eBGP vs. iBGP

| Attribute | External BGP (eBGP) | Internal BGP (iBGP) |
| :--- | :--- | :--- |
| **Peering Scope** | Established between routers in **different** Autonomous Systems | Established between routers within the **same** Autonomous System |
| **Primary Role** | Exchange routing reachability across administrative borders | Distribute externally learned Internet routes to all internal core routers |
| **Default Administrative Distance**| Highly trusted external routes: **AD = 20** (Cisco default) | Internal distribution: **AD = 200** (Cisco default) |
| **AS-PATH Modification** | Prepends local ASN to AS_PATH upon export | Does NOT modify AS_PATH when forwarding to iBGP peers |
| **Loop Prevention Rule** | AS-PATH inspection (drops if local ASN present) | **iBGP Split Horizon**: A route learned via iBGP is never forwarded to another iBGP peer (requires full mesh or Route Reflectors) |

### The BGP Best-Path Decision Algorithm
When an enterprise or ISP receives multiple valid BGP paths to the exact same prefix, BGP evaluates attributes in a strict, deterministic hierarchy:

1. **Highest Weight** (Cisco-specific, local to router only).
2. **Highest Local Preference** (`LOCAL_PREF`: exchanged across iBGP, communicates outbound exit preference for entire AS).
3. **Prefer Locally Originated Routes** (via `network` or `aggregate-address` command).
4. **Shortest AS_PATH** (fewer traversed AS hops).
5. **Lowest Origin Type** (IGP < EGP < Incomplete `?`).
6. **Lowest Multi-Exit Discriminator** (`MED`: metric sent to external neighbor to suggest inbound entry point).
7. **Prefer eBGP over iBGP** (external paths favored over internal).
8. **Lowest IGP Metric to BGP Next Hop**.
9. **Lowest Router ID (RID)** (tie-breaker).

**Citations & References:**
- RFC 4271: A Border Gateway Protocol 4 (BGP-4) (Y. Rekhter, T. Li, S. Hares)
- BGP Design and Implementation (Randy Zhang & Micah Bartell), Cisco Press
- RFC 4456: BGP Route Reflection: An Alternative to Full Mesh Internal BGP (iBGP)

---

## Internet Security Hazards: BGP Hijacking & RPKI Defense
### The Vulnerability of Implicit Trust in BGP

When BGP was conceived in 1989 (RFC 1105), the Internet was a small consortium of trusted academic and research institutions. Consequently, BGP contains **no built-in cryptographic authentication** of routing claims: if an autonomous system advertises to its peers that it owns an IP prefix, adjacent routers blindly trust and propagate the announcement worldwide.

### BGP Prefix Hijacking Mechanics
An attacker can hijack global Internet traffic directed toward a victim organization through **Prefix Hijacking**:

```
 Normal State:
   Victim (YouTube / AS36561) advertises:  208.65.152.0/22
   Global Internet forwards traffic to AS36561.

 Hijack Attack:
   Attacker (Pakistan Telecom / AS17557) advertises:  208.65.153.0/24
   Because /24 is MORE SPECIFIC than /22, Longest Prefix Match (LPM)
   forces ALL GLOBAL ROUTERS to send YouTube traffic to Pakistan!
```

#### The 2008 YouTube Hijack Incident
In February 2008, Pakistan's government ordered local ISP Pakistan Telecom (PTCL) to block YouTube locally. To implement the block, PTCL injected a black-hole static route for `208.65.153.0/24` (a `/24` subnet inside YouTube's `/22` block). However, PTCL's upstream transit provider accidentally leaked this BGP advertisement to the global Internet. Within minutes, core routers worldwide updated their forwarding tables because `/24` was more specific than YouTube's legitimate `/22`. Global traffic for YouTube was redirected into PTCL's network, causing an immediate worldwide blackout of YouTube for over two hours.

### Modern Cryptographic Defense: RPKI (Resource Public Key Infrastructure)

To eradicate unauthenticated prefix hijacking, the Internet engineering community standardized **RPKI (RFC 6480)**:

```
  [ Regional Internet Registry (RIR) ]
                   │ Issues Cryptographic X.509 Certificate
                   ▼
  [ Route Origin Authorization (ROA) ]
    "Prefix 208.65.152.0/22 is authorized to originate ONLY from AS36561, max length /24"
                   │ Cryptographically Signed
                   ▼
  [ Validating Core Routers (Route Origin Validation - ROV) ]
    ├── Received prefix matches ROA & ASN ──► VALID (Installed in FIB)
    ├── Received prefix has wrong ASN ──────► INVALID (Dropped immediately!)
    └── No ROA published for prefix ────────► NOT FOUND (Permitted as legacy fallback)
```

Through Route Origin Validation (ROV), when an illegitimate AS attempts to announce someone else's IP prefix, Tier-1 and transit routers verify the announcement against the RPKI repository, mark the route as `INVALID`, and immediately drop the advertisement before it can contaminate global forwarding tables.

**Citations & References:**
- RFC 6480: An Infrastructure to Support Secure Internet Routing (RPKI Architecture)
- RFC 6811: BGP Prefix Origin Validation
- RIPE NCC: BGP Routing Security and RPKI Deployment Guidelines

---

## Network Convergence, Stability & Routing Loop Dynamics
### Convergence Across Protocols

**Network Convergence** is the state reached when all routers in a network have processed topological events, updated their databases, and arrived at a consistent, accurate, and mutually compatible set of forwarding paths.

**Convergence Time** is the duration between the occurrence of a network topology change (e.g., fiber cut, router reload) and the restoration of full, consistent reachability across all nodes.

#### Comparative Convergence Profile

| Protocol | Convergence Speed | Bottleneck Factor | Primary Failure Mechanism |
| :--- | :--- | :--- | :--- |
| **RIP** | **Very Slow** (minutes) | 30-second periodic update timers, 180s holddown timers | Count-to-Infinity loops, slow metric propagation |
| **OSPF** | **Very Fast** (sub-second to few seconds) | Dijkstra SPF CPU calculation, LSA flooding rate | Micro-loops during asynchronous SPF recalculations across adjacent routers |
| **BGP** | **Slow by Design** (tens of seconds to minutes) | MinRouteAdvertisementInterval (MRAI) timers, route dampening | BGP path hunting, flapping prefix oscillation across multiple transit tiers |

### Multi-Tier Loop Prevention Taxonomy
Because routing loops can devastate network capacity by spinning packets in infinite cycles, modern networks employ specialized loop prevention mechanisms at every architectural layer:

```
┌─────────────────┬─────────────────┬────────────────────────────────────────────────────────┐
│ Layer / Domain  │ Protocol        │ Loop Prevention Mechanism                              │
├─────────────────┼─────────────────┼────────────────────────────────────────────────────────┤
│ Layer 2 (LAN)   │ STP / 802.1D    │ Disables redundant physical bridge ports; enforces MST │
│ Layer 3 (IP)    │ IPv4 / IPv6     │ Time To Live (TTL) / Hop Limit decremented at each hop │
│ Layer 3 (DV)    │ RIP             │ Split Horizon, Poison Reverse, max 15 hops limit       │
│ Layer 3 (LS)    │ OSPF            │ Identical LSDB map + Dijkstra produces loop-free trees │
│ Layer 3 (PV)    │ BGP             │ AS-PATH attribute: discard route if own ASN is present  │
└─────────────────┴─────────────────┴────────────────────────────────────────────────────────┘
```

### Comprehensive Protocol Comparison Matrix

| Feature | RIPv2 | OSPFv2 | BGP-4 |
| :--- | :--- | :--- | :--- |
| **Routing Type** | Distance Vector | Link State | Path Vector |
| **Algorithmic Core**| Bellman-Ford | Dijkstra (SPF) | Policy Best-Path Selection |
| **Metric / Cost** | Hop Count (1 to 15) | Bandwidth Cost ($10^8 / \text{BW}$) | Multi-Attribute (LocalPref, AS-PATH, MED) |
| **Scope** | Small campus/office IGP | Large enterprise / DC IGP | Global Internet backbone EGP |
| **Transport Layer**| UDP port 520 | Raw IP (Protocol 89) | TCP port 179 |
| **Scalability** | $\le 15$ hops | Thousands of routers (Multi-area) | Over 950,000 global prefixes |
| **Update Mechanism**| Periodic (30s) + Triggered | Event-driven LSAs + periodic refresh | Incremental event-driven updates |

**Citations & References:**
- RFC 2453: RIP Version 2
- RFC 2328: OSPF Version 2
- RFC 4271: A Border Gateway Protocol 4 (BGP-4)
- Computer Networks: A Systems Approach, Chapter 4.3 (Routing Between Peers)

---
