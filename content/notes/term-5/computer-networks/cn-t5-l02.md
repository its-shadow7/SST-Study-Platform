# Network Packets, Layered Architecture & Data Link Communication
**Term:** Term 5 | **Subject:** CN | **Note ID:** `cn-t5-l02`
**Last Updated:** 2026-10-13T00:00:00Z

## Abstract & Summary
An exhaustive, rigorous deep dive into layered network design, the OSI vs. TCP/IP models, protocol encapsulation mechanics, Ethernet II framing standards, MAC address taxonomy, and Layer 2 switch forwarding and filtering algorithms.

## Learning Objectives
- Explain the theoretical and engineering justification for layered network architecture and protocol abstraction.
- Compare the 7-layer OSI reference model with the pragmatic 4/5-layer TCP/IP architectural model, categorizing Protocol Data Units (PDUs).
- Trace the end-to-end mechanics of encapsulation at the sender and decapsulation at the receiver across intermediate network hops.
- Dissect the byte-by-byte anatomy of an Ethernet II frame, explaining preambles, EtherType demultiplexing, minimum payload padding, and FCS CRC-32.
- Contrast link-layer MAC addressing (EUI-48, OUI, U/L and I/G bits) with network-layer IP addressing and transport-layer port numbers.
- Demonstrate how Layer 2 switches perform transparent bridging via the MAC learning algorithm, CAM tables, filtering, flooding, and aging.

## Key Takeaways
- Layering enforces modularity, abstraction, and independent protocol evolution; higher layers remain agnostic of lower-layer physical media.
- Protocol Data Units (PDUs) change terminology at each layer: Application Data/Message -> Transport Segment/Datagram -> Network Packet -> Data Link Frame -> Physical Bits.
- The Cardinal Invariant of Network Routing: End-to-end IP addresses remain invariant across hops, while link-layer MAC addresses are rewritten at every Layer 3 router interface.
- Ethernet II frames require a minimum length of 64 bytes (excluding preamble/SFD) to ensure reliable CSMA/CD collision detection, mandating padding for payloads under 46 bytes.
- MAC addresses are 48-bit (6-octet) identifiers split into a 24-bit IEEE Organizationally Unique Identifier (OUI) and a 24-bit vendor extension, featuring explicit Unicast/Multicast and Universal/Local bits.
- Transparent Layer 2 switches learn source MACs on ingress ports into a CAM table, forward frames to known destination ports, and flood unknown unicast or broadcast frames across all other active ports.

---

## 1. Why Layered Architecture? Modularity and Abstraction
### The Necessity of Protocols
In digital telecommunications, a **protocol** is a formal, standardized set of rules governing how two or more entities exchange data across a medium. A protocol specification strictly defines three dimensions:
1. **Syntax:** The structural format of data units—which fields exist, their bit lengths, and their exact byte order (e.g., big-endian network byte order).
2. **Semantics:** The operational meaning of individual fields—what specific action or control state a bit pattern signifies (e.g., an HTTP status code `404` vs. `200`, or a TCP `SYN` flag).
3. **Timing and Sequencing:** The chronological order in which messages must be transmitted and the rules for reacting to asynchronous events (e.g., timer expirations, retransmissions, handshakes).

---

### The Engineering Rationale for Layering
Networking involves an overwhelmingly broad spectrum of engineering challenges: modulating high-frequency electromagnetic waves across physical antennas, arbitrating access to shared copper media, routing packets across planetary topologies, guaranteeing byte-stream reliability over lossy channels, and serializing dynamic JSON objects in web browsers.

Attempting to implement all these capabilities in a single monolithic software protocol would produce an unmaintainable, brittle system. Instead, networking relies on a **layered architecture**.

```text
+------------------------------------------------------------------------+
|                            LAYERED SYSTEM BENEFITS                     |
+------------------------------------------------------------------------+
| 1. Modularity & Abstraction:                                           |
|    Each layer solves a well-defined sub-problem and presents a clean   |
|    API (service interface) to the layer above.                         |
|                                                                        |
| 2. Reusability:                                                        |
|    A single transport protocol (TCP) runs identically across diverse   |
|    link layers: Cat6 Ethernet, Wi-Fi 6, 5G Cellular, or DOCSIS Cable.  |
|                                                                        |
| 3. Independent Evolution:                                              |
|    Engineers can upgrade the physical and link layer to 800 Gbps fiber  |
|    optics without modifying a single line of web browser HTTP code!    |
|                                                                        |
| 4. Failure Isolation & Troubleshooting:                                |
|    Engineers diagnose faults methodically: if an IP ping succeeds,     |
|    Layers 1 through 3 are healthy; an application error is isolated    |
|    to Layers 4 through 7.                                              |
+------------------------------------------------------------------------+
```

