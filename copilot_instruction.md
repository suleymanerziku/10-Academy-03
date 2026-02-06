## Copilot Instructions


**Guidelines**

- Project Context
This is Project Chimera, an autonomous influencer system designed for safe, auditable, and economically governed agent autonomy.

- Prime Directive (Non-Negotiable)
NEVER generate code without first checking the specs/ directory.
Specifications are executable contracts. If a requirement is missing, unclear, or contradictory:
- STOP
- Ask for clarification
- Or request a spec update
Do not guess or invent behavior.

**Traceability Requirement**
- Before writing any code, explain your plan.
The explanation must include:
- Which specs/ file(s) are being referenced
- What behavior will be implemented
- Why the implementation satisfies the specification
- Only after this explanation may code be produced.

Be concise and actionable. Prioritize minimal, correct changes over broad refactors.
Follow the project’s existing style, structure, and architectural boundaries.
When changing specs or contract documents under specs/, preserve intent and ask clarifying questions if changes may alter requirements.
NEVER introduce or approve content that facilitates wrongdoing, abuse, unsafe autonomy, or uncontrolled external access.

**Do NOT introduce:**
- Direct agent-to-agent communication
- Direct third-party API calls (all external access must go through MCP)
- Hidden background loops or unsupervised autonomy

Use the repository’s TODO tracking (manage_todo_list) for multi-step changes and update task status as work progresses.

When referring to files in responses, present workspace-relative paths where supported.

**Commit and Test**
- Run unit tests (if present) after edits when feasible.
- Keep commits focused, scoped, and descriptive.
- Do not bundle specification changes with implementation unless explicitly instructed.

**Communication**

Provide a brief, structured preamble before making edits that may affect multiple files.

**After edits, provide:**
- A concise progress summary
- Any assumptions made
- A suggested next step
- Clarity and correctness take precedence over speed.

**Contact**

If specifications are insufficient or conflicting, request clarification from the repository owner or open an issue before proceeding.

**Acknowledgement**

By operating in this repository, you acknowledge that:
- Specifications define reality
- Autonomy is earned through constraints
- Traceability is mandatory