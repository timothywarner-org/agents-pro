from __future__ import annotations

from pathlib import Path
import re

path = Path(r"c:/github/agents2/docs/chatgpt_research.md")
text = path.read_text(encoding="utf-8")

text = text.replace("\r\n", "\n")
text = re.sub(r"\n([.,;:?!])", r"\1", text)

heading_map = {
    "Enterprise AI Agents in 2026: Key Considerations and Best Practices": "# Enterprise AI Agents in 2026: Key Considerations and Best Practices",
    "Design Considerations for AI Agents": "## Design Considerations for AI Agents",
    "Architectural Frameworks and Platforms": "## Architectural Frameworks and Platforms",
    "Implementation Stack: Tools and Best Practices": "## Implementation Stack: Tools and Best Practices",
    "Security and Compliance Controls": "## Security and Compliance Controls",
    "Testing and Evaluation Workflows": "## Testing and Evaluation Workflows",
    "Maintenance and Operations": "## Maintenance and Operations",
    "2026 Outlook and Emerging Trends": "## 2026 Outlook and Emerging Trends",
    "Recommendations and Next Steps for the Agent MVP": "## Recommendations and Next Steps for the Agent MVP",
}

for original, replacement in heading_map.items():
    text = re.sub(fr"(?m)^\s*{re.escape(original)}\s*$", replacement, text, count=1)

text = re.sub(r"([.!?]) (Immediate Actions)", r"\1\n\2", text)
text = re.sub(r"([.!?]) (If You Have More Time)", r"\1\n\2", text)

text = re.sub(r"(?m)^(#{1,3} .+)$", r"\1\n", text)

lines = text.splitlines()
new_lines: list[str] = []
i = 0
while i < len(lines):
    stripped = lines[i].strip()
    if stripped.startswith("Immediate Actions ") and stripped.endswith(":"):
        new_lines.append(f"### {stripped[:-1]}")
        new_lines.append("")
        i += 1
        while i < len(lines):
            candidate = lines[i].strip()
            if not candidate:
                i += 1
                continue
            if (
                candidate.startswith("Immediate Actions ")
                or candidate.startswith("If You Have More Time ")
                or candidate.startswith("## ")
                or candidate.startswith("# ")
                or candidate.startswith("Table: ")
            ):
                break
            new_lines.append(f"- {candidate}")
            i += 1
        new_lines.append("")
        continue
    if stripped.startswith("If You Have More Time ") and stripped.endswith(":"):
        new_lines.append(f"### {stripped[:-1]}")
        new_lines.append("")
        i += 1
        while i < len(lines):
            candidate = lines[i].strip()
            if not candidate:
                i += 1
                continue
            if (
                candidate.startswith("Immediate Actions ")
                or candidate.startswith("If You Have More Time ")
                or candidate.startswith("## ")
                or candidate.startswith("# ")
                or candidate.startswith("Table: ")
            ):
                break
            new_lines.append(f"- {candidate}")
            i += 1
        new_lines.append("")
        continue
    new_lines.append(lines[i])
    i += 1

text = "\n".join(new_lines)

if "Framework / Platform" in text and "Table: Leading AI Agent frameworks in 2026" in text:
    start = text.index("Framework / Platform")
    end = text.index("Table: Leading AI Agent frameworks in 2026")
    table = """Framework / Platform | Maturity (2026) | Guardrails & Compliance | Ecosystem & Integrations | TCO & Hosting
--- | --- | --- | --- | ---
LangGraph (LangChain) | Mature open-source (since 2024). Used in production by advanced teams. | Strong custom guardrails possible with RBAC and state persistence. | Part of the LangChain ecosystem; integrates with LangSmith. Python-centric. | Self-hosted library. Low license cost, higher engineering effort.
CrewAI (open-source + AMP) | High adoption by 2025 with an enterprise Agent Management Platform. | Built-in workflow tracing, task guardrails, and role-based access control. | Rich OSS integrations (tools, memory) plus an enterprise UI. | Hosted SaaS (CrewAI AMP) or self-managed. Fast value, limited ceiling for extreme cases.
Microsoft Agent Framework | Public preview in late 2025, GA expected Q1 2026. | Enterprise-grade compliance, Azure AD integration, and managed governance. | Deep Azure integrations, multi-language support, Agent-to-Agent protocol. | Higher Azure costs but tightly supported; ideal for Microsoft-centric orgs.
AWS Agents for Bedrock | Launched 2024 on AWS Bedrock infrastructure. | Explicit tool/data permissions and managed memory/knowledge stores. | Native integrations with AWS services and Bedrock model catalog. | Fully managed, serverless runtime with pay-per-use pricing.
Google Vertex AI Agents | Rapidly evolving multi-agent platform aligned to open protocols. | Deterministic guardrails via Agent Dev Kit and managed policy enforcement. | Ecosystem-neutral with LangChain, LangGraph, CrewAI support and 100+ connectors. | Managed Vertex Agent Engine with competitive pricing and cross-framework flexibility.
Salesforce Einstein / Agentforce | Internal platform extended to customers in 2025. | Atlas Reasoner guardrails, MCP connectivity, and secure agent delegation. | Deep Salesforce integration with published pattern library. | Bundled with Salesforce licensing; best for existing Salesforce customers.
NVIDIA NeMo + Guardrails | Mature framework plus open-source safety toolkit. | Programmable guardrails enforce format, citations, and safety policies. | Integrates with NVIDIA AI stack; layers onto other orchestrators. | Open-source; infrastructure costs tied to NVIDIA hardware or cloud.
Meta Llama Stack (Open) | Vibrant open ecosystem around Llama models. | No native guardrails; relies on add-on safety tooling. | Highly flexible mix-and-match with OSS tools like LangChain or Haystack. | Free software, higher engineering overhead and hosting responsibilities.
"""
    text = text[:start] + table + text[end:]

text = re.sub(r"\n{3,}", "\n\n", text)
text = text.strip() + "\n"

path.write_text(text, encoding="utf-8")
