# Quick-Win Triggers and Descriptions

Two ways an agent decides what to do, and you author for both:

- **Generative orchestration (default):** the agent picks a topic, tool, or knowledge source by reading its **description**. Here you write sharp `modelDescription` text.
- **Classic orchestration (deterministic fallback):** the agent matches the user utterance to **trigger phrases**. Here you write 5 to 10 example utterances per topic.

Microsoft guidance: 5 to 10 trigger phrases per topic is the sweet spot. More is not better; variety of phrasing beats volume.

---

## Topic: Inventory Lookup (`T01_InventoryLookup`)

**Model description (generative):**
> Handles questions about which pinball machines Contoso has in stock, their price, manufacturer, year, condition, and availability, including comparisons between two machines. Grounds answers in the inventory catalog.

**Trigger phrases (classic fallback):**
- do you have Medieval Madness
- is the Godzilla Premium in stock
- what pinball machines do you have
- how much is the Twilight Zone
- check availability
- any Stern machines available
- price of Attack from Mars
- what's your cheapest machine

---

## Topic: Repair Triage (`T02_RepairTriage`)

**Model description (generative):**
> Triages a reported problem with a pinball machine (weak flipper, stuck ball, flickering display, no power, no scoring, audio fault), gives safe first-line checks from the repair playbook, and offers to book a service visit. Does not quote firm prices; hands off to the quote flow.

**Trigger phrases (classic fallback):**
- my flipper is weak
- pinball won't start
- ball keeps getting stuck
- display is flickering
- machine needs repair
- book a service appointment
- troubleshoot my pinball
- no sound coming from my machine

---

## Easy additional topics worth stubbing (each a clean win)

These are low-effort, high-payoff topics that round out the agent. Each is a "quick win" because it grounds in docs you already have.

| Topic idea | Model description (generative) | Sample trigger phrases |
|-----------|--------------------------------|------------------------|
| **Machine Research** | Answers history and background questions about a machine: designer, era, significance, features. Grounds in the history/research source. | "who made Attack from Mars", "what era is Black Knight", "tell me about Twilight Zone", "history of Medieval Madness" |
| **Warranty and Services** | Explains warranty coverage, service tiers, price bands, turnaround, delivery, trade-ins. | "what does the warranty cover", "how much is a flipper repair", "how long does service take", "do you take trade-ins" |
| **Compare Two Machines** | Compares two showroom titles on price, era, condition, and play style. | "compare Medieval Madness and Attack from Mars", "which is better Godzilla or Jaws", "cheaper than the Twilight Zone" |
| **Store Info and Hours** | Static facts: hours, location, pickup, contact. A good candidate for a simple deterministic message topic. | "what are your hours", "where are you located", "can I pick up locally" |

---

## Authoring notes (the why)

- **Front-load nouns.** Trigger phrases and descriptions should carry the words a customer actually says: machine names, "price," "repair," "warranty." That is what the NLU and semantic retrieval anchor on.
- **Do not overlap topics.** If two topics both claim "repair" phrasing, the agent shows a "did you mean" disambiguation. Keep each topic's phrases distinct.
- **Descriptions are the contract in generative mode.** A weak `modelDescription` is the number-one cause of the wrong topic firing. Spend the words there, not on adding a 20th trigger phrase.
