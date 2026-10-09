# Lecture 2: Network Packets and Layered Communication
## Student Notes — SST Computer Networks (Term 5)

---

## 🎯 Learning Objectives

By the end of this lecture, you should be able to:
- Define what a **network protocol** is and explain the architectural necessity of **layered models**.
- Detail all **7 layers of the OSI model** and describe their individual responsibilities, abstractions, and failure modes.
- Map the theoretical 7-layer OSI model to the practical **4-layer TCP/IP model** used on the global Internet.
- Trace the complete **encapsulation and decapsulation** pipeline with exact byte headers.
- Distinguish rigorously between **PDUs (Protocol Data Units)**: Bits, Frames, Packets, Segments, and Application Data.
- Dissect the **Ethernet II frame structure** down to individual fields, including Preamble, SFD, EtherType, and FCS (CRC-32).
- Calculate why the **minimum Ethernet frame size is 64 bytes** using CSMA/CD slot-time and cable propagation physics.
- Explain **MTU vs. MSS**, the mechanics of **IP Fragmentation** (DF/MF flags, Fragment Offset), and modern **Path MTU Discovery (PMTUD)**.
- Break down **MAC addresses**, OUIs, Unicast vs. Multicast bits, Broadcasts, and how ARP bridges Layer 2 and Layer 3.
- Walk through the full hop-by-hop lifecycle of an HTTP request across switches, default gateways, and routers.

---

## 1. What is a Protocol & Why Layering?

### The Core Definition
A **network protocol** is a formal specification of rules and conventions governing communication between two or more computing systems. Without protocols, an electrical voltage on a wire or a radio wave in the air is merely meaningless physical noise.

A protocol strictly codifies:
1. **Syntax (Format)**: The structural layout of bits and bytes (which fields exist, their length, and byte order such as Big-Endian / Network Byte Order).
2. **Semantics (Meaning)**: What each bit pattern signifies and which state transitions it triggers in the sender and receiver.
3. **Timing & Synchronization**: Sequence of message exchanges, transmission speeds, flow control, and timeout/retransmission behavior under packet loss.

```
       Sender                               Receiver
   ┌────────────┐                       ┌────────────┐
   │ Application│ ──[ 1. Syntax: HTTP ]──► │ Application│
   ├────────────┤                       ├────────────┤
   │ Transport  │ ──[ 2. Semantics: TCP]─► │ Transport  │
   ├────────────┤                       ├────────────┤
   │ Network    │ ──[ 3. Routing: IP ]──►  Network   │
   ├────────────┤                       ├────────────┤
   │ Data Link  │ ──[ 4. Delivery: ETH]─►  Data Link │
   └────────────┘                       └────────────┘
```

### Why Layered Protocols? The Engineering Rationale
Without layering, a single monolithic software application would have to manage user input, graphic rendering, data compression, cryptographic encryption, TCP retransmissions, routing tables, Ethernet framing, and the physical voltage of the copper cable simultaneously.

Layering enforces **Separation of Concerns (SoC)** and strict **Information Hiding**:
- **Modularity & Loose Coupling**: Any layer can be refactored or upgraded without touching adjacent layers. When HTTP/1.1 evolved into binary multiplexed HTTP/2 and UDP-based HTTP/3 (QUIC), the physical Wi-Fi and Ethernet hardware remained completely untouched.
- **Reusability / Multiplexing**: Multiple high-level protocols (HTTP, SSH, DNS, SMTP) seamlessly share a single transport protocol (TCP or UDP), which in turn shares a single network layer (IPv4 or IPv6), running over heterogeneous physical media (Fiber, Copper, 5G, Satellite).
- **Standardized Interfaces**: Independent vendors (Cisco, Apple, Intel, Broadcom) can develop hardware and software that interoperate flawlessly worldwide provided they implement the open standard interfaces.
- **Troubleshooting Isolation**: Enables targeted fault isolation using top-down or bottom-up troubleshooting methodology (e.g., verifying physical link status at L1 before debugging SSL handshake certificates at L6/L7).

