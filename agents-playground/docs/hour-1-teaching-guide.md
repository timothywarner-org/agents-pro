# Hour 1 Teaching Guide: What is an Agent?

**Goal:** Students understand what AI agents are, how they differ from chatbots, and get hands-on experience with Claude Code and Copilot Studio.

**Time:** 60 minutes

---

## Opening (5 minutes)

**What We're Doing This Hour:**

1. Define what an AI agent actually is (not just a chatbot)
2. Understand the cognitive architecture of agents
3. Hands-on with Claude Code (coding agent)
4. Hands-on with Microsoft Copilot Studio (low-code agent builder)
5. Compare approaches and choose your path

**Key Message:** "An agent is an AI that can take actions, not just answer questions. Today you'll build with two very different agent platforms."

---

## What is an AI Agent? (10 minutes)

### The Chatbot vs Agent Distinction

**Draw on whiteboard:**

```
Chatbot                          Agent
-------                          -----
Q: "What time is it?"            Q: "Schedule a meeting for 3pm"
A: "I don't have access          A: *Checks calendar*
    to current time"                *Finds available slot*
                                    *Sends invite*
                                    "Done. Meeting scheduled."
```

**Key Differences:**

| Aspect | Chatbot | Agent |
| --- | --- | --- |
| Capability | Answers questions | Takes actions |
| Memory | Stateless (each message fresh) | Stateful (remembers context) |
| Tools | None | APIs, databases, file systems |
| Autonomy | Responds only | Plans and executes |
| Loop | Single turn | Multi-step reasoning |

**Say:** "The difference is ACTION. An agent doesn't just tell you what to do -- it does it."

### The Cognitive Architecture

**Show the ReAct Loop:**

```
┌─────────────────────────────────────────┐
│                                         │
│   Observe → Think → Act → Observe...   │
│                                         │
└─────────────────────────────────────────┘
```

**Break it down:**

1. **Observe:** Agent receives input (user message, file change, API response)
2. **Think:** LLM reasons about what to do next
3. **Act:** Agent uses a tool (write file, call API, run command)
4. **Loop:** Results feed back into observation

**Real Example:**

```
User: "Add a login button to the header"

Agent thinks: "I need to find the header file first"
Agent acts:   [Searches for header.tsx]
Agent observes: "Found src/components/Header.tsx"

Agent thinks: "Now I'll read it to understand the structure"
Agent acts:   [Reads Header.tsx]
Agent observes: "It's a React component with NavBar"

Agent thinks: "I'll add a LoginButton import and JSX"
Agent acts:   [Edits Header.tsx]
Agent observes: "File updated successfully"

Agent responds: "I've added a login button to your header."
```

**Key Point:** "The agent took 3 actions before responding. That's the difference."

---

## Hands-On: Claude Code (20 minutes)

### What is Claude Code?

**Say:** "Claude Code is Anthropic's AI coding agent. It runs in your terminal and can read, write, and execute code."

**Key capabilities:**

- Reads and writes files directly
- Executes terminal commands
- Searches codebases
- Creates commits and PRs
- Runs tests

### Setup Check (3 minutes)

**Everyone verify:**

```bash
# Check Claude Code is installed
claude --version

# Should show something like:
# Claude Code v1.x.x
```

**If not installed:**

```bash
npm install -g @anthropic-ai/claude-code
```

### Demo: Claude Code in Action (7 minutes)

**Open terminal in the agents2 repo:**

```bash
cd agents2/oreilly-agent-mvp
claude
```

**Demo these prompts:**

1. **Exploration:**
   ```
   What files handle the PM agent? Give me a quick overview.
   ```

2. **Code understanding:**
   ```
   Explain how token tracking works in this project.
   ```

3. **Making changes:**
   ```
   Add a docstring to the pm_node function explaining what it does.
   ```

**Point out:** "Watch Claude's tool use -- it reads files, searches, then edits. That's the agent loop."

### Hands-On Exercise (10 minutes)

**Everyone try:**

1. Start Claude Code in the project:
   ```bash
   cd agents2/oreilly-agent-mvp
   claude
   ```

2. Ask Claude to explore:
   ```
   List all the Python files in src/ and briefly describe what each does.
   ```

3. Ask Claude to explain:
   ```
   How does the pipeline flow from issue input to final result?
   ```

4. Ask Claude to find something:
   ```
   Where are the prompts for each agent defined?
   ```

**Debrief questions:**

- How many tool calls did Claude make?
- Did it read files before answering?
- How is this different from asking ChatGPT the same questions?

---

## Hands-On: Microsoft Copilot Studio (20 minutes)

### What is Copilot Studio?

**Say:** "Copilot Studio is Microsoft's low-code platform for building conversational agents. It's part of Power Platform."

**Key capabilities:**

- Visual topic designer (no code required)
- Built-in connectors to Microsoft 365
- Knowledge sources (SharePoint, websites, files)
- Generative AI answers
- Publish to Teams, web, or custom channels

### Access Copilot Studio (3 minutes)

**Navigate to:**

```
https://copilotstudio.microsoft.com
```

**Sign in with Microsoft account (work/school or personal).**

**If first time:** Create a new environment or use default.

### Demo: Build a Simple Agent (7 minutes)

**Walk through creating an agent:**

