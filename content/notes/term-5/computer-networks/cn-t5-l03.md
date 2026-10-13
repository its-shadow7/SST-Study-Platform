# IPv4 Addressing, Subnetting, CIDR & Special Address Blocks
**Term:** Term 5 | **Subject:** CN | **Note ID:** `cn-t5-l03`
**Last Updated:** 2026-10-13T00:00:00Z

## Abstract & Summary
An exhaustive, rigorous masterclass in IPv4 architecture. Details binary numbering, classful history, CIDR prefix mechanics, bitwise AND operations, the mathematical foundations of subnetting, VLSM engineering, and RFC-reserved address spaces.

## Learning Objectives
- Explain why logical hierarchical IP addressing is required for global routing instead of flat hardware MAC addresses.
- Perform rapid, bidirectional binary-to-decimal and decimal-to-binary conversions across all 8-bit octet boundaries.
- Critique legacy classful addressing (Classes A, B, C, D, E) and explain the historical drivers behind the IPv4 address exhaustion crisis.
- Apply bitwise ANDing between IPv4 addresses and subnet masks to determine network IDs and route forwarding decisions.
- Master the step-by-step 'Magic Number' subnetting algorithm to compute network addresses, broadcast addresses, and usable host ranges (2^H - 2).
- Categorize reserved IPv4 blocks: RFC 1918 private spaces (10/8, 172.16/12, 192.168/16), loopback (127/8), APIPA (169.254/16), and RFC 3021 /31 point-to-point links.

## Key Takeaways
- Hierarchical IP addressing allows routers to summarize millions of endpoints into compact prefix entries, solving the global routing table explosion problem.
- An IPv4 address is an unsigned 32-bit integer divided into Network bits (N) and Host bits (H), where N + H = 32.
- A Subnet Mask is a contiguous sequence of N binary 1s followed by H binary 0s; routers perform a bitwise AND between destination IP and mask to extract the Network ID.
- Every standard IPv4 subnet reserves two addresses: the Network Address (all host bits 0) and the Broadcast Address (all host bits 1), yielding 2^H - 2 usable host addresses.
- RFC 3021 provides an exception for point-to-point links using /31 masks (H = 1), allowing both addresses to be assigned to router interfaces with zero wasted broadcast addresses.
- RFC 1918 reserves three private address spaces (10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16) that are non-routable on the public Internet, requiring NAT/PAT for public access.

---

## 1. Why Logical IP Addressing & IPv4 Architecture
### Why Can't the Internet Route Using MAC Addresses?
A natural question every engineer asks is: *If every network interface card (NIC) on earth already has a globally unique 48-bit MAC address, why did we invent a completely separate addressing system (IP addresses)?*

The answer lies in **topological hierarchy and routing scalability**:
- **MAC Addresses are Flat:** A manufacturer assigns a MAC address (e.g., Apple assigning `3C:52:82:...` in California) based on chip production, not physical location. If a laptop travels from Tokyo to New York to London, its MAC address never changes.
- **The Global Scaling Catastrophe:** If Internet core routers routed on flat MAC addresses, every single router on Earth would need to maintain a routing table entry for every connected device on the planet (over 20 billion devices!). A table lookup on 20 billion flat entries at 400 Gbps line rate is mathematically and physically impossible.
- **Hierarchical IP Addresses Solve Scaling:** An IP address indicates **topological location** within a network hierarchy, directly analogous to postal addresses:
  $$\text{Country} \longrightarrow \text{State} \longrightarrow \text{City} \longrightarrow \text{Postal Code} \longrightarrow \text{Street} \longrightarrow \text{House Number}$$
  A router in Tokyo does not need to know the specific laptop MAC in London; it only needs an entry matching the high-level network prefix representing the London ISP. The hundreds of thousands of individual devices behind that prefix are summarized into a single routing entry!

---

### IPv4 Address Anatomy
An IPv4 address is an unsigned **32-bit binary integer** ($2^{32} = 4,294,967,296$ unique addresses). To make this manageable for humans, it is expressed in **dotted-decimal notation**:
- The 32 bits are divided into **four 8-bit groups** called **octets**.
- Each octet is converted to a decimal integer from $0$ to $255$ ($2^8 = 256$ possibilities).
- The four decimal numbers are separated by periods:
  $$\mathbf{192.168.1.5}$$

