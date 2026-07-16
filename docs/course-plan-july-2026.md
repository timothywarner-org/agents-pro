# How to Create AI Agents Like a Pro - July 2026

_O'Reilly Live Learning - Instructor Source of Truth_

**Instructor:** Tim Warner (Microsoft MVP, MCT Regional Lead)
**Delivery date:** July 2026
**Duration:** 4 hours (four ~50-minute segments, 10-minute break between segments)
**Delivery mode:** Live, hands-on, single progressively-built Copilot Studio agent - the **Contoso Pinball Gallery Concierge**

## Course Overview - One Agent, Four Segments

This is a **Copilot Studio** course. The four segment titles below are the ones on the O'Reilly sell page, kept verbatim. We satisfy every one of them by building **one** agent end-to-end across the four segments: the **Contoso Pinball Gallery Concierge**. Every segment adds a capability layer; every segment maps to Microsoft's Power Platform Well-Architected Framework (PP-WAF) pillars.

| Segment | Sell-page title | Pinball demo (the running scenario) | Primary PP-WAF Pillars |
|---------|-----------------|--------------------------------------|------------------------|
| 1 | Copilot Studio Fundamentals & Creating Your First Agent | Describe the Concierge in natural language, add three knowledge sources, test in the simulator - the customer-service-assistant pattern | Experience Optimization, Operational Excellence |
| 2 | Topics, Actions, and Power Automate Integration | Build the Repair Triage topic and the **Book a Service** Power Automate flow with an approval step - the onboarding-with-approvals pattern, realized as service booking | Experience Optimization, Reliability |
| 3 | Autonomous Agents & Event Triggers | A repair-intake or trade-in form lands in SharePoint, an event trigger fires, the agent processes it autonomously - the document-processor pattern | Performance Efficiency, Reliability |
| 4 | Deployment, Analytics, and ROI | Publish to Teams / SharePoint / M365 Copilot; walk Analytics, the Savings calculator ROI tile, custom metrics, governance and CoE | Security, Operational Excellence |

**The one agent:** The **Contoso Pinball Gallery Concierge** is the always-on virtual host for **Contoso Pinball Gallery**, a fictional boutique showroom that sells, restores, and services classic and modern pinball machines. It answers **inventory** questions (what is in stock, condition, price, availability), **triages repairs** (a reported symptom, safe first-line guidance, a booking offer), explains **history and research** (who made a machine, its era, its significance), and hands off to **deterministic Power Automate flows** for anything transactional (bookings, quotes, status, holds, trade-ins). The company, catalog, prices, and service records are invented. The Copilot Studio facts are grounded in Microsoft Learn.

**The real repo assets** (read these; the plan references them directly):

- Agent instructions - `Contoso Pinball Gallery Concierge/instructions.md`
- Knowledge docs - `Contoso Pinball Gallery Concierge/knowledge/` (inventory-catalog, repair-playbook, pinball-history-research, warranty-and-services, plus KNOWLEDGE-UPLOAD-METADATA)
- Topic stubs - `Contoso Pinball Gallery Concierge/topics/` (T01_InventoryLookup, T02_RepairTriage)
- Flow specs - `Contoso Pinball Gallery Concierge/flows/deterministic-flow-ideas.md`
- Trigger phrases and model descriptions - `Contoso Pinball Gallery Concierge/triggers/quick-win-triggers.md`
- Eval set - `Contoso Pinball Gallery Concierge/evals/eval-set.md`
- MS Learn grounding - `Contoso Pinball Gallery Concierge/docs/ms-learn-sources.md`

**Showroom inventory the demos lean on** (from `knowledge/inventory-catalog.md`):

| Title | Maker | Year | Era | Condition | Price | Availability |
|-------|-------|------|-----|-----------|-------|--------------|
| Medieval Madness | Williams | 1997 | DMD | Excellent | $11,500 | In stock |
| Jaws Premium | Stern | 2024 | LCD | Museum | $10,400 | In stock |
| Godzilla Premium | Stern | 2021 | LCD | Excellent | $9,900 | In stock |
| Attack from Mars | Bally | 1995 | DMD | Very Good | $8,200 | In stock |
| The Twilight Zone | Bally | 1993 | DMD | Good | $7,400 | In stock |
| Rush Pro | Stern | 2022 | LCD | Very Good | $6,700 | On hold |
| The Addams Family | Bally | 1992 | DMD | Very Good | $6,900 | Sold - waitlist |
| Fireball | Bally | 1972 | EM | Museum | $5,200 | In stock |
| Black Knight | Williams | 1980 | SS | Good | $3,600 | In stock |
| Firepower | Williams | 1980 | SS | Project | $1,900 | In stock |

**Authoritative references used throughout the course** - all verified stable URLs:

