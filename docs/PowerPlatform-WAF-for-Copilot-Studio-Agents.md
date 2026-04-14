# Power Platform Well-Architected Framework (WAF) for Copilot Studio Agents  
**Applies to:** Customer Service Assistant · Employee Onboarding Agent · Document Processor Agent  
**Goal:** Teach “how Microsoft wants you to build this” and still ship something that works on Monday.  
**Last updated:** 2025-12-14  

---

## How to use this doc (for instructors + learners)

### Instructor plan (90–150 minutes)
1. **Frame the workload** (10 min): what each agent does, and what “good” looks like.  
2. **Pillar sprint** (45–60 min): do the cross-cutting checklist once.  
3. **Agent deep dives** (25–45 min): apply the same pillar lens to each of the three agents.  
4. **Capstone** (10–30 min): add one stability improvement and one safety improvement per agent.  

### Learner rhythm (repeat per agent)
- **Understand** the workload boundary.  
- **Name** the failure modes.  
- **Pick** 3 WAF recommendations you can implement today.  
- **Prove** it with a test transcript and analytics checkpoint.  

---

## What WAF is (Power Platform edition)
**Power Platform Well-Architected** is Microsoft’s set of best practices, architecture guidance, and review tools for designing “modern application workloads” built with Power Platform.  
Start with the **pillars**, align design choices to each pillar, and use the **assessment tool** to track improvements over milestones.  

**Primary references (Microsoft Learn):**
- Power Platform Well-Architected overview: https://learn.microsoft.com/power-platform/well-architected/  
- Pillars: https://learn.microsoft.com/power-platform/well-architected/pillars  
- Assessment guidance: https://learn.microsoft.com/power-platform/well-architected/implementing-recommendations  
- Power Platform + Copilot Studio Architecture Center: https://learn.microsoft.com/power-platform/architecture/  
- Copilot Studio reference architectures (includes autonomous doc processing): https://learn.microsoft.com/power-platform/architecture/products/copilot-studio  

---

## The workload: three agents, one architecture mindset

### Agent A: Customer Service Assistant (conversational)
**Job:** Answer policy questions, triage inbound issues, draft replies, escalate when needed.  
**Typical integrations:** Outlook/Exchange, Teams, ticketing system, knowledge docs.  
**Primary risks:** wrong policy, privacy leak, hallucinated promises, missed escalations.

### Agent B: Employee Onboarding Agent (internal)
**Job:** Day 1 checklist, FAQs, access requests, status nudges, “who do I ask” routing.  
**Typical integrations:** Entra ID, Teams, SharePoint, Dataverse/HR data, request workflow.  
**Primary risks:** over-sharing HR data, unauthorized access requests, identity mix-ups.

### Agent C: Document Processor Agent (autonomous + conversational)
**Job:** React to new files, classify, extract metadata, route, request missing info, hand off to humans.  
**Typical integrations:** SharePoint, Dataverse, Power Automate, approvals, downstream LOB systems.  
**Primary risks:** routing the wrong file, data exfiltration via connectors, silent failure, runaway cost.

> Microsoft provides a reference architecture for an **autonomous document processing agent** in Copilot Studio.  
> Use it as your “known-good” baseline for Agent C, and as a pattern library for A and B.  
> https://learn.microsoft.com/power-platform/architecture/reference-architectures/document-processing-agent

---

## “Stable now” vs “Forward-looking” (preview/prerelease)
You want learners to build **stable** foundations, and also understand what’s coming.

### Stable building blocks (use freely in class)
- **Generative orchestration** (default for new agents) and how it chooses tools/topics/knowledge.  
  https://learn.microsoft.com/microsoft-copilot-studio/advanced-generative-actions  
- **Event triggers** (autonomous reactions) for agents with generative orchestration enabled.  
  https://learn.microsoft.com/microsoft-copilot-studio/authoring-trigger-event  
- **Agent flows** (Copilot Studio-built flows) to extend capabilities.  
  https://learn.microsoft.com/microsoft-copilot-studio/advanced-flow  
