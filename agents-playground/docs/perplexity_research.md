# Enterprise AI Agents in 2026 – Single-File Practical Brief

## 1. Design: Autonomy, Oversight, and Agent Roles

### 1.1 Autonomy Within Guardrails

For 2026, enterprises that are not getting burned are converging on **three explicit autonomy tiers** instead of “let the agent figure it out”:

1. **Tier 1 – Routine, auto-execute**
   - Read-only or low-risk writes (e.g., drafting responses, generating summaries, enriching tickets).
   - Agent can **decide and execute** without human approval, but must:
     - Log every action.
     - Be bounded to specific tools/data scopes.

2. **Tier 2 – Elevated, single-approval**
   - Actions that change state or have financial/compliance implications (e.g., updating issue status in Jira/Azure DevOps, minor config changes, sending emails to customers).
   - Agent prepares an **action proposal**:
     - What it wants to do.
     - Why.
     - What data it used.
   - Human gives **one-click approve/reject**.

3. **Tier 3 – Critical, decision-support only**
   - Anything that can delete data, move money, commit code to protected branches, or implicate regulated data.
   - Agent only:
     - Surfaces options, pros/cons, diffs.
     - Suggests next steps.
   - Human decides and executes via normal systems.

**Design rule:**
Every tool/endpoint the agent can call must be labeled with a **Tier (1/2/3)** and have matching UI/UX affordances (auto-exec vs “proposed action” queue vs “read-only analysis”).

For your **O’Reilly Agent MVP**:

- LangGraph pipeline and CrewAI flows should:
  - Treat **GitHub issue ingestion and triage** as Tier 1.
  - Treat **branch creation / PR suggestions** as Tier 2.
  - Treat **direct main-branch commits, infra changes** as Tier 3 (no agent writes).

***

### 1.2 Agent Role Design & Collaboration

Pragmatic pattern: **“Orchestrator + Specialists”**, not “a swarm of peers”.

- **Orchestrator (Conductor / PM agent)**
  - Manages workflow state (LangGraph fits perfectly here).
  - Decides **which specialist to call next** based on current graph node and state.
  - Enforces **approval tiers** and routes to humans when needed.

- **Specialists**
  - Examples tuned to your MVP:
    - **PM agent** – clarifies requirements, reforms GitHub issues into structured spec.
    - **Dev agent** – reads codebase (via MCP tools), proposes patches/diffs.
    - **QA agent** – generates tests, simulates scenarios, checks acceptance criteria.
  - Each specialist:
    - Has **narrow scope** (tools + domains).
    - Owns **one slice** of the pipeline.
    - Is easier to test and monitor.

For CrewAI, mirror this via **roles + tasks** with clear boundaries instead of “everyone can call everything”.

***

### 1.3 Context, Memory, and RAG

Avoid magical “long-term memory”. Use **three explicit memory tiers**:

1. **Ephemeral / Turn-level**
   - Conversation-in-progress, current file, current issue.
   - Implemented via LangGraph state, short-lived context, or in-memory store.
   - TTL: minutes–hours.

2. **Session / Task-level**
   - For a user’s current work session or a single feature/epic.
   - Store:
     - Decisions made.
     - Links to issues, PRs, specs.
   - TTL: hours–days (e.g., 24–72h in Redis/Postgres).

3. **Organizational / Knowledge-level**
   - Product docs, runbooks, coding standards, system diagrams.
   - Stored in **RAG vector index** (Pinecone/pgvector/Weaviate/Azure AI Search).
   - Versioned like code and docs.

**Key design constraints:**

- **Never** store:
  - Tokens of entire conversations in perpetuity without data retention policy.
  - Raw PII or secrets in vector DBs.
- For your MVP:
  - Push Azure architecture docs, debugging guides, MCP quick refs into a **RAG index**.
  - Have PM/Dev/QA agents always ground answers via RAG, not pure model knowledge.

***

### 1.4 Tooling & MCP Design

Treat tools as **capabilities with contracts**, not arbitrary callouts:

- Each tool:
  - Has a **typed schema** (JSON schema) and **explicit side effects**.
  - Is documented with:
    - Inputs.
    - Outputs.
    - Tier (1–3).
    - Owner.
- Prefer **MCP-based tools** for:
  - Consistency across orchestrators (LangGraph, CrewAI, VS Code, browser agents).
  - Easier future integration with IDE/CLI/browsers.

For your **FastMCP server + Inspector**:

