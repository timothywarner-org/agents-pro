# Build Steps — Request Missing Info

## Goal
When the agent isn’t confident, it asks a human reviewer for exactly what it needs.

## Steps
1. Open **Document Processor Agent** → **Topics** → **+ New topic**.
2. Name it: **Request Missing Info**.
3. Trigger: **The agent chooses**.
4. Add a **Generative answers** node:
   - Paste instructions from `topic.blueprint.yaml`.
   - Save output to `t_request_message`.
5. Add an **Action** node (recommended) that posts to a Teams channel via Power Automate.
6. Add a **Message** node confirming what was sent.
7. End.