- **Knowledge file uploads** (MD/HTML/CSV/JSON/YAML/PDF/etc).  
  https://learn.microsoft.com/microsoft-copilot-studio/knowledge-add-file-upload  
- **Analytics** for conversational and autonomous agents.  
  https://learn.microsoft.com/microsoft-copilot-studio/analytics-overview  
- **Solutions + ALM** (export/import agents via solutions).  
  https://learn.microsoft.com/microsoft-copilot-studio/authoring-solutions-import-export  
- **DLP data policies for Copilot Studio** (connector guardrails).  
  https://learn.microsoft.com/microsoft-copilot-studio/admin-data-loss-prevention  

### Forward-looking capabilities (teach as “handle with oven mitts”)
- **(Preview) GPT‑5 models** in Copilot Studio (experiment, don’t bet the farm).  
  https://learn.microsoft.com/microsoft-copilot-studio/whats-new  
- **Prerelease: REST API tools** via OpenAPI specs (subject to change).  
  https://learn.microsoft.com/microsoft-copilot-studio/agent-extend-action-rest-api  

---

# The WAF pillars, translated into Copilot Studio language

WAF pillars (Power Platform) map cleanly to agent workloads:
- **Reliability**
- **Security**
- **Operational Excellence**
- **Performance Efficiency**
- **Experience Optimization**

Reference: https://learn.microsoft.com/power-platform/well-architected/pillars  

---

## Pillar 1 — Reliability (your agent keeps its promises)

### What reliability means for agents
- The agent **does not silently fail** when connectors, flows, or knowledge sources wobble.  
- The agent **escapes gracefully** when confidence is low.  
- The agent **doesn’t double-process** the same event (idempotency).  

### Reliability design checklist (copy/paste into your backlog)
**Events + autonomy**
- [ ] Every event-triggered path writes a **correlation ID** (eventId / fileId / ticketId) into storage.  
- [ ] Every event-triggered path is **idempotent** by design (re-run is safe).  
- [ ] Every autonomous action has a **human fallback** topic or approval path.  
- [ ] Every integration has a **timeout + retry** strategy, and retries don’t create duplicates.  

**Conversation safety**
- [ ] The agent never “guesses” policy.  
- [ ] The agent offers **escalation** when it lacks evidence.  
- [ ] The agent repeats back the **key facts** it is about to act on.  

**Platform mechanics you should teach**
- Event triggers require **generative orchestration**.  
  https://learn.microsoft.com/microsoft-copilot-studio/authoring-trigger-event  
- Event triggers can affect **billing calculations**.  
  https://learn.microsoft.com/microsoft-copilot-studio/authoring-triggers-about  

### Reliability lab (15 minutes)
1. Add an **Escalate to human** topic in Agent A and Agent B.  
2. Add an **“I need missing info”** topic in Agent C.  
3. Add a simple storage step in your flow (Dataverse row or SharePoint list item) for **correlation IDs**.  
4. Replay the same test payload twice.  
5. Verify no duplicate side effects.  

---

## Pillar 2 — Security (your agent doesn’t leak your org into the sun)

### What security means for Copilot Studio workloads
- Your agent follows **least privilege** for connector auth and data access.  
- Your agent obeys **DLP connector constraints** so business data does not cross boundaries.  
- Your agent has **channel security** and governance guardrails.  

### Security checklist (agent-specific)
**Governance + controls**
- [ ] Review Copilot Studio **security and governance** controls and apply tenant/environment settings.  
  https://learn.microsoft.com/microsoft-copilot-studio/security-and-governance  
- [ ] Use **key configuration settings** guidance for tenant, environment, and agent controls.  
  https://learn.microsoft.com/microsoft-copilot-studio/guidance/sec-gov-config-settings  

**DLP**
- [ ] Create a **data policy strategy** aligned with your environment strategy.  
  https://learn.microsoft.com/power-platform/guidance/adoption/dlp-strategy  
- [ ] Configure data policies for agents, and ensure connectors are in correct data groups.  
  https://learn.microsoft.com/microsoft-copilot-studio/admin-data-loss-prevention  
- [ ] Teach learners that DLP applies at **tenant/environment level**, not per-user.  
  https://learn.microsoft.com/power-platform/guidance/adoption/dlp-strategy  