- Codify tools for:
  - GitHub issues (read/write).
  - Repo browsing (read-only).
  - Test execution (read-only, but high-risk if commands are arbitrary).
- Tag each with a Tier and a **max frequency / rate limit**.

***

### Design – Immediate Actions

1. Define **Tier 1/2/3** autonomy for your demo pipeline (PM/Dev/QA + tools).
2. Write a **1-page spec** per agent:
   - Inputs, outputs, tools, autonomy level, failure modes.
3. List all tools (MCP + non-MCP) and assign **Tier + owner**.

### Design – If You Have More Time

1. Introduce a **“proposal” object** format for Tier 2/3 actions (common schema across agents).
2. Add **RAG-backed knowledge** for your docs and runbooks, and require agents to cite sources.
3. Define a **global “decision space”** document: what agents may *never* do (e.g., delete production data).

***

## 2. Architecture: Frameworks and 2026 Readiness

### 2.1 Orchestration Framework Comparison (2026 Snapshot)

**Scoring scale (relative, opinionated):**
1–5 where **5 = strong** / production-ready.

| Platform                             | Maturity | Guardrails / Policy | Ecosystem & Integrations | Observability | TCO / Lock-in | Notes |
|--------------------------------------|----------|----------------------|---------------------------|--------------|---------------|------|
| **LangGraph (LangChain stack)**      | 5        | 3 (BYO)             | 5 (Python, JS, tools)    | 4 (LangSmith) | 5 (low lock-in) | Best general-purpose orchestrator for 2026; explicit graphs, great for teaching and prod. |
| **CrewAI**                           | 4        | 2 (BYO)             | 3                        | 2            | 5             | Fast to prototype multi-agent flows; less opinionated on safety/observability. |
| **Azure Agent Framework**            | 4        | 5                   | 5 (M365, DevOps, data)   | 4            | 2 (Azure lock-in) | Strong when you live in Azure; top-tier security story. |
| **AWS Agents for Bedrock**           | 4        | 4                   | 5 (AWS services)         | 3            | 2             | Great serverless integration and model router; policies improving quickly. |
| **Google Vertex AI Agents**          | 3        | 4                   | 4 (GCP services)         | 3            | 2             | Strong in multimodal and search; still maturing as an “agent” story. |
| **Salesforce Einstein / Agents**     | 3        | 4                   | 5 (CRM/Service Cloud)    | 3            | 2             | Ideal when your whole world is CRM/Service; not general-purpose. |
| **NVIDIA NeMo / microservices**      | 3        | 2 (BYO)             | 4 (GPU, RAG, vector)     | 3            | 3             | Great for GPU-first shops & custom models; heavier infra. |
| **Meta Llama Stack (open)**          | 3        | 2 (BYO)             | 4 (OSS ecosystem)        | 2            | 5             | Excellent for open-source / self-hosted, but you assemble everything. |

**Opinionated guidance for your use case:**

- **Teaching / O’Reilly Agent MVP:**
  - Primary: **LangGraph**, because:
    - State machine model is explicit and inspectable.
    - Pairs well with LangSmith-type tooling.
  - Alternate path: **CrewAI** for “minimal code to multi-agent”.

- **Enterprise “we’re all-in on one cloud” patterns:**
  - Azure-heavy shops: **Azure Agent Framework** + Azure AI Studio.
  - AWS-heavy shops: **Bedrock Agents** for serverless-first flows.
  - GCP: **Vertex AI Agents** plus Vertex Search & Conversation.

***

### 2.2 Macro Architecture for Enterprise Agents

A pragmatic **reference architecture**:

- **Edge / Channels**
  - CLI, Web UI, Slack/Teams, IDE, GitHub apps.

- **Orchestration Layer**
  - **LangGraph** graph:
    - Nodes: PM/Dev/QA agents + supervisor + human-review nodes.
    - Edges: transitions based on state (requirements_ready, code_gen_done, tests_passed, etc.).
  - Optional: **CrewAI** flows for simpler linear multi-agent runs.

- **Model Gateway Layer**
  - Abstraction over:
    - OpenAI / Azure OpenAI.
    - Claude.
    - Gemini.
    - Open models (Llama variants).
  - Implement with:
    - LangChain LLM abstraction, or
    - A gateway (custom), or
    - Cloud-native routing (Bedrock, Vertex).

