# Network Diagnostics, Packet Sniffing & 7-Layer Troubleshooting
**Term:** Term 5 | **Subject:** CN | **Note ID:** `cn-t5-l12`
**Last Updated:** 2026-10-14T00:00:00Z

## Abstract & Summary
An exhaustive, rigorous masterclass on enterprise network diagnostics and full-stack troubleshooting. Explores bottom-up OSI problem isolation, ICMP mechanics in ping and traceroute, advanced DNS debugging with dig, kernel socket inspection via ss, line-rate packet capture with tcpdump and Berkeley Packet Filters, and deep protocol analysis in Wireshark.

## Learning Objectives
- Apply the systematic bottom-up OSI troubleshooting methodology from physical link to application layer.
- Dissect ICMP mechanics in ping: Echo Request/Reply, Round-Trip Time (RTT), jitter (mdev), and Path MTU testing.
- Analyze traceroute operation: intentional TTL expiration (ICMP Type 11), latency spikes, and UDP vs ICMP vs TCP probe modes.
- Execute comprehensive DNS troubleshooting using dig: query sections, reverse lookups, and recursive delegation tracing via dig +trace.
- Inspect active kernel socket tables and TCP connection states using ss: LISTEN, SYN_SENT, CLOSE_WAIT, and TIME_WAIT.
- Capture and filter live network traffic using tcpdump with Berkeley Packet Filters (BPF) and analyze TCP flag combinations.
- Analyze packet captures in Wireshark: display filters, TCP stream reassembly, and diagnosing real-world outage signatures.

## Key Takeaways
- Systematic troubleshooting follows a bottom-up flow: Physical (link up) -> Data Link (MAC/ARP) -> Network (IP/gateway ping) -> Transport (port open/listening) -> Application (service response).
- ping uses ICMP Echo Request (Type 8) and Echo Reply (Type 0); TTL in the reply reveals the number of intermediate router hops traversed.
- traceroute exploits ICMP Time Exceeded (Type 11) by sending probes with incrementally increasing TTL (1, 2, 3...); * * * indicates routers that filter ICMP probes but still forward data traffic.
- dig is the preferred DNS diagnostic tool; dig +trace bypasses resolver caches to perform raw iterative resolution from Root to Authoritative nameservers.
- ss is the modern Linux replacement for netstat; binding to 127.0.0.1 restricts access to local processes only, while binding to 0.0.0.0 exposes the service across all network interfaces.
- Many sockets in CLOSE_WAIT indicate an application-level bug failing to invoke close(); high Recv-Q values indicate that the application is CPU-starved or blocked.
- tcpdump captures raw packets using kernel Berkeley Packet Filters (BPF); Wireshark provides deep protocol tree dissection, TCP stream reassembly, and retransmission anomaly graphs.

---

## Systematic 7-Layer Troubleshooting Methodology
### The Engineering Approach to Problem Isolation

When a service outage or connectivity degradation occurs, untrained engineers guess blindly—randomly rebooting routers or modifying application code. Professional network engineers apply a deterministic, systematic troubleshooting methodology grounded in the **OSI / TCP/IP Layer Stack**.

```
 ┌────────────────────────────────────────────────────────────────────────┐
 │               THE SYSTEMATIC BOTTOM-UP TROUBLESHOOTING LADDER          │
 ├────────────────────────┬───────────────────────────────────────────────┤
 │ Layer 7: Application   │ curl, HTTP status, application logs, TLS certs│
 │ Layer 4: Transport     │ ss -tulpn, nc, telnet, listening sockets, FW  │
 │ Layer 3: Network       │ ping 8.8.8.8, ping gateway, ip route, traceroute│
 │ Layer 2: Data Link     │ ip link, ip neigh show, ARP resolution        │
 │ Layer 1: Physical      │ Ethernet link lights, Wi-Fi association, fiber│
 └────────────────────────┴───────────────────────────────────────────────┘
```

### The 6-Step Rapid Diagnostic Checklist
When diagnosing a network failure on any server or host, execute this rapid triage checklist in strict chronological order:

1. **Step 1: Check Physical Link & IP (`ip addr`)**
   - Is the interface in `UP` state with carrier detected?
   - Does the interface have a valid IPv4 address assigned via DHCP or static configuration?
2. **Step 2: Check Local LAN & Gateway (`ping <Default Gateway>`)**
   - Can the host communicate with its default gateway (e.g., `192.168.1.1`)?
   - If this fails: Issue is strictly local (bad Wi-Fi, unplugged cable, failed switch port, or ARP failure).
