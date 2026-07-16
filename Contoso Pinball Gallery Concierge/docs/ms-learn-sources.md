# MS Learn Grounding Sources

The **pinball content** in this folder is invented for teaching. The **Copilot Studio facts** -- how orchestration, knowledge grounding, topics, deterministic flows, and publishing to M365 Copilot / Teams / SharePoint work -- are grounded in Microsoft Learn. These are the pages consulted when building this asset pack (verified July 2026).

## Orchestration and AI capabilities

- Orchestrate agent behavior with generative AI -- <https://learn.microsoft.com/microsoft-copilot-studio/advanced-generative-actions>
- Apply generative orchestration capabilities (architecture, custom triggers) -- <https://learn.microsoft.com/microsoft-copilot-studio/guidance/generative-orchestration>
- Explore AI capabilities in Copilot Studio -- <https://learn.microsoft.com/microsoft-copilot-studio/guidance/ai-capabilities>
- Design effective language understanding (generative vs classic, NLU/NLU+) -- <https://learn.microsoft.com/microsoft-copilot-studio/guidance/language-understanding>
- Choose how to control the conversation (deterministic vs generative) -- <https://learn.microsoft.com/microsoft-copilot-studio/guidance/voice-agents-control-conversation>

## Knowledge and grounding

- Knowledge sources summary (agent-level vs topic-level, moderation, semantic search) -- <https://learn.microsoft.com/microsoft-copilot-studio/knowledge-copilot-studio>
- Enhance AI responses with Retrieval Augmented Generation (RAG) -- <https://learn.microsoft.com/microsoft-copilot-studio/guidance/retrieval-augmented-generation>
- Use public websites to improve generative answers -- <https://learn.microsoft.com/microsoft-copilot-studio/guidance/generative-ai-public-websites>
- Add Copilot connectors as a knowledge source -- <https://learn.microsoft.com/microsoft-copilot-studio/knowledge-copilot-connectors>

## Topics, triggers, deterministic flows

- Create and edit topics -- <https://learn.microsoft.com/microsoft-copilot-studio/authoring-create-edit-topics>
- Follow topic authoring best practices -- <https://learn.microsoft.com/microsoft-copilot-studio/guidance/topic-authoring-best-practices>
- Design effective trigger phrases (5 to 10 sweet spot) -- <https://learn.microsoft.com/microsoft-copilot-studio/guidance/trigger-phrases-best-practices>
- Triggering topics -- <https://learn.microsoft.com/microsoft-copilot-studio/guidance/triggering-topics>
- Use agent tools to extend and automate agents -- <https://learn.microsoft.com/microsoft-copilot-studio/guidance/agent-tools>

## VS Code extension and the .mcs.yml agent definition

- Overview of the Copilot Studio VS Code extension (GA) -- <https://learn.microsoft.com/microsoft-copilot-studio/visual-studio-code-extension-overview>
- Edit agent components in VS Code (topics are AdaptiveDialog; YAML structure) -- <https://learn.microsoft.com/microsoft-copilot-studio/visual-studio-code-extension-edit-agent-components>

## Publishing to channels

- Publish agents to channels and clients -- <https://learn.microsoft.com/microsoft-copilot-studio/guidance/channels>
- Key concepts: publish and deploy your agent -- <https://learn.microsoft.com/microsoft-copilot-studio/publication-fundamentals-publish-channels>
- Connect and configure an agent for Teams and Microsoft 365 -- <https://learn.microsoft.com/microsoft-copilot-studio/publication-add-bot-to-microsoft-teams>
- Publish agents for Microsoft 365 Copilot -- <https://learn.microsoft.com/microsoft-365/copilot/extensibility/publish>
- Manage requested Copilot Studio agents (admin approval) -- <https://learn.microsoft.com/microsoft-365/copilot/agent-essentials/agent-lifecycle/agent-copilot-studio-requested>
- Available channels for agents (SharePoint channel status) -- <https://learn.microsoft.com/microsoft-copilot-studio/agents-experience/publication-channels-overview>

## Responsible AI

- Best practices for integrating and deploying Copilot Studio (ground in trusted data, human oversight) -- <https://learn.microsoft.com/microsoft-copilot-studio/system-service-card-copilot-studio>

## Honesty note

One channel caveat surfaced in the docs: the **new agent experience** lists the SharePoint channel as not yet available in that specific preview experience, while the **classic** experience and the broader publishing docs describe SharePoint as a supported native channel. Before you demo the SharePoint publish live, confirm the channel is present in your tenant's experience, because which channels appear depends on the agent experience and admin settings. Do not promise a channel on stage you have not seen in your own environment.