### The Russian Nesting Dolls Analogy
A helpful mental model for layered networking is a set of **Russian nesting dolls** (matryoshka) or nested postal envelopes:
- The user's confidential letter (Application Data) is placed inside an inner envelope marked with the recipient's department (Transport Port).
- That envelope is sealed inside a shipping parcel addressed to the corporate campus street address (Network IP).
- The parcel is loaded into a postal delivery truck marked with the route to the next regional sorting depot (Data Link MAC).
- At each step, handlers inspect only the outer label relevant to their level of transport, leaving the inner contents intact.

**Citations & References:**
- RFC 1122 - Requirements for Internet Hosts -- Communication Layers
- Kurose & Ross, Computer Networking: A Top-Down Approach (8th Ed), Chapter 1.5
- Tanenbaum & Wetherall, Computer Networks (5th Ed), Section 1.3

---

## 2. The 7-Layer OSI Model vs. The Practical TCP/IP Architecture
### The OSI 7-Layer Reference Model (ISO 7498)
Developed in the 1980s by the International Organization for Standardization (ISO), the **Open Systems Interconnection (OSI)** model provides a theoretical framework dividing network functionality into 7 discrete vertical layers:

```text
┌───┬──────────────┬────────────────────────────────────────────────────────┐
│ # │ Layer Name   │ Primary Functional Responsibility & Core Standards     │
├───┼──────────────┼────────────────────────────────────────────────────────┤
│ 7 │ Application  │ User-facing network services (HTTP, DNS, SMTP, SSH)   │
├───┼──────────────┼────────────────────────────────────────────────────────┤
│ 6 │ Presentation │ Data formatting, compression, encryption (TLS, JSON)   │
├───┼──────────────┼────────────────────────────────────────────────────────┤
│ 5 │ Session      │ Dialog control, checkpointing, session tokens (RPC)    │
├───┼──────────────┼────────────────────────────────────────────────────────┤
│ 4 │ Transport    │ End-to-end reliability, multiplexing (TCP, UDP)       │
├───┼──────────────┼────────────────────────────────────────────────────────┤
│ 3 │ Network      │ Logical addressing, global internet routing (IPv4, IPv6)│
├───┼──────────────┼────────────────────────────────────────────────────────┤
│ 2 │ Data Link    │ Local frame delivery, physical addressing (Ethernet, MAC)│
├───┼──────────────┼────────────────────────────────────────────────────────┤
│ 1 │ Physical     │ Raw bit signaling across medium (voltages, light pulses)│
└───┴──────────────┴────────────────────────────────────────────────────────┘
```

**Mnemonic (Bottom-up: Layers 1 to 7):**  
"**P**lease **D**o **N**ot **T**hrow **S**ausage **P**izza **A**way"  
*(Physical -> Data Link -> Network -> Transport -> Session -> Presentation -> Application)*

---

### Why the OSI Model Lost in Implementation
Although the OSI model remains the universal *vocabulary* of networking (engineers routinely speak of "Layer 3 switches" and "Layer 7 load balancers"), the OSI protocol suite itself was never widely adopted on the Internet. 

Historians and computer scientists attribute this failure to the **"Apocalypse of the Two Elephants"**:
1. **Bad Timing:** By the time the ISO committee finished standardizing the 7-layer suite, TCP/IP had already been implemented and deployed across ARPANET and university Unix kernels for free.
2. **Bad Technology:** Layers 5 (Session) and 6 (Presentation) were thin, ambiguous, and almost empty in practice. Applications typically handle their own serialization and session logic directly.
3. **Bad Implementation:** Early OSI reference software implementations were notoriously bloated, slow, and resource-intensive compared to lean TCP/IP code.

---

