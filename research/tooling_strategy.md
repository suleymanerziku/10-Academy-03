# Purpose

MCP tools exist to make development safer, clearer, and human-centered. Their purpose is threefold:

- Help humans develop safely: MCP tools provide guarded automation, reproducible workflows, and policy checks that reduce the risk of accidental or unsafe changes. They surface suggestions, validations, and audit trails so human engineers remain in control while benefiting from high-quality assistance.

- Give IDE agents context (not authority): Tooling feeds IDE-integrated agents with project state, tests, and constraints so agents can make useful proposals. This context improves suggestions and reduces mistakes, but it never grants agents autonomous control—humans review and authorize all meaningful decisions.

- Never expose to runtime agents: Tooling and developer-facing MCP interfaces run in development/CI contexts and must never be reachable by runtime or production agents. This separation prevents escalation, protects secrets and environments, and keeps development-time automation from affecting running systems without explicit human oversight.

These principles keep tooling powerful and useful while preserving human responsibility and system safety.