3. **Step 3: Check WAN Routing (`ping 8.8.8.8`)**
   - Can the host reach an external public IP on the Internet?
   - If Step 2 succeeds but Step 3 fails: Local LAN is functional, but WAN connection, ISP link, or NAT gateway is down.
4. **Step 4: Check Domain Name Resolution (`dig google.com` or `ping google.com`)**
   - Can the host translate hostnames to IP addresses?
   - If Step 3 succeeds (can ping `8.8.8.8`) but Step 4 fails (cannot resolve `google.com`): The Internet connection is fully functional, but DNS configuration (`/etc/resolv.conf`) is broken.
5. **Step 5: Check Local Service Port (`ss -tulpn | grep :<port>`)**
   - Is the target application process actively listening on the expected port?
   - Is it bound to `0.0.0.0` (all interfaces) or erroneously bound to `127.0.0.1` (localhost only)?
6. **Step 6: Check End-to-End Application Response (`curl -Iv https://<target>`)**
   - Does the web server complete the TCP handshake, negotiate TLS, and return a valid HTTP 200 response?

**Citations & References:**
- RFC 1812: Requirements for IPv4 Routers, Section 8 (Operations and Maintenance)
- Network Warrior (Gary A. Donahue), O'Reilly Media, Chapter 1 (Network Troubleshooting)
- The Practice of System and Network Administration (Limoncelli, Chalup, Hogan)

---

## ICMP Architecture & Ping Diagnostics
### The Internet Control Message Protocol (ICMP)

Defined in RFC 792, **ICMP** is an integral companion protocol to IPv4 (and ICMPv6 in RFC 4443). Operating logically alongside Layer 3, ICMP generates error reports and operational diagnostics regarding packet processing failures.

### How `ping` Works: Echo Request and Echo Reply
Written by Mike Muuss in 1983 (named after submarine sonar acoustics), `ping` transmits **ICMP Type 8 (Echo Request)** datagrams and listens for returning **ICMP Type 0 (Echo Reply)** datagrams.

```
 Client (192.168.1.5)                                             Target Server (142.250.195.46)
        │                                                                       │
        │ ─── ICMP Type 8, Code 0 (Echo Request, seq=1, timestamp=t0) ────────► │
        │                                                                       │
        │ ◄── ICMP Type 0, Code 0 (Echo Reply, seq=1, timestamp=t0) ─────────── │
        │                                                                       │
   [Calculates RTT = t1 - t0]
```

### Dissecting `ping` Output Statistics

```bash
$ ping -c 4 142.250.195.46
64 bytes from 142.250.195.46: icmp_seq=1 ttl=115 time=6.82 ms
64 bytes from 142.250.195.46: icmp_seq=2 ttl=115 time=7.10 ms
64 bytes from 142.250.195.46: icmp_seq=3 ttl=115 time=6.45 ms
64 bytes from 142.250.195.46: icmp_seq=4 ttl=115 time=6.79 ms

--- 142.250.195.46 ping statistics ---
4 packets transmitted, 4 received, 0% packet loss, time 3004ms
rtt min/avg/max/mdev = 6.45/6.79/7.10/0.265 ms
```

1. **`ttl=115` (Estimating Router Hop Count)**:
   - Standard server OS starting TTLs: Linux = $64$, Windows = $128$, Cisco IOS = $255$.
   - Because the received TTL is $115$, the responding server is almost certainly Windows (initial $\text{TTL} = 128$).
   - Traversed router hops: $\text{Hops} = 128 - 115 = \mathbf{13\text{ intermediate router hops}}$.
2. **`mdev` (Mean Deviation / Jitter)**:
   - Represents the variance in round-trip times. A low `mdev` ($0.265\text{ ms}$) indicates a stable, uncongested path. A high `mdev` indicates severe bufferbloat, dynamic rerouting, or Wi-Fi interference.
3. **Path MTU Testing via Ping**:
   ```bash
   # Linux: send 1472-byte payload + 28 bytes (20 IP + 8 ICMP) = 1500 bytes with Don't Fragment flag:
   ping -M do -s 1472 8.8.8.8
   # If MTU is < 1500, returns: "Frag needed and DF set (mtu = 1492)"
   ```

**Citations & References:**
- RFC 792: Internet Control Message Protocol (ICMP)
- RFC 4443: Internet Control Message Protocol (ICMPv6) for IPv6
- USENIX: The Story of the PING Program (Mike Muuss)

---

## Traceroute, Tracert & MTR: Hop-by-Hop Path Deconstruction
### The Mechanics of Intentional TTL Expiration

