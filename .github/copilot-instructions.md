# Copilot Instructions for agents-pro

## Project Snapshot
- Repository curates course collateral for the “How to Create AI Agents Like a Pro” O’Reilly live training.
- Source capture: How to Create AI Agents Like a Pro.html (full marketing page).
- Authored assets: how-to-create-ai-agents-like-a-pro-markdown.md (condensed course page) and how-to-create-ai-agents-like-a-pro-training-proposal.md (executive proposal).

## Core Workflows
1. **HTML → Markdown conversions**
   - Always run the MarkItDown MCP server (`convert_to_markdown`) instead of manual parsing.
   - Strip navigation/footer noise after conversion; keep course-specific information, schedules, and links.
2. **Content authoring**
   - Proposal files follow the structure seen in how-to-create-ai-agents-like-a-pro-training-proposal.md: Executive Summary → Outcomes → Audience → Prerequisites → Agenda → Cohorts → Instructor → Resources.
   - Marketing markdown stays concise (one-paragraph overview, key outcomes, schedule, instructor, resources) mirroring how-to-create-ai-agents-like-a-pro-markdown.md.

## Editing Conventions
- Default to ASCII; introduce non-ASCII glyphs only when already present (see existing typography with en dash for segment headers).
- Headings are Title Case (`# How to Create AI Agents Like a Pro — Training Proposal`).
- Bullets use `-`; preserve compact lists (no blank separators) unless clarity demands.
- Keep external links intact and use angle brackets `<...>` for bare URLs in checklists.
- Include course dates with bolded day and em dash format (`**December 18, 2025** — 9:00 AM…`).

## Tooling & Repo Layout
- There is no build or test pipeline; focus on content accuracy.
- .vscode/settings.json only disables SARIF GitHub connection—no additional tooling.
- Add new collateral as top-level `.md` files unless a new directory hierarchy is justified.

## Quality Checklist Before PR
- Confirm MarkItDown output was post-processed: remove duplicated nav/footers and summarize sections clearly.
- Cross-check agenda segments against the original HTML to ensure timing and bullet ordering remain accurate.
- Verify all URLs resolve to the correct O’Reilly resources or course materials.
- Ensure file names remain lowercase with hyphens for readability (`course-name-detail.md`).

Need clarification or missing patterns? Ping the maintainer with proposed updates before diverging from these structures.
