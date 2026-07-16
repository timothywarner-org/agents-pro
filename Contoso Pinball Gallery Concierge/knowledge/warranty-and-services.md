# Contoso Pinball Gallery -- Warranty and Services

Grounds the Concierge's answers about warranty coverage, service tiers, pricing bands, turnaround, and delivery. Prices are bands, not quotes: the deterministic **Request a Quote** flow returns the actual number.

Fictional policies for course demos.

---

## Warranty

Every machine sold by Contoso includes a **90-day mechanical warranty** from delivery.

**Covered:** coils, switches, flipper assemblies, displays (as delivered), power supply, and any mechanism that was working at delivery and fails under normal home use.

**Not covered:** cosmetic wear, playfield inserts, consumables (rubbers, balls, bulbs), customer-caused damage, damage from opening the backbox, and machines sold **Project / as-is**.

**Project-grade machines** are sold with **no warranty** and are clearly marked as-is. That is the trade-off for the lower price.

Extended coverage: an optional **12-month Gallery Care plan** is available at purchase for **8 percent of sale price**, covering the same components plus one free annual tune-up.

---

## Service tiers

| Tier | What it covers | Price band | Turnaround |
|------|----------------|------------|------------|
| **Diagnostic** | On-site or in-shop assessment, written findings | $95 flat (credited toward repair) | Same week |
| **Standard** | Common fixes: flipper rebuild, switch/opto, coil, ball trough, leveling | $150 - $350 | 3 - 5 business days |
| **Premium** | Display conversion (DMD-to-LED), board-level repair, mech replacement, audio upgrade | $350 - $800 | 1 - 2 weeks |
| **Restoration** | Full teardown, playfield, cosmetics, concours work | Quoted per project | 4 - 12 weeks |
| **Priority** | Any tier, expedited (burning smell, dead-on-arrival) | Tier price + 40 percent | 24 - 48 hours |

House-call surcharge: **$60** within the metro service area; mileage beyond.

---

## What is a safe customer step vs. a service call

Customers can safely: level the machine, swap the pinballs, check the power switch and outlet, and check for a binding flipper button. Everything else -- coils, switches, displays, boards, anything inside the backbox -- is a service call. See `repair-playbook.md` for symptom-by-symptom triage.

---

## Booking, quotes, and status

These are handled by **deterministic flows**, not by the Concierge guessing:

- **Book a Service Visit** -- collects machine, symptom, and preferred window; returns a confirmed booking reference.
- **Request a Repair Quote** -- collects machine and symptom; returns a price band and a quote reference.
- **Check Order or Service Status** -- takes a reference number; returns current status.

The Concierge should always route these to the flow so the customer gets a real reference number, not an invented one.

---

## Delivery and setup

- **Local white-glove delivery and setup:** $180 within the metro area, includes leveling and a play-test.
- **Freight (crated, out of area):** quoted by weight and distance.
- **Local pickup:** free, by appointment.
- **Holds:** a machine can be placed on a **48-hour hold** with contact details via the Reserve flow. Holds expire automatically.

---

## Trade-ins

Contoso accepts trade-ins toward a purchase. Bring the machine's title, era, and condition; the **Request a Quote** flow can start a trade-in valuation, which a specialist confirms in person. Trade-in offers depend on condition grade and current demand.
