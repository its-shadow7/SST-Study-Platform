# Lecture 3: IP Addresses and Subnetting I
## Student Notes — SST Computer Networks (Term 5)

---

## 🎯 Learning Objectives

By the end of this lecture, you should be able to:
- Explain why global logical addressing (**IPv4**) is necessary alongside physical MAC addressing.
- Convert fluently between **32-bit binary** and **dotted-decimal** notation using fast mental math heuristics.
- Understand the historical **Classful Addressing Architecture** (Classes A, B, C, D, E) and analyze why it led to catastrophic address exhaustion.
- Master **CIDR (Classless Inter-Domain Routing)** prefix notation and the mechanics of the **Subnet Mask**.
- Perform bitwise **AND operations** to extract the **Network Address** from an arbitrary IP and mask.
- Accurately calculate the **Network ID, First Usable Host, Last Usable Host, Broadcast Address**, and **Total Usable Capacity** for any prefix length.
- Master the **"Magic Number" Subnetting Technique** to solve subnet boundary problems in seconds without paper-and-pencil binary expansion.
- Distinguish between **RFC 1918 Private IP Spaces**, Public IPs, and specialized reservations (Loopback, APIPA, CGNAT, Limited Broadcast).
- Solve real-world subnetting numericals across arbitrary octet boundaries (/18, /22, /26, /29, /30).

---

## 1. Why Do We Need IP Addresses?

In Lecture 2, we learned that Network Interface Cards possess burned-in 48-bit **MAC addresses**. Why can't the global internet simply route packets directly using MAC addresses?

### The Inherent Flaw of Flat vs. Hierarchical Addressing
MAC addresses are **flat identifiers**:
- `3C:22:FB:4A:89:12` provides zero geographic or network topological information. It tells you *who* the manufacturer was, but nothing about *where* the computer is located.
- If routers forwarded packets based on MAC addresses, every core router on the planet would need a routing table entry for every single device connected to the internet (>30 billion devices). This is an $O(N)$ lookup disaster causing immediate memory and bandwidth collapse.

In contrast, **IP addresses are hierarchical**:
- Analogous to postal mailing addresses: `Country -> State -> City -> Zip Code -> Street -> House Number`.
- Core routers only need to inspect the top-level **Network Prefix** to forward packets to the correct Autonomous System or ISP. Intermediate routers ignore host details until the packet reaches the local subnet.

```
Postal Address:    [ USA ] . [ California ] . [ San Francisco ] . [ House #42 ]
IPv4 Address:      [ 192 . 168 . 1 ] . [ 50 ]
                   └─ Network Portion ┘ └ Host Portion ┘
```

---

## 2. Anatomy of an IPv4 Address

An **IPv4 address** is a **32-bit unsigned binary integer**, divided into **four 8-bit fields called octets**, separated by dots:

```
Binary:  11000000 . 10101000 . 00000001 . 00110010
Octet:       1st        2nd        3rd        4th
Decimal:     192   .    168   .     1    .     50
```

- Each octet ranges from `00000000` ($0$) to `11111111` ($255$).
- Total possible IPv4 addresses:

  $$2^{32} = 4,294,967,296 \approx 4.29\text{ billion addresses}$$

### Binary $\leftrightarrow$ Decimal Conversion Mastery
Each octet has 8 bit positions with descending powers of 2:

```
Bit Position:  b7   b6   b5   b4   b3   b2   b1   b0
Power of 2:    2^7  2^6  2^5  2^4  2^3  2^2  2^1  2^0
Decimal Value: 128   64   32   16    8    4    2    1
```

#### Fast Mental Conversion Shortcuts:
1. **Accumulation Table (All leading 1s)**:
   - `10000000` = **128**
   - `11000000` = 128 + 64 = **192**
   - `11100000` = 192 + 32 = **224**
   - `11110000` = 224 + 16 = **240**
   - `11111000` = 240 + 8 = **248**
   - `11111100` = 248 + 4 = **252**
   - `11111110` = 252 + 2 = **254**
   - `11111111` = 254 + 1 = **255**