**Channel security**
- [ ] For web chat, enable and rotate **Direct Line** secrets/tokens.  
  https://learn.microsoft.com/microsoft-copilot-studio/configure-web-security  

### Security lab (20 minutes)
1. List every connector and data store used by the three agents.  
2. Classify each connector as **Business / Non-business / Blocked** in a DLP plan.  
3. Demonstrate one “blocked combo” scenario and show the guardrail working.  
4. For web channel, rotate a Direct Line secret and confirm clients still connect.

---

## Pillar 3 — Operational Excellence (you can operate what you build)

### What ops excellence means for agents
- You can **test**, **deploy**, **observe**, and **roll back** without panic.  
- You can connect changes to outcomes using analytics and transcript review.  
- You treat prompts, topics, knowledge sources, and flows as **versioned artifacts**.

### Operational excellence checklist
**ALM**
- [ ] Use **solutions** as the unit of shipping for agents.  
  https://learn.microsoft.com/microsoft-copilot-studio/authoring-solutions-overview  
- [ ] Export/import agents via solutions across environments.  
  https://learn.microsoft.com/microsoft-copilot-studio/authoring-solutions-import-export  
- [ ] Follow Power Platform ALM principles: separate **dev/test/prod** environments.  
  https://learn.microsoft.com/power-platform/alm/environment-strategy-alm  
- [ ] Consider **pipelines** for repeatable deployments.  
  https://learn.microsoft.com/power-platform/alm/pipelines  

**Observability**
- [ ] Use Copilot Studio **Analytics** to track quality and usage.  
  https://learn.microsoft.com/microsoft-copilot-studio/analytics-overview  
- [ ] Build a transcript analysis loop using Microsoft’s reference architecture.  
  https://learn.microsoft.com/power-platform/architecture/reference-architectures/analyze-agent-conversation-transcripts  

**Testing**
- [ ] Use Power CAT **Copilot Studio Kit** or equivalent to run regression tests against Direct Line APIs.  
  WAF mentions the Kit in ops recommendations:  
  https://learn.microsoft.com/power-platform/well-architected/operational-excellence/tools-processes  
  Copilot Studio “What’s new” also points to the Kit:  
  https://learn.microsoft.com/microsoft-copilot-studio/whats-new  

### Ops lab (30 minutes)
1. Create a **dev** and **test** environment.  
2. Move one agent between them using **solutions**.  
3. Publish to a demo channel and validate the behavior.  
4. Capture 5 “golden conversations” and store them in source control as JSON transcripts.  
5. Add a rubric: expected intent, expected tool call, expected response constraints.

---

## Pillar 4 — Performance Efficiency (fast enough, cheap enough, predictable enough)

### What performance means for agents
- The agent answers quickly.  
- The agent avoids unnecessary tool calls and knowledge searches.  
- The agent respects payload sizes and uses structured outputs where possible.

### Performance checklist
**Prompt + instruction discipline**
- [ ] Write concise agent **instructions** and update them intentionally.  
  https://learn.microsoft.com/microsoft-copilot-studio/authoring-instructions  
- [ ] Follow Microsoft guidance for generative mode instructions.  
  https://learn.microsoft.com/microsoft-copilot-studio/guidance/generative-mode-guidance  
- [ ] Prefer structured outputs from topics/tools, then let orchestration compose the final message.  
  https://learn.microsoft.com/microsoft-copilot-studio/advanced-generative-actions  

**Tooling discipline**
- [ ] Use **agent flows** for deterministic steps (lookups, writes, approvals).  
  https://learn.microsoft.com/microsoft-copilot-studio/advanced-flow  
- [ ] Use event triggers only where autonomy adds real value, because events can affect billing.  
  https://learn.microsoft.com/microsoft-copilot-studio/authoring-trigger-event  

### Performance lab (15 minutes)
1. Take one topic per agent and remove “chatty” fluff from its steps.  
2. Replace one free-form “thinky” step with a small deterministic lookup via flow.  
3. Measure perceived latency using a stopwatch and log “slow turns.”

---

