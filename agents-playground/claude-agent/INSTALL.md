# Installing Claude Code Agents and Skills

Quick guide to installing and using the LangGraph Tutor agent and skill.

---

## TL;DR Installation

```bash
# Install the Agent (simple prompt file)
cp agents/langgraph-tutor.md ~/.claude/agents/

# Install the Skill (full package with scripts)
cp -r skills/langgraph-tutor ~/.claude/skills/
```

---

## What's the Difference?

| Feature | Agent | Skill |
| --- | --- | --- |
| **File type** | Single `.md` file | Directory with `SKILL.md` + supporting files |
| **Invocation** | Manual via prompt | Auto-triggered by keywords |
| **Complexity** | Simple instructions | Full package with scripts, examples, references |
| **Best for** | Quick persona/behavior changes | Complex workflows with artifacts |

---

## Installing the Agent

The agent is a single markdown file with instructions.

### Personal Installation (All Projects)

```bash
# Create agents directory if it doesn't exist
mkdir -p ~/.claude/agents

# Copy the agent file
cp agents/langgraph-tutor.md ~/.claude/agents/
```

### Project Installation (This Project Only)

```bash
# Create project agents directory
mkdir -p .claude/agents

# Copy the agent file
cp agents/langgraph-tutor.md .claude/agents/
```

### Using the Agent

Once installed, invoke by asking about LangGraph:

```
> Explain how StateGraph works in LangGraph
> Help me build a multi-agent system
> What's the difference between nodes and edges?
```

---

## Installing the Skill

The skill is a complete package with documentation, examples, and scripts.

### Personal Installation (All Projects)

```bash
# Create skills directory if it doesn't exist
mkdir -p ~/.claude/skills

# Copy the entire skill directory
cp -r skills/langgraph-tutor ~/.claude/skills/
```

### Project Installation (This Project Only)

```bash
# Create project skills directory
mkdir -p .claude/skills

# Copy the entire skill directory
cp -r skills/langgraph-tutor .claude/skills/
```

### Skill Structure

```
langgraph-tutor/
├── SKILL.md              # Core skill (auto-loaded)
├── references/           # Detailed docs (loaded on demand)
│   ├── patterns.md       # Common patterns
│   ├── multi-agent.md    # Multi-agent architectures
│   └── tools.md          # Tool integration
├── examples/             # Working code examples
│   ├── simple_chatbot.py
│   ├── tool_agent.py
│   └── multi_agent.py
└── scripts/              # Utility scripts
    ├── validate_graph.py
    ├── run_example.sh
    └── install_deps.sh
```

### Using the Skill

The skill auto-activates when you mention keywords like "langgraph", "state graph", "agent workflow", etc.

```
> I need help with LangGraph
> How do I add checkpointing to my graph?
> Show me how to validate my graph
```

Claude will:
1. Load the core SKILL.md
2. Reference detailed docs as needed
3. Suggest running examples or scripts

---

## Running the Examples

After installing the skill, run the examples:

```bash
# Install LangGraph dependencies
bash ~/.claude/skills/langgraph-tutor/scripts/install_deps.sh

# Set your API key
export ANTHROPIC_API_KEY=your-key-here

# Run an example
python ~/.claude/skills/langgraph-tutor/examples/simple_chatbot.py
```

---

## Validating Your Own Graphs

Use the validation script to check your LangGraph code:

```bash
python ~/.claude/skills/langgraph-tutor/scripts/validate_graph.py your_graph.py
```

Output:
```
Validating: your_graph.py
==================================================

Analysis:
  State class found: Yes
  StateGraph found: Yes
  Nodes: ['chatbot', 'tools']
  Edges: 4 found

==================================================
✅ Validation PASSED
```

---

## Troubleshooting

### Skill Not Triggering

1. Check the skill is in the right location:
   ```bash
   ls ~/.claude/skills/langgraph-tutor/SKILL.md
   ```

2. Verify SKILL.md has correct frontmatter:
   ```yaml
   ---
   name: langgraph-tutor
   description: ...keywords like "langgraph"...
   ---
   ```

3. Use explicit keywords: "LangGraph", "StateGraph", "agent graph"

### Agent Not Found

1. Check the agent file exists:
   ```bash
   ls ~/.claude/agents/langgraph-tutor.md
   ```

2. Restart Claude Code to reload agents

### Examples Won't Run

1. Activate virtual environment:
   ```bash
   source .venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install langgraph langchain-anthropic
   ```

3. Set API key:
   ```bash
   export ANTHROPIC_API_KEY=your-key
   ```

---

## Uninstalling

### Remove Agent

```bash
rm ~/.claude/agents/langgraph-tutor.md
```

### Remove Skill

```bash
rm -rf ~/.claude/skills/langgraph-tutor
```

---

## Questions?

Ask Claude: "How do agents and skills work in Claude Code?"