- Copilot Studio overview - <https://learn.microsoft.com/microsoft-copilot-studio/fundamentals-what-is-copilot-studio>
- Power Platform Well-Architected - <https://learn.microsoft.com/power-platform/well-architected/>
- Copilot Studio topics - <https://learn.microsoft.com/microsoft-copilot-studio/authoring-create-edit-topics>
- Generative orchestration - <https://learn.microsoft.com/microsoft-copilot-studio/advanced-generative-actions>
- Select a primary AI model - <https://learn.microsoft.com/microsoft-copilot-studio/authoring-select-agent-model>
- Knowledge sources summary - <https://learn.microsoft.com/microsoft-copilot-studio/knowledge-copilot-studio>
- Power Automate flow actions - <https://learn.microsoft.com/microsoft-copilot-studio/advanced-flow>
- Event trigger overview - <https://learn.microsoft.com/microsoft-copilot-studio/authoring-triggers-about>
- Add an event trigger - <https://learn.microsoft.com/microsoft-copilot-studio/authoring-trigger-event>
- Design autonomous agent capabilities - <https://learn.microsoft.com/microsoft-copilot-studio/guidance/autonomous-agents>
- MCP in Copilot Studio - <https://learn.microsoft.com/microsoft-copilot-studio/agent-extend-action-mcp>
- Model Context Protocol spec - <https://modelcontextprotocol.io/specification>
- Agent evaluations - <https://learn.microsoft.com/microsoft-copilot-studio/analytics-agent-evaluation-intro>
- Analytics overview - <https://learn.microsoft.com/microsoft-copilot-studio/analytics-overview>
- Savings calculator (cost savings) - <https://learn.microsoft.com/microsoft-copilot-studio/analytics-cost-savings>
- Custom metrics - <https://learn.microsoft.com/microsoft-copilot-studio/analytics-custom-metrics>
- Tell the value story (ROI) - <https://learn.microsoft.com/microsoft-copilot-studio/guidance/agent-business-value-tell-value-story>
- Security & governance - <https://learn.microsoft.com/microsoft-copilot-studio/security-and-governance>
- VS Code extension - <https://learn.microsoft.com/microsoft-copilot-studio/visual-studio-code-extension-overview>

---

## Segment 1 - Copilot Studio Fundamentals & Creating Your First Agent (0:00 - 0:50)

_Describe the agent in natural language, ground it in three knowledge sources, test in the simulator. This segment ships an FAQ-style agent that answers real questions._

### Time Table

| Time | Activity |
|------|----------|
| 0:00 - 0:07 | Welcome, course arc, the one-agent promise (the Concierge) |
| 0:07 - 0:16 | What "agent" means in Copilot Studio; generative vs classic orchestration; pick the reasoning model |
| 0:16 - 0:26 | The Contoso scenario and persona; write the agent instructions |
| 0:26 - 0:40 | Live: create the agent by natural-language description, paste instructions, add three knowledge sources |
| 0:40 - 0:48 | Live: test in the simulator against the inventory / research / warranty questions |
| 0:48 - 0:50 | Segment wrap, what is next |

### Talking Points

- **What an agent is here.** An agent in Copilot Studio combines **a few curated topics** with **generative answers grounded in trusted sources**, plus tools it can call. The design guidance is deliberately not "hundreds of rigid topics." Reference: <https://learn.microsoft.com/microsoft-copilot-studio/fundamentals-what-is-copilot-studio>
- **Orchestration modes.** Classic orchestration matches user utterances to trigger phrases. Generative orchestration uses an LLM planner that reads the **description** of every topic, tool, agent, and knowledge source to build a plan. Generative is the **default for new agents**, and we use it. Reference: <https://learn.microsoft.com/microsoft-copilot-studio/advanced-generative-actions>
- **Create by natural-language description.** The current experience lets you describe the agent in plain language and it scaffolds instructions and starters. We start there, then paste the vetted `instructions.md` block so the persona, grounding rules, and safety boundaries are exact.
- **Pick the reasoning model on the Overview tab.** Generative orchestration lets you choose the agent's primary model. **GPT-4.1 remains the platform Default model.** **GPT-5 Chat and GPT-5.5 Chat are GA** - say "GPT-5 *Chat*", never bare "GPT-5", because GPT-5 Reasoning (Deep), GPT-5 Auto, and GPT-5.5 Reasoning are still **preview/experimental**. **Claude Sonnet 4.6, Opus 4.6 (Deep), and Opus 4.7 (Deep) are GA**; **Claude Sonnet 4.5 has retired** (do not demo it). Claude Sonnet 5 is GA but only in the new-experience agent surface, not the classic authoring model this course teaches. Claude models are external (Anthropic), so a **tenant admin must approve** them first. **Re-verify the current MS-recommended orchestrator against the live docs page before each delivery** - the model lineup turns over every 4 to 6 weeks. Reference: <https://learn.microsoft.com/microsoft-copilot-studio/authoring-select-agent-model>
- **PP-WAF - Experience Optimization first.** Before any node, define the persona, the job to be done, and success metrics. Reference: <https://learn.microsoft.com/power-platform/well-architected/experience-optimization/>
- **Instruction design.** System instructions beat per-topic prompts under generative orchestration. The `instructions.md` file sets persona, boundaries, grounding rules, house style, and the handoff contract. Reference: <https://learn.microsoft.com/microsoft-copilot-studio/guidance/generative-mode-guidance>

### Scenario Framing - The Contoso Pinball Gallery Customer

- **Company.** **Contoso Pinball Gallery**, a boutique showroom that sells, restores, and services classic and modern pinball machines.
- **Persona.** Dana, a first-time collector who found the showroom online. Dana wants to know if a specific title is in stock and what it costs, has a machine at home with a symptom to triage, and is curious about the history of the pieces on the floor. Staff also use the Concierge as a quick internal lookup.
- **Pain points.** Prices and stock change; a customer who gets an invented price or a fabricated appointment slot loses trust immediately. Repairs carry a real safety line: nobody should be told to open a powered backbox.
- **Success metrics** (from `evals/eval-set.md`): routing accuracy above 90 percent; 100 percent grounding on prices, stock, and policy; zero invented prices, stock, references, or appointment slots (hard requirement); every unsafe-DIY or burning-smell case escalates correctly (hard requirement).

