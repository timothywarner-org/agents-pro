# Course Plan

## Course Overview

| Hour | Theme | Key Platforms & Tools |
|------|-------|-----------------------|
| 1 | What "Agent" Means | M365 Copilot agents (custom GPTs), declarative agents, agent landscape taxonomy |
| 2 | Low-Code Agents | Copilot Studio, Antigrav, Claude Code / GitHub Copilot agents |
| 3 | Code-First Agents | Azure AI Foundry agents, Python, LangGraph, FastMCP |
| 4 | TBD | Best practices, MCP deep dive, future trends (finalize before delivery) |

---

## Segment 1 -- What "Agent" Means (60 Minutes)

### Opening Hook: Agent in Action (10 min)
- **DEMO: Claude Code Subagents**
  - Show Claude Code orchestrating multiple subagents to complete a complex task
  - Highlight: autonomous decision-making, tool selection, multi-step reasoning
  - Key takeaway: "This is what agent orchestration looks like under the hood"

### Agent Taxonomy: Building a Mental Model (10 min)
- Define the landscape with clear distinctions:

| Term | Definition | Example |
|------|-----------|---------|
| **Chatbot** | Scripted Q&A with fixed flows; no reasoning | FAQ bot on a support page |
| **Copilot** | AI assistant embedded in a tool; user stays in the driver's seat | GitHub Copilot autocomplete, M365 Copilot in Word |
| **RPA** | Rule-based automation of repetitive UI tasks; no language understanding | UiPath clicking through legacy ERP screens |
| **Agent** | Autonomous AI that reasons, plans, selects tools, and acts toward a goal | Claude Code orchestrating subagents; Azure AI Foundry agent querying APIs |

- Key talking points:
  - Agents have a *reasoning loop* -- they observe, plan, act, and reflect
  - Agents *select and use tools* dynamically rather than following a fixed script
  - The spectrum is not binary -- many systems blend categories (e.g., Copilot Studio agents sit between copilot and agent)
  - "If it can't choose its own next step, it's not an agent"

### M365 Copilot Agents Tour (15 min)
- Open Microsoft 365 Copilot and demonstrate the agent ecosystem:

