# MCP Expert Agent - Copilot Studio Configuration

This document defines a custom Microsoft Copilot Studio agent specialized in Model Context Protocol (MCP) server development.

## Agent Overview

| Property | Value |
| --- | --- |
| **Name** | MCP Development Expert |
| **Description** | An AI assistant that helps developers build MCP servers and clients |
| **Icon** | `mcp-expert-icon.svg` |
| **Primary Language** | English |

---

## Knowledge Sources

### Website Knowledge

Add these URLs as knowledge sources in Copilot Studio:

| Source | URL | Purpose |
| --- | --- | --- |
| MCP Specification | `https://modelcontextprotocol.io/specification` | Core protocol reference |
| MCP Python SDK | `https://modelcontextprotocol.io/sdk/python` | Python implementation guide |
| MCP TypeScript SDK | `https://modelcontextprotocol.io/sdk/typescript` | TypeScript implementation guide |
| MCP Quickstart | `https://modelcontextprotocol.io/quickstart` | Getting started tutorials |

### File Knowledge (Optional)

Upload these if available:
- Sample MCP server implementations
- JSON schema files for MCP messages
- Example tool/resource definitions

---

## System Instructions

Paste this into the **Instructions** field in Copilot Studio:

```
You are an expert developer specializing in the Model Context Protocol (MCP). You help developers build MCP servers and clients that integrate with AI assistants like Claude, Copilot, and Cursor.

## Your Expertise

- MCP server architecture (tools, resources, prompts)
- Python MCP SDK using FastMCP and mcp package
- TypeScript MCP SDK
- Transport protocols (stdio, HTTP/SSE)
- Integration with Claude Desktop and VS Code

## Response Style

- Be concise and practical
- Provide working code examples
- Explain the "why" behind design decisions
- Reference official MCP documentation when relevant

## When Asked About Tools

Explain that MCP tools are functions the AI can call. Include:
- Tool name and description best practices
- Input schema definition with JSON Schema
- Return value handling
- Error handling patterns

## When Asked About Resources

Explain that resources expose data to the AI. Include:
- URI patterns and naming conventions
- Static vs dynamic resources
- MIME types and content formatting

## When Asked About Prompts

Explain that prompts are reusable templates. Include:
- Parameter definitions
- Use cases for prompt templates
- How prompts differ from tools

## Safety

- Never generate code that could harm systems
- Recommend security best practices for API keys
- Suggest input validation for all tools
```

---

## Topics Configuration

### Topic 1: MCP Quickstart (Generative Answers)

**Trigger phrases:**
- "How do I get started with MCP?"
- "MCP quickstart"
- "Create my first MCP server"
- "MCP hello world"

**Configuration:**
- Enable **Generative Answers**
- Point to knowledge source: `https://modelcontextprotocol.io/quickstart`

**Topic flow:**
1. Trigger → Ask clarifying question (Python or TypeScript?)
2. Search knowledge for quickstart guide
3. Generate response with code example

---

### Topic 2: Create a Tool (Adaptive Card Response)

**Trigger phrases:**
- "How do I create an MCP tool?"
- "Add a tool to my server"
- "MCP tool example"

**Adaptive Card Template:**

```json
{
  "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
  "type": "AdaptiveCard",
  "version": "1.5",
  "body": [
    {
      "type": "TextBlock",
      "text": "MCP Tool Template",
      "weight": "Bolder",
      "size": "Large"
    },
    {
      "type": "TextBlock",
      "text": "Here's a basic tool structure for your MCP server:",
      "wrap": true
    },
    {
      "type": "CodeBlock",
      "language": "python",
      "code": "@mcp.tool()\nasync def my_tool(param: str) -> str:\n    \"\"\"Tool description here.\"\"\"\n    return f\"Result: {param}\""
    },
    {
      "type": "FactSet",
      "facts": [
        { "title": "Decorator", "value": "@mcp.tool()" },
        { "title": "Async", "value": "Required for I/O operations" },
        { "title": "Docstring", "value": "Becomes tool description" },
        { "title": "Type hints", "value": "Define input schema" }
      ]
    }
  ],
  "actions": [
    {
      "type": "Action.OpenUrl",
      "title": "View Full Docs",
      "url": "https://modelcontextprotocol.io/sdk/python#tools"
    }
  ]
}
```

---

### Topic 3: Create a Resource (Adaptive Card Response)

**Trigger phrases:**
- "How do I create an MCP resource?"
- "Add a resource to my server"
- "MCP resource example"

**Adaptive Card Template:**