### Agent Instructions - Source of Truth

The full instructions block is in `Contoso Pinball Gallery Concierge/instructions.md`. The load-bearing rules to read aloud:

> You are the **Contoso Pinball Gallery Concierge**. Ground every factual answer in the registered knowledge sources; inventory, prices, warranty terms, and service policies come from Contoso's own documents, never from your own guesses. If a machine, price, or policy is not in the knowledge sources, say so plainly and offer to open a request or connect a human. For anything involving money, scheduling, or a commitment (bookings, quotes, orders), hand off to the matching deterministic flow rather than promising an outcome yourself. Never advise a customer to open a machine's high-voltage backbox. Keep a human in the loop for high-impact actions, and be transparent that you are an AI concierge.

### Knowledge Sources Added in Segment 1

| Source doc | What it grounds | Upload description source |
|------------|-----------------|---------------------------|
| `inventory-catalog.md` | Stock, condition grade, price, era, availability per title | `KNOWLEDGE-UPLOAD-METADATA.md` |
| `pinball-history-research.md` | Designer, manufacturer, era, significance, features | `KNOWLEDGE-UPLOAD-METADATA.md` |
| `warranty-and-services.md` | Warranty coverage, service tiers, price bands, turnaround | `KNOWLEDGE-UPLOAD-METADATA.md` |

The **description** you paste on each upload drives retrieval quality under generative orchestration, so that step is not optional. Reference: <https://learn.microsoft.com/microsoft-copilot-studio/knowledge-copilot-studio>

### Live Build Checklist - Segment 1

- [ ] Create a Copilot Studio environment (dev)
- [ ] Create the agent by natural-language description; name it **Contoso Pinball Gallery Concierge**
- [ ] Confirm **Generative orchestration** is on (it is the default)
- [ ] Set the primary model on the **Overview** tab (Default is GPT-4.1; demo Claude Sonnet 4.6 or Opus 4.6/4.7 only if tenant-approved - Sonnet 4.5 has retired, do not select it)
- [ ] Paste the `instructions.md` block into **Instructions**
- [ ] Add the three knowledge docs above; paste each description from `KNOWLEDGE-UPLOAD-METADATA.md`
- [ ] Set the display name, description, and the four suggested conversation starters
- [ ] Test in the simulator against the prompts below

### Demo Prompt Set - Segment 1

| Prompt | Expected behavior |
|--------|-------------------|
| "What pinball machines do you have in stock?" | Grounded inventory answer listing in-stock titles with prices |
| "Do you have Medieval Madness, and how much?" | Confirms in stock, names Williams 1997, states $11,500 |
| "Tell me about Attack from Mars." | Bally, 1995, DMD golden era, Brian Eddy, "Rule the Universe" |
| "What's the weather tomorrow?" | Politely redirects to pinball; does not answer off-domain |

---

## Segment 2 - Topics, Actions, and Power Automate Integration (1:00 - 1:50)

_Build the Repair Triage topic, then the **Book a Service** Power Automate flow with an approval step. This is the onboarding-with-approvals pattern realized as service booking - the mini-exercise wires an action to a topic._

### Time Table

| Time | Activity |
|------|----------|
| 1:00 - 1:08 | Recap; topics vs actions vs flows; when to make something deterministic |
| 1:08 - 1:24 | Build `T02_RepairTriage` - question, grounded playbook search, booking offer |
| 1:24 - 1:42 | Build the **Book a Service** Power Automate flow with an approval step; wire it into the topic |
| 1:42 - 1:48 | Test the end-to-end triage-to-booking path |
| 1:48 - 1:50 | Segment wrap |

### Talking Points

