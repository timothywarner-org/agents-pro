# Hour 3 Teaching Guide: MCP and RAG Implementation

**Goal:** Students configure MCP server/client integration and implement a RAG vector source using vibe coding with Claude Code.

**Time:** 60 minutes

---

## Opening (3 minutes)

**What We're Doing This Hour:**

1. Understand MCP (Model Context Protocol)
2. Configure our MCP server and test it
3. Connect MCP to Claude Desktop and VS Code
4. **Vibe code** a new feature: local RAG vector source
5. Use ChromaDB for cheap, local vector storage

**Key Message:** "MCP is how you give AI assistants superpowers. RAG is how you give them memory. We're doing both."

---

## What is MCP? (10 minutes)

### The Problem MCP Solves

**Draw on whiteboard:**

```
Before MCP:
┌──────────┐     ┌──────────┐     ┌──────────┐
│ Claude   │     │ Copilot  │     │ Cursor   │
└────┬─────┘     └────┬─────┘     └────┬─────┘
     │                │                │
     ▼                ▼                ▼
  Custom           Custom           Custom
Integration      Integration      Integration
     │                │                │
     ▼                ▼                ▼
┌──────────────────────────────────────────┐
│           Your Application               │
└──────────────────────────────────────────┘

After MCP:
┌──────────┐     ┌──────────┐     ┌──────────┐
│ Claude   │     │ Copilot  │     │ Cursor   │
└────┬─────┘     └────┬─────┘     └────┬─────┘
     │                │                │
     └────────────────┼────────────────┘
                      ▼
               ┌──────────────┐
               │  MCP Server  │ ← One integration
               └──────────────┘
                      │
                      ▼
               ┌──────────────┐
               │ Your App     │
               └──────────────┘
```

**Say:** "MCP is a standard protocol. Build once, connect to any AI assistant."

### MCP Architecture

**Three components:**

| Component | Role | Example |
| --- | --- | --- |
| **Server** | Exposes tools, resources, prompts | Our `agent-mcp` server |
| **Client** | Calls tools, reads resources | Claude Desktop, VS Code |
| **Transport** | Communication layer | stdio (local), HTTP (remote) |

### Our MCP Server Capabilities

**Show the summary:**

```
╔══════════════════════════════════════════╗
║          O'REILLY AGENT MVP MCP          ║
╠══════════════════════════════════════════╣
║ TOOLS (5):                               ║
║  • fetch_github_issue                    ║
║  • list_mock_issues                      ║
║  • load_mock_issue                       ║
║  • run_agent_pipeline                    ║
║  • process_issue_file                    ║
╠══════════════════════════════════════════╣
║ RESOURCES (4):                           ║
║  • config://settings                     ║
║  • issues://mock/{filename}              ║
║  • pipeline://schema                     ║
║  • pipeline://architecture               ║
╠══════════════════════════════════════════╣
║ PROMPTS (3):                             ║
║  • analyze_github_issue                  ║
║  • review_implementation_plan            ║
║  • generate_test_issue                   ║
╚══════════════════════════════════════════╝
```

---

## Configure MCP Server (12 minutes)

### Start the Server (3 minutes)

**Verify MCP is installed:**

```bash
cd agents2/oreilly-agent-mvp
source .venv/Scripts/activate

# Check MCP package
pip show mcp

# If not installed:
pip install mcp>=1.0.0
pip install -e .
```

**Start the server:**

```bash
# Option 1: CLI command
agent-mcp

# Option 2: Direct Python
python -m agent_mvp.mcp_server

# Option 3: PowerShell launcher
.\mcp.ps1
```

### Test with MCP Inspector (5 minutes)

**Launch the inspector (requires Node.js):**

```bash
# Git Bash / Linux / macOS
./scripts/run_mcp_inspector.sh

# PowerShell
.\scripts\run_mcp_inspector.ps1
```

**In the browser:**

1. Navigate to the Tools tab
2. Click "list_mock_issues"
3. Click "Run"
4. See the list of available mock issues