### The Practical TCP/IP 4-Layer & 5-Layer Models
The actual operational architecture of the global Internet is the **TCP/IP model** (RFC 1122), often taught pedagogically as a 5-layer stack:

```text
   OSI 7-Layer Model                     TCP/IP 5-Layer Model
+---------------------+                 +---------------------+
| 7. Application      |                 |                     |
| 6. Presentation     |  ===========>   | 5. Application      | (HTTP, DNS, SSH, TLS)
| 5. Session          |                 |                     |
+---------------------+                 +---------------------+
| 4. Transport        |  ===========>   | 4. Transport        | (TCP, UDP)
+---------------------+                 +---------------------+
| 3. Network          |  ===========>   | 3. Network          | (IPv4, IPv6, ICMP)
+---------------------+                 +---------------------+
| 2. Data Link        |  ===========>   | 2. Data Link        | (Ethernet, 802.11 Wi-Fi)
+---------------------+                 +---------------------+
| 1. Physical         |  ===========>   | 1. Physical         | (Cables, Radio Waves)
+---------------------+                 +---------------------+
```

---

### Protocol Data Units (PDUs) Across the Stack
At each layer of the hierarchy, the unit of exchanged data has a formal standardized designation. Using precise terminology is critical during technical evaluations:

| Layer Number | Layer Name | Protocol Data Unit (PDU) | Primary Protocols |
| :--- | :--- | :--- | :--- |
| **Layer 5 (OSI 7)** | Application | **Data / Message** | HTTP/2, HTTP/3, DNS, SMTP, SSH, WebSocket |
| **Layer 4** | Transport | **Segment** (TCP) / **Datagram** (UDP) | TCP, UDP, QUIC, SCTP |
| **Layer 3** | Network | **Packet** / **Datagram** | IPv4, IPv6, ICMP, IPsec |
| **Layer 2** | Data Link | **Frame** | Ethernet (IEEE 802.3), Wi-Fi (802.11) |
| **Layer 1** | Physical | **Bits / Symbols** | Manchester, 1000BASE-T, NRZ, PAM-4 |

**Citations & References:**
- ISO/IEC 7498-1: Information technology -- Open Systems Interconnection
- RFC 1122 - Requirements for Internet Hosts -- Communication Layers
- Kurose & Ross, Computer Networking: A Top-Down Approach (8th Ed), Chapter 1.5
- Stevens, W. R., TCP/IP Illustrated, Volume 1: The Protocols

---

## 3. Encapsulation, Decapsulation, and Layer Invariants
### The Mechanics of Encapsulation
**Encapsulation** is the process whereby a protocol layer receives a data payload from the layer immediately above it, prepends its own protocol-specific **header** (and optionally appends a trailing trailer), and delivers the resulting Protocol Data Unit to the layer immediately below it.

```text
SENDER HOST (Moving DOWN the stack):
Application Layer:  [       HTTP Request Message Data        ]
                                     |
                                     v (passed to Transport)
Transport Layer:    [ TCP Header ] [        Application Payload        ]  ==> Segment
                                     |
                                     v (passed to Network)
Network Layer:      [ IP Header ] [  TCP Header  | Application Payload ]  ==> Packet
                                     |
                                     v (passed to Data Link)
Data Link Layer:    [ Eth Header ] [ IP Header | TCP Header | Data ] [ FCS Trailer ] ==> Frame
                                     |
                                     v (passed to Physical)
Physical Layer:     01101001011011100110010101110100... (Bits on the wire)
```

At each layer, everything received from the layer above is treated strictly as an **opaque payload**. The network layer does not inspect or understand the TCP sequence numbers inside its payload; it simply transports the segment inside an IP envelope.

---

### Decapsulation at the Receiver
When physical bits arrive at the destination host, the process is inverted (**decapsulation**):
1. **Physical Layer:** Receives signals, reconstructs digital bits, and passes them to the Data Link layer.
2. **Data Link Layer:** Verifies the Frame Check Sequence (FCS) checksum. If intact, it inspects the destination MAC address to ensure the frame was intended for this machine. It strips the Ethernet header/trailer, reads the **EtherType field** (e.g., `0x0800` for IPv4), and dispatches the payload upward to the IPv4 subsystem.
3. **Network Layer:** Verifies the IPv4 header checksum, validates the destination IP address, strips the IP header, reads the **Protocol field** (e.g., `6` for TCP, `17` for UDP), and dispatches the payload upward to the TCP subsystem.
4. **Transport Layer:** Inspects the TCP segment checksum, validates sequence numbers, strips the TCP header, reads the **Destination Port field** (e.g., `80` or `443`), and writes the reconstructed application byte stream into the target process's socket buffer.
5. **Application Layer:** The application process reads the clean HTTP GET request.