---

## 2. The OSI Reference Model (7 Layers)

Published by the **International Organization for Standardization (ISO)** in 1984 as standard ISO/IEC 7498, the **Open Systems Interconnection (OSI)** model serves as the foundational conceptual framework for understanding computer networks.

```
┌───┬──────────────┬───────────────────┬────────────────────────────────────────────────────────┐
│ # │ Layer Name   │ Data Unit (PDU)   │ Primary Function & Key Protocols                       │
├───┼──────────────┼───────────────────┼────────────────────────────────────────────────────────┤
│ 7 │ Application  │ Message / Data    │ User-facing network services (HTTP, DNS, SSH, SMTP)    │
├───┼──────────────┼───────────────────┼────────────────────────────────────────────────────────┤
│ 6 │ Presentation │ Message / Data    │ Data translation, serialization, TLS/SSL, compression  │
├───┼──────────────┼───────────────────┼────────────────────────────────────────────────────────┤
│ 5 │ Session      │ Message / Data    │ Dialog control, session token lifecycle, RPC           │
├───┼──────────────┼───────────────────┼────────────────────────────────────────────────────────┤
│ 4 │ Transport    │ Segment / Datagram│ End-to-end delivery, port multiplexing, TCP/UDP flow   │
├───┼──────────────┼───────────────────┼────────────────────────────────────────────────────────┤
│ 3 │ Network      │ Packet            │ Logical addressing (IP), path determination, routing   │
├───┼──────────────┼───────────────────┼────────────────────────────────────────────────────────┤
│ 2 │ Data Link    │ Frame             │ Physical addressing (MAC), node-to-node framing, CRC   │
├───┼──────────────┼───────────────────┼────────────────────────────────────────────────────────┤
│ 1 │ Physical     │ Bits              │ Raw transmission over physical medium (volts, photons) │
└───┴──────────────┴───────────────────┴────────────────────────────────────────────────────────┘
```

> **Memory Mnemonics:**
> - Bottom-Up (1 to 7): **P**lease **D**o **N**ot **T**hrow **S**ausage **P**izza **A**way
> - Top-Down (7 to 1): **A**ll **P**eople **S**eem **T**o **N**eed **D**ata **P**rocessing

### Layer-by-Layer Architectural Analysis

#### Layer 1 — Physical Layer
- **Role**: Converting raw binary bits ($0$s and $1$s) into physical signals (voltage levels, optical light pulses, radio frequency waves).
- **Key Concepts**: Bit-rate, clock synchronization, signal encoding (NRZ, Manchester), multiplexing (TDM, FDM, WDM), connectors (RJ-45, SFP+), cable categories (Cat5e, Cat6a, Single-Mode Fiber).
- **Failure Indicators**: Cable disconnected, transceiver burnout, bent optical fiber, electromagnetic interference (EMI), clock drift.

#### Layer 2 — Data Link Layer
- **Role**: Point-to-point and point-to-multipoint reliable data transfer across a single physical link or Local Area Network (LAN).
- **Sublayers**:
  1. **LLC (Logical Link Control - IEEE 802.2)**: Multiplexes network layer protocols and provides flow control and error notifications.
  2. **MAC (Media Access Control - IEEE 802.3/802.11)**: Manages physical hardware addressing (48-bit MAC addresses) and channel access arbitration (CSMA/CD, CSMA/CA).
- **Hardware Device**: **Layer 2 Switch**, Network Interface Card (NIC), Bridge.
- **Failure Indicators**: MAC address flapping, VLAN misconfiguration, duplicate MAC, duplex mismatch, CRC/FCS frame alignment errors.