```text
Dotted Decimal:        192      .     168      .      1       .      5
                        |              |              |              |
Binary Octets:      11000000    .  10101000    .  00000001    .  00000101
Bits:              [8 bits]       [8 bits]       [8 bits]       [8 bits]
Total Length:      32 bits (4 bytes)
```

---

### Binary <--> Decimal Conversion Fundamentals
Every network engineer must be able to convert 8-bit octets instantaneously. An octet consists of 8 positional bit weights:

| Bit Position | $b_7$ | $b_6$ | $b_5$ | $b_4$ | $b_3$ | $b_2$ | $b_1$ | $b_0$ |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Decimal Weight ($2^n$)** | **128** | **64** | **32** | **16** | **8** | **4** | **2** | **1** |

#### Decimal to Binary Algorithm:
Subtract positional values from left to right:
- **Example: Convert 218 to binary:**
  - $218 \ge 128 \implies \mathbf{1}$ (Remainder: $218 - 128 = 90$)
  - $90 \ge 64 \implies \mathbf{1}$ (Remainder: $90 - 64 = 26$)
  - $26 < 32 \implies \mathbf{0}$
  - $26 \ge 16 \implies \mathbf{1}$ (Remainder: $26 - 16 = 10$)
  - $10 \ge 8 \implies \mathbf{1}$ (Remainder: $10 - 8 = 2$)
  - $2 < 4 \implies \mathbf{0}$
  - $2 \ge 2 \implies \mathbf{1}$ (Remainder: $2 - 2 = 0$)
  - $0 < 1 \implies \mathbf{0}$
  $$\mathbf{218_{10} = 11011010_2}$$

#### The 8 Fundamental Subnetting Numbers to Memorize:
Subnet masks always feature contiguous runs of 1s from the left. There are only eight possible non-zero octet values in any valid subnet mask:

| Consecutive 1s | Binary Value | Positional Sum | Decimal Value |
| :---: | :--- | :--- | :---: |
| **1** | `10000000` | $128$ | **128** |
| **2** | `11000000` | $128 + 64$ | **192** |
| **3** | `11100000` | $128 + 64 + 32$ | **224** |
| **4** | `11110000` | $128 + 64 + 32 + 16$ | **240** |
| **5** | `11111000` | $128 + 64 + 32 + 16 + 8$ | **248** |
| **6** | `11111100` | $128 + 64 + 32 + 16 + 8 + 4$ | **252** |
| **7** | `11111110` | $128 + 64 + 32 + 16 + 8 + 4 + 2$ | **254** |
| **8** | `11111111` | $128 + 64 + 32 + 16 + 8 + 4 + 2 + 1$ | **255** |

**Citations & References:**
- RFC 791 - Internet Protocol Specification
- Kurose & Ross, Computer Networking: A Top-Down Approach (8th Ed), Chapter 4.3
- Comer, Internetworking with TCP/IP Vol. 1 (6th Ed), Chapter 4

---

## 2. Legacy Classful Addressing & The Address Exhaustion Crisis
### The Original Design: Classful Addressing (RFC 791)
When DARPA standardized IPv4 in 1981, they divided the 32-bit address space into five rigid **Classes (A, B, C, D, and E)** based on the leading high-order bits of the first octet:

```text
Class A:  0 [  7 bits Network  ] [        24 bits Host ID (16.7M hosts)       ]
Class B:  1 0 [  14 bits Net   ] [          16 bits Host ID (65,534 hosts)    ]
Class C:  1 1 0 [  21 bits Net ] [             8 bits Host ID (254 hosts)     ]
Class D:  1 1 1 0 [               28 bits Multicast Group ID                  ]
Class E:  1 1 1 1 [               28 bits Experimental / Reserved             ]
```

#### Detailed Breakdown of Address Classes:

