# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Purpose

This is an O'Reilly Live Learning course repository for "How to Create AI Agents Like a Pro" - a 4-hour instructor-led course teaching Microsoft Copilot Studio agent development. The repository serves as the instructor's source of truth and learner reference material.

**Course Structure:**
- Segment 1: Copilot Studio Fundamentals (intro)
- Segment 2: Customer Service Assistant (beginner) - knowledge-driven FAQ bot with escalation
- Segment 3: Employee Onboarding Agent (intermediate) - Power Automate flows, authentication, approvals
- Segment 4: Document Processor Agent (advanced) - autonomous triggers, AI Builder, event-driven automation

## Architecture

### Agent Scaffold Pattern

Every agent folder (`copilot-studio-agents/{agent-name}/`) follows the same structure:
- `topics/` - Conversation paths with trigger phrases and dialog logic (YAML blueprints, not code)
- `actions/` - Power Automate flows, connectors, and tool integrations
- `knowledge/` - Data sources, generative answers config, SharePoint/OneDrive references

Topic folders use `T##_` prefix for sequencing (e.g., `T01_ReturnsAndRefunds/`). Each contains:
- `README.md` - Overview and learning objectives
- `topic.build.md` - Step-by-step Copilot Studio build instructions
- `topic.blueprint.yaml` - Truth table for triggers, variables, branching
- `assets/` - Sample payloads, test transcripts, adaptive card templates

### Key Files

- `docs/course-plan.md` - Instructor segment breakdown and learning activities
- `docs/PowerPlatform-WAF-for-CopilotStudio-Agents.md` - CAF Power Platform Well-Architected Framework guidance
- `copilot-studio-agents/_labs/` - Hands-on lab guides (Lab-00 through Lab-03)
- `copilot-studio-agents/_topics/README.md` - Topic blueprint conventions and naming standards
- `copilot-studio-agents/_automations/` - Power Automate flow templates with sample payloads

## Authoring Conventions

### Document Structure

Long-form guides follow: Overview > Scenario > Success Metrics > Phased Build Instructions > Testing/Publishing > Sample Transcript/Log

### Naming Standards

- Topic folders: `T##_TopicName` (e.g., `T01_ReturnsAndRefunds`)
- Topic variables: prefix with `t_` (e.g., `t_orderId`)
- Sample payloads: `snake_case` keys
- Filenames: lowercase with hyphens

### Mermaid Diagrams

Use existing color palette and grouped subgraph styles for architecture, triggers, and flow designs.

### Style

- Headings: Title Case, em dash pattern for subtitles
- Lists: compact with `-`
- URLs: inside angle brackets `<...>`
- ASCII default; preserve existing em dashes

## Copilot Studio Specifics

- **Topic names**: Avoid periods (`.`) - breaks solution exports
- **Event triggers**: Require generative orchestration enabled; affect billing
- **Analytics**: Test-panel interactions don't appear in Analytics
- **DLP**: Most restrictive policy wins when multiple apply

### Authoring Checklist

1. Define business goals and success metrics before custom topics
2. Create topics with Copilot or manually, then layer guardrails with system topics
3. Use generative answers sparingly; back with curated knowledge sources
4. Capture environment variables and connection references in actions notes for ALM readiness
5. Publish to sandbox first, then promote via managed solutions

## GitHub Copilot Agent and Prompts

The repository includes GitHub Copilot configurations:
- `.github/agents/copilot-studio-expert.agent.md` - Expert on Copilot Studio, Power Platform, Power Automate, and CAF WAF
- `.github/prompts/copilot-studio-architect.prompt.md` - Design and review prompt for agent blueprints
- `.github/instructions/power-platform-connector-dev.instructions.md` - Power Platform Custom Connectors JSON Schema development

## No Build System

This repository contains documentation, YAML blueprints, and sample data - no automated build or test pipeline. Quality comes from cross-checking against the course proposal, marketing materials, and Microsoft documentation.

## Key External References

- [Copilot Studio Documentation](https://learn.microsoft.com/en-us/microsoft-copilot-studio/)
- [Power Platform Well-Architected](https://learn.microsoft.com/power-platform/well-architected/)
- [Autonomous Document Processing Reference Architecture](https://learn.microsoft.com/power-platform/architecture/reference-architectures/document-processing-agent)
- [Topic Authoring Best Practices](https://learn.microsoft.com/en-us/microsoft-copilot-studio/guidance/topic-authoring-best-practices)
