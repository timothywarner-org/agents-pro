# Claude Code Agents and Skills - Teaching Examples

This folder contains teaching examples demonstrating the difference between **Agents** and **Skills** in Claude Code.

---

## What's in This Folder?

```
claude-agent/
├── README.md           # This file
├── INSTALL.md          # Installation guide
├── agents/
│   └── langgraph-tutor.md    # Agent definition (single file)
└── skills/
    └── langgraph-tutor/      # Skill package (directory)
        ├── SKILL.md          # Core skill definition
        ├── references/       # Detailed documentation
        ├── examples/         # Working code examples
        └── scripts/          # Utility scripts
```

---

## Agents vs Skills: Key Differences

### Agents

**Definition:** A single markdown file that defines a persona or behavior.

**Structure:**
```markdown
# Agent Name

## Agent Configuration
- Description, allowed tools, model

## Instructions
- How the agent should behave
- What it should do
```

**Installation:**
```bash
cp agents/langgraph-tutor.md ~/.claude/agents/
```

**Invocation:** Ask about the topic; Claude uses the agent's instructions.

**Best for:**
- Simple behavior modifications
- Persona-based responses
- Quick setup

---

### Skills

**Definition:** A directory with `SKILL.md` plus supporting files (references, examples, scripts).

**Structure:**
```
skill-name/
├── SKILL.md              # Required - core instructions
├── references/           # Optional - detailed docs
├── examples/             # Optional - code samples
└── scripts/              # Optional - utility scripts
```

**Installation:**
```bash
cp -r skills/langgraph-tutor ~/.claude/skills/
```

**Invocation:** Auto-triggered by keywords in the skill's description.

**Best for:**
- Complex workflows
- Providing artifacts (code, scripts)
- Progressive disclosure (load details on demand)

---

## The LangGraph Tutor Example

Both the agent and skill teach LangGraph, but differently:

### Agent Approach (`agents/langgraph-tutor.md`)

- **Single file** with comprehensive instructions
- **Manual invocation** - ask about LangGraph
- **All content in one place** - instructions, examples, patterns
- **~500 lines** of markdown

**Use when:** You want Claude to adopt a LangGraph expert persona.

### Skill Approach (`skills/langgraph-tutor/`)

- **Directory structure** with organized content
- **Auto-triggered** by keywords like "langgraph", "state graph"
- **Progressive disclosure**:
  - `SKILL.md` - Core concepts (~200 lines)
  - `references/` - Deep dives (~1000+ lines total)
  - `examples/` - Runnable Python files
  - `scripts/` - Validation and setup tools
- **Artifacts included** - actual code you can run

**Use when:** You need a full teaching toolkit with runnable examples.

---

## Side-by-Side Comparison

| Aspect | Agent | Skill |
| --- | --- | --- |
| **Files** | 1 markdown file | Directory with multiple files |
| **Setup** | Copy one file | Copy entire directory |
| **Activation** | Manual (ask about topic) | Automatic (keyword detection) |
| **Content loading** | All at once | Progressive (on-demand) |
| **Code examples** | Embedded in markdown | Separate runnable files |
| **Scripts** | Not supported | Supported (in `scripts/`) |
| **Best for** | Simple behaviors | Complex workflows |
| **Context usage** | Higher (all loaded) | Lower (loads as needed) |

---

## Teaching with These Examples

### Lesson 1: Create a Simple Agent

1. Show `agents/langgraph-tutor.md`
2. Explain the structure:
   - Configuration (name, description, tools)
   - Instructions (how to behave)
   - Examples (sample interactions)
3. Copy to `~/.claude/agents/`
4. Test by asking about LangGraph

### Lesson 2: Create a Full Skill

1. Show `skills/langgraph-tutor/` structure
2. Explain progressive disclosure:
   - SKILL.md loads first
   - References load when needed
   - Examples are available to run
3. Copy to `~/.claude/skills/`
4. Test by mentioning "langgraph" keywords
5. Ask Claude to run an example

### Lesson 3: When to Use Which

**Use an Agent when:**
- Simple persona or behavior change
- All instructions fit in one file
- No external files needed
- Quick to set up and modify

**Use a Skill when:**
- Complex topic with many aspects
- Need runnable code examples
- Want utility scripts included
- Content should load progressively
- Teaching or documentation use case

---

## Quick Start

```bash
# Install both
cp agents/langgraph-tutor.md ~/.claude/agents/
cp -r skills/langgraph-tutor ~/.claude/skills/

# Test the agent
# Ask: "Explain LangGraph StateGraph"

# Test the skill
# Say: "I need help with langgraph"
# Ask: "Run the simple chatbot example"
```

---

## Resources

- [Claude Code Documentation](https://docs.anthropic.com/claude-code)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [INSTALL.md](INSTALL.md) - Detailed installation instructions