---

### The Cardinal Invariant of Network Traversal
One of the most vital principles in all of computer networking governs what fields change and what fields remain constant as a packet traverses intermediate routers:

```text
[Host A] ======> (Router R1) ======> (Router R2) ======> [Server B]
IP: 10.0.0.5     IP: 10.0.0.1        IP: 172.16.0.1      IP: 192.168.1.100
MAC: AA:AA:AA    MAC: BB:BB:BB       MAC: DD:DD:DD       MAC: FF:FF:FF
```

Across every standard hop along the journey:
- **The IP Packet Header REMAINS INVARIANT (End-to-End Scope):**
  - The **Source IP Address** (`10.0.0.5`) and **Destination IP Address** (`192.168.1.100`) do not change across hops (in the absence of NAT). The network layer specifies the ultimate origin and final destination across the global Internet.
  *(The only fields modified in transit are TTL, which is decremented by 1, and the IP Header Checksum).*
- **The Ethernet Frame Header CHANGES AT EVERY HOP (Hop-by-Hop Scope):**
  - **Hop 1 (Host A -> Router R1):** Source MAC = `AA:AA:AA`, Destination MAC = `BB:BB:BB` (R1's ingress MAC).
  - Router R1 strips the incoming Ethernet frame, performs an IP lookup, and builds an entirely new Ethernet frame for Hop 2!
  - **Hop 2 (Router R1 -> Router R2):** Source MAC = `CC:CC:CC` (R1's egress MAC), Destination MAC = `DD:DD:DD` (R2's ingress MAC).
  - Router R2 strips that frame and builds another for Hop 3!
  - **Hop 3 (Router R2 -> Server B):** Source MAC = `EE:EE:EE` (R2's egress MAC), Destination MAC = `FF:FF:FF` (Server B's MAC).

> **Key Rule to Memorize:** MAC addresses have **local link-layer significance only**. They never cross a Layer 3 boundary. IP addresses have **global end-to-end significance**.

**Citations & References:**
- RFC 791 - Internet Protocol
- RFC 894 - A Standard for the Transmission of IP Datagrams over Ethernet Networks
- Kurose & Ross, Computer Networking: A Top-Down Approach (8th Ed), Chapter 5.1-5.3

---

## 4. Deep Dive: Ethernet II Frame Anatomy, Minimum Sizes & MTU
### The Ethernet II (DIX) Frame Standard
The dominant link-layer framing format across global enterprise networks and the Internet is the **Ethernet II** framing standard (historically specified by DEC, Intel, and Xerox, later codified in IEEE 802.3).

```text
+----------+------+----------+----------+-----------+----------------------+---------+
| Preamble | SFD  | Dest MAC | Src MAC  | EtherType |   Payload (Data)     |   FCS   |
| 7 bytes  | 1 B  | 6 bytes  | 6 bytes  |  2 bytes  |   46 to 1500 bytes   | 4 bytes |
+----------+------+----------+----------+-----------+----------------------+---------+
|<--- PHY Overhead ------>|<------------------- Frame Overhead --------------------->|
```

#### Field-by-Field Dissection:
1. **Preamble (7 Bytes):** An alternating pattern of binary bits (`10101010` repeated 7 times). Used by the receiving physical Network Interface Card (NIC) to synchronize its clock frequency with the incoming electrical or optical bitstream.
2. **Start Frame Delimiter / SFD (1 Byte):** The byte sequence `10101011`. The concluding two consecutive `1`s break the synchronization pattern, signaling to the receiver that the very next bit represents the start of the actual frame header.
3. **Destination MAC Address (6 Bytes / 48 Bits):** The hardware link address of the destination interface on the local network segment.
4. **Source MAC Address (6 Bytes / 48 Bits):** The hardware link address of the transmitting interface.
5. **EtherType (2 Bytes):** A multiplexing key identifying which network-layer protocol is encapsulated within the payload:
   - `0x0800`: IPv4 (Internet Protocol Version 4)
   - `0x86DD`: IPv6 (Internet Protocol Version 6)
   - `0x0806`: ARP (Address Resolution Protocol)
   - `0x8100`: IEEE 802.1Q (VLAN Tagging)
6. **Payload (Data) (46 to 1500 Bytes):** The higher-layer PDU (typically an IPv4 or IPv6 packet).
7. **Frame Check Sequence / FCS (4 Bytes / 32 Bits):** A 32-bit **Cyclic Redundancy Check (CRC-32)** computed over all fields from the Destination MAC through the end of the Payload. If the receiver calculates a CRC that does not match the FCS, the frame is corrupted and is silently discarded.

---

### Why Must the Payload Be at Least 46 Bytes? (The Minimum 64-Byte Rule)
The official standard mandates that an Ethernet frame (excluding the Preamble and SFD) must be **at least 64 bytes** in total length:
$$\text{Minimum Frame Length} = 6\text{ (Dest MAC)} + 6\text{ (Src MAC)} + 2\text{ (EtherType)} + 46\text{ (Min Payload)} + 4\text{ (FCS)} = 64\text{ bytes}$$

If an application generates a payload smaller than 46 bytes (for example, a 20-byte TCP ACK packet with an empty payload inside a 20-byte IP packet = 40 bytes), the Data Link layer must append **padding bytes (`0x00`)** to bring the payload up to 46 bytes.

#### The Physics Behind the 64-Byte Limit:
In half-duplex legacy coaxial Ethernet networks using **CSMA/CD (Carrier Sense Multiple Access with Collision Detection)**:
- When a host transmits a frame, it must continue transmitting long enough to detect if another host on the farthest end of the cable (up to 2.5 km away across repeaters) transmitted at the same time.
- The worst-case round-trip propagation time across the maximum allowed network diameter was roughly $51.2\;\mu s$.
- On a 10 Mbps Ethernet link, transmitting for $51.2\;\mu s$ produces:
  $$\text{Bits transmitted} = 10\text{ Mbps} \times 51.2\;\mu s = 512\text{ bits} = 64\text{ bytes}$$
- If a frame were shorter than 64 bytes, a host could finish transmitting and believe the frame was sent successfully before the collision signal arrived back, corrupting communication without detection!
- Even though modern switched Ethernet networks run full duplex with zero collisions, the 64-byte minimum frame size is permanently preserved for backward compatibility.

---

### Maximum Transmission Unit (MTU)
The **Maximum Transmission Unit (MTU)** defines the maximum size of a Layer 3 packet (in bytes) that can be encapsulated into a Layer 2 frame without fragmentation.
- Standard Ethernet MTU: **1500 bytes**
- Total Maximum Ethernet Frame Size: $1500\text{ (Payload)} + 14\text{ (Header)} + 4\text{ (FCS)} = 1518\text{ bytes}$ (or 1522 bytes with 802.1Q VLAN tagging).
- **Jumbo Frames:** Specialized enterprise data center and SAN networks support MTUs up to **9000 bytes**, dramatically reducing CPU interrupt overhead when moving massive storage volumes.

#### IP Fragmentation
If a router receives an IP packet of length 1500 bytes but must forward it across an outgoing link with an MTU of 1280 bytes (common on VPN tunnels):
- If the packet's `DF` (Don't Fragment) flag is set to `0`, the router divides the packet into multiple smaller IP fragments.
- If the `DF` flag is set to `1`, the router drops the packet and sends an ICMP "Fragmentation Needed and DF set" message back to the sender, triggering **Path MTU Discovery (PMTUD)**.