#### Layer 3 — Network Layer
- **Role**: Global end-to-end routing and logical addressing across multiple intermediate networks and subnets.
- **Key Concepts**: IPv4/IPv6 logical addressing, hierarchical routing, router hops, Time To Live (TTL) decrementing, ICMP error reporting, Longest Prefix Match (LPM).
- **Hardware Device**: **Router**, Layer 3 Multilayer Switch.
- **Failure Indicators**: Wrong default gateway, missing routing table entry, MTU black hole, routing loop (TTL expired in transit).

#### Layer 4 — Transport Layer
- **Role**: Process-to-process communication delivery across hosts using **16-bit Port Numbers** (0–65535).
- **Protocols**:
  - **TCP (Transmission Control Protocol)**: Connection-oriented, 3-way handshake, reliable sequenced delivery, sliding-window flow control, congestion avoidance (CUBIC, BBR).
  - **UDP (User Datagram Protocol)**: Connectionless, lightweight, unreliable, zero connection setup overhead (DNS, VoIP, streaming).
- **Failure Indicators**: Port closed (`Connection Refused`), firewall blocking port, buffer starvation, TCP sequence desynchronization.

#### Layer 5 — Session Layer
- **Role**: Establishing, maintaining, synchronizing, and terminating communication dialogues/sessions between processes.
- **Modern Context**: In modern web architectures, session management is handled directly inside the Application layer (HTTP cookies, JWT tokens, WebSockets, gRPC sessions) or Transport (TCP keep-alives).

#### Layer 6 — Presentation Layer
- **Role**: Translating abstract application data structures into standardized network-independent wire formats. Handles character encoding (ASCII, UTF-8), serialization (JSON, Protobuf), compression (Gzip, Brotli, Zstandard), and cryptographic encapsulation (TLS/SSL).
- **Modern Context**: Almost universally implemented in application libraries (OpenSSL, JSON parsers) rather than the operating system kernel.

#### Layer 7 — Application Layer
- **Role**: Directly provides network services to user applications and end-user processes.
- **Protocols**: HTTP/HTTPS (Web), DNS (Domain Name System), SMTP/IMAP (Email), SSH (Secure Shell), DHCP (Configuration).
- **Failure Indicators**: HTTP 404/500 errors, DNS lookup failure (`NXDOMAIN`), authentication failures.

---

## 3. The TCP/IP Model (The Reality of the Internet)

While the OSI model was developed by a theoretical standards committee, the **TCP/IP model** (also known as the Internet Reference Model, RFC 1122) was engineered pragmatically by DARPA in the 1970s and 1980s. The internet runs exclusively on TCP/IP.

```
OSI 7-Layer Model                    TCP/IP 4-Layer Model
┌─────────────────────────┐          ┌─────────────────────────────────────────┐
│ 7. Application          │ ──┐      │                                         │
│ 6. Presentation         │ ──┼────► │ Application Layer                       │
│ 5. Session              │ ──┘      │ (HTTP, DNS, SSH, TLS, gRPC, SMTP)       │
├─────────────────────────┤          ├─────────────────────────────────────────┤
│ 4. Transport            │ ───────► │ Transport Layer (Host-to-Host)          │
│                         │          │ (TCP, UDP, SCTP, QUIC)                  │
├─────────────────────────┤          ├─────────────────────────────────────────┤
│ 3. Network              │ ───────► │ Internet Layer                          │
│                         │          │ (IPv4, IPv6, ICMP, ARP, IPsec)          │
├─────────────────────────┤          ├─────────────────────────────────────────┤
│ 2. Data Link            │ ──┐      │ Link Layer / Network Access             │
│ 1. Physical             │ ──┴────► │ (Ethernet 802.3, Wi-Fi 802.11, DOCSIS) │
└─────────────────────────┘          └─────────────────────────────────────────┘
```

### Architectural Comparison: OSI vs. TCP/IP

