# Deterministic Flow Ideas -- the "act, do not improvise" layer

Generative answers are great for *telling* a customer something. But when the customer wants to *do* something with an exact, auditable outcome -- a booking, a quote, a status check -- you want a **deterministic flow**: a fixed path that runs the same way every time and returns a **real** reference number instead of a hallucinated one.

In Copilot Studio these are built as **Power Automate flows** (actions/tools the agent calls) or as classic **deterministic topics** with fixed steps. The rule of thumb from Microsoft guidance: if the business says "the agent must follow these exact steps," make it deterministic.

Each flow below is a spec a maker can build in an hour. Inputs, steps, outputs, and where the agent hands off.

---

## Flow 1 -- Book a Service Visit (top priority, wires into T02_RepairTriage)

- **Trigger:** called from the Repair Triage topic when the customer says yes to booking.
- **Inputs:** `MachineTitle` (text), `Symptom` (text), `PreferredWindow` (choice: this week / next week / weekend), `ContactEmail` (text).
- **Steps:**
  1. Validate the inputs are non-empty (deterministic guard).
  2. Create a row in a **Dataverse** table `ServiceBookings` (or a SharePoint list for a lighter demo).
  3. Generate a booking reference: `SVC-` + sequential or GUID short.
  4. (Optional) Send a confirmation email via the Office 365 Outlook connector.
- **Outputs:** `BookingReference` (text), `ConfirmedWindow` (text), `Status` = "Booked".
- **Agent handoff:** the Concierge reports the reference and window verbatim from the flow output. It never invents these.
- **Why deterministic:** an appointment slot is a commitment. A generated slot that does not exist erodes trust instantly.

---

## Flow 2 -- Request a Repair Quote

- **Trigger:** called when a customer asks "how much to fix X."
- **Inputs:** `MachineTitle` (text), `Symptom` (text).
- **Steps:**
  1. Map the symptom to a **service tier** using a fixed lookup (weak flipper -> Standard, display fault -> Standard or Premium, etc.). This lookup mirrors `repair-playbook.md`.
  2. Return the tier's **price band** from `warranty-and-services.md`.
  3. Create a `QuoteReference`: `QUO-` + short id.
- **Outputs:** `Tier` (text), `PriceBand` (text, e.g. "$150 - $350"), `Turnaround` (text), `QuoteReference` (text).
- **Agent handoff:** Concierge states the band and reference and notes a specialist confirms the firm price.
- **Why deterministic:** pricing must come from the policy table, not from a model guessing a number.

---

## Flow 3 -- Check Order or Service Status

- **Trigger:** "what's the status of SVC-1042" or "check my order."
- **Inputs:** `ReferenceNumber` (text).
- **Steps:**
  1. Validate the reference format (`SVC-` / `QUO-` / `ORD-`).
  2. Look up the row in Dataverse/SharePoint.
  3. If found, return status; if not, return a clear "not found, check the number" message.
- **Outputs:** `Status` (text), `LastUpdated` (date), `Found` (boolean).
- **Why deterministic:** a status lookup is a database read. There is exactly one correct answer.

---

## Flow 4 -- Reserve / Hold a Machine (48-hour hold)

- **Trigger:** "can you hold Medieval Madness for me."
- **Inputs:** `MachineTitle` (text), `ContactEmail` (text).
- **Steps:**
  1. Check the machine is currently `In stock` in the inventory source.
  2. If yes, write a hold row with a 48-hour expiry timestamp.
  3. Return a `HoldReference` and the expiry time.
  4. If the machine is sold or on hold, offer the waitlist instead.
- **Outputs:** `HoldReference` (text), `ExpiresAt` (datetime), `Placed` (boolean).
- **Why deterministic:** a hold changes inventory state and has a hard expiry. That is transactional, not conversational.

---

## Flow 5 -- Trade-In Valuation Start

- **Trigger:** "I want to trade in my Firepower."
- **Inputs:** `MachineTitle` (text), `Era` (choice), `ConditionSelfGrade` (choice), `ContactEmail` (text).
- **Steps:**
  1. Record the trade-in request in a `TradeIns` table.
  2. Return an estimate band based on era + self-graded condition (fixed lookup).
  3. Flag that a specialist confirms in person.
- **Outputs:** `EstimateBand` (text), `TradeInReference` (text).
- **Why deterministic:** a valuation offer is a business commitment; it follows a rate table.

---

## Build order (highest value first)

1. **Book a Service Visit** -- closes the loop on the repair triage topic. Build this first.
2. **Request a Repair Quote** -- pairs with booking.
3. **Check Status** -- the natural follow-up call.
4. **Reserve / Hold** and **Trade-In** -- nice-to-have revenue flows.

## Connector and governance notes

- A lightweight demo can back all of these with **SharePoint lists** instead of Dataverse. Dataverse is the production choice.
- Flows that write data or send email need **connections**; when you import the agent to a new environment, set up the connection references.
- Keep the **most restrictive DLP policy** in mind: if a connector is blocked by policy, the flow will not run. Test in the target environment.
- Sensitive or high-impact actions (anything that spends money or commits a slot) should stay deterministic and, per responsible-AI guidance, keep a human confirmation in the loop.
