# Copilot Instructions for agents-pro

## Repository Purpose
- Align every addition with the four-hour O’Reilly live course outlined in [README.md](README.md) and [course-plan.md](course-plan.md); each segment builds toward the three Copilot Studio agents.
- Keep marketing and proposal collateral synchronized with [reference/how-to-create-ai-agents-like-a-pro-markdown.md](reference/how-to-create-ai-agents-like-a-pro-markdown.md) and [reference/how-to-create-ai-agents-like-a-pro-training-proposal.md](reference/how-to-create-ai-agents-like-a-pro-training-proposal.md).
- Treat the repo as the instructor’s source of truth: capture objectives, prerequisites, success metrics, and deliverables for every agent experience.

## Key Reference Materials
- Use [copilot-studio-agents/README.md](copilot-studio-agents/README.md) as the scaffold blueprint; it documents how topics, actions, and knowledge notes interlock.
- Mirror the depth and sequencing in [copilot-studio-agents/customer-service-assistant/README.md](copilot-studio-agents/customer-service-assistant/README.md), [copilot-studio-agents/employee-onboarding-agent/README.md](copilot-studio-agents/employee-onboarding-agent/README.md), and [copilot-studio-agents/document-processor-agent/README.md](copilot-studio-agents/document-processor-agent/README.md).
- Cross-reference supporting playbooks in each `topics/`, `actions/`, and `knowledge/` folder; tables there define flow inputs, environment variables, and content calendars.

## Agent Scaffold
- Every agent folder should expose the same trio of subdirectories (`topics`, `actions`, `knowledge`) with README files that explain trigger strategy, automation design, and data sources.
- Document flows with connection references and environment variables as shown in [copilot-studio-agents/customer-service-assistant/actions/README.md](copilot-studio-agents/customer-service-assistant/actions/README.md) so solutions stay ALM-ready.
- Maintain knowledge architecture diagrams and maintenance schedules like those in [copilot-studio-agents/customer-service-assistant/knowledge/README.md](copilot-studio-agents/customer-service-assistant/knowledge/README.md); surface SharePoint scopes, crawl cadences, and review owners.

## Authoring Patterns
- Long-form guides follow the rhythm: Overview → Scenario → Success Metrics → Phased build instructions → Testing/Publishing → Sample transcript/log; reuse the five-phase structure when adding new material.
- Include Mermaid diagrams for architecture, triggers, and flow designs; imitate existing styles (e.g., fill colors, grouped subgraphs) for visual consistency.
- Capture trigger phrases, variable schemas, and step-by-step tables directly in text so Copilot Studio builders can reproduce flows without guessing.
- When introducing Power Automate integrations, list inputs/outputs, adaptive card templates, and connector licensing to reflect classroom expectations.

## Tooling & Workflows
- Perform HTML-to-Markdown conversions with the MarkItDown MCP server (`convert_to_markdown`); remove navigation, legal footers, and duplicate sections post-conversion.
- There is no automated build or test pipeline; quality comes from cross-checking timelines, flow steps, and URLs against the source proposal and marketing copies.
- Reuse sample data references (e.g., link to the copilot-studio-business repo) so learners can preload environments during the course.
- Note authentication scopes, AI Builder requirements, and autonomous trigger setup steps whenever an agent depends on premium Power Platform features.

## Style Conventions
- Headings remain Title Case and may use the existing em dash pattern for subtitles (see How to Create AI Agents Like a Pro — Training Proposal).
- Default to ASCII; only keep existing non-ASCII glyphs (em dashes) when necessary.
- Bulleted lists stay compact with `-`, tables present key metrics, and bare URLs appear inside angle brackets `<...>`.
- Keep filenames lowercase with hyphens; add new collateral as top-level `.md` files unless a new hierarchy is justified.

## Review Checklist
- Verify agenda timing, learning objectives, and deliverables align with the canonical references before finalizing edits.
- Confirm knowledge sources, triggers, and flows you mention match the details documented in the corresponding `knowledge` and `actions` READMEs.
- Ensure MarkItDown output is trimmed to course content and that all external links resolve to official Microsoft or O’Reilly resources.
- Preview diagrams and tables for readability and update dates, seat counts, and resource links when schedules shift.

Need clarification or missing patterns? Ping the maintainer before diverging from these structures.