| Dimension | OSI Model | TCP/IP Model |
| :--- | :--- | :--- |
| **Origin** | ISO academic standard (top-down design) | DARPA practical implementation (bottom-up evolution) |
| **Layers** | 7 Distinct Layers | 4 Pragmatic Layers |
| **Presentation & Session** | Dedicated standalone layers | Integrated directly into Application and Transport |
| **Transport Layer** | Connection-oriented only (initially) | Both Connection-oriented (TCP) and Connectionless (UDP) |
| **Network Layer** | Supports Connection-oriented & Connectionless | Purely Connectionless (IP datagram service) |
| **Industry Adoption** | Educational vocabulary standard | Universal global internet standard |

---

## 4. Encapsulation, Decapsulation & Protocol Data Units (PDUs)

Data cannot simply be thrown onto a wire. At each layer of the networking stack, metadata must be attached to guide handling, routing, and error checking.

### The Specific Terminology of PDUs
Each layer calls its packaged unit of data by a specific name:
- **Layer 7/6/5**: **Application Data / Message**
- **Layer 4**: **Segment** (TCP) or **Datagram** (UDP)
- **Layer 3**: **Packet** (IP)
- **Layer 2**: **Frame** (Ethernet / Wi-Fi)
- **Layer 1**: **Bits / Physical Symbols**

```
                  APPLICATION LAYER
         ┌─────────────────────────────────┐
         │       HTTP Payload (Data)       │
         └─────────────────────────────────┘
                         │ Encapsulate (Add L4 Header)
                         ▼
                  TRANSPORT LAYER
   ┌────────────┬──────────────────────────┐
   │ TCP Header │       HTTP Payload       │   ──► TCP Segment
   └────────────┴──────────────────────────┘
                         │ Encapsulate (Add L3 Header)
                         ▼
                   NETWORK LAYER
   ┌───────────┬────────────┬──────────────┐
   │ IP Header │ TCP Header │ HTTP Payload │   ──► IP Packet
   └───────────┴────────────┴──────────────┘
                         │ Encapsulate (Add L2 Header + L2 Trailer)
                         ▼
                  DATA LINK LAYER
┌───────────┬───────────┬────────────┬──────────────┬───────────┐
│ ETH Header│ IP Header │ TCP Header │ HTTP Payload │ETH Trailer│ ──► Ethernet Frame
└───────────┴───────────┴────────────┴──────────────┴───────────┘
                         │ Modulate onto physical medium
                         ▼
                  PHYSICAL LAYER
  0 1 1 0 1 0 0 1 0 1 1 0 1 1 1 1 0 0 1 0 1 0 1 0 1 1 1 0 1 0  ──► Raw Bits
```

### Decapsulation at the Receiving Host
When raw bits arrive at the destination:
1. **NIC (L1/L2)**: Synchronizes clock, checks the Frame Check Sequence (FCS). If CRC matches, it strips the Ethernet Header and Trailer, reads the `EtherType` (`0x0800` for IPv4), and dispatches the payload to the IP driver.
2. **IP Driver (L3)**: Verifies IP Header Checksum, decrements TTL, checks destination IP against host addresses. Strips the IP header, reads the `Protocol` field (`6` for TCP, `17` for UDP), and forwards the segment to the TCP module.
3. **TCP Engine (L4)**: Verifies TCP checksum, verifies sequence numbers, manages flow buffers, strips the TCP header, and looks up the active socket bound to the destination port (e.g., port 443).
4. **Application (L7)**: Reads clean application data stream from the OS socket buffer.

---

## 5. Dissecting the Ethernet II Frame

The standard frame format used on modern wired networks is the **Ethernet II frame** (also known as DIX Ethernet):

```
┌──────────────┬─────┬─────────────┬─────────────┬───────────┬──────────────────┬───────────┐
│ Preamble     │ SFD │ Destination │ Source MAC  │ EtherType │ Payload Data     │ FCS (CRC) │
│ 7 Bytes      │ 1 B │ MAC (6 B)   │ (6 Bytes)   │ (2 Bytes) │ (46–1500 Bytes)  │ (4 Bytes) │
└──────────────┴─────┴─────────────┴─────────────┴───────────┴──────────────────┴───────────┘
▲                                                                                           ▲
└──────────────────────── Ethernet Frame Transmitted on Wire ───────────────────────────────┘
```

