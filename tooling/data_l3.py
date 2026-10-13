"""
Data generator for Term 5 Computer Networks - Lecture 03
Topic: IPv4 Addressing, Subnetting, CIDR & Special Address Blocks
"""

L3_DATA = {
    "schema_version": 1,
    "note_id": "cn-t5-l03",
    "term": "Term 5",
    "subject_code": "CN",
    "topic_title": "IPv4 Addressing, Subnetting, CIDR & Special Address Blocks",
    "tags": ["Networking", "IP Addressing", "IPv4", "Subnetting", "CIDR", "VLSM", "RFC 1918", "Private IP", "Loopback", "APIPA"],
    "learning_objectives": [
        "Explain why logical hierarchical IP addressing is required for global routing instead of flat hardware MAC addresses.",
        "Perform rapid, bidirectional binary-to-decimal and decimal-to-binary conversions across all 8-bit octet boundaries.",
        "Critique legacy classful addressing (Classes A, B, C, D, E) and explain the historical drivers behind the IPv4 address exhaustion crisis.",
        "Apply bitwise ANDing between IPv4 addresses and subnet masks to determine network IDs and route forwarding decisions.",
        "Master the step-by-step 'Magic Number' subnetting algorithm to compute network addresses, broadcast addresses, and usable host ranges (2^H - 2).",
        "Categorize reserved IPv4 blocks: RFC 1918 private spaces (10/8, 172.16/12, 192.168/16), loopback (127/8), APIPA (169.254/16), and RFC 3021 /31 point-to-point links."
    ],
    "summary": "An exhaustive, rigorous masterclass in IPv4 architecture. Details binary numbering, classful history, CIDR prefix mechanics, bitwise AND operations, the mathematical foundations of subnetting, VLSM engineering, and RFC-reserved address spaces.",
    "key_takeaways": [
        "Hierarchical IP addressing allows routers to summarize millions of endpoints into compact prefix entries, solving the global routing table explosion problem.",
        "An IPv4 address is an unsigned 32-bit integer divided into Network bits (N) and Host bits (H), where N + H = 32.",
        "A Subnet Mask is a contiguous sequence of N binary 1s followed by H binary 0s; routers perform a bitwise AND between destination IP and mask to extract the Network ID.",
        "Every standard IPv4 subnet reserves two addresses: the Network Address (all host bits 0) and the Broadcast Address (all host bits 1), yielding 2^H - 2 usable host addresses.",
        "RFC 3021 provides an exception for point-to-point links using /31 masks (H = 1), allowing both addresses to be assigned to router interfaces with zero wasted broadcast addresses.",
        "RFC 1918 reserves three private address spaces (10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16) that are non-routable on the public Internet, requiring NAT/PAT for public access."
    ],
    "sections": [
        {
            "section_id": "sec-01-motivation-and-anatomy",
            "heading": "1. Why Logical IP Addressing & IPv4 Architecture",
            "body": """### Why Can't the Internet Route Using MAC Addresses?
A natural question every engineer asks is: *If every network interface card (NIC) on earth already has a globally unique 48-bit MAC address, why did we invent a completely separate addressing system (IP addresses)?*

The answer lies in **topological hierarchy and routing scalability**:
- **MAC Addresses are Flat:** A manufacturer assigns a MAC address (e.g., Apple assigning `3C:52:82:...` in California) based on chip production, not physical location. If a laptop travels from Tokyo to New York to London, its MAC address never changes.
- **The Global Scaling Catastrophe:** If Internet core routers routed on flat MAC addresses, every single router on Earth would need to maintain a routing table entry for every connected device on the planet (over 20 billion devices!). A table lookup on 20 billion flat entries at 400 Gbps line rate is mathematically and physically impossible.
- **Hierarchical IP Addresses Solve Scaling:** An IP address indicates **topological location** within a network hierarchy, directly analogous to postal addresses:
  $$\\text{Country} \\longrightarrow \\text{State} \\longrightarrow \\text{City} \\longrightarrow \\text{Postal Code} \\longrightarrow \\text{Street} \\longrightarrow \\text{House Number}$$
  A router in Tokyo does not need to know the specific laptop MAC in London; it only needs an entry matching the high-level network prefix representing the London ISP. The hundreds of thousands of individual devices behind that prefix are summarized into a single routing entry!

---

### IPv4 Address Anatomy
An IPv4 address is an unsigned **32-bit binary integer** ($2^{32} = 4,294,967,296$ unique addresses). To make this manageable for humans, it is expressed in **dotted-decimal notation**:
- The 32 bits are divided into **four 8-bit groups** called **octets**.
- Each octet is converted to a decimal integer from $0$ to $255$ ($2^8 = 256$ possibilities).
- The four decimal numbers are separated by periods:
  $$\\mathbf{192.168.1.5}$$

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
  - $218 \\ge 128 \\implies \\mathbf{1}$ (Remainder: $218 - 128 = 90$)
  - $90 \\ge 64 \\implies \\mathbf{1}$ (Remainder: $90 - 64 = 26$)
  - $26 < 32 \\implies \\mathbf{0}$
  - $26 \\ge 16 \\implies \\mathbf{1}$ (Remainder: $26 - 16 = 10$)
  - $10 \\ge 8 \\implies \\mathbf{1}$ (Remainder: $10 - 8 = 2$)
  - $2 < 4 \\implies \\mathbf{0}$
  - $2 \\ge 2 \\implies \\mathbf{1}$ (Remainder: $2 - 2 = 0$)
  - $0 < 1 \\implies \\mathbf{0}$
  $$\\mathbf{218_{10} = 11011010_2}$$

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
| **8** | `11111111` | $128 + 64 + 32 + 16 + 8 + 4 + 2 + 1$ | **255** |""",
            "citations": [
                "RFC 791 - Internet Protocol Specification",
                "Kurose & Ross, Computer Networking: A Top-Down Approach (8th Ed), Chapter 4.3",
                "Comer, Internetworking with TCP/IP Vol. 1 (6th Ed), Chapter 4"
            ]
        },
        {
            "section_id": "sec-02-classful-addressing-history",
            "heading": "2. Legacy Classful Addressing & The Address Exhaustion Crisis",
            "body": """### The Original Design: Classful Addressing (RFC 791)
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
| **Class A** | `0...` | **1 – 126** | `255.0.0.0` (/8) | $126$ | $2^{24} - 2 = \\mathbf{16,777,214}$ |
| **Class B** | `10...` | **128 – 191** | `255.255.0.0` (/16) | $16,384$ | $2^{16} - 2 = \\mathbf{65,534}$ |
| **Class C** | `110...` | **192 – 223** | `255.255.255.0` (/24) | $2,097,152$ | $2^8 - 2 = \\mathbf{254}$ |
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
- **Immediate solution:** Abolishing classful boundaries through **CIDR (Classless Inter-Domain Routing - RFC 1519)** and introducing **Private Address Spaces (RFC 1918)** coupled with **NAT**.""",
            "citations": [
                "RFC 791 - Internet Protocol",
                "RFC 1519 - Classless Inter-Domain Routing (CIDR): an Address Assignment and Aggregation Strategy",
                "Kurose & Ross, Computer Networking: A Top-Down Approach (8th Ed), Chapter 4.3"
            ]
        },
        {
            "section_id": "sec-03-subnet-masks-and-cidr",
            "heading": "3. Subnet Masks, Bitwise ANDing, and CIDR Notation",
            "body": """### The Architectural Split: Network Bits vs. Host Bits
Every IPv4 address is conceptually partitioned into two segments:
$$\\mathbf{32\\text{ bits total}} = \\mathbf{N\\text{ (Network bits)}} + \\mathbf{H\\text{ (Host bits)}}$$

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

$$\\mathbf{\\text{Network ID} = \\text{Destination IP Address} \\;\\mathbf{AND}\\; \\text{Subnet Mask}}$$

Recall the truth table for the bitwise AND ($\\&$) operator:
- $1 \\;\\&\\; 1 = 1$
- $1 \\;\\&\\; 0 = 0$
- $0 \\;\\&\\; 1 = 0$
- $0 \\;\\&\\; 0 = 0$

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
$$\\mathbf{192.168.1.0/24} \\quad \\Longleftrightarrow \\quad \\text{Subnet Mask: } \\mathbf{255.255.255.0}$$
$$\\mathbf{10.50.0.0/16} \\quad \\Longleftrightarrow \\quad \\text{Subnet Mask: } \\mathbf{255.255.0.0}$$
$$\\mathbf{172.16.85.0/28} \\quad \\Longleftrightarrow \\quad \\text{Subnet Mask: } \\mathbf{255.255.255.240}$$

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
| **/32** | `255.255.255.255` | $0$ | $1$ | **1 (Host Route)** | $1$ |""",
            "citations": [
                "RFC 1519 - Classless Inter-Domain Routing (CIDR)",
                "RFC 4632 - Classless Inter-domain Routing (CIDR): The Internet Address Assignment and Aggregation Plan",
                "Kurose & Ross, Computer Networking: A Top-Down Approach (8th Ed), Chapter 4.3"
            ]
        },
        {
            "section_id": "sec-04-subnet-anatomy-and-calculations",
            "heading": "4. Subnet Anatomy & The Step-by-Step Subnetting Algorithm",
            "body": """### The Anatomy of Every Subnet
Within any standard IPv4 subnet with $H$ host bits ($H \\ge 2$), the total address space contains $2^H$ IP addresses. However, exactly **two addresses are reserved by protocol standard** and cannot be assigned to host interfaces:

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
$$\\mathbf{\\text{Usable Hosts} = 2^H - 2}$$
We subtract $2$ because:
1. One address is consumed by the **Network Identifier** (Host bits all 0).
2. One address is consumed by the **Directed Broadcast Identifier** (Host bits all 1).

---

### The Two Critical Exceptions: /31 and /32
- **RFC 3021 (/31 Subnets for Point-to-Point Links):**
  Historically, connecting two routers required a `/30` subnet ($2^2 = 4$ addresses: 1 network, 1 broadcast, leaving only 2 usable for the routers—wasting $50\\%$ of allocated space!).
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
$$\\mathbf{\\text{Magic Number (Block Size)} = 256 - \\text{Mask Value}}$$
*(Alternatively: $\\text{Magic Number} = 2^{8 - (N \\bmod 8)}$ where $N \\bmod 8$ is non-zero).*

#### Step 3: Find the Subnet Multiples
Subnets always begin at multiples of the Magic Number:
$$0, \\; \\text{Block Size}, \\; 2 \\times \\text{Block Size}, \\; 3 \\times \\text{Block Size}, \\dots$$

#### Step 4: Determine the Network Address
Find the multiple of the Block Size that is less than or equal to the target IP's interesting octet. All preceding octets remain unchanged; all trailing octets become $0$.

#### Step 5: Determine the Broadcast Address
The Broadcast Address is one less than the *next* subnet multiple.

#### Step 6: Identify the Usable Range
$$\\text{First Usable} = \\text{Network Address} + 1$$
$$\\text{Last Usable} = \\text{Broadcast Address} - 1$$

---

### Worked Comprehensive Examples

#### Example 1: Analyze `192.168.10.142/26`
1. **Prefix:** `/26` means 26 ones. $26 - 24 = 2$ network bits in the 4th octet.
2. **Subnet Mask:** The 4th octet has two ones: $128 + 64 = 192$. Mask = `255.255.255.192`.
3. **Magic Number:** $256 - 192 = \\mathbf{64}$.
4. **Subnet Multiples:** $0, 64, 128, 192, 256$.
5. **Target Octet:** $142$ falls between $128$ and $192$.
   - **Network Address:** `192.168.10.128`
   - **First Usable Host:** `192.168.10.129`
   - **Last Usable Host:** `192.168.10.190`
   - **Broadcast Address:** `192.168.10.191` (Next multiple $192 - 1$)
   - **Total Usable Hosts:** $2^6 - 2 = 64 - 2 = \\mathbf{62}$.

#### Example 2: Analyze `172.16.85.45/20` (Subnetting in Octet 3)
1. **Prefix:** `/20` falls in the 3rd octet ($20 - 16 = 4$ bits).
2. **Subnet Mask:** The 3rd octet has four ones: $128 + 64 + 32 + 16 = 240$. Mask = `255.255.240.0`.
3. **Magic Number:** $256 - 240 = \\mathbf{16}$ (in Octet 3).
4. **Subnet Multiples:** $0, 16, 32, 48, 64, 80, 96, \\dots$
5. **Target Octet 3:** $85$ falls between $80$ and $96$.
   - **Network Address:** `172.16.80.0`
   - **First Usable Host:** `172.16.80.1`
   - **Last Usable Host:** `172.16.95.254`
   - **Broadcast Address:** `172.16.95.255`
   - **Total Usable Hosts:** $2^{12} - 2 = 4096 - 2 = \\mathbf{4094}$.""",
            "citations": [
                "RFC 3021 - Using 31-Bit Prefixes on IPv4 Point-to-Point Links",
                "Lammle, T., CompTIA Network+ Study Guide (Sybex)",
                "Kurose & Ross, Computer Networking: A Top-Down Approach (8th Ed), Chapter 4.3"
            ]
        },
        {
            "section_id": "sec-05-special-address-blocks",
            "heading": "5. Special-Purpose IPv4 Address Blocks & RFC 1918",
            "body": """### Reserved IPv4 Address Blocks
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
| **`240.0.0.0/4`** | RFC 1112 | **Reserved Space:** Class E experimental addresses (unusable on the public Internet). |""",
            "citations": [
                "RFC 1918 - Address Allocation for Private Internets",
                "RFC 3927 - Dynamic Configuration of IPv4 Link-Local Addresses",
                "RFC 6598 - IANA-Reserved IPv4 Prefix for Shared Address Space",
                "RFC 1122 - Requirements for Internet Hosts -- Communication Layers"
            ]
        },
        {
            "section_id": "sec-06-ip-planning-and-inspection",
            "heading": "6. IP Planning, VLSM Design & CLI Inspection",
            "body": """### Variable Length Subnet Masking (VLSM)
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
```""",
            "citations": [
                "RFC 1878 - Variable Length Subnet Table For IPv4",
                "Kurose & Ross, Computer Networking: A Top-Down Approach (8th Ed), Chapter 4.3",
                "Stevens, W. R., TCP/IP Illustrated, Volume 1: The Protocols"
            ]
        }
    ],
    "last_updated": "2026-10-13T00:00:00Z",
    "approval_status": "approved",
    "quiz": {
        "title": "Computer Networks Lecture 3: IPv4 Addressing, Subnetting, CIDR & Special Blocks",
        "description": "Comprehensive 25-question examination testing IPv4 binary conversions, classful history, bitwise AND operations, subnet calculation algorithms, VLSM, RFC 1918 private spaces, and loopback mechanics.",
        "estimated_minutes": 35,
        "questions": [
            # EASY QUESTIONS (Q1 - Q8)
            {
                "id": "q01",
                "type": "single_choice",
                "difficulty": "easy",
                "subtopic": "IPv4 Address Length",
                "question": "What is the total length of an IPv4 address in bits, and how many unique addresses does it provide?",
                "options": [
                    {"id": "opt-a", "text": "32 bits (approx. 4.29 billion addresses)"},
                    {"id": "opt-b", "text": "48 bits (approx. 281 trillion addresses)"},
                    {"id": "opt-c", "text": "64 bits"},
                    {"id": "opt-d", "text": "128 bits (approx. 3.4 * 10^38 addresses)"}
                ],
                "correctOptionIds": ["opt-a"],
                "explanation": "An IPv4 address is 32 bits long, yielding 2^32 = 4,294,967,296 addresses. (128 bits is the size of an IPv6 address; 48 bits is an Ethernet MAC address)."
            },
            {
                "id": "q02",
                "type": "single_choice",
                "difficulty": "easy",
                "subtopic": "Binary Conversion",
                "question": "What is the decimal equivalent of the binary octet '11000000'?",
                "options": [
                    {"id": "opt-a", "text": "128"},
                    {"id": "opt-b", "text": "192"},
                    {"id": "opt-c", "text": "224"},
                    {"id": "opt-d", "text": "168"}
                ],
                "correctOptionIds": ["opt-b"],
                "explanation": "Bit weights are 128 and 64 for the first two positions: 128 + 64 = 192."
            },
            {
                "id": "q03",
                "type": "single_choice",
                "difficulty": "easy",
                "subtopic": "Subnet Mask CIDR Notation",
                "question": "What is the dotted-decimal subnet mask corresponding to the CIDR prefix '/24'?",
                "options": [
                    {"id": "opt-a", "text": "255.0.0.0"},
                    {"id": "opt-b", "text": "255.255.0.0"},
                    {"id": "opt-c", "text": "255.255.255.0"},
                    {"id": "opt-d", "text": "255.255.255.128"}
                ],
                "correctOptionIds": ["opt-c"],
                "explanation": "A /24 prefix contains 24 consecutive binary 1s: 11111111.11111111.11111111.00000000, which evaluates to 255.255.255.0."
            },
            {
                "id": "q04",
                "type": "multiple_choice",
                "difficulty": "easy",
                "subtopic": "RFC 1918 Private Ranges",
                "question": "Which of the following IPv4 address ranges are officially defined as private (non-routable on the public Internet) under RFC 1918? (Select all that apply)",
                "options": [
                    {"id": "opt-a", "text": "10.0.0.0/8 (10.0.0.0 to 10.255.255.255)"},
                    {"id": "opt-b", "text": "172.16.0.0/12 (172.16.0.0 to 172.31.255.255)"},
                    {"id": "opt-c", "text": "192.168.0.0/16 (192.168.0.0 to 192.168.255.255)"},
                    {"id": "opt-d", "text": "8.8.8.0/24 (8.8.8.0 to 8.8.8.255)"}
                ],
                "correctOptionIds": ["opt-a", "opt-b", "opt-c"],
                "explanation": "RFC 1918 defines 10.0.0.0/8, 172.16.0.0/12, and 192.168.0.0/16 as private address blocks. 8.8.8.8 is a globally routable public anycast DNS server operated by Google."
            },
            {
                "id": "q05",
                "type": "single_choice",
                "difficulty": "easy",
                "subtopic": "Usable Host Formula",
                "question": "Given a standard IPv4 subnet with H host bits, what is the formula to calculate the number of usable host IP addresses?",
                "options": [
                    {"id": "opt-a", "text": "2^H"},
                    {"id": "opt-b", "text": "2^H - 1"},
                    {"id": "opt-c", "text": "2^H - 2"},
                    {"id": "opt-d", "text": "2^(H - 2)"}
                ],
                "correctOptionIds": ["opt-c"],
                "explanation": "The formula is 2^H - 2. The subtract-2 accounts for the reserved Network Address (all host bits 0) and Directed Broadcast Address (all host bits 1)."
            },
            {
                "id": "q06",
                "type": "single_choice",
                "difficulty": "easy",
                "subtopic": "Loopback Functionality",
                "question": "What is the primary operational characteristic of the IPv4 loopback address 127.0.0.1 (localhost)?",
                "options": [
                    {"id": "opt-a", "text": "Packets sent to it are transmitted over the local Wi-Fi router and looped back over the air."},
                    {"id": "opt-b", "text": "Packets never leave the host system; they are processed entirely within the local OS kernel network stack."},
                    {"id": "opt-c", "text": "It can be accessed by any computer on the local office LAN."},
                    {"id": "opt-d", "text": "It requires an active internet connection to resolve."}
                ],
                "correctOptionIds": ["opt-b"],
                "explanation": "The 127.0.0.0/8 block is reserved for loopback. Traffic sent to 127.0.0.1 is handled entirely within the host's operating system networking stack without ever leaving the machine or touching a physical network card."
            },
            {
                "id": "q07",
                "type": "multiple_choice",
                "difficulty": "easy",
                "subtopic": "Classful Addressing History",
                "question": "Which of the following statements regarding the historical Classful Addressing scheme are correct? (Select all that apply)",
                "options": [
                    {"id": "opt-a", "text": "Class A networks used an 8-bit network prefix (/8) and supported over 16 million hosts per network."},
                    {"id": "opt-b", "text": "Class C networks supported a maximum of 254 usable hosts."},
                    {"id": "opt-c", "text": "Class D addresses (224.0.0.0 to 239.255.255.255) were reserved for IP Multicast."},
                    {"id": "opt-d", "text": "Classful addressing was eliminated because it was too flexible and gave small companies too few addresses."}
                ],
                "correctOptionIds": ["opt-a", "opt-b", "opt-c"],
                "explanation": "Class A supported 16.7M hosts; Class C supported 254 hosts; Class D is multicast. Classful addressing was eliminated because it was rigid and wasteful, causing massive address exhaustion, not because it was 'too flexible'."
            },
            {
                "id": "q08",
                "type": "single_choice",
                "difficulty": "easy",
                "subtopic": "APIPA Link-Local",
                "question": "If an operating system with DHCP enabled boots up and assigns itself an IP address of '169.254.12.85', what does this typically indicate?",
                "options": [
                    {"id": "opt-a", "text": "The computer successfully received a public IP from an ISP."},
                    {"id": "opt-b", "text": "The computer failed to contact a DHCP server and auto-assigned an APIPA link-local address."},
                    {"id": "opt-c", "text": "The computer's network interface card is permanently damaged."},
                    {"id": "opt-d", "text": "The machine has connected directly to a Google data center."}
                ],
                "correctOptionIds": ["opt-b"],
                "explanation": "Addresses in 169.254.0.0/16 are APIPA (Automatic Private IP Addressing) link-local addresses. When a host requests DHCP but receives no response, the OS auto-assigns an address in this range, indicating the DHCP server is unreachable."
            },

            # MEDIUM QUESTIONS (Q9 - Q18)
            {
                "id": "q09",
                "type": "single_choice",
                "difficulty": "medium",
                "subtopic": "Bitwise AND Operation",
                "question": "A packet with destination IP address 192.168.1.75 arrives at a router where the subnet mask is 255.255.255.224 (/27). What is the Network Address for this packet?",
                "options": [
                    {"id": "opt-a", "text": "192.168.1.0"},
                    {"id": "opt-b", "text": "192.168.1.64"},
                    {"id": "opt-c", "text": "192.168.1.75"},
                    {"id": "opt-d", "text": "192.168.1.96"}
                ],
                "correctOptionIds": ["opt-b"],
                "explanation": "The mask /27 has a block size of 256 - 224 = 32 in the 4th octet. Subnet multiples are 0, 32, 64, 96, ... 75 falls between 64 and 96. Thus, the Network Address is 192.168.1.64."
            },
            {
                "id": "q10",
                "type": "single_choice",
                "difficulty": "medium",
                "subtopic": "Broadcast Address Calculation",
                "question": "What is the Directed Broadcast Address for the subnet containing the host IP 10.20.30.140/28?",
                "options": [
                    {"id": "opt-a", "text": "10.20.30.143"},
                    {"id": "opt-b", "text": "10.20.30.159"},
                    {"id": "opt-c", "text": "10.20.30.255"},
                    {"id": "opt-d", "text": "10.20.30.128"}
                ],
                "correctOptionIds": ["opt-a"],
                "explanation": "For /28, the mask is 255.255.255.240. Block size = 256 - 240 = 16. Multiples: 0, 16, 32, ... 128, 144. 140 falls in the subnet starting at 128. The next subnet starts at 144. The broadcast address is 144 - 1 = 143, so 10.20.30.143."
            },
            {
                "id": "q11",
                "type": "multiple_choice",
                "difficulty": "medium",
                "subtopic": "Subnet Characteristics",
                "question": "For the subnet 172.16.50.0/26, which of the following statements are correct? (Select all that apply)",
                "options": [
                    {"id": "opt-a", "text": "The subnet mask is 255.255.255.192."},
                    {"id": "opt-b", "text": "There are 62 usable host IP addresses in this subnet."},
                    {"id": "opt-c", "text": "The broadcast address is 172.16.50.63."},
                    {"id": "opt-d", "text": "172.16.50.64 is a usable host address in this subnet."}
                ],
                "correctOptionIds": ["opt-a", "opt-b", "opt-c"],
                "explanation": "/26 has 6 host bits: 2^6 - 2 = 62 usable hosts. Mask is 255.255.255.192. Range: Network is 172.16.50.0, Usable is .1 to .62, Broadcast is .63. 172.16.50.64 is the Network address of the NEXT subnet, not a usable host in this subnet."
            },
            {
                "id": "q12",
                "type": "single_choice",
                "difficulty": "medium",
                "subtopic": "Host Requirements & Prefix Selection",
                "question": "A network engineer must create a subnet that supports at least 28 simultaneous host interfaces. What is the most efficient CIDR prefix that satisfies this requirement without wasting addresses?",
                "options": [
                    {"id": "opt-a", "text": "/28 (supports 14 hosts)"},
                    {"id": "opt-b", "text": "/27 (supports 30 hosts)"},
                    {"id": "opt-c", "text": "/26 (supports 62 hosts)"},
                    {"id": "opt-d", "text": "/25 (supports 126 hosts)"}
                ],
                "correctOptionIds": ["opt-b"],
                "explanation": "We need 2^H - 2 >= 28. If H = 4, 2^4 - 2 = 14 (too small). If H = 5, 2^5 - 2 = 30 >= 28. Prefix length = 32 - 5 = /27."
            },
            {
                "id": "q13",
                "type": "multiple_choice",
                "difficulty": "medium",
                "subtopic": "Special IPv4 Addresses",
                "question": "Which of the following IPv4 addresses CANNOT be assigned to a standard PC network interface card? (Select all that apply)",
                "options": [
                    {"id": "opt-a", "text": "192.168.1.255 on a /24 network"},
                    {"id": "opt-b", "text": "127.0.0.1"},
                    {"id": "opt-c", "text": "10.10.10.0 on a /24 network"},
                    {"id": "opt-d", "text": "10.10.10.1 on a /24 network"}
                ],
                "correctOptionIds": ["opt-a", "opt-b", "opt-c"],
                "explanation": "192.168.1.255/24 is the broadcast address; 10.10.10.0/24 is the network address; 127.0.0.1 is reserved for internal loopback. None of these can be assigned to a physical host NIC. 10.10.10.1 is a perfectly valid usable host IP."
            },
            {
                "id": "q14",
                "type": "single_choice",
                "difficulty": "medium",
                "subtopic": "RFC 3021 /31 Subnets",
                "question": "What is the primary advantage of deploying /31 subnet masks on point-to-point router links as standardized in RFC 3021?",
                "options": [
                    {"id": "opt-a", "text": "It provides 10 Gbps encryption natively."},
                    {"id": "opt-b", "text": "It conserves IPv4 address space by eliminating wasted network and broadcast addresses, allocating both addresses to the two router interfaces."},
                    {"id": "opt-c", "text": "It allows 31 routers to share one physical wire."},
                    {"id": "opt-d", "text": "It prevents BGP route flapping."}
                ],
                "correctOptionIds": ["opt-b"],
                "explanation": "On point-to-point links between two routers, broadcast addresses are unnecessary. RFC 3021 allows using /31 (2 addresses total), assigning one to each router. This saves 50% of addresses compared to legacy /30 subnets."
            },
            {
                "id": "q15",
                "type": "multiple_choice",
                "difficulty": "medium",
                "subtopic": "NAT & Private IP Routing",
                "question": "Why can two completely unrelated companies both assign the identical IP address 192.168.1.100 to internal workstations without causing any IP conflict on the Internet? (Select all that apply)",
                "options": [
                    {"id": "opt-a", "text": "192.168.1.100 is an RFC 1918 private address and is never routed across public Internet backbones."},
                    {"id": "opt-b", "text": "Each company's border NAT router translates internal traffic to their respective unique public IP addresses before forwarding onto the Internet."},
                    {"id": "opt-c", "text": "The IEEE ensures that only one of the two companies can access the web at any given second."},
                    {"id": "opt-d", "text": "DNS automatically deletes the second company's duplicate packet."}
                ],
                "correctOptionIds": ["opt-a", "opt-b"],
                "explanation": "Private IP addresses (RFC 1918) have local scope within their respective enterprise networks and are filtered by public routers. Outbound communication uses NAT/PAT to translate to distinct public IP addresses, so duplicate private IPs never collide."
            },
            {
                "id": "q16",
                "type": "single_choice",
                "difficulty": "medium",
                "subtopic": "Subnet Mask Validation",
                "question": "Which of the following dotted-decimal values is an INVALID subnet mask?",
                "options": [
                    {"id": "opt-a", "text": "255.255.255.192"},
                    {"id": "opt-b", "text": "255.255.240.0"},
                    {"id": "opt-c", "text": "255.255.255.228"},
                    {"id": "opt-d", "text": "255.255.255.248"}
                ],
                "correctOptionIds": ["opt-c"],
                "explanation": "A valid subnet mask must consist of contiguous 1s followed by contiguous 0s. 228 in binary is 11100100, which has non-contiguous 1s separated by 0s. Hence, 255.255.255.228 is invalid."
            },
            {
                "id": "q17",
                "type": "multiple_choice",
                "difficulty": "medium",
                "subtopic": "Subnet Boundary Identification",
                "question": "Which of the following IP addresses represent valid Network Addresses (subnets) under a /28 mask? (Select all that apply)",
                "options": [
                    {"id": "opt-a", "text": "192.168.1.0"},
                    {"id": "opt-b", "text": "192.168.1.16"},
                    {"id": "opt-c", "text": "192.168.1.32"},
                    {"id": "opt-d", "text": "192.168.1.25"}
                ],
                "correctOptionIds": ["opt-a", "opt-b", "opt-c"],
                "explanation": "For /28, the block size is 256 - 240 = 16. Valid network addresses must be multiples of 16 in the 4th octet: 0, 16, 32, 48, 64, ... 25 is not a multiple of 16 (it is a usable host address inside the 192.168.1.16/28 subnet)."
            },
            {
                "id": "q18",
                "type": "single_choice",
                "difficulty": "medium",
                "subtopic": "Default Route Mechanics",
                "question": "What is the meaning of the route entry '0.0.0.0/0' in an operating system or router routing table?",
                "options": [
                    {"id": "opt-a", "text": "It drops all incoming traffic immediately."},
                    {"id": "opt-b", "text": "It represents the Default Route (Gateway of Last Resort), matching any destination IP address not matched by a more specific prefix."},
                    {"id": "opt-c", "text": "It restricts traffic to the local loopback adapter."},
                    {"id": "opt-d", "text": "It forces all traffic to route through satellite connections."}
                ],
                "correctOptionIds": ["opt-b"],
                "explanation": "0.0.0.0/0 has a prefix length of 0, meaning zero bits are masked. It matches all possible 32-bit destination IP addresses and acts as the Default Gateway of last resort when no more specific route matches."
            },

            # HARD QUESTIONS (Q19 - Q25)
            {
                "id": "q19",
                "type": "single_choice",
                "difficulty": "hard",
                "subtopic": "Subnetting Across Third Octet",
                "question": "Host A has the IP address 10.45.163.22/19. What is the First Usable IP and Last Usable IP of the subnet to which Host A belongs?",
                "options": [
                    {"id": "opt-a", "text": "First: 10.45.160.1, Last: 10.45.191.254"},
                    {"id": "opt-b", "text": "First: 10.45.163.1, Last: 10.45.163.254"},
                    {"id": "opt-c", "text": "First: 10.45.128.1, Last: 10.45.159.254"},
                    {"id": "opt-d", "text": "First: 10.45.160.0, Last: 10.45.191.255"}
                ],
                "correctOptionIds": ["opt-a"],
                "explanation": "/19 has 19 network bits. 19 - 16 = 3 bits in the 3rd octet. Mask = 255.255.224.0. Block size in 3rd octet = 256 - 224 = 32. Multiples: 0, 32, 64, 96, 128, 160, 192. The target 3rd octet 163 falls between 160 and 192. Network address = 10.45.160.0. Broadcast address = 10.45.191.255. First usable = 10.45.160.1; Last usable = 10.45.191.254."
            },
            {
                "id": "q20",
                "type": "multiple_choice",
                "difficulty": "hard",
                "subtopic": "Subnet Mask Mismatch & Communication",
                "question": "Host X (IP: 192.168.1.50/24) and Host Y (IP: 192.168.1.150/25) are connected to the exact same unmanaged Layer 2 switch with no router. What happens when Host X attempts to ping Host Y, and when Host Y attempts to ping Host X? (Select all that apply)",
                "options": [
                    {"id": "opt-a", "text": "Host X considers Host Y to be on its local subnet and transmits an ARP request directly for Host Y's MAC address."},
                    {"id": "opt-b", "text": "Host Y considers Host X to be outside its local subnet (since Host Y's /25 subnet covers only .128 to .255) and attempts to forward the reply to its default gateway."},
                    {"id": "opt-c", "text": "If Host Y has no default gateway configured, Host Y's ARP lookup for the gateway fails and the ping reply is never sent."},
                    {"id": "opt-d", "text": "The ping succeeds bidirectionally because both hosts are on the same physical switch."}
                ],
                "correctOptionIds": ["opt-a", "opt-b", "opt-c"],
                "explanation": "Under /24, Host X sees 192.168.1.150 as local and ARPs for Y directly. Y receives the ICMP request and prepares a reply to 192.168.1.50. But Y has a /25 mask (local range 192.168.1.128-255). Y calculates that 192.168.1.50 is REMOTE! Y tries to send the reply to its default gateway. If no gateway is configured, Y drops the reply. This asymmetric mask mismatch causes unidirectional reachability failure."
            },
            {
                "id": "q21",
                "type": "single_choice",
                "difficulty": "hard",
                "subtopic": "VLSM Design Allocation",
                "question": "An architect is subnetting 10.10.0.0/22. Department 1 requires 400 hosts, Department 2 requires 200 hosts, and Department 3 requires 100 hosts. Applying the VLSM rule of allocating from largest to smallest, what is the allocated subnet for Department 2?",
                "options": [
                    {"id": "opt-a", "text": "10.10.2.0/24"},
                    {"id": "opt-b", "text": "10.10.1.0/24"},
                    {"id": "opt-c", "text": "10.10.0.0/23"},
                    {"id": "opt-d", "text": "10.10.3.0/25"}
                ],
                "correctOptionIds": ["opt-a"],
                "explanation": "10.10.0.0/22 spans 10.10.0.0 to 10.10.3.255 (1024 addresses). Department 1 needs 400 hosts -> requires /23 (512 addresses: 10.10.0.0 to 10.10.1.255). The next available address is 10.10.2.0. Department 2 needs 200 hosts -> requires /24 (256 addresses: 10.10.2.0 to 10.10.2.255). Thus, Department 2 is allocated 10.10.2.0/24."
            },
            {
                "id": "q22",
                "type": "single_choice",
                "difficulty": "hard",
                "subtopic": "Overlapping Subnets",
                "question": "A network administrator attempts to configure two router interfaces: Interface 1 with 172.16.32.1/20, and Interface 2 with 172.16.40.1/22. Why does the router reject the configuration on Interface 2 with an 'Address overlap' error?",
                "options": [
                    {"id": "opt-a", "text": "The subnet 172.16.32.0/20 spans 172.16.32.0 to 172.16.47.255, completely encompassing the block 172.16.40.0/22 (172.16.40.0 to 172.16.43.255)."},
                    {"id": "opt-b", "text": "Both interfaces use the same port number."},
                    {"id": "opt-c", "text": "172.16.0.0 is a public Class B network that cannot be subnetted."},
                    {"id": "opt-d", "text": "Routers cannot have more than one interface configured."}
                ],
                "correctOptionIds": ["opt-a"],
                "explanation": "For /20, block size in octet 3 is 16: subnet spans 172.16.32.0 to 172.16.47.255. The /22 subnet spans 172.16.40.0 to 172.16.43.255. Because the /22 range is entirely contained within the /20 range, the router detects overlapping IP spaces and rejects the configuration."
            },
            {
                "id": "q23",
                "type": "multiple_choice",
                "difficulty": "hard",
                "subtopic": "RFC 1918 Boundary Analysis",
                "question": "Which of the following IP addresses fall STRICTLY INSIDE the RFC 1918 Class B private address space (172.16.0.0/12)? (Select all that apply)",
                "options": [
                    {"id": "opt-a", "text": "172.16.255.1"},
                    {"id": "opt-b", "text": "172.31.100.50"},
                    {"id": "opt-c", "text": "172.32.0.1"},
                    {"id": "opt-d", "text": "172.15.200.1"}
                ],
                "correctOptionIds": ["opt-a", "opt-b"],
                "explanation": "RFC 1918 defines the Class B private space as 172.16.0.0 through 172.31.255.255. Addresses 172.16.255.1 and 172.31.100.50 fall within this range. 172.15.200.1 (< 172.16) and 172.32.0.1 (> 172.31) are publicly routable Internet addresses!"
            },
            {
                "id": "q24",
                "type": "single_choice",
                "difficulty": "hard",
                "subtopic": "Longest Prefix Match",
                "question": "A core router possesses the following four routes in its forwarding table: 1) 10.0.0.0/8 via NextHop A; 2) 10.128.0.0/10 via NextHop B; 3) 10.130.0.0/16 via NextHop C; 4) 10.130.40.0/24 via NextHop D. When a packet arrives destined for 10.130.40.155, which NextHop is selected under standard IP routing rules?",
                "options": [
                    {"id": "opt-a", "text": "NextHop A (matches first)"},
                    {"id": "opt-b", "text": "NextHop B"},
                    {"id": "opt-c", "text": "NextHop C"},
                    {"id": "opt-d", "text": "NextHop D (Longest Prefix Match)"}
                ],
                "correctOptionIds": ["opt-d"],
                "explanation": "IP routing algorithms enforce the 'Longest Prefix Match' rule. The destination 10.130.40.155 matches all four routes (/8, /10, /16, and /24). The route with the longest prefix length (/24, NextHop D) is the most specific route and is strictly chosen."
            },
            {
                "id": "q25",
                "type": "multiple_choice",
                "difficulty": "hard",
                "subtopic": "Subnet Aggregation (Supernetting)",
                "question": "An ISP wants to summarize four contiguous /24 customer customer routes into a single BGP routing advertisement: 198.51.100.0/24, 198.51.101.0/24, 198.51.102.0/24, and 198.51.103.0/24. What single aggregated CIDR prefix accurately covers these four subnets without including any extra IP addresses? (Select all that apply)",
                "options": [
                    {"id": "opt-a", "text": "198.51.100.0/22"},
                    {"id": "opt-b", "text": "Subnet mask 255.255.252.0"},
                    {"id": "opt-c", "text": "198.51.100.0/23"},
                    {"id": "opt-d", "text": "198.51.96.0/20"}
                ],
                "correctOptionIds": ["opt-a", "opt-b"],
                "explanation": "Four /24s equal 4 * 256 = 1024 addresses (2^10). Host bits H = 10, so network bits N = 32 - 10 = 22. In the 3rd octet, the numbers are 100 (01100100), 101 (01100101), 102 (01100110), 103 (01100111). The first 6 bits of the 3rd octet match (011001xx), giving a /22 prefix: 198.51.100.0/22. The subnet mask for /22 is 255.255.252.0."
            }
        ]
    }
}