| Class | Leading Bits | 1st Octet Decimal Range | Default Subnet Mask | Total Networks | Usable Hosts per Network |
| :---: | :---: | :---: | :---: | :---: | :---: |
| **Class A** | `0...` | **1 – 126** | `255.0.0.0` (/8) | $126$ | $2^{24} - 2 = \mathbf{16,777,214}$ |
| **Class B** | `10...` | **128 – 191** | `255.255.0.0` (/16) | $16,384$ | $2^{16} - 2 = \mathbf{65,534}$ |
| **Class C** | `110...` | **192 – 223** | `255.255.255.0` (/24) | $2,097,152$ | $2^8 - 2 = \mathbf{254}$ |
| **Class D** | `1110...` | **224 – 239** | None (Multicast) | N/A | Multicast Groups |
| **Class E** | `1111...` | **240 – 255** | None (Reserved) | N/A | Reserved for Future Use |

*(Note: The first octet value `127` was excluded from Class A and reserved exclusively for internal host loopback).*

---

### Why Classful Addressing Failed Catastrophically
By the early 1990s, the explosive growth of the commercial Internet exposed severe architectural flaws in the rigid classful allocation model:

1. **The Massive Inflexibility Gap:**
   - Suppose an enterprise had **500 computers**.
   - A **Class C** allocation was too small (max 254 hosts).
   - The only alternative was to grant the enterprise a **Class B** block ($65,534$ host addresses).
   - The enterprise utilized 500 addresses and left over **65,000 public IP addresses permanently wasted!**
2. **Rapid Depletion of Class B Blocks:**
   - There were only 16,384 Class B networks in existence. By 1992, available Class B allocations were rapidly approaching total exhaustion.
3. **Routing Table Explosion:**
   - If ISPs instead allocated multiple Class C blocks to a growing organization, global backbone routers had to store separate routing entries for each Class C block, threatening to overwhelm router memory.

To prevent the total collapse of the Internet, the IETF enacted a two-pronged emergency strategy in 1993:
- **Long-term solution:** Designing an entirely new protocol with a vast 128-bit address space (**IPv6**).
- **Immediate solution:** Abolishing classful boundaries through **CIDR (Classless Inter-Domain Routing - RFC 1519)** and introducing **Private Address Spaces (RFC 1918)** coupled with **NAT**.

**Citations & References:**
- RFC 791 - Internet Protocol
- RFC 1519 - Classless Inter-Domain Routing (CIDR): an Address Assignment and Aggregation Strategy
- Kurose & Ross, Computer Networking: A Top-Down Approach (8th Ed), Chapter 4.3

---

## 3. Subnet Masks, Bitwise ANDing, and CIDR Notation
### The Architectural Split: Network Bits vs. Host Bits
Every IPv4 address is conceptually partitioned into two segments:
$$\mathbf{32\text{ bits total}} = \mathbf{N\text{ (Network bits)}} + \mathbf{H\text{ (Host bits)}}$$

1. **Network Bits ($N$):** Identify the specific network/subnet on which the device resides. All devices sharing the same local physical network segment must have identical network bits.
2. **Host Bits ($H$):** Identify the unique individual host interface within that specific network.

```text
IP Address: [      Network Identifier (N bits)      ] [ Host ID (H bits) ]
Subnet Mask:[ 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 ] [ 0 0 0 0 0 0 0 0 ]
```

---

### What is a Subnet Mask?
A **Subnet Mask** is a 32-bit bitmask consisting of a **contiguous run of $N$ binary 1s** starting from the most significant bit, followed by **$H$ binary 0s** filling the remaining positions.
- The 1s "mask" out the network portion.
- The 0s expose the host portion.

---

### The Bitwise AND Operation: How Routers Think
When a router receives a packet with a destination IP, it does not understand classes. It extracts the network ID by performing a **bitwise AND operation** between the destination IP address and the configured subnet mask:

$$\mathbf{\text{Network ID} = \text{Destination IP Address} \;\mathbf{AND}\; \text{Subnet Mask}}$$

Recall the truth table for the bitwise AND ($\&$) operator:
- $1 \;\&\; 1 = 1$
- $1 \;\&\; 0 = 0$
- $0 \;\&\; 1 = 0$
- $0 \;\&\; 0 = 0$

#### Worked Example:
Suppose a packet arrives with Destination IP `192.168.1.130` and the router interface has a subnet mask of `255.255.255.192` (`/26`).
Let us convert the fourth octet to binary and execute the bitwise AND:

