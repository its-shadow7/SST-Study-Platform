# Introduction to Computer Networks & Network Core
**Term:** Term 3 | **Subject:** CN | **Note ID:** `cn-lecture-01-introduction`
**Last Updated:** 2026-10-07T10:00:00Z

## Abstract & Summary
Foundational overview of computer networks, examining network infrastructure, edge versus core devices, packet transmission dynamics, and latency components.

## Learning Objectives
- Understand the difference between the network edge and network core.
- Explain packet switching vs circuit switching and multiplexing techniques.
- Comprehend delays in packet-switched networks: processing, queuing, transmission, and propagation.

## Key Takeaways
- The Internet is a network of networks governed by open RFC protocols.
- Packet switching achieves statistical multiplexing, utilizing bandwidth dynamically compared to circuit switching.
- Total nodal delay = d_proc + d_queue + d_trans + d_prop.

---

## 1. What is the Internet?
The Internet is a globally interconnected system of computing devices (**hosts** or **end systems**) communicating through transmission links and packet switches (routers and link-layer switches).

End systems access the Internet through **Internet Service Providers (ISPs)**, forming a multi-tier hierarchical topology consisting of Tier-1 access providers, regional networks, and local access networks.

All network communication is governed by protocols. A **protocol** defines the format and the order of messages exchanged between two or more communicating entities, as well as the actions taken on the transmission and/or receipt of a message.

**Citations & References:**
- Kurose & Ross, Computer Networking: A Top-Down Approach (8th Ed), Chapter 1

---

## 2. Network Core: Circuit vs Packet Switching
The network core consists of the mesh of interconnected routers. How does data travel across this core?

### Circuit Switching
- Dedicated resource reservation per session (traditional telephone networks).
- Guaranteed performance, but idle resources are wasted.

### Packet Switching
- Messages are divided into discrete chunks called **packets** of length $L$ bits.
- Packets travel through communication links at transmission rate $R$ bps.
- Uses **Store-and-Forward** transmission: the packet switch must receive the entire packet before it can begin transmitting the first bit onto the outbound link.

```text
[Host A] ---> (Router 1) ---> (Router 2) ---> [Host B]
             L bits / R bps
```

**Citations & References:**
- Scaler School of Technology - Computer Networks Lecture 1

---

## 3. Four Sources of Packet Delay
When a packet traverses a path from source to destination, it experiences four major components of nodal delay:

1. **Nodal Processing Delay ($d_{proc}$)**: Time required to inspect packet headers, check bit-level errors, and determine the output link.
2. **Queuing Delay ($d_{queue}$)**: Time spent waiting in line to be transmitted on the link. Depends on network congestion.
3. **Transmission Delay ($d_{trans}$)**: Time required to push all packet bits onto the link:
   $$d_{trans} = \frac{L}{R}$$
   where $L$ is packet length (bits) and $R$ is link transmission rate (bps).
4. **Propagation Delay ($d_{prop}$)**: Time needed for a bit to propagate from router to router at the speed of light in the physical medium ($s$):
   $$d_{prop} = \frac{d}{s}$$

$$\text{Total Nodal Delay} = d_{proc} + d_{queue} + d_{trans} + d_{prop}$$

**Citations & References:**
- RFC 2544 - Benchmarking Methodology for Network Interconnect Devices

---