- **Tooling / MCP Layer**
  - FastMCP server exposing:
    - GitHub (issues, PRs).
    - File system (repo, docs).
    - CI (test runs).
    - Monitoring APIs.
  - MCP Inspector used for demos & debugging.

- **Data / RAG Layer**
  - Vector DB (Pinecone, pgvector, Weaviate, Azure AI Search).
  - Metadata store (Postgres).
  - Indexes:
    - Architecture docs, runbooks, standards, prior incidents.

- **Safety & Policy Layer**
  - Content safety (Azure AI Content Safety, Bedrock Guardrails, or equivalent).
  - Authorization (OPA/Rego or cloud RBAC).
  - DLP (Presidio or vendor-native).
  - Audit trail (Postgres + object store).

- **Observability Layer**
  - Traces (LangSmith-like tracing/telemetry).
  - Metrics & logs (Datadog/Prometheus + ELK/Splunk).
  - Evaluation dashboards (LangSmith, Weights & Biases).

***

### Architecture – Immediate Actions

1. **Choose primary orchestration**:
   - Default: **LangGraph** for the pipeline (keep CrewAI as optional alt-path demo).
2. Sketch a **high-level box diagram**:
   - Channels → Orchestrator → Model gateway → Tools/MCP → Data/RAG → Safety/Observability.
3. Decide on a **vector DB** (Pinecone or pgvector are safe defaults).

### Architecture – If You Have More Time

1. Introduce a **model gateway pattern** so you can swap model vendors with config only.
2. Define **separate graphs** for:
   - Issue triage.
   - Code generation.
   - QA/test creation.
   And then compose them.
3. Capture this as a **reference Azure architecture diagram** that mirrors your docs.

***

## 3. Implementation: Stack, Vendors, and Patterns

### 3.1 Recommended Implementation Stack

**Language & runtimes (you’re there already):**

- **Python** for LangGraph / orchestration.
- Node/TypeScript for MCP servers if you prefer, but FastMCP + Python is fine.

**Core layers:**

- **Orchestration:** LangGraph.
- **Alternate flows / teaching:** CrewAI.
- **Tools:** FastMCP tools for:
  - GitHub.
  - Local repo.
  - CI/test runner.
  - File watcher (to feed issues/events).
- **RAG:**
  - Use **Pinecone** if you want managed, or **Postgres + pgvector** if you want low-cost, familiar operations.
- **Prompt & workflow versioning:**
  - Store prompts and graph configs in **git** along with code.
  - Use structured prompt templates with clear variables; name them and version them semantically (`pm_triage_v3`, etc.).
- **Observability:**
  - Application-level tracing + eval (LangSmith-style).
  - Infra metrics/logs (Datadog or Prometheus + Grafana).

***

### 3.2 Toolbox Matrix (Opinionated Defaults)

**Observability**

| Category      | Primary Choice         | Why                          |
|---------------|------------------------|-------------------------------|
| Traces/Evals  | LangSmith-style tool   | LLM-native tracing & eval.   |
| Metrics/APM   | Datadog                | Mature, easy dashboards.     |
| Logs/SIEM     | ELK or Splunk          | Standard enterprise log stack.|

**Governance & Security**

| Category            | Primary Choice                        |
|---------------------|----------------------------------------|
| Content Safety      | Azure AI Content Safety / Bedrock Guardrails |
| Policy Engine       | OPA/Rego (multi-cloud)                |
| Identity & RBAC     | Azure Entra ID / AWS IAM / GCP IAM    |
| DLP / PII           | Presidio (if DIY) or cloud-native     |
| Compliance Mapping  | NIST AI RMF + ISO 42001 checklists    |

**Evaluation & Testing**

| Category       | Primary Choice           |
|----------------|-------------------------|
| Scenario evals | LangSmith-like eval     |
| Experiment mgmt| Weights & Biases (Weave)|
| Unit testing   | pytest + custom harness |

**Deployment & Runtime**

| Category        | Primary Choice                    |
|-----------------|-----------------------------------|
| Runtime         | Kubernetes or managed containers  |
| CI/CD           | GitHub Actions / Azure DevOps     |
| Blue/Green/Canary | Built-in in K8s / cloud LB      |

**Incident Response**

| Category          | Primary Choice        |
|-------------------|-----------------------|
| On-call management| PagerDuty / Opsgenie  |
| Notifications     | Slack / Teams channels|
| Runbooks          | Markdown in repo + Wiki |

***

### Implementation – Immediate Actions

