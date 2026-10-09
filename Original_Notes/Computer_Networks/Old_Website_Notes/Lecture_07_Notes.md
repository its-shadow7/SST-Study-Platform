# Lecture 7: Routing and Forwarding I
## Student Notes — SST Computer Networks (Term 5)

---

## 🎯 Learning Objectives

By the end of this lecture, you should be able to:
- Rigorously differentiate between the **Control Plane (Routing)** and the **Data Plane (Forwarding)**.
- Contrast the **Routing Information Base (RIB)** against the compiled hardware **Forwarding Information Base (FIB)**.
- Read, interpret, and troubleshoot production **IP Routing Tables** across Linux, Windows, and enterprise routers.
- Master the **Longest Prefix Match (LPM)** algorithm and resolve complex route overlap collisions.
- Understand high-speed lookup data structures: **Binary Tries, Patricia/Radix Tries**, and hardware **TCAM (Ternary Content Addressable Memory)**.
- Configure and evaluate **Static Routes**, **Default Routes (Gateway of Last Resort)**, and **Floating Static Routes** with Administrative Distance.
- Trace the complete 9-step **Packet Forwarding Lifecycle** inside router silicon, from ingress PHY to egress serialization.

---

## 1. Routing vs. Forwarding: The Architectural Divide

One of the most foundational paradigms in modern networking (and the direct precursor to Software-Defined Networking / SDN) is the separation between **Control Plane** and **Data Plane**.

```
    ┌───────────────────────────────────────────────────────────┐
    │                CONTROL PLANE (Routing)                    │
    │  - Brain of the network                                   │
    │  - Runs distributed algorithms (OSPF, BGP, RIP)           │
    │  - Exchanges route updates, builds topological maps       │
    │  - Time scale: Seconds to minutes                         │
    │  - Implemented in general-purpose CPU software            │
    └─────────────────────────────┬─────────────────────────────┘
                                  │ Compiles & Downloads
                                  ▼
    ┌───────────────────────────────────────────────────────────┐
    │                 DATA PLANE (Forwarding)                   │
    │  - Muscle of the network                                  │
    │  - Moves packets from input interface to output interface │
    │  - Performs Longest Prefix Match table lookups            │
    │  - Time scale: Nanoseconds to microseconds                │
    │  - Implemented in specialized hardware ASICs & TCAM       │
    └───────────────────────────────────────────────────────────┘
```

### Comprehensive Comparison Matrix

| Dimension | Routing (Control Plane) | Forwarding (Data Plane) |
| :--- | :--- | :--- |
| **Primary Goal** | Determine the end-to-end path packets will follow | Move individual packets across the router's switching fabric |
| **Execution Rate** | Triggered on topology changes (periodic / event-based) | Executed for **every single packet** arriving at wire speed |
| **Hardware** | Main Router Processor (Control CPU / OS RAM) | Line Cards, Network Processors, Hardware ASICs, TCAM |
| **Key Protocols** | OSPF, BGP, IS-IS, RIP, Static configuration | IP Forwarding Engine, ARP lookup, MAC rewriting |
| **Data Structure** | **RIB** (Routing Information Base) | **FIB** (Forwarding Information Base) |

---

## 2. RIB vs. FIB: From Protocols to Silicon

A high-end core router does not query complex protocol state machines while forwarding 100 Gbps of traffic. It strictly decouples routing intelligence from switching execution:

1. **RIB (Routing Information Base)**:
   - Resides in main control plane RAM.
   - Contains all candidate routes learned from all active sources (OSPF, BGP, connected interfaces, static routes).
   - If three different protocols learn paths to the same destination, all three exist in the RIB, and the router uses **Administrative Distance (AD)** to select the best one.
2. **FIB (Forwarding Information Base)**:
   - Resides directly on the network line card in ultra-fast memory (TCAM/SRAM).
   - A compiled, stripped-down, flattened lookup table containing **only the single best winning next-hop** for each destination prefix.
   - Optimized for $O(1)$ hardware lookups.

```
  [ OSPF Process ] ──┐
  [ BGP Process ]  ──┼──► [ RIB (Routing Table) ] ──(Best Path Selection)──► [ FIB (Forwarding Table) ]
  [ Static Routes] ──┘         In Control RAM                                    In Line Card Silicon
```

---