Unlike `ping` (which measures end-to-end latency), `traceroute` reveals every single Layer 3 router hop along the path by weaponizing **ICMP Time-to-Live Exceeded (Type 11, Code 0)** messages:

```
 Probe 1 (TTL=1) ──► [ Router 1 ] ──► (Drops packet, returns ICMP Type 11 from R1 IP) ──► Latency: 1.0 ms
 Probe 2 (TTL=2) ──► [ Router 1 ] ──► [ Router 2 ] ──► (Drops packet, returns ICMP Type 11 from R2 IP) ──► Latency: 8.2 ms
 Probe 3 (TTL=3) ──► [ Router 1 ] ──► [ Router 2 ] ──► [ Router 3 ] ──► (Drops packet, ICMP Type 11) ──► Latency: 15.1 ms
 ...
 Probe N (TTL=N) ──► [ Destination Server ] ──► Returns Port Unreachable or TCP SYN-ACK / Echo Reply! ──► Target reached!
```

### Probe Methodologies Across Operating Systems
- **Linux/macOS (`traceroute`)**: Transmits UDP datagrams to high, unused ports (`33434 - 33534`) by default.
- **Windows (`tracert`)**: Transmits ICMP Echo Request packets by default.
- **TCP Traceroute (`traceroute -T -p 80` or `tcptraceroute`)**: Transmits TCP SYN packets to port 80/443. Crucial in enterprise environments where firewalls block all UDP and ICMP traffic but permit web traffic.

### Reading and Interpreting Traceroute Output

```bash
$ traceroute -n 142.250.195.46
 1  192.168.1.1   1.042 ms   0.985 ms   0.912 ms  # Local Gateway
 2  10.50.0.1     8.214 ms   8.150 ms   8.099 ms  # ISP Access Concentrator
 3  * * *                                         # Firewalled / Rate-limited hop
 4  182.79.245.1  14.320 ms  14.280 ms  14.195 ms # Regional Transit Hub
 5  72.14.239.45  18.420 ms  18.390 ms  18.310 ms # Google Peering Edge
 6  142.250.195.46 19.890 ms 19.750 ms  19.680 ms # Final Destination Server
```

#### Crucial Interpretation Principles
1. **The `* * *` Mystery**: Asterisks do NOT mean the link is broken! If subsequent hops (Hops 4, 5, 6) reply, traffic is flowing smoothly. It simply means Router 3 is configured to suppress ICMP TTL generation to conserve CPU.
2. **Diagnosing Asymmetric Link Congestion**: If latency jumps from $14\text{ ms}$ at Hop 4 to $210\text{ ms}$ at Hop 5 and **remains elevated** across all subsequent hops, the link between Hop 4 and Hop 5 is the physical bottleneck (e.g., congested undersea fiber cable or saturated circuit).
3. **MTR (My Traceroute)**: Combines `traceroute` and `ping` into an interactive live display, sending continuous probes to measure packet loss percentage and jitter at every hop simultaneously.

**Citations & References:**
- RFC 1393: Traceroute Using an IP Option
- Linux man-pages: traceroute(8), mtr(8)
- NANOG: A Practical Guide to (Correctly) Troubleshooting with Traceroute (Richard A Steenbergen)

---

## DNS Diagnostic Mastery: `dig` and `nslookup`
### The Power of `dig` (Domain Information Grok)

While legacy tools like `nslookup` remain available, `dig` (RFC 1035, developed by ISC) is the definitive industry standard for debugging DNS infrastructure.

### Dissecting Complete `dig` Output

```bash
$ dig @8.8.8.8 google.com A
; <<>> DiG 9.18.28 <<>> @8.8.8.8 google.com A
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 48215
;; flags: qr rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 512
;; QUESTION SECTION:
;google.com.                    IN      A

;; ANSWER SECTION:
google.com.             300     IN      A       142.250.195.46

;; Query time: 14 msec
;; SERVER: 8.8.8.8#53(8.8.8.8) (UDP)
;; WHEN: Wed Oct 14 00:00:00 IST 2026
;; MSG SIZE  rcvd: 55
```

#### Anatomy of the Header & Flags
- **`status: NOERROR`**: Resolution succeeded. Common error statuses include:
  - `NXDOMAIN` (Non-Existent Domain): The queried domain is not registered or misspelled.
  - `SERVFAIL` (Server Failure): The resolver encountered an internal failure or DNSSEC signature validation failed.
  - `REFUSED`: The nameserver refused to answer (e.g., query policy violation).