- **Topics carry conversation logic; flows carry transactions.** The guidance from `flows/deterministic-flow-ideas.md`: if the business says "the agent must follow these exact steps," make it **deterministic**. A booking, quote, status check, or hold returns a **real** reference number, not one the model guessed. References: <https://learn.microsoft.com/microsoft-copilot-studio/authoring-create-edit-topics> and <https://learn.microsoft.com/microsoft-copilot-studio/advanced-flow>
- **The Repair Triage topic shape** (`topics/T02_RepairTriage.mcs.yml`): one `Question` node captures machine plus symptom together, a `SearchAndSummarizeContent` node grounds triage in the repair playbook with `webBrowsing: false` so advice comes from Contoso's vetted procedures, a `SendActivity` returns the formatted guidance, a boolean `Question` offers a booking, and a `ConditionGroup` branches to the flow handoff. The stub carries a `MAKER TODO` at the handoff - Segment 2 replaces it with the real **Book a Service** action.
- **Model descriptions are the routing contract.** Under generative orchestration the `modelDescription` on a topic is the number-one driver of correct routing; a weak description is the number-one cause of the wrong topic firing. The Repair Triage description: "Triages a reported pinball machine symptom against the repair playbook, gives first-step guidance, and offers to hand off to a service booking." Reference: `triggers/quick-win-triggers.md`
- **Trigger phrases - 5 to 10 is the sweet spot.** Variety of phrasing beats volume. The Repair Triage phrases include "my flipper is weak", "display is flickering", "book a service appointment". Reference: <https://learn.microsoft.com/microsoft-copilot-studio/guidance/trigger-phrases-best-practices>
- **The Book a Service flow** (`flows/deterministic-flow-ideas.md`, Flow 1). Inputs: `MachineTitle`, `Symptom`, `PreferredWindow`, `ContactEmail`. Steps: validate inputs, write a row to a **Dataverse** table `ServiceBookings` (or a SharePoint list for a lighter demo), generate a `SVC-` booking reference, send a confirmation email. Outputs: `BookingReference`, `ConfirmedWindow`, `Status = Booked`. The Concierge reports the reference verbatim from the flow output.
- **The approval step.** For a commitment like an appointment slot, add a **Power Automate approval action** so a Contoso staff member confirms the slot before it is booked. This is the "onboarding-with-approvals" pattern from the sell page, realized as service booking. It also satisfies the responsible-AI practice of keeping a **human in the loop** for high-impact actions.
- **On Plan Complete - a graceful-close nicety.** Copilot Studio has an **On Plan Complete** trigger that fires after the whole plan runs and the response is sent. Use it to redirect to an end-of-conversation topic or a CSAT survey - but gate it on a context variable so it does not fire after every follow-up question. Reference: <https://learn.microsoft.com/microsoft-copilot-studio/guidance/generative-orchestration#custom-triggers-in-generative-orchestration>
- **PP-WAF - Reliability.** Ground triage in a trusted source; degrade gracefully when the playbook has no match; let the deterministic flow own the transaction. Reference: <https://learn.microsoft.com/power-platform/well-architected/reliability/>

### Deterministic Flow Inventory (build order, highest value first)

| # | Flow | Trigger | Real reference it returns | Why deterministic |
|---|------|---------|---------------------------|-------------------|
| 1 | Book a Service Visit | Repair Triage says yes to booking | `SVC-` | An appointment slot is a commitment |
| 2 | Request a Repair Quote | "how much to fix X" | `QUO-` | Pricing comes from the policy table, not a guess |
| 3 | Check Order or Service Status | "status of SVC-1042" | (status read) | A status lookup is a database read |
| 4 | Reserve / Hold a Machine | "hold Medieval Madness" | `HOLD-` | A hold changes inventory state, hard 48-hour expiry |
| 5 | Trade-In Valuation Start | "trade in my Firepower" | `TRD-` | A valuation offer follows a rate table |

### Live Build Checklist - Segment 2

- [ ] Author `T02_RepairTriage` (machine+symptom question, grounded playbook search, booking offer, condition branch)
- [ ] Bind the `SearchAndSummarizeContent` node to the **repair playbook** knowledge source so triage resolves
- [ ] Register the connections the flow needs (Dataverse or SharePoint, Office 365 Outlook)
- [ ] Create the **Book a Service** Power Automate flow (`MachineTitle`, `Symptom`, `PreferredWindow`, `ContactEmail`)
- [ ] Add a Power Automate **approval** step before the booking is committed
- [ ] Replace the `MAKER TODO` handoff in `T02_RepairTriage` with the flow action, passing `MachineAndSymptom`
- [ ] Validate topic YAML via `/copilot-studio:validate`
- [ ] Test the triage-to-booking path in the test panel

### Demo Prompt Set - Segment 2

| Prompt | Expected behavior |
|--------|-------------------|
| "My flipper feels weak on my Godzilla." | Routes to Repair Triage, gives level + button check, routes to Standard service, offers booking |
| "Yes, book the visit." | Invokes the Book a Service flow, approval fires, returns a real `SVC-` reference and confirmed window |
| "There's a burning smell when I turn it on." | Escalates: unplug immediately, do not power on, Priority service |
| "Can you help me rewire the transformer myself?" | Declines the unsafe DIY, recommends a technician / service visit |

---

## Segment 3 - Autonomous Agents & Event Triggers (2:00 - 2:50)

_A repair-intake or trade-in form lands in SharePoint, an event trigger fires, and the agent processes it autonomously with no user in the chat. This is the document-processor pattern. The mini-exercise wires an event trigger to autonomous instructions._

### Time Table

| Time | Activity |
|------|----------|
| 2:00 - 2:08 | Conversational vs autonomous; what an event trigger is; billing impact |
| 2:08 - 2:24 | Add "When an item is created in SharePoint" trigger; define the payload |
| 2:24 - 2:38 | Write the autonomous plan: read the intake row, triage, create a booking or trade-in record |
| 2:38 - 2:46 | Debug with the activity map; discuss the 15-consecutive-call guardrail |
| 2:46 - 2:50 | Segment wrap; the MCP option for pro-code extension |

### Talking Points

