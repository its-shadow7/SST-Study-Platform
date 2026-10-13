"""
Data module for Term 5 Lecture 10:
Transport Layer & TCP Reliability
Strictly 0 occurrences of forbidden instructor names.
"""

L10_DATA = {
    "schema_version": 1,
    "note_id": "cn-t5-l10",
    "term": "Term 5",
    "subject_code": "CN",
    "topic_title": "Transport Layer, TCP Reliability & Socket Programming",
    "tags": [
        "Networking",
        "Transport Layer",
        "TCP",
        "UDP",
        "Three-Way Handshake",
        "Four-Way Close",
        "Flow Control",
        "Congestion Control",
        "Sliding Window",
        "Fast Retransmit",
        "Socket Programming"
    ],
    "learning_objectives": [
        "Explain the transport layer's role in process-to-process multiplexing and demultiplexing via port addressing.",
        "Compare TCP and UDP architectures, header structures, and design trade-offs across real-time and reliable applications.",
        "Trace the TCP 3-way connection establishment handshake, sequence number synchronization, and ISN randomization.",
        "Analyze TCP 4-way termination, the half-closed state, and the engineering necessity of the 2MSL TIME_WAIT state.",
        "Model TCP reliability mechanisms: cumulative ACKs, Round-Trip Time (RTT) estimation, Retransmission Timeouts (RTO), and Fast Retransmit via 3 duplicate ACKs.",
        "Distinguish between Receiver Flow Control (sliding window rwnd) and Network Congestion Control (cwnd, Slow Start, AIMD).",
        "Implement network client-server communication using low-level socket programming in Python (TCP stream and UDP datagram)."
    ],
    "summary": "An exhaustive, rigorous masterclass on the Transport Layer. Covers process-to-process addressing via 16-bit ports, contrasting lightweight UDP with the Transmission Control Protocol (TCP). Deconstructs the TCP 3-way handshake, 4-way teardown, TIME_WAIT state, cumulative acknowledgment mathematics, sliding window flow control, Reno/Tahoe congestion control algorithms, and socket programming implementations.",
    "key_takeaways": [
        "The Transport Layer provides logical process-to-process communication, abstracting the underlying network of routers into direct end-to-end socket connections.",
        "Ports are 16-bit integers (0 to 65535) divided into Well-Known (0-1023), Registered (1024-49151), and Ephemeral/Dynamic (49152-65535) ranges.",
        "UDP is an 8-byte, connectionless, unreliable datagram transport optimized for low latency, broadcast, or custom application-layer transport protocols (like QUIC).",
        "TCP guarantees reliable, ordered byte-stream delivery with flow control and congestion control using a 20-to-60 byte header with sequence numbers and control flags.",
        "The 3-way handshake synchronizes Initial Sequence Numbers (ISNs) to prevent stale ghost segments from corrupting new connections; the 4-way teardown gracefully closes bidirectional streams, concluding with a 2MSL TIME_WAIT state.",
        "Flow control prevents the sender from overwhelming the receiver's buffer via rwnd; Congestion control prevents the sender from saturating the network bottleneck link via cwnd (Slow Start exponential growth, AIMD additive increase / multiplicative decrease).",
        "Retransmissions are triggered either by an RTO timer expiration (severe delay) or Fast Retransmit upon receiving 3 duplicate ACKs (immediate loss recovery)."
    ],
    "last_updated": "2026-10-14T00:00:00Z",
    "approval_status": "approved",
    "sections": [
        {
            "section_id": "sec-l10-01",
            "heading": "Transport Layer Fundamentals: Process Addressing & Multiplexing",
            "body": "### The Need for Process-to-Process Communication\n\nThe Network Layer (Layer 3) is responsible for host-to-host delivery: an IP packet successfully reaches a physical machine with a destination IP address. However, a modern computer executes dozens of concurrent network processes (web browsers, SSH terminals, database engines, messaging daemons). The Network Layer has no mechanism to determine which application process should receive an incoming packet.\n\nThe **Transport Layer (Layer 4)** bridges this boundary by providing **process-to-process logical communication** through the abstraction of **Port Numbers** and **Sockets**:\n\n```\n                                  HOST A (Client)\n         ┌──────────────┐         ┌──────────────┐         ┌──────────────┐\n         │ Web Browser  │         │  SSH Client  │         │ Spotify App  │\n         │ (Port 52341) │         │ (Port 48102) │         │ (Port 55190) │\n         └──────┬───────┘         └──────┬───────┘         └──────┬───────┘\n                │                        │                        │\n                └────────────────────────┼────────────────────────┘\n                                         ▼\n                            TRANSPORT LAYER (Layer 4)\n                          Multiplexing: Adds Port Headers\n                                         ▼\n                             NETWORK LAYER (Layer 3)\n                           Encapsulates into IP Packets\n                                         ▼\n                                  INTERNET CORE\n                                         ▼\n                             NETWORK LAYER (Layer 3)\n                                         ▼\n                            TRANSPORT LAYER (Layer 4)\n                        Demultiplexing: Reads Dst Port\n                                         ▼\n                            ┌────────────────────────┐\n                            │ Web Server (Port 443)  │\n                            └────────────────────────┘\n                                  HOST B (Server)\n```\n\n### The Socket Tuple\nA network endpoint is defined as a **Socket Address** (`IP Address : Port Number`). An active, established TCP connection across the Internet is uniquely identified by an immutable **5-Tuple**:\n$$\\text{Connection Identifier} = \\big( \\text{Protocol}, \\text{Source IP}, \\text{Source Port}, \\text{Destination IP}, \\text{Destination Port} \\big)$$\n\nBecause of this 5-tuple demultiplexing rule, a web server listening on port `443` (`0.0.0.0:443`) can maintain hundreds of thousands of concurrent active TCP connections simultaneously, as long as each client has a distinct combination of Source IP and Source Port.\n\n### Port Number Taxonomy (RFC 6335)\nPorts are 16-bit unsigned integers spanning from $0$ to $65,535$ ($2^{16}$ possible ports), categorized into three standardized tiers:\n\n1. **Well-Known Ports ($0 - 1,023$)**:\n   - Assigned by the Internet Assigned Numbers Authority (IANA) for core system protocols.\n   - On UNIX/Linux systems, binding to a well-known port requires root privileges (`sudo`).\n   - Examples: `20/21` (FTP), `22` (SSH), `25` (SMTP), `53` (DNS), `80` (HTTP), `443` (HTTPS), `123` (NTP).\n2. **Registered Ports ($1,024 - 49,151$)**:\n   - Registered by software vendors for specific application services; non-root processes can bind to them.\n   - Examples: `3306` (MySQL), `5432` (PostgreSQL), `6379` (Redis), `8080` (HTTP alternate), `27017` (MongoDB).\n3. **Dynamic / Ephemeral / Private Ports ($49,152 - 65,535$)**:\n   - Automatically assigned by the host operating system kernel to client sockets upon initiating outbound connections.",
            "citations": [
                "RFC 6335: Internet Assigned Numbers Authority (IANA) Procedures for the Management of the Service Name and Transport Protocol Port Number Registry",
                "Computer Networks: A Systems Approach, Chapter 5 (End-to-End Protocols)",
                "Computer Networking: A Top-Down Approach (Kurose & Ross), Chapter 3 (Transport Layer)"
            ]
        },
        {
            "section_id": "sec-l10-02",
            "heading": "UDP Architecture: Lightweight, Connectionless Datagrams",
            "body": "### The Minimalist Transport Protocol\n\nThe **User Datagram Protocol (UDP)**, defined in RFC 768 by David P. Reed in 1980, is the simplest possible transport layer protocol. UDP adds almost nothing to IP other than port-based process multiplexing and basic error detection.\n\n#### The 8-Byte UDP Header Anatomy\nWhile TCP requires a minimum of 20 bytes (and up to 60 bytes with options), the UDP header is strictly **8 bytes** in size:\n\n```\n 0                   15 16                  31\n┌──────────────────────┬──────────────────────┐\n│     Source Port      │   Destination Port   │   (4 Bytes)\n├──────────────────────┼──────────────────────┤\n│    Length (bytes)    │       Checksum       │   (4 Bytes)\n└──────────────────────┴──────────────────────┘\n│               Data Payload ...              │\n```\n\n1. **Source Port (16 bits)**: Port of the sending process (optional; set to 0 if no reply is expected).\n2. **Destination Port (16 bits)**: Port of the destination process.\n3. **Length (16 bits)**: Total length in bytes of the UDP header plus UDP payload (minimum value is 8).\n4. **Checksum (16 bits)**: Error-detection checksum covering the UDP header, payload, and an IPv4/IPv6 **pseudo-header** (containing source/destination IPs to detect misrouted datagrams). In IPv4, checksum is optional (set to 0 to disable); in IPv6, checksum is **strictly mandatory**.\n\n### Core Properties of UDP\n- **Connectionless**: No handshake or teardown. Senders transmit immediately without negotiating state.\n- **Unreliable Delivery**: Datagrams may be lost, reordered, or duplicated in transit without warning. UDP provides zero ACKs and zero retransmissions.\n- **Message-Oriented (Preserves Framing)**: UDP preserves application message boundaries. If an application calls `sendto()` with 500 bytes, the receiver's `recvfrom()` returns exactly that 500-byte datagram in a single read, unlike TCP's continuous byte stream.\n- **Zero Congestion Control**: Senders can blast datagrams at the physical link rate regardless of network congestion.\n\n### Production Use Cases for UDP\n\n| Domain | Why UDP is Required | Engineering Rationale |\n| :--- | :--- | :--- |\n| **DNS (Port 53)** | Query/Response speed | Single request-reply cycle; a 3-way TCP handshake would double latency from 1 RTT to 2 RTT. |\n| **DHCP (Ports 67/68)** | Broadcast capability | Clients have no IP yet; TCP cannot broadcast across a LAN segment. |\n| **Real-Time Audio / Video (VoIP / WebRTC)**| Timeliness over perfection | In a live voice call, an audio packet arriving 300 ms late due to TCP retransmission is useless noise. Skipping lost packets is preferable to freezing playback. |\n| **Multiplayer Online Gaming** | Low-latency state sync | Player positions update at 60 Hz. Old positional updates are superseded by newer ones; stalling for retransmission creates unbearable input lag. |\n| **HTTP/3 & QUIC** | Userspace transport | Builds modern multiplexing, encryption, and reliability on top of UDP to bypass operating system kernel update delays and middlebox ossification. |",
            "citations": [
                "RFC 768: User Datagram Protocol (David P. Reed)",
                "RFC 5405: Unicast UDP Usage Guidelines for Application Designers",
                "Computer Networks: A Systems Approach, Chapter 5.1 (Simple Demultiplexor - UDP)"
            ]
        },
        {
            "section_id": "sec-l10-03",
            "heading": "TCP Architecture: Reliable, Connection-Oriented Byte Streams",
            "body": "### The Transmission Control Protocol (TCP)\n\nDefined in RFC 793, TCP transforms an inherently unreliable, best-effort packet network (IP) into a rock-solid, fully reliable, ordered, bi-directional **virtual byte stream**.\n\n```\n 0                   15 16                  31\n┌──────────────────────┬──────────────────────┐\n│     Source Port      │   Destination Port   │\n├──────────────────────┴──────────────────────┤\n│               Sequence Number               │\n├─────────────────────────────────────────────┤\n│            Acknowledgment Number            │\n├──────┬─────────┬─────┬──────────────────────┤\n│Offset│ Reserved│Flags│     Window Size      │\n├──────┴─────────┴─────┼──────────────────────┤\n│       Checksum       │    Urgent Pointer    │\n├──────────────────────┴──────────────────────┤\n│          Options (0 to 40 bytes) ...        │\n└─────────────────────────────────────────────┘\n│               Data Payload ...              │\n```\n\n#### Deep Header Field Analysis\n1. **Sequence Number (32 bits)**:\n   - Identifies the byte offset of the first data byte in this segment within the overall transmitted stream.\n   - If the `SYN` flag is set ($1$), this field represents the **Initial Sequence Number (ISN)**, and the first actual data byte begins at $\\text{ISN} + 1$.\n2. **Acknowledgment Number (32 bits)**:\n   - Valid only when the `ACK` flag is set.\n   - Contains the **next sequence number the receiver is expecting to receive**. Acknowledgment is **cumulative**: an ACK of $N$ confirms that all bytes from $0$ up to $N - 1$ have been successfully received.\n3. **Data Offset / Header Length (4 bits)**:\n   - Specifies the size of the TCP header in 32-bit (4-byte) words. Minimum value is $5$ ($5 \\times 4 = 20$ bytes); maximum is $15$ ($15 \\times 4 = 60$ bytes).\n4. **Control Flags (6 to 9 bits)**:\n   - **SYN (Synchronize)**: Initiates a connection; synchronizes Initial Sequence Numbers.\n   - **ACK (Acknowledgment)**: Signifies that the Acknowledgment Number field is valid.\n   - **FIN (Finish)**: Sender has completed transmitting data; initiates connection teardown.\n   - **RST (Reset)**: Aborts an invalid connection, rejects connection attempts, or recovers from fatal errors.\n   - **PSH (Push)**: Instructs receiver to push buffered data immediately to the application layer.\n   - **URG (Urgent)**: Indicates that the Urgent Pointer field is valid (legacy out-of-band data).\n5. **Window Size (`rwnd`, 16 bits)**:\n   - Advertises the receiver's currently available receive buffer capacity in bytes for flow control.\n   - Allows a maximum window of $65,535$ bytes, extendable up to $1$ gigabyte using the **Window Scale Option** (RFC 7323).\n6. **Checksum (16 bits)**:\n   - Mandatory error check computed over the TCP header, payload, and IP pseudo-header.",
            "citations": [
                "RFC 793: Transmission Control Protocol (DARPA Internet Program Protocol Specification)",
                "RFC 7323: TCP Extensions for High Performance (Window Scale, Timestamps)",
                "TCP/IP Illustrated, Volume 1: The Protocols (W. Richard Stevens), Chapter 17"
            ]
        },
        {
            "section_id": "sec-l10-04",
            "heading": "TCP Connection Lifecycle: The 3-Way Handshake & 4-Way Teardown",
            "body": "### The 3-Way Handshake (Connection Setup)\n\nBefore a single byte of application data can be exchanged, the client and server must agree on socket state, synchronize Initial Sequence Numbers (ISNs), and negotiate options (e.g., Maximum Segment Size - MSS, Window Scaling, Selective Acknowledgment - SACK):\n\n```\n   Client (State)                                                   Server (State: LISTEN)\n         │                                                                    │\n         │ ─── Step 1: SYN (seq = x) ───────────────────────────────────────► │\n   SYN_SENT                                                                SYN_RCVD\n         │                                                                    │\n         │ ◄── Step 2: SYN-ACK (seq = y, ack = x + 1) ────────────────────── │\n  ESTABLISHED                                                                 │\n         │                                                                    │\n         │ ─── Step 3: ACK (seq = x + 1, ack = y + 1) [Piggyback Data OK] ──► │\n         │                                                                 ESTABLISHED\n```\n\n1. **Step 1: Client sends `SYN`**\n   - Flags: `SYN=1, ACK=0`\n   - Header: `Sequence Number = x` (random client ISN). Note: SYN consumes $1$ phantom sequence number even though it carries zero payload bytes!\n   - Client enters `SYN_SENT` state.\n2. **Step 2: Server replies `SYN-ACK`**\n   - Flags: `SYN=1, ACK=1`\n   - Header: `Sequence Number = y` (random server ISN), `Acknowledgment Number = x + 1` (confirms receipt of client's SYN).\n   - Server enters `SYN_RCVD` state.\n3. **Step 3: Client sends `ACK`**\n   - Flags: `ACK=1, SYN=0`\n   - Header: `Sequence Number = x + 1`, `Acknowledgment Number = y + 1` (confirms server's SYN).\n   - Client enters `ESTABLISHED`. Upon receiving this segment, the server enters `ESTABLISHED`.\n\n#### Why Random Initial Sequence Numbers (ISNs)?\nISNs are generated pseudo-randomly (RFC 6528) rather than starting at $0$ for two critical reasons:\n1. **Ghost Packet Immunity**: If a previous TCP connection between the same pair of ports terminated abruptly, delayed packets drifting through the Internet could arrive and be injected into a newly opened connection if sequence numbers overlapped.\n2. **TCP Sequence Prediction Attacks (Kevin Mitnick Attack)**: If ISNs were predictable (e.g., incremented by a constant counter), a blind remote attacker could spoof trusted IP addresses and inject malicious data into TCP sessions.\n\n---\n\n### The 4-Way Teardown (Connection Termination)\nBecause TCP connections are full-duplex (two independent data streams in opposite directions), each direction must be terminated independently:\n\n```\n   Client (ESTABLISHED)                                            Server (ESTABLISHED)\n         │                                                                    │\n         │ ─── Step 1: FIN (seq = u) ───────────────────────────────────────► │\n    FIN_WAIT_1                                                             CLOSE_WAIT\n         │                                                                    │\n         │ ◄── Step 2: ACK (ack = u + 1) ─────────────────────────────────── │\n    FIN_WAIT_2                                                                │\n         │                                                       (Server finishes sending)\n         │                                                                    │\n         │ ◄── Step 3: FIN (seq = v) ─────────────────────────────────────── │\n     TIME_WAIT                                                             LAST_ACK\n         │                                                                    │\n         │ ─── Step 4: ACK (ack = v + 1) ───────────────────────────────────► │\n         │                                                                  CLOSED\n    [Waits 2MSL]\n         ▼\n       CLOSED\n```\n\n#### The Engineering Rationale for TIME_WAIT (2MSL)\nAfter transmitting the final `ACK` (Step 4), the active closer does not immediately transition to `CLOSED`. Instead, it enters the **`TIME_WAIT`** state for a duration of **$2 \\times \\text{MSL}$ (Maximum Segment Lifetime)**, typically $60$ seconds (or $120$ seconds in standard RFC 793):\n1. **Ensure Graceful Final ACK Delivery**: If the client's final `ACK` is lost in transit, the server will time out and retransmit its `FIN`. If the client were already `CLOSED`, it would respond with an abrupt `RST`, causing the server to believe the connection terminated abnormally with data loss.\n2. **Draining Delayed Segments**: Ensures that all wandering, delayed duplicate packets belonging to this connection die in the network before their sequence numbers could contaminate a subsequent incarnation of the same 5-tuple.",
            "citations": [
                "RFC 793: Transmission Control Protocol, Section 3.4 (Establishing a Connection)",
                "RFC 6528: Defending Against Sequence Number Attacks",
                "UNIX Network Programming, Volume 1 (W. Richard Stevens), Chapter 2"
            ]
        },
        {
            "section_id": "sec-l10-05",
            "heading": "TCP Reliability & Flow Control: Sliding Windows and Fast Retransmit",
            "body": "### Cumulative Acknowledgments & Retransmission Timers\n\nTCP views data as a continuous stream of numbered bytes. The receiver acknowledges bytes **cumulatively**: `ACK = N` means *\"I have successfully received and assembled all bytes up to $N - 1$. I am expecting byte $N$.\"*\n\n```\n Sender transmits:    [Bytes 1–1000]     [Bytes 1001–2000]    [Bytes 2001–3000 (LOST!)]    [Bytes 3001–4000]\n Receiver replies:     ACK 1001           ACK 2001                                          ACK 2001 (Dup 1!)\n                                                              [Bytes 4001–5000] ──►         ACK 2001 (Dup 2!)\n                                                              [Bytes 5001–6000] ──►         ACK 2001 (Dup 3!)\n                                                                                            ▲\n                                                              3 DUPLICATE ACKs RECEIVED! ───┘\n                                                              Sender immediately fires FAST RETRANSMIT:\n                                                              Retransmits [Bytes 2001–3000] WITHOUT waiting for RTO!\n```\n\n#### Loss Recovery Mechanisms\n1. **Retransmission Timeout (RTO)**:\n   - For every segment sent, TCP runs an RTO timer calculated from exponential weighted moving averages of measured RTT (Jacobson's algorithm, RFC 6298):\n     $$\\text{SRTT} = (1 - \\alpha) \\cdot \\text{SRTT} + \\alpha \\cdot \\text{RTT}$$   $$\\text{RTTVAR} = (1 - \\beta) \\cdot \\text{RTTVAR} + \\beta \\cdot |\\text{SRTT} - \\text{RTT}|$$   $$\\text{RTO} = \\text{SRTT} + 4 \\cdot \\text{RTTVAR}$$\n   - If the timer expires before an ACK arrives, the sender retransmits the oldest unacknowledged segment. RTO expiration is an emergency fallback: it forces the sender back to Slow Start ($cwnd = 1\\text{ MSS}$), crushing throughput.\n2. **Fast Retransmit (3 Duplicate ACKs)**:\n   - When an out-of-order segment arrives at the receiver (e.g., segment 3 was lost, but segments 4, 5, and 6 arrived), the receiver cannot ACK beyond 2000. It repeatedly transmits duplicate ACKs with `ACK = 2001`.\n   - When the sender receives **3 duplicate ACKs** (total of 4 identical ACKs for byte 2001), it infers that packet 2001 was dropped while subsequent packets reached the receiver.\n   - Rather than waiting for the sluggish RTO timer to expire, the sender immediately retransmits the missing segment (**Fast Retransmit**) and enters **Fast Recovery**.\n\n### Receiver Flow Control: The Sliding Window (`rwnd`)\nFlow control ensures that a fast sending sender does not overflow the memory buffer of a slow receiving host.\n\n$$\\text{Effective Window} = \\min(rwnd, cwnd)$$\n\n- The receiver advertises its available buffer space in every TCP segment header: `Window Size = rwnd`.\n- The sender maintains three logical pointer offsets:\n  - Bytes Sent and Acknowledged\n  - Bytes Sent but In-Flight (unacknowledged)\n  - Bytes Allowed to Send Immediately without waiting for ACKs\n- **Zero Window Probe**: If the receiver's application is blocked and the receive buffer fills completely, the receiver sends `rwnd = 0`. The sender stops transmitting data immediately. To prevent a deadlock if the subsequent window update is lost, the sender periodically sends 1-byte **Zero Window Probes** to force the receiver to re-advertise its current buffer state.",
            "citations": [
                "RFC 6298: Computing TCP's Retransmission Timer",
                "RFC 5681: TCP Congestion Control (Fast Retransmit and Fast Recovery)",
                "Computer Networks: A Systems Approach, Chapter 5.2 (Reliable Transmission)"
            ]
        },
        {
            "section_id": "sec-l10-06",
            "heading": "TCP Congestion Control: Slow Start, AIMD & Modern Algorithms",
            "body": "### The Distinction Between Flow Control and Congestion Control\n\n- **Flow Control (`rwnd`)**: Protects the **destination host**'s internal memory buffer.\n- **Congestion Control (`cwnd`)**: Protects the **shared intermediate network** (routers and bottleneck switches) from collapsing under buffer overflow.\n\n```\n                                        TCP RENO LIFECYCLE\n\n     cwnd (MSS)\n         ▲\n         │                                         Timeout (RTO) ──► cwnd resets to 1\n      32 │                              /\\                           │\n         │                             /  \\  ◄── 3 Dup ACKs          │\n      16 │             ssthresh ──►   /    \\     (Fast Recovery)     │\n         │                           /      \\                        │\n       8 │                          /        \\                       │\n         │                         /          \\                      │\n       4 │                        /            \\                     │\n       2 │        /\\             /              \\                    │\n       1 │  ─────/  ────────────/                ────────────────────/──────► Time\n             Slow Start   Congestion Avoidance    Congestion Avoidance  Slow Start\n            (Exponential)     (Linear AIMD)           (Linear AIMD)    (Exponential)\n```\n\n### The Classical Phases of TCP Congestion Control (RFC 5681)\n\n1. **Slow Start**:\n   - Starts conservatively with $cwnd = 1$ to $10\\text{ MSS}$ (Initial Window).\n   - For every ACK received, $cwnd$ increments by $1\\text{ MSS}$. Consequently, for every round trip time (RTT), $cwnd$ **doubles** exponentially ($1 \\to 2 \\to 4 \\to 8 \\to 16$).\n   - Continues until $cwnd$ reaches the **Slow Start Threshold (`ssthresh`)**.\n2. **Congestion Avoidance (AIMD - Additive Increase / Multiplicative Decrease)**:\n   - Once $cwnd \\ge ssthresh$, exponential growth ceases.\n   - **Additive Increase**: $cwnd$ increases linearly by $1\\text{ MSS}$ per RTT (probing cautiously for available bandwidth):\n     $$cwnd \\leftarrow cwnd + \\frac{\\text{MSS} \\times \\text{MSS}}{cwnd}$$\n   - **Multiplicative Decrease**: When packet loss is detected via 3 duplicate ACKs, the network is signaled as saturated:\n     $$ssthresh \\leftarrow \\frac{cwnd}{2}, \\quad cwnd \\leftarrow ssthresh$$\n3. **Modern Congestion Control: Loss-Based vs. Delay-Based / BBR**:\n   - **Cubic**: The Linux default since 2006. Uses a cubic polynomial function to rapidly ramp up after backoff, stabilizing near the prior saturation point.\n   - **BBR (Bottleneck Bandwidth and RTT)**: Developed by Google in 2016. Rejects loss-based triggers (which cause bufferbloat). Instead, BBR probes physical bottleneck bandwidth and minimum propagation delay, maximizing throughput without filling router buffers.",
            "citations": [
                "RFC 5681: TCP Congestion Control",
                "Congestion Avoidance and Control (Van Jacobson & Michael J. Karels, SIGCOMM 1988)",
                "BBR: Congestion-Based Congestion Control (Neal Cardwell, Yuchung Cheng, et al., ACM Queue 2016)"
            ]
        },
        {
            "section_id": "sec-l10-07",
            "heading": "Socket Programming in Python: TCP Stream & UDP Datagram",
            "body": "### The Socket API Architecture\n\nA **Socket** is an operating system kernel abstraction representing an endpoint of a bidirectional inter-process communication flow. In Python, socket programming is facilitated through the built-in `socket` module wrapping the standard BSD socket API.\n\n```\n      TCP SERVER LIFECYCLE                               TCP CLIENT LIFECYCLE\n    ┌──────────────────────┐                           ┌──────────────────────┐\n    │ socket(AF_INET, ...) │                           │ socket(AF_INET, ...) │\n    └──────────┬───────────┘                           └──────────┬───────────┘\n               ▼                                                  │\n    ┌──────────────────────┐                                      │\n    │ bind(('0.0.0.0', ...))│                                     │\n    └──────────┬───────────┘                                      │\n               ▼                                                  │\n    ┌──────────────────────┐                                      │\n    │     listen(backlog)  │                                      │\n    └──────────┬───────────┘                                      │\n               ▼                                                  ▼\n    ┌──────────────────────┐    3-Way Handshake (SYN)  ┌──────────────────────┐\n    │  accept() [Blocks]   │◄──────────────────────────┤ connect(('127...', ))│\n    └──────────┬───────────┘                           └──────────┬───────────┘\n               ▼                                                  ▼\n    ┌──────────────────────┐      Data Transfer        ┌──────────────────────┐\n    │  recv() / send()     │◄─────────────────────────►│    send() / recv()   │\n    └──────────┬───────────┘                           └──────────┬───────────┘\n               ▼                                                  ▼\n    ┌──────────────────────┐      4-Way Close (FIN)    ┌──────────────────────┐\n    │   conn.close()       │◄──────────────────────────┤     client.close()   │\n    └──────────────────────┘                           └──────────────────────┘\n```\n\n### Production-Grade Python TCP Echo Server & Client\n\n#### TCP Server (`tcp_server.py`)\n```python\nimport socket\n\nHOST = '0.0.0.0'  # Listen on all local interfaces\nPORT = 8080       # Non-privileged registered port\n\n# AF_INET = IPv4; SOCK_STREAM = TCP\nwith socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:\n    # Prevent 'Address already in use' socket errors upon quick restart:\n    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)\n    s.bind((HOST, PORT))\n    s.listen(5)  # Backlog queue: up to 5 unaccepted connections\n    print(f\"[*] TCP Server listening on {HOST}:{PORT}\")\n    \n    while True:\n        client_sock, client_addr = s.accept()  # Blocks until 3-way handshake succeeds\n        print(f\"[+] Accepted connection from {client_addr}\")\n        with client_sock:\n            while True:\n                data = client_sock.recv(1024)  # Read up to 1024 bytes\n                if not data:  # Empty byte string (b'') indicates client sent FIN\n                    print(f\"[-] Connection closed by {client_addr}\")\n                    break\n                print(f\"[<] Received: {data.decode()}\")\n                client_sock.sendall(data)  # Echo back all bytes\n```\n\n#### TCP Client (`tcp_client.py`)\n```python\nimport socket\n\nSERVER_IP = '127.0.0.1'\nSERVER_PORT = 8080\n\nwith socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:\n    client.connect((SERVER_IP, SERVER_PORT))  # Triggers 3-way handshake\n    message = \"Hello, Secure TCP Network!\"\n    client.sendall(message.encode('utf-8'))\n    \n    response = client.recv(1024)\n    print(f\"[>] Server Echo: {response.decode('utf-8')}\")\n# Exiting 'with' block calls client.close(), initiating 4-way FIN teardown\n```\n\n### Python UDP Datagram Server & Client\n\n#### UDP Server (`udp_server.py`)\n```python\nimport socket\n\nHOST = '0.0.0.0'\nPORT = 9090\n\n# SOCK_DGRAM = UDP\nwith socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:\n    s.bind((HOST, PORT))\n    print(f\"[*] UDP Server listening on {HOST}:{PORT}\")\n    while True:\n        data, client_addr = s.recvfrom(2048)  # Receives packet and client socket tuple\n        print(f\"[<] Received {len(data)} bytes from {client_addr}: {data.decode()}\")\n        s.sendto(b\"ACK: \" + data, client_addr)  # Direct datagram transmission\n```",
            "citations": [
                "Python Software Foundation: socket — Low-level networking interface Documentation",
                "Unix Network Programming: The Sockets Networking API (Stevens, Fenner, Rudoff)",
                "Linux man-pages: socket(2), bind(2), listen(2), accept(2)"
            ]
        }
    ],
    "quiz": {
        "quiz_id": "quiz-cn-t5-l10",
        "title": "Topic Mastery Assessment: Transport Layer, TCP Reliability & Socket Programming",
        "description": "25 comprehensive questions testing mastery of transport multiplexing, UDP headers, TCP handshakes/teardowns, sliding window flow control, congestion avoidance (AIMD), and Python socket implementations.",
        "questions": [
            {
                "id": "q-l10-01",
                "difficulty": "easy",
                "type": "single_choice",
                "question": "What is the primary role of the Transport Layer (Layer 4) in the network hierarchy?",
                "options": [
                    {"id": "opt-a", "text": "Framing physical bitstreams on optical fiber."},
                    {"id": "opt-b", "text": "Routing packets across intermediate autonomous systems via IP."},
                    {"id": "opt-c", "text": "Providing logical process-to-process communication between applications using port addressing."},
                    {"id": "opt-d", "text": "Resolving IP addresses to MAC addresses via ARP."}
                ],
                "correctOptionIds": ["opt-c"],
                "explanation": "The Transport Layer provides logical process-to-process communication, using port numbers to multiplex and demultiplex data among concurrent applications running on host systems."
            },
            {
                "id": "q-l10-02",
                "difficulty": "easy",
                "type": "single_choice",
                "question": "What is the size in bytes of a standard UDP header?",
                "options": [
                    {"id": "opt-a", "text": "4 bytes"},
                    {"id": "opt-b", "text": "8 bytes"},
                    {"id": "opt-c", "text": "20 bytes"},
                    {"id": "opt-d", "text": "64 bytes"}
                ],
                "correctOptionIds": ["opt-b"],
                "explanation": "A UDP header is strictly 8 bytes in length, composed of four 16-bit fields: Source Port, Destination Port, Length, and Checksum."
            },
            {
                "id": "q-l10-03",
                "difficulty": "easy",
                "type": "single_choice",
                "question": "What are the flags set in the three sequential packets of the standard TCP connection establishment handshake?",
                "options": [
                    {"id": "opt-a", "text": "1: SYN; 2: SYN-ACK; 3: ACK"},
                    {"id": "opt-b", "text": "1: ACK; 2: SYN; 3: FIN"},
                    {"id": "opt-c", "text": "1: RST; 2: SYN; 3: PSH"},
                    {"id": "opt-d", "text": "1: SYN; 2: ACK; 3: FIN"}
                ],
                "correctOptionIds": ["opt-a"],
                "explanation": "The standard TCP 3-way handshake sequence is: Client sends SYN -> Server responds with SYN-ACK -> Client replies with ACK."
            },
            {
                "id": "q-l10-04",
                "difficulty": "easy",
                "type": "single_choice",
                "question": "In Python's socket library, what constant specifies the TCP transport protocol?",
                "options": [
                    {"id": "opt-a", "text": "socket.SOCK_DGRAM"},
                    {"id": "opt-b", "text": "socket.SOCK_RAW"},
                    {"id": "opt-c", "text": "socket.SOCK_STREAM"},
                    {"id": "opt-d", "text": "socket.SOCK_PACKET"}
                ],
                "correctOptionIds": ["opt-c"],
                "explanation": "'socket.SOCK_STREAM' designates a sequenced, reliable, two-way, connection-based byte stream (TCP). 'socket.SOCK_DGRAM' designates UDP."
            },
            {
                "id": "q-l10-05",
                "difficulty": "easy",
                "type": "single_choice",
                "question": "What port range is reserved for Well-Known system ports (e.g., HTTP, SSH, DNS)?",
                "options": [
                    {"id": "opt-a", "text": "0 to 1023"},
                    {"id": "opt-b", "text": "1024 to 49151"},
                    {"id": "opt-c", "text": "49152 to 65535"},
                    {"id": "opt-d", "text": "1 to 255"}
                ],
                "correctOptionIds": ["opt-a"],
                "explanation": "Ports 0 through 1023 are Well-Known ports assigned by IANA for standard privileged network services."
            },
            {
                "id": "q-l10-06",
                "difficulty": "easy",
                "type": "multiple_choice",
                "question": "Which of the following guarantees are provided natively by TCP? (Select all that apply)",
                "options": [
                    {"id": "opt-a", "text": "Reliable data delivery via acknowledgments and retransmissions."},
                    {"id": "opt-b", "text": "In-order byte delivery to the application layer."},
                    {"id": "opt-c", "text": "Receiver flow control to prevent buffer exhaustion."},
                    {"id": "opt-d", "text": "Guaranteed maximum latency (bounded real-time delay)."}
                ],
                "correctOptionIds": ["opt-a", "opt-b", "opt-c"],
                "explanation": "TCP provides reliability, in-order delivery, flow control, and congestion control. It does NOT guarantee bounded latency or real-time delivery."
            },
            {
                "id": "q-l10-07",
                "difficulty": "easy",
                "type": "single_choice",
                "question": "What does a TCP Acknowledgment Number of 5001 signify to the sender?",
                "options": [
                    {"id": "opt-a", "text": "The receiver has received byte 5001 and is discarding all future bytes."},
                    {"id": "opt-b", "text": "The receiver has successfully received all bytes up to 5000 and is now expecting byte 5001."},
                    {"id": "opt-c", "text": "The receiver can accept 5001 more packets."},
                    {"id": "opt-d", "text": "The connection has timed out after 5001 milliseconds."}
                ],
                "correctOptionIds": ["opt-b"],
                "explanation": "TCP ACKs are cumulative: an ACK number of N informs the sender that all bytes up to N - 1 have been received in order, and byte N is the next byte expected."
            },
            {
                "id": "q-l10-08",
                "difficulty": "easy",
                "type": "single_choice",
                "question": "When a TCP client calls 'sock.recv(1024)' and receives an empty byte string (b''), what does this indicate?",
                "options": [
                    {"id": "opt-a", "text": "The network cable was unplugged."},
                    {"id": "opt-b", "text": "The remote peer gracefully closed the connection by sending a FIN segment."},
                    {"id": "opt-c", "text": "The buffer is full and the client must pause."},
                    {"id": "opt-d", "text": "A checksum error occurred in the last segment."}
                ],
                "correctOptionIds": ["opt-b"],
                "explanation": "In BSD and Python socket APIs, recv() returning 0 bytes (b'') is the standard indication that the remote peer performed an orderly shutdown and sent a FIN segment."
            },
            {
                "id": "q-l10-09",
                "difficulty": "easy",
                "type": "multiple_choice",
                "question": "Which of the following applications typically rely on UDP rather than TCP? (Select all that apply)",
                "options": [
                    {"id": "opt-a", "text": "Domain Name System (DNS) queries."},
                    {"id": "opt-b", "text": "Live VoIP audio and video conferencing."},
                    {"id": "opt-c", "text": "File Transfer Protocol (FTP) file uploads."},
                    {"id": "opt-d", "text": "Dynamic Host Configuration Protocol (DHCP)."}
                ],
                "correctOptionIds": ["opt-a", "opt-b", "opt-d"],
                "explanation": "DNS, VoIP, and DHCP use UDP for low latency, broadcast capability, and time-sensitive delivery. FTP requires 100% loss-free transmission and uses TCP."
            },
            {
                "id": "q-l10-10",
                "difficulty": "medium",
                "type": "single_choice",
                "question": "Why does TCP implement the TIME_WAIT state (lasting 2MSL) on the endpoint that initiates an active close?",
                "options": [
                    {"id": "opt-a", "text": "To allow the CPU to cool down after intense data processing."},
                    {"id": "opt-b", "text": "To ensure the final ACK arrives at the peer (retransmitting if lost) and to let wandering duplicate packets from this connection expire in the network."},
                    {"id": "opt-c", "text": "To negotiate new encryption keys for the next session."},
                    {"id": "opt-d", "text": "To keep the router's NAT table active indefinitely."}
                ],
                "correctOptionIds": ["opt-b"],
                "explanation": "TIME_WAIT lasts for 2 Maximum Segment Lifetimes (2MSL) to ensure that the active closer's final ACK reached the other end (handling retransmitted FINs if lost) and to guarantee all delayed packets expire before a new socket reuses the 5-tuple."
            },
            {
                "id": "q-l10-11",
                "difficulty": "medium",
                "type": "single_choice",
                "question": "What event triggers TCP Fast Retransmit without waiting for the Retransmission Timeout (RTO) to expire?",
                "options": [
                    {"id": "opt-a", "text": "Receiving an ICMP Source Quench message."},
                    {"id": "opt-b", "text": "Receiving 3 duplicate ACKs (4 identical ACKs total) for the same sequence number."},
                    {"id": "opt-c", "text": "The sender's cwnd exceeding the receiver's rwnd."},
                    {"id": "opt-d", "text": "A sudden increase in round-trip time."}
                ],
                "correctOptionIds": ["opt-b"],
                "explanation": "When a sender receives 3 duplicate ACKs for a missing segment, it assumes the packet was dropped while subsequent packets reached the receiver. It immediately retransmits the missing segment (Fast Retransmit) without waiting for the slow RTO timer."
            },
            {
                "id": "q-l10-12",
                "difficulty": "medium",
                "type": "single_choice",
                "question": "What is the primary difference between Flow Control and Congestion Control in TCP?",
                "options": [
                    {"id": "opt-a", "text": "Flow control is handled by routers; congestion control is handled by switches."},
                    {"id": "opt-b", "text": "Flow control prevents overwhelming the receiver's buffer (rwnd); congestion control prevents overwhelming the intermediate network links (cwnd)."},
                    {"id": "opt-c", "text": "Flow control uses UDP; congestion control uses TCP."},
                    {"id": "opt-d", "text": "Flow control controls packet size; congestion control controls port numbers."}
                ],
                "correctOptionIds": ["opt-b"],
                "explanation": "Flow control protects the destination receiver's buffer space via the advertised window (rwnd). Congestion control protects the intermediate network switches and routers from buffer collapse via the congestion window (cwnd)."
            },
            {
                "id": "q-l10-13",
                "difficulty": "medium",
                "type": "single_choice",
                "question": "During the TCP Slow Start phase, at what rate does the Congestion Window (cwnd) grow?",
                "options": [
                    {"id": "opt-a", "text": "Linearly by 1 MSS per RTT."},
                    {"id": "opt-b", "text": "Exponentially, effectively doubling cwnd each round-trip time (RTT)."},
                    {"id": "opt-c", "text": "Logarithmically based on packet size."},
                    {"id": "opt-d", "text": "It remains constant until packet loss occurs."}
                ],
                "correctOptionIds": ["opt-b"],
                "explanation": "In Slow Start, cwnd increases by 1 MSS for every received ACK. Because an entire window of segments is ACKed each RTT, cwnd doubles every RTT (exponential growth: 1 -> 2 -> 4 -> 8 -> 16)."
            },
            {
                "id": "q-l10-14",
                "difficulty": "medium",
                "type": "multiple_choice",
                "question": "Which of the following components constitute the 5-Tuple uniquely identifying an established TCP connection? (Select all that apply)",
                "options": [
                    {"id": "opt-a", "text": "Source IP Address."},
                    {"id": "opt-b", "text": "Destination IP Address."},
                    {"id": "opt-c", "text": "Source Port and Destination Port."},
                    {"id": "opt-d", "text": "Transport Protocol (e.g., TCP)."}
                ],
                "correctOptionIds": ["opt-a", "opt-b", "opt-c", "opt-d"],
                "explanation": "The 5-Tuple is (Protocol, Source IP, Source Port, Destination IP, Destination Port). All 5 fields are required to uniquely distinguish connections."
            },
            {
                "id": "q-l10-15",
                "difficulty": "medium",
                "type": "single_choice",
                "question": "Why does a TCP server set 's.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)' before binding to a port?",
                "options": [
                    {"id": "opt-a", "text": "To enable hardware decryption on the network interface card."},
                    {"id": "opt-b", "text": "To permit the server to bind to the port immediately even if previous sockets remain in TIME_WAIT state."},
                    {"id": "opt-c", "text": "To allow UDP traffic on the same TCP socket."},
                    {"id": "opt-d", "text": "To automatically forward packets across NAT gateways."}
                ],
                "correctOptionIds": ["opt-b"],
                "explanation": "SO_REUSEADDR allows a server to bind to a local port that is currently occupied by a connection in TIME_WAIT, preventing 'Address already in use' errors when restarting services."
            },
            {
                "id": "q-l10-16",
                "difficulty": "medium",
                "type": "single_choice",
                "question": "What is the purpose of a 'Zero Window Probe' in TCP flow control?",
                "options": [
                    {"id": "opt-a", "text": "To shut down an idle connection after 60 seconds."},
                    {"id": "opt-b", "text": "To test if an optical fiber link has zero attenuation."},
                    {"id": "opt-c", "text": "To periodically send a 1-byte segment when rwnd=0, forcing the receiver to reply with its current window size and preventing deadlock."},
                    {"id": "opt-d", "text": "To reset sequence numbers back to 0."}
                ],
                "correctOptionIds": ["opt-c"],
                "explanation": "When the receiver advertises rwnd=0, the sender must pause. If the subsequent window update segment (reopening the window) is lost, a deadlock would occur. Senders periodically transmit a 1-byte Zero Window Probe to elicit an ACK showing the current rwnd."
            },
            {
                "id": "q-l10-17",
                "difficulty": "medium",
                "type": "multiple_choice",
                "question": "Why must Initial Sequence Numbers (ISNs) in TCP be randomized rather than starting at zero? (Select all that apply)",
                "options": [
                    {"id": "opt-a", "text": "To prevent delayed duplicate packets from prior closed connections with the same 5-tuple from corrupting the new stream."},
                    {"id": "opt-b", "text": "To prevent sequence number prediction attacks by remote malicious attackers."},
                    {"id": "opt-c", "text": "To compress the TCP header from 20 bytes to 8 bytes."},
                    {"id": "opt-d", "text": "To bypass router access control lists."}
                ],
                "correctOptionIds": ["opt-a", "opt-b"],
                "explanation": "ISN randomization prevents ghost segments from past incarnations of a connection from being accepted as valid data, and stops attackers from forging TCP sessions via blind sequence number guessing."
            },
            {
                "id": "q-l10-18",
                "difficulty": "medium",
                "type": "single_choice",
                "question": "What is the formula for Additive Increase in TCP Congestion Avoidance (AIMD)?",
                "options": [
                    {"id": "opt-a", "text": "cwnd doubles every RTT (cwnd = cwnd * 2)."},
                    {"id": "opt-b", "text": "cwnd increases linearly by 1 MSS per RTT (cwnd = cwnd + 1 MSS)."},
                    {"id": "opt-c", "text": "cwnd resets to 1 MSS on every ACK."},
                    {"id": "opt-d", "text": "cwnd is clamped to rwnd / 2."}
                ],
                "correctOptionIds": ["opt-b"],
                "explanation": "In Congestion Avoidance, AIMD adds 1 MSS to cwnd for each RTT (additive increase), probing conservatively for available network capacity."
            },
            {
                "id": "q-l10-19",
                "difficulty": "hard",
                "type": "single_choice",
                "question": "A TCP connection has a current cwnd of 32 MSS and ssthresh of 16 MSS. A Retransmission Timeout (RTO) occurs due to severe packet loss. According to TCP Reno, what are the new values of ssthresh and cwnd?",
                "options": [
                    {"id": "opt-a", "text": "ssthresh = 16 MSS, cwnd = 16 MSS"},
                    {"id": "opt-b", "text": "ssthresh = 16 MSS, cwnd = 1 MSS"},
                    {"id": "opt-c", "text": "ssthresh = 8 MSS, cwnd = 8 MSS"},
                    {"id": "opt-d", "text": "ssthresh = 32 MSS, cwnd = 0 MSS"}
                ],
                "correctOptionIds": ["opt-b"],
                "explanation": "Upon an RTO timeout in TCP Reno: ssthresh is set to half of the current cwnd (32 / 2 = 16 MSS), and cwnd collapses all the way back to 1 MSS (entering Slow Start)."
            },
            {
                "id": "q-l10-20",
                "difficulty": "hard",
                "type": "single_choice",
                "question": "Host A sends a TCP SYN packet with Sequence Number 100,000 to Host B. Host B replies with a SYN-ACK with Sequence Number 200,000. What is the Acknowledgment Number in Host B's SYN-ACK, and what are the Sequence and Acknowledgment Numbers in Host A's subsequent ACK?",
                "options": [
                    {"id": "opt-a", "text": "B's ACK = 100,000; A's Seq = 100,000, A's ACK = 200,000"},
                    {"id": "opt-b", "text": "B's ACK = 100,001; A's Seq = 100,001, A's ACK = 200,001"},
                    {"id": "opt-c", "text": "B's ACK = 100,001; A's Seq = 100,000, A's ACK = 200,001"},
                    {"id": "opt-d", "text": "B's ACK = 200,001; A's Seq = 100,001, A's ACK = 100,001"}
                ],
                "correctOptionIds": ["opt-b"],
                "explanation": "A SYN packet consumes 1 sequence number byte. Host B acknowledges Host A's SYN by sending ACK = 100,000 + 1 = 100,001. Host A's subsequent packet has Seq = 100,001, and acknowledges Host B's SYN (Seq 200,000) by sending ACK = 200,000 + 1 = 200,001."
            },
            {
                "id": "q-l10-21",
                "difficulty": "hard",
                "type": "multiple_choice",
                "question": "Which of the following statements regarding TCP Window Scaling (RFC 7323) are TRUE? (Select all that apply)",
                "options": [
                    {"id": "opt-a", "text": "The standard 16-bit Window field in the TCP header limits the maximum unscaled window size to 65,535 bytes."},
                    {"id": "opt-b", "text": "Window Scaling defines a logarithmic scale factor negotiated exclusively in SYN segments during the 3-way handshake."},
                    {"id": "opt-c", "text": "Window Scaling allows the effective receive window to expand up to 1 Gigabyte (2^30 bytes), essential for high Bandwidth-Delay Product (BDP) links."},
                    {"id": "opt-d", "text": "Window Scaling can be enabled dynamically mid-connection on data segments."}
                ],
                "correctOptionIds": ["opt-a", "opt-b", "opt-c"],
                "explanation": "Without scaling, a 16-bit field caps window at 65,535 bytes. RFC 7323 negotiates a scale shift (0-14 bits) in SYN segments, enabling up to 2^30 bytes (~1 GB). It cannot be negotiated mid-stream."
            },
            {
                "id": "q-l10-22",
                "difficulty": "hard",
                "type": "single_choice",
                "question": "Why does Google's BBR (Bottleneck Bandwidth and RTT) congestion control algorithm outperform classical loss-based TCP algorithms like Reno and Cubic on modern high-speed networks?",
                "options": [
                    {"id": "opt-a", "text": "BBR replaces IP routing tables with neural networks."},
                    {"id": "opt-b", "text": "BBR models the physical network by measuring bottleneck bandwidth and minimum round-trip time, operating at optimal queue size without causing bufferbloat or misinterpreting non-congestive packet loss."},
                    {"id": "opt-c", "text": "BBR disables retransmissions completely."},
                    {"id": "opt-d", "text": "BBR forces all intermediate switches to prioritize its packets using DiffServ."}
                ],
                "correctOptionIds": ["opt-b"],
                "explanation": "Loss-based algorithms (Reno, Cubic) fill intermediate switch buffers until packets drop, causing bufferbloat and high latency. BBR continuously estimates the true bottleneck bandwidth and min-RTT, keeping buffers nearly empty and delivering high throughput with minimal delay."
            },
            {
                "id": "q-l10-23",
                "difficulty": "hard",
                "type": "multiple_choice",
                "question": "What issues occur if an operating system server application fails to call 'close()' on accepted sockets after client communication ends? (Select all that apply)",
                "options": [
                    {"id": "opt-a", "text": "Sockets accumulate in the 'CLOSE_WAIT' state on the server."},
                    {"id": "opt-b", "text": "The operating system eventually exhausts available file descriptors (EMFILE / ENFILE error)."},
                    {"id": "opt-c", "text": "Kernel socket buffers remain allocated in non-paged memory, creating a memory leak."},
                    {"id": "opt-d", "text": "The server's physical Ethernet MAC address is wiped from the network switch."}
                ],
                "correctOptionIds": ["opt-a", "opt-b", "opt-c"],
                "explanation": "Failing to close sockets leaves them in CLOSE_WAIT, leaking file descriptors and kernel socket buffer memory until the OS refuses new connections with 'Too many open files'."
            },
            {
                "id": "q-l10-24",
                "difficulty": "hard",
                "type": "single_choice",
                "question": "Suppose a link has a Round-Trip Time (RTT) of 100 ms and a bottleneck bandwidth of 1 Gbps. What is the Bandwidth-Delay Product (BDP) in Megabytes, and what is the consequence if the TCP Window Size is capped at the default 65,535 bytes?",
                "options": [
                    {"id": "opt-a", "text": "BDP = 100 MB; the link will achieve 1 Gbps throughput."},
                    {"id": "opt-b", "text": "BDP = 12.5 MB; throughput will be throttled to ~5.24 Mbps (65,535 * 8 / 0.1s), utilizing less than 1% of link capacity."},
                    {"id": "opt-c", "text": "BDP = 1.25 MB; throughput will be exactly 500 Mbps."},
                    {"id": "opt-d", "text": "BDP = 64 KB; the connection will immediately terminate."}
                ],
                "correctOptionIds": ["opt-b"],
                "explanation": "BDP = Bandwidth * RTT = (1,000,000,000 bps * 0.1 s) = 100,000,000 bits = 12.5 Megabytes. If window is capped at 65,535 bytes, max throughput = 65,535 bytes / 0.1 s = 655,350 bytes/s ≈ 5.24 Mbps. The sender spends >99% of its time idling waiting for ACKs!"
            },
            {
                "id": "q-l10-25",
                "difficulty": "hard",
                "type": "single_choice",
                "question": "In Python socket programming, what happens if a multi-client server implementation executes 'client_sock.recv(1024)' synchronously on the main thread inside an infinite 'while True' accept loop without using threads, processes, or an event loop (asyncio/select)?",
                "options": [
                    {"id": "opt-a", "text": "The server automatically spawns OS background threads for each connection."},
                    {"id": "opt-b", "text": "The entire server blocks on the first client; subsequent clients attempting to connect are queued in the listen backlog and cannot be served until the first client closes."},
                    {"id": "opt-c", "text": "The kernel sends a TCP RST segment to all other connecting clients."},
                    {"id": "opt-d", "text": "The socket switches automatically to UDP datagram mode."}
                ],
                "correctOptionIds": ["opt-b"],
                "explanation": "Synchronous single-threaded blocking sockets block the thread during recv(). If client 1 connects and stays idle, the server remains stuck in recv() and cannot loop back to accept() to service client 2, stalling all other incoming connections."
            }
        ]
    }
}