## 3. Reading and Interpreting a Routing Table

A routing table contains entries that map destination network address blocks to next-hop gateways and physical egress interfaces.

### Linux Kernel Routing Table (`ip route show`)
```bash
$ ip route show
default via 192.168.1.1 dev eth0 proto dhcp metric 100 
10.0.0.0/8 via 10.200.1.1 dev wg0 proto static 
172.16.50.0/24 via 192.168.1.254 dev eth0 
192.168.1.0/24 dev eth0 proto kernel scope link src 192.168.1.50 metric 100 
```

### Enterprise Router Routing Table (Cisco IOS Format)
```text
Gateway of last resort is 203.0.113.1 to network 0.0.0.0

C    192.168.1.0/24 is directly connected, GigabitEthernet0/0
S    10.0.0.0/8 [1/0] via 192.168.1.254
O    172.16.0.0/16 [110/20] via 192.168.1.253, 00:14:22, GigabitEthernet0/0
B    198.51.100.0/24 [20/0] via 203.0.113.2, 02:45:11, GigabitEthernet0/1
S*   0.0.0.0/0 [1/0] via 203.0.113.1
```

### Route Codes & Notations Explained:
- **C (Directly Connected)**: Networks physically attached to the router's active interfaces ($\text{AD} = 0$).
- **S (Static)**: Manually configured by an engineer ($\text{AD} = 1$).
- **O (OSPF)**: Learned dynamically via Open Shortest Path First ($\text{AD} = 110$).
- **B (BGP)**: Learned via Border Gateway Protocol ($\text{AD} = 20$ for eBGP, $200$ for iBGP).
- **[110/20] Notation**:
  - First number ($110$): **Administrative Distance (AD)** — trustworthiness of the routing protocol. Lower is more preferred.
  - Second number ($20$): **Metric / Cost** — calculated cost of the path within that specific protocol. Lower is more preferred.

---

## 4. The Longest Prefix Match (LPM) Principle

When a router receives an IP packet, multiple routing table entries may encompass the destination IP address.

> 🏆 **THE GOLDEN RULE OF ROUTING**:
> **A router ALWAYS forwards traffic using the entry with the LONGEST PREFIX LENGTH (the most specific subnet mask), regardless of Administrative Distance or Metric!**

### Step-by-Step LPM Resolution Example
Consider a router whose routing table contains the following four entries:

| Route Entry # | Destination Prefix | Subnet Mask | Next-Hop Gateway | Outgoing Interface |
| :--- | :--- | :--- | :--- | :--- |
| **Route 1** | `0.0.0.0/0` | `0.0.0.0` (/0) | `203.0.113.1` (Default GW) | `wan0` |
| **Route 2** | `192.168.0.0/16` | `255.255.0.0` (/16) | `10.0.1.1` (Corporate Hub) | `eth1` |
| **Route 3** | `192.168.1.0/24` | `255.255.255.0` (/24) | `10.0.2.1` (Branch Switch) | `eth2` |
| **Route 4** | `192.168.1.128/26` | `255.255.255.192` (/26)| `10.0.3.1` (Engineering LAN)| `eth3` |

#### Scenario A: Packet arrives destined for `192.168.1.140`
1. Does it match Route 1 (`0.0.0.0/0`)? **YES** (Matches 0 bits).
2. Does it match Route 2 (`192.168.0.0/16`)? **YES** ($192.168.1.140 \text{ AND } /16 = 192.168.0.0$).
3. Does it match Route 3 (`192.168.1.0/24`)? **YES** ($192.168.1.140 \text{ AND } /24 = 192.168.1.0$).
4. Does it match Route 4 (`192.168.1.128/26`)?
   - Binary of 4th octet ($140$): `10001100`.
   - Subnet mask `/26` 4th octet: `11000000` ($192$).
   - Bitwise AND: `10000000` ($128$).
   - **YES**, matches `192.168.1.128`!
5. **Selection**: Prefix lengths are $/0, /16, /24, /26$.
   - The longest prefix is **/26**.
   - **Winning Action**: Packet is forwarded out interface **`eth3`** to Next-Hop `10.0.3.1`.

#### Scenario B: Packet arrives destined for `192.168.1.50`
- Matches Route 1 (/0), Route 2 (/16), Route 3 (/24).
- Does NOT match Route 4 (/26, which covers .128–.191).
- **Winning Action**: Longest match is **/24** $\rightarrow$ Forwarded out interface **`eth2`**.