2. **Reverse Subtraction Rule**:
   To convert decimal to binary: Subtract the largest power of 2 that fits, record a `1`, and repeat with the remainder:
   - Example ($172$):
     - $172 - 128 = 44$ (bit 7 = 1)
     - $44 < 64$ (bit 6 = 0)
     - $44 - 32 = 12$ (bit 5 = 1)
     - $12 < 16$ (bit 4 = 0)
     - $12 - 8 = 4$ (bit 3 = 1)
     - $4 - 4 = 0$ (bit 2 = 1)
     - Remaining bits = 0
     - Result: `10101100`

---

## 3. Historical Context: The Classful Addressing System

In the original 1981 ARPANET architecture (RFC 791), IPv4 addresses were rigidly divided into 5 classes based on the initial bits of the first octet:

```
Class A:  0 | Network (7 bits) | Host (24 bits)
Class B: 10 | Network (14 bits) | Host (16 bits)
Class C: 110 | Network (21 bits) | Host (8 bits)
Class D: 1110 | Multicast Group ID (28 bits)
Class E: 1111 | Experimental / Reserved (28 bits)
```

### The Class Breakdown Table

| Class | Leading Bits | 1st Octet Range | Default Mask | Networks Available | Hosts per Network | Intended Use Case |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **A** | `0` | $1 - 126$ | `255.0.0.0` (/8) | $126$ ($2^7 - 2$) | $16,777,214$ ($2^{24} - 2$) | Enormous national/corporate entities (IBM, MIT, DoD) |
| **B** | `10` | $128 - 191$ | `255.255.0.0` (/16) | $16,384$ ($2^{14}$) | $65,534$ ($2^{16} - 2$) | Universities and mid-sized organizations |
| **C** | `110` | $192 - 223$ | `255.255.255.0` (/24) | $2,097,152$ ($2^{21}$) | $254$ ($2^8 - 2$) | Small business subnets |
| **D** | `1110` | $224 - 239$ | N/A (No host bits) | N/A | N/A | IP Multicasting (video streaming, routing protocols) |
| **E** | `1111` | $240 - 255$ | N/A | N/A | N/A | Experimental & research (permanently reserved) |

> **Note on Octet 127**: `127.0.0.0/8` was intentionally omitted from Class A to serve as the system **Loopback block** (`127.0.0.1` = localhost).

### Why Classful Addressing Failed
1. **Infinitesimal Flexibility**: If a company had 300 employees, a Class C license (max 254 hosts) was too small. The company was forced to acquire a Class B license (65,534 hosts), **wasting over 65,000 global public IP addresses**.
2. **Rapid Routing Table Explosion**: Routing tables in internet core routers grew exponentially because routers had to track individual Class C allocations.
3. **Imminent Exhaustion**: By 1992, available Class B space was on the brink of total exhaustion, threatening the survival of the global Internet.

---

## 4. CIDR & Subnet Masks (The Classless Era)

In 1993, **CIDR (Classless Inter-Domain Routing - RFC 1519)** abolished the rigid A/B/C boundaries. Under CIDR, the boundary between the **Network Portion** and the **Host Portion** can be placed at **any arbitrary bit position from 0 to 32**.

### The Subnet Mask
A **subnet mask** is a 32-bit sequence containing **contiguous 1s** followed by **contiguous 0s**:
- The **1s** designate the **Network/Subnet bits**.
- The **0s** designate the **Host bits**.

```
Example: 255.255.255.192
Binary:  11111111 . 11111111 . 11111111 . 11000000
         └───────────── 26 Network Bits ──────────┘└─ 6 Host Bits ─┘
```

### CIDR Prefix Notation (`/N`)
Instead of writing out dotted-decimal masks (`255.255.255.192`), CIDR appends a slash followed by the count of active network bits:

$$\text{IP Address} / N \implies \mathbf{192.168.1.50/26}$$