- **Autonomous means no user prompt.** Event triggers let the agent act in response to an external event instead of a user message. The orchestrator turns the **trigger payload** plus the agent's instructions into a plan and executes it. This capability is **only available when generative orchestration is on**. References: <https://learn.microsoft.com/microsoft-copilot-studio/authoring-triggers-about> and <https://learn.microsoft.com/microsoft-copilot-studio/guidance/autonomous-agents>
- **The Contoso event.** A repair-intake or trade-in form is submitted and lands as a new item in a SharePoint list. The **"When an item is created in SharePoint"** trigger fires. Other examples in the docs: "When a file is created in OneDrive", "When a task is completed in Planner", and a **Recurrence** (time-based) trigger. Reference: <https://learn.microsoft.com/microsoft-copilot-studio/authoring-triggers-about>
- **Author the trigger from Overview > Triggers.** On the agent's **Overview** page, go to the **Triggers** section, select **Add trigger**, choose the event, provide the maker's authentication, then define the event parameters and the **trigger payload**. Triggers ship a default payload; you add your own content and instructions. Reference: <https://learn.microsoft.com/microsoft-copilot-studio/authoring-trigger-event>
- **The payload plus instructions drive the plan.** The trigger payload carries the intake data (machine title, reported symptom, contact). Trigger-level instructions plus the agent's own instructions tell the orchestrator which topic, tool, or flow to call - for Contoso, triage the symptom against the playbook and create a **Book a Service** row, or start a **Trade-In Valuation**. Reference: <https://learn.microsoft.com/microsoft-copilot-studio/faqs-generative-orchestration>
- **Billing impact is real.** Enabling event triggers changes how billing is calculated (Copilot Credits) because the agent can run without a user. Say this out loud so learners scope pilots deliberately. Reference: <https://learn.microsoft.com/microsoft-copilot-studio/requirements-messages-management>
- **Debug with the activity map.** Autonomous runs record an activity trail: which action or topic the agent called and why. When an autonomous plan misses an input, the activity map is where you find the gap. Keep **consecutive action/topic calls under 15** so a plan does not run away. Reference: <https://learn.microsoft.com/microsoft-copilot-studio/authoring-triggers-about>
- **Trigger connectors respect data policies.** Which triggers are available depends on your organization's DLP policies, configured in Power Automate by an admin. The trigger connector authenticates as the **agent maker's** account, so the maker can only trigger on systems they can access. Reference: <https://learn.microsoft.com/microsoft-copilot-studio/authoring-triggers-about>
- **Pro-code extension - MCP (optional, if time allows).** When a capability is already a well-formed external tool, connect it as an **MCP** tool. Copilot Studio supports the **Streamable HTTP** transport only; **SSE was deprecated and is no longer supported for MCP after August 2025**. Add via the **MCP onboarding wizard** (Tools > Add a tool > New tool > Model Context Protocol), which handles None / API key / OAuth 2.0 auth. MCP requires generative orchestration. For a Python server, **FastMCP** turns docstrings into tool descriptions and type hints into parameter schemas; serve it over Streamable HTTP. References: <https://learn.microsoft.com/microsoft-copilot-studio/agent-extend-action-mcp> and <https://modelcontextprotocol.io/specification>
- **PP-WAF - Performance Efficiency.** Autonomous background processing removes a human step from routine intake; keep the plan short and the instruction budget tight. Reference: <https://learn.microsoft.com/power-platform/well-architected/performance-efficiency/>

### Autonomous Flow - Contoso Repair Intake

1. A customer submits the **Repair Intake** form; a row is created in the SharePoint list `RepairIntake`.
2. The **"When an item is created in SharePoint"** trigger fires and sends the payload (machine, symptom, contact, preferred window) to the agent.
3. The orchestrator triages the symptom against the **repair playbook** knowledge source.
4. It calls the **Book a Service** flow to create a `ServiceBookings` row and a `SVC-` reference.
5. It sends the customer a confirmation via the Outlook connector, and (optional) posts a summary to the staff Teams channel.
6. The **activity map** records each step for audit.

### FastMCP Reference Sketch (optional pro-code tool)

```python
# mcp_servers/pinball_parts/server.py
from fastmcp import FastMCP

mcp = FastMCP("pinball-parts")

@mcp.tool()
def lookup_part_availability(machine: str, part: str) -> dict:
    """Return parts-stock and lead time for a repair part.

    Args:
        machine: The machine title (Godzilla Premium, Medieval Madness, ...).
        part: The part or assembly (coil sleeve, flipper linkage, DMD, ...).
    """
    # Read a local parts index; the flow owns the actual order commitment.
    return parts_index.lookup(machine, part)

if __name__ == "__main__":
    # stdio for local dev; serve Streamable HTTP for Copilot Studio.
    # SSE is no longer supported for MCP after Aug 2025.
    mcp.run()
```

### Live Build Checklist - Segment 3

- [ ] Create the SharePoint list `RepairIntake` with columns for machine, symptom, contact, preferred window
- [ ] Confirm the SharePoint trigger connector is allowed by the tenant DLP policy
- [ ] On **Overview > Triggers**, add **"When an item is created in SharePoint"**
- [ ] Define the trigger payload and the autonomous instructions (triage, then book or start a trade-in)
- [ ] Test by submitting an intake row; watch the plan run with no chat input
- [ ] Open the **activity map** and confirm each action fired with the right inputs
- [ ] (Optional) Add a FastMCP tool via the onboarding wizard for a parts lookup
- [ ] Note the Copilot Credits billing impact before enabling in a shared environment

### Demo Prompt Set - Segment 3 (event-driven, not chat)

| Event | Expected behavior |
|-------|-------------------|
| A new `RepairIntake` row: "Godzilla Premium, left flipper weak, weekend" | Trigger fires; agent triages, calls Book a Service, writes a `SVC-` row, emails confirmation |
| A trade-in intake row: "Firepower, EM, Project grade" | Agent starts the Trade-In Valuation, writes a `TRD-` record, flags specialist confirmation |
| A malformed intake row (missing machine) | Activity map shows the missing input; agent requests follow-up rather than inventing a booking |

---

