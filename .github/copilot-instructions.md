# Copilot Instructions for agents-pro

## Repository Purpose

- Align every addition with the four-hour O'Reilly live course outlined in [README.md](../README.md) and [CLAUDE.md](../CLAUDE.md); the detailed instructor plan lives in [docs/course-plan-july-2026.md](../docs/course-plan-july-2026.md).
- The course's primary built-live agent is the **Contoso Pinball Gallery Concierge** (root folder `Contoso Pinball Gallery Concierge/`, see `docs/course-plan-july-2026.md`). It is ONE agent carrying the sell page's three patterns (customer service, onboarding-with-approvals, autonomous document processor) as modes across four Copilot Studio segments. The `src/copilot-studio-agent/` three-agent set below is older blueprint material; keep the two workloads distinct and don't conflate them.
- Treat the repo as the instructor's source of truth: capture objectives, prerequisites, success metrics, and deliverables for every agent experience.

## Key Reference Materials

- Use [src/copilot-studio-agent/](../src/copilot-studio-agent/) as the scaffold blueprint for the three-agent WAF teaching set; it documents how topics, actions, and knowledge notes interlock. The workload framing and pillar sequencing for this set live in [docs/PowerPlatform-WAF-for-Copilot-Studio-Agents.md](../docs/PowerPlatform-WAF-for-Copilot-Studio-Agents.md).
- Mirror the depth and sequencing in `src/copilot-studio-agent/customer-service-assistant/`, `src/copilot-studio-agent/employee-onboarding-agent/`, and `src/copilot-studio-agent/document-processor-agent/`.
- Cross-reference supporting playbooks in each `topics/`, `actions/`, and `knowledge/` folder; tables there define flow inputs, environment variables, and content calendars.
- Two top-level folders hold real, deployable `.mcs.yml` Copilot Studio agents (importable, not just documentation): `CKA Exam Prep Assistant/` and `RAI Advisor/`. When editing any `.mcs.yml` file, delegate to the `@copilot-studio:*` sub-agents.

## Agent Scaffold

- Every agent folder under `src/copilot-studio-agent/` should expose the same trio of subdirectories (`topics`, `actions`, `knowledge`) with README files that explain trigger strategy, automation design, and data sources.
- Document flows with connection references and environment variables as shown in `src/copilot-studio-agent/customer-service-assistant/actions/` so solutions stay ALM-ready.
- Maintain knowledge architecture diagrams and maintenance schedules like those in `src/copilot-studio-agent/customer-service-assistant/knowledge/`; surface SharePoint scopes, crawl cadences, and review owners.

## Authoring Patterns

- Long-form guides follow the rhythm: Overview -> Scenario -> Success Metrics -> Phased build instructions -> Testing/Publishing -> Sample transcript/log; reuse the five-phase structure when adding new material.
- Include Mermaid diagrams for architecture, triggers, and flow designs; imitate existing styles (e.g., fill colors, grouped subgraphs) for visual consistency.
- Capture trigger phrases, variable schemas, and step-by-step tables directly in text so Copilot Studio builders can reproduce flows without guessing.
- When introducing Power Automate integrations, list inputs/outputs, adaptive card templates, and connector licensing to reflect classroom expectations.

## Tooling & Workflows

- There is no automated build or test pipeline for `src/copilot-studio-agent/`; quality comes from cross-checking timelines, flow steps, and URLs against `docs/course-plan-july-2026.md` and Microsoft documentation.
- Note authentication scopes, AI Builder requirements, and autonomous trigger setup steps whenever an agent depends on premium Power Platform features.

## Style Conventions

- Headings remain Title Case and may use the existing em dash pattern for subtitles.
- Default to ASCII; only keep existing non-ASCII glyphs (em dashes) when necessary.
- Bulleted lists stay compact with `-`, tables present key metrics, and bare URLs appear inside angle brackets `<...>`.
- Keep filenames lowercase with hyphens; add new collateral under the appropriate existing folder (e.g., `docs/`, `src/copilot-studio-agent/`) unless a new hierarchy is justified.

## Review Checklist

- Verify agenda timing, learning objectives, and deliverables align with `docs/course-plan-july-2026.md` and `README.md` before finalizing edits.
- Confirm knowledge sources, triggers, and flows you mention match the details documented in the corresponding `knowledge` and `actions` folders.
- Ensure all external links resolve to official Microsoft or O'Reilly resources.
- Preview diagrams and tables for readability and update dates, seat counts, and resource links when schedules shift.

Need clarification or missing patterns? Ping the maintainer before diverging from these structures.