---

## 5. Hardware Bitwise ANDing: How Routers Find the Network ID

When a packet arrives at an interface, a router does not parse text strings. Its silicon ALU computes a single clock-cycle bitwise **AND operation** between the packet's Destination IP and the interface Subnet Mask:

$$\text{Bitwise Truth Table: } 1 \land 1 = 1, \quad 1 \land 0 = 0, \quad 0 \land 1 = 0, \quad 0 \land 0 = 0$$

### Step-by-Step Bitwise Example
Determine the Network Address of `192.168.10.157/27`:

```
Decimal Value     Binary Octet Breakdown
IP:   192.168.10.157  ──►  11000000 . 10101000 . 00001010 . 10011101
Mask: 255.255.255.224 ──►  11111111 . 11111111 . 11111111 . 11100000
-----------------------------------------------------------------------
AND Result:                11000000 . 10101000 . 00001010 . 10000000
Dotted Decimal:            192      . 168      . 10       . 128
```

The router determines that this packet belongs to subnet **`192.168.10.128/27`**.

---

## 6. The Anatomy of Any Subnet: The 4 Critical Addresses

Every IPv4 subnet contains four mathematically defined boundaries:

```
[ Network Address ] [ First Usable Host . . . . . . Last Usable Host ] [ Directed Broadcast ]
  (Host bits all 0)   (Network + 1)                 (Broadcast - 1)      (Host bits all 1)
```

1. **Network Address**:
   - Bit pattern: All host bits set to `0`.
   - **Purpose**: Identifies the subnet itself in router routing tables. Cannot be assigned to any individual host NIC.
2. **First Usable Host Address**:
   - Bit pattern: Host bits are `000...001`.
   - Formula: $\text{Network Address} + 1$.
   - Conventionally assigned to the default gateway router interface.
3. **Last Usable Host Address**:
   - Bit pattern: Host bits are `111...110`.
   - Formula: $\text{Broadcast Address} - 1$.
4. **Directed Broadcast Address**:
   - Bit pattern: All host bits set to `1`.
   - **Purpose**: Sends a frame to every active host residing inside this specific subnet. Never forwarded across outside routers.
5. **Total Usable Host Formula**:

   $$\text{Total Addresses} = 2^H = 2^{(32 - N)}$$
   $$\text{Usable Hosts} = 2^H - 2$$

   *(Subtracting 2: one for the Network Address, one for the Broadcast Address)*

---

## 7. The "Magic Number" Shortcut Technique

In exams, interviews, and real-world network engineering, you cannot afford to write out 32 bits of binary for every question. The **Magic Number** method calculates all boundaries in under 10 seconds.

### The Algorithm
1. **Identify the "Interesting Octet"**:
   - `/1` to `/8`: 1st octet
   - `/9` to `/16`: 2nd octet
   - `/17` to `/24`: 3rd octet
   - `/25` to `/32`: 4th octet
2. **Calculate the Magic Number (Block Size)**:

   $$\text{Magic Number} = 256 - \text{Mask Value of the Interesting Octet}$$

   *(Alternatively: $2^{(8 - \text{borrowed bits})}$)*
3. **Find the Multiples of the Magic Number**:
   - Subnet boundaries in that octet always increment by the Magic Number:
   - $0, M, 2M, 3M, 4M, \dots$
