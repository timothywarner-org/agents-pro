# Topic Blueprints (Learner-Friendly “Source Code”)

Copilot Studio topics are built in a visual canvas, not authored as code files.
These YAML and Markdown files are **blueprints** you can copy/paste from while building topics in the UI.

## How to use these files in class

1. Pick an agent folder (customer-service-assistant, employee-onboarding-agent, document-processor-agent).
2. Open the topic folder (for example `topics/T01_ReturnsAndRefunds/`).
3. Follow `topic.build.md` in Copilot Studio, step by step.
4. Use `topic.blueprint.yaml` as your “truth table” for triggers, variables, branching, and prompts.
5. Use files in `assets/` for consistent testing and demos.

## Naming conventions used here

- Topic folders start with `T##_` so learners can move left-to-right.
- Topic variables start with `t_` (topic) so they’re easy to spot.
- Sample payloads use `snake_case` keys so they’re readable outside the product.

## “Good citizen” notes

- Aim for **5–10 trigger phrases** per topic so Copilot Studio learns reliably.
- Keep one intent per topic, then use **Go to** nodes to hand off to other topics.
- When you call Power Automate, treat it like a function:
  - validate inputs first
  - pass structured variables in
  - return structured variables out

