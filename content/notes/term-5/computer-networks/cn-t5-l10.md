# Transport Layer, TCP Reliability & Socket Programming
**Term:** Term 5 | **Subject:** CN | **Note ID:** `cn-t5-l10`
**Last Updated:** 2026-10-14T00:00:00Z

## Abstract & Summary
An exhaustive, rigorous masterclass on the Transport Layer. Covers process-to-process addressing via 16-bit ports, contrasting lightweight UDP with the Transmission Control Protocol (TCP). Deconstructs the TCP 3-way handshake, 4-way teardown, TIME_WAIT state, cumulative acknowledgment mathematics, sliding window flow control, Reno/Tahoe congestion control algorithms, and socket programming implementations.

## Learning Objectives
- Explain the transport layer's role in process-to-process multiplexing and demultiplexing via port addressing.
- Compare TCP and UDP architectures, header structures, and design trade-offs across real-time and reliable applications.
- Trace the TCP 3-way connection establishment handshake, sequence number synchronization, and ISN randomization.
- Analyze TCP 4-way termination, the half-closed state, and the engineering necessity of the 2MSL TIME_WAIT state.
- Model TCP reliability mechanisms: cumulative ACKs, Round-Trip Time (RTT) estimation, Retransmission Timeouts (RTO), and Fast Retransmit via 3 duplicate ACKs.
- Distinguish between Receiver Flow Control (sliding window rwnd) and Network Congestion Control (cwnd, Slow Start, AIMD).
- Implement network client-server communication using low-level socket programming in Python (TCP stream and UDP datagram).

## Key Takeaways
- The Transport Layer provides logical process-to-process communication, abstracting the underlying network of routers into direct end-to-end socket connections.
- Ports are 16-bit integers (0 to 65535) divided into Well-Known (0-1023), Registered (1024-49151), and Ephemeral/Dynamic (49152-65535) ranges.
- UDP is an 8-byte, connectionless, unreliable datagram transport optimized for low latency, broadcast, or custom application-layer transport protocols (like QUIC).
- TCP guarantees reliable, ordered byte-stream delivery with flow control and congestion control using a 20-to-60 byte header with sequence numbers and control flags.
- The 3-way handshake synchronizes Initial Sequence Numbers (ISNs) to prevent stale ghost segments from corrupting new connections; the 4-way teardown gracefully closes bidirectional streams, concluding with a 2MSL TIME_WAIT state.
- Flow control prevents the sender from overwhelming the receiver's buffer via rwnd; Congestion control prevents the sender from saturating the network bottleneck link via cwnd (Slow Start exponential growth, AIMD additive increase / multiplicative decrease).
- Retransmissions are triggered either by an RTO timer expiration (severe delay) or Fast Retransmit upon receiving 3 duplicate ACKs (immediate loss recovery).

---

## Transport Layer Fundamentals: Process Addressing & Multiplexing
### The Need for Process-to-Process Communication

The Network Layer (Layer 3) is responsible for host-to-host delivery: an IP packet successfully reaches a physical machine with a destination IP address. However, a modern computer executes dozens of concurrent network processes (web browsers, SSH terminals, database engines, messaging daemons). The Network Layer has no mechanism to determine which application process should receive an incoming packet.

The **Transport Layer (Layer 4)** bridges this boundary by providing **process-to-process logical communication** through the abstraction of **Port Numbers** and **Sockets**:

```
                                  HOST A (Client)
         ┌──────────────┐         ┌──────────────┐         ┌──────────────┐
         │ Web Browser  │         │  SSH Client  │         │ Spotify App  │
         │ (Port 52341) │         │ (Port 48102) │         │ (Port 55190) │
         └──────┬───────┘         └──────┬───────┘         └──────┬───────┘
                │                        │                        │
                └────────────────────────┼────────────────────────┘
                                         ▼
                            TRANSPORT LAYER (Layer 4)
                          Multiplexing: Adds Port Headers
                                         ▼
                             NETWORK LAYER (Layer 3)
                           Encapsulates into IP Packets
                                         ▼
                                  INTERNET CORE
                                         ▼
                             NETWORK LAYER (Layer 3)
                                         ▼
                            TRANSPORT LAYER (Layer 4)
                        Demultiplexing: Reads Dst Port
                                         ▼
                            ┌────────────────────────┐
                            │ Web Server (Port 443)  │
                            └────────────────────────┘
                                  HOST B (Server)
```