1. Lock in:
   - **LangGraph** as orchestrator.
   - **One vector DB** (Pinecone or pgvector).
   - **One tracing solution** (LangSmith-like).
2. Put prompts and graph configs under **version control** with semantic names.
3. Implement a **first RAG index** for your docs (architecture, MCP tools, debugging guides).

### Implementation – If You Have More Time

1. Introduce a **semantic cache** (Redis or vendor caching) to cut LLM costs.
2. Create a **model routing layer** (cheap vs expensive models).
3. Add **feature flags** for enabling/disabling tools and agents without code changes.

***

## 4. Security: Controls, Guardrails, and Compliance

### 4.1 Threat Themes (2026)

The same patterns keep biting teams:

- Prompt injection → RAG or tool misuse.
- Over-privileged agents → unauthorized data access.
- Hallucinations presented as facts → business or legal decisions on bad data.
- Cost explosions due to loops/bad routing.
- Evolving regulation (EU AI Act, sectoral rules).

Mitigation is **layered**, not “just add a safety API”.

***

### 4.2 Practical Control Stack

**Layer 1 – Prompt & Tool Guardrails**

- Content safety:
  - Azure AI Content Safety or AWS Bedrock Guardrails.
- Strict tool schemas:
  - Validate inputs before executing tools (types, ranges, whitelists).
- Prompt hardening:
  - Explicit “tool use rules”.
  - Clear separation of:
    - System instructions.
    - Tool descriptions.
    - User input.
    - Retrieved context.

**Layer 2 – Authorization & Policy**

- **Principle of Least Privilege**:
  - Each agent has **separate identity** and tool scopes.
- **Policy engine (OPA/Rego)** between orchestrator and tools:
  - “Can this agent call this tool with these parameters for this user?”
- Cloud-native identity:
  - Azure Entra ID / AWS IAM / GCP IAM for infra and data access.

**Layer 3 – Data Protection & DLP**

- PII detection/redaction:
  - Presidio or cloud-native DLP before indexing and before returning answers.
- Secrets:
  - Never via LLM context; always via **side channels** (KMS, Vault).

**Layer 4 – Logging, Audit, & Forensics**

- Immutable audit trail with:
  - User, agent, tools, inputs (hashed), outputs (hashed), cost, latency.
- Centralized logs (ELK/Splunk).
- Access limited to security/compliance roles.

**Layer 5 – Governance & Compliance**

- Map the system to **NIST AI RMF**:
  - Govern / Map / Measure / Manage.
- Identify:
  - Regimes that may apply: GDPR, HIPAA, SOX, EU AI Act, etc.
- Maintain:
  - Data inventories, processing purposes, retention schedules.

***

### 4.3 Mini Risk Register (Condensed)

| Risk                                       | Likelihood | Impact | Mitigation Highlights                                               |
|--------------------------------------------|------------|--------|----------------------------------------------------------------------|
| Prompt injection → tool misuse / data leak | High       | High   | Content safety + RAG hygiene + strict tool schemas + policy engine. |
| Unauthorized data access                   | Med-High   | High   | Least privilege, ABAC/RBAC, quarterly permission reviews.           |
| Hallucinations as “facts”                  | High       | Med-High | RAG with sources + evals + human review for high-risk flows.      |
| Compliance violations                      | Med        | High   | NIST AI RMF alignment + audit trails + legal review.               |
| Cost explosions                            | Med-High   | Med-High | Cost caps, semantic cache, routing, dashboards.                    |

***

### Security – Immediate Actions

1. Explicitly **list sensitive tools** (DBs, CI, prod APIs) and mark them Tier 2/3.
2. Add at least **one safety layer** in front of the LLM:
   - Azure AI Content Safety / Bedrock Guardrails / similar.
3. Start writing logs that contain:
   - `user_id`, `agent_id`, `tool_name`, `timestamp`, `cost`, `latency`.

### Security – If You Have More Time

1. Implement an **OPA/Rego policy check** for each tool call.
2. Integrate a **DLP layer** (Presidio or cloud-native).
3. Draft a **NIST AI RMF worksheet** for your Agent MVP and identify gaps.

***

## 5. Testing & Evaluation

### 5.1 Three Layers of Testing

1. **Unit-level**
   - Prompts: deterministic regression tests with known inputs/outputs.
   - Tool wrappers: validate input/output schemas and error handling.
   - Graph logic: node transitions, fallback branches.