### Detailed Field Breakdown

1. **Preamble (7 Bytes - 56 bits)**:
   - Alternating pattern of `10101010` repeated 7 times.
   - **Purpose**: Allows receiver physical clock circuits to lock onto the incoming bitstream frequency.
2. **Start of Frame Delimiter / SFD (1 Byte - 8 bits)**:
   - Pattern: `10101011` (ending with twin consecutive `1`s).
   - **Purpose**: Alerts the NIC that the very next bit is the start of the Destination MAC address.
3. **Destination MAC (6 Bytes - 48 bits)**:
   - Hardware address of the recipient NIC on the immediate local segment.
4. **Source MAC (6 Bytes - 48 bits)**:
   - Hardware address of the sending NIC.
5. **EtherType / Length (2 Bytes - 16 bits)**:
   - Values $\ge 1536$ (`0x0600`) represent **EtherType** (identifies the encapsulated Layer 3 protocol):
     - `0x0800` $\rightarrow$ IPv4
     - `0x86DD` $\rightarrow$ IPv6
     - `0x0806` $\rightarrow$ ARP
     - `0x8100` $\rightarrow$ IEEE 802.1Q (VLAN-tagged frame)
6. **Payload (46 to 1500 Bytes)**:
   - The encapsulated L3 packet. Must be at least 46 bytes. If the packet is smaller (e.g., a 28-byte ARP packet), **padding bytes (0x00)** are appended.
7. **Frame Check Sequence / FCS (4 Bytes - 32 bits)**:
   - Cyclic Redundancy Check (**CRC-32**). The sender computes a polynomial remainder over the frame contents. The receiver recalculates it; if a single bit flipped during transmission, the frame is silently dropped at Layer 2.
8. **Interpacket Gap (IPG)**:
   - A minimum idle transmission gap equivalent to 96 bit times (9.6 µs on 10 Mbps, 0.096 µs on 1 Gbps) required between frames to allow receiver recovery.

---

## 6. Physics & Mathematics: Why the 64-Byte Minimum Frame?

A fundamental question in computer networking: **Why does Ethernet specify a minimum frame size of 64 bytes (512 bits)?**

### The CSMA/CD Collision Window
In half-duplex legacy Ethernet, multiple hosts shared a single coaxial cable using **Carrier Sense Multiple Access with Collision Detect (CSMA/CD)**:
1. **Carrier Sense**: Listen before transmitting.
2. **Multiple Access**: Anyone can transmit when the bus is idle.
3. **Collision Detect**: Listen while transmitting. If two devices transmit simultaneously, their signals collide, corrupting voltages.

```
Host A [======================= Max Cable Distance =======================] Host B
  |                                                                           |
Transmits t=0                                                       Transmits t = t_prop - ε
  └────────────────────────────► (Signal Traveling) ◄─────────────────────────┘
                                       COLLISION occurs near B!
  ◄──────────────────────────── (Collision Runt travels back to A)
 Arrives at A at time t = 2 * t_prop (Round Trip Time / Slot Time)
```

### The Mathematical Derivation
To detect a collision, **the sender MUST still be actively transmitting when the collision signal returns from the farthest point of the network.**

If a frame is too short, Host A finishes transmitting and assumes success *before* the collision wavefront returns. The corrupted frame is lost without Host A realizing it needs to retransmit!

Let:
- Maximum network segment length = $2500\text{ meters}$ (with 4 repeaters in IEEE 802.3 10BASE-5).
- Speed of electrical signal in copper $\approx 2 \times 10^8\text{ m/s}$ ($\frac{2}{3}$ speed of light $c$).
- One-way propagation delay $t_{\text{prop}} = \frac{2500\text{ m}}{2 \times 10^8\text{ m/s}} = 12.5\ \mu\text{s}$.
- Round-Trip Time (RTT) including repeater delays $\approx 51.2\ \mu\text{s}$.