1. **Create new copilot:**
   - Click "Create" → "New copilot"
   - Name: "Issue Triage Assistant"
   - Description: "Helps categorize GitHub issues"

2. **Add a topic:**
   - Topics → Add topic → From blank
   - Name: "Categorize Issue"
   - Trigger phrases:
     - "categorize this issue"
     - "what type of issue is this"
     - "help me triage"

3. **Add conversation flow:**
   - Add node: "Ask a question"
   - Question: "Paste the issue title and description"
   - Save response as: `IssueText`

4. **Add generative answer:**
   - Add node: "Generative answers"
   - Configure to use `IssueText` as context

5. **Test in the canvas:**
   - Click "Test" in top right
   - Try: "Categorize this issue: Users can't login after password reset"

**Point out:** "No code. We built an agent that can reason about issues using drag-and-drop."

### Hands-On Exercise (10 minutes)

**Everyone try:**

1. Create a new copilot named "Code Review Helper"

2. Add a topic with triggers:
   - "review this code"
   - "check my implementation"
   - "code review"

3. Add a question node:
   - "Paste the code you'd like me to review"

4. Add a generative answer that reviews the code

5. Test with some Python code:
   ```python
   def add(a, b):
       return a + b
   ```

**Challenge:** Add a second topic for "explain this code" that explains code instead of reviewing it.

---

## Comparison: Claude Code vs Copilot Studio (5 minutes)

### Side-by-Side

| Aspect | Claude Code | Copilot Studio |
| --- | --- | --- |
| Interface | Terminal / CLI | Web GUI |
| Code required | None (but code-aware) | None |
| Primary use | Developer productivity | Business automation |
| Deployment | Local | Cloud (Microsoft 365) |
| Customization | Prompt engineering | Visual designer |
| Integration | Git, file system, terminal | Power Platform, Teams |
| Cost model | API usage | Per-user licensing |

### When to Use Which

**Use Claude Code when:**

- You're a developer working in code
- You need file system access
- You want terminal integration
- You're building or debugging software

**Use Copilot Studio when:**

- You need a customer-facing bot
- You want Microsoft 365 integration
- Non-developers need to maintain it
- You need Teams or SharePoint publishing

**Key Point:** "These aren't competitors -- they solve different problems. Know both."

---

## Wrap-Up (5 minutes)

### What We Accomplished

- Defined what makes an agent different from a chatbot
- Understood the Observe → Think → Act loop
- Used Claude Code to explore and modify a codebase
- Built a conversational agent in Copilot Studio
- Compared code-first vs low-code approaches

### What's Next (Hour 2)

- Run the full agent pipeline (PM → Dev → QA)
- Understand the architecture of multi-agent systems
- Debug agent behavior with VSCode
- See token usage and costs in real-time

### Key Takeaways

1. **Agents take actions** -- they don't just respond
2. **The ReAct loop** is the core pattern (Observe → Think → Act)
3. **Claude Code** is for developers in the terminal
4. **Copilot Studio** is for business automation with GUI
5. **Both are valid** -- choose based on your use case

---

## Teaching Tips

### If Claude Code Installation Fails

**Common fixes:**

```bash
# Clear npm cache
npm cache clean --force

# Install with different registry
npm install -g @anthropic-ai/claude-code --registry https://registry.npmjs.org

# Check Node version (needs 18+)
node --version
```

### If Copilot Studio Access Is Blocked

**Options:**

1. Use personal Microsoft account
2. Request admin to enable Power Platform
3. Demo on your screen while students watch
4. Use screenshots for key concepts

### If Students Are Ahead

**Advanced challenges:**

1. "Make Claude Code create a new test file for an existing function"
2. "Build a Copilot Studio agent with multiple topics that hand off to each other"
3. "Configure Claude Code with a custom system prompt in CLAUDE.md"

### Time Management

- If Claude Code setup takes too long: Skip to demo, have students watch
- If Copilot Studio is slow: Pre-create the agent before class
- If running ahead: Add the comparison exercise below

### Bonus Exercise: Head-to-Head

**If time permits:**

Give both agents the same task:

```
Explain what a Python decorator is and show an example.
```

Compare:
- How each agent approaches the task
- Response quality and depth
- Time to complete
- Format of the output

---

## Quick Reference: Agent Patterns

### The ReAct Pattern

```
Reasoning: "I need to find the file first"
Action: search_files("*.tsx")
Observation: ["Header.tsx", "Footer.tsx"]
Reasoning: "Header.tsx is what I need"
Action: read_file("Header.tsx")
...
```

### Tool Use Pattern

```
User → Agent → [Tool Call] → Tool Result → Agent → Response
```

### Multi-Agent Pattern (Preview for Hour 2)

```
Issue → [PM Agent] → Plan → [Dev Agent] → Code → [QA Agent] → Verdict
```

---

## Resources

**Claude Code:**

- [Documentation](https://docs.anthropic.com/claude-code)
- [GitHub](https://github.com/anthropics/claude-code)

**Copilot Studio:**

- [Documentation](https://learn.microsoft.com/copilot-studio)
- [Training Path](https://learn.microsoft.com/training/paths/power-virtual-agents)

**Agent Patterns:**

- [ReAct Paper](https://arxiv.org/abs/2210.03629)
- [LangGraph Concepts](https://langchain-ai.github.io/langgraph/)

---

**You got this! The journey from chatbot to agent starts here.**