- **Flags**:
  - `qr` (Query Response): This packet is a response, not a request.
  - `rd` (Recursion Desired): The client requested recursive resolution.
  - `ra` (Recursion Available): The nameserver supports recursive queries.
  - `aa` (Authoritative Answer): The responding server is the authoritative nameserver for this domain zone (not a cached response from a resolver).

### Advanced Production Diagnostic Commands

```bash
# 1. Trace iterative traversal from Root servers down to Authoritative:
dig +trace example.com

# 2. Extract strictly the returned IP addresses (ideal for shell scripts):
dig +short google.com

# 3. Query specific record types:
dig cloudflare.com MX +short
dig github.com TXT

# 4. Reverse DNS lookup (IP to Hostname via in-addr.arpa):
dig -x 142.250.195.46 +short
```

**Citations & References:**
- RFC 1035: Domain Names - Implementation and Specification
- BIND 9 Administrator Reference Manual (ISC BIND)
- DNS and BIND (Cricket Liu & Paul Albitz), O'Reilly Media

---

## Socket & Connection Inspection: `ss` and `netstat`
### Modern Kernel Socket Inspection with `ss`

Historically, administrators used `netstat`. On modern Linux kernels, `netstat` is deprecated because it parses `/proc/net/tcp` slowly. The modern tool **`ss` (Socket Statistics)** queries the kernel networking subsystem directly via `netlink` sockets, operating orders of magnitude faster on servers hosting hundreds of thousands of connections.

### The Standard Diagnostic Command: `ss -tulpn`
```bash
$ sudo ss -tulpn
Netid  State   Recv-Q  Send-Q   Local Address:Port    Peer Address:Port   Process
tcp    LISTEN  0       128      0.0.0.0:22            0.0.0.0:*           users:(("sshd",pid=942,fd=3))
tcp    LISTEN  0       511      127.0.0.1:6379        0.0.0.0:*           users:(("redis-server",pid=1120,fd=6))
tcp    LISTEN  0       10       0.0.0.0:8080          0.0.0.0:*           users:(("python3",pid=4150,fd=4))
tcp    ESTAB   0       0        192.168.1.5:52341     142.250.195.46:443  users:(("chrome",pid=3210,fd=45))
udp    UNCONN  0       0        0.0.0.0:53            0.0.0.0:*           users:(("dnsmasq",pid=780,fd=4))
```

- Flag breakdown: `-t` (TCP), `-u` (UDP), `-l` (Listening sockets only), `-p` (show Process name & PID), `-n` (numeric ports/IPs without DNS resolution).

#### The `127.0.0.1` vs. `0.0.0.0` Bind Address Trap
One of the most frequent junior developer pitfalls:
- **`127.0.0.1:8080` (Loopback Interface)**: The application is bound strictly to the local host. External machines on the LAN or Internet **cannot connect** to this port!
- **`0.0.0.0:8080` (INADDR_ANY)**: The application listens on **all active network interfaces** (Ethernet, Wi-Fi, VPN), accepting external connections.

### Interpreting Queue Backlogs: `Recv-Q` and `Send-Q`
- For an **ESTABLISHED** connection:
  - `Recv-Q > 0`: Bytes received by the kernel but not yet read by the application (application is CPU-saturated or hanging).
  - `Send-Q > 0`: Bytes buffered in kernel memory awaiting transmission/ACK from peer (network is congested or peer is slow).
- For a **LISTEN** socket:
  - `Recv-Q`: Number of completed connections waiting in the accept queue.
  - `Send-Q`: Maximum backlog capacity (e.g., `listen(backlog)` parameter). If `Recv-Q == Send-Q`, incoming connections are being dropped!

**Citations & References:**
- Linux man-pages: ss(8), ip-route(8)
- Linux Kernel Documentation: Documentation/networking/netlink.rst
- Systems Performance: Enterprise and the Cloud (Brendan Gregg), Chapter 10 (Network)

---

## Packet Sniffing & Wire Analysis: `tcpdump` & Berkeley Packet Filters (BPF)
### Capturing Raw Packets at Wire Speed

When high-level diagnostic tools fail to identify an elusive network bug, engineers capture raw packets directly from the network interface using **`tcpdump`**. Operating in promiscuous mode via `libpcap`, `tcpdump` captures Layer 2, Layer 3, Layer 4, and payload data directly off the network driver.