For a $10\text{ Mbps}$ network:

$$\text{Slot Time} = 51.2\ \mu\text{s}$$
$$\text{Minimum Bits Transmitted} = 10\text{ Mbps} \times 51.2\ \mu\text{s} = 512\text{ bits} = 64\text{ Bytes}$$

$$\text{Minimum Frame} = 6\text{ (Dst MAC)} + 6\text{ (Src MAC)} + 2\text{ (Type)} + 46\text{ (Payload)} + 4\text{ (FCS)} = 64\text{ Bytes}$$

> Even though modern Ethernet is full-duplex with dedicated switch ports (no CSMA/CD collisions), the **64-byte minimum frame size remains standardized** for backward compatibility across all Ethernet ASIC switching silicon.

---

## 7. MTU, MSS & IP Fragmentation

### MTU (Maximum Transmission Unit)
The **MTU** is the maximum size of a Layer 3 packet (including IP header and IP payload) that can be transmitted across a Layer 2 link without requiring fragmentation.
- Standard Ethernet MTU = **1500 Bytes**.
- Jumbo Frames (Data Centers/SANs) = **9000 Bytes**.
- PPPoE (DSL connections) = **1492 Bytes** (due to 8-byte PPPoE header).

### MSS (Maximum Segment Size)
The **MSS** is the maximum amount of pure TCP application data that a host can send in a single TCP segment:

$$\text{MSS} = \text{MTU} - (\text{IP Header Size} + \text{TCP Header Size})$$

Assuming standard 20-byte IPv4 header and 20-byte TCP header:

$$\text{MSS} = 1500 - 20 - 20 = 1460\text{ Bytes}$$

```
┌─────────────────────────────────────────────────────────────┐
│                    Ethernet MTU (1500 B)                    │
├─────────────────┬──────────────────┬────────────────────────┤
│ IPv4 Header     │ TCP Header       │ TCP MSS (Payload)      │
│ (20 Bytes)      │ (20 Bytes)       │ (1460 Bytes)           │
└─────────────────┴──────────────────┴────────────────────────┘
```

