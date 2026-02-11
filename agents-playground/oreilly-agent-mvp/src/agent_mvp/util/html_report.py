"""HTML report generator for pipeline runs.

Generates attractive, educational HTML reports that explain:
- What happened at each pipeline stage
- Why each agent made its decisions
- Enterprise-class advice for production deployments
"""

from __future__ import annotations

import html
from pathlib import Path

from ..models import PipelineResult


PIPELINE_EDUCATION = {
    "overview": "<p>This report shows the results of an <strong>AI Agent Pipeline</strong> that processed a GitHub issue through three specialized agents.</p><p>Key patterns demonstrated: <strong>Separation of Concerns</strong> (each agent has focused responsibility), <strong>Chain of Thought</strong> (complex tasks broken into steps), and <strong>Human-in-the-Loop</strong> (QA checkpoint before action).</p>",
    "pm_agent": "<h4>PM Agent</h4><p>The PM (Product Manager) agent acts as a <em>strategic analyst</em>. It transforms vague requirements into actionable specifications with acceptance criteria and implementation plans. This prevents costly misunderstandings downstream.</p>",
    "dev_agent": "<h4>Dev Agent</h4><p>The Dev agent is the <em>implementer</em>. It takes the PM's plan and produces code, tests, and implementation notes. This demonstrates <em>context chaining</em> - each agent builds on the previous agent's work.</p>",
    "qa_agent": "<h4>QA Agent</h4><p>The QA agent is the <em>critical reviewer</em>. It examines Dev output against PM criteria and provides a verdict (pass/fail/needs-human). This quality gate prevents poor-quality code from proceeding.</p>",
}

ENTERPRISE_ADVICE = {
    "architecture": "<h4>Scaling This Architecture</h4><ul><li><strong>Message Queues</strong>: Use Redis/RabbitMQ for async processing</li><li><strong>Horizontal Scaling</strong>: Each agent can run as a separate service</li><li><strong>State Management</strong>: Consider event sourcing for audit trails</li><li><strong>Caching</strong>: Cache LLM responses for identical inputs</li></ul>",
    "security": "<h4>Security Considerations</h4><ul><li><strong>Prompt Injection</strong>: Sanitize all user input before passing to LLMs</li><li><strong>Code Execution</strong>: Never auto-execute generated code without sandbox</li><li><strong>Secrets</strong>: Use secret managers (Azure Key Vault, AWS Secrets Manager)</li><li><strong>Rate Limiting</strong>: Protect against API abuse and cost overruns</li></ul>",
    "monitoring": "<h4>Production Monitoring</h4><ul><li><strong>Token Tracking</strong>: Monitor usage to predict costs</li><li><strong>Latency Metrics</strong>: Alert on slow LLM responses</li><li><strong>Error Rates</strong>: Track JSON parse failures and API errors</li><li><strong>Quality Metrics</strong>: Track pass/fail ratio over time</li></ul>",
    "cost": "<h4>Cost Optimization</h4><ul><li><strong>Model Selection</strong>: Use cheaper models for simpler tasks</li><li><strong>Prompt Engineering</strong>: Shorter prompts = lower costs</li><li><strong>Caching</strong>: Semantic caching for similar queries</li><li><strong>Batching</strong>: Process multiple issues in parallel</li></ul>",
}


HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Pipeline Report: {issue_id}</title>
<style>
:root{{--primary:#2563eb;--primary-dark:#1d4ed8;--success:#16a34a;--warning:#ca8a04;--danger:#dc2626;--bg:#f8fafc;--card-bg:#fff;--text:#1e293b;--text-muted:#64748b;--border:#e2e8f0;--code-bg:#1e293b}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:var(--bg);color:var(--text);line-height:1.6;padding:2rem}}
.container{{max-width:1200px;margin:0 auto}}
header{{text-align:center;margin-bottom:2rem;padding:2rem;background:linear-gradient(135deg,var(--primary),var(--primary-dark));border-radius:12px;color:#fff}}
header h1{{font-size:2rem;margin-bottom:.5rem}}
.subtitle{{opacity:.9;font-size:1.1rem}}
.verdict{{display:inline-block;padding:.5rem 1.5rem;border-radius:50px;font-weight:bold;font-size:1.1rem;margin-top:1rem;text-transform:uppercase;letter-spacing:.05em}}
.verdict.pass{{background:var(--success)}}
.verdict.fail{{background:var(--danger)}}
.verdict.needs-human{{background:var(--warning);color:#1e293b}}
.card{{background:var(--card-bg);border-radius:12px;padding:1.5rem;margin-bottom:1.5rem;box-shadow:0 1px 3px rgba(0,0,0,.1);border:1px solid var(--border)}}
.card h2{{color:var(--primary);margin-bottom:1rem;padding-bottom:.5rem;border-bottom:2px solid var(--border)}}
.card h3{{color:var(--text);margin:1.5rem 0 .75rem;font-size:1.1rem}}
.card h4{{color:var(--primary-dark);margin:1rem 0 .5rem;font-size:1rem}}
.education-box{{background:#eff6ff;border-left:4px solid var(--primary);padding:1rem 1.5rem;margin:1rem 0;border-radius:0 8px 8px 0}}
.enterprise-box{{background:#fef3c7;border-left:4px solid var(--warning);padding:1rem 1.5rem;margin:1rem 0;border-radius:0 8px 8px 0}}
ul,ol{{margin:.5rem 0 .5rem 1.5rem}}
li{{margin:.25rem 0}}
.metrics-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:1rem;margin:1rem 0}}
.metric{{background:var(--bg);padding:1rem;border-radius:8px;text-align:center}}
.metric-value{{font-size:1.5rem;font-weight:bold;color:var(--primary)}}
.metric-label{{font-size:.875rem;color:var(--text-muted)}}
.file-block{{margin:1rem 0;border:1px solid var(--border);border-radius:8px;overflow:hidden}}
.file-header{{background:var(--code-bg);color:#e2e8f0;padding:.75rem 1rem;font-family:'Monaco','Consolas',monospace;font-size:.875rem;display:flex;justify-content:space-between}}
.file-language{{background:var(--primary);padding:.25rem .5rem;border-radius:4px;font-size:.75rem}}
pre{{background:var(--code-bg);color:#e2e8f0;padding:1rem;overflow-x:auto;font-family:'Monaco','Consolas',monospace;font-size:.875rem;line-height:1.5;margin:0}}
code{{font-family:'Monaco','Consolas',monospace}}
.finding{{background:#fef2f2;border-left:4px solid var(--danger);padding:.75rem 1rem;margin:.5rem 0;border-radius:0 8px 8px 0}}
.suggestion{{background:#f0fdf4;border-left:4px solid var(--success);padding:.75rem 1rem;margin:.5rem 0;border-radius:0 8px 8px 0}}
.pipeline-flow{{display:flex;justify-content:center;align-items:center;gap:.5rem;padding:1.5rem;background:var(--bg);border-radius:8px;margin:1rem 0;flex-wrap:wrap}}
.pipeline-node{{background:var(--primary);color:#fff;padding:.75rem 1.25rem;border-radius:8px;font-weight:500}}
.pipeline-arrow{{color:var(--text-muted);font-size:1.5rem}}
.token-table{{width:100%;border-collapse:collapse;margin:1rem 0}}
.token-table th,.token-table td{{padding:.75rem;text-align:left;border-bottom:1px solid var(--border)}}
.token-table th{{background:var(--bg);font-weight:600}}
.token-table tr:last-child{{font-weight:bold;background:var(--bg)}}
.next-steps{{background:#f0f9ff;padding:1.5rem;border-radius:8px;margin:1rem 0}}
.next-steps h3{{margin-top:0;color:var(--primary)}}
footer{{text-align:center;padding:2rem;color:var(--text-muted);font-size:.875rem}}
</style>
</head>
<body>
<div class="container">
<header>
<h1>AI Agent Pipeline Report</h1>
<div class="subtitle">{issue_id}: {issue_title}</div>
<div class="verdict {verdict_class}">{verdict}</div>
</header>

<div class="card">
<h2>Pipeline Overview</h2>
<div class="education-box">{pipeline_overview}</div>
<div class="pipeline-flow">
<div class="pipeline-node">Issue</div>
<span class="pipeline-arrow">&rarr;</span>
<div class="pipeline-node">PM Agent</div>
<span class="pipeline-arrow">&rarr;</span>
<div class="pipeline-node">Dev Agent</div>
<span class="pipeline-arrow">&rarr;</span>
<div class="pipeline-node">QA Agent</div>
<span class="pipeline-arrow">&rarr;</span>
<div class="pipeline-node">Result</div>
</div>
<div class="metrics-grid">
<div class="metric"><div class="metric-value">{duration}</div><div class="metric-label">Duration</div></div>
<div class="metric"><div class="metric-value">{total_tokens}</div><div class="metric-label">Total Tokens</div></div>
<div class="metric"><div class="metric-value">{total_cost}</div><div class="metric-label">Estimated Cost</div></div>
<div class="metric"><div class="metric-value">{num_files}</div><div class="metric-label">Files Generated</div></div>
</div>
</div>

<div class="card">
<h2>Original Issue</h2>
<p><strong>Repository:</strong> <a href="{issue_url}">{issue_repo}</a></p>
<p><strong>Labels:</strong> {issue_labels}</p>
<h3>Description</h3>
<div style="background:var(--bg);padding:1rem;border-radius:8px;white-space:pre-wrap">{issue_body}</div>
</div>

<div class="card">
<h2>PM Agent Analysis</h2>
<div class="education-box">{pm_education}</div>
<h3>Summary</h3>
<p>{pm_summary}</p>
<h3>Acceptance Criteria</h3>
<ol>{pm_criteria}</ol>
<h3>Implementation Plan</h3>
<ol>{pm_plan}</ol>
{pm_assumptions}
</div>

<div class="card">
<h2>Dev Agent Implementation</h2>
<div class="education-box">{dev_education}</div>
{dev_files}
{dev_notes}
</div>

<div class="card">
<h2>QA Agent Review</h2>
<div class="education-box">{qa_education}</div>
<h3>Verdict: <span style="color:{verdict_color};font-weight:bold">{verdict}</span></h3>
<h3>Findings</h3>
{qa_findings}
<h3>Suggested Changes</h3>
{qa_suggestions}
</div>

<div class="card">
<h2>Next Steps</h2>
<div class="next-steps">
<ol>{next_steps}</ol>
</div>
</div>

<div class="card">
<h2>Token Usage &amp; Cost Analysis</h2>
<div class="enterprise-box">{cost_advice}</div>
{token_table}
</div>

<div class="card">
<h2>Enterprise Architecture Advice</h2>
<div class="enterprise-box">{architecture_advice}</div>
<div class="enterprise-box">{security_advice}</div>
<div class="enterprise-box">{monitoring_advice}</div>
</div>

<footer>
<p>Generated by O'Reilly Agent MVP | Run ID: {run_id}</p>
<p>Timestamp: {timestamp}</p>
</footer>
</div>
</body>
</html>'''


def escape(text: str) -> str:
    """HTML-escape text."""
    return html.escape(str(text))


def generate_html_report(result: PipelineResult) -> str:
    """Generate an HTML report from a pipeline result."""
    verdict_value = result.qa.verdict.value
    verdict_class = verdict_value
    verdict_colors = {"pass": "#16a34a", "fail": "#dc2626", "needs-human": "#ca8a04"}
    verdict_color = verdict_colors.get(verdict_value, "#64748b")

    duration = "N/A"
    if result.metadata and result.metadata.duration_seconds:
        duration = f"{result.metadata.duration_seconds:.1f}s"

    total_tokens = "N/A"
    total_cost = "N/A"
    token_table = "<p>Token usage data not available.</p>"

    if result.metadata and result.metadata.token_usage:
        tokens = result.metadata.token_usage
        total_tokens = f"{tokens.total_tokens:,}"
        if tokens.estimated_total_cost_usd is not None:
            total_cost = f"${tokens.estimated_total_cost_usd:.4f}"

        rows = []
        for agent in tokens.agents:
            cost = agent.usage.estimated_cost_usd
            cost_str = f"${cost:.6f}" if cost else "N/A"
            rows.append(
                f"<tr><td>{escape(agent.agent_name)}</td>"
                f"<td>{agent.usage.input_tokens:,}</td>"
                f"<td>{agent.usage.output_tokens:,}</td>"
                f"<td>{agent.usage.total_tokens:,}</td>"
                f"<td>{cost_str}</td></tr>"
            )
        rows.append(
            f"<tr><td><strong>TOTAL</strong></td>"
            f"<td><strong>{tokens.total_input_tokens:,}</strong></td>"
            f"<td><strong>{tokens.total_output_tokens:,}</strong></td>"
            f"<td><strong>{tokens.total_tokens:,}</strong></td>"
            f"<td><strong>{total_cost}</strong></td></tr>"
        )
        token_table = (
            "<table class='token-table'><thead><tr>"
            "<th>Agent</th><th>Input Tokens</th><th>Output Tokens</th>"
            "<th>Total Tokens</th><th>Est. Cost</th></tr></thead>"
            f"<tbody>{''.join(rows)}</tbody></table>"
        )

    pm_criteria = "".join(f"<li>{escape(c)}</li>" for c in result.pm.acceptance_criteria)
    pm_plan = "".join(f"<li>{escape(step)}</li>" for step in result.pm.plan)
    pm_assumptions = ""
    if result.pm.assumptions:
        assumptions_list = "".join(f"<li>{escape(a)}</li>" for a in result.pm.assumptions)
        pm_assumptions = f"<h3>Assumptions</h3><ul>{assumptions_list}</ul>"

    dev_files_html = ""
    for f in result.dev.files:
        content = escape(f.content)
        dev_files_html += (
            f'<div class="file-block">'
            f'<div class="file-header"><span>{escape(f.path)}</span>'
            f'<span class="file-language">{escape(f.language)}</span></div>'
            f"<pre><code>{content}</code></pre></div>"
        )
    if not dev_files_html:
        dev_files_html = "<p>No files generated.</p>"

    dev_notes = ""
    if result.dev.notes:
        notes_list = "".join(f"<li>{escape(n)}</li>" for n in result.dev.notes)
        dev_notes = f"<h3>Implementation Notes</h3><ul>{notes_list}</ul>"

    qa_findings = "".join(
        f'<div class="finding">{escape(f)}</div>' for f in result.qa.findings
    ) or "<p>No findings.</p>"

    qa_suggestions = "".join(
        f'<div class="suggestion">{escape(s)}</div>' for s in result.qa.suggested_changes
    ) or "<p>No suggested changes.</p>"

    next_steps = "".join(f"<li>{escape(step)}</li>" for step in result.next_steps)

    issue_labels = ", ".join(
        f"<code>{escape(label)}</code>" for label in result.issue.labels
    ) or "None"

    return HTML_TEMPLATE.format(
        issue_id=escape(result.issue.issue_id),
        issue_title=escape(result.issue.title),
        verdict=verdict_value.upper(),
        verdict_class=verdict_class,
        verdict_color=verdict_color,
        pipeline_overview=PIPELINE_EDUCATION["overview"],
        duration=duration,
        total_tokens=total_tokens,
        total_cost=total_cost,
        num_files=len(result.dev.files),
        issue_url=escape(result.issue.url),
        issue_repo=escape(result.issue.repo),
        issue_labels=issue_labels,
        issue_body=escape(result.issue.body),
        pm_education=PIPELINE_EDUCATION["pm_agent"],
        pm_summary=escape(result.pm.summary),
        pm_criteria=pm_criteria,
        pm_plan=pm_plan,
        pm_assumptions=pm_assumptions,
        dev_education=PIPELINE_EDUCATION["dev_agent"],
        dev_files=dev_files_html,
        dev_notes=dev_notes,
        qa_education=PIPELINE_EDUCATION["qa_agent"],
        qa_findings=qa_findings,
        qa_suggestions=qa_suggestions,
        next_steps=next_steps,
        token_table=token_table,
        cost_advice=ENTERPRISE_ADVICE["cost"],
        architecture_advice=ENTERPRISE_ADVICE["architecture"],
        security_advice=ENTERPRISE_ADVICE["security"],
        monitoring_advice=ENTERPRISE_ADVICE["monitoring"],
        run_id=escape(result.run_id),
        timestamp=escape(result.timestamp_utc),
    )


def save_html_report(result: PipelineResult, output_path: Path) -> Path:
    """Save an HTML report to disk.

    Args:
        result: The pipeline result to render.
        output_path: Path for the JSON result (HTML will use same name with .html).

    Returns:
        Path to the saved HTML file.
    """
    html_content = generate_html_report(result)
    html_path = Path(output_path).with_suffix(".html")
    html_path.write_text(html_content, encoding="utf-8")
    return html_path
