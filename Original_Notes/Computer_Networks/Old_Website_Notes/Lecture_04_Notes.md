# Lecture 4: IP Addresses and Subnetting II
## Student Notes — SST Computer Networks (Term 5)

---

## 🎯 Learning Objectives

By the end of this lecture, you should be able to:
- Engineer custom subnet architectures given arbitrary organizational host requirements.
- Distinguish between **FLSM (Fixed Length Subnet Masking)** and **VLSM (Variable Length Subnet Masking)**.
- Apply the **VLSM Allocation Algorithm** using the binary address partition tree to eliminate IP address waste.
- Master the **128-bit IPv6 architecture**, hexadecimal hextet representation, and **RFC 5952 compression rules**.
- Classify IPv6 address scopes: **Global Unicast, Unique Local, Link-Local, and Multicast**, and explain why IPv6 completely eliminates broadcasts.
- Trace the internal host forwarding decision logic: Local subnet delivery via direct ARP vs. off-subnet delivery via the **Default Gateway**.
- Deconstruct **Network Address Translation (NAT/NAPT/PAT)**, stateful translation tables, port forwarding (DNAT), and the necessity of NAT traversal protocols (STUN/TURN/ICE).

---

## 1. Subnet Design: From Requirements to CIDR

In real-world network engineering, you do not start with a CIDR prefix; you start with **business constraints** (e.g., "Engineering has 120 developers, Marketing has 25 staff, and we have two point-to-point router links").

### The Mathematical Requirement Formula
To accommodate $H_{\text{req}}$ physical host interfaces on a single subnet:

$$2^N - 2 \ge H_{\text{req}}$$

Where:
- $N$ is the number of **Host Bits** required.
- The subtracted $2$ accounts for the unusable **Network ID** and **Directed Broadcast Address**.

Once $N$ is determined:

$$\text{Subnet Mask Prefix Length } P = 32 - N$$
$$\text{Block Size (Subnet Multiplier)} = 2^N$$
$$\text{Total Capacity} = 2^N - 2\text{ usable hosts}$$

### The Host-to-Prefix Lookup Matrix

| Host Requirement ($H_{\text{req}}$) | Smallest $2^N \ge H+2$ | Host Bits ($N$) | Prefix ($32 - N$) | Subnet Mask | Usable Hosts |
| :--- | :--- | :--- | :--- | :--- | :--- |
| $2$ (WAN Router Link) | $4$ ($2^2$) | 2 | **/30** | `255.255.255.252` | 2 |
| $3 - 6$ | $8$ ($2^3$) | 3 | **/29** | `255.255.255.248` | 6 |
| $7 - 14$ | $16$ ($2^4$) | 4 | **/28** | `255.255.255.240` | 14 |
| $15 - 30$ | $32$ ($2^5$) | 5 | **/27** | `255.255.255.224` | 30 |
| $31 - 62$ | $64$ ($2^6$) | 6 | **/26** | `255.255.255.192` | 62 |
| $63 - 126$ | $128$ ($2^7$) | 7 | **/25** | `255.255.255.128` | 126 |
| $127 - 254$ | $256$ ($2^8$) | 8 | **/24** | `255.255.255.0` | 254 |
| $255 - 510$ | $512$ ($2^9$) | 9 | **/23** | `255.255.254.0` | 510 |
| $511 - 1022$ | $1024$ ($2^{10}$) | 10 | **/22** | `255.255.252.0` | 1022 |

---

## 2. Variable Length Subnet Masking (VLSM)

### The Inefficiency of Fixed Length Subnet Masking (FLSM)
In FLSM, every subnet is partitioned with the exact same prefix length.
- Suppose an organization is assigned `192.168.1.0/24`.
- Department A has 110 hosts, Department B has 26 hosts, and a router link has 2 hosts.
- If we slice the `/24` into `/25` subnets to satisfy Department A (126 hosts), we only have two subnets total—not enough for three networks.
- If we slice it into `/27` subnets (30 hosts), Department A cannot fit.
- Using FLSM results in either **unsupported subnets** or **astronomical address wastage**.

### The VLSM Solution & The Golden Rule
**VLSM** allows network architects to apply different subnet masks to different subnets derived from the same root network block.

> 🚨 **THE GOLDEN RULE OF VLSM**:
> **Always sort host requirements in strictly descending order (Largest $\rightarrow$ Smallest) and allocate the largest blocks first.**
>
> If you allocate small subnets first, you will fragment the continuous binary space, making it mathematically impossible to allocate larger contiguous subnets later!

