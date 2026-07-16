# Contoso Pinball Gallery -- Repair and Triage Playbook

First-line triage guidance for common pinball symptoms. This document grounds the Concierge's repair triage. The goal is to give a customer **safe** first checks, then route anything real to a service visit. Nothing here asks a customer to open the backbox, touch high-voltage components, or discharge capacitors -- that is technician work.

Fictional service content for course demos.

---

## Safety first (applies to every symptom)

- Power the machine off at the switch before touching anything inside the cabinet.
- Never open the **backbox** (the upright head) or touch the transformer, high-voltage boards, or the flyback. High voltage is present even when off.
- Safe customer-level checks are limited to: the power switch, the plug, leg levelers, the ball trough (front cabinet), and the flipper buttons.
- When in doubt, book a service visit. A $95 diagnostic is cheaper than a damaged board.

---

## Symptom: Weak or dead flipper

**Likely causes:** worn coil sleeve, loose flipper linkage, dirty or misadjusted end-of-stroke (EOS) switch, weak coil.

**Safe customer checks:**
1. Is the machine level? A tilted playfield feels like a weak flipper. Adjust leg levelers.
2. Is the flipper button binding or sticky? Press and release -- it should snap back.
3. Does one flipper work and the other not? That points to a single-coil issue, which is a service fix.

**Route:** If both buttons are fine and the machine is level, this is a **service visit** (coil sleeve or linkage). Typical fix: **Standard tier**.

---

## Symptom: Ball keeps getting stuck

**Likely causes:** dirty ball, worn playfield, a stuck-up post or scoop, magnetized ball, debris in a lane.

**Safe customer checks:**
1. Where does it stick -- a ramp, a scoop, a specific lane? Note the exact spot.
2. Is the ball itself dull, chipped, or magnetized? A worn ball is a common culprit. Replacing pinballs is a safe customer step.
3. Is the machine level front-to-back and side-to-side?

**Route:** A stuck ball at a scoop or under a mech is a **service visit** (coil or opto adjustment). A dull ball is a **$25 ball set**. Repeated sticking after a ball swap: **Standard tier**.

---

## Symptom: Display flickering, dim, or blank (DMD / LCD)

**Likely causes (DMD):** aging dot-matrix display, loose display ribbon cable, display power board.
**Likely causes (LCD):** loose HDMI/ribbon, node board, backlight.

**Safe customer checks:**
1. Does it flicker from cold or all the time? Note the pattern.
2. Is there any image at all, or fully blank?
3. Do NOT open the backbox to reseat cables. This is technician work.

**Route:** Any display fault is a **service visit**. A failing plasma DMD may need a **DMD-to-LED conversion** (Premium tier). Loose ribbon is often **Standard tier**.

---

## Symptom: Machine will not power on

**Likely causes:** blown line fuse, tripped outlet, failed power switch, power supply.

**Safe customer checks:**
1. Is it plugged in and is the outlet live? Test the outlet with another device.
2. Is the cabinet power switch fully on? It is on the lower-left of the cabinet on most machines.
3. Any burning smell? If yes, unplug immediately and book service -- do not power it again.

**Route:** If the outlet is live and the switch is on with no life, this is a **service visit** (fuse or power supply). Burning smell escalates to **priority**.

---

## Symptom: Scoring or targets not registering

**Likely causes:** dirty or misaligned switch, broken switch leaf, dead opto, disconnected connector.

**Safe customer checks:**
1. Which target or switch? Be specific -- "the left orbit does not score."
2. Is it intermittent or dead?

**Route:** Switch and opto work is a **service visit**, **Standard tier**.

---

## Symptom: Sound cut out or distorted

**Likely causes:** volume set low, loose speaker connector, failing amp, aging speakers.

**Safe customer checks:**
1. Check the volume setting in the operator menu if you are comfortable, or the coin-door volume control.
2. Is it fully silent or distorted?

**Route:** Distortion or dead audio beyond the volume control is a **service visit**, **Standard tier**; speaker upgrade is optional **Premium tier**.

---

## Triage-to-tier quick map

| Symptom | Safe customer step | Most likely route |
|---------|--------------------|--------------------|
| Weak flipper | Level machine, check button | Standard service |
| Stuck ball | Swap dull ball, level | Ball set, then Standard |
| Display fault | Note pattern; do not open backbox | Standard or Premium |
| No power | Check outlet, switch, smell | Standard (Priority if burning) |
| No scoring | Identify the switch | Standard service |
| Audio fault | Check volume | Standard service |

See `warranty-and-services.md` for tier pricing, turnaround, and what warranty covers.