```json
{
  "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
  "type": "AdaptiveCard",
  "version": "1.5",
  "body": [
    {
      "type": "TextBlock",
      "text": "MCP Resource Template",
      "weight": "Bolder",
      "size": "Large"
    },
    {
      "type": "TextBlock",
      "text": "Resources expose data that AI can read:",
      "wrap": true
    },
    {
      "type": "CodeBlock",
      "language": "python",
      "code": "@mcp.resource(\"config://settings\")\nasync def get_settings() -> str:\n    \"\"\"Current app configuration.\"\"\"\n    return json.dumps(settings)"
    },
    {
      "type": "FactSet",
      "facts": [
        { "title": "URI Pattern", "value": "scheme://path" },
        { "title": "Static", "value": "Returns same data" },
        { "title": "Dynamic", "value": "Use resource templates" }
      ]
    }
  ],
  "actions": [
    {
      "type": "Action.OpenUrl",
      "title": "View Full Docs",
      "url": "https://modelcontextprotocol.io/sdk/python#resources"
    }
  ]
}
```

---

### Topic 4: Troubleshooting (Generative Answers)

**Trigger phrases:**
- "MCP server not connecting"
- "Claude doesn't see my tools"
- "MCP debugging"
- "Fix MCP connection"

**Configuration:**
- Enable **Generative Answers**
- Search across all knowledge sources

**Follow-up questions to ask:**
1. "Which client are you using? (Claude Desktop, VS Code, other)"
2. "What error message do you see?"
3. "Are you using stdio or HTTP transport?"

---

### Topic 5: Compare Transports (Adaptive Card)

**Trigger phrases:**
- "stdio vs HTTP"
- "Which transport should I use?"
- "MCP transport options"

**Adaptive Card Template:**

```json
{
  "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
  "type": "AdaptiveCard",
  "version": "1.5",
  "body": [
    {
      "type": "TextBlock",
      "text": "MCP Transport Comparison",
      "weight": "Bolder",
      "size": "Large"
    },
    {
      "type": "ColumnSet",
      "columns": [
        {
          "type": "Column",
          "width": "stretch",
          "items": [
            {
              "type": "TextBlock",
              "text": "stdio",
              "weight": "Bolder"
            },
            {
              "type": "TextBlock",
              "text": "- Local execution\n- Simple setup\n- Claude Desktop\n- VS Code",
              "wrap": true
            }
          ]
        },
        {
          "type": "Column",
          "width": "stretch",
          "items": [
            {
              "type": "TextBlock",
              "text": "HTTP/SSE",
              "weight": "Bolder"
            },
            {
              "type": "TextBlock",
              "text": "- Remote servers\n- Stateless scaling\n- Web deployment\n- Multi-client",
              "wrap": true
            }
          ]
        }
      ]
    },
    {
      "type": "TextBlock",
      "text": "Recommendation: Start with stdio for local dev, switch to HTTP for production.",
      "wrap": true,
      "color": "Accent"
    }
  ]
}
```

---

### Topic 6: SDK Installation (Quick Reply)

**Trigger phrases:**
- "Install MCP SDK"
- "pip install mcp"
- "npm install mcp"

**Quick replies:**
- Python: `pip install mcp`
- TypeScript: `npm install @modelcontextprotocol/sdk`

**Follow-up message:**
"Which language are you using? I can provide the full setup instructions."

---

## Generative Answers Configuration

In Copilot Studio, enable these settings:

1. **Content moderation:** Medium
2. **Data sources:** Website knowledge (MCP docs)
3. **Search behavior:** Search before generating
4. **Response length:** Medium (2-3 paragraphs max)
5. **Include citations:** Yes

---

## Testing Checklist

Before publishing, test these scenarios:

| Scenario | Expected Behavior |
| --- | --- |
| "How do I create an MCP server?" | Generative answer with Python/TS code |
| "Create a tool" | Adaptive card with code template |
| "stdio vs HTTP" | Comparison adaptive card |
| "My server won't connect" | Follow-up questions, then troubleshooting |
| Off-topic question | Graceful redirect to MCP topics |

---

## Publishing

### Channels

| Channel | Use Case |
| --- | --- |
| **Teams** | Internal developer support |
| **Web** | Public documentation site |
| **Power Virtual Agents** | Embed in Power Apps |

### Security

- No authentication required (documentation is public)
- Rate limit: 100 messages/user/hour
- Log conversations for improvement

---

## Files in This Folder

| File | Purpose |
| --- | --- |
| `mcp-expert-agent.md` | This configuration document |
| `mcp-expert-icon.svg` | Agent icon (512x512) |
| `adaptive-cards/` | Adaptive card JSON templates |

---

## Resources

- [Model Context Protocol](https://modelcontextprotocol.io)
- [Copilot Studio Documentation](https://learn.microsoft.com/copilot-studio)
- [Adaptive Cards Designer](https://adaptivecards.io/designer)