2. **Scenario / Integration**
   - Multi-step flows:
     - “Ingest GitHub issue → clarify → propose fix → generate patch → tests.”
   - Check:
     - Correct agent is called.
     - No loops/fail storms.
     - Reasonable latency and token usage.

3. **End-to-End / Sandbox**
   - Run full flows **against a staging environment**:
     - Real repo (copy).
     - Real CI (sandbox).
   - Human review of outcomes.

### 5.2 Evaluation Frameworks & Metrics

Core metrics:

- **Task success rate** (did the agent achieve the intended outcome?).
- **Groundedness/faithfulness** (aligned with RAG or source data).
- **Safety violations**.
- **Latency & cost per request**.

Use:

- A tracing/eval platform (LangSmith-like) to:
  - Store conversations and outcomes.
  - Run **batch evaluations** against a test set.
- Experiment platform (Weights & Biases) to:
  - Compare prompt versions.
  - Compare models.

***

### Testing – Immediate Actions

1. Create **at least 20 test scenarios**:
   - 60% happy path, 20% edge, 20% adversarial.
2. Add a simple **pytest-based harness**:
   - Run scenarios against your LangGraph pipeline.
   - Fail if success < target baseline.
3. Record baseline:
   - Success %, latency, cost.

### Testing – If You Have More Time

1. Expand to **50–100 test cases** and wire into CI (GitHub Actions).
2. Add **LLM-as-judge** evaluation for quality scoring.
3. Add **regression gating** in CI:
   - Block deploys on >5% drop in success/quality.

***

## 6. Maintenance & Operations

### 6.1 Observability

At minimum track:

- **p95 latency** per agent and per tool.
- **Cost** per request, per workflow, per customer/team.
- **Error rates** (LLM, tool errors, safety rejections).
- **Guardrail events** (blocked prompts, blocked outputs).

You want:

- Application-level tracing:
  - Every step in the graph, with inputs, outputs, token counts.
- Infra-level telemetry:
  - CPU/memory, queue depths, container health.
- Dashboards and alerts:
  - Latency, cost, and error SLOs.

***

### 6.2 Cost Management

Cost volatility is a **genuine risk**:

- Tactics:
  - **Semantic caching**:
    - Cache embeddings + responses for common prompts.
  - **Model routing**:
    - Easy queries → cheap model; hard ones → more capable model.
  - **Hard caps**:
    - Per-request token caps and per-agent/day budgets.
  - **Batch processing**:
    - For non-interactive workloads.

***

### 6.3 Operational Runbooks

Define **runbooks** for:

- Accuracy drop:
  - Check eval dashboards, revert prompt or model, tighten RAG context.
- Latency spike:
  - Migrate to cheaper/faster model, scale infra, optimize tools.
- Cost spike:
  - Check for loops, over-eager routing, new call patterns.

Runbooks should include:

- Detection criteria.
- Triage questions.
- Standard mitigations.
- Rollback plan.
- Follow-up actions.

***

### Maintenance – Immediate Actions

1. Define **SLOs**:
   - p95 latency, cost per request, success rate, safety incident rate.
2. Stand up **one dashboard** that shows:
   - Latency, cost, errors for your MVP.
3. Write **one runbook**:
   - “Agent accuracy drops below X% or complaints spike.”

### Maintenance – If You Have More Time

1. Add **on-call rotation** and integrate alerts into Slack/Teams.
2. Add **weekly evaluation reports** for PM/Dev/QA agents.
3. Tune prompts and routing based on evaluation + telemetry.

***

## 7. 2026 Outlook: Trends & Volatility Hotspots

### 7.1 Trends That Matter

1. **MCP becoming de facto standard for tools**
   - IDEs, CLIs, browsers, and orchestrators are converging on MCP.
   - Your FastMCP server is strategically aligned; keep investing.

2. **Multi-model / multi-vendor routing**
   - Best practice is **not** “we’re a GPT shop”; it’s:
     - Choose model per-use-case and have a **fallback**.

3. **Agent marketplaces / internal “agent stores”**
   - Teams will be able to “install” agents like apps, within guardrails.
   - Your O’Reilly Agent MVP can be framed as a **template** for such agents.

4. **Regulatory hardening (EU AI Act, ISO 42001, sectoral rules)**
   - Expect:
     - Model documentation.
     - Data lineage.
     - Human-oversight requirements.