## Pillar 5 — Experience Optimization (humans feel in control)

### What “experience” means for agents
- Users know what the agent can do.  
- The agent asks for confirmation before irreversible actions.  
- The agent uses consistent language and visible structure.

### Experience checklist
**Topic craft**
- [ ] Follow topic authoring best practices: bite-sized, reusable, minimal overlap.  
  https://learn.microsoft.com/microsoft-copilot-studio/guidance/topic-authoring-best-practices  
- [ ] Follow topic design process guidance for scope and scenarios.  
  https://learn.microsoft.com/microsoft-copilot-studio/guidance/defining-chatbot-topics  
- [ ] Avoid periods in topic names, because it can break solution exports.  
  https://learn.microsoft.com/microsoft-copilot-studio/guidance/topics-overview  

**Knowledge craft**
- [ ] Upload knowledge files in supported formats (MD/HTML/CSV/JSON/YAML/etc).  
  https://learn.microsoft.com/microsoft-copilot-studio/knowledge-add-file-upload  
- [ ] Keep knowledge sources small and modular so learners can reason about grounding.

**Publishing + channels**
- [ ] Teach “publish is a real step,” and each update requires re-publishing.  
  https://learn.microsoft.com/microsoft-copilot-studio/publication-fundamentals-publish-channels  

### Experience lab (15 minutes)
1. Add a “Before I do that, confirm X/Y/Z” node for one action per agent.  
2. Add one **structured response** (table, numbered steps, or a small card-like summary).  
3. Run a learner usability check: can a stranger predict what happens next?

---

# Apply WAF to each of your three agents (scorecards + improvements)

## Agent A — Customer Service Assistant (WAF scorecard)
**Reliability**
- Add correlation IDs for inbound email triage events.  
- Add explicit escalation topic + SLA handoff.  

**Security**
- DLP: keep customer data inside business connectors only.  
- Avoid pasting full customer email bodies into tools that do not need it.  

**Ops**
- Store “golden” transcripts for top 10 questions (returns, warranty, shipping, billing).  
- Track deflection rate and escalation rate in Analytics.  

**Performance**
- Keep policy answers grounded in knowledge docs.  
- Use flows for deterministic order lookups.  

**Experience**
- Always cite policy section titles (not hallucinated policy).  
- Confirm identity before discussing account details.

## Agent B — Employee Onboarding Agent (WAF scorecard)
**Reliability**
- Use a checklist-driven flow for onboarding steps.  
- Add “missing info” prompts for manager, start date, department.  

**Security**
- Treat HR data as sensitive.  
- Implement strict environment access controls for makers.  

**Ops**
- Version knowledge sources (HR policies) and review quarterly.  
- Use solutions + pipelines for promotion to production.  

**Performance**
- Use short, role-based instructions.  
- Use flow calls for access provisioning requests.  

**Experience**
- Provide a “Day 1 in 5 bullets” quick response.  
- Offer an explicit “talk to a human” path for exceptions.

## Agent C — Document Processor Agent (WAF scorecard)
**Reliability**
- Idempotency is mandatory.  
- Human review queue for low-confidence classification.  
- Use Microsoft’s doc processing reference architecture as baseline.  
  https://learn.microsoft.com/power-platform/architecture/reference-architectures/document-processing-agent  

**Security**
- Lock connector combinations with DLP.  
- Keep audit trails of actions and file movement.  

**Ops**
- Build automated transcript + event log analysis dashboards using Microsoft’s transcript reference architecture.  
  https://learn.microsoft.com/power-platform/architecture/reference-architectures/analyze-agent-conversation-transcripts  

**Performance**
- Keep payloads small: send file references, not full file content.  
- Use flows for extraction and routing mechanics.  

**Experience**
- When asking for missing info, show a form-like list of fields needed.  
- Provide a “what I did” summary after processing.

---

# Forward-thinking module (optional, but fun and useful)

## Preview: GPT‑5 models in Copilot Studio
**Teach it as an experiment track.**  
Make learners compare answer quality, latency, and safety behaviors between the default model and GPT‑5 (preview).  
Reference: https://learn.microsoft.com/microsoft-copilot-studio/whats-new  