## Segment 4 - Deployment, Analytics, and ROI (3:00 - 3:50)

_Publish to the three targets, walk Analytics, build the Savings ROI tile, define custom metrics, and lay down governance. The mini-exercise: publish and read a real KPI._

### Time Table

| Time | Activity |
|------|----------|
| 3:00 - 3:08 | Publish once, connect channels; Teams / M365 Copilot / SharePoint |
| 3:08 - 3:20 | Analytics: the built-in KPIs; conversational vs autonomous |
| 3:20 - 3:30 | Savings calculator ROI tile; up to three custom metrics; themes to eval sets |
| 3:30 - 3:40 | Native agent evaluations; App Insights KQL |
| 3:40 - 3:48 | Security, DLP, governance, CoE |
| 3:48 - 3:50 | Course wrap, resources, Q&A pointers |

### Talking Points

- **Publish once, connect channels.** Publishing updates every connected channel at the same time, so re-publish after any edit. Reference: <https://learn.microsoft.com/microsoft-copilot-studio/publication-fundamentals-publish-channels>
- **The three Contoso targets.** **Microsoft 365 Copilot** and **Microsoft Teams** are served by one **Teams and Microsoft 365 Copilot** channel; **SharePoint** is a separate channel for embedding contextual help on a site. Publishing to M365 Copilot submits the agent as a **request** in the Microsoft 365 admin center, which an admin approves before org users see it. Keep **Authenticate with Microsoft** on so the agent works across Teams, M365 Copilot, and SharePoint with Entra ID. Reference: <https://learn.microsoft.com/microsoft-copilot-studio/publication-add-bot-to-microsoft-teams>
- **Honesty note on the SharePoint channel.** The new agent experience has listed the SharePoint channel as not yet available in that specific experience, while the classic experience and the broad publishing docs describe SharePoint as a supported native channel. Confirm the channel is present in your tenant's experience before you demo the SharePoint publish live. Reference: `Contoso Pinball Gallery Concierge/docs/ms-learn-sources.md`
- **Built-in conversational KPIs.** Every published agent emits analytics from the first conversation: **Total Sessions**, **Engagement Rate**, **Resolution Rate** (confirmed or implied), **Escalation Rate**, **Abandon Rate** (an engaged session that ends without resolution or escalation after **60 minutes**), and **CSAT** (1 to 5, from the End of Conversation survey). Test-panel traffic is excluded from Analytics. References: <https://learn.microsoft.com/microsoft-copilot-studio/analytics-overview> and <https://learn.microsoft.com/microsoft-copilot-studio/guidance/deflection-overview>
- **The Savings calculator produces a defensible ROI tile.** On the agent's **Analytics** page, the **Savings** area lets you enter the estimated time or money saved per run or per tool. Copilot Studio computes totals in real time against successful runs in the period and updates retroactively when you change inputs - an ROI tile with no data engineering. References: <https://learn.microsoft.com/microsoft-copilot-studio/analytics-cost-savings> and <https://learn.microsoft.com/microsoft-copilot-studio/guidance/agent-business-value-tell-value-story>
- **Up to three custom metrics, defined in natural language.** Copilot Studio scores a sample of sessions against your definition and shows each metric as a labeled **donut graph** under **Custom metrics**. For Contoso, a good one is "share of sessions where the customer got a grounded price or availability without escalation." Reference: <https://learn.microsoft.com/microsoft-copilot-studio/analytics-custom-metrics>
- **Autonomous agents get their own KPIs.** For agents that run on event triggers rather than chat, analytics reports **run outcomes, trigger use, tool use, and knowledge-source use** - the right lens for the Segment 3 repair-intake agent. Reference: <https://learn.microsoft.com/microsoft-copilot-studio/analytics-improve-agent-effectiveness>
- **Themes become eval test sets in one click.** Copilot Studio groups generative questions into **themes**; any theme can be turned into an evaluation test set with one select. That is the on-ramp from "what are people actually asking" to a regression suite. Reference: <https://learn.microsoft.com/microsoft-copilot-studio/analytics-themes>
- **Native agent evaluations (GA).** Agent evaluations are **generally available as of March 2026**: build a **test set** by hand, by import, or **generated from your knowledge and topics**; grade with text-match, similarity, and quality graders; inspect each case with an **activity map**; and **compare agent versions** side by side. **Multi-turn (full-conversation) evaluation is GA** (up to 20 test cases per conversational test set). Seed the set from `evals/eval-set.md`. Reference: <https://learn.microsoft.com/microsoft-copilot-studio/analytics-agent-evaluation-intro>
- **Deep telemetry with Application Insights.** Connect from **Settings > Analytics**; the agent then emits logged messages, topic-trigger events, and custom telemetry for KQL analysis. Reference: <https://learn.microsoft.com/microsoft-copilot-studio/advanced-bot-framework-composer-capture-telemetry>
- **Security and governance.** Entra ID SSO, per-agent content moderation, DLP classification of connectors (the **most restrictive DLP policy wins**), solution-aware ALM (dev to test to prod), and a **CoE Starter Kit** inventory entry. References: <https://learn.microsoft.com/microsoft-copilot-studio/security-and-governance> and <https://learn.microsoft.com/power-platform/guidance/coe/starter-kit>
- **PP-WAF - Security and Operational Excellence** are the Segment 4 pillars. References: <https://learn.microsoft.com/power-platform/well-architected/security/> and <https://learn.microsoft.com/power-platform/well-architected/operational-excellence/>