5. **Security research pace**
   - New prompt injection and jailbreaking techniques appear continuously.
   - Vendors respond with new mitigations; expect churn.

***

### 7.2 Volatility Hotspots & Mitigation Playbooks

- **Model deprecations / pricing changes**
  - Mitigation:
    - Model abstraction layer.
    - Continuous A/B testing against alternatives.

- **Guardrail effectiveness**
  - Mitigation:
    - Defense-in-depth (content safety + policy + DLP).
    - Red-team exercises.

- **Regulatory interpretation**
  - Mitigation:
    - Early collaboration with legal/compliance.
    - Adopt **NIST AI RMF** now; it maps well to coming requirements.

***

### Outlook – Immediate Actions

1. Ensure your architecture has **clean seams** where:
   - Models can be swapped.
   - Tools are MCP-based.
2. Start an **internal record** of:
   - Which models are used.
   - For which purposes.
   - With what evaluation scores.

### Outlook – If You Have More Time

1. Run a **mini red-team** against your MVP (internal adversarial testing).
2. Draft an **“AI Risk & Opportunity” one-pager** for leadership.

***

## 8. Recommendations & Roadmap (O’Reilly Agent MVP → Enterprise)

### 8.1 Gaps vs Enterprise Requirements

Your current components:

- LangGraph Pipeline (PM/Dev/QA graph).
- CrewAI alternate orchestration.
- Watcher Service.
- FastMCP server + Inspector.
- Interactive CLI.
- Documentation (Azure architecture, debugging, MCP refs).

**Key gaps:**

1. **No formal autonomy tiers / approval flows**.
2. **Safety & security layers** not fully codified:
   - Prompt injection defenses.
   - Content safety.
   - Authorization & DLP.
3. **Testing/evaluation harness** likely ad-hoc:
   - Need repeatable test suites and CI gating.
4. **Observability & cost metrics** not fully wired:
   - No single pane for latency/cost/success.
5. **Compliance & governance** not documented:
   - NIST AI RMF mapping incomplete.
   - No risk register formally tied to controls.

***

### 8.2 Roadmap (3–12 Months)

#### Phase 0 (Now – 2 weeks): Baseline Hardening

1. Define **Tier 1/2/3** for all tools in the LangGraph and CrewAI flows.
2. Add basic **logging** for:
   - Agent decisions.
   - Tool calls.
   - Cost/latency.
3. Put **all prompts and graph configs in git** with versioned names.

#### Phase 1 (Month 1–2): Security & Observability

1. Integrate:
   - A **content safety API** (Azure/B edrock or equivalent).
   - **Basic authorization** at tool boundary (role + tool whitelists).
2. Introduce:
   - Tracing/Eval (LangSmith-like).
   - A minimal **dashboard** showing error/latency/cost.

#### Phase 2 (Month 3–4): Testing & Evaluation

1. Build **50+ test cases** covering:
   - GitHub issues.
   - Requirements translation.
   - Code generation and QA.
2. Wire regression tests into **CI/CD**:
   - Block deploys on quality regressions.
3. Add **LLM-as-judge** scoring for key flows.

#### Phase 3 (Month 5–6): Compliance & Governance

1. Map system to **NIST AI RMF**.
2. Create:
   - Risk register.
   - Risk acceptance process.
3. Implement:
   - DLP for PII.
   - Immutable audit logs.

#### Phase 4 (Month 7–12): Scale & Reuse

1. Refine architecture as a **reusable blueprint**:
   - “O’Reilly Agent Template” with:
     - LangGraph skeleton.
     - MCP tool catalog.
     - Security & logging patterns baked in.
2. Add:
   - Model routing.
   - Semantic caching.
   - Multi-tenant support for multiple teams/courses.

***

### Roadmap – Immediate Actions

1. Decide and document:
   - **Primary orchestration** for teaching (LangGraph).
2. Add a **simple but real log & trace story** to the MVP so students can:
   - See the graph.
   - Inspect steps and tokens.
3. Write a **1–2 page “Enterprise Gap” doc**:
   - List of gaps from this section, tagged by phase.

### Roadmap – If You Have More Time

1. Turn this brief into:
   - A **reference repo** in GitHub with:
     - `docs/` (this brief).
     - `graph/` (LangGraph flows).
     - `tests/` (scenarios).
     - `security/` (policies, diagrams).
2. Layer in:
   - A minimal **NIST AI RMF appendix**:
     - For each function, show which code/config implements it.

***