## Prerelease: REST API tools (OpenAPI)
**Teach it as a controlled extension mechanism.**  
Make learners add one small tool that returns deterministic data, like “company holiday list.”  
Reference: https://learn.microsoft.com/microsoft-copilot-studio/agent-extend-action-rest-api  

**Rule:** Every preview/prerelease feature gets:
- A rollback plan.  
- A test plan.  
- A “this might change” warning in the learner lab.

---

# Appendix: a simple WAF milestone cadence (use the assessment tool)

### When to assess
- **Milestone 0:** initial design.  
- **Milestone 1:** first working end-to-end path.  
- **Milestone 2:** pre-production.  
- **Milestone 3:** 30 days after launch.

Microsoft guidance: take the assessment during initial design and periodically at milestones, export recommendations to CSV, and add them to the backlog.  
Reference: https://learn.microsoft.com/power-platform/well-architected/implementing-recommendations  

---

# Appendix: “Don’t step on rakes” (common gotchas)

- **Topic names:** avoid periods (`.`) because it can prevent solution export.  
  https://learn.microsoft.com/microsoft-copilot-studio/guidance/topics-overview  
- **Event triggers:** require generative orchestration and can affect billing.  
  https://learn.microsoft.com/microsoft-copilot-studio/authoring-trigger-event  
- **Analytics:** test-panel interactions don’t show in Analytics.  
  https://learn.microsoft.com/microsoft-copilot-studio/analytics-overview  
- **DLP:** the most restrictive policy wins when multiple policies apply.  
  https://learn.microsoft.com/power-platform/guidance/adoption/dlp-strategy  

---

## Sources (Microsoft Learn)
(These are the “non-random internet” references used in this doc.)

- https://learn.microsoft.com/power-platform/well-architected/  
- https://learn.microsoft.com/power-platform/well-architected/pillars  
- https://learn.microsoft.com/power-platform/well-architected/implementing-recommendations  
- https://learn.microsoft.com/power-platform/architecture/  
- https://learn.microsoft.com/power-platform/architecture/products/copilot-studio  
- https://learn.microsoft.com/power-platform/architecture/reference-architectures/document-processing-agent  
- https://learn.microsoft.com/power-platform/architecture/reference-architectures/analyze-agent-conversation-transcripts  
- https://learn.microsoft.com/microsoft-copilot-studio/advanced-generative-actions  
- https://learn.microsoft.com/microsoft-copilot-studio/authoring-trigger-event  
- https://learn.microsoft.com/microsoft-copilot-studio/advanced-flow  
- https://learn.microsoft.com/microsoft-copilot-studio/knowledge-add-file-upload  
- https://learn.microsoft.com/microsoft-copilot-studio/analytics-overview  
- https://learn.microsoft.com/microsoft-copilot-studio/authoring-solutions-overview  
- https://learn.microsoft.com/microsoft-copilot-studio/authoring-solutions-import-export  
- https://learn.microsoft.com/microsoft-copilot-studio/admin-data-loss-prevention  
- https://learn.microsoft.com/microsoft-copilot-studio/security-and-governance  
- https://learn.microsoft.com/microsoft-copilot-studio/guidance/sec-gov-config-settings  
- https://learn.microsoft.com/microsoft-copilot-studio/configure-web-security  
- https://learn.microsoft.com/microsoft-copilot-studio/guidance/topic-authoring-best-practices  
- https://learn.microsoft.com/microsoft-copilot-studio/guidance/defining-chatbot-topics  
- https://learn.microsoft.com/microsoft-copilot-studio/guidance/topics-overview  
- https://learn.microsoft.com/microsoft-copilot-studio/whats-new  
- https://learn.microsoft.com/microsoft-copilot-studio/agent-extend-action-rest-api  
- https://learn.microsoft.com/power-platform/alm/environment-strategy-alm  
- https://learn.microsoft.com/power-platform/alm/pipelines  
- https://learn.microsoft.com/power-platform/guidance/adoption/environment-strategy  
- https://learn.microsoft.com/power-platform/guidance/adoption/dlp-strategy  
