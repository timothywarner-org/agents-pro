# Knowledge Upload Metadata -- the descriptions that drive retrieval

**Why this file exists.** In generative orchestration, the agent decides *which knowledge source to search* by reading each source's **name and description** -- not its contents. A vague description ("company docs") makes the orchestrator guess; a sharp one routes the right query to the right document on the first try. Metadata is the cheapest accuracy you will ever buy. Paste these when you add each source in Copilot Studio (**Knowledge** > add source > **Description**), or set them in the `.mcs.yml` `mcs.metadata.description` field if you author code-first.

The pattern for a good source description: **what it contains + what questions it answers + when the agent should reach for it.** Front-load the nouns a user would say (machine names, "price," "repair," "warranty") so semantic retrieval has strong anchors.

---

## Source 1 -- Inventory Catalog

- **Display name:** `Contoso Inventory Catalog`
- **File:** `inventory-catalog.md`
- **Description (paste this):**
  > Current Contoso Pinball Gallery showroom inventory. Use this source for any question about which pinball machines are available, their manufacturer, year, era, condition grade, price in USD, and stock status (in stock, on hold, sold, waitlist). Covers titles such as Medieval Madness, Godzilla, Jaws, Attack from Mars, Twilight Zone, Addams Family, Black Knight, Firepower, and Fireball. Reach for this whenever a user asks about buying, price, availability, condition, or comparing two machines.

## Source 2 -- Repair and Triage Playbook

- **Display name:** `Contoso Repair Playbook`
- **File:** `repair-playbook.md`
- **Description (paste this):**
  > First-line repair triage for pinball symptoms. Use this source when a user reports a problem with a machine: weak or dead flipper, ball getting stuck, display flickering or blank, machine will not power on, scoring or targets not registering, or audio cutting out. Gives safe customer-level checks and the likely service tier. Use it to triage a symptom before offering to book a service visit. Does not cover pricing details (see the Warranty and Services source).

## Source 3 -- History and Research Reference

- **Display name:** `Contoso Pinball History and Research`
- **File:** `pinball-history-research.md`
- **Description (paste this):**
  > Background on pinball history, eras, and manufacturers, and deep dives on the specific titles Contoso carries. Use this source for research and history questions: who designed or made a machine, what era it belongs to (electromechanical, solid-state, DMD, modern LCD), what makes it significant, its signature features, and which showroom titles are related. Reach for it when a user wants to learn about a machine rather than buy or repair it.

## Source 4 -- Warranty and Services

- **Display name:** `Contoso Warranty and Services`
- **File:** `warranty-and-services.md`
- **Description (paste this):**
  > Contoso warranty coverage, service tiers, price bands, turnaround times, delivery, holds, and trade-ins. Use this source when a user asks what the warranty covers, how much a repair tier costs, how long service takes, delivery and setup options, or how trade-ins work. Use it alongside the Repair Playbook: the playbook triages the symptom, this source explains cost and turnaround. Actual quotes and bookings come from the deterministic flows, not from this document.

---

## Agent-level description (for M365 Copilot / Teams / SharePoint discovery)

When you publish, the agent's own **description** is metadata too: it is how the agent shows up in the Microsoft 365 Copilot agent list, the Teams store, and admin review. Make it a discovery magnet.

- **Agent name:** `Contoso Pinball Gallery Concierge`
- **Agent description (paste in channel details / Edit details):**
  > Your expert guide to Contoso Pinball Gallery. Ask about pinball machines in stock and their prices, get first-line help with a repair, learn the history of classic and modern tables, or book a service visit. Grounded in Contoso's live inventory, repair playbook, and service policies.
- **Suggested / conversation-starter prompts** (these are maker-authored metadata that make the agent feel alive on first open):
  1. "What pinball machines do you have in stock?"
  2. "My flipper feels weak -- can you help?"
  3. "Tell me about Medieval Madness."
  4. "Book a service visit."

---

## Chunking and format notes (so retrieval actually works)

- These docs use **clear headings and short sections** on purpose. Generative answers retrieve better when each fact sits under a descriptive heading, because headings become part of the searchable chunk.
- Keep **one machine or one symptom per section** so a retrieved chunk is self-contained. A customer asking about one title should not pull a chunk that blends three.
- The **quick-reference tables** exist so a single retrieved chunk can answer a comparison question ("cheapest DMD machine you have?") without stitching multiple chunks together.
- If you later move these to SharePoint, remember the agent needs `Sites.Read.All` and `Files.Read.All`, and that sources set on a generative-answers node override agent-level sources.