**1. Custom GPTs / Agent Builder**
  - Show how end users create simple agents with natural language instructions
  - Demonstrate adding SharePoint knowledge and custom instructions
  - Highlight: no code required, available to any M365 Copilot licensed user
  - Reference: [Build a declarative agent with Agent Builder](https://learn.microsoft.com/en-us/microsoft-365-copilot/extensibility/agent-builder)

**2. @Mention Agents in Copilot Chat**
  - Show how published agents appear in the Copilot sidebar
  - Demonstrate @mentioning an agent mid-conversation
  - Show suggested prompts and conversation handoff
  - Reference: [Agents for Microsoft 365 Copilot](https://learn.microsoft.com/en-us/microsoft-365-copilot/extensibility/agents-overview)

**3. Declarative Agents**
  - Explain the declarative approach: instructions + knowledge + actions, powered by Copilot's orchestrator and models
  - Show the agent manifest structure (JSON/YAML)
  - Contrast with custom engine agents (bring your own orchestrator and model)
  - Reference: [Declarative agents for Microsoft 365 Copilot](https://learn.microsoft.com/en-us/microsoft-365-copilot/extensibility/overview-declarative-agent)

**4. Agent Sidebar and Discovery**
  - Walk through the agent gallery in Teams and Copilot Chat
  - Show how agents are shared, pinned, and managed by admins
  - Reference: [Microsoft 365 Copilot agents admin guide](https://learn.microsoft.com/en-us/copilot/microsoft-365/agent-essentials/m365-agents-admin-guide)

### Copilot Studio Introduction (10 min)
- **What it is**: Graphical, low-code platform for building AI agents -- the gateway to Hour 2
- **Live walkthrough of the Studio interface** -- highlight the four pillars:

**1. Generative Orchestration** (the brain)
  - Default for new agents -- AI autonomously selects best combination of topics, tools, and knowledge
  - Selection based on descriptions, not just trigger phrases
  - Can chain multiple topics/tools in sequence for multi-intent queries
  - Reference: [Generative orchestration](https://learn.microsoft.com/en-us/microsoft-copilot-studio/advanced-generative-actions)

**2. Topics** (conversation building blocks)
  - Represent portions of conversational threads
  - Visual editor with connected nodes and conditional logic
  - AI-assisted creation from plain language descriptions

**3. Knowledge Sources** (the data layer)
  - SharePoint sites (respects user permissions)
  - Graph connectors (admin-configured enterprise data)
  - Public websites and uploaded files

**4. Channels** (deployment targets)
  - Microsoft Teams, websites, Microsoft 365 Copilot, Facebook, Azure Bot Service

- Reference: [What is Copilot Studio](https://learn.microsoft.com/en-us/microsoft-copilot-studio/fundamentals-what-is-copilot-studio)

### Azure AI Foundry Context (2 min)
- Brief mention only -- this is the gateway to Hour 3
- Position as: "Where you go for code-first agents, custom model hosting, and full SDK control"
- Copilot Studio is the low-code path; Foundry is the code-first path
- Reference: [What is Azure AI Foundry](https://learn.microsoft.com/en-us/azure/ai-foundry/)

### Environment Readiness Check (3 min)
- Confirm Copilot Studio access for all participants
- Verify sample data availability (SharePoint sites, documents)
- Check Teams deployment targets are accessible
- Confirm Python environments for Hour 3 (Python 3.10+, pip access)

### Q&A and Break (10 min)
- 5 min Q&A
- 5 min break

---

## Segment 2 -- Low-Code Agents (60 Minutes)

**Agent:** Customer Service Assistant for Contoso Electronics
**Level:** Beginner
**Goal:** Demonstrate knowledge-powered conversations, generative answers, and escalation handling -- then broaden the lens to adjacent low-code and developer-facing agent tools

### Instructor Quick-Reference Outline

| Time | Activity | Key Deliverable |
|------|----------|-----------------|
| 0-10 min | **Setup & Context** | Agent created from natural language description |
| 10-25 min | **Knowledge Configuration** | SharePoint + website sources connected; generative answers enabled |
| 25-40 min | **Topic Authoring** | Returns/Refunds and Order Status topics built with variables |
| 40-48 min | **Live Demo** | Run 4-6 test prompts in simulator; show fallback and escalation |
| 48-53 min | **Antigrav + Dev Agent Demos** | Rapid prototyping comparison; bridge to Hour 3 |
| 53-55 min | **Publish to Teams** | Agent available in Teams for learner testing |
| 55-60 min | **Q&A + Break** | Address questions; 5-minute break |

### Demo Prompts: "Flex the Muscles"

Use these prompts in sequence to demonstrate the agent's full capability range.

#### Prompt Set A: Knowledge-Grounded Answers

| # | Test Prompt | What It Demonstrates |
|---|-------------|---------------------|
| 1 | "What laptops do you sell with 32GB RAM?" | **Generative answers** from product knowledge; shows how the agent synthesizes information from SharePoint/web sources |
| 2 | "Is the Contoso Pro X15 compatible with an external 4K monitor?" | **Specificity handling**; agent retrieves product specs and answers a technical compatibility question |

#### Prompt Set B: Guided Topic Flows

| # | Test Prompt | What It Demonstrates |
|---|-------------|---------------------|
| 3 | "I want to return my order" | **Returns and Refunds topic** triggers; agent collects order number and reason, then uses generative answers to determine eligibility |
| 4 | "Where is my order CT-991100?" | **Order Status topic** triggers; agent extracts order number and calls the lookup action (or simulates status response) |

#### Prompt Set C: Escalation and Edge Cases

| # | Test Prompt | What It Demonstrates |
|---|-------------|---------------------|
| 5 | "Let me talk to a human, this isn't working" | **Escalate to Human topic** triggers; agent summarizes the conversation, assigns priority, and prepares handoff context |
| 6 | "What's the weather in Seattle?" | **Fallback behavior**; agent gracefully handles out-of-scope questions when "AI General Knowledge" is disabled |

### Talking Points (MS Learn Grounded)

**1. Natural Language Agent Creation**
- Copilot Studio allows creating agents by describing them in plain English
- The platform auto-generates greeting topics, conversation starters, and default system topics
- Reference: [Create and delete copilots](https://learn.microsoft.com/en-us/microsoft-copilot-studio/fundamentals-get-started)

**2. Knowledge Sources and Generative Answers**
- SharePoint requires `Sites.Read.All` and `Files.Read.All` scopes
- Website sources crawl public pages; indexing takes 30-60 minutes
- Set `moderationLevel: High` for customer-facing agents to filter inappropriate content
- Sources in a generative answers node override agent-level sources
- Reference: [Knowledge sources overview](https://learn.microsoft.com/en-us/microsoft-copilot-studio/knowledge-copilot-studio)

**3. Topic Authoring Best Practices**
- Include 5-15 trigger phrases with natural variation (short, varied phrasing)
- **Never use periods in topic names** -- causes solution export failures
- Use descriptive variable names with scope prefix (e.g., `Topic.OrderNumber`)
- Use the Topic Checker to identify and resolve overlapping triggers
- Reference: [Topic authoring best practices](https://learn.microsoft.com/en-us/microsoft-copilot-studio/guidance/topic-authoring-best-practices)

**4. Escalation Design**
- Always capture context before handoff (issue summary, order numbers, customer sentiment)
- Use generative answers to auto-summarize the conversation for the human agent
- Mark escalation outcomes with `conversationOutcome: Escalated` for accurate analytics
- Reference: [Hand off to a live agent](https://learn.microsoft.com/en-us/microsoft-copilot-studio/advanced-hand-off)

**5. Testing and Publishing**
- Use the built-in Test panel before publishing
- Test positive paths, negative paths, and edge cases
- Enable conversation logging in Settings > Security for transcript review
- Publish to Teams requires configuring the agent card (icon, descriptions)
- Reference: [Publish to Teams](https://learn.microsoft.com/en-us/microsoft-copilot-studio/publication-add-bot-to-microsoft-teams)

### Antigrav Demo (5 min)

- **Purpose:** Show rapid agent prototyping as a comparison point to Copilot Studio
- Demonstrate creating a simple agent in Antigrav from a natural language description
- Highlight speed-to-prototype: describe the agent, get a working demo in under 2 minutes
- Compare and contrast with Copilot Studio:

| Dimension | Copilot Studio | Antigrav |
|-----------|---------------|----------|
| Strength | Enterprise governance, M365 integration, Power Platform ecosystem | Rapid prototyping, iteration speed, simplicity |
| Best for | Production agents with compliance requirements | Exploring ideas, validating agent concepts quickly |
| Deployment | Teams, M365 Copilot, websites | Standalone, embeddable |

- Key takeaway: "Different tools for different stages of the agent lifecycle -- prototype fast, then productionize in the platform that fits"

### Claude Code / GitHub Copilot Agents (5 min)

- **Purpose:** Bridge from low-code to code-first -- show developer-facing agents as a preview of Hour 3
- Briefly demonstrate:
  - **Claude Code**: AI agent in the terminal -- reads codebases, writes files, runs commands, orchestrates subagents
  - **GitHub Copilot agents**: @workspace, @terminal, custom agents in VS Code that understand your codebase
- Key distinction: these agents assist *developers* in building software, whereas Copilot Studio agents assist *end users* in completing business tasks
- Transition line: "In Hour 3, we'll build agents like these from scratch using Python, LangGraph, and MCP"

### Live Build Checklist

```
[ ] Create agent with natural language description
[ ] Add SharePoint knowledge source (contoso.sharepoint.com/sites/CustomerSupport)
[ ] Add website knowledge source (www.contoso.com/support, /products, /warranty)
[ ] Enable generative answers with High moderation
[ ] Disable AI General Knowledge (restrict to configured sources only)
[ ] Build "Returns and Refunds" topic with trigger phrases and variables
[ ] Build "Order Status" topic with action node (or generative stub)
[ ] Customize Escalate topic to capture issue summary
[ ] Run all 6 demo prompts in Test panel
[ ] Publish to Microsoft Teams
```

---

## Segment 3 -- Code-First Agents (60 Minutes)

**Level:** Intermediate to Advanced
**Goal:** Build agents using Python SDKs and frameworks -- Azure AI Foundry, LangGraph, and FastMCP -- then show how MCP bridges code-first tools into low-code platforms

### Instructor Quick-Reference Outline

| Time | Activity | Key Deliverable |
|------|----------|-----------------|
| 0-5 min | **Context & Setup** | Explain code-first vs low-code tradeoffs; confirm Python environments |
| 5-15 min | **Azure AI Foundry Agent** | Agent created via `azure-ai-projects` SDK; runs in Foundry portal |
| 15-30 min | **LangGraph Multi-Step Agent** | State machine agent with nodes, edges, and tool calls |
| 30-45 min | **FastMCP Server** | MCP server exposing tools to LLM clients; demo with Claude or MCP client |
| 45-50 min | **Connecting It All** | Show how MCP bridges code-first tools into Copilot Studio and other platforms |
| 50-55 min | **Learner Exercise** | Extend the FastMCP server with one new tool |
| 55-60 min | **Q&A + Break** | Address questions; 5-minute break |

### Demo Scenario 1: Azure AI Foundry Agent (10 min)

**Objective:** Create an agent via the Azure AI Projects SDK and demonstrate the Hub + Project model.

**Setup:**
- Ensure `azure-ai-projects` and `azure-identity` are installed: `pip install azure-ai-projects azure-identity`
- Set environment variables: `PROJECT_ENDPOINT`, `MODEL_DEPLOYMENT_NAME`
- Authenticate with `az login`

**Live Coding Walkthrough:**

```python
import os
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

project_client = AIProjectClient(
    endpoint=os.environ["PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
)

# Create an agent with instructions
agent = project_client.agents.create_agent(
    model=os.environ["MODEL_DEPLOYMENT_NAME"],
    name="ContoseSupportAgent",
    instructions="You are a helpful support agent for Contoso Electronics. Answer product questions accurately and concisely.",
)
print(f"Agent created: {agent.id}")

# Create a thread and send a message
thread = project_client.agents.threads.create()
message = project_client.agents.messages.create(
    thread_id=thread.id,
    role="user",
    content="What laptops do you recommend for software development?",
)

# Run the agent
run = project_client.agents.runs.create_and_process(
    thread_id=thread.id,
    agent_id=agent.id,
)

# Retrieve response
messages = project_client.agents.messages.list(thread_id=thread.id)
for msg in messages:
    if msg.role == "assistant":
        print(msg.content[0].text.value)

# Clean up
project_client.agents.delete_agent(agent.id)
```

**Talking Points:**
- Azure AI Foundry uses a **Hub + Project** model: the Hub holds shared resources (compute, connections, models), and Projects are workspaces within a Hub
- Agents in Foundry support tools: code interpreter, file search, function calling, Azure AI Search
- The `azure-ai-projects` SDK provides a unified client for agents, models, and project management
- Foundry agents persist server-side (threads, messages, runs) -- similar to the OpenAI Assistants API pattern
- Reference: [Azure AI Foundry agents quickstart](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/quickstart)
- Reference: [Azure AI Foundry overview](https://learn.microsoft.com/en-us/azure/ai-foundry/)

### Demo Scenario 2: LangGraph Multi-Step Agent (15 min)

**Objective:** Build a state machine agent with nodes and edges that orchestrates tool calls in a reasoning loop.

**Live Coding Walkthrough:**

```python
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages

# Define the state schema
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]

# Define tools the agent can use
def lookup_order(order_id: str) -> str:
    """Look up order status by order ID."""
    # Simulated lookup
    orders = {
        "CT-991100": "Shipped - arrives Jan 15",
        "CT-991101": "Processing - estimated Jan 20",
    }
    return orders.get(order_id, "Order not found")

def check_return_eligibility(order_id: str) -> str:
    """Check if an order is eligible for return."""
    return f"Order {order_id} is eligible for return within 30 days of delivery."

tools = [lookup_order, check_return_eligibility]

# Create the model with tool binding
model = ChatOpenAI(model="gpt-4o-mini").bind_tools(tools)

# Define nodes
def call_model(state: AgentState):
    response = model.invoke(state["messages"])
    return {"messages": [response]}

def should_continue(state: AgentState):
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "tools"
    return END

# Build the graph
graph = StateGraph(AgentState)
graph.add_node("agent", call_model)
graph.add_node("tools", ToolNode(tools))
graph.add_edge(START, "agent")
graph.add_conditional_edges("agent", should_continue, {"tools": "tools", END: END})
graph.add_edge("tools", "agent")

# Compile and run
app = graph.compile()
result = app.invoke({
    "messages": [HumanMessage(content="What's the status of order CT-991100? Is it eligible for return?")]
})

for msg in result["messages"]:
    print(f"{msg.type}: {msg.content}")
```

**Talking Points:**
- LangGraph models agent logic as a **directed graph** -- nodes are functions, edges define control flow
- The `should_continue` function implements the **reasoning loop**: if the model wants to call a tool, route to the tool node; otherwise, finish
- This pattern naturally supports **multi-step reasoning** -- the agent calls `lookup_order`, gets the result, then decides to call `check_return_eligibility`
- State is explicit and inspectable -- you can serialize, checkpoint, and replay any step
- LangGraph supports persistence, streaming, human-in-the-loop breakpoints, and parallel tool execution
- Reference: [LangGraph documentation](https://langchain-ai.github.io/langgraph/)
- Compare with Copilot Studio: topics with conditional nodes are the low-code equivalent of this graph

### Demo Scenario 3: FastMCP Server (15 min)

**Objective:** Build a Model Context Protocol server that exposes tools to any MCP-compatible LLM client.

**Setup:**
- Install FastMCP: `pip install fastmcp`

**Live Coding Walkthrough:**

```python
from fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("Contoso Support Tools")

@mcp.tool()
def lookup_order(order_id: str) -> str:
    """Look up the current status of a customer order by its order ID.

    Args:
        order_id: The order identifier (e.g., CT-991100)
    """
    orders = {
        "CT-991100": "Shipped via FedEx, tracking #1234567890, arrives Jan 15",
        "CT-991101": "Processing - payment confirmed, estimated ship date Jan 18",
        "CT-991102": "Delivered on Jan 10 - signed by J. Smith",
    }
    return orders.get(order_id, f"Order {order_id} not found in system")

@mcp.tool()
def check_warranty(product_name: str) -> str:
    """Check warranty status and coverage for a Contoso product.

    Args:
        product_name: The product name to check warranty for
    """
    warranties = {
        "Contoso Pro X15": "2-year limited warranty, valid until 2027-03-15",
        "Contoso Surface Dock": "1-year warranty, valid until 2026-06-01",
    }
    return warranties.get(product_name, f"No warranty record found for {product_name}")

@mcp.tool()
def submit_support_ticket(
    customer_email: str,
    issue_summary: str,
    priority: str = "medium",
) -> str:
    """Submit a new support ticket for a customer issue.

    Args:
        customer_email: Customer's email address
        issue_summary: Brief description of the issue
        priority: Ticket priority - low, medium, or high
    """
    # In production, this would call a ticketing API
    ticket_id = "TKT-2026-00042"
    return f"Ticket {ticket_id} created for {customer_email} (priority: {priority}): {issue_summary}"

@mcp.resource("support://policies/returns")
def get_return_policy() -> str:
    """Contoso Electronics return policy document."""
    return """
    Contoso Electronics Return Policy:
    - Items may be returned within 30 days of delivery
    - Original packaging required for full refund
    - Electronics must be in working condition
    - Restocking fee of 15% applies to opened items
    - Defective items are exempt from restocking fee
    """

if __name__ == "__main__":
    mcp.run()
```

**Testing the Server:**
- Run: `python contoso_mcp_server.py` (starts stdio transport by default)
- Connect with Claude Desktop, VS Code + MCP extension, or any MCP-compatible client
- Show the client discovering tools automatically and calling them during conversation

**Talking Points:**
- MCP is an **open standard** for connecting AI applications to external data and tools -- think "USB-C for AI"
- The protocol defines three primitives: **tools** (functions the model can call), **resources** (data the model can read), and **prompts** (reusable prompt templates)
- FastMCP provides a Pythonic decorator-based API -- docstrings become tool descriptions, type hints become parameter schemas
- Any MCP-compatible client (Claude, ChatGPT, Copilot, custom apps) can discover and use these tools without client-specific integration code
- This is the key unlock: **build once, connect everywhere**
- Reference: [Model Context Protocol specification](https://modelcontextprotocol.io)
- Reference: [FastMCP on GitHub](https://github.com/jlowin/fastmcp)

### Connecting It All (10 min)

**Objective:** Show how MCP bridges code-first tools into low-code platforms and other clients.

**Talking Points:**
- MCP servers can be consumed by:
  - Claude Desktop and Claude Code (native MCP support)
  - VS Code with MCP extensions
  - Custom Python/TypeScript clients using MCP SDK
  - Copilot Studio via custom connectors (wrap MCP server in a REST API)
- The pattern: **domain experts build MCP servers, platform teams consume them**
- Example architecture:

```
  [MCP Server: Contoso Tools]
       |          |          |
  [Claude]   [Copilot     [Custom
              Studio]      App]
```

- In production, MCP servers run as HTTP/SSE endpoints behind API management
- Security: MCP supports authentication, authorization, and tool-level access control
- This bridges the gap between Segment 2 (low-code) and Segment 3 (code-first) -- the same tools serve both worlds

### Learner Exercise (5 min)

**Challenge:** Extend the FastMCP server with one new tool. Choose from:

1. **`check_inventory`** -- Accept a product name, return stock level and warehouse location
2. **`calculate_shipping`** -- Accept a destination zip code and order weight, return estimated cost and delivery date
3. **`get_product_reviews`** -- Accept a product name, return average rating and recent review snippets

**Instructions:**
- Add a new `@mcp.tool()` decorated function to the server
- Include a clear docstring with Args section (this becomes the tool description for LLM clients)
- Return a formatted string with the result
- Restart the server and verify the new tool appears in your MCP client

This exercise reinforces the pattern: define a function with type hints and a docstring, decorate it, and the MCP protocol handles discovery and invocation.

### Live Coding Checklist

```
[ ] Python 3.10+ environment confirmed with pip access
[ ] azure-ai-projects and azure-identity installed
[ ] Azure AI Foundry agent created and tested via SDK
[ ] Hub + Project model explained; portal walkthrough complete
[ ] langgraph and langchain-openai installed
[ ] LangGraph agent built with state, nodes, edges, and tool calls
[ ] Reasoning loop demonstrated (model -> tool -> model -> finish)
[ ] fastmcp installed
[ ] FastMCP server built with 3+ tools and 1 resource
[ ] MCP server tested with Claude or another MCP-compatible client
[ ] MCP bridge architecture explained (code-first tools -> low-code platforms)
[ ] Learner exercise assigned and debriefed
```

### Resources for Learners

- [Azure AI Foundry documentation](https://learn.microsoft.com/en-us/azure/ai-foundry/)
- [Azure AI Foundry agents quickstart (Python)](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/quickstart)
- [Azure AI Projects SDK reference](https://learn.microsoft.com/en-us/python/api/overview/azure/ai-projects-readme)
- [LangGraph documentation](https://langchain-ai.github.io/langgraph/)
- [LangGraph quickstart tutorial](https://langchain-ai.github.io/langgraph/tutorials/introduction/)
- [FastMCP on GitHub](https://github.com/jlowin/fastmcp)
- [Model Context Protocol specification](https://modelcontextprotocol.io)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)

---

## Segment 4 -- TBD (60 Minutes)

> **PLACEHOLDER** -- Finalize based on learner profile and current industry momentum before delivery.

### Candidate Topics

#### Option A: Best Practices -- Testing, Observability, Security, Governance

- **Testing agents across all three tiers:**
  - Copilot Studio: Test panel, simulated conversations, analytics dashboards
  - Code-first: unit testing tool functions, integration testing agent graphs, evaluation frameworks (e.g., LangSmith, Azure AI Evaluation)
  - End-to-end: user acceptance testing, A/B testing agent responses
- **Observability and monitoring:**
  - Tracing agent reasoning chains (LangSmith, Azure Monitor, OpenTelemetry)
  - Logging tool calls, latency, token usage, and error rates
  - Alerting on confidence score degradation and escalation spikes
- **Security considerations:**
  - Prompt injection defense (input validation, output filtering)
  - Tool authorization and least-privilege access
  - Data Loss Prevention (DLP) policies across platforms
  - Reference: [Agent governance best practices](https://learn.microsoft.com/en-us/microsoft-copilot-studio/admin-data-loss-prevention)
- **Governance at scale:**
  - Solution lifecycle management (ALM) for Copilot Studio agents
  - Version control and CI/CD for code-first agents
  - Responsible AI review gates before production deployment
  - Reference: [Power Platform ALM](https://learn.microsoft.com/en-us/power-platform/alm/)

#### Option B: MCP Deep Dive -- Protocol, Architecture, Production Servers

- **Protocol specification walkthrough:**
  - JSON-RPC 2.0 transport layer
  - Capability negotiation between client and server
  - Tool, resource, and prompt primitives in detail
  - Reference: [MCP specification](https://modelcontextprotocol.io)
- **Server/client architecture:**
  - stdio vs HTTP/SSE transports
  - Authentication and authorization patterns
  - Server discovery and registry patterns
- **Building production MCP servers:**
  - Error handling, retries, and graceful degradation
  - Rate limiting and connection management
  - Deployment patterns: Docker containers, Azure Container Apps, serverless
  - Monitoring and health checks
- **Hands-on:** Build a more complex MCP server with multiple resources, error handling, and an HTTP transport

#### Option C: Future Trends -- Multi-Agent, A2A, Autonomous Safety

- **Multi-agent orchestration:**
  - Patterns: supervisor, swarm, hierarchical delegation
  - LangGraph multi-agent workflows
  - Copilot Studio agent chaining
- **Agent-to-agent communication:**
  - Google's A2A (Agent-to-Agent) protocol
  - Azure AI Foundry A2A support
  - Reference: [A2A agent endpoint in Foundry](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/how-to/tools/agent-to-agent)
- **Autonomous agent safety:**
  - Human-in-the-loop breakpoints and approval gates
  - Guardrails and constitutional AI patterns
  - Sandboxing and capability restrictions
  - When to use agents vs when to keep humans in the loop
- **Industry direction:**
  - MCP adoption trajectory (Anthropic, OpenAI, Microsoft, Google)
  - Convergence of low-code and code-first agent platforms
  - The shift from single-agent to multi-agent systems

### Wrap-Up Structure (5 min -- applies to whichever option is selected)

**Course Recap:**
- Hour 1: Built a shared vocabulary -- agent vs chatbot vs copilot vs RPA
- Hour 2: Built a low-code agent in Copilot Studio with knowledge, topics, and escalation
- Hour 3: Built code-first agents with Azure AI Foundry, LangGraph, and FastMCP
- Hour 4: [Selected topic summary]

**Resources and Next Steps:**
- Course repository: link to this repo with all code samples and blueprints
- [Microsoft Copilot Studio documentation](https://learn.microsoft.com/en-us/microsoft-copilot-studio/)
- [Azure AI Foundry documentation](https://learn.microsoft.com/en-us/azure/ai-foundry/)
- [LangGraph documentation](https://langchain-ai.github.io/langgraph/)
- [Model Context Protocol](https://modelcontextprotocol.io)
- Recommended follow-up: Microsoft Applied Skills for Copilot Studio, Azure AI Engineer Associate certification path

**Final Q&A (5 min)**
- Open floor for remaining questions
- Collect feedback (link to post-course survey)
- Thank learners and close