### Comprehensive Enterprise VLSM Case Study
**Assigned Base Block**: `10.50.0.0/24` (Total 256 IP addresses).
**Requirements**:
1. **Engineering**: 100 hosts
2. **Sales & Marketing**: 45 hosts
3. **Finance & HR**: 20 hosts
4. **Server DMZ**: 10 hosts
5. **WAN Link (Router to ISP)**: 2 hosts

```
                             10.50.0.0/24 (256 addresses)
                              ┌─────────────┴─────────────┐
                    10.50.0.0/25 (128 IPs)        10.50.0.128/25 (128 IPs)
                   [ ALLOCATED: Engineering ]     ┌───────────┴───────────┐
                                          10.50.0.128/26 (64 IPs) 10.50.0.192/26 (64 IPs)
                                          [ ALLOCATED: Sales ]    ┌───────┴───────┐
                                                     10.50.0.192/27 (32 IPs)  10.50.0.224/27
                                                     [ ALLOCATED: Finance ]   ┌───┴───┐
                                                              10.50.0.224/28 (16) 10.50.0.240/28
                                                              [ ALLOCATED: DMZ ]  ┌───┴───┐
                                                                          10.50.0.240/30 (4)
                                                                          [ WAN Link ]
```

### Complete VLSM Allocation Table

| Department | Hosts Needed | Host Bits ($N$) | Prefix | Block Size | Subnet Address Range | Usable Host Range | Broadcast Address |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Engineering** | 100 | 7 | **/25** | 128 | `10.50.0.0/25` | `10.50.0.1` – `10.50.0.126` | `10.50.0.127` |
| **Sales** | 45 | 6 | **/26** | 64 | `10.50.0.128/26` | `10.50.0.129` – `10.50.0.190` | `10.50.0.191` |
| **Finance** | 20 | 5 | **/27** | 32 | `10.50.0.192/27` | `10.50.0.193` – `10.50.0.222` | `10.50.0.223` |
| **Server DMZ** | 10 | 4 | **/28** | 16 | `10.50.0.224/28` | `10.50.0.225` – `10.50.0.238` | `10.50.0.239` |
| **WAN Link** | 2 | 2 | **/30** | 4 | `10.50.0.240/30` | `10.50.0.241` – `10.50.0.242` | `10.50.0.243` |
| *Unused Pool* | N/A | N/A | Mixed | 12 | `10.50.0.244 – 10.50.0.255` | *Reserved for future growth* | N/A |

---

## 3. IPv6: Architecture, Representation & Scopes

### Why IPv6?
- **Address Space Depletion**: The global IPv4 free address pool administered by IANA officially ran dry in February 2011.
- **Scale of IPv6**: IPv6 utilizes a **128-bit address space**:

  $$2^{128} \approx 3.4028 \times 10^{38}\text{ unique addresses}$$

  This is approximately $6.67 \times 10^{23}$ addresses per square meter of Earth's surface—sufficient to assign an IP address to every grain of sand on the planet.

### IPv6 Text Format & RFC 5952 Compression Rules
An IPv6 address is written as **eight 16-bit blocks called hextets** (or quads), separated by colons, represented in hexadecimal:

```
2001 : 0db8 : 0000 : 0000 : 0000 : 8a2e : 0370 : 7334
──1─   ──2─   ──3─   ──4─   ──5─   ──6─   ──7─   ──8─  (8 Hextets x 16 bits = 128 bits)
```

#### The 3 Golden Rules of RFC 5952 Representation:
1. **Omit Leading Zeros**: Within any 16-bit hextet, suppress all leading zeros:
   - `0db8` becomes `db8`
   - `0000` becomes `0`
   - `0370` becomes `370`
   - Example: `2001:0db8:0000:0000:0000:8a2e:0370:7334` $\rightarrow$ `2001:db8:0:0:0:8a2e:370:7334`
2. **Double Colon (`::`) Compression**:
   - Replace the **longest consecutive run of all-zero hextets** with a double colon `::`.
   - Result: `2001:db8::8a2e:370:7334`
   - ⚠️ **Strict Constraint**: `::` can appear **ONLY ONCE** in an address. If two runs of identical length exist, compress the first (leftmost) run.
3. **Lowercase Hexadecimal**: Always use lowercase characters `a-f` (never uppercase `A-F`).

### IPv6 Scopes and Address Classification

