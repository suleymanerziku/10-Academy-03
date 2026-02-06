# Technical Specification

## Architecture

Project Chimera follows a Hierarchical Swarm Architecture composed of:

- Central Orchestrator – owns global state, policy, and coordination

- Planner Agents – decompose objectives into tasks

- Worker Agents – perform constrained execution

- Judge Agents – validate outputs and enforce governance

All external interactions are mediated through MCP (Model Context Protocol) servers. Agents are never aware of vendor APIs or credentials.

## API and Data Models

- API endpoints
### System & Orchestrator APIs
**System Status**

`GET /system/status`

**Purpose**
- Expose high-level operational state
- Used by dashboards, HITL, and optional OpenClaw publishing

**Response**

```
{
  "system": "chimera",
  "status": "active | paused | degraded",
  "active_agents": 42,
  "pending_tasks": 128,
  "last_updated": "ISO-8601"
}
```

**Called by**
- Human operators
- External read-only integrations

**Submit Campaign Objective**

`POST /campaigns`

**Purpose**
- Entry point for human intent
- Triggers Planner agent execution

**Request**
```
{
  "objective": "Grow TikTok presence in fitness niche",
  "constraints": {
    "platform": "tiktok",
    "budget_usd": 50,
    "time_horizon_days": 7
  }
}
```


**Response**
```
{
  "campaign_id": "uuid",
  "status": "accepted"
}
```

**Called by**
- Human operator only

### Planner Agent APIs
**Generate Tasks**
`POST /planner/tasks`

**Purpose**
- Planner submits decomposed tasks to orchestrator

**Request**
```
{
  "campaign_id": "uuid",
  "tasks": [
    {
      "task_id": "uuid",
      "objective": "Generate caption + hashtags",
      "constraints": {
        "platform": "tiktok",
        "budget_usd": 2.5
      }
    }
  ]
}

```
**Response**
```
{
  "accepted_tasks": ["uuid"],
  "rejected_tasks": []
}
```

**Called by**
- Planner agent only

### Worker Agent APIs
**Fetch Assigned Task**
`GET /workers/tasks/next`

*Purpose*
- Pull-based task acquisition (prevents chaos)

*Response*
```
{
  "task_id": "uuid",
  "objective": "Generate video metadata",
  "constraints": {
    "platform": "tiktok",
    "budget_usd": 2.5
  }
}
```

**Called by**
- Worker agents

**Submit Task Result**
`POST /workers/tasks/{task_id}/result`

**Purpose**
- Submit execution output for judgment

**Request**
```
{
  "result": {
    "caption": "string",
    "hashtags": ["string"],
    "estimated_cost_usd": 1.8
  },
  "confidence": 0.87
}
```


**Response**

{
  "status": "received"
}


**Called by**
- Worker agents only

### Judge Agent APIs
**Evaluate Output**
`POST /judge/evaluations`

**Purpose**
- Judge submits approval decision

**Request**
```
{
  "task_id": "uuid",
  "decision": "approve | reject | escalate",
  "reason": "string",
  "confidence": 0.92
}

```
**Response**

{
  "status": "recorded"
}


**Called by**
- Judge agents only

### Human-in-the-Loop (HITL) APIs
**Fetch Escalations**
`GET /hitl/escalations`

**Purpose**
- Show only items requiring human review

**Response**
```
[
  {
    "task_id": "uuid",
    "reason": "Low confidence score",
    "submitted_at": "ISO-8601"
  }
]
```
**Resolve Escalation**
`POST /hitl/escalations/{task_id}/resolve`

**Purpose**
- Human approves or rejects escalated output

**Request**
```
{
  "decision": "approve | reject",
  "notes": "string"
}
```

### Video Metadata APIs (Read-Only for Agents)
**List Video Metadata**
`GET /videos`

**Purpose**
- Analytics, dashboards, audits

**Query Params**
- platform
- status
- agent_id
- from, to

**Get Video Metadata by ID**
`GET /videos/{video_id}`

**Purpose**
- Traceability and audit

### MCP Integration APIs (Outbound Only)
**MCP Tool Invocation (Internal)**
`POST /mcp/invoke`

**Purpose**
- Orchestrator → MCP server bridge
- Agents never call this directly

**Request**
```
{
  "tool": "fetch_trends",
  "payload": {
    "platform": "tiktok"
  }
}
```
- Data Model: Video Metadata 

Database Type: SQL (PostgreSQL)

Entity: VideoMetadata

- id (UUID, primary key)
- agent_id (UUID, foreign key) 
- platform (TEXT)
- caption (TEXT)
- hashtags (TEXT[])
- status (draft | approved | published | rejected)
- engagement (JSONB)
- estimated_cost_usd (NUMERIC)
- created_at (TIMESTAMP)
- published_at (TIMESTAMP, nullable)

Rules:
- Append-only records
- No hard deletes
- All state transitions are explicit and auditable

## Implementation Details

- Language: Python 3.12
- Dependency Management: uv
- Validation: Judge agents + test suites
- Integration: MCP servers only
Deployment targets and CI/CD pipelines are defined in later stages.

## Non-functional Requirements

**Performance**
- Support high write throughput for video metadata
- Horizontal scalability for worker agents

**Security**
- Least-privilege agent execution
- No embedded API credentials
- One-way external status publication only

**Observability**
- Structured logs for all agent actions
- Deterministic replay of decisions
- Clear escalation signals for HITL