### IP Fragmentation Mechanics
If an IP packet larger than 1500 bytes reaches a router whose outgoing interface MTU is smaller, the router must fragment the packet (unless the **DF: Don't Fragment** bit is set).

Fragmentation fields in the IPv4 Header:
1. **Identification (16 bits)**: Unique ID assigned by the source to identify all fragments belonging to the original datagram.
2. **Flags (3 bits)**:
   - Bit 0: Reserved (must be 0).
   - Bit 1: **DF (Don't Fragment)** $\rightarrow$ If $1$, drop packet and reply with ICMP Type 3 Code 4 if MTU exceeded.
   - Bit 2: **MF (More Fragments)** $\rightarrow$ $1$ for all intermediate fragments; $0$ for the final fragment.
3. **Fragment Offset (13 bits)**: Specifies the position of this fragment's data in the original packet, measured in **8-byte units** (64-bit blocks).

#### Worked Numerical Example:
A $4000\text{-byte}$ IPv4 packet ($20\text{ bytes header} + 3980\text{ bytes payload}$) enters an Ethernet link with $\text{MTU} = 1500\text{ bytes}$.

Each fragment can carry at most $1500 - 20 = 1480\text{ bytes}$ of payload. Since $1480$ is divisible by $8$ ($1480 / 8 = 185$), it is a valid fragment payload size.

| Fragment | Total Size | IP Header | Payload Size | Payload Byte Range | MF Flag | Fragment Offset |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Frag 1** | 1500 B | 20 B | 1480 B | $0 - 1479$ | $1$ | $0 / 8 = \mathbf{0}$ |
| **Frag 2** | 1500 B | 20 B | 1480 B | $1480 - 2959$ | $1$ | $1480 / 8 = \mathbf{185}$ |
| **Frag 3** | 1040 B | 20 B | 1020 B | $2960 - 3979$ | $0$ | $2960 / 8 = \mathbf{370}$ |

> **Critical Rule**: Fragments are **ONLY reassembled at the final destination host**, never by intermediate routers! If even one fragment is dropped, the entire packet is lost and TCP must retransmit the entire segment.

### Modern Solution: Path MTU Discovery (PMTUD)
Because fragmentation causes massive CPU overhead and high packet drop rates, modern TCP uses **PMTUD** (RFC 1191):
1. Sender marks all outgoing IP packets with `DF = 1`.
2. If an intermediate router has an MTU bottleneck, it drops the packet and sends back an **ICMP Type 3, Code 4** message: *"Destination Unreachable: Fragmentation Needed and DF Set"*, including the router's MTU value.
3. Sender adjusts its TCP MSS downward and retransmits without fragmentation.

---

## 8. MAC Addresses & The Layer 2 / Layer 3 Interface

### MAC Address Anatomy
A **MAC (Media Access Control)** address is a 48-bit (6-byte) physical identifier permanently burned into the ROM of a Network Interface Card (EUI-48 format).

```
        48-Bit MAC: 3C:22:FB:4A:89:12
       ┌──────────────────┬──────────────────┐
       │   OUI (24 bits)  │ Device ID (24 b) │
       └──────────────────┴──────────────────┘
                 │
                 ├─ Bit 0 of Byte 1: I/G Bit (0 = Unicast, 1 = Multicast)
                 └─ Bit 1 of Byte 1: U/L Bit (0 = Globally Unique, 1 = Locally Administered)
```

- **OUI (Organizationally Unique Identifier)**: Assigned by the IEEE to manufacturers (e.g., `3C:22:FB` belongs to Apple).
- **Special MACs**:
  - Broadcast: `FF:FF:FF:FF:FF:FF` (all 48 bits set to 1).
  - IPv4 Multicast prefix: `01:00:5E:xx:xx:xx`.

### Scope Comparison: MAC vs. IP Address

| Property | MAC Address (Layer 2) | IP Address (Layer 3) |
| :--- | :--- | :--- |
| **Scope** | Local segment only (Hop-by-Hop) | Global end-to-end (Source to Destination) |
| **Router Behavior** | Stripped and replaced at every router hop | Preserved end-to-end (unless modified by NAT) |
| **Analogy** | In-person student ID badge | Postal mailing address |
| **Format** | 48 bits (Hexadecimal) | 32 bits IPv4 (Decimal) / 128 bits IPv6 (Hex) |

---

## 9. Comprehensive End-to-End Walkthrough: Sending a Web Request

**Topology Scenario**:
- Client PC: IP `192.168.1.50`, MAC `AA:AA:AA:AA:AA:AA`
- Default Gateway Router (LAN Interface): IP `192.168.1.1`, MAC `BB:BB:BB:BB:BB:BB`
- Default Gateway Router (WAN Interface): IP `203.0.113.1`, MAC `CC:CC:CC:CC:CC:CC`
- Next-Hop ISP Router: IP `203.0.113.2`, MAC `DD:DD:DD:DD:DD:DD`
- Web Server: IP `142.250.190.46`, MAC `EE:EE:EE:EE:EE:EE`

```
  Client PC                    Gateway Router                  ISP Router                 Web Server
192.168.1.50                    192.168.1.1                   203.0.113.2               142.250.190.46
[AA:AA:AA:AA:AA:AA] ──LAN──► [BB:BB:BB:BB:BB:BB] ──WAN──► [DD:DD:DD:DD:DD:DD] ──...──► [EE:EE:EE:EE:EE:EE]
```

### Trace of the Outgoing Frame Across Hops

#### Hop 1: Client PC to Default Gateway
1. Browser creates HTTP GET request.
2. OS creates TCP segment (`SrcPort: 54321, DstPort: 80`).
3. OS creates IP packet:
   - `SrcIP: 192.168.1.50`
   - `DstIP: 142.250.190.46`
4. Client checks routing table: `142.250.190.46` is on an external subnet. The packet must be sent to default gateway `192.168.1.1`.
5. Client looks up ARP table for `192.168.1.1` $\rightarrow$ finds `BB:BB:BB:BB:BB:BB`.
6. Client wraps packet in Ethernet frame:
   - `SrcMAC: AA:AA:AA:AA:AA:AA`
   - `DstMAC: BB:BB:BB:BB:BB:BB` *(Router MAC, NOT Web Server MAC!)*

#### Hop 2: Router Processing & WAN Forwarding
1. Gateway router receives frame on LAN port. FCS check passes.
2. Router strips Ethernet header and inspects IP packet.
3. Router checks its routing table: matches default route `0.0.0.0/0 via 203.0.113.2 dev wan0`.
4. Router decrements `TTL: 64 -> 63` and recalculates the IPv4 Header Checksum.
5. Router builds a completely **NEW Ethernet frame** for the WAN link:
   - `SrcMAC: CC:CC:CC:CC:CC:CC` *(Router WAN MAC)*
   - `DstMAC: DD:DD:DD:DD:DD:DD` *(ISP Router MAC)*
   - The inner IP packet (`SrcIP: 192.168.1.50, DstIP: 142.250.190.46`) remains identical!

> **Core Axiom of Networking**: Throughout the entire multi-hop journey across the internet, **Layer 2 headers are repeatedly destroyed and recreated at each hop**, while the **Layer 3 packet remains invariant from source to destination**.

---

## 📌 Summary Checklist & Exam Cram Notes

1. **Protocol Definition**: Syntax (format), Semantics (meaning), Timing (rules for speed and sequencing).
2. **Layering Principle**: Modularity, abstraction, and standardized independent protocol evolution.
3. **OSI Model**: 7 layers (Physical $\rightarrow$ Data Link $\rightarrow$ Network $\rightarrow$ Transport $\rightarrow$ Session $\rightarrow$ Presentation $\rightarrow$ Application).
4. **TCP/IP Model**: 4 layers (Network Access $\rightarrow$ Internet $\rightarrow$ Transport $\rightarrow$ Application).
5. **PDUs**: Bits (L1) $\rightarrow$ Frames (L2) $\rightarrow$ Packets (L3) $\rightarrow$ Segments (L4) $\rightarrow$ Data (L7).
6. **Ethernet II Frame**: Preamble (7B) + SFD (1B) + Dst MAC (6B) + Src MAC (6B) + EtherType (2B) + Payload (46–1500B) + FCS (4B).
7. **Minimum Frame Size**: 64 bytes total (46 bytes payload) to ensure collision detection over max collision domains under CSMA/CD.
8. **MTU vs. MSS**: MTU is Layer 3 limit (standard 1500B); MSS is TCP Layer 4 payload limit ($\text{MTU} - 40 = 1460\text{B}$).
9. **IP Fragmentation**: Handled via Identification, DF/MF flags, and Fragment Offset (in 8-byte units); reassembled strictly at destination.
10. **MAC Scope**: 48 bits, local subnet scope only. IP addresses provide global end-to-end addressing.

---

## 🧠 Practice Problems & Self-Check Questions

1. A network engineer runs `ping -s 2000 -M do 8.8.8.8` on Linux and receives an error message `ping: local error: message too long, mtu=1500`. Explain which flag in the IP header caused this drop and why.
2. A raw packet captured on an interface contains an EtherType of `0x86DD`. What network layer protocol is encapsulated?
3. Calculate the Fragment Offset value for the second fragment of a 3000-byte datagram traveling over a link with MTU 1000 bytes (assuming standard 20-byte IP header).
4. Why does an L2 switch ignore IP addresses, while an L3 router inspects them? Can an L2 switch forward traffic between two devices on different IP subnets?
5. What is the difference between an Ethernet broadcast MAC address and an IP broadcast address?