### The Socket Tuple
A network endpoint is defined as a **Socket Address** (`IP Address : Port Number`). An active, established TCP connection across the Internet is uniquely identified by an immutable **5-Tuple**:
$$\text{Connection Identifier} = \big( \text{Protocol}, \text{Source IP}, \text{Source Port}, \text{Destination IP}, \text{Destination Port} \big)$$

Because of this 5-tuple demultiplexing rule, a web server listening on port `443` (`0.0.0.0:443`) can maintain hundreds of thousands of concurrent active TCP connections simultaneously, as long as each client has a distinct combination of Source IP and Source Port.

### Port Number Taxonomy (RFC 6335)
Ports are 16-bit unsigned integers spanning from $0$ to $65,535$ ($2^{16}$ possible ports), categorized into three standardized tiers:

1. **Well-Known Ports ($0 - 1,023$)**:
   - Assigned by the Internet Assigned Numbers Authority (IANA) for core system protocols.
   - On UNIX/Linux systems, binding to a well-known port requires root privileges (`sudo`).
   - Examples: `20/21` (FTP), `22` (SSH), `25` (SMTP), `53` (DNS), `80` (HTTP), `443` (HTTPS), `123` (NTP).
2. **Registered Ports ($1,024 - 49,151$)**:
   - Registered by software vendors for specific application services; non-root processes can bind to them.
   - Examples: `3306` (MySQL), `5432` (PostgreSQL), `6379` (Redis), `8080` (HTTP alternate), `27017` (MongoDB).
3. **Dynamic / Ephemeral / Private Ports ($49,152 - 65,535$)**:
   - Automatically assigned by the host operating system kernel to client sockets upon initiating outbound connections.

**Citations & References:**
- RFC 6335: Internet Assigned Numbers Authority (IANA) Procedures for the Management of the Service Name and Transport Protocol Port Number Registry
- Computer Networks: A Systems Approach, Chapter 5 (End-to-End Protocols)
- Computer Networking: A Top-Down Approach (Kurose & Ross), Chapter 3 (Transport Layer)

---

## UDP Architecture: Lightweight, Connectionless Datagrams
### The Minimalist Transport Protocol

The **User Datagram Protocol (UDP)**, defined in RFC 768 by David P. Reed in 1980, is the simplest possible transport layer protocol. UDP adds almost nothing to IP other than port-based process multiplexing and basic error detection.

#### The 8-Byte UDP Header Anatomy
While TCP requires a minimum of 20 bytes (and up to 60 bytes with options), the UDP header is strictly **8 bytes** in size:

```
 0                   15 16                  31
┌──────────────────────┬──────────────────────┐
│     Source Port      │   Destination Port   │   (4 Bytes)
├──────────────────────┼──────────────────────┤
│    Length (bytes)    │       Checksum       │   (4 Bytes)
└──────────────────────┴──────────────────────┘
│               Data Payload ...              │
```

1. **Source Port (16 bits)**: Port of the sending process (optional; set to 0 if no reply is expected).
2. **Destination Port (16 bits)**: Port of the destination process.
3. **Length (16 bits)**: Total length in bytes of the UDP header plus UDP payload (minimum value is 8).
4. **Checksum (16 bits)**: Error-detection checksum covering the UDP header, payload, and an IPv4/IPv6 **pseudo-header** (containing source/destination IPs to detect misrouted datagrams). In IPv4, checksum is optional (set to 0 to disable); in IPv6, checksum is **strictly mandatory**.