**Try other tools:**

- `load_mock_issue` with filename: `issue_001.json`
- `run_agent_pipeline` with the loaded issue

**Say:** "The Inspector lets you test MCP tools interactively before connecting to Claude."

### Connect to Claude Desktop (4 minutes)

**Find the config file:**

- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

**Add server configuration:**

```json
{
  "mcpServers": {
    "oreilly-agent-mvp": {
      "command": "python",
      "args": ["-m", "agent_mvp.mcp_server"],
      "cwd": "C:/github/agents2/oreilly-agent-mvp",
      "env": {
        "PYTHONPATH": "C:/github/agents2/oreilly-agent-mvp/src"
      }
    }
  }
}
```

**IMPORTANT:** Update paths to match your system!

**Restart Claude Desktop completely (quit from system tray).**

**Verify connection:**

- Look for the 🔌 (plug) icon in Claude's interface
- Test with: "List available mock issues"

---

## Vibe Coding: Add RAG Vector Source (30 minutes)

### What is Vibe Coding?

**Say:** "Vibe coding is using AI to implement features conversationally. You describe WHAT you want, Claude Code figures out HOW."

**The approach:**

1. Describe the feature clearly
2. Let Claude Code explore and implement
3. Review, iterate, refine
4. Test the result

### The Feature: Local RAG for Issue Context

**What we're building:**

```
┌─────────────────────────────────────────┐
│           RAG-Enhanced Pipeline         │
├─────────────────────────────────────────┤
│                                         │
│  Issue → [Vector Search] → Similar      │
│              ↓            Issues        │
│         [PM Agent] ← Context from       │
│              ↓        past issues       │
│         [Dev Agent]                     │
│              ↓                          │
│         [QA Agent]                      │
│                                         │
└─────────────────────────────────────────┘
```

**Why local and cheap?**

- ChromaDB runs in-process (no external service)
- Free, no API costs for embeddings (use sentence-transformers)
- Fast iteration during development
- Easy to upgrade to cloud later

### Step 1: Start Claude Code (5 minutes)

**Open Claude Code in the project:**

```bash
cd agents2/oreilly-agent-mvp
claude
```

**Initial exploration prompt:**

```
I want to add a RAG (Retrieval Augmented Generation) feature to this
agent pipeline. The goal is to:

1. Store processed issues in a local vector database (ChromaDB)
2. When a new issue comes in, find similar past issues
3. Provide that context to the PM agent for better analysis

First, explore the codebase and tell me:
- Where would the vector store fit in the architecture?
- What files would need to change?
- What dependencies do we need?
```

**Watch Claude Code:**

- It will read `pipeline/graph.py`
- It will examine `models.py`
- It will suggest an approach

### Step 2: Install Dependencies (3 minutes)

**Have Claude Code add dependencies:**

```
Add ChromaDB and sentence-transformers to our dependencies.
Use a lightweight embedding model that runs locally.
Update pyproject.toml and install them.
```

**Expected additions:**

```toml
# In pyproject.toml
dependencies = [
    # ... existing ...
    "chromadb>=0.4.0",
    "sentence-transformers>=2.2.0",
]
```

**Install:**

```bash
pip install -e .
```

### Step 3: Create Vector Store Module (10 minutes)

**Prompt Claude Code:**

```
Create a new module at src/agent_mvp/rag/vector_store.py that:

1. Initializes a ChromaDB collection for issues
2. Has a function to add an issue (with its full result) to the store
3. Has a function to search for similar issues given a query
4. Uses a small, fast embedding model from sentence-transformers
5. Stores the DB in data/chroma/ (local, not in git)

Keep it simple - we can enhance later.
```

**Review what Claude Code creates:**