```
┌───────────────────────────┬──────────────────┬────────────────────────────────────────────────────────┐
│ Address Scope             │ Binary Prefix    │ Purpose & Real-World Role                              │
├───────────────────────────┼──────────────────┼────────────────────────────────────────────────────────┤
│ **Global Unicast (GUA)**  │ `2000::/3`       │ Globally routable public IP on the internet            │
│ **Unique Local (ULA)**    │ `fc00::/7`       │ Private internal enterprise network (like RFC 1918)    │
│ **Link-Local (LLA)**      │ `fe80::/10`      │ Automatically auto-configured on every interface;      │
│                           │                  │ valid only on the local link; never routed             │
│ **Multicast**             │ `ff00::/8`       │ Replaces broadcasts; delivers to registered groups     │
│ **Loopback**              │ `::1/128`        │ Equivalent to IPv4 `127.0.0.1`                         │
│ **Unspecified**           │ `::/128`         │ Equivalent to IPv4 `0.0.0.0` (used before IP assigned) │
└───────────────────────────┴──────────────────┴────────────────────────────────────────────────────────┘
```

> **CRITICAL ARCHITECTURAL DIFFERENCE**:
> **There is NO BROADCAST in IPv6!** Broadcast storms, which plagued early Ethernet switches, are structurally impossible in IPv6. All one-to-many operations rely on efficient **Multicast** groups (`ff02::1` = all nodes, `ff02::2` = all routers).

### IPv4 vs. IPv6 Architectural Comparison

| Dimension | IPv4 | IPv6 |
| :--- | :--- | :--- |
| **Address Length** | 32 bits (4 Bytes) | 128 bits (16 Bytes) |
| **Header Size** | Variable (20 to 60 Bytes with Options) | Fixed 40 Bytes (Extension headers daisy-chained) |
| **Checksum** | Verified at every router hop | Removed! (Handled by L2 and L4 to reduce router CPU) |
| **Address Resolution**| Broadcast ARP | ICMPv6 Neighbor Discovery Protocol (NDP) |
| **Fragmentation** | Intermediate routers can fragment | **Source host ONLY** (Routers drop and send ICMPv6) |
| **Auto-Configuration**| DHCP or static manual | Stateless Address Autoconfiguration (**SLAAC**) or DHCPv6|

---

## 4. Default Gateway: The Host Forwarding Decision Tree

How does an operating system (Windows, Linux, macOS, iOS) know whether to transmit an IP packet directly onto the local LAN wire or forward it to the router?

### The Host Routing Decision Algorithm
When an application initiates a connection to target IP address $D$:

```
                            Packet to Send to Destination IP (D)
                                            │
                                            ▼
                        Compute: Network_D = D AND Host_Subnet_Mask
                                            │
                                  Is Network_D == Host_Local_Network?
                                           / \
                                   YES    /   \    NO
                                         /     \
                                        ▼       ▼
                       [ DIRECT DELIVERY ]     [ INDIRECT DELIVERY ]
                     Destination is on LAN.   Destination is on External Network.
                     Resolve ARP for D.       Resolve ARP for Default Gateway IP.
                     Set Dst MAC = D's MAC.   Set Dst MAC = Gateway's MAC.
                     Transmit frame on LAN.   Transmit frame to Gateway Router.
```

### Demonstration:
- Host IP: `192.168.1.50`
- Host Subnet Mask: `255.255.255.0` (/24)
- Host Network ID: `192.168.1.0`
- Default Gateway: `192.168.1.1`

1. **Target $D_1 = 192.168.1.75$**:
   - $192.168.1.75 \text{ AND } 255.255.255.0 = 192.168.1.0$.
   - Matches local subnet. Host broadcasts an ARP request: *"Who has 192.168.1.75?"* Frame destination MAC is set to $D_1$'s NIC.
2. **Target $D_2 = 142.250.190.46$ (google.com)**:
   - $142.250.190.46 \text{ AND } 255.255.255.0 = 142.250.190.0 \ne 192.168.1.0$.
   - Off-subnet! Host ignores $D_2$'s MAC and resolves the MAC of Default Gateway `192.168.1.1`. Frame destination MAC is set to the Gateway Router.

---

## 5. Network Address Translation (NAT / NAPT / PAT)

### The Problem NAT Solves
A standard home fiber connection or corporate office is assigned **exactly one single public routable IPv4 address** by the ISP. However, hundreds of personal phones, laptops, smart TVs, and IoT sensors require simultaneous internet access.

**NAT (Network Address Translation - RFC 1631 / RFC 3022)** maps an entire private address space (e.g., `192.168.1.0/24`) to a single public IP address using transport-layer port numbers.

### NAPT / PAT (Port Address Translation) Mechanics
The router maintains an in-memory **NAT State Table**:

```
[ Private Host A ] 192.168.1.5:54321 ──┐
                                       ├──► [ NAT Gateway Router ] ──Public: 203.0.113.8──► [ Internet ]
[ Private Host B ] 192.168.1.9:54321 ──┘    Translates to unique
                                            source ports!
```

