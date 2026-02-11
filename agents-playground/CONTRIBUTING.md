# Contributing to agents2

Thank you for your interest in contributing to this O'Reilly Live Learning project! 🎉

This repository demonstrates AI agent patterns for educational purposes. We welcome contributions that improve the learning experience.

## 🎯 Project Goals

This project aims to:
- Teach AI agent orchestration patterns (LangGraph, CrewAI)
- Provide working examples for O'Reilly courses
- Demonstrate production-ready practices
- Remain beginner-friendly and well-documented

## 🤝 How to Contribute

### Types of Contributions Welcome

#### 📚 Documentation
- Fix typos or unclear explanations
- Add examples or clarifications
- Improve teaching guides
- Translate to other languages

#### 🐛 Bug Fixes
- Fix broken functionality
- Improve error handling
- Update deprecated dependencies

#### ✨ Features (Please Discuss First)
- New agent types (Security, Documentation, etc.)
- Additional LLM providers
- New orchestration patterns
- Teaching aids (diagrams, exercises)

#### ❌ Not Accepting
- Major architecture changes (would break teaching flow)
- Features that complicate setup
- Non-educational additions

## 🚀 Getting Started

### 1. Fork and Clone

```bash
# Fork on GitHub, then:
git clone https://github.com/YOUR-USERNAME/agents2.git
cd agents2/oreilly-agent-mvp
```

### 2. Set Up Environment

```bash
# Create virtual environment
python -m venv .venv
source .venv/Scripts/activate  # Git Bash/Linux/Mac
# OR
.\.venv\Scripts\Activate.ps1   # PowerShell

# Install dependencies (editable mode)
pip install -e ".[dev]"

# Configure .env
cp .env.example .env
# Add your API keys
```

### 3. Create a Branch

```bash
git checkout -b feature/your-feature-name
# OR
git checkout -b fix/issue-description
```

### 4. Make Changes

- Follow existing code style (see Code Standards below)
- Add tests if applicable
- Update documentation
- Keep commits focused and atomic

### 5. Test Your Changes

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=agent_mvp

# Test the interactive menu
agent-menu

# Process a mock issue
agent-mvp mock_issues/issue_001.json
```

### 6. Commit and Push

```bash
git add .
git commit -m "feat: add security agent example"
# Use conventional commits: feat, fix, docs, test, refactor

git push origin feature/your-feature-name
```

### 7. Open a Pull Request

- Go to the [Pull Requests page](https://github.com/timothywarner-org/agents2/pulls)
- Click "New Pull Request"
- Select your branch
- Fill out the PR template

## 📋 Pull Request Guidelines

### PR Checklist

- [ ] Branch is up-to-date with `main`
- [ ] Tests pass locally (`pytest`)
- [ ] Code follows style guidelines (see below)
- [ ] Documentation is updated
- [ ] Commit messages are clear
- [ ] PR description explains what/why

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation
- [ ] Refactoring
- [ ] Teaching improvement

## Testing
How did you test this?

## Screenshots (if applicable)
Add screenshots for UI/output changes

## Related Issues
Closes #123
```

## 🎨 Code Standards

### Python Style

- **PEP 8** compliance
- **Line length:** 100 characters (configured in ruff)
- **Type hints:** Use where helpful (not required everywhere)
- **Docstrings:** Required for public functions

```python
def example_function(param: str) -> dict:
    """
    Brief description of what this does.

    Args:
        param: Description of parameter

    Returns:
        Description of return value
    """
    return {"result": param}
```

### Project Structure

```
src/agent_mvp/
├── __init__.py           # Package metadata only
├── models.py             # Pydantic models
├── config.py             # Configuration
├── pipeline/             # Agent orchestration
│   ├── graph.py         # LangGraph
│   ├── crew.py          # CrewAI
│   └── prompts.py       # Prompt templates
└── integrations/         # External services
```

**Rules:**
- No business logic in `__init__.py`
- Keep prompts separate from orchestration
- Use Pydantic for all data models
- Avoid deep nesting (max 3 levels)

### Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: add cost tracking to pipeline
fix: handle missing GitHub token gracefully
docs: update Hour 3 teaching guide
test: add schema validation tests
refactor: simplify error handling in watcher
```

### Testing

- Write tests for new features
- Keep tests simple and focused
- Use descriptive test names
- Mock external API calls

```python
def test_pm_agent_returns_valid_output():
    """PM agent should return structured PMOutput."""
    # Given
    issue = Issue(title="Test", description="...", ...)

    # When
    result = pm_node({"issue": issue.model_dump()})

    # Then
    assert "pm_output" in result
    assert PMOutput(**result["pm_output"])  # Validates schema
```

## 📖 Documentation Guidelines

### Teaching Guides

Located in `docs/`:
- Use simple language (middle school reading level)
- Include exact file paths and line numbers
- Add "What to SAY" vs "What to DO" sections
- Provide time estimates
- Include troubleshooting tips

### README Updates

- Keep main README focused on course outline
- Put technical details in `oreilly-agent-mvp/README.md`
- Use mermaid diagrams for visual learners
- Add code examples with comments

### Code Comments

- Explain WHY, not WHAT
- Document non-obvious decisions
- Use TODO/FIXME for known issues
- Keep comments up-to-date with code

```python
# Use structured JSON to ensure reliable parsing
# Natural language responses would require brittle regex
pm_data = _extract_json(response.content)
```

## 🔍 Review Process

### What We Look For

✅ **Good:**
- Solves a real problem
- Well-tested
- Clear documentation
- Maintains simplicity
- Enhances learning

❌ **Needs Work:**
- Breaks existing functionality
- Lacks tests
- Complicates setup
- Missing documentation

### Timeline

- Initial review: Within 3 business days
- Feedback: Ongoing conversation
- Merge: When approved by maintainer

## 💬 Getting Help

### Questions?

- **Documentation:** Check `oreilly-agent-mvp/README.md` first
- **Issues:** [Search existing issues](https://github.com/timothywarner-org/agents2/issues)
- **Discussion:** [Open a discussion](https://github.com/timothywarner-org/agents2/discussions)
- **Email:** tim@techtrainertim.com (for complex questions)

### Stuck on Setup?

See [Troubleshooting Guide](oreilly-agent-mvp/README.md#troubleshooting)

## 🏆 Recognition

Contributors are recognized in:
- Pull request acknowledgments
- Release notes (for significant contributions)
- Optional mention in course materials

## 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License.

## 🙏 Thank You!

Your contributions help thousands of learners understand AI agents better. Every typo fix, bug report, and feature makes this project more valuable.

**Tim Warner**
tim@techtrainertim.com
[TechTrainerTim.com](https://TechTrainerTim.com)

---

*Happy coding! 🚀*