```python
# Expected structure:
# src/agent_mvp/rag/vector_store.py

import chromadb
from sentence_transformers import SentenceTransformer

class IssueVectorStore:
    def __init__(self, persist_dir: str = "data/chroma"):
        self.client = chromadb.PersistentClient(path=persist_dir)
        self.collection = self.client.get_or_create_collection("issues")
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')

    def add_issue(self, issue_id: str, title: str, body: str, result: dict):
        """Add a processed issue to the vector store."""
        text = f"{title}\n{body}"
        embedding = self.embedder.encode(text).tolist()
        self.collection.add(
            ids=[issue_id],
            embeddings=[embedding],
            documents=[text],
            metadatas=[{"result": json.dumps(result)}]
        )

    def search_similar(self, query: str, n_results: int = 3):
        """Find similar past issues."""
        embedding = self.embedder.encode(query).tolist()
        results = self.collection.query(
            query_embeddings=[embedding],
            n_results=n_results
        )
        return results
```

### Step 4: Integrate with Pipeline (7 minutes)

**Prompt Claude Code:**

```
Now integrate the vector store with the pipeline:

1. In finalize_node, after saving the result, add the issue to the vector store
2. In pm_node, before calling the LLM, search for similar issues
3. If similar issues are found, add them to the PM prompt as context
4. Update the PM prompt template to accept optional similar_issues context

Make minimal changes - we want this to be easy to toggle on/off.
```

**Key integration points:**

```python
# In graph.py, pm_node:
from agent_mvp.rag.vector_store import IssueVectorStore

def pm_node(state: PipelineState) -> PipelineState:
    # ... existing code ...

    # NEW: Search for similar issues
    try:
        vs = IssueVectorStore()
        similar = vs.search_similar(f"{issue.title}\n{issue.body}")
        similar_context = format_similar_issues(similar)
    except Exception:
        similar_context = ""

    # Include in prompt
    prompt = format_pm_prompt(issue, similar_context=similar_context)
    # ... rest of function ...
```

### Step 5: Test the Feature (5 minutes)

**Run pipeline twice to populate the vector store:**

```bash
agent-menu
# Process issue_001.json
# Process issue_002.json
```

**Check the vector store:**

```bash
ls data/chroma/
# Should see ChromaDB files
```

**Test similarity search:**

```python
# Quick test in Python
from agent_mvp.rag.vector_store import IssueVectorStore

vs = IssueVectorStore()
results = vs.search_similar("API rate limiting")
print(results)
```

**Process a third issue and observe:**

- PM agent should now have context from similar issues
- Check the output for references to past solutions

---

## Wrap-Up (5 minutes)

### What We Accomplished

- Understood MCP architecture and our server
- Configured MCP with Claude Desktop
- Tested tools with MCP Inspector
- Vibe coded a complete RAG feature:
  - ChromaDB local vector store
  - Automatic issue storage after processing
  - Similar issue retrieval for PM context

### The Vibe Coding Process

1. **Describe** the feature at a high level
2. **Explore** the codebase with Claude
3. **Implement** incrementally with prompts
4. **Review** each change before continuing
5. **Test** the integrated feature

### What's Next (Hour 4)

- Deploy to Azure Container Apps
- Set up Azure API Management
- Configure Azure Cosmos DB for state
- Review production best practices

### Quick Reference: MCP Commands

**Start server:**
```bash
agent-mcp
```

**Test with inspector:**
```bash
.\scripts\run_mcp_inspector.ps1
```

**Claude Desktop config location:**
```
Windows: %APPDATA%\Claude\claude_desktop_config.json
macOS: ~/Library/Application Support/Claude/claude_desktop_config.json
```

---

## Teaching Tips

### If MCP Installation Fails

**Common issues:**

```bash
# Missing mcp package
pip install mcp>=1.0.0

# Missing CLI command
pip install -e .

# Node.js required for inspector
# Install from nodejs.org
```

### If Claude Desktop Doesn't Connect

**Checklist:**

1. Config file is valid JSON (no trailing commas)
2. Paths are correct for your system
3. Claude Desktop fully restarted (quit from system tray)
4. Check logs: `%APPDATA%\Claude\logs\mcp*.log`