### Sample KQL - Sessions and Messages per Day (last 30 days)

```kusto
// Common adoption starting point once App Insights is connected.
requests
| where timestamp > ago(30d)
| summarize sessions = dcount(session_Id), messages = count() by bin(timestamp, 1d)
| render timechart
```

The same pattern answers top topics, escalation rate over time, agent latency, and peak-hour volume.

### ROI Story - Contoso Pinball Gallery Concierge

| Value driver | Metric to show | Where to read it |
|--------------|----------------|------------------|
| Efficiency | Hours saved on inventory and warranty questions the Concierge deflects | Savings calculator |
| Quality | Resolution rate, escalation rate, groundedness | Analytics Overview + Effectiveness |
| Revenue | Holds placed and trade-ins started through the agent | Custom metric (donut) |
| Autonomy | Repair-intake runs completed without staff touch | Autonomous KPIs (run outcomes, tool use) |

### Test Matrix - Contoso Pinball Gallery Concierge

| Layer | Tool | What we cover |
|-------|------|---------------|
| Unit | Copilot Studio test panel | Each topic's trigger + happy path from `evals/eval-set.md` |
| Scenario | Test panel multi-turn | Triage-to-booking with follow-ups |
| Batch | Native agent evaluations (GA) | Inventory, repair, research, warranty, flow-handoff, and out-of-scope cases; quality + similarity graders |
| Batch (scale) | Copilot Studio Kit | Optional Direct Line regression suite; complements native evaluations |
| Integration | Teams / SharePoint channel | End-to-end install, auth, rendering |
| Regression | Native eval set + solution export | Re-run and version-compare before every publish |

### Security & Governance Checklist

- [ ] Authentication: Entra ID, **Authenticate with Microsoft** on
- [ ] DLP policy: Dataverse/SharePoint and Outlook connectors classified; unknowns blocked
- [ ] Content moderation set for the audience
- [ ] Secrets in environment variables (never in YAML)
- [ ] Solution-aware deployment (dev to test to prod), connection references reset per environment
- [ ] CoE inventory entry for the agent
- [ ] Responsible-AI notice in conversation starters; human-in-the-loop on the booking approval

### Live Build Checklist - Segment 4

- [ ] Publish; add the **Teams and Microsoft 365 Copilot** channel; keep **Make available in Microsoft 365 Copilot** selected
- [ ] Confirm the **SharePoint** channel is present in your experience, then add it
- [ ] Submit the M365 Copilot request; note the admin-approval step
- [ ] On **Analytics**, read Total Sessions, Engagement, Resolution, Escalation, Abandon, CSAT
- [ ] Enter Savings calculator inputs to produce the ROI tile
- [ ] Define one custom metric in natural language; review the donut
- [ ] Turn a **theme** into an evaluation test set; run native agent evaluations seeded from `evals/eval-set.md`
- [ ] Connect Application Insights; run the sample KQL
- [ ] Tag the DLP policy; export the solution from dev into test; file the CoE entry

### Demo Prompt Set - Segment 4

| Prompt / action | Expected behavior |
|-----------------|-------------------|
| Publish, then chat in Teams: "Do you have Jaws?" | Confirms Jaws Premium, Stern 2024, Museum, $10,400 through the Teams channel |
| (Batch) Run the eval set | Evaluation shows pass/fail + graded score per case |
| "Show analytics for this week." | Instructor walks the KPI Overview and the Savings tile |
| "Email the confirmation to external@gmail.com" | DLP / auth path blocks the external address if policy is set |

---

## Course Wrap & Resources

### Pro-Code Bridge - The Copilot Studio VS Code Extension (GA)

_Optional closer for the developers in the room; ties the no-code build to real source control._

- **What it is.** The Microsoft Copilot Studio extension for Visual Studio Code is **generally available**. Clone an agent from Copilot Studio to your machine, edit its **agent definition YAML** (`.mcs.yml`) locally, manage it with **Git and pull requests**, then apply changes back to your environment.
- **Why it matters here.** It turns a portal-authored agent into a versioned artifact with diffs and code review. The topic stubs in `Contoso Pinball Gallery Concierge/topics/` are already in the `.mcs.yml` shape the extension reads.
- **The hook for this audience.** Microsoft's own docs name **GitHub Copilot and Claude Code** as authoring agents you can point at the YAML - agent-driven authoring of an agent.
- **Caveat.** The two topic files are deliberately **stubs**, not a complete deployable agent. To deploy them, scaffold the agent shell (generative orchestration on), bind the knowledge sources so each `SearchAndSummarizeContent` node resolves, and replace the T02 `MAKER TODO` handoff with the real Book a Service action. Do any `.mcs.yml` edits through the `@copilot-studio:*` sub-agents.
- Reference: <https://learn.microsoft.com/microsoft-copilot-studio/visual-studio-code-extension-overview>

### Recap - What We Built

- One Copilot Studio agent, the **Contoso Pinball Gallery Concierge**, progressively enriched across four segments.
- Segment 1: an FAQ-style agent grounded in three knowledge sources. Segment 2: the Repair Triage topic and a Book a Service flow with an approval step. Segment 3: an autonomous repair-intake agent on a SharePoint event trigger. Segment 4: published to three channels, measured with Analytics, the Savings ROI tile, custom metrics, and native evaluations, governed with DLP and CoE.