### Core Properties of UDP
- **Connectionless**: No handshake or teardown. Senders transmit immediately without negotiating state.
- **Unreliable Delivery**: Datagrams may be lost, reordered, or duplicated in transit without warning. UDP provides zero ACKs and zero retransmissions.
- **Message-Oriented (Preserves Framing)**: UDP preserves application message boundaries. If an application calls `sendto()` with 500 bytes, the receiver's `recvfrom()` returns exactly that 500-byte datagram in a single read, unlike TCP's continuous byte stream.
- **Zero Congestion Control**: Senders can blast datagrams at the physical link rate regardless of network congestion.

### Production Use Cases for UDP

| Domain | Why UDP is Required | Engineering Rationale |
| :--- | :--- | :--- |
| **DNS (Port 53)** | Query/Response speed | Single request-reply cycle; a 3-way TCP handshake would double latency from 1 RTT to 2 RTT. |
| **DHCP (Ports 67/68)** | Broadcast capability | Clients have no IP yet; TCP cannot broadcast across a LAN segment. |
| **Real-Time Audio / Video (VoIP / WebRTC)**| Timeliness over perfection | In a live voice call, an audio packet arriving 300 ms late due to TCP retransmission is useless noise. Skipping lost packets is preferable to freezing playback. |
| **Multiplayer Online Gaming** | Low-latency state sync | Player positions update at 60 Hz. Old positional updates are superseded by newer ones; stalling for retransmission creates unbearable input lag. |
| **HTTP/3 & QUIC** | Userspace transport | Builds modern multiplexing, encryption, and reliability on top of UDP to bypass operating system kernel update delays and middlebox ossification. |

**Citations & References:**
- RFC 768: User Datagram Protocol (David P. Reed)
- RFC 5405: Unicast UDP Usage Guidelines for Application Designers
- Computer Networks: A Systems Approach, Chapter 5.1 (Simple Demultiplexor - UDP)

---

## TCP Architecture: Reliable, Connection-Oriented Byte Streams
### The Transmission Control Protocol (TCP)

Defined in RFC 793, TCP transforms an inherently unreliable, best-effort packet network (IP) into a rock-solid, fully reliable, ordered, bi-directional **virtual byte stream**.

```
 0                   15 16                  31
┌──────────────────────┬──────────────────────┐
│     Source Port      │   Destination Port   │
├──────────────────────┴──────────────────────┤
│               Sequence Number               │
├─────────────────────────────────────────────┤
│            Acknowledgment Number            │
├──────┬─────────┬─────┬──────────────────────┤
│Offset│ Reserved│Flags│     Window Size      │
├──────┴─────────┴─────┼──────────────────────┤
│       Checksum       │    Urgent Pointer    │
├──────────────────────┴──────────────────────┤
│          Options (0 to 40 bytes) ...        │
└─────────────────────────────────────────────┘
│               Data Payload ...              │
```

#### Deep Header Field Analysis
1. **Sequence Number (32 bits)**:
   - Identifies the byte offset of the first data byte in this segment within the overall transmitted stream.
   - If the `SYN` flag is set ($1$), this field represents the **Initial Sequence Number (ISN)**, and the first actual data byte begins at $\text{ISN} + 1$.
2. **Acknowledgment Number (32 bits)**:
   - Valid only when the `ACK` flag is set.
   - Contains the **next sequence number the receiver is expecting to receive**. Acknowledgment is **cumulative**: an ACK of $N$ confirms that all bytes from $0$ up to $N - 1$ have been successfully received.
3. **Data Offset / Header Length (4 bits)**:
   - Specifies the size of the TCP header in 32-bit (4-byte) words. Minimum value is $5$ ($5 \times 4 = 20$ bytes); maximum is $15$ ($15 \times 4 = 60$ bytes).
4. **Control Flags (6 to 9 bits)**:
   - **SYN (Synchronize)**: Initiates a connection; synchronizes Initial Sequence Numbers.
   - **ACK (Acknowledgment)**: Signifies that the Acknowledgment Number field is valid.
   - **FIN (Finish)**: Sender has completed transmitting data; initiates connection teardown.
   - **RST (Reset)**: Aborts an invalid connection, rejects connection attempts, or recovers from fatal errors.
   - **PSH (Push)**: Instructs receiver to push buffered data immediately to the application layer.
   - **URG (Urgent)**: Indicates that the Urgent Pointer field is valid (legacy out-of-band data).