**Citations & References:**
- IEEE 802.3 Standard for Ethernet
- RFC 894 - A Standard for the Transmission of IP Datagrams over Ethernet Networks
- RFC 1191 - Path MTU Discovery
- Kurose & Ross, Computer Networking: A Top-Down Approach (8th Ed), Chapter 5.4

---

## 5. Addressing Hierarchy: Ports, IP Addresses, and MAC Addresses
### The Three Tiers of Network Addressing
To ensure an incoming data payload finds its exact destination process, modern operating systems coordinate three distinct addressing namespaces:

```text
+------------------------------------------------------------------------+
| Level 3: Port Number (Transport Layer - Layer 4)                       |
| Identifies the specific OS PROCESS / APPLICATION SOCKET                |
| Scope: Local to the host operating system kernel (16-bit: 0 - 65,535)  |
+------------------------------------------------------------------------+
                                   ^
                                   | Multiplexed into
+------------------------------------------------------------------------+
| Level 2: IP Address (Network Layer - Layer 3)                          |
| Identifies the HOST INTERFACE on the global internetwork               |
| Scope: Global, hierarchical logical addressing (32-bit IPv4 / 128-bit) |
+------------------------------------------------------------------------+
                                   ^
                                   | Routed across
+------------------------------------------------------------------------+
| Level 1: MAC Address (Data Link Layer - Layer 2)                       |
| Identifies the PHYSICAL NETWORK INTERFACE CARD (NIC) on the local link |
| Scope: Link-local flat addressing (48-bit EUI-48)                      |
+------------------------------------------------------------------------+
```