### Essential `tcpdump` Operational Flags
```bash
# -i: interface; -n: no DNS; -nn: no port names; -v/-vv: verbose; -s0: capture full packet
sudo tcpdump -i eth0 -nn -s0

# Save packet stream to a standard PCAP file for Wireshark analysis:
sudo tcpdump -i eth0 -nn -w outage_capture.pcap port 80 or port 443

# Read back and inspect a previously captured PCAP file:
tcpdump -nn -r outage_capture.pcap
```

### Berkeley Packet Filters (BPF) Syntax
BPF programs compile into bytecode executed directly in kernel space, filtering packets before copying them to user memory:

```bash
# Filter by IP Host or Subnet:
sudo tcpdump host 198.51.100.10
sudo tcpdump net 192.168.1.0/24

# Filter by Layer 4 Port:
sudo tcpdump port 443
sudo tcpdump portrange 8000-8080

# Exclude Noise (e.g., exclude your active SSH connection):
sudo tcpdump not port 22

# Advanced Bitwise TCP Flag Filtering:
# Capture only TCP SYN packets (Connection Initiation):
sudo tcpdump 'tcp[tcpflags] & tcp-syn != 0 and tcp[tcpflags] & tcp-ack == 0'

# Capture TCP RST packets (Connection Aborts / Port Refusals):
sudo tcpdump 'tcp[tcpflags] & tcp-rst != 0'
```

**Citations & References:**
- The BSD Packet Filter: A New Architecture for User-level Packet Capture (Steven McCanne & Van Jacobson, USENIX 1993)
- tcpdump/libpcap Project Documentation: tcpdump.org
- Linux man-pages: pcap-filter(7)

---

## Wireshark Analysis & Common Outage Signatures
### Graphical Packet Dissection with Wireshark

**Wireshark** (originally Ethereal) is the world's preeminent graphical network protocol analyzer. It decodes thousands of protocol layers down to individual bits, provides cryptographic TLS decryption with session keys, and reconstructs multi-packet conversations.

```
┌────────────────────────────────────────────────────────────────────────┐
│                      WIRESHARK THREE-PANE INTERFACE                    │
├────────────────────────────────────────────────────────────────────────┤
│ 1. PACKET LIST PANE: Chronological table (No., Time, Src, Dst, Proto)  │
│ 2. PACKET DETAILS PANE: Tree structure of decoded headers (L2 -> L7)   │
│ 3. PACKET BYTES PANE: Raw hexadecimal and ASCII byte dump              │
└────────────────────────────────────────────────────────────────────────┘
```

### Crucial Wireshark Display Filters
Unlike capture filters (which discard packets before saving), **Display Filters** filter captured packets on screen:
- `ip.addr == 192.168.1.5` : All traffic involving this IP.
- `tcp.port == 443` : All HTTPS traffic.
- `http.request.method == "POST"` : Filter for specific HTTP methods.
- `dns.flags.response == 1 && dns.flags.rcode != 0` : Capture all failed DNS queries.
- `tcp.analysis.retransmission` : Isolates dropped packets triggering retransmissions.
- `tcp.analysis.flags` : Highlights duplicate ACKs, window updates, and zero-window warnings.

### The 'Follow TCP Stream' Superpower
By right-clicking any TCP packet in Wireshark and selecting **Follow -> TCP Stream**, Wireshark reassembles all out-of-order segments across the entire session into a clean, human-readable transcript, displaying client transmissions in red and server responses in blue.

### Common Real-World Production Outage Signatures

| Symptom / Error | Diagnostic Signature | Root Cause | Engineering Solution |
| :--- | :--- | :--- | :--- |
| **`Connection Refused`** | Client sends `SYN`; Server immediately replies with `RST` | No process is listening on the target port | Check service status (`systemctl status`), verify port in config. |
| **Connection Times Out** | Client sends `SYN`, receives zero reply, retransmits `SYN` repeatedly | A firewall (iptables/AWS Security Group) is dropping packets | Open ingress port rules on firewall/security group. |
| **`CLOSE_WAIT` Accumulation** | Hundreds of sockets in `CLOSE_WAIT` on server | Application code receives `EOF` on socket but never calls `close()` | Fix socket leak in application backend code. |
| **`NXDOMAIN` on internal host**| `dig` returns `status: NXDOMAIN` | Typo in hostname or missing search domain in `/etc/resolv.conf` | Correct domain spelling or configure local DNS search domain. |

**Citations & References:**
- Wireshark User's Guide (Gerald Combs et al.)
- Practical Packet Analysis: Using Wireshark to Solve Real-World Network Problems (Chris Sanders)
- RFC 793: Transmission Control Protocol (RST Generation)

---