5. **Window Size (`rwnd`, 16 bits)**:
   - Advertises the receiver's currently available receive buffer capacity in bytes for flow control.
   - Allows a maximum window of $65,535$ bytes, extendable up to $1$ gigabyte using the **Window Scale Option** (RFC 7323).
6. **Checksum (16 bits)**:
   - Mandatory error check computed over the TCP header, payload, and IP pseudo-header.

**Citations & References:**
- RFC 793: Transmission Control Protocol (DARPA Internet Program Protocol Specification)
- RFC 7323: TCP Extensions for High Performance (Window Scale, Timestamps)
- TCP/IP Illustrated, Volume 1: The Protocols (W. Richard Stevens), Chapter 17

---

## TCP Connection Lifecycle: The 3-Way Handshake & 4-Way Teardown
### The 3-Way Handshake (Connection Setup)

Before a single byte of application data can be exchanged, the client and server must agree on socket state, synchronize Initial Sequence Numbers (ISNs), and negotiate options (e.g., Maximum Segment Size - MSS, Window Scaling, Selective Acknowledgment - SACK):

```
   Client (State)                                                   Server (State: LISTEN)
         │                                                                    │
         │ ─── Step 1: SYN (seq = x) ───────────────────────────────────────► │
   SYN_SENT                                                                SYN_RCVD
         │                                                                    │
         │ ◄── Step 2: SYN-ACK (seq = y, ack = x + 1) ────────────────────── │
  ESTABLISHED                                                                 │
         │                                                                    │
         │ ─── Step 3: ACK (seq = x + 1, ack = y + 1) [Piggyback Data OK] ──► │
         │                                                                 ESTABLISHED
```

1. **Step 1: Client sends `SYN`**
   - Flags: `SYN=1, ACK=0`
   - Header: `Sequence Number = x` (random client ISN). Note: SYN consumes $1$ phantom sequence number even though it carries zero payload bytes!
   - Client enters `SYN_SENT` state.