### If ChromaDB Is Slow

**First run downloads the embedding model (~90MB).**

**Speed up:**
```python
# Use smaller model
embedder = SentenceTransformer('all-MiniLM-L6-v2')  # 80MB, fast

# Instead of larger model
# embedder = SentenceTransformer('all-mpnet-base-v2')  # 420MB, slower
```

### If Students Are Ahead

**Advanced challenges:**

1. Add a new MCP tool: `search_similar_issues`
2. Store embeddings for Dev and QA outputs too
3. Add metadata filtering (by label, repo, date)
4. Implement a "learning mode" that improves prompts based on past successes

### Time Management

- If MCP setup takes too long: Skip Claude Desktop, use Inspector only
- If vibe coding is slow: Have pre-built code ready to show
- If running ahead: Add the MCP tool for vector search

---

## Code Reference: Vector Store

**Full implementation for reference:**

```python
# src/agent_mvp/rag/vector_store.py
"""Local vector store for RAG-enhanced issue processing."""

import json
from pathlib import Path
from typing import Optional

import chromadb
from sentence_transformers import SentenceTransformer


class IssueVectorStore:
    """ChromaDB-backed vector store for processed issues."""

    def __init__(self, persist_dir: str = "data/chroma"):
        """Initialize the vector store.

        Args:
            persist_dir: Directory to persist ChromaDB data
        """
        Path(persist_dir).mkdir(parents=True, exist_ok=True)
        self.client = chromadb.PersistentClient(path=persist_dir)
        self.collection = self.client.get_or_create_collection(
            name="issues",
            metadata={"description": "Processed GitHub issues with results"}
        )
        # Small, fast model for local use
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')

    def add_issue(
        self,
        issue_id: str,
        title: str,
        body: str,
        result: dict
    ) -> None:
        """Add a processed issue to the vector store.

        Args:
            issue_id: Unique identifier for the issue
            title: Issue title
            body: Issue body/description
            result: Full pipeline result dictionary
        """
        text = f"{title}\n\n{body}"
        embedding = self.embedder.encode(text).tolist()

        # Upsert to handle duplicates
        self.collection.upsert(
            ids=[issue_id],
            embeddings=[embedding],
            documents=[text],
            metadatas=[{
                "title": title,
                "result_json": json.dumps(result)
            }]
        )

    def search_similar(
        self,
        query: str,
        n_results: int = 3
    ) -> list[dict]:
        """Find similar past issues.

        Args:
            query: Search query (usually issue title + body)
            n_results: Number of results to return

        Returns:
            List of similar issues with their results
        """
        if self.collection.count() == 0:
            return []

        embedding = self.embedder.encode(query).tolist()
        results = self.collection.query(
            query_embeddings=[embedding],
            n_results=min(n_results, self.collection.count())
        )

        similar = []
        for i, doc in enumerate(results["documents"][0]):
            metadata = results["metadatas"][0][i]
            similar.append({
                "title": metadata.get("title", ""),
                "document": doc,
                "distance": results["distances"][0][i],
                "result": json.loads(metadata.get("result_json", "{}"))
            })

        return similar

    def count(self) -> int:
        """Return the number of stored issues."""
        return self.collection.count()
```

---

## MCP Server Quick Reference

**Available tools:**

| Tool | Description |
| --- | --- |
| `fetch_github_issue` | Fetch issue from GitHub API |
| `list_mock_issues` | List test issue files |
| `load_mock_issue` | Load specific mock issue |
| `run_agent_pipeline` | Run PM→Dev→QA pipeline |
| `process_issue_file` | Process JSON file through pipeline |

**Available resources:**

| URI | Description |
| --- | --- |
| `config://settings` | Current app configuration |
| `issues://mock/{filename}` | Mock issue content |
| `pipeline://schema` | Pydantic model schemas |
| `pipeline://architecture` | Pipeline documentation |

---

**You got this! Vibe code with confidence.**
