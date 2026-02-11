const pptxgen = require('pptxgenjs');
const sharp = require('sharp');
const path = require('path');
const fs = require('fs');

// Import html2pptx
const html2pptx = require('C:/Users/timot/.claude/plugins/cache/anthropic-agent-skills/document-skills/f23222824449/skills/pptx/scripts/html2pptx.js');

// Color palette - Deep Purple & Tech Blue
const colors = {
    primary: '1E293B',      // Dark slate
    secondary: '3B82F6',    // Bright blue
    accent: '10B981',       // Emerald green
    highlight: 'F59E0B',    // Amber
    text: 'F8FAFC',         // Light text
    textDark: '1E293B',     // Dark text
    pmColor: 'F59E0B',      // PM - Amber
    devColor: '10B981',     // Dev - Green
    qaColor: '8B5CF6',      // QA - Purple
    resultColor: '3B82F6'   // Result - Blue
};

async function createGradientBg(filename, color1, color2, angle = 135) {
    const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="1440" height="810">
        <defs>
            <linearGradient id="g" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" style="stop-color:#${color1}"/>
                <stop offset="100%" style="stop-color:#${color2}"/>
            </linearGradient>
        </defs>
        <rect width="100%" height="100%" fill="url(#g)"/>
    </svg>`;
    await sharp(Buffer.from(svg)).png().toFile(filename);
    return filename;
}

async function createPresentation() {
    const slidesDir = path.join(__dirname, 'slides');

    // Create gradient backgrounds
    console.log('Creating gradient backgrounds...');
    const titleBg = await createGradientBg(path.join(slidesDir, 'title-bg.png'), '0F172A', '1E3A5F');
    const slideBg = await createGradientBg(path.join(slidesDir, 'slide-bg.png'), '0F172A', '1E293B');

    // Create HTML slides
    console.log('Creating HTML slides...');

    // Slide 1: Title
    const slide1Html = `<!DOCTYPE html>
<html><head><style>
html { background: #0F172A; }
body { width: 720pt; height: 405pt; margin: 0; padding: 0; font-family: Arial, sans-serif; display: flex; background-image: url('${titleBg}'); background-size: cover; }
.container { width: 100%; display: flex; flex-direction: column; justify-content: center; align-items: center; padding: 40pt; box-sizing: border-box; }
h1 { color: #F8FAFC; font-size: 42pt; margin: 0 0 15pt 0; text-align: center; }
.subtitle { color: #94A3B8; font-size: 22pt; margin: 0 0 30pt 0; text-align: center; }
.tagline { color: #10B981; font-size: 16pt; margin: 0 0 40pt 0; text-align: center; }
.tech-badges { display: flex; gap: 20pt; justify-content: center; }
.badge { background: rgba(59, 130, 246, 0.2); border: 2pt solid #3B82F6; border-radius: 8pt; padding: 8pt 16pt; }
.badge p { color: #60A5FA; font-size: 12pt; margin: 0; }
</style></head>
<body>
<div class="container">
    <h1>O'Reilly AI Agents MVP</h1>
    <p class="subtitle">Issue Triage + Implementation Draft Pipeline</p>
    <p class="tagline">A production-ready demo of AI agent orchestration</p>
    <div class="tech-badges">
        <div class="badge"><p>LangGraph</p></div>
        <div class="badge"><p>CrewAI</p></div>
        <div class="badge"><p>MCP</p></div>
    </div>
</div>
</body></html>`;
    fs.writeFileSync(path.join(slidesDir, 'slide1.html'), slide1Html);

    // Slide 2: Pipeline Architecture (Dataflow Diagram)
    const slide2Html = `<!DOCTYPE html>
<html><head><style>
html { background: #0F172A; }
body { width: 720pt; height: 405pt; margin: 0; padding: 0; font-family: Arial, sans-serif; display: flex; background-image: url('${slideBg}'); background-size: cover; }
.container { width: 100%; padding: 25pt 35pt; box-sizing: border-box; }
h1 { color: #F8FAFC; font-size: 28pt; margin: 0 0 20pt 0; }
.diagram { display: flex; flex-direction: column; gap: 15pt; }
.sources { display: flex; gap: 15pt; justify-content: center; margin-bottom: 10pt; }
.source-box { padding: 10pt 15pt; border-radius: 6pt; text-align: center; }
.github { background: #EF4444; }
.mock { background: #10B981; }
.watcher { background: #3B82F6; }
.source-box p { color: #FFFFFF; font-size: 11pt; margin: 0; }
.arrow-down { text-align: center; }
.arrow-down p { color: #64748B; font-size: 20pt; margin: 0; }
.pipeline { display: flex; align-items: center; justify-content: center; gap: 8pt; }
.node { padding: 12pt 18pt; border-radius: 8pt; text-align: center; min-width: 70pt; }
.load { background: #475569; }
.pm { background: #F59E0B; }
.dev { background: #10B981; }
.qa { background: #8B5CF6; }
.result { background: #3B82F6; }
.node p { color: #FFFFFF; font-size: 11pt; margin: 0; font-weight: bold; }
.arrow { color: #64748B; font-size: 16pt; }
.arrow p { margin: 0; }
.outputs { display: flex; gap: 30pt; justify-content: center; margin-top: 15pt; }
.output-item { text-align: center; }
.output-item p { color: #94A3B8; font-size: 9pt; margin: 2pt 0; }
.output-label { color: #CBD5E1 !important; font-size: 10pt !important; font-weight: bold; }
</style></head>
<body>
<div class="container">
    <h1>Pipeline Architecture</h1>
    <div class="diagram">
        <div class="sources">
            <div class="source-box github"><p>GitHub Issue</p></div>
            <div class="source-box mock"><p>Mock Issue</p></div>
            <div class="source-box watcher"><p>File Watcher</p></div>
        </div>
        <div class="arrow-down"><p>v</p></div>
        <div class="pipeline">
            <div class="node load"><p>Load</p></div>
            <div class="arrow"><p>-></p></div>
            <div class="node pm"><p>PM</p></div>
            <div class="arrow"><p>-></p></div>
            <div class="node dev"><p>Dev</p></div>
            <div class="arrow"><p>-></p></div>
            <div class="node qa"><p>QA</p></div>
            <div class="arrow"><p>-></p></div>
            <div class="node result"><p>Result</p></div>
        </div>
        <div class="outputs">
            <div class="output-item">
                <p class="output-label">PM Output</p>
                <p>Acceptance Criteria</p>
                <p>Implementation Plan</p>
            </div>
            <div class="output-item">
                <p class="output-label">Dev Output</p>
                <p>Code Files</p>
                <p>Tests</p>
            </div>
            <div class="output-item">
                <p class="output-label">QA Output</p>
                <p>Verdict</p>
                <p>Findings</p>
            </div>
            <div class="output-item">
                <p class="output-label">Final</p>
                <p>JSON Result</p>
                <p>SQLite DB</p>
            </div>
        </div>
    </div>
</div>
</body></html>`;
    fs.writeFileSync(path.join(slidesDir, 'slide2.html'), slide2Html);

    // Slide 3: Agent Roles
    const slide3Html = `<!DOCTYPE html>
<html><head><style>
html { background: #0F172A; }
body { width: 720pt; height: 405pt; margin: 0; padding: 0; font-family: Arial, sans-serif; display: flex; background-image: url('${slideBg}'); background-size: cover; }
.container { width: 100%; padding: 25pt 35pt; box-sizing: border-box; }
h1 { color: #F8FAFC; font-size: 28pt; margin: 0 0 20pt 0; }
.agents { display: flex; gap: 20pt; }
.agent-card { flex: 1; background: rgba(30, 41, 59, 0.8); border-radius: 10pt; padding: 18pt; border-top: 4pt solid; }
.pm-card { border-color: #F59E0B; }
.dev-card { border-color: #10B981; }
.qa-card { border-color: #8B5CF6; }
.agent-card h2 { margin: 0 0 8pt 0; font-size: 16pt; }
.pm-card h2 { color: #F59E0B; }
.dev-card h2 { color: #10B981; }
.qa-card h2 { color: #8B5CF6; }
.agent-card p { color: #94A3B8; font-size: 10pt; margin: 0 0 10pt 0; }
.agent-card ul { margin: 0; padding-left: 14pt; }
.agent-card li { color: #CBD5E1; font-size: 9pt; margin: 4pt 0; }
</style></head>
<body>
<div class="container">
    <h1>Agent Responsibilities</h1>
    <div class="agents">
        <div class="agent-card pm-card">
            <h2>PM Agent</h2>
            <p>Product Manager</p>
            <ul>
                <li>Analyzes GitHub issues</li>
                <li>Creates acceptance criteria</li>
                <li>Builds implementation plan</li>
                <li>Documents assumptions</li>
            </ul>
        </div>
        <div class="agent-card dev-card">
            <h2>Dev Agent</h2>
            <p>Senior Developer</p>
            <ul>
                <li>Implements PM's plan</li>
                <li>Drafts code files</li>
                <li>Writes unit tests</li>
                <li>Adds implementation notes</li>
            </ul>
        </div>
        <div class="agent-card qa-card">
            <h2>QA Agent</h2>
            <p>QA Engineer</p>
            <ul>
                <li>Reviews implementation</li>
                <li>Provides pass/fail/needs-human</li>
                <li>Lists specific findings</li>
                <li>Suggests improvements</li>
            </ul>
        </div>
    </div>
</div>
</body></html>`;
    fs.writeFileSync(path.join(slidesDir, 'slide3.html'), slide3Html);

    // Slide 4: Technology Stack
    const slide4Html = `<!DOCTYPE html>
<html><head><style>
html { background: #0F172A; }
body { width: 720pt; height: 405pt; margin: 0; padding: 0; font-family: Arial, sans-serif; display: flex; background-image: url('${slideBg}'); background-size: cover; }
.container { width: 100%; padding: 25pt 35pt; box-sizing: border-box; }
h1 { color: #F8FAFC; font-size: 28pt; margin: 0 0 20pt 0; }
.tech-grid { display: flex; gap: 25pt; }
.tech-col { flex: 1; }
.tech-box { background: rgba(30, 41, 59, 0.8); border-radius: 10pt; padding: 15pt; margin-bottom: 15pt; border-left: 4pt solid #3B82F6; }
.tech-box h2 { color: #60A5FA; font-size: 14pt; margin: 0 0 8pt 0; }
.tech-box p { color: #94A3B8; font-size: 10pt; margin: 0 0 8pt 0; }
.tech-box ul { margin: 0; padding-left: 14pt; }
.tech-box li { color: #CBD5E1; font-size: 9pt; margin: 3pt 0; }
.highlight { border-color: #10B981 !important; }
.highlight h2 { color: #34D399 !important; }
</style></head>
<body>
<div class="container">
    <h1>Technology Stack</h1>
    <div class="tech-grid">
        <div class="tech-col">
            <div class="tech-box">
                <h2>LangGraph</h2>
                <p>Stateful orchestration framework</p>
                <ul>
                    <li>TypedDict state management</li>
                    <li>Explicit node-to-node edges</li>
                    <li>Production-ready checkpointing</li>
                    <li>Built-in error handling</li>
                </ul>
            </div>
            <div class="tech-box highlight">
                <h2>CrewAI</h2>
                <p>Multi-agent role definitions</p>
                <ul>
                    <li>Role/goal/backstory pattern</li>
                    <li>High-level abstractions</li>
                    <li>Rapid prototyping</li>
                    <li>Extensible with tools</li>
                </ul>
            </div>
        </div>
        <div class="tech-col">
            <div class="tech-box">
                <h2>Model Context Protocol</h2>
                <p>Standard tool/resource protocol</p>
                <ul>
                    <li>Claude Desktop integration</li>
                    <li>VS Code Copilot support</li>
                    <li>GitHub issue fetching</li>
                    <li>Portable across clients</li>
                </ul>
            </div>
            <div class="tech-box">
                <h2>Data & Persistence</h2>
                <p>Pydantic + SQLite</p>
                <ul>
                    <li>Strict data contracts</li>
                    <li>Token usage tracking</li>
                    <li>Run history in SQLite</li>
                    <li>JSON result files</li>
                </ul>
            </div>
        </div>
    </div>
</div>
</body></html>`;
    fs.writeFileSync(path.join(slidesDir, 'slide4.html'), slide4Html);

    // Slide 5: Key Features
    const slide5Html = `<!DOCTYPE html>
<html><head><style>
html { background: #0F172A; }
body { width: 720pt; height: 405pt; margin: 0; padding: 0; font-family: Arial, sans-serif; display: flex; background-image: url('${slideBg}'); background-size: cover; }
.container { width: 100%; padding: 25pt 35pt; box-sizing: border-box; }
h1 { color: #F8FAFC; font-size: 28pt; margin: 0 0 18pt 0; }
.features { display: flex; flex-wrap: wrap; gap: 12pt; }
.feature { width: 48%; background: rgba(30, 41, 59, 0.7); border-radius: 8pt; padding: 12pt 15pt; display: flex; align-items: flex-start; gap: 10pt; }
.icon { width: 28pt; height: 28pt; background: #3B82F6; border-radius: 6pt; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.icon p { color: #FFFFFF; font-size: 14pt; margin: 0; }
.feature-text h3 { color: #F8FAFC; font-size: 12pt; margin: 0 0 4pt 0; }
.feature-text p { color: #94A3B8; font-size: 9pt; margin: 0; }
</style></head>
<body>
<div class="container">
    <h1>Key Features</h1>
    <div class="features">
        <div class="feature">
            <div class="icon"><p>1</p></div>
            <div class="feature-text">
                <h3>Multi-Provider LLM Support</h3>
                <p>Anthropic, OpenAI, Azure, DeepSeek via LangChain</p>
            </div>
        </div>
        <div class="feature">
            <div class="icon"><p>2</p></div>
            <div class="feature-text">
                <h3>Token Tracking & Cost Awareness</h3>
                <p>Per-agent usage stats with estimated USD costs</p>
            </div>
        </div>
        <div class="feature">
            <div class="icon"><p>3</p></div>
            <div class="feature-text">
                <h3>Interactive CLI Menu</h3>
                <p>Easy launch: GitHub, mock issues, or file watcher</p>
            </div>
        </div>
        <div class="feature">
            <div class="icon"><p>4</p></div>
            <div class="feature-text">
                <h3>MCP Server Built-in</h3>
                <p>Expose pipeline as tools for Claude & VS Code</p>
            </div>
        </div>
        <div class="feature">
            <div class="icon"><p>5</p></div>
            <div class="feature-text">
                <h3>Event-Driven Processing</h3>
                <p>Folder watcher auto-processes incoming issues</p>
            </div>
        </div>
        <div class="feature">
            <div class="icon"><p>6</p></div>
            <div class="feature-text">
                <h3>SQLite Persistence</h3>
                <p>Full run history with queryable metadata</p>
            </div>
        </div>
    </div>
</div>
</body></html>`;
    fs.writeFileSync(path.join(slidesDir, 'slide5.html'), slide5Html);

    // Slide 6: Getting Started
    const slide6Html = `<!DOCTYPE html>
<html><head><style>
html { background: #0F172A; }
body { width: 720pt; height: 405pt; margin: 0; padding: 0; font-family: Arial, sans-serif; display: flex; background-image: url('${slideBg}'); background-size: cover; }
.container { width: 100%; padding: 25pt 35pt; box-sizing: border-box; }
h1 { color: #F8FAFC; font-size: 28pt; margin: 0 0 18pt 0; }
.content { display: flex; gap: 30pt; }
.steps { flex: 1; }
.step { display: flex; gap: 12pt; margin-bottom: 15pt; }
.step-num { width: 24pt; height: 24pt; background: #3B82F6; border-radius: 50%; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.step-num p { color: #FFFFFF; font-size: 12pt; margin: 0; font-weight: bold; }
.step-text h3 { color: #F8FAFC; font-size: 12pt; margin: 0 0 3pt 0; }
.step-text p { color: #94A3B8; font-size: 9pt; margin: 0; }
.code-box { flex: 1; background: #1E293B; border-radius: 8pt; padding: 15pt; border: 1pt solid #334155; }
.code-box h3 { color: #10B981; font-size: 11pt; margin: 0 0 10pt 0; }
.code-box p { color: #E2E8F0; font-size: 9pt; margin: 4pt 0; font-family: Courier New, monospace; }
.code-box .comment { color: #64748B; }
</style></head>
<body>
<div class="container">
    <h1>Getting Started</h1>
    <div class="content">
        <div class="steps">
            <div class="step">
                <div class="step-num"><p>1</p></div>
                <div class="step-text">
                    <h3>Clone & Setup</h3>
                    <p>Run setup script to create venv</p>
                </div>
            </div>
            <div class="step">
                <div class="step-num"><p>2</p></div>
                <div class="step-text">
                    <h3>Configure Environment</h3>
                    <p>Copy .env.example, add API keys</p>
                </div>
            </div>
            <div class="step">
                <div class="step-num"><p>3</p></div>
                <div class="step-text">
                    <h3>Launch Interactive Menu</h3>
                    <p>Run agent-menu or launch.ps1</p>
                </div>
            </div>
            <div class="step">
                <div class="step-num"><p>4</p></div>
                <div class="step-text">
                    <h3>Process an Issue</h3>
                    <p>Select GitHub, mock, or watcher mode</p>
                </div>
            </div>
        </div>
        <div class="code-box">
            <h3>Quick Commands</h3>
            <p class="comment"># Setup</p>
            <p>./scripts/setup.ps1</p>
            <p class="comment"># Interactive menu</p>
            <p>agent-menu</p>
            <p class="comment"># Direct run</p>
            <p>python -m agent_mvp.pipeline.run_once</p>
            <p class="comment"># MCP server</p>
            <p>agent-mcp</p>
        </div>
    </div>
</div>
</body></html>`;
    fs.writeFileSync(path.join(slidesDir, 'slide6.html'), slide6Html);

    // Create presentation
    console.log('Building PowerPoint presentation...');
    const pptx = new pptxgen();
    pptx.layout = 'LAYOUT_16x9';
    pptx.title = "O'Reilly AI Agents MVP";
    pptx.author = 'Tim Warner';
    pptx.subject = 'AI Agent Orchestration Demo';

    // Process each slide
    const slideFiles = ['slide1.html', 'slide2.html', 'slide3.html', 'slide4.html', 'slide5.html', 'slide6.html'];

    for (const slideFile of slideFiles) {
        console.log(`Processing ${slideFile}...`);
        await html2pptx(path.join(slidesDir, slideFile), pptx, { tmpDir: slidesDir });
    }

    // Save
    const outputPath = path.join(__dirname, 'oreilly-agent-mvp-overview.pptx');
    await pptx.writeFile({ fileName: outputPath });
    console.log(`\nPresentation saved to: ${outputPath}`);
}

createPresentation().catch(err => {
    console.error('Error:', err);
    process.exit(1);
});
