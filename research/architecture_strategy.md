# Domain Architecture Strategy

## Purpose

This document translates **research insights and SRS intent** into a concrete architectural direction for Project Chimera. It answers *how* the system should be structured, *why* specific patterns are chosen, and *where* humans, agents, and infrastructure interact.

This is a **pre-code artifact**. No implementation decisions should contradict this document.



## 1. Architectural Goals
From the Chimera SRS, the architecture must:

1. Support **thousands of autonomous influencer agents** concurrently
2. Enable **goal-directed autonomy**, not scripted automation
3. Enforce **governance, safety, and budget control**
4. Decouple agent cognition from external platforms
5. Allow a **single human operator** to manage the system (Management by Exception)

These goals eliminate monolithic-agent and ad-hoc prompt architectures.



## 2. Chosen Agent Pattern

### 2.1 Pattern Selected: **Hierarchical Swarm (Planner–Worker–Judge)**

#### Why This Pattern

| Requirement     | Reason Planner–Worker–Judge Fits      |
| --------------- | ------------------------------------- |
| Scalability     | Workers scale horizontally, stateless |
| Quality Control | Judges enforce acceptance criteria    |
| Adaptability    | Planners dynamically re-plan          |
| Fault Isolation | Worker failure does not cascade       |
| Governance      | Judge is a natural safety gate        |

This pattern directly aligns with:

* FastRender Swarm Architecture
* Management-by-exception philosophy
* Real-world constraints of LLM unreliability

#### Rejected Patterns

* **Single Autonomous Agent** – brittle, ungovernable
* **Sequential Chain-of-Thought Pipelines** – low parallelism
* **Peer-to-Peer Agent Mesh** – high coordination complexity



## 3. High-Level System Topology

### 3.1 Hub-and-Spoke Model

* **Central Orchestrator (Hub)**

  * Maintains global state
  * Enforces policy and budgets
  * Hosts dashboard and HITL queues

* **Agent Swarms (Spokes)**

  * Planner service
  * Worker pool
  * Judge service

All external interactions flow **only through MCP servers**.

![alt text](image.png)



## 4. Human-in-the-Loop (HITL) Strategy

### 4.1 HITL Insertion Points

Humans do **not** approve everything. They intervene only when:

1. Judge confidence score is below threshold
2. Content is flagged as sensitive (politics, health, finance)
3. Financial actions exceed budget norms

### 4.2 HITL Flow

![alt text](image-1.png)

This preserves velocity while maintaining accountability.



## 5. Data Architecture Decisions

### 5.1 Storage Types and Rationale

| Data Type               | Storage              | Rationale                        |
| ----------------------- | -------------------- | -------------------------------- |
| Agent memory (semantic) | Weaviate (Vector DB) | Long-term recall, RAG            |
| Tasks & state           | PostgreSQL           | Strong consistency, audit trails |
| Short-term context      | Redis                | Low latency, ephemeral           |
| Financial ledger        | Blockchain           | Immutable, auditable             |

### 5.2 Why Not a Single Database

* Mixing semantic and transactional data creates scaling conflicts
* Vector search requires different indexing strategies
* Financial data demands immutability

Separation enforces correctness.


## Regarding storing video metadata
Chimera agents generate and process **large volumes of video-related metadata**, including:

- Video IDs, platforms, formats
- Generation timestamps
- Agent ID / persona ID
- Content attributes (hashtags, captions, topics)
- Engagement metrics (views, likes, shares)
- Processing status (draft, published, archived)
- Cost and resource attribution

Characteristics:
- **Write-heavy** during content bursts
- **Append-first** lifecycle
- **Query-heavy** for analytics, dashboards, and governance
- Requires **auditability and traceability**


## Option A: NoSQL (Document / Key-Value Stores)

### Strengths
- High write throughput
- Flexible schemas
- Easy horizontal scaling

### Weaknesses (Critical for Chimera)
- Weak or eventual consistency
- Poor support for:
  - Cross-agent joins
  - Temporal analytics
  - Auditing & compliance queries
- Schema drift risk (dangerous for agent-built systems)
- Harder to enforce invariants (e.g., one wallet ↔ many videos)

### Assessment
NoSQL is optimized for **unstructured content blobs**, not governed agent output.

**Risk:** Agents may silently diverge data structures over time.



## Option B: SQL (Relational Database)

### Strengths
- Strong consistency guarantees
- Explicit schemas = executable contracts
- Excellent support for:
  - Time-series queries
  - Aggregations
  - Auditing and rollback
- Natural fit for:
  - Governance
  - Budget attribution
  - HITL review trails

### Performance Considerations
Modern SQL databases (PostgreSQL) support:
- High insert rates (partitioning, batching)
- JSONB for semi-structured fields
- Time-based partitioning for scale
- Read replicas for analytics

### Assessment
SQL aligns with **Spec-Driven Development** and **agent governance**.


## Decision: Use SQL

### Rationale
| Requirement | SQL Fit |
|-----------|--------|
| High-velocity writes | Partitioned inserts |
| Agent traceability | Foreign keys + constraints |
| Governance & audits | ACID + history tables |
| Analytics | Native aggregations |
| Schema enforcement | Prevents agent drift |

We intentionally **trade schema rigidity for correctness**.



## 6. Inter-Agent & External Communication

### 6.1 Internal Communication

* Agents **do not message each other directly**
* All coordination flows through:

  * Task queues
  * Global state
  * Planner decisions

This avoids emergent chaos.

### 6.2 External Communication

* All external systems accessed via **MCP Servers**
* Agents are unaware of:

  * API keys
  * Platform quirks
  * Vendor-specific logic

This enables hot-swapping platforms without rewriting agent logic.



## 7. Security & Governance Considerations

### 7.1 Key Principles

* Least privilege per agent
* No direct API credentials inside agent logic
* Budget enforcement before action execution

### 7.2 Governance Layers

| Layer        | Responsibility          |
| ------------ | ----------------------- |
| Specs        | Define allowed behavior |
| Tests        | Enforce contracts       |
| Judge Agents | Runtime enforcement     |
| CI/CD        | Prevent bad merges      |
| HITL         | Final human authority   |



## 8. Architectural Risks & Mitigations

| Risk                 | Mitigation                  |
| -------------------- | --------------------------- |
| Agent drift          | Centralized persona + specs |
| Cost runaway         | CFO Judge + budgets         |
| Platform API changes | MCP abstraction             |
| LLM hallucination    | TDD + Judge validation      |
| Human overload       | Management by exception     |



## 9. Conclusion

This architecture positions Project Chimera as:

* A **governed agent factory**, not a prompt system
* Compatible with emerging **agent social networks**
* Scalable by design, safe by default

With this strategy locked, implementation can proceed **without ambiguity**.