#### Step-by-Step Translation Walkthrough:
1. Host A (`192.168.1.5`) connects to Web Server (`142.250.1.1:80`) with ephemeral source port `54321`.
2. Packet arrives at NAT Router. Router rewrites:
   - `Old Source`: `192.168.1.5:54321` $\rightarrow$ `New Source`: `203.0.113.8:10001`
   - Recalculates IPv4 and TCP checksums.
3. Host B (`192.168.1.9`) also connects to Web Server with source port `54321`.
4. Router rewrites:
   - `Old Source`: `192.168.1.9:54321` $\rightarrow$ `New Source`: `203.0.113.8:10002`
5. **The NAT Translation Table**:

| Inside Local (Private) | Inside Global (Public NAT) | Outside Destination | Protocol | Timeout |
| :--- | :--- | :--- | :--- | :--- |
| `192.168.1.5:54321` | `203.0.113.8:10001` | `142.250.1.1:80` | TCP | 300s |
| `192.168.1.9:54321` | `203.0.113.8:10002` | `142.250.1.1:80` | TCP | 300s |

6. When Google replies to `203.0.113.8:10001`, the router matches port `10001` in the table, rewrites the destination back to `192.168.1.5:54321`, and forwards it onto the private LAN.

### Port Forwarding (DNAT - Destination NAT)
Under standard NAT, **unsolicited inbound connections from the internet are impossible** because no translation entry exists in the table.

**Port Forwarding (DNAT)** creates a static, permanent mapping in the NAT table:
- Rule: `External Port 8080 -> 192.168.1.200:80`
- Any external request hitting `203.0.113.8:8080` is automatically translated and forwarded to internal web server `192.168.1.200:80`.

### NAT Traversal: The Challenge for P2P and WebRTC
Peer-to-peer applications (BitTorrent, Zoom, Discord voice, multiplayer gaming) require direct host-to-host communication without routing media through a central server.
Because both peers are often behind NAT routers, they cannot directly initiate connections to each other's private IPs.

**The Traversal Architecture**:
1. **STUN (Session Traversal Utilities for NAT - RFC 5389)**: Client queries an external public STUN server: *"What is my public IP and port as seen by the outside world?"*
2. **TURN (Traversal Using Relays around NAT - RFC 5766)**: If symmetric NAT prevents direct P2P hole punching, traffic falls back to an expensive relay server.
3. **ICE (Interactive Connectivity Establishment - RFC 5245)**: Protocol framework that tests all possible STUN/direct/TURN candidates to establish the lowest-latency connection.

---

## 📌 Summary Checklist & Exam Cram Notes

1. **Subnet Formula**: $2^N - 2 \ge \text{Hosts}$, where $N = \text{host bits}$. Subnet prefix $= 32 - N$.
2. **VLSM Rule**: Always allocate largest subnets first to avoid address space fragmentation.
3. **IPv6 Length**: 128 bits, 8 hextets of 16 bits each, written in lowercase hexadecimal.
4. **RFC 5952 Compression**: Omit leading zeros in hextet; compress longest run of zeros to `::` (once only).
5. **No Broadcast in IPv6**: Broadcast replaced entirely by targeted Multicast (`ff00::/8`).
6. **IPv6 Link-Local**: `fe80::/10`, automatically configured on every interface for single-hop control traffic.
7. **Default Gateway Decision**: Host computes `Destination AND Mask`. If equal to local network, direct ARP; if not, forward to Gateway router MAC.
8. **NAT/PAT**: Rewrites `(Private IP:Port)` to `(Public IP:Port)` to conserve IPv4 addresses.
9. **DNAT / Port Forwarding**: Static inbound rule allowing external clients to reach internal private servers.
10. **NAT Traversal**: STUN discovers public endpoint; TURN relays traffic when firewall/NAT hole punching fails.

---

## 🧠 Practice Problems & Self-Check Questions

1. Given the block `172.16.0.0/22`, partition it using VLSM for three subnets: Subnet A (400 hosts), Subnet B (180 hosts), and Subnet C (50 hosts). List the network address and CIDR prefix for each.
2. Compress the following IPv6 address using RFC 5952 rules: `2001:0db8:0000:0000:0042:0000:0000:0001`.
3. Can an IPv6 address contain two `::` symbols? Explain the mathematical ambiguity that would occur if this were allowed.
4. If a computer's default gateway is misconfigured (e.g., points to an IP on a different subnet), can the computer still communicate with devices on its own local LAN? Can it browse websites on the internet?
5. Why does FTP or SIP (VoIP) break when passing through a standard NAT router, and what mechanism is required to fix it?