```text
Target IP Octet 4 (130):   1 0 0 0 0 0 1 0
Subnet Mask Octet 4 (192): 1 1 0 0 0 0 0 0
------------------------------------------
Bitwise AND Result:        1 0 0 0 0 0 0 0  ==> Decimal 128
```
The router concludes that this host belongs to the subnet: **`192.168.1.128`**!

---

### Classless Inter-Domain Routing (CIDR) Notation
Under CIDR (RFC 1519), rigid classes are completely eliminated. Any arbitrary prefix length from `/1` to `/32` is valid. We denote the prefix length by appending a slash followed by the count of network bits $N$:
$$\mathbf{192.168.1.0/24} \quad \Longleftrightarrow \quad \text{Subnet Mask: } \mathbf{255.255.255.0}$$
$$\mathbf{10.50.0.0/16} \quad \Longleftrightarrow \quad \text{Subnet Mask: } \mathbf{255.255.0.0}$$
$$\mathbf{172.16.85.0/28} \quad \Longleftrightarrow \quad \text{Subnet Mask: } \mathbf{255.255.255.240}$$

---

### Complete CIDR Reference Table (4th Octet Subnetting: /24 to /32)

| CIDR Prefix | Subnet Mask | Host Bits ($H$) | Total Addresses ($2^H$) | Usable Hosts ($2^H - 2$) | Block Size (Magic #) |
| :---: | :--- | :---: | :---: | :---: | :---: |
| **/24** | `255.255.255.0` | $8$ | $256$ | **254** | $256$ |
| **/25** | `255.255.255.128` | $7$ | $128$ | **126** | $128$ |
| **/26** | `255.255.255.192` | $6$ | $64$ | **62** | $64$ |
| **/27** | `255.255.255.224` | $5$ | $32$ | **30** | $32$ |
| **/28** | `255.255.255.240` | $4$ | $16$ | **14** | $16$ |
| **/29** | `255.255.255.248` | $3$ | $8$ | **6** | $8$ |
| **/30** | `255.255.255.252` | $2$ | $4$ | **2** | $4$ |
| **/31** | `255.255.255.254` | $1$ | $2$ | **2 (RFC 3021)** | $2$ |
| **/32** | `255.255.255.255` | $0$ | $1$ | **1 (Host Route)** | $1$ |

**Citations & References:**
- RFC 1519 - Classless Inter-Domain Routing (CIDR)
- RFC 4632 - Classless Inter-domain Routing (CIDR): The Internet Address Assignment and Aggregation Plan
- Kurose & Ross, Computer Networking: A Top-Down Approach (8th Ed), Chapter 4.3

---

## 4. Subnet Anatomy & The Step-by-Step Subnetting Algorithm
### The Anatomy of Every Subnet
Within any standard IPv4 subnet with $H$ host bits ($H \ge 2$), the total address space contains $2^H$ IP addresses. However, exactly **two addresses are reserved by protocol standard** and cannot be assigned to host interfaces:

```text
+------------------------------------------------------------------------+
| 1. The Network Address (First Address):                                |
|    All H host bits are set to binary 0.                                |
|    Used exclusively in routing tables to identify the entire subnet.   |
+------------------------------------------------------------------------+
                                   |
                                   v
+------------------------------------------------------------------------+
| Usable Host Range (2^H - 2 addresses):                                 |
|    First Usable IP = Network Address + 1                               |
|    Last Usable IP  = Broadcast Address - 1                             |
+------------------------------------------------------------------------+
                                   |
                                   v
+------------------------------------------------------------------------+
| 2. The Directed Broadcast Address (Last Address):                      |
|    All H host bits are set to binary 1.                                |
|    A frame sent to this IP is delivered to every host on this subnet.  |
+------------------------------------------------------------------------+
```

#### Why $2^H - 2$?
$$\mathbf{\text{Usable Hosts} = 2^H - 2}$$
We subtract $2$ because:
1. One address is consumed by the **Network Identifier** (Host bits all 0).
2. One address is consumed by the **Directed Broadcast Identifier** (Host bits all 1).

---

### The Two Critical Exceptions: /31 and /32
- **RFC 3021 (/31 Subnets for Point-to-Point Links):**
  Historically, connecting two routers required a `/30` subnet ($2^2 = 4$ addresses: 1 network, 1 broadcast, leaving only 2 usable for the routers—wasting $50\%$ of allocated space!).
  RFC 3021 standardizes `/31` prefixes ($H = 1$, $2^1 = 2$ addresses) on point-to-point links. Because only two routers exist on the wire, no broadcast address is needed; both addresses are valid host endpoints!
- **/32 Subnets (Host Route / Loopback):**
  A `/32` prefix ($H = 0$, $2^0 = 1$ address) specifies an exact single IP address, commonly used for server loopback interfaces or VPN endpoints.

---

### The Step-by-Step "Magic Number" Subnetting Method
To find the subnet boundaries for any IP address and CIDR prefix without drawing out 32 bits of binary, use the **Magic Number (Block Size)** algorithm:

#### Step 1: Identify the "Interesting Octet"
Examine the CIDR prefix $/N$:
- If $N$ is between $1$ and $8$: Interesting octet is Octet 1.
- If $N$ is between $9$ and $16$: Interesting octet is Octet 2.
- If $N$ is between $17$ and $24$: Interesting octet is Octet 3.
- If $N$ is between $25$ and $32$: Interesting octet is Octet 4.

#### Step 2: Compute the Magic Number (Block Size)
Subtract the subnet mask value of the interesting octet from $256$:
$$\mathbf{\text{Magic Number (Block Size)} = 256 - \text{Mask Value}}$$
*(Alternatively: $\text{Magic Number} = 2^{8 - (N \bmod 8)}$ where $N \bmod 8$ is non-zero).*

#### Step 3: Find the Subnet Multiples
Subnets always begin at multiples of the Magic Number:
$$0, \; \text{Block Size}, \; 2 \times \text{Block Size}, \; 3 \times \text{Block Size}, \dots$$

#### Step 4: Determine the Network Address
Find the multiple of the Block Size that is less than or equal to the target IP's interesting octet. All preceding octets remain unchanged; all trailing octets become $0$.

#### Step 5: Determine the Broadcast Address
The Broadcast Address is one less than the *next* subnet multiple.

#### Step 6: Identify the Usable Range
$$\text{First Usable} = \text{Network Address} + 1$$
$$\text{Last Usable} = \text{Broadcast Address} - 1$$

---

### Worked Comprehensive Examples

#### Example 1: Analyze `192.168.10.142/26`
1. **Prefix:** `/26` means 26 ones. $26 - 24 = 2$ network bits in the 4th octet.
2. **Subnet Mask:** The 4th octet has two ones: $128 + 64 = 192$. Mask = `255.255.255.192`.
3. **Magic Number:** $256 - 192 = \mathbf{64}$.
4. **Subnet Multiples:** $0, 64, 128, 192, 256$.
5. **Target Octet:** $142$ falls between $128$ and $192$.
   - **Network Address:** `192.168.10.128`
   - **First Usable Host:** `192.168.10.129`
   - **Last Usable Host:** `192.168.10.190`
   - **Broadcast Address:** `192.168.10.191` (Next multiple $192 - 1$)
   - **Total Usable Hosts:** $2^6 - 2 = 64 - 2 = \mathbf{62}$.

#### Example 2: Analyze `172.16.85.45/20` (Subnetting in Octet 3)
1. **Prefix:** `/20` falls in the 3rd octet ($20 - 16 = 4$ bits).
2. **Subnet Mask:** The 3rd octet has four ones: $128 + 64 + 32 + 16 = 240$. Mask = `255.255.240.0`.
3. **Magic Number:** $256 - 240 = \mathbf{16}$ (in Octet 3).
4. **Subnet Multiples:** $0, 16, 32, 48, 64, 80, 96, \dots$
5. **Target Octet 3:** $85$ falls between $80$ and $96$.
   - **Network Address:** `172.16.80.0`
   - **First Usable Host:** `172.16.80.1`
   - **Last Usable Host:** `172.16.95.254`
   - **Broadcast Address:** `172.16.95.255`
   - **Total Usable Hosts:** $2^{12} - 2 = 4096 - 2 = \mathbf{4094}$.

**Citations & References:**
- RFC 3021 - Using 31-Bit Prefixes on IPv4 Point-to-Point Links
- Lammle, T., CompTIA Network+ Study Guide (Sybex)
- Kurose & Ross, Computer Networking: A Top-Down Approach (8th Ed), Chapter 4.3

---

## 5. Special-Purpose IPv4 Address Blocks & RFC 1918
### Reserved IPv4 Address Blocks
The Internet Assigned Numbers Authority (IANA) has reserved specific IPv4 address spaces for dedicated operational purposes. Routers and hosts treat these blocks with special routing rules.

---

### 1. Private Address Spaces (RFC 1918)
To address IPv4 exhaustion, RFC 1918 designated three private address blocks for enterprise and residential local networks:

| RFC 1918 Block | CIDR Prefix | Address Range | Total Addresses | Typical Deployment Scope |
| :--- | :---: | :--- | :---: | :--- |
| **24-bit Block** | **`10.0.0.0/8`** | `10.0.0.0` – `10.255.255.255` | $16,777,216$ | Massive enterprise corporate intranets, cloud VPCs (AWS, GCP) |
| **20-bit Block** | **`172.16.0.0/12`** | `172.16.0.0` – `172.31.255.255` | $1,048,576$ | Medium-to-large business campuses, Docker container bridges |
| **16-bit Block** | **`192.168.0.0/16`** | `192.168.0.0` – `192.168.255.255` | $65,536$ | Residential Wi-Fi routers, small home offices (SOHO) |

#### The Cardinal Rule of RFC 1918:
> **Private IP addresses are NON-ROUTABLE on the public Internet.**  
> Internet backbone routers instantly drop any packet containing an RFC 1918 source or destination address.

To allow millions of private hosts to access the public Internet, routers deploy **Network Address Translation (NAT) / Port Address Translation (PAT)**:
- The NAT gateway maps hundreds of internal private IPs to a single shared public IP address by assigning unique Layer 4 source port numbers.

```text
[Phone: 192.168.1.10:52134] --+
                              |--> [NAT Router: Public IP 203.0.113.5] ===> Public Internet
[Laptop: 192.168.1.20:52134] -+    (Translates to Port 60001 & 60002)
```

---

### 2. Loopback Address Block (RFC 1122): `127.0.0.0/8`
- Range: `127.0.0.0` to `127.255.255.255` (most commonly `127.0.0.1`, named `localhost`).
- **Behavior:** Packets transmitted to `127.x.x.x` are intercepted directly by the operating system kernel network stack and looped back internally to local listening sockets.
- **Hardware Isolation:** Bits addressed to loopback **never hit the physical network card or the wire**. It allows testing client-server software locally on a single machine without network access.

---

### 3. Automatic Private IP Addressing / Link-Local (RFC 3927): `169.254.0.0/16`
- Range: `169.254.1.0` to `169.254.254.255` (commonly referred to as **APIPA**).
- **Behavior:** When a computer boots up with DHCP enabled but receives no response from any DHCP server (e.g., the router is unplugged), the OS auto-assigns an address in this range.
- **Diagnostic Golden Rule:** *If an employee's machine displays an IP address starting with `169.254.x.x`, they have lost connection to the DHCP server!*

---

### 4. Other Specialized IPv4 Allocations

| Address / Block | Standard Reference | Operational Purpose |
| :--- | :--- | :--- |
| **`0.0.0.0/0`** | RFC 1122 | **Default Route** ("The Quad Zero"): Used in routing tables to match all internet destinations not covered by explicit prefixes. |
| **`0.0.0.0/32`** | RFC 1122 | Source address used by an unconfigured host during **DHCP Discover** before it possesses an assigned IP. |
| **`255.255.255.255`** | RFC 919 | **Limited Broadcast:** Sent to all hosts on the local physical link. Standard routers NEVER forward this packet to other subnets. |
| **`100.64.0.0/10`** | RFC 6598 | **Carrier-Grade NAT (CGNAT):** Used by mobile cellular and broadband ISPs to share public IPs among subscribers before residential routers. |
| **`224.0.0.0/4`** | RFC 1112 | **Multicast Space:** Class D addresses (`224.0.0.0` to `239.255.255.255`). |
| **`240.0.0.0/4`** | RFC 1112 | **Reserved Space:** Class E experimental addresses (unusable on the public Internet). |

**Citations & References:**
- RFC 1918 - Address Allocation for Private Internets
- RFC 3927 - Dynamic Configuration of IPv4 Link-Local Addresses
- RFC 6598 - IANA-Reserved IPv4 Prefix for Shared Address Space
- RFC 1122 - Requirements for Internet Hosts -- Communication Layers

---

## 6. IP Planning, VLSM Design & CLI Inspection
### Variable Length Subnet Masking (VLSM)
In complex enterprise networks, different subnets require wildly differing numbers of host addresses (e.g., a corporate headquarters campus might require 500 hosts for Engineering, 100 for Sales, 20 for Executive suites, and only 2 for router-to-router point-to-point links).

Under fixed-length subnetting, all subnets are constrained to the same mask size, causing massive address wastage. **Variable Length Subnet Masking (VLSM)** allows engineers to recursively subnet an address block, tailoring prefix sizes to exact host requirements.

#### The Golden Rule of VLSM Allocation:
> **Always allocate subnets in descending order of size—from largest host requirement to smallest host requirement.**

---

### Real-World VLSM Case Study
Suppose you are assigned the network block **`192.168.100.0/24`** ($256$ total addresses) and must support four distinct departments:
1. **Engineering:** 110 hosts
2. **Sales:** 50 hosts
3. **Finance:** 25 hosts
4. **Router WAN Link:** 2 hosts

```text
Step-by-Step Allocation Table:
+-------------+----------------+----------------+---------+--------------------+---------------------+
| Subnet Name | Hosts Required | Host Bits (H)  | Prefix  | Allocated Subnet   | Usable Host Range   |
+-------------+----------------+----------------+---------+--------------------+---------------------+
| Engineering | 110 hosts      | 2^7 - 2 = 126  | /25     | 192.168.100.0/25   | .1 to .126          |
| Sales       | 50 hosts       | 2^6 - 2 = 62   | /26     | 192.168.100.128/26 | .129 to .190        |
| Finance     | 25 hosts       | 2^5 - 2 = 30   | /27     | 192.168.100.192/27 | .193 to .222        |
| WAN Link    | 2 hosts        | 2^2 - 2 = 2    | /30     | 192.168.100.224/30 | .225 to .226        |
+-------------+----------------+----------------+---------+--------------------+---------------------+
Remaining Unallocated Space: 192.168.100.228 to 192.168.100.255 (available for future growth!)
```

---

### Command-Line Network Interface Inspection
Engineers verify local IP addressing, subnet masks, and default gateways using standard terminal commands:

#### On Windows:
```powershell
# Display active network configuration:
PS C:\> ipconfig /all
Ethernet adapter Ethernet:
   IPv4 Address. . . . . . . . . . . : 192.168.1.105(Preferred)
   Subnet Mask . . . . . . . . . . . : 255.255.255.0
   Default Gateway . . . . . . . . . : 192.168.1.1
   DHCP Server . . . . . . . . . . . : 192.168.1.1
   DNS Servers . . . . . . . . . . . : 1.1.1.1, 8.8.8.8

# Display local IP routing table:
PS C:\> route print
```

#### On Linux / macOS:
```bash
# Modern Linux network interface inspection:
$ ip -c addr show eth0
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP
    link/ether 00:15:5d:01:ca:82 brd ff:ff:ff:ff:ff:ff
    inet 10.0.4.15/24 brd 10.0.4.255 scope global dynamic eth0

# Inspect kernel routing table:
$ ip route show
default via 10.0.4.1 dev eth0 proto dhcp metric 100
10.0.4.0/24 dev eth0 proto kernel scope link src 10.0.4.15 metric 100
```

**Citations & References:**
- RFC 1878 - Variable Length Subnet Table For IPv4
- Kurose & Ross, Computer Networking: A Top-Down Approach (8th Ed), Chapter 4.3
- Stevens, W. R., TCP/IP Illustrated, Volume 1: The Protocols

---