---

### Deep Dive: MAC Address Architecture (EUI-48)
A Media Access Control (MAC) address is a **48-bit (6-byte)** identifier assigned to a network interface controller. It is conventionally written as six pairs of hexadecimal digits separated by colons or hyphens:
$$\text{Example: } \mathbf{3C:52:82:A1:4F:02}$$

```text
+-------------------------------+-------------------------------+
|  Organizationally Unique      |  Network Interface Controller |
|  Identifier (OUI - 24 bits)   |  (NIC Extension - 24 bits)    |
+-------------------------------+-------------------------------+
| Octet 1 | Octet 2 | Octet 3   | Octet 4 | Octet 5 | Octet 6   |
+---------+---------+--------- -+---------+---------+-----------+
  3C   :     52   :    82       :    A1   :    4F   :    02
```

1. **Organizationally Unique Identifier (OUI - First 24 bits):** Assigned exclusively by the IEEE to hardware manufacturers (e.g., Apple, Intel, Cisco, Realtek). Looking up an OUI reveals the hardware vendor.
2. **Vendor Extension (Last 24 bits):** Uniquely assigned by the manufacturer to each physical chip during fabrication, historically termed the **Burned-In Address (BIA)**.

#### The Two Magic Bits in Octet 1:
The least-significant bits of the **very first octet** of a MAC address have critical architectural meanings:

```text
First Octet Binary: [ b7  b6  b5  b4  b3  b2  b1  b0 ]
                                              ^   ^
                                              |   +--- Bit 0: I/G (Individual / Group)
                                              +------- Bit 1: U/L (Universal / Local)
```

- **Bit 0: I/G (Individual / Group Bit):**
  - `0`: **Individual Address (Unicast).** Destined for a single specific network interface.
  - `1`: **Group Address (Multicast / Broadcast).** Destined for multiple network interfaces.
  *(Example: `FF:FF:FF:FF:FF:FF` has `0xFF` = `11111111_2` where bit 0 is `1` -> Broadcast).*
- **Bit 1: U/L (Universal / Local Bit):**
  - `0`: **Universally Administered.** Factory-assigned by the IEEE and vendor (guaranteed globally unique).
  - `1`: **Locally Administered.** Overridden by a network administrator, virtual machine hypervisor, or operating system privacy randomization.

#### MAC Address Randomization in Modern Operating Systems
Modern mobile and desktop operating systems (iOS, Android, Windows 11, macOS) enable **MAC address randomization** by default when connecting to Wi-Fi networks:
- If a smartphone always broadcast its factory BIA, shopping malls and public venues could track an individual's physical movements across the city via ambient Wi-Fi probe requests.
- Randomization generates a locally administered MAC (with the U/L bit set to `1`) unique to each Wi-Fi SSID, preserving user privacy without violating link-layer protocols.

**Citations & References:**
- IEEE Standard 802-2014 - IEEE Standard for Local and Metropolitan Area Networks
- RFC 7042 - IANA Considerations and IETF Protocol and Documentation Usage for IEEE 802 Numbers
- Comer, Internetworking with TCP/IP Vol. 1 (6th Ed), Chapter 2

---

## 6. Data Link Delivery Modes & Layer 2 Switch Operations
### Frame Delivery Modes
Link-layer communication across a local area network operates under three transmission modes:

