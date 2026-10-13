# Packet Switching & Layered Architecture (OSI / TCP/IP)
**Term:** Term 3 | **Subject:** CN | **Note ID:** `cn-lecture-02-packet-switching`
**Last Updated:** 2026-10-07T10:15:00Z

## Abstract & Summary
Covers the modular layered architecture of computer networking protocols, protocol data units (PDU), header overhead, and end-to-end transmission dynamics.

## Learning Objectives
- Differentiate the 5-layer Internet protocol stack from the 7-layer OSI model.
- Understand protocol encapsulation and decapsulation with headers at each tier.
- Analyze packet loss, buffer overflow, and throughput metrics.

## Key Takeaways
- Layering provides modularity, clean abstraction, and independent protocol evolution.
- The 5-layer Internet stack consists of Application, Transport, Network, Link, and Physical layers.
- Data encapsulation wraps application messages into segments, packets, frames, and raw bits.

---

## 1. Why Layering?
Complex systems like the global Internet are organized hierarchically through **layering**. Each layer provides a well-defined service to the layer above it by utilizing services from the layer below.

### The 5-Layer Internet Protocol Stack
- **Application Layer**: Supports networked applications (HTTP, SMTP, DNS). Unit: *Message*.
- **Transport Layer**: Host-to-host process data transfer (TCP, UDP). Unit: *Segment*.
- **Network Layer**: Routing datagrams from source to destination (IP, ICMP, BGP). Unit: *Datagram / Packet*.
- **Link Layer**: Data transfer between neighboring network elements (Ethernet, Wi-Fi). Unit: *Frame*.
- **Physical Layer**: Carries individual bits across the physical medium (Copper, Fiber, Radio waves).

**Citations & References:**
- Kurose & Ross (8th Ed), Section 1.5

---

## 2. Protocol Encapsulation
As application data travels down the protocol stack at the transmitting end-system:

1. **Application**: `[ Message ]`
2. **Transport**: `[ TCP Header | Message ]` (Segment)
3. **Network**: `[ IP Header | TCP Header | Message ]` (Datagram)
4. **Link**: `[ Frame Header | IP Header | TCP Header | Message | Frame Trailer ]` (Frame)

At the receiving side, routers inspect only up to Layer 3, switches inspect Layer 2, and the destination host decapsulates the message up to Layer 5.

**Citations & References:**
- RFC 1122 - Requirements for Internet Hosts -- Communication Layers

---