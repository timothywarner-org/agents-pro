# Build Steps — Escalate to Human

## Goal
When a user asks for a human, generate a clean summary that a human agent can act on.

## Steps
1. Open **Customer Service Assistant** → **Topics** → **+ New topic**.
2. Name it: **Escalate to Human**.
3. Trigger: **User says a phrase**.
4. Add trigger phrases:
   - talk to a person
   - human agent
   - representative
   - escalate this
   - this isn't working
   - complaint
   - supervisor
   - I need help now
5. Add a **Generative answers** node.
   - Paste the instructions in `topic.blueprint.yaml` under “Summarize”.
   - Save outputs to:
     - `t_issue_summary` (Text)
     - `t_priority` (Text)
6. Add a **Message** node that prints the summary and priority.
7. Optional: add an **Action** node to create a ticket or notify a Teams channel.
8. End topic.