4. **Locate the Interval**:
   - Find the multiple that is $\le \text{IP's octet value}$. That is your **Network Address**.
   - The next multiple $- 1$ is your **Broadcast Address**.

---

## 8. Complete Master CIDR Reference Table

| CIDR Prefix | Subnet Mask | Interesting Octet Mask | Magic Number (Block) | Total IPs | Usable Hosts | Typical Deployment |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **/24** | `255.255.255.0` | 0 | 256 | 256 | 254 | Standard LAN / Office Subnet |
| **/25** | `255.255.255.128` | 128 | 128 | 128 | 126 | Large Department Subnet |
| **/26** | `255.255.255.192` | 192 | 64 | 64 | 62 | Medium Workgroup |
| **/27** | `255.255.255.224` | 224 | 32 | 32 | 30 | Small Branch Office |
| **/28** | `255.255.255.240` | 240 | 16 | 16 | 14 | DMZ / Server Subnet |
| **/29** | `255.255.255.248` | 248 | 8 | 8 | 6 | Public Server Cluster |
| **/30** | `255.255.255.252` | 252 | 4 | 4 | 2 | Point-to-Point Router WAN Links |
| **/31** | `255.255.255.254` | 254 | 2 | 2 | 2 (RFC 3021) | High-density Data Center P2P links |
| **/32** | `255.255.255.255` | 255 | 1 | 1 | 1 | Single Host Route / Loopback IP |

---

## 9. Private IP Addresses (RFC 1918) & Special Blocks

To prevent immediate depletion of the 4.3 billion address space, the IETF standardized **RFC 1918**, reserving three blocks of IPv4 space strictly for private internal networks. Routers on the public internet are hardcoded to **drop any packets bearing these destination addresses**.

```
┌───────────────────────────────┬────────────────────────────────┬─────────────────┐
│ Private Address Range         │ CIDR Block                     │ Total Addresses │
├───────────────────────────────┼────────────────────────────────┼─────────────────┤
│ 10.0.0.0 – 10.255.255.255     │ 10.0.0.0/8 (Single Class A)    │ 16,777,216      │
│ 172.16.0.0 – 172.31.255.255   │ 172.16.0.0/12 (16 Class Bs)    │ 1,048,576       │
│ 192.168.0.0 – 192.168.255.255 │ 192.168.0.0/16 (256 Class Cs)  │ 65,536          │
└───────────────────────────────┴────────────────────────────────┴─────────────────┘
```

### Other Essential Reserved IPv4 Blocks

| Block | Description | Practical Real-World Meaning |
| :--- | :--- | :--- |
| `127.0.0.0/8` | **Loopback** | `127.0.0.1` refers to the local host machine itself. Traffic never reaches a physical NIC. |
| `169.254.0.0/16` | **APIPA (Link-Local)** | Automatic Private IP Addressing (RFC 3927). If your PC displays `169.254.x.x`, **your DHCP server is down or unreachable**! |
| `100.64.0.0/10` | **CGNAT (Carrier-Grade NAT)** | RFC 6598 space used by ISPs (Jio, Airtel, Starlink) to share public IPs among thousands of mobile subscribers. |
| `0.0.0.0/0` | **Default Route ("The Quad Zero")** | Represents "any network / unknown destinations" in router tables. |
| `255.255.255.255` | **Limited Broadcast** | Broadcast sent to all nodes on the immediate physical wire. Never forwarded by routers. |

---

## 10. Comprehensive Worked Subnetting Numericals

### Problem 1: 4th Octet Subnetting
**Prompt**: Given IP `192.168.5.178` with subnet mask `255.255.255.224` (/27), find:
1. Subnet mask in binary
2. Magic Number
3. Network Address
4. First Usable Host
5. Last Usable Host
6. Broadcast Address
7. Total Usable Hosts

**Solution**:
1. Mask `/27` = $24 + 3$ bits = `11111111.11111111.11111111.11100000`
2. Interesting octet is the 4th octet ($224$).

   $$\text{Magic Number} = 256 - 224 = \mathbf{32}$$

3. Subnet multiples: $0, 32, 64, 96, 128, \mathbf{160}, 192, \dots$
   - Target octet is $178$. The largest multiple $\le 178$ is $160$.
   - **Network Address** = `192.168.5.160`
4. **First Usable Host** = $160 + 1$ = `192.168.5.161`
5. Next subnet starts at $192$, so:
   - **Broadcast Address** = $192 - 1$ = `192.168.5.191`
   - **Last Usable Host** = $191 - 1$ = `192.168.5.190`
6. Host bits $H = 32 - 27 = 5$.

   $$\text{Usable Hosts} = 2^5 - 2 = 32 - 2 = \mathbf{30}\text{ hosts}$$

---

### Problem 2: 3rd Octet Subnetting (Across Octet Boundaries)
**Prompt**: An enterprise network administrator allocates `172.16.89.200/20`. Determine all boundary parameters.

**Solution**:
1. Prefix `/20`: Network bits span $16 + 4$ bits.
   - Mask: `255.255.240.0`.
2. Interesting octet is the **3rd octet** ($240$).

   $$\text{Magic Number} = 256 - 240 = \mathbf{16}$$

3. Multiples of 16 in the 3rd octet:
   - $0, 16, 32, 48, 64, \mathbf{80}, 96, \dots$
   - IP's 3rd octet is $89$. The largest multiple $\le 89$ is $80$.
4. Boundaries:
   - **Network Address**: `172.16.80.0`
   - **First Usable Host**: `172.16.80.1`
   - Next block begins at $96$, so the 3rd octet ends at $95$ and 4th octet ends at $255$:
   - **Broadcast Address**: `172.16.95.255`
   - **Last Usable Host**: `172.16.95.254`
5. Usable hosts:

   $$H = 32 - 20 = 12 \implies 2^{12} - 2 = 4096 - 2 = \mathbf{4094}\text{ hosts}$$

---

### Problem 3: Point-to-Point WAN Link Design
**Prompt**: Design a subnet for two router interfaces connected directly over a fiber serial link using `10.10.10.0/24`. We want zero wasted host addresses.

**Solution**:
- Hosts needed = 2 router interfaces.
- Formula: $2^H - 2 \ge 2 \implies 2^H \ge 4 \implies H = 2\text{ host bits}$.
- Prefix: $32 - 2 = \mathbf{/30}$.
- Subnet Mask: `255.255.255.252`.
- Magic Number = $256 - 252 = 4$.
- Subnet 1:
  - Network ID: `10.10.10.0/30`
  - Router 1 IP: `10.10.10.1`
  - Router 2 IP: `10.10.10.2`
  - Broadcast: `10.10.10.3`
  - Wasted host addresses: **0**!

---

## 📌 Summary Checklist & Exam Cram Notes

1. **Hierarchy**: IP addresses represent hierarchical routing domains, preventing flat-table global scale collapse.
2. **32 Bits**: 4 octets of 8 bits each; range 0.0.0.0 to 255.255.255.255.
3. **Classful System**: Class A (/8, 1-126), Class B (/16, 128-191), Class C (/24, 192-223), Class D (Multicast, 224-239), Class E (Experimental, 240-255).
4. **CIDR**: Classless Inter-Domain Routing allows subnetting at any arbitrary prefix length `/N`.
5. **Bitwise AND**: Router extracts Network Address by computing `Destination_IP AND Subnet_Mask`.
6. **Usable Hosts Formula**: $2^{(32 - \text{prefix})} - 2$ (excluding Network ID and Directed Broadcast).
7. **Magic Number**: $256 - \text{interesting\_octet\_mask} = \text{block size}$.
8. **RFC 1918 Private Blocks**: `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`.
9. **Troubleshooting Flag**: `169.254.x.x` indicates DHCP failure (APIPA).
10. **Loopback**: `127.0.0.1` stays inside the local TCP/IP kernel stack.

---

## 🧠 Practice Problems & Self-Check Questions

1. A computer is assigned IP `10.150.23.45` with mask `255.254.0.0`. What is its prefix length in CIDR notation? What is its Network Address?
2. Why is an address with all host bits set to `1` prohibited from being assigned to an individual computer interface?
3. Calculate the valid host range for `192.168.100.64/26`. Is `192.168.100.127` a valid host IP?
4. A network engineer claims that `172.32.1.1` is a private IP address. Is this correct or false? Justify using RFC 1918 specifications.
5. In a `/23` subnet, how many total IP addresses exist, and what is the subnet mask in dotted-decimal format?
