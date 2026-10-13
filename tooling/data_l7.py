"""
Data module for Term 5 Lecture 07:
Routing vs Forwarding, Router Architecture & Longest Prefix Match (LPM)
Strictly 0 occurrences of forbidden instructor names.
"""

L7_DATA = {
    "schema_version": 1,
    "note_id": "cn-t5-l07",
    "term": "Term 5",
    "subject_code": "CN",
    "topic_title": "Routing vs Forwarding, Router Architecture & Longest Prefix Match (LPM)",
    "tags": [
        "Networking",
        "Routing",
        "Forwarding",
        "Control Plane",
        "Data Plane",
        "Routing Table",
        "Longest Prefix Match",
        "LPM",
        "Static Routing",
        "Default Route",
        "Hop-by-Hop",
        "TTL",
        "ASIC"
    ],
    "learning_objectives": [
        "Distinguish between control plane routing (calculating paths) and data plane forwarding (switching packets).",
        "Examine physical and logical router architecture: input ports, switching fabric, output queues, and routing engines.",
        "Interpret routing table entries: destination prefix, next hop, outgoing interface, metric, and administrative distance.",
        "Analyze multi-router topologies interconnected via point-to-point /30 WAN links and trace connected vs remote routes.",
        "Master the Longest Prefix Match (LPM) algorithm through bitwise binary evaluations and disambiguate overlapping subnet routes.",
        "Configure and trace static routes, floating backup routes, and default routes (0.0.0.0/0) in Linux and enterprise routers.",
        "Trace hop-by-hop packet forwarding: invariant IP header fields, TTL decrement, checksum recalculation, and L2 MAC frame rewrites."
    ],
    "summary": "A comprehensive deep-dive into the architectural mechanics of network layer packet delivery. Contrasts control plane routing against hardware-accelerated data plane forwarding, dissects internal router switching fabrics, details routing table structure, provides rigorous binary walkthroughs of Longest Prefix Match (LPM), and traces the hop-by-hop encapsulation lifecyle across heterogeneous network segments.",
    "key_takeaways": [
        "Routing is a control plane function (slow, intelligent, global path computation), while Forwarding is a data plane function (fast, per-packet hardware switching out the correct port).",
        "Modern routers split processing: general-purpose CPUs compute routing protocols (OSPF, BGP) into the Routing Information Base (RIB), which compiles into the Forwarding Information Base (FIB) loaded into Ternary Content-Addressable Memory (TCAM).",
        "Routing tables contain five critical fields: Destination Prefix, Next Hop, Outgoing Interface, Metric, and Route Source (Connected, Static, Dynamic).",
        "When an incoming packet matches multiple routing table entries, Longest Prefix Match (LPM) mandates that the entry with the greatest number of mask bits (most specific prefix) wins.",
        "The default route (0.0.0.0/0) has a prefix length of 0, matching every possible IPv4 destination as a fallback gateway of last resort.",
        "Across every router hop, IP source and destination addresses remain unchanged (end-to-end invariant, non-NAT), while the IP TTL is decremented by 1, IP checksum is recalculated, and Layer 2 source/destination MAC addresses are completely replaced."
    ],
    "last_updated": "2026-10-13T00:00:00Z",
    "approval_status": "approved",
    "sections": [
        {
            "section_id": "sec-l07-01",
            "heading": "Control Plane vs. Data Plane: Architectural Decoupling",
            "body": "### The Fundamental Duality of Network Routing\n\nAt Layer 3 (Network Layer), router functionality is partitioned into two distinct operational planes: the **Control Plane** and the **Data Plane** (often termed the *Forwarding Plane*). Conflating these two concepts is one of the most common pitfalls in network engineering.\n\n```\n┌─────────────────────────────────────────────────────────────────┐\n│                      CONTROL PLANE (Brain)                      │\n│  - Routing Protocols (OSPF, BGP, RIP)                           │\n│  - Generates Routing Information Base (RIB)                     │\n│  - Milliseconds to Seconds timescale                            │\n│  - Software execution on General-Purpose Route Processor (CPU)  │\n└────────────────────────────────┬────────────────────────────────┘\n                                 │ Compiles & Pushes\n                                 ▼\n┌─────────────────────────────────────────────────────────────────┐\n│                       DATA PLANE (Muscle)                       │\n│  - Packet Forwarding Engine                                     │\n│  - Forwarding Information Base (FIB) in TCAM / ASICs            │\n│  - Nanoseconds timescale (Line Rate: 100 Gbps - 400 Gbps)       │\n│  - Hardware table lookup, header rewriting, switching fabric   │\n└─────────────────────────────────────────────────────────────────┘\n```\n\n#### Detailed Comparison\n\n| Dimension | Control Plane (Routing) | Data Plane (Forwarding) |\n| :--- | :--- | :--- |\n| **Core Objective** | Determine the end-to-end path packets will take across the network graph | Move an incoming packet from an input interface to the appropriate output interface |\n| **Analogy** | Reading a road map to plan a cross-country itinerary | A highway interchange driving a car through a specific exit ramp |\n| **Frequency** | Triggered periodically (e.g., Hello timers) or on topology state changes | Executed for **every single individual packet** arriving at an interface |\n| **Execution Medium** | Operating system process running on a general-purpose CPU | Specialized hardware Application-Specific Integrated Circuits (ASICs) & TCAM |\n| **Performance Target** | Milliseconds to seconds (convergence time) | Nanoseconds (wire-speed line rate, e.g., < 100 ns per packet) |\n| **Data Structure** | Routing Information Base (RIB / Routing Table) | Forwarding Information Base (FIB / Hardware Forwarding Table) |\n| **Protocols & Scope** | OSPF, IS-IS, BGP, RIP, static configuration | IP lookup, TTL decrement, checksum recalculation, L2 MAC rewrite |\n\n### Software-Defined Networking (SDN) Context\nIn traditional classical routers, the control plane and data plane reside physically within the same chassis (e.g., Cisco, Juniper core routers). In **Software-Defined Networking (SDN)**, this separation is made physical: a centralized software controller (e.g., OpenFlow, ONOS, OpenDaylight) runs the control plane off-box on server clusters, while simple white-box hardware switches execute only data plane forwarding instructions pushed via open APIs.",
            "citations": [
                "RFC 1812: Requirements for IPv4 Routers, Section 2.2 (Router Architecture)",
                "Computer Networks: A Systems Approach (Larry Peterson & Bruce Davie), Chapter 3 (Routing and Forwarding)",
                "RFC 7426: Software-Defined Networking (SDN): Layers and Architecture Terminology"
            ]
        },
        {
            "section_id": "sec-l07-02",
            "heading": "Router Internals & Anatomy of a Routing Table",
            "body": "### Physical & Logical Architecture of a Modern Router\n\nA production enterprise router is fundamentally composed of four principal architectural subsystems:\n\n1. **Input Ports**:\n   - Terminate physical layer links (optical fiber, copper twisted-pair).\n   - Decapsulate the incoming Layer 2 frame (Ethernet, POS, PPP) and verify the Frame Check Sequence (FCS) checksum.\n   - Extract the Layer 3 IPv4/IPv6 packet.\n   - Perform line-rate lookup in the localized Forwarding Information Base (FIB) using TCAM to identify the destination output port without interrupting the central CPU.\n2. **Switching Fabric**:\n   - The high-speed interconnect connecting input ports to output ports.\n   - **Memory-based**: Packets copied to shared system memory by CPU (legacy, limited bandwidth).\n   - **Bus-based**: Input ports transfer packets directly over a shared bus (bandwidth capped by bus speed).\n   - **Crossbar Fabric (Cross-point)**: A matrix interconnect enabling multiple non-blocking parallel transfers simultaneously (modern multi-terabit standard).\n3. **Output Ports**:\n   - Buffer packets in egress queues when the switching fabric delivers packets faster than the outgoing link transmission rate.\n   - Implement active queue management (e.g., Random Early Detection - RED) and Quality of Service (QoS) scheduling (Weighted Fair Queuing - WFQ).\n   - Encapsulate the packet inside a newly constructed Layer 2 frame with the next-hop MAC address.\n4. **Routing Processor (CPU)**:\n   - Runs routing protocol engines (OSPF, BGP, RIP), manages SNMP monitoring, processes SSH/CLI sessions, and handles control packets addressed to the router itself (e.g., ICMP Echo Requests, BGP keepalives).\n\n```\n                 ┌─────────────────────────────────────────┐\n                 │        Routing Processor (CPU)          │\n                 └────────────────────┬────────────────────┘\n                                      │ Control Path\n   Input Ports                        ▼                       Output Ports\n   ┌──────────┐             ┌───────────────────┐             ┌──────────┐\n   │ Physical ├────────────►│                   ├────────────►│  Buffer  │\n   │ Data Link│             │                   │             │ Scheduler│\n   │ FIB/TCAM │             │     SWITCHING     │             │ L2 Frame │\n   └──────────┘             │      FABRIC       │             └──────────┘\n   ┌──────────┐             │    (Crossbar)     │             ┌──────────┐\n   │ Physical ├────────────►│                   ├────────────►│  Buffer  │\n   │ Data Link│             │                   │             │ Scheduler│\n   │ FIB/TCAM │             │                   │             │ L2 Frame │\n   └──────────┘             └───────────────────┘             └──────────┘\n```\n\n### Anatomy of the Routing Table\n\nThe routing table (RIB) maps network destinations to immediate physical next steps. A routing table contains five mandatory fields:\n\n```\nDestination Network / Mask ──► [ Next Hop IP ] ──► [ Outgoing Interface ] ──► [ Metric / AD ]\n```\n\n1. **Destination Network & Prefix Length**: The target IP address range represented in CIDR format (e.g., `192.168.10.0/24`).\n2. **Next Hop IP Address**: The Layer 3 IP address of the adjacent router interface on the shared link that will handle subsequent forwarding. For directly attached subnets, this field is marked as *Direct* or *Connected*.\n3. **Outgoing Interface**: The local physical or logical network interface (e.g., `eth0`, `ge-0/0/1`, `wlan0`) out of which the packet must be transmitted.\n4. **Metric (Cost)**: A numeric value assigned by the routing protocol representing path quality (lower is preferred). Hop count in RIP, bandwidth cost in OSPF, composite delay/bandwidth in EIGRP.\n5. **Route Source (Origin)**: Indicates how the route was learned:\n   - **Connected (`C`)**: Automatically generated when an IP is configured on an active link.\n   - **Static (`S`)**: Manually configured by an administrator.\n   - **Dynamic (`O`, `B`, `R`)**: Discovered dynamically via OSPF, BGP, or RIP.\n\n### Viewing and Interpreting Host & Router Routing Tables\n\nOn modern Linux kernels:\n```bash\n$ ip route show\ndefault via 192.168.1.1 dev eth0 proto dhcp metric 100 \n10.0.0.0/30 dev eth1 proto kernel scope link src 10.0.0.1 \n172.16.0.0/16 via 10.0.0.2 dev eth1 metric 20 \n192.168.1.0/24 dev eth0 proto kernel scope link src 192.168.1.5 \n```\n\n- `default via 192.168.1.1 dev eth0`: Catch-all default route (`0.0.0.0/0`) via the local LAN gateway.\n- `10.0.0.0/30 dev eth1 proto kernel scope link`: Point-to-point link directly connected to interface `eth1`.\n- `172.16.0.0/16 via 10.0.0.2 dev eth1`: Remote subnet reachable by forwarding packets to neighbor router `10.0.0.2` through outgoing interface `eth1`.",
            "citations": [
                "RFC 1812: Requirements for IPv4 Routers, Section 5.2 (Forwarding Algorithm)",
                "Computer Networking: A Top-Down Approach (Kurose & Ross), Chapter 4 (Inside a Router)",
                "Linux Advanced Routing & Traffic Control HOWTO (LARTC), Chapter 2"
            ]
        },
        {
            "section_id": "sec-l07-03",
            "heading": "The 2-Router Hop Architecture & Connected Subnets",
            "body": "### Multi-Router Remote Network Routing\n\nTo understand how independent local area networks (LANs) communicate across wide area network (WAN) boundaries, consider two enterprise offices connected across a point-to-point router transit link:\n\n```\n Host A (Workstation)            Router R1                        Router R2                     Host B (Server)\n   192.168.1.10/24               192.168.1.1                      10.0.0.2/30                   172.16.5.10/24\n   ┌───────────────┐           eth0 ┌──────────┐ eth1           eth0 ┌──────────┐ eth1          ┌───────────────┐\n   │    Host A     ├───────────────►│    R1    ├───────────────►│    R2    ├─────────────►│    Host B     │\n   └───────────────┘           LAN A└────┬─────┘ WAN: 10.0.0.0/30└───┬──────┘ LAN B         └───────────────┘\n    192.168.1.0/24                   10.0.0.1/30                  172.16.5.1/24          172.16.5.0/24\n   (Default GW: .1)                                                                      (Default GW: .1)\n```\n\n#### Subnet Architecture Breakdown\n1. **LAN A (Branch Office)**: `192.168.1.0/24`\n   - Usable host range: `192.168.1.1` to `192.168.1.254`\n   - Router R1 interface `eth0`: `192.168.1.1` (serves as default gateway for LAN A)\n   - Host A interface: `192.168.1.10`\n2. **WAN Transit Subnet**: `10.0.0.0/30`\n   - Mask: `255.255.255.252` ($2^2 = 4$ total addresses, $2$ usable hosts)\n   - Router R1 interface `eth1`: `10.0.0.1`\n   - Router R2 interface `eth0`: `10.0.0.2`\n   - Broadcast address: `10.0.0.3`\n3. **LAN B (Data Center)**: `172.16.5.0/24`\n   - Usable host range: `172.16.5.1` to `172.16.5.254`\n   - Router R2 interface `eth1`: `172.16.5.1` (default gateway for LAN B)\n   - Host B interface: `172.16.5.10`\n\n### Where Routing Table Entries Originate\n\nRouting entries are populated through three mechanisms:\n1. **Connected Routes**: Created automatically by the kernel when an interface is assigned an IP address and brought up (`ip link set up`). Next hop is direct.\n2. **Static Routes**: Manually entered by an engineer using administrative commands (`ip route add`).\n3. **Dynamic Routes**: Populated automatically by routing daemons exchanging route updates (OSPF, RIP, BGP).\n\n#### Routing Table for Router R1\n\n| Destination Prefix | Next Hop IP | Outgoing Interface | Route Type | Rationale |\n| :--- | :--- | :--- | :--- | :--- |\n| `192.168.1.0/24` | *Direct* | `eth0` | Connected | Directly attached to local LAN A |\n| `10.0.0.0/30` | *Direct* | `eth1` | Connected | Directly attached to WAN transit link |\n| `172.16.5.0/24` | `10.0.0.2` | `eth1` | Static / OSPF | Remote LAN B reachable across WAN via R2 |\n\n#### Routing Table for Router R2\n\n| Destination Prefix | Next Hop IP | Outgoing Interface | Route Type | Rationale |\n| :--- | :--- | :--- | :--- | :--- |\n| `172.16.5.0/24` | *Direct* | `eth1` | Connected | Directly attached to local LAN B |\n| `10.0.0.0/30` | *Direct* | `eth0` | Connected | Directly attached to WAN transit link |\n| `192.168.1.0/24` | `10.0.0.1` | `eth0` | Static / OSPF | Remote LAN A reachable across WAN via R1 |\n\n### Linux CLI Commands for Route Manipulation\n\n```bash\n# Adding a static route to remote network 172.16.5.0/24 via R2's WAN IP:\nsudo ip route add 172.16.5.0/24 via 10.0.0.2 dev eth1\n\n# Adding a static neighbor ARP mapping for next-hop router:\nsudo ip neigh add 10.0.0.2 lladdr 00:1a:2b:3c:4d:5e dev eth1\n\n# Deleting a route:\nsudo ip route del 172.16.5.0/24\n\n# Inspecting specific route decision for a destination IP:\nip route get 172.16.5.10\n# Output: 172.16.5.10 via 10.0.0.2 dev eth1 src 10.0.0.1 uid 1000\n```",
            "citations": [
                "RFC 1812: Requirements for IPv4 Routers, Section 4.2.2 (IP Address Assignment)",
                "RFC 3021: Using 31-Bit Prefixes on IPv4 Point-to-Point Links",
                "Linux man-pages: ip-route(8), ip-neighbour(8)"
            ]
        },
        {
            "section_id": "sec-l07-04",
            "heading": "Longest Prefix Match (LPM) Theory & Mathematical Foundations",
            "body": "### The Principle of Maximum Specificity\n\nBecause Classless Inter-Domain Routing (CIDR) enables route summarization and overlapping address blocks, a single destination IP address can simultaneously match multiple prefix entries in a router's forwarding table. When an IP matches more than one entry, which route must the router choose?\n\n**The Longest Prefix Match (LPM) Axiom**:\n$$\\text{Longest Prefix Length } (/P) \\iff \\text{Greatest Number of Mask Bits} \\iff \\text{Smallest Destination Range} \\iff \\mathbf{HIGHEST\\ PRIORITY}$$\n\nThe router evaluates every route whose network prefix covers the destination IP, counts the number of matching leading bits, and chooses the route with the **largest prefix length ($/P$)**.\n\n```\n                      INCOMING PACKET: Dest IP\n                                │\n                                ▼\n           Evaluate all Routing Table entries against Dest IP\n                   (Dest IP AND Route Mask == Route Prefix)\n                                │\n                     ┌──────────┴──────────┐\n                     ▼                     ▼\n              Zero Matches           Multiple Matches\n                     │                     │\n         Has default (0.0.0.0/0)?          ▼\n         ├── YES: Use default         Compare Prefix Lengths (/P)\n         └── NO: Drop packet               │\n             (ICMP Net Unreachable)        ▼\n                                      Select route with MAX(P)\n                                           │\n                                           ▼\n                                Forward packet out corresponding\n                                 interface to Next Hop\n```\n\n### Why LPM is Mathematically Essential\nWithout LPM, the Internet routing architecture would collapse under table explosion:\n1. **Hierarchical Route Aggregation**: An ISP can advertise a broad aggregate prefix (e.g., `198.51.100.0/22`, containing $1,024$ addresses) to the global Internet backbone.\n2. **Specific Exceptions**: If one corporate customer inside that range (`198.51.100.128/26`, $64$ addresses) switches to a different upstream link, the upstream router can inject the specific `/26` route. Global routers will forward traffic for the customer out the `/26` path, while all other traffic in the `/22` continues uninterrupted out the aggregate path.\n\n### Hardware Implementation: From Tries to TCAM\n1. **Radix Trees / Binary Tries**: In software, prefixes are organized in a binary tree where traversing left represents bit `0` and right represents bit `1`. Lookup time is proportional to prefix depth $O(W)$, where $W = 32$ for IPv4 or $W = 128$ for IPv6.\n2. **Ternary Content-Addressable Memory (TCAM)**:\n   - Standard RAM receives an address and outputs data.\n   - CAM receives data and outputs the matching address in parallel.\n   - **Ternary CAM** supports three states: `0`, `1`, and `X` (Don't Care / Wildcard).\n   - A TCAM compares an incoming 32-bit destination IP against **every single routing prefix in parallel in a single clock cycle** (under $5$ nanoseconds), making wire-speed 400 Gbps forwarding possible.",
            "citations": [
                "RFC 1519: Classless Inter-Domain Routing (CIDR): an Address Assignment and Aggregation Strategy",
                "RFC 4632: Classless Inter-domain Routing (CIDR): The Internet Address Assignment and Aggregation Plan",
                "High Performance Switches and Routers (H. Jonathan Chao & Bin Liu), Chapter 4 (IP Address Lookup Algorithms)"
            ]
        },
        {
            "section_id": "sec-l07-05",
            "heading": "Exhaustive Step-by-Step LPM Walkthroughs",
            "body": "### Detailed Case Studies & Binary Dissections\n\nTo master Longest Prefix Match, we trace real-world packet routing decisions through exact bitwise evaluations.\n\n---\n\n### Case Study 1: Resolving Destination `172.16.20.50`\n\nConsider a router with the following routing table:\n- Entry 1: `172.16.0.0/16` via `10.0.0.2` on `eth1`\n- Entry 2: `172.16.20.0/24` via `10.0.0.6` on `eth2`\n- Entry 3: `0.0.0.0/0` via `10.0.0.2` on `eth1` (Default Route)\n\n#### Step-by-Step Evaluation:\n1. **Test Entry 1 (`/16`)**:\n   - Destination `172.16.20.50` masked with `255.255.0.0` yields `172.16.0.0`.\n   - `172.16.0.0 == 172.16.0.0` $\\implies$ **MATCH** (16 bits matched).\n2. **Test Entry 2 (`/24`)**:\n   - Destination `172.16.20.50` masked with `255.255.255.0` yields `172.16.20.0`.\n   - `172.16.20.0 == 172.16.20.0` $\\implies$ **MATCH** (24 bits matched).\n3. **Test Entry 3 (`/0`)**:\n   - Destination `172.16.20.50` masked with `0.0.0.0` yields `0.0.0.0`.\n   - `0.0.0.0 == 0.0.0.0` $\\implies$ **MATCH** (0 bits matched).\n\n#### Selection:\nAll three entries match. The router compares prefix lengths:\n$$24 > 16 > 0$$\n**Winner:** `172.16.20.0/24`. The router forwards the packet out interface `eth2` to next hop `10.0.0.6`.\n\n---\n\n### Case Study 2: Bitwise Evaluation of `10.10.20.150`\n\nRouting table entries:\n- Entry A: `10.0.0.0/8` $\\to$ Next Hop `192.168.1.1` on `eth0`\n- Entry B: `10.10.0.0/16` $\\to$ Next Hop `192.168.2.1` on `eth1`\n- Entry C: `10.10.20.0/24` $\\to$ Next Hop `192.168.3.1` on `eth2`\n- Entry D: `10.10.20.128/25` $\\to$ Next Hop `192.168.4.1` on `eth3`\n- Entry E: `0.0.0.0/0` $\\to$ Next Hop `192.168.5.1` on `eth4`\n\n#### Detailed Binary Dissection of 4th Octet:\n- Destination 4th octet is $150_{10}$:\n  $$150_{10} = \\mathbf{1}0010110_2$$\n- Entry D prefix is `10.10.20.128/25`:\n  - Base 4th octet is $128_{10} = \\mathbf{1}0000000_2$\n  - A `/25` mask requires the first 25 bits to match identically. The first 24 bits (`10.10.20.`) match. The 25th bit (1st bit of the 4th octet) of the packet is `1`, which matches the prefix's 25th bit `1`.\n  - The address range for `10.10.20.128/25` spans `10.10.20.128` through `10.10.20.255`.\n  - Because $150$ falls inside $[128, 255]$, Entry D matches!\n\n#### Selection:\nEntries A (/8), B (/16), C (/24), D (/25), and E (/0) all match.\n$$25 > 24 > 16 > 8 > 0$$\n**Winner:** `10.10.20.128/25`. The router forwards the packet out interface `eth3` to next hop `192.168.4.1`.\n\n---\n\n### Case Study 3: The Deceptive Distractor `172.16.10.200`\n\nRouting table entries:\n- Entry 1: `172.16.0.0/12` $\\to$ Router R1\n- Entry 2: `172.16.0.0/16` $\\to$ Router R2\n- Entry 3: `172.16.10.0/24` $\\to$ Router R3\n- Entry 4: `172.16.10.64/26` $\\to$ Router R4\n- Entry 5: `0.0.0.0/0` $\\to$ Router R5\n\n#### Detailed Binary Evaluation:\n1. **Evaluate Entry 4 (`172.16.10.64/26`)**:\n   - Prefix requires 26 bits to match. Octets 1, 2, 3 (`172.16.10.`) match (24 bits).\n   - 4th octet of prefix is $64_{10} = \\mathbf{01}000000_2$. The mask requires the first two bits of octet 4 to be `01` (spanning range $64$ to $127$).\n   - 4th octet of packet destination is $200_{10} = \\mathbf{11}001000_2$.\n   - Compare leading bits: $\\mathbf{11}_2 \\ne \\mathbf{01}_2$!\n   - $200$ is outside the range $[64, 127]$.\n   - **Entry 4 DOES NOT MATCH!**\n2. **Evaluate Entry 3 (`172.16.10.0/24`)**:\n   - Octets 1, 2, 3 match `172.16.10.`. Any 4th octet ($0$ to $255$) matches.\n   - **MATCH** (24 bits).\n3. **Evaluate Entries 1, 2, and 5**:\n   - Entry 2 (`/16`) matches (16 bits).\n   - Entry 1 (`/12`) matches (12 bits).\n   - Entry 5 (`/0`) matches (0 bits).\n\n#### Selection:\nAmong matching entries (/24, /16, /12, /0), Entry 3 has the greatest prefix length.\n**Winner:** `172.16.10.0/24`. The packet is forwarded to **Router R3**! (Novice engineers incorrectly select R4 simply because /26 is the longest prefix in the table, ignoring that it failed the bitwise match).",
            "citations": [
                "RFC 1812: Requirements for IPv4 Routers, Section 5.2.4.3 (Longest Match)",
                "Computer Networks: A Systems Approach, Chapter 3.2 (Internet Protocol)",
                "Interconnections: Bridges, Routers, Switches, and Internetworking Protocols (Radia Perlman), Chapter 10"
            ]
        },
        {
            "section_id": "sec-l07-06",
            "heading": "Default Routing (0.0.0.0/0) & Internet Routing Hierarchy",
            "body": "### The Gateway of Last Resort\n\nThe **default route**, designated as `0.0.0.0/0` in IPv4 and `::/0` in IPv6, is the ultimate fallback entry in a routing table. Its prefix length is $0$, meaning that zero network bits are required to match: every valid IPv4 address in existence satisfies `Dest IP AND 0.0.0.0 == 0.0.0.0`.\n\n```\nDestination: 0.0.0.0/0  via  10.1.1.2  dev  eth2\nSemantic Meaning: \"If no more specific route in this table matches the destination IP, forward the packet to 10.1.1.2!\"\n```\n\n### The Internet Routing Hierarchy & Default-Free Zone (DFZ)\n\nDefault routing is what allows the Internet to scale without requiring every consumer device to store the entire global routing table:\n\n```\n  [Home Device] (Laptop, Phone)\n        │ Default Route: 0.0.0.0/0 via 192.168.1.1 (Home Wi-Fi AP)\n        ▼\n  [Home Wi-Fi Router]\n        │ Default Route: 0.0.0.0/0 via ISP Gateway (e.g., 203.0.113.1)\n        ▼\n  [Access / Tier-3 ISP Router]\n        │ Default Route: 0.0.0.0/0 via Regional Transit Provider\n        ▼\n  [Tier-2 Regional ISP Router]\n        │ Default Route: 0.0.0.0/0 via Tier-1 Backbone Provider\n        ▼\n  [Tier-1 Core Transit Backbone Routers]\n        │\n        └───► NO DEFAULT ROUTE! (The Default-Free Zone - DFZ)\n              Holds the COMPLETE Global BGP Routing Table (> 950,000 routes)\n              If a Tier-1 router has no route for an IP, the packet is instantly dropped!\n```\n\n### Static Routing vs. Dynamic Routing\n\nA **static route** is manually programmed into the routing table by an administrator. A **dynamic route** is discovered, validated, and updated autonomously by routing protocols.\n\n#### Comparative Trade-Off Matrix\n\n| Evaluation Metric | Static Routing | Dynamic Routing (OSPF, BGP, RIP) |\n| :--- | :--- | :--- |\n| **Configuration Complexity** | Minimal for small networks; becomes unmanageable ($O(N^2)$) in large networks | Higher initial protocol setup, then self-managing |\n| **Topology Scalability** | Low: every topology change requires manual admin reconfiguration | High: automatically scales across thousands of subnets and autonomous systems |\n| **Automatic Failover** | None by default (black-holes traffic if next-hop link drops) | Automatic: detects link failures via keepalive timers and reroutes traffic |\n| **CPU & Bandwidth Overhead** | Exactly **0%** protocol overhead | Consumes periodic CPU, memory, and bandwidth for Hello packets and LSA/route exchanges |\n| **Predictability & Security** | Completely deterministic; immune to malicious route injection or spoofing | Vulnerable to rogue route advertisements, route poisoning, and BGP hijacking |\n\n### Floating Static Routes (Backup Routes)\nNetwork engineers frequently deploy **floating static routes** as emergency failover mechanisms for dynamic protocols. Routers use **Administrative Distance (AD)** to rank route trustworthiness (lower AD is preferred):\n- Connected: AD = 0\n- Static: AD = 1\n- OSPF: AD = 110\n- RIP: AD = 120\n\nBy configuring a static route with an artificially inflated metric / AD higher than the dynamic protocol, the static route remains dormant (invisible in the FIB). If the primary OSPF link drops, the OSPF route is withdrawn, and the floating static route immediately surfaces into the active forwarding table:\n```bash\n# Linux syntax: primary route learned dynamically; backup static route configured with high metric:\nsudo ip route add 10.5.0.0/24 via 10.0.1.1 dev eth2 metric 500\n```",
            "citations": [
                "RFC 1812: Requirements for IPv4 Routers, Section 5.2.4.4 (Default Route)",
                "BGP in the Data Center (Dinesh G. Dutt), Chapter 1 (Network Architecture)",
                "CIDR Report: Global Internet Routing Table Statistics (CIDR-Report.org)"
            ]
        },
        {
            "section_id": "sec-l07-07",
            "heading": "Hop-by-Hop Packet Forwarding & Per-Hop Header Transformations",
            "body": "### The Invariant and Variant Fields in Packet Forwarding\n\nPackets traverse the Internet **hop-by-hop**. No intermediate router possesses the end-to-end roadmap of every subsequent device. Each router knows only the single immediate next-hop neighbor.\n\nWhen an IPv4 packet arrives at a router interface, what changes, and what remains invariant?\n\n```\n       ┌────────────────────────────────────────────────────────┐\n       │                     IP PACKET                          │\n       │  [Src IP: 192.168.1.5]  ──►  [Dst IP: 10.50.20.100]    │ ◄── UNCHANGED (End-to-End)\n       │  [TTL: 64 ──► 63]       ──►  [Checksum Recalculated]   │ ◄── MODIFIED at every hop\n       └────────────────────────────────────────────────────────┘\n                                    ▲\n                                    │ Encapsulated inside\n       ┌────────────────────────────┴───────────────────────────┐\n       │                  ETHERNET LAYER 2 FRAME                │\n       │  [Src MAC: Router Outgoing] ──► [Dst MAC: Next-Hop NIC]│ ◄── COMPLETELY STRIPPED\n       │                                                        │     & REBUILT at every hop\n       └────────────────────────────────────────────────────────┘\n```\n\n#### The Per-Hop Transformation Matrix\n\n| Header Field | Layer | Modified at Router? | Engineering Mechanism & Justification |\n| :--- | :--- | :--- | :--- |\n| **IP Source Address** | Layer 3 | ❌ **No** (unless NAT) | Preserves original client identity for end-to-end reply transmission. |\n| **IP Destination Address** | Layer 3 | ❌ **No** (unless NAT) | Directs subsequent downstream routers to the final destination host. |\n| **Time To Live (TTL)** | Layer 3 | ✅ **YES** | Decremented by $1$ at each router hop. Prevents looping packets from congesting networks indefinitely. |\n| **IP Header Checksum** | Layer 3 | ✅ **YES** | Because TTL is modified, the 16-bit one's complement checksum must be recalculated. |\n| **Ethernet Source MAC** | Layer 2 | ✅ **YES** | Overwritten with the hardware MAC address of the router's **outgoing interface**. |\n| **Ethernet Destination MAC** | Layer 2 | ✅ **YES** | Overwritten with the hardware MAC address of the **next-hop router's incoming interface** (resolved via ARP). |\n| **Frame Check Sequence (FCS)**| Layer 2 | ✅ **YES** | CRC32 recomputed for the brand new Layer 2 Ethernet frame. |\n\n### The Lifecycle of Time To Live (TTL)\n\n1. Initial host operating systems assign a default TTL: Linux/macOS = $64$, Windows = $128$, Cisco IOS = $255$.\n2. Upon receipt of a packet, the router examines its TTL:\n   - If $\\text{TTL} > 1$: Router decrements TTL by $1$ ($\\text{TTL} \\leftarrow \\text{TTL} - 1$), recomputes checksum, and forwards.\n   - If $\\text{TTL} \\le 1$: The router **drops the packet immediately** and transmits an **ICMP Time Exceeded (Type 11, Code 0)** error datagram back to the original source IP.\n\n#### How Traceroute Exploits TTL Expiration:\nTraceroute maps the exact Layer 3 path across the Internet using intentional TTL expiration:\n- Probe 1: Sent with $\\text{TTL} = 1$. Dropped by Router 1 $\\implies$ Router 1 sends ICMP Time Exceeded (reveals Router 1's IP and RTT).\n- Probe 2: Sent with $\\text{TTL} = 2$. Passes Router 1, dropped by Router 2 $\\implies$ Router 2 sends ICMP Time Exceeded.\n- Probe $N$: Continues incrementally until the final destination host is reached and replies with ICMP Port Unreachable or Echo Reply.",
            "citations": [
                "RFC 791: Internet Protocol (DARPA Internet Program Protocol Specification), Section 3.1",
                "RFC 792: Internet Control Message Protocol (ICMP), Time Exceeded Message",
                "RFC 1812: Requirements for IPv4 Routers, Section 5.3 (IP Header Processing)"
            ]
        }
    ],
    "quiz": {
        "quiz_id": "quiz-cn-t5-l07",
        "title": "Topic Mastery Assessment: Routing vs Forwarding, Router Architecture & Longest Prefix Match",
        "description": "25 comprehensive questions testing mastery of control/data plane architecture, router switching fabrics, routing tables, binary Longest Prefix Match (LPM), and hop-by-hop packet forwarding transformations.",
        "questions": [
            {
                "id": "q-l07-01",
                "difficulty": "easy",
                "type": "single_choice",
                "question": "Which of the following functions belongs strictly to the router's Control Plane rather than its Data Plane?",
                "options": [
                    {"id": "opt-a", "text": "Decrementing the IPv4 Time To Live (TTL) field for each passing packet."},
                    {"id": "opt-b", "text": "Exchanging OSPF Link State Advertisements (LSAs) and computing shortest path routing tables."},
                    {"id": "opt-c", "text": "Performing hardware TCAM table lookups to switch packets across a crossbar fabric."},
                    {"id": "opt-d", "text": "Rewriting the Layer 2 Ethernet destination MAC address to the next hop."}
                ],
                "correctOptionIds": ["opt-b"],
                "explanation": "Computing routes, running dynamic routing protocols (OSPF, BGP, RIP), and constructing the Routing Information Base (RIB) are Control Plane tasks. Decrementing TTL, hardware lookups, and L2 MAC rewriting are executed per packet in the Data Plane."
            },
            {
                "id": "q-l07-02",
                "difficulty": "easy",
                "type": "single_choice",
                "question": "What is the primary operational distinction between routing and forwarding?",
                "options": [
                    {"id": "opt-a", "text": "Routing occurs at Layer 2 using MAC addresses, while forwarding occurs at Layer 3 using IP addresses."},
                    {"id": "opt-b", "text": "Routing is the control plane process of determining end-to-end paths; forwarding is the data plane action of moving a packet from an input port to an output port."},
                    {"id": "opt-c", "text": "Routing is performed on every packet at line rate, while forwarding is performed periodically every 30 seconds."},
                    {"id": "opt-d", "text": "Routing refers to LAN packet switching, while forwarding refers exclusively to WAN Internet transit."}
                ],
                "correctOptionIds": ["opt-b"],
                "explanation": "Routing is slow and intelligent (control plane, building routing tables across seconds/minutes), whereas forwarding is fast and mechanical (data plane, moving packets across nanosecond hardware switching fabrics)."
            },
            {
                "id": "q-l07-03",
                "difficulty": "easy",
                "type": "single_choice",
                "question": "What prefix length is represented by the IPv4 default route '0.0.0.0/0'?",
                "options": [
                    {"id": "opt-a", "text": "32 bits."},
                    {"id": "opt-b", "text": "24 bits."},
                    {"id": "opt-c", "text": "0 bits."},
                    {"id": "opt-d", "text": "8 bits."}
                ],
                "correctOptionIds": ["opt-c"],
                "explanation": "The default route is 0.0.0.0/0, which has a prefix length of 0 bits. Because 0 network bits must match, it matches every destination IP address as a fallback gateway of last resort."
            },
            {
                "id": "q-l07-04",
                "difficulty": "easy",
                "type": "single_choice",
                "question": "When a router receives an IP packet, what occurs to the Time To Live (TTL) field before forwarding?",
                "options": [
                    {"id": "opt-a", "text": "It is incremented by 1 to track total hops traversed."},
                    {"id": "opt-b", "text": "It remains unchanged unless network congestion is detected."},
                    {"id": "opt-c", "text": "It is decremented by 1; if it reaches 0, the packet is dropped and an ICMP Time Exceeded message is sent."},
                    {"id": "opt-d", "text": "It is reset to the router's local default TTL (64 or 128)."}
                ],
                "correctOptionIds": ["opt-c"],
                "explanation": "Every Layer 3 router decrements the TTL field by 1. If TTL reaches 0, the packet is discarded and an ICMP Time Exceeded (Type 11, Code 0) message is generated to prevent persistent routing loops."
            },
            {
                "id": "q-l07-05",
                "difficulty": "easy",
                "type": "multiple_choice",
                "question": "Which of the following fields are typically included in a standard router's routing table entry? (Select all that apply)",
                "options": [
                    {"id": "opt-a", "text": "Destination Network Prefix and Subnet Mask."},
                    {"id": "opt-b", "text": "Next Hop IP Address."},
                    {"id": "opt-c", "text": "Outgoing Network Interface."},
                    {"id": "opt-d", "text": "Destination Host MAC Address."}
                ],
                "correctOptionIds": ["opt-a", "opt-b", "opt-c"],
                "explanation": "A routing table contains Destination Prefix, Next Hop IP, Outgoing Interface, and Metric. Host MAC addresses are maintained in the ARP cache / neighbor table, not in the routing table."
            },
            {
                "id": "q-l07-06",
                "difficulty": "easy",
                "type": "single_choice",
                "question": "What Linux command is used to display the active kernel routing table?",
                "options": [
                    {"id": "opt-a", "text": "ip route show"},
                    {"id": "opt-b", "text": "ifconfig -a"},
                    {"id": "opt-c", "text": "ping -r"},
                    {"id": "opt-d", "text": "traceroute -n"}
                ],
                "correctOptionIds": ["opt-a"],
                "explanation": "'ip route show' (or 'ip route' / 'netstat -rn') displays the active IPv4 kernel routing table on Linux."
            },
            {
                "id": "q-l07-07",
                "difficulty": "easy",
                "type": "single_choice",
                "question": "A packet is forwarded from Host A across 4 intermediate routers to Server B. How many times is the Layer 2 Ethernet frame stripped and reconstructed?",
                "options": [
                    {"id": "opt-a", "text": "0 times (the frame travels intact end-to-end)."},
                    {"id": "opt-b", "text": "1 time (only at the first router)."},
                    {"id": "opt-c", "text": "4 times (at each intermediate router)."},
                    {"id": "opt-d", "text": "8 times."}
                ],
                "correctOptionIds": ["opt-c"],
                "explanation": "At each Layer 3 router hop, the existing Layer 2 frame is stripped upon ingress, and a completely new Layer 2 frame with new source and destination MAC addresses is constructed upon egress. Traversing 4 routers means 4 frame reconstructions."
            },
            {
                "id": "q-l07-08",
                "difficulty": "easy",
                "type": "single_choice",
                "question": "What happens if a router has NO default route configured and receives a packet destined for an IP that matches none of its routing table entries?",
                "options": [
                    {"id": "opt-a", "text": "The router broadcasts the packet out all active interfaces."},
                    {"id": "opt-b", "text": "The router drops the packet and transmits an ICMP Destination Network Unreachable message to the source."},
                    {"id": "opt-c", "text": "The router holds the packet in memory until a route is dynamically learned."},
                    {"id": "opt-d", "text": "The packet is looped back to the ingress interface."}
                ],
                "correctOptionIds": ["opt-b"],
                "explanation": "If no route matches and no default route exists, the router must discard the packet and send an ICMP Destination Network Unreachable (Type 3, Code 0) datagram back to the source."
            },
            {
                "id": "q-l07-09",
                "difficulty": "easy",
                "type": "multiple_choice",
                "question": "Which header fields of an IP packet remain invariant (unchanged) when forwarded across a non-NAT router? (Select all that apply)",
                "options": [
                    {"id": "opt-a", "text": "Source IP Address."},
                    {"id": "opt-b", "text": "Destination IP Address."},
                    {"id": "opt-c", "text": "Time To Live (TTL)."},
                    {"id": "opt-d", "text": "Header Checksum."}
                ],
                "correctOptionIds": ["opt-a", "opt-b"],
                "explanation": "In standard non-NAT routing, the IP Source Address and Destination Address remain unchanged end-to-end. TTL is decremented, which subsequently forces the Header Checksum to be recomputed."
            },
            {
                "id": "q-l07-10",
                "difficulty": "medium",
                "type": "single_choice",
                "question": "A router has three routing table entries:\n1) 172.16.0.0/16 via 10.0.0.1\n2) 172.16.20.0/24 via 10.0.0.2\n3) 0.0.0.0/0 via 10.0.0.3\nWhere is a packet destined for 172.16.20.75 forwarded?",
                "options": [
                    {"id": "opt-a", "text": "To 10.0.0.3 via the default route."},
                    {"id": "opt-b", "text": "To 10.0.0.1 because /16 covers a wider address space."},
                    {"id": "opt-c", "text": "To 10.0.0.2 because /24 is the longest prefix match among matching entries."},
                    {"id": "opt-d", "text": "It is dropped due to conflicting routing entries."}
                ],
                "correctOptionIds": ["opt-c"],
                "explanation": "All three entries match 172.16.20.75. Longest Prefix Match selects the entry with the greatest prefix length: 24 > 16 > 0. Therefore, 172.16.20.0/24 via 10.0.0.2 wins."
            },
            {
                "id": "q-l07-11",
                "difficulty": "medium",
                "type": "single_choice",
                "question": "A routing table contains:\n- 10.0.0.0/8 via Next Hop A\n- 10.10.0.0/16 via Next Hop B\n- 10.10.20.0/24 via Next Hop C\n- 10.10.20.128/25 via Next Hop D\nA packet arrives addressed to 10.10.20.150. Which next hop is selected?",
                "options": [
                    {"id": "opt-a", "text": "Next Hop A"},
                    {"id": "opt-b", "text": "Next Hop B"},
                    {"id": "opt-c", "text": "Next Hop C"},
                    {"id": "opt-d", "text": "Next Hop D"}
                ],
                "correctOptionIds": ["opt-d"],
                "explanation": "In binary, 150 = 10010110_2. The 10.10.20.128/25 prefix covers addresses from 10.10.20.128 to 10.10.20.255. Because 150 is within this range, /25 matches. Since 25 > 24 > 16 > 8, Next Hop D wins by Longest Prefix Match."
            },
            {
                "id": "q-l07-12",
                "difficulty": "medium",
                "type": "single_choice",
                "question": "A router has entries:\n- 172.16.0.0/16 via R1\n- 172.16.10.0/24 via R2\n- 172.16.10.64/26 via R3\n- 0.0.0.0/0 via R4\nA packet arrives for 172.16.10.200. Which router is the packet forwarded to?",
                "options": [
                    {"id": "opt-a", "text": "R3, because /26 is the longest prefix in the table."},
                    {"id": "opt-b", "text": "R2, because 172.16.10.200 matches /24 but does NOT match the /26 range [64-127]."},
                    {"id": "opt-c", "text": "R1, because /16 is the standard Class B boundary."},
                    {"id": "opt-d", "text": "R4, via the default route."}
                ],
                "correctOptionIds": ["opt-b"],
                "explanation": "The /26 subnet covers 172.16.10.64 to 172.16.10.127. In binary, 200 = 11001000_2, while 64/26 requires the leading bits of octet 4 to be 01. Thus, /26 does NOT match. The longest matching entry is 172.16.10.0/24, so R2 is selected."
            },
            {
                "id": "q-l07-13",
                "difficulty": "medium",
                "type": "multiple_choice",
                "question": "Why are point-to-point WAN links between two enterprise routers commonly configured with /30 or /31 subnets? (Select all that apply)",
                "options": [
                    {"id": "opt-a", "text": "A /30 subnet allocates exactly 4 IP addresses (1 network, 2 usable host interfaces, 1 broadcast), preventing IPv4 address waste."},
                    {"id": "opt-b", "text": "RFC 3021 permits /31 subnets on point-to-point links by eliminating directed broadcast, using exactly 2 addresses."},
                    {"id": "opt-c", "text": "A /30 subnet is required because routing protocols cannot run on subnets larger than /28."},
                    {"id": "opt-d", "text": "Points-to-point links connect exactly two router interfaces, meaning additional host addresses are superfluous."}
                ],
                "correctOptionIds": ["opt-a", "opt-b", "opt-d"],
                "explanation": "Point-to-point links interconnect exactly two router endpoints. A /30 provides 2 usable IPs (with network and broadcast), and RFC 3021 defines /31 for 2 host IPs without broadcast. Routing protocols can run on any valid subnet size."
            },
            {
                "id": "q-l07-14",
                "difficulty": "medium",
                "type": "single_choice",
                "question": "What is the primary architectural advantage of using a Crossbar Switch Fabric over a shared bus or shared memory fabric in core routers?",
                "options": [
                    {"id": "opt-a", "text": "A crossbar fabric eliminates the need for output port buffering."},
                    {"id": "opt-b", "text": "A crossbar fabric enables multiple parallel, non-blocking packet transfers between different input and output ports simultaneously."},
                    {"id": "opt-c", "text": "A crossbar fabric allows the central CPU to inspect every packet payload for malware."},
                    {"id": "opt-d", "text": "A crossbar fabric reduces power consumption by transmitting packets without Layer 2 headers."}
                ],
                "correctOptionIds": ["opt-b"],
                "explanation": "Shared memory and shared bus architectures suffer from bottleneck contention because only one packet can traverse the bus/memory bus at a time. A crossbar fabric features an NxN grid of crosspoints, permitting multiple non-conflicting transfers in parallel."
            },
            {
                "id": "q-l07-15",
                "difficulty": "medium",
                "type": "single_choice",
                "question": "What is a 'floating static route' and how is it implemented?",
                "options": [
                    {"id": "opt-a", "text": "A static route that changes its next hop dynamically based on DNS query responses."},
                    {"id": "opt-b", "text": "A backup static route configured with an Administrative Distance higher than dynamic routing protocols, remaining dormant until the dynamic route fails."},
                    {"id": "opt-c", "text": "A multicast route that floats across all router interfaces simultaneously."},
                    {"id": "opt-d", "text": "A static route without an egress interface specified."}
                ],
                "correctOptionIds": ["opt-b"],
                "explanation": "A floating static route has an administrative distance configured higher than the active dynamic protocol (e.g., AD = 200 vs OSPF AD = 110). It is dormant in the RIB until the primary dynamic route is withdrawn, whereupon it takes over."
            },
            {
                "id": "q-l07-16",
                "difficulty": "medium",
                "type": "single_choice",
                "question": "How does traceroute determine the IP address of each successive intermediate router along a network path?",
                "options": [
                    {"id": "opt-a", "text": "It sends packets with the IP 'Record Route' option enabled in the header."},
                    {"id": "opt-b", "text": "It sends sequential packets with incrementally increasing TTL values (1, 2, 3...) and reads the source IP of returning ICMP Time Exceeded messages."},
                    {"id": "opt-c", "text": "It requests the OSPF Link State Database from the local default gateway."},
                    {"id": "opt-d", "text": "It queries the public BGP looking glass of Tier-1 providers."}
                ],
                "correctOptionIds": ["opt-b"],
                "explanation": "Traceroute sends packets starting with TTL=1. The first router decrements TTL to 0, drops the packet, and returns an ICMP Time Exceeded packet (revealing its IP). TTL is then incremented to 2, 3, etc., uncovering each subsequent router."
            },
            {
                "id": "q-l07-17",
                "difficulty": "medium",
                "type": "multiple_choice",
                "question": "Which of the following statements regarding the Internet's 'Default-Free Zone' (DFZ) are TRUE? (Select all that apply)",
                "options": [
                    {"id": "opt-a", "text": "Routers operating within the DFZ do NOT have a default route (0.0.0.0/0)."},
                    {"id": "opt-b", "text": "DFZ routers must maintain the complete global BGP routing table (over 900,000 routes)."},
                    {"id": "opt-c", "text": "If a DFZ router has no explicit route entry matching a destination IP, the packet is dropped."},
                    {"id": "opt-d", "text": "Home Wi-Fi routers operate inside the DFZ by maintaining direct BGP peering with Tier-1 providers."}
                ],
                "correctOptionIds": ["opt-a", "opt-b", "opt-c"],
                "explanation": "The DFZ consists of Tier-1 backbone routers that possess complete global routing information and do not use a default route. If a route is absent, the packet is discarded. Home routers rely heavily on default routes to their ISP."
            },
            {
                "id": "q-l07-18",
                "difficulty": "medium",
                "type": "single_choice",
                "question": "What hardware technology enables modern core routers to perform Longest Prefix Match lookups across hundreds of thousands of routes in under 5 nanoseconds?",
                "options": [
                    {"id": "opt-a", "text": "Dynamic RAM (DRAM) with binary search algorithms."},
                    {"id": "opt-b", "text": "Ternary Content-Addressable Memory (TCAM)."},
                    {"id": "opt-c", "text": "Solid-State Drive (SSD) caching layers."},
                    {"id": "opt-d", "text": "Central Processing Unit L1 data caches."}
                ],
                "correctOptionIds": ["opt-b"],
                "explanation": "Ternary Content-Addressable Memory (TCAM) allows parallel hardware matching across all entries in a single clock cycle using '0', '1', and 'wildcard/don't care' bit states, enabling nanosecond line-rate LPM lookups."
            },
            {
                "id": "q-l07-19",
                "difficulty": "hard",
                "type": "single_choice",
                "question": "A core router's forwarding table contains the following four routes:\n1. 198.51.100.0/24 via eth1\n2. 198.51.100.128/25 via eth2\n3. 198.51.100.160/27 via eth3\n4. 198.51.100.192/28 via eth4\nA packet with destination IP 198.51.100.174 arrives. Through which interface is the packet forwarded?",
                "options": [
                    {"id": "opt-a", "text": "eth1"},
                    {"id": "opt-b", "text": "eth2"},
                    {"id": "opt-c", "text": "eth3"},
                    {"id": "opt-d", "text": "eth4"}
                ],
                "correctOptionIds": ["opt-c"],
                "explanation": "Let's analyze the 4th octet (174):\n- 198.51.100.0/24: range 0-255 (matches, prefix 24)\n- 198.51.100.128/25: range 128-255 (matches, prefix 25)\n- 198.51.100.160/27: block size = 2^(32-27) = 32. Range = 160 to 160 + 31 = 191. 174 is in [160, 191]! (matches, prefix 27)\n- 198.51.100.192/28: block size = 16. Range = 192 to 207. 174 is NOT in [192, 207] (fails)\nMatching prefixes: /24, /25, /27. Longest match is /27 on eth3."
            },
            {
                "id": "q-l07-20",
                "difficulty": "hard",
                "type": "single_choice",
                "question": "Consider the destination address 10.240.85.19 and a routing table with:\n- Route A: 10.128.0.0/9 via Gateway 1\n- Route B: 10.224.0.0/11 via Gateway 2\n- Route C: 10.240.64.0/20 via Gateway 3\n- Route D: 10.240.80.0/21 via Gateway 4\nWhich gateway will forward the packet?",
                "options": [
                    {"id": "opt-a", "text": "Gateway 1"},
                    {"id": "opt-b", "text": "Gateway 2"},
                    {"id": "opt-c", "text": "Gateway 3"},
                    {"id": "opt-d", "text": "Gateway 4"}
                ],
                "correctOptionIds": ["opt-d"],
                "explanation": "Let's check Route D (10.240.80.0/21):\n- Mask /21 has 5 network bits in the 3rd octet (mask = 255.255.248.0, block size = 8).\n- Base 3rd octet = 80. Range = 80 to 87.\n- The packet's 3rd octet is 85, which is inside [80, 87]!\n- Route D matches with prefix length 21.\nSince 21 > 20 > 11 > 9, and Route D matches, Route D via Gateway 4 is the Longest Prefix Match."
            },
            {
                "id": "q-l07-21",
                "difficulty": "hard",
                "type": "multiple_choice",
                "question": "Why must the IPv4 Header Checksum be recomputed at EVERY intermediate router hop, whereas the Layer 2 Ethernet Frame Check Sequence (FCS) is also recomputed? (Select all that apply)",
                "options": [
                    {"id": "opt-a", "text": "Because the router decrements the TTL field in the IPv4 header, altering the 16-bit one's complement sum of the header."},
                    {"id": "opt-b", "text": "Because intermediate routers rewrite the payload of TCP segments to reflect queuing delays."},
                    {"id": "opt-c", "text": "Because the Layer 2 frame has its source and destination MAC addresses replaced, invalidating the previous frame's CRC32 FCS."},
                    {"id": "opt-d", "text": "Because the IP header checksum protects the entire packet payload including the application data."}
                ],
                "correctOptionIds": ["opt-a", "opt-c"],
                "explanation": "The IPv4 checksum covers ONLY the IPv4 header (not payload). Because TTL is decremented, the header bits change, requiring checksum recalculation. The Ethernet FCS covers the L2 frame; since source/destination MAC addresses change at each hop, FCS must also be recalculated."
            },
            {
                "id": "q-l07-22",
                "difficulty": "hard",
                "type": "single_choice",
                "question": "In a router with Head-of-Line (HOL) blocking at its input ports, what is the theoretical maximum throughput of an input-queued switch fabric under independent uniform traffic without Virtual Output Queuing (VOQ)?",
                "options": [
                    {"id": "opt-a", "text": "100% of line rate."},
                    {"id": "opt-b", "text": "Approximately 58.6% (2 - sqrt(2))."},
                    {"id": "opt-c", "text": "Exactly 75%."},
                    {"id": "opt-d", "text": "Approximately 25%."}
                ],
                "correctOptionIds": ["opt-b"],
                "explanation": "In 1987, Karol, Hluchyj, and Morgan proved that Head-of-Line (HOL) blocking in First-In-First-Out (FIFO) input-buffered switches limits the maximum throughput to (2 - sqrt(2)) ≈ 58.6%. Modern routers overcome this by using Virtual Output Queuing (VOQ)."
            },
            {
                "id": "q-l07-23",
                "difficulty": "hard",
                "type": "multiple_choice",
                "question": "Which of the following conditions can trigger an intermediate router to generate an ICMP error datagram back to the source host? (Select all that apply)",
                "options": [
                    {"id": "opt-a", "text": "The packet arrives with TTL = 1 and requires another forwarding hop (ICMP Time Exceeded)."},
                    {"id": "opt-b", "text": "The packet's Don't Fragment (DF) flag is set to 1, but the packet size exceeds the MTU of the egress link (ICMP Fragmentation Needed)."},
                    {"id": "opt-c", "text": "No route matches the destination address and no default route is configured (ICMP Destination Network Unreachable)."},
                    {"id": "opt-d", "text": "The packet successfully reaches its final destination without transmission errors."}
                ],
                "correctOptionIds": ["opt-a", "opt-b", "opt-c"],
                "explanation": "TTL expiration generates Type 11 Code 0. Exceeding MTU with DF=1 generates Type 3 Code 4 (Path MTU Discovery). Absence of a route generates Type 3 Code 0. Normal successful delivery generates no ICMP error."
            },
            {
                "id": "q-l07-24",
                "difficulty": "hard",
                "type": "single_choice",
                "question": "Suppose Router R1 receives a packet destined for 192.168.10.45. Its routing table contains:\n- 192.168.10.0/26 via 10.0.0.2 (AD 110, Metric 20)\n- 192.168.10.0/24 via 10.0.0.3 (AD 1, Metric 0 - Static Route)\nWhich path is selected by the router and why?",
                "options": [
                    {"id": "opt-a", "text": "192.168.10.0/24 because the static route has a much lower Administrative Distance (AD 1 < AD 110)."},
                    {"id": "opt-b", "text": "192.168.10.0/26 because Longest Prefix Match (/26 > /24) takes absolute precedence over Administrative Distance and Metric."},
                    {"id": "opt-c", "text": "The router performs Equal-Cost Multi-Path (ECMP) load balancing across both next hops."},
                    {"id": "opt-d", "text": "The packet is dropped due to an administrative route collision."}
                ],
                "correctOptionIds": ["opt-b"],
                "explanation": "A critical networking principle: Administrative Distance (AD) and Metric are ONLY evaluated between routes with the EXACT SAME prefix length to decide which one enters the routing table. When multiple entries with DIFFERENT prefix lengths reside in the table, Longest Prefix Match (/26 > /24) ALWAYS takes precedence during forwarding!"
            },
            {
                "id": "q-l07-25",
                "difficulty": "hard",
                "type": "single_choice",
                "question": "An administrator executes the following Linux commands:\n$ sudo ip route add 192.168.50.0/24 via 10.0.0.2 dev eth1\nHowever, 'ip route get 192.168.50.10' returns 'RTNETLINK answers: Network is unreachable'. What is the most likely root cause?",
                "options": [
                    {"id": "opt-a", "text": "The interface eth1 is configured with full duplex instead of half duplex."},
                    {"id": "opt-b", "text": "The next-hop IP 10.0.0.2 is not reachable within any directly connected subnet configured on the router."},
                    {"id": "opt-c", "text": "Linux does not support static routes with /24 prefix masks."},
                    {"id": "opt-d", "text": "The router's ARP table is filled to capacity."}
                ],
                "correctOptionIds": ["opt-b"],
                "explanation": "In IP routing, a next-hop gateway IP must itself be resolvable (directly connected on a local subnet). If the router has no local interface with an IP subnet covering 10.0.0.2 (e.g., 10.0.0.0/30 or /24), the kernel rejects the next-hop as unreachable ('Network is unreachable')."
            }
        ]
    }
}