#### Scenario C: Packet arrives destined for `8.8.8.8`
- Does not match Routes 2, 3, 4.
- Matches only Route 1 (`0.0.0.0/0`).
- **Winning Action**: Forwarded to Default Gateway on **`wan0`**.

---

## 5. High-Performance Hardware Lookup: Tries & TCAM

If a router contains 1,000,000 global internet BGP routes, linearly testing each entry would require 1,000,000 comparison operations per packet. At 100 Gbps, this is impossible.

### Software Data Structure: Radix / Patricia Trie
In software routing (Linux kernel, DPDK), routes are organized into a tree where each node represents a bit ($0$ = left branch, $1$ = right branch):
- **Path Compression**: Consecutive non-branching bit chains are collapsed into single nodes.
- **Lookup Complexity**: $O(K)$, where $K \le 32$ bits for IPv4 ($128$ bits for IPv6), regardless of whether the table contains 10 routes or 1,000,000 routes.

```
                           [ Root ]
                          /        \
                    (Bit 0 = 0)   (Bit 0 = 1)
                                      \
                                    [ 192... ]
                                    /        \
                             (Bit 16 = 0)  (Bit 16 = 1)
                                 /                \
                         [ 192.168.0.0/16 ]    [ Other ]
```

### Hardware Silicon: TCAM (Ternary Content Addressable Memory)
Standard RAM takes an address as input and returns the data stored at that address.
**CAM (Content Addressable Memory)** does the reverse: it takes data as input and immediately outputs the address where that data is found in **a single clock cycle**.