1. **Unicast:** The frame specifies the individual MAC address of a single destination NIC (I/G bit = `0`). Only the targeted NIC processes the frame; other stations ignore it.
2. **Broadcast:** The frame is addressed to the universal broadcast address **`FF:FF:FF:FF:FF:FF`** (all 48 bits set to `1`). Every active interface on the local Layer 2 broadcast domain must ingest and process the frame. Broadcasts are used by discovery protocols such as ARP and DHCP.
3. **Multicast:** The frame is addressed to a specialized group MAC address (e.g., `01:00:5E:xx:xx:xx` for IPv4 multicast). Only interfaces that have explicitly joined that multicast group process the frame.

---

### How Layer 2 Switches Work: Transparent Bridging
A modern **Layer 2 Switch** is an intelligent multi-port link-layer device that connects multiple hosts within a local network. Unlike legacy hubs, switches provide **micro-segmentation**: every single port on a switch represents an **independent collision domain** operating in full-duplex mode.

A switch operates as a **transparent bridge**: hosts do not need to be configured with the switch's existence; it plugs in and begins operating automatically without manual network topology configuration.

```text
                          +------------------------+
                          |   Layer 2 Switch CAM   |
                          |      MAC Table         |
                          | Port 1 -> AA:AA:AA     |
                          | Port 2 -> BB:BB:BB     |
                          | Port 3 -> CC:CC:CC     |
                          +------------------------+
                               /      |      \
                       Port 1 /Port 2 | Port 3\
                             v        v        v
                         [Host A]  [Host B]  [Host C]
```

---

### The Three Operating Rules of a Layer 2 Switch
A switch maintains a **CAM (Content Addressable Memory) Table** or **MAC Address Table**, mapping `MAC Address -> (Port Number, Aging Timer)`. For every incoming frame arriving on port $P$, the switch applies three strict rules:

#### Rule 1: The Learning Rule (Examine SOURCE MAC)
- Whenever a frame arrives on ingress port $P$, the switch inspects the **Source MAC address**.
- The switch records or refreshes the mapping:
  $$\text{Source MAC} \longrightarrow \text{Port } P$$
- An **aging timer** (default 300 seconds / 5 minutes) is started or reset for that entry. If no traffic arrives from that MAC address before the timer expires, the entry is purged to handle disconnected or moved laptops.

#### Rule 2: The Forwarding / Filtering Rule (Examine DESTINATION MAC)
The switch inspects the **Destination MAC address** and checks its CAM table:
- **Case A (Known MAC on a different port):** If the destination MAC is in the table on port $Q$ (where $Q \neq P$), the switch forwards the frame **strictly out of port $Q$**. No other ports see the frame!
- **Case B (Filtering):** If the destination MAC is mapped to the *same* port $P$ where it arrived, the switch **filters (drops)** the frame because the destination already received it on that shared segment.

#### Rule 3: The Flooding Rule (Unknown Unicast or Broadcast)
- If the destination MAC address is **not present** in the CAM table (an **Unknown Unicast**), OR if the destination MAC is the **broadcast address (`FF:FF:FF:FF:FF:FF`)**, the switch **floods** the frame:
- It transmits a copy of the frame out of **every single active port EXCEPT the ingress port $P$** on which it arrived!

```text
WALKTHROUGH: Initial State (CAM Table Empty)
1. Host A (AA:AA) sends frame to Host B (BB:BB) on Port 1.
   - Learning: Switch learns [AA:AA -> Port 1].
   - Forwarding: BB:BB is UNKNOWN in table!
   - Action: Floods frame out Port 2 and Port 3.
2. Host B (BB:BB) receives the frame and replies to Host A (AA:AA) on Port 2.
   - Learning: Switch learns [BB:BB -> Port 2].
   - Forwarding: AA:AA IS KNOWN (Port 1)!
   - Action: Direct Unicast forwarding to Port 1 ONLY. Port 3 never sees this frame!
```

**Citations & References:**
- IEEE 802.1D Standard for Local and metropolitan area networks: Media Access Control (MAC) Bridges
- Kurose & Ross, Computer Networking: A Top-Down Approach (8th Ed), Chapter 5.4
- Perlman, R., Interconnections: Bridges, Routers, Switches, and Internetworking Protocols (Addison-Wesley)

---
