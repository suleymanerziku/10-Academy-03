# Chimera Agent Skills

## Purpose

This directory defines the **runtime skills** available to Chimera agents.

A **Skill** is a **specific capability package** that an agent may invoke to perform an action or retrieve information. Skills represent the **only allowed way** for agents to interact with the outside world or perform non-trivial operations.

Agents **do not** execute arbitrary code.  
Agents **only** act through approved skills.

---

## What Is a Skill?

A Skill:
- Encapsulates **one clear capability**
- Has an explicit **Input → Output contract**
- Declares expected side effects and costs
- Is invoked **via the orchestrator**, never directly by another agent
- Contains no hidden state or implicit behavior

A Skill is **not**:
- A prompt
- A workflow
- A long-running autonomous loop

---

## Skill Governance Rules

All skills must comply with the following rules:

1. Skills must define clear input and output schemas
2. Skills must be deterministic where possible
3. Skills must declare costs or resource usage if applicable
4. Skills must not persist data directly
5. All external effects must go through MCP-managed interfaces
6. Skills may be disabled or rate-limited by the orchestrator

---

## Skill Catalog

### 1. skill_fetch_trends

**Description**  
Fetch platform-specific trend signals (topics, hashtags, formats) to inform content generation.

This skill provides **context**, not decisions.

**Input Contract**
```json
{
  "platform": "string",
  "region": "string",
  "limit": "number"
}
```

(See <attachments> above for file contents. You may not need to search or read the file again.)


**Output Contract**
```json
{
  "trends": [
    {
      "topic": "string",
      "confidence": "number"
    }
  ],
  "source": "string",
  "retrieved_at": "ISO-8601"
}


```


Notes
- Read-only skill
- No content generation
- No persistence

### 2. skill_generate_video_metadata

**Description**
Generate structured metadata for short-form video content based on an objective and contextual inputs.

This skill produces data, not media.

**Input Contract**
```json
{
  "objective": "string",
  "platform": "string",
  "trend_context": "object",
  "constraints": {
    "max_length": "number",
    "tone": "string"
  }
}
```

**Output Contract**
```json
{
  "caption": "string",
  "hashtags": ["string"],
  "estimated_cost_usd": "number",
  "confidence": "number"
}
```

**Notes**
- Must include a cost estimate
- Output is subject to Judge validation
- No publishing or persistence

### 3. skill_publish_status

**Description**
Publish Chimera’s operational status or availability to external agent networks (e.g., OpenClaw).

This is a one-way, read-only communication skill.

**Input Contract**
```json
{
  "status": "active | idle | paused",
  "capabilities": ["string"]
}
```

**Output Contract**
```json
{
  "acknowledged": true,
  "published_at": "ISO-8601"
}
```

**Notes**
- No inbound commands are accepted
- No credentials exposed
- Rate-limited by the orchestrator