**TCAM (Ternary CAM)** supports three states per bit:
- `0`
- `1`
- `X` (Don't Care / Wildcard)

```
TCAM Entry Table:
Entry 1: 11000000.10101000.00000001.10XXXXXX (/26)  ──► Egress Interface: eth3
Entry 2: 11000000.10101000.00000001.XXXXXXXX (/24)  ──► Egress Interface: eth2
Entry 3: 11000000.10101000.XXXXXXXX.XXXXXXXX (/16)  ──► Egress Interface: eth1
Entry 4: XXXXXXXX.XXXXXXXX.XXXXXXXX.XXXXXXXX (/0)   ──► Egress Interface: wan0
```

When a destination IP arrives, the TCAM evaluates **all 1,000,000 entries simultaneously in parallel in a single hardware cycle (approx. 2–5 nanoseconds)**, and an encoder priority circuit outputs the longest match!

---

## 6. Static Routing & The Gateway of Last Resort

### Static Routing
An administrator manually programs routes into the router's configuration.
- **Advantages**: Minimal CPU overhead, zero protocol chatter on links, absolute administrative control.
- **Disadvantages**: Fragile. If a fiber link is cut, the router blindly sends packets into a dead-end black hole until an engineer manually edits the configuration.

### Default Route (`0.0.0.0/0`)
Known as the **Gateway of Last Resort**:
- Subnet Mask: `0.0.0.0` (Prefix length 0 bits).
- Matches every packet because $0$ bits need to match.
- Acts as the fallback bucket when no more specific entry exists.

### Floating Static Route (Fault Tolerant Redundancy)
A network engineer wants traffic to use a primary fiber link, but automatically failover to a cellular backup link if the fiber fails:

```cisco
! Primary Route (Uses default AD of 1 for static routes)
ip route 0.0.0.0 0.0.0.0 203.0.113.1

! Backup Floating Static Route (Configured with AD of 10)
ip route 0.0.0.0 0.0.0.0 198.51.100.1 10
```

- While the primary link is alive, the router installs the primary route ($\text{AD} = 1$). The backup route ($\text{AD} = 10$) sits dormant in the RIB.
- If the primary link goes down, the router removes the primary route and immediately installs the floating static route into the FIB without human intervention.

---

## 7. The 9-Step Packet Forwarding Life Cycle Inside a Router

When an IP datagram arrives at a router interface, router silicon executes this exact sequential pipeline:

```
[ Ingress PHY/MAC ] ──► 1. Verify FCS / Drop if Corrupt
                         │
                         ▼
                     2. Strip L2 Ethernet Header
                         │
                         ▼
                     3. Verify IPv4 Header Checksum
                         │
                         ▼
                     4. Decrement TTL by 1 (Drop & ICMP if TTL <= 0)
                         │
                         ▼
                     5. Query FIB using Longest Prefix Match (LPM)
                         │
                         ▼
                     6. Check Outgoing MTU (Fragment if needed)
                         │
                         ▼
                     7. Recalculate IPv4 Header Checksum
                         │
                         ▼
                     8. Query ARP Cache for Next-Hop MAC
                         │
                         ▼
[ Egress PHY/MAC ]  ◄── 9. Encapsulate New L2 Frame & Transmit
```

### Detailed Breakdown:
1. **FCS Validation**: Layer 2 CRC is checked. If transmission noise corrupted any bit, the frame is silently discarded.
2. **L2 Stripping**: Router strips the source MAC, destination MAC, and EtherType.
3. **IPv4 Header Validation**: Router verifies the version is 4, header length $\ge 20$ bytes, and checks the IP header checksum.
4. **TTL Decrementing**:
   - `TTL = TTL - 1`.
   - If $\text{TTL} \le 0$: Router discards the packet and generates an **ICMP Type 11, Code 0** error message (*Time-to-Live Exceeded in Transit*) back to the sender. This prevents infinite routing loops from melting the network.
5. **FIB Route Lookup**: Hardware TCAM performs LPM to discover:
   - Next-Hop IP address.
   - Outgoing physical interface (e.g., `GigabitEthernet0/1`).
6. **MTU & Fragmentation**: If packet size exceeds egress MTU:
   - If `DF = 0`: Packet is sliced into fragments.
   - If `DF = 1`: Packet is dropped, and an **ICMP Type 3, Code 4** is sent back.
7. **Checksum Recalculation**: Because TTL and flags changed, the router recalculates the 16-bit One's Complement IPv4 Header Checksum.
8. **Next-Hop MAC Lookup**: Router queries its local ARP cache for the Next-Hop IP. If missing, it buffers the packet and broadcasts an ARP request.
9. **Layer 2 Encapsulation & Serialization**:
   - New Destination MAC = Next-Hop Router's MAC.
   - New Source MAC = This router's egress interface MAC.
   - Recomputes Layer 2 CRC-32 FCS.
   - Transmits bits out onto the physical wire.

---

## 📌 Summary Checklist & Exam Cram Notes

1. **Control vs. Data Plane**: Control plane (Routing) builds the map; Data plane (Forwarding) moves packets at wire speed.
2. **RIB vs. FIB**: RIB contains all candidate routes in CPU RAM; FIB is the compiled, single-best-route table in hardware TCAM silicon.
3. **Administrative Distance (AD)**: Priority of route source: Connected (0) $>$ Static (1) $>$ eBGP (20) $>$ OSPF (110) $>$ iBGP (200).
4. **Longest Prefix Match (LPM)**: The most specific prefix length always wins, regardless of AD or metric.
5. **Default Route**: `0.0.0.0/0`, matches all destinations when no specific route exists.
6. **TCAM**: Hardware memory performing parallel LPM lookups across 1M routes in a single clock cycle ($O(1)$).
7. **TTL Function**: Decremented at every router hop; drops packet at $\text{TTL} = 0$ to kill loops.
8. **MAC Rewriting**: Routers strip the incoming Ethernet frame and construct a brand-new frame for the next hop.
9. **Floating Static Route**: Backup static route configured with higher AD that takes over upon primary link loss.

---

## 🧠 Practice Problems & Self-Check Questions

1. A router receives a packet for `172.16.20.15`. Its table contains:
   - Route A: `172.16.0.0/16` via `10.1.1.1` [AD 110]
   - Route B: `172.16.20.0/24` via `10.2.2.2` [AD 120]
   - Route C: `172.16.20.0/28` via `10.3.3.3` [AD 200]
   Which route will the router choose? Explain why AD does not override prefix length.
2. Why is the IPv4 header checksum recalculated at every single router hop, while the TCP checksum is left untouched?
3. What is the fundamental difference between an ARP table and a routing table?
4. How does the `traceroute` diagnostic utility deliberately exploit the TTL decrement mechanism to map router paths across the internet?
5. What is the consequence if two routers configure static routes pointing to each other for the same subnet?