2. **Step 2: Server replies `SYN-ACK`**
   - Flags: `SYN=1, ACK=1`
   - Header: `Sequence Number = y` (random server ISN), `Acknowledgment Number = x + 1` (confirms receipt of client's SYN).
   - Server enters `SYN_RCVD` state.
3. **Step 3: Client sends `ACK`**
   - Flags: `ACK=1, SYN=0`
   - Header: `Sequence Number = x + 1`, `Acknowledgment Number = y + 1` (confirms server's SYN).
   - Client enters `ESTABLISHED`. Upon receiving this segment, the server enters `ESTABLISHED`.

#### Why Random Initial Sequence Numbers (ISNs)?
ISNs are generated pseudo-randomly (RFC 6528) rather than starting at $0$ for two critical reasons:
1. **Ghost Packet Immunity**: If a previous TCP connection between the same pair of ports terminated abruptly, delayed packets drifting through the Internet could arrive and be injected into a newly opened connection if sequence numbers overlapped.
2. **TCP Sequence Prediction Attacks (Kevin Mitnick Attack)**: If ISNs were predictable (e.g., incremented by a constant counter), a blind remote attacker could spoof trusted IP addresses and inject malicious data into TCP sessions.

---

### The 4-Way Teardown (Connection Termination)
Because TCP connections are full-duplex (two independent data streams in opposite directions), each direction must be terminated independently:

```
   Client (ESTABLISHED)                                            Server (ESTABLISHED)
         │                                                                    │
         │ ─── Step 1: FIN (seq = u) ───────────────────────────────────────► │
    FIN_WAIT_1                                                             CLOSE_WAIT
         │                                                                    │
         │ ◄── Step 2: ACK (ack = u + 1) ─────────────────────────────────── │
    FIN_WAIT_2                                                                │
         │                                                       (Server finishes sending)
         │                                                                    │
         │ ◄── Step 3: FIN (seq = v) ─────────────────────────────────────── │
     TIME_WAIT                                                             LAST_ACK
         │                                                                    │
         │ ─── Step 4: ACK (ack = v + 1) ───────────────────────────────────► │
         │                                                                  CLOSED
    [Waits 2MSL]
         ▼
       CLOSED
```

#### The Engineering Rationale for TIME_WAIT (2MSL)
After transmitting the final `ACK` (Step 4), the active closer does not immediately transition to `CLOSED`. Instead, it enters the **`TIME_WAIT`** state for a duration of **$2 \times \text{MSL}$ (Maximum Segment Lifetime)**, typically $60$ seconds (or $120$ seconds in standard RFC 793):
1. **Ensure Graceful Final ACK Delivery**: If the client's final `ACK` is lost in transit, the server will time out and retransmit its `FIN`. If the client were already `CLOSED`, it would respond with an abrupt `RST`, causing the server to believe the connection terminated abnormally with data loss.
2. **Draining Delayed Segments**: Ensures that all wandering, delayed duplicate packets belonging to this connection die in the network before their sequence numbers could contaminate a subsequent incarnation of the same 5-tuple.

**Citations & References:**
- RFC 793: Transmission Control Protocol, Section 3.4 (Establishing a Connection)
- RFC 6528: Defending Against Sequence Number Attacks
- UNIX Network Programming, Volume 1 (W. Richard Stevens), Chapter 2

---

## TCP Reliability & Flow Control: Sliding Windows and Fast Retransmit
### Cumulative Acknowledgments & Retransmission Timers

TCP views data as a continuous stream of numbered bytes. The receiver acknowledges bytes **cumulatively**: `ACK = N` means *"I have successfully received and assembled all bytes up to $N - 1$. I am expecting byte $N$."*

```
 Sender transmits:    [Bytes 1–1000]     [Bytes 1001–2000]    [Bytes 2001–3000 (LOST!)]    [Bytes 3001–4000]
 Receiver replies:     ACK 1001           ACK 2001                                          ACK 2001 (Dup 1!)
                                                              [Bytes 4001–5000] ──►         ACK 2001 (Dup 2!)
                                                              [Bytes 5001–6000] ──►         ACK 2001 (Dup 3!)
                                                                                            ▲
                                                              3 DUPLICATE ACKs RECEIVED! ───┘
                                                              Sender immediately fires FAST RETRANSMIT:
                                                              Retransmits [Bytes 2001–3000] WITHOUT waiting for RTO!
```

#### Loss Recovery Mechanisms
1. **Retransmission Timeout (RTO)**:
   - For every segment sent, TCP runs an RTO timer calculated from exponential weighted moving averages of measured RTT (Jacobson's algorithm, RFC 6298):
     $$\text{SRTT} = (1 - \alpha) \cdot \text{SRTT} + \alpha \cdot \text{RTT}$$   $$\text{RTTVAR} = (1 - \beta) \cdot \text{RTTVAR} + \beta \cdot |\text{SRTT} - \text{RTT}|$$   $$\text{RTO} = \text{SRTT} + 4 \cdot \text{RTTVAR}$$
   - If the timer expires before an ACK arrives, the sender retransmits the oldest unacknowledged segment. RTO expiration is an emergency fallback: it forces the sender back to Slow Start ($cwnd = 1\text{ MSS}$), crushing throughput.
2. **Fast Retransmit (3 Duplicate ACKs)**:
   - When an out-of-order segment arrives at the receiver (e.g., segment 3 was lost, but segments 4, 5, and 6 arrived), the receiver cannot ACK beyond 2000. It repeatedly transmits duplicate ACKs with `ACK = 2001`.
   - When the sender receives **3 duplicate ACKs** (total of 4 identical ACKs for byte 2001), it infers that packet 2001 was dropped while subsequent packets reached the receiver.
   - Rather than waiting for the sluggish RTO timer to expire, the sender immediately retransmits the missing segment (**Fast Retransmit**) and enters **Fast Recovery**.

### Receiver Flow Control: The Sliding Window (`rwnd`)
Flow control ensures that a fast sending sender does not overflow the memory buffer of a slow receiving host.

$$\text{Effective Window} = \min(rwnd, cwnd)$$

- The receiver advertises its available buffer space in every TCP segment header: `Window Size = rwnd`.
- The sender maintains three logical pointer offsets:
  - Bytes Sent and Acknowledged
  - Bytes Sent but In-Flight (unacknowledged)
  - Bytes Allowed to Send Immediately without waiting for ACKs
- **Zero Window Probe**: If the receiver's application is blocked and the receive buffer fills completely, the receiver sends `rwnd = 0`. The sender stops transmitting data immediately. To prevent a deadlock if the subsequent window update is lost, the sender periodically sends 1-byte **Zero Window Probes** to force the receiver to re-advertise its current buffer state.

**Citations & References:**
- RFC 6298: Computing TCP's Retransmission Timer
- RFC 5681: TCP Congestion Control (Fast Retransmit and Fast Recovery)
- Computer Networks: A Systems Approach, Chapter 5.2 (Reliable Transmission)

---

## TCP Congestion Control: Slow Start, AIMD & Modern Algorithms
### The Distinction Between Flow Control and Congestion Control

- **Flow Control (`rwnd`)**: Protects the **destination host**'s internal memory buffer.
- **Congestion Control (`cwnd`)**: Protects the **shared intermediate network** (routers and bottleneck switches) from collapsing under buffer overflow.

```
                                        TCP RENO LIFECYCLE

     cwnd (MSS)
         ▲
         │                                         Timeout (RTO) ──► cwnd resets to 1
      32 │                              /\                           │
         │                             /  \  ◄── 3 Dup ACKs          │
      16 │             ssthresh ──►   /    \     (Fast Recovery)     │
         │                           /      \                        │
       8 │                          /        \                       │
         │                         /          \                      │
       4 │                        /            \                     │
       2 │        /\             /              \                    │
       1 │  ─────/  ────────────/                ────────────────────/──────► Time
             Slow Start   Congestion Avoidance    Congestion Avoidance  Slow Start
            (Exponential)     (Linear AIMD)           (Linear AIMD)    (Exponential)
```

### The Classical Phases of TCP Congestion Control (RFC 5681)

1. **Slow Start**:
   - Starts conservatively with $cwnd = 1$ to $10\text{ MSS}$ (Initial Window).
   - For every ACK received, $cwnd$ increments by $1\text{ MSS}$. Consequently, for every round trip time (RTT), $cwnd$ **doubles** exponentially ($1 \to 2 \to 4 \to 8 \to 16$).
   - Continues until $cwnd$ reaches the **Slow Start Threshold (`ssthresh`)**.
2. **Congestion Avoidance (AIMD - Additive Increase / Multiplicative Decrease)**:
   - Once $cwnd \ge ssthresh$, exponential growth ceases.
   - **Additive Increase**: $cwnd$ increases linearly by $1\text{ MSS}$ per RTT (probing cautiously for available bandwidth):
     $$cwnd \leftarrow cwnd + \frac{\text{MSS} \times \text{MSS}}{cwnd}$$
   - **Multiplicative Decrease**: When packet loss is detected via 3 duplicate ACKs, the network is signaled as saturated:
     $$ssthresh \leftarrow \frac{cwnd}{2}, \quad cwnd \leftarrow ssthresh$$
3. **Modern Congestion Control: Loss-Based vs. Delay-Based / BBR**:
   - **Cubic**: The Linux default since 2006. Uses a cubic polynomial function to rapidly ramp up after backoff, stabilizing near the prior saturation point.
   - **BBR (Bottleneck Bandwidth and RTT)**: Developed by Google in 2016. Rejects loss-based triggers (which cause bufferbloat). Instead, BBR probes physical bottleneck bandwidth and minimum propagation delay, maximizing throughput without filling router buffers.

**Citations & References:**
- RFC 5681: TCP Congestion Control
- Congestion Avoidance and Control (Van Jacobson & Michael J. Karels, SIGCOMM 1988)
- BBR: Congestion-Based Congestion Control (Neal Cardwell, Yuchung Cheng, et al., ACM Queue 2016)

---

## Socket Programming in Python: TCP Stream & UDP Datagram
### The Socket API Architecture

A **Socket** is an operating system kernel abstraction representing an endpoint of a bidirectional inter-process communication flow. In Python, socket programming is facilitated through the built-in `socket` module wrapping the standard BSD socket API.

```
      TCP SERVER LIFECYCLE                               TCP CLIENT LIFECYCLE
    ┌──────────────────────┐                           ┌──────────────────────┐
    │ socket(AF_INET, ...) │                           │ socket(AF_INET, ...) │
    └──────────┬───────────┘                           └──────────┬───────────┘
               ▼                                                  │
    ┌──────────────────────┐                                      │
    │ bind(('0.0.0.0', ...))│                                     │
    └──────────┬───────────┘                                      │
               ▼                                                  │
    ┌──────────────────────┐                                      │
    │     listen(backlog)  │                                      │
    └──────────┬───────────┘                                      │
               ▼                                                  ▼
    ┌──────────────────────┐    3-Way Handshake (SYN)  ┌──────────────────────┐
    │  accept() [Blocks]   │◄──────────────────────────┤ connect(('127...', ))│
    └──────────┬───────────┘                           └──────────┬───────────┘
               ▼                                                  ▼
    ┌──────────────────────┐      Data Transfer        ┌──────────────────────┐
    │  recv() / send()     │◄─────────────────────────►│    send() / recv()   │
    └──────────┬───────────┘                           └──────────┬───────────┘
               ▼                                                  ▼
    ┌──────────────────────┐      4-Way Close (FIN)    ┌──────────────────────┐
    │   conn.close()       │◄──────────────────────────┤     client.close()   │
    └──────────────────────┘                           └──────────────────────┘
```

### Production-Grade Python TCP Echo Server & Client

#### TCP Server (`tcp_server.py`)
```python
import socket

HOST = '0.0.0.0'  # Listen on all local interfaces
PORT = 8080       # Non-privileged registered port

# AF_INET = IPv4; SOCK_STREAM = TCP
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # Prevent 'Address already in use' socket errors upon quick restart:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(5)  # Backlog queue: up to 5 unaccepted connections
    print(f"[*] TCP Server listening on {HOST}:{PORT}")
    
    while True:
        client_sock, client_addr = s.accept()  # Blocks until 3-way handshake succeeds
        print(f"[+] Accepted connection from {client_addr}")
        with client_sock:
            while True:
                data = client_sock.recv(1024)  # Read up to 1024 bytes
                if not data:  # Empty byte string (b'') indicates client sent FIN
                    print(f"[-] Connection closed by {client_addr}")
                    break
                print(f"[<] Received: {data.decode()}")
                client_sock.sendall(data)  # Echo back all bytes
```

#### TCP Client (`tcp_client.py`)
```python
import socket

SERVER_IP = '127.0.0.1'
SERVER_PORT = 8080

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
    client.connect((SERVER_IP, SERVER_PORT))  # Triggers 3-way handshake
    message = "Hello, Secure TCP Network!"
    client.sendall(message.encode('utf-8'))
    
    response = client.recv(1024)
    print(f"[>] Server Echo: {response.decode('utf-8')}")
# Exiting 'with' block calls client.close(), initiating 4-way FIN teardown
```

### Python UDP Datagram Server & Client

#### UDP Server (`udp_server.py`)
```python
import socket

HOST = '0.0.0.0'
PORT = 9090

# SOCK_DGRAM = UDP
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.bind((HOST, PORT))
    print(f"[*] UDP Server listening on {HOST}:{PORT}")
    while True:
        data, client_addr = s.recvfrom(2048)  # Receives packet and client socket tuple
        print(f"[<] Received {len(data)} bytes from {client_addr}: {data.decode()}")
        s.sendto(b"ACK: " + data, client_addr)  # Direct datagram transmission
```

**Citations & References:**
- Python Software Foundation: socket — Low-level networking interface Documentation
- Unix Network Programming: The Sockets Networking API (Stevens, Fenner, Rudoff)
- Linux man-pages: socket(2), bind(2), listen(2), accept(2)

---