### PP-WAF Pillar Recap

| Pillar | Where we applied it |
|--------|---------------------|
| Experience Optimization | Segment 1 persona and grounded answers, Segment 2 clear topic routing |
| Reliability | Segment 2 grounded triage and deterministic flows, Segment 3 auditable autonomous plan |
| Performance Efficiency | Segment 3 background event-driven processing |
| Security | Segment 4 DLP, auth, moderation, approval in the loop |
| Operational Excellence | Segment 1 environment strategy, Segment 4 CoE + ALM + analytics |

### Reference Library

- Copilot Studio docs - <https://learn.microsoft.com/microsoft-copilot-studio/>
- Power Platform Well-Architected - <https://learn.microsoft.com/power-platform/well-architected/>
- Event trigger overview - <https://learn.microsoft.com/microsoft-copilot-studio/authoring-triggers-about>
- Design autonomous agent capabilities - <https://learn.microsoft.com/microsoft-copilot-studio/guidance/autonomous-agents>
- Analytics overview - <https://learn.microsoft.com/microsoft-copilot-studio/analytics-overview>
- Savings calculator - <https://learn.microsoft.com/microsoft-copilot-studio/analytics-cost-savings>
- Custom metrics - <https://learn.microsoft.com/microsoft-copilot-studio/analytics-custom-metrics>
- Tell the value story - <https://learn.microsoft.com/microsoft-copilot-studio/guidance/agent-business-value-tell-value-story>
- Agent evaluations - <https://learn.microsoft.com/microsoft-copilot-studio/analytics-agent-evaluation-intro>
- MCP in Copilot Studio - <https://learn.microsoft.com/microsoft-copilot-studio/agent-extend-action-mcp>
- Model Context Protocol - <https://modelcontextprotocol.io/>
- Copilot Studio VS Code extension - <https://learn.microsoft.com/microsoft-copilot-studio/visual-studio-code-extension-overview>
- CoE Starter Kit - <https://learn.microsoft.com/power-platform/guidance/coe/starter-kit>

### Instructor Follow-Up

- Slide deck: `docs/warner-agents-pro-july-2026.pptx`
- Agent source: `Contoso Pinball Gallery Concierge/`
- Knowledge docs for SharePoint upload: `Contoso Pinball Gallery Concierge/knowledge/`
- Eval set: `Contoso Pinball Gallery Concierge/evals/eval-set.md`
- Issues / errata: <https://github.com/timothywarner-org/agents-pro/issues>

---

## Appendix - Bonus (Off-Contract): Where Copilot Studio Hands Off to Azure AI Foundry

> **Not on the sell page.** This appendix is **not** part of the contracted four segments. It is an optional 5-minute aside for the pro-code attendees who want to know where the no-code ceiling is and how Contoso would graduate the Concierge's heavier reasoning to Azure. Skip it if the room is business-user heavy.

**The honest tie-in.** The Concierge is a great no-code fit for inventory, triage, and research. If Contoso later needs deep multi-step reasoning (for example, a full restoration-planning agent that weighs parts availability, labor, and resale value), that heavier work is a candidate for a **Foundry prompt agent** that Copilot Studio calls as a **connected agent**.

**Verified July-2026 facts:**

- The **classic Hub + Project** agents are **deprecated** and retire **March 31, 2027**. Do not start new work there.
- The GA path is the **Microsoft Foundry Agents Service**, SDK **`azure-ai-projects>=2.3.0`**, auth via `az login` + `DefaultAzureCredential`, endpoint supplied through the **`PROJECT_ENDPOINT`** environment variable (not a connection string).
- Two agent flavors: **Prompt Agents** (server-side, created with `AIProjectClient.agents.create_version()` using a `PromptAgentDefinition`) and **Hosted Agents** (your own container).
- **MCP is a first-class tool** in Foundry, the same protocol Copilot Studio consumes.
- **The Copilot Studio bridge:** from Copilot Studio you can add a **Microsoft Foundry agent as a connected agent (preview)**, so the no-code Concierge can delegate one hard sub-task to a Foundry prompt agent and stitch the answer back.

**Tiny prompt-agent sketch (Foundry Agents Service):**

```python
# Requires: pip install "azure-ai-projects>=2.3.0"
# Auth: az login first; DefaultAzureCredential picks up the CLI session.
import os
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition

# PROJECT_ENDPOINT is the Foundry project endpoint, not a connection string.
project = AIProjectClient(
    endpoint=os.environ["PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
)

# A server-side prompt agent Contoso could connect back into Copilot Studio.
agent = project.agents.create_version(
    agent_name="pinball-restoration-planner",
    definition=PromptAgentDefinition(
        model=os.environ["MODEL_DEPLOYMENT_NAME"],
        instructions=(
            "You plan pinball restorations. Given a machine, its condition grade, "
            "and a target resale band, propose a staged restoration plan with parts, "
            "labor estimate, and go/no-go economics. Defer firm pricing to the shop."
        ),
    ),
)
```

**Reference (verify before delivery; Foundry surfaces move fast):**

- Azure AI Foundry Agents documentation - <https://learn.microsoft.com/azure/ai-foundry/agents/>
- `azure-ai-projects` (PyPI) - <https://pypi.org/project/azure-ai-projects/>
- Add a Foundry agent to Copilot Studio (preview) - <https://learn.microsoft.com/microsoft-copilot-studio/add-agent-foundry-agent>
