# Course Plan

## Segment 1 - Using AI Agents (60 Minutes)

### Opening Hook: Agent in Action (10 min)
- **DEMO: Claude Code Subagents**
  - Show Claude Code orchestrating multiple subagents to complete a complex task
  - Highlight: autonomous decision-making, tool selection, multi-step reasoning
  - Key takeaway: "This is what agent orchestration looks like under the hood"

### M365 Copilot Chat Agents Tour (10 min)
- Open Microsoft 365 Copilot and @mention a published agent
- Show how agents extend Copilot with:
  - Specialized vocabulary and domain knowledge
  - Custom tools (REST API connections)
  - SharePoint and Graph connector knowledge sources
- Demonstrate: agent sidebar selection, conversation handoff, suggested prompts
- Reference: [Extend Microsoft 365 Copilot](https://learn.microsoft.com/en-us/microsoft-copilot-studio/copilot-conversational-plugins)

### Copilot Studio Introduction (25 min)
- **What it is**: Graphical, low-code tool for building AI agents without data scientists or developers
- **Live walkthrough of the Studio interface** - highlight these four pillars:

**1. Generative Orchestration** (the brain)
  - Default for new agents - AI autonomously selects best combination of topics, tools, and knowledge
  - Selection based on descriptions, not just trigger phrases
  - Can chain multiple topics/tools in sequence for multi-intent queries
  - Reference: [Generative orchestration](https://learn.microsoft.com/en-us/microsoft-copilot-studio/advanced-generative-actions)

**2. Topics** (conversation building blocks)
  - Represent portions of conversational threads
  - Visual editor with connected nodes and conditional logic
  - AI-assisted creation from plain language descriptions
  - TIP: In generative mode, write clear purpose descriptions - they drive selection

**3. Knowledge Sources** (the data layer)
  - SharePoint sites (respects user permissions)
  - Graph connectors (admin-configured enterprise data)
  - Public websites
  - Uploaded files
  - Auto-generates responses from linked sources

**4. Channels** (deployment targets)
  - Microsoft Teams (internal agents)
  - Websites and mobile apps
  - Microsoft 365 Copilot (via @mention)
  - Facebook and Azure Bot Service channels

- Reference: [What is Copilot Studio](https://learn.microsoft.com/en-us/microsoft-copilot-studio/fundamentals-what-is-copilot-studio)

### Azure AI Foundry Context (2 min)
- Brief mention only - no hands-on in this course
- Position as: "Where you go for custom model fine-tuning, prompt flow orchestration, and enterprise AI governance"
- Copilot Studio is the fast path; Foundry is the custom path
- Learners who need deeper customization can explore post-course

### Environment Readiness Check (3 min)
- Confirm Copilot Studio access for all participants
- Verify sample data availability (SharePoint sites, documents)
- Check Teams deployment targets are accessible
- Assign learners to solution tracks for the three builds

### Q&A and Break (10 min)
- 5 min Q&A
- 5 min break

---

## Segment 2 - Customer Service Assistant Build (60 Minutes)

**Agent:** Customer Service Assistant for Contoso Electronics
**Level:** Beginner
**Goal:** Demonstrate knowledge-powered conversations, generative answers, and escalation handling

### Instructor Quick-Reference Outline

| Time | Activity | Key Deliverable |
|------|----------|-----------------|
| 0-10 min | **Setup & Context** | Agent created from natural language description |
| 10-25 min | **Knowledge Configuration** | SharePoint + website sources connected; generative answers enabled |
| 25-40 min | **Topic Authoring** | Returns/Refunds and Order Status topics built with variables |
| 40-50 min | **Live Demo** | Run 4-6 test prompts in simulator; show fallback and escalation |
| 50-55 min | **Publish to Teams** | Agent available in Teams for learner testing |
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
- **Never use periods in topic names** - causes solution export failures
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

## Segment 3 - Employee Onboarding Agent Build (60 Minutes)

**Agent:** Employee Onboarding Agent for Contoso
**Level:** Intermediate
**Goal:** Demonstrate authentication, Power Automate integration, variable-driven personalization, and approval workflows

### Instructor Quick-Reference Outline

| Time | Activity | Key Deliverable |
|------|----------|-----------------|
| 0-10 min | **Auth & Personalization** | Agent requires sign-in; retrieves user profile from Entra ID token |
| 10-25 min | **Day 1 Checklist Topic** | Generative answers create personalized onboarding plan by role/location |
| 25-40 min | **Power Automate Integration** | Request Access topic calls IT ticket flow; Benefits FAQ uses grounded answers |
| 40-50 min | **Live Demo** | Run 4-6 test prompts showing authenticated, personalized flows |
| 50-55 min | **Analytics Preview** | Show session analytics and completion tracking |
| 55-60 min | **Q&A + Break** | Learner exercise: extend workflow with one new action; 5-minute break |

### Demo Prompts: "Flex the Muscles"

Use these prompts to demonstrate the intermediate-level capabilities.

#### Prompt Set A: Personalized Onboarding

| # | Test Prompt | What It Demonstrates |
|---|-------------|---------------------|
| 1 | "What do I do on my first day?" | **Day 1 Checklist topic** triggers; agent asks for role, start date, and location, then generates a personalized Morning/Midday/Afternoon plan using generative answers |
| 2 | "I'm a Junior Software Engineer starting January 5th, working remote" | **Follow-up to prompt 1**; shows variable capture and how generative answers tailor the checklist to role and location |

#### Prompt Set B: Access Requests and Power Automate

| # | Test Prompt | What It Demonstrates |
|---|-------------|---------------------|
| 3 | "I need access to GitHub" | **Request Access topic** triggers; agent collects system, reason, and manager, then generates a structured request summary and (optionally) creates an IT ticket via Power Automate |
| 4 | "I need VPN access for client site work, my manager is jane.smith@contoso.com" | **Complete access request flow**; shows multi-variable capture and action node invocation |

#### Prompt Set C: Knowledge-Grounded Benefits FAQ

| # | Test Prompt | What It Demonstrates |
|---|-------------|---------------------|
| 5 | "When do my benefits start?" | **Benefits FAQ topic** triggers; agent answers from benefits-faq.yaml and hr-policies.md knowledge sources with source attribution |
| 6 | "Do we have a 401k match and how much PTO do I get?" | **Multi-part question**; demonstrates generative answers handling compound questions from HR knowledge base |

### Talking Points (MS Learn Grounded)

**1. Authentication for Personalization**
- Microsoft Entra ID authentication enables personalized experiences
- Configure scopes: `User.Read`, `profile`, `openid`, `email`
- Access user profile via system variables: `System.User.DisplayName`, `System.User.Email`
- "Require users to sign in" ensures only authenticated users interact with the agent
- Reference: [Configure user authentication](https://learn.microsoft.com/en-us/microsoft-copilot-studio/advanced-end-user-authentication)

**2. Variable Management**
- **Topic scope** (`Topic.VarName`): Variables exist only within the current topic
- **Global scope** (`Global.VarName`): Variables persist across topics and conversation turns
- Initialize variables with `init:Topic.VarName` in Question nodes
- Use descriptive names that indicate purpose (e.g., `t_role`, `t_start_date`)
- Reference: [Use variables](https://learn.microsoft.com/en-us/microsoft-copilot-studio/authoring-variables)

**3. Power Automate Integration (Agent Flows)**
- Agent flows allow calling Power Automate directly from topics
- Define inputs (from topic variables) and outputs (returned to topic)
- Common patterns: create tickets, send notifications, query databases, start approvals
- Test flows independently in Power Automate before connecting to topics
- Reference: [Agent flows overview](https://learn.microsoft.com/en-us/microsoft-copilot-studio/flows-overview)

**4. Generative Answers with Multiple Knowledge Sources**
- Onboarding agents benefit from multiple source types: CSV (checklists), Markdown (policies), YAML (FAQs)
- Include specific source instructions in the generative answers node prompt
- Request structured output (bullets, grouped sections) for better readability
- Keep answers concise: specify word limits in instructions (e.g., "under 120 words")
- Reference: [Generative answers node](https://learn.microsoft.com/en-us/microsoft-copilot-studio/nlu-boost-node)

**5. Approval Workflows**
- Use the Approvals connector in Power Automate for benefits enrollment, equipment requests
- "Start and wait for an approval" action pauses the flow until approved/rejected
- Notify employees of approval status via email or Teams message
- Track pending approvals in the agent by storing `ApprovalID` in a global variable
- Reference: [Approvals connector](https://learn.microsoft.com/en-us/connectors/approvals/)

**6. Analytics and Optimization**
- Session analytics show completion rates, drop-off points, and escalation triggers
- Track onboarding progress by storing checklist state in Dataverse or SharePoint
- Use analytics to identify topics that need more training data or clearer flows
- Reference: [Analyze agent performance](https://learn.microsoft.com/en-us/microsoft-copilot-studio/analytics-overview)

### Live Build Checklist

```
[ ] Create agent with authentication enabled (Microsoft Entra ID)
[ ] Configure required scopes: User.Read, profile, openid, email
[ ] Enable "Require users to sign in"
[ ] Build "Day 1 Checklist" topic with role/date/location variables
[ ] Configure generative answers to use onboarding-checklist.csv, hr-policies.md
[ ] Build "Request Access" topic with app/reason/manager capture
[ ] (Optional) Create Power Automate flow: CreateITTicket
[ ] Build "Benefits FAQ" topic with generative answers from benefits knowledge
[ ] Run all 6 demo prompts in Test panel (sign in when prompted)
[ ] Review session analytics dashboard
```

### Learner Exercise (5 minutes)

**Challenge:** Extend the onboarding agent with one new capability. Choose from:

1. **Policy Acknowledgment Topic** - Loop through 3 company policies, capture acknowledgment for each, record timestamps
2. **Team Introduction Topic** - Ask for manager email, query org chart, suggest a "meet the team" calendar invite
3. **Equipment Preference Topic** - Collect laptop type (Standard/Power User/Mac) and office location, call IT provisioning flow

This exercise reinforces the pattern: trigger phrases -> variable capture -> generative/action node -> confirmation message.

---

## Segment 4 - Autonomous Document Processor Build (60 Minutes)

**Agent:** Document Processor Agent for Contoso
**Level:** Advanced
**Goal:** Build a fully autonomous agent that processes documents without user interaction, using event triggers, AI classification, and intelligent routing

**Key Differentiator:** Unlike Segments 2-3 (conversational agents), this agent operates in the background with zero user prompts.

### Instructor Quick-Reference Outline

| Time | Activity | Instructor Focus |
|------|----------|------------------|
| 0:00-0:05 | Concept intro: autonomous vs conversational | Explain event-driven architecture |
| 0:05-0:15 | Demo: Configure SharePoint trigger | Show trigger setup in Copilot Studio |
| 0:15-0:25 | Demo: Connect AI Builder classification | Walk through model selection and confidence thresholds |
| 0:25-0:35 | Demo: Build routing logic and Power Automate flows | Show condition branches for Invoice/Contract/Resume/Exception |
| 0:35-0:45 | Live test: Upload sample documents | Use UPLOADME files from repo |
| 0:45-0:50 | Governance and security discussion | DLP, retention, PII handling |
| 0:50-0:55 | ROI measurement and analytics | Show agent health dashboard |
| 0:55-1:00 | Wrap-up, Q&A, next steps | Assign follow-up exercise |

### Demo Scenarios: Event-Driven Testing

Because autonomous agents are event-driven (not conversational), testing focuses on trigger scenarios and validation.

#### Scenario 1: Invoice Auto-Routing (Happy Path)

**Trigger:** Upload `UPLOADME-Invoice-ACME-2025-0007.pdf` to Incoming Documents library

**Expected Behavior:**
- Agent triggers on file creation
- AI Builder classifies as Invoice with confidence >= 90%
- System extracts: Vendor=ACME Corp, Amount=$4,750.00, Due Date=2025-01-15
- File routes to Finance/AP-Queue
- Teams notification posts to #finance-automation channel
- Dataverse record created in Document Processing Log

**Validation Prompt:**
> "Watch the Teams channel - within 30 seconds you should see an adaptive card with the invoice details. Let's check the Dataverse table to confirm the extraction worked."

#### Scenario 2: Contract with Approval Workflow

**Trigger:** Upload `UPLOADME-Contract-Fabrikam-MSA-2025-12.docx` to Incoming Documents library

**Expected Behavior:**
- Agent triggers on file creation
- AI Builder classifies as Contract with confidence >= 85%
- System detects Value >= $50,000 based on extracted terms
- Approval workflow initiates (routes to Legal-Review queue)
- File copied to secure Contracts library with metadata tags
- Notification sent to #legal-contracts channel

**Validation Prompt:**
> "Contracts over $50K require approval - let's check the Approvals center in Teams to see the pending request. Notice how the agent added metadata columns automatically."

#### Scenario 3: Low Confidence Exception Path

**Trigger:** Upload `UPLOADME-LowConfidence-MessyDoc.txt` to Incoming Documents library

**Expected Behavior:**
- Agent triggers on file creation
- AI Builder returns confidence < 60% (unstructured text file)
- Document routes to ManualReview queue
- File moved to Exceptions folder
- Teams notification posts to #doc-processor-admin with warning flag
- Dataverse log shows ProcessingStatus = "ManualReview"

**Validation Prompt:**
> "This messy text file doesn't match any trained category. Watch how the agent gracefully handles uncertainty - it routes to the QA team instead of making a wrong guess. That's the safety net."

#### Scenario 4: Resume Candidate Creation

**Trigger:** Upload `UPLOADME-Resume-Jordan-Lee.docx` to Incoming Documents library

**Expected Behavior:**
- Agent triggers on file creation
- AI Builder classifies as Resume with confidence >= 80%
- System extracts: CandidateName=Jordan Lee, Skills=[Python, Azure, Power Platform]
- Candidate record created in Dataverse (HRIS Intake table)
- File routes to Resumes folder
- Notification sent to #recruiting channel with quick-action buttons

**Validation Prompt:**
> "The agent extracted skills from the resume automatically. Let's open the Dataverse table and see the structured candidate record - this saves the recruiting team 10 minutes per resume."

#### Scenario 5: Bulk Processing Stress Test

**Trigger:** Upload 5 documents simultaneously (mix of invoices, contracts, resumes)

**Expected Behavior:**
- Agent handles concurrent triggers without failure
- Each document processed independently
- Processing completes within 2 minutes for all 5 documents
- No duplicate records created
- Agent health dashboard shows 5 successful triggers

**Validation Prompt:**
> "Real-world scenarios involve bursts of documents. Let's verify the agent scales - check the analytics dashboard for trigger count and average latency. We're targeting under 30 seconds per document."

#### Scenario 6: Large File Exception

**Trigger:** Upload a 15MB PDF file to Incoming Documents library

**Expected Behavior:**
- Agent triggers on file creation
- Pre-processing check detects file size > 10MB threshold
- Exception path activates before AI Builder call (saves credits)
- File moved to Exceptions folder with status "FileTooLarge"
- Admin notification includes file size and recommended action

**Validation Prompt:**
> "We deliberately set a 10MB limit to avoid burning AI Builder credits on huge files. The agent caught this before processing - that's defensive design. The admin can manually split or compress the file."

### Talking Points (MS Learn Grounded)

**1. Autonomous Agent Architecture**
- Autonomous agents use event triggers (SharePoint, Dataverse, scheduled) instead of user utterances
- No conversational UI required; agent runs entirely in background
- Reference: [Create automated copilots triggered by events](https://learn.microsoft.com/en-us/microsoft-copilot-studio/authoring-triggers)

**2. Event Trigger Types**
- SharePoint: File created, file modified, item created
- Dataverse: Row created, row updated, row deleted
- Scheduled: Time-based triggers for batch processing
- Reference: [Trigger types overview](https://learn.microsoft.com/en-us/microsoft-copilot-studio/authoring-triggers)

**3. AI Builder Integration**
- Document processing models classify and extract structured data
- Pre-built models available for invoices, receipts, business cards
- Custom models trainable with 5+ sample documents per category
- Reference: [AI Builder document processing](https://learn.microsoft.com/en-us/ai-builder/document-processing-model-overview)

**4. Confidence Thresholds and Exception Handling**
- Best practice: Route documents with confidence >= 85% automatically
- Documents with 60-84% confidence get flagged for spot-check
- Below 60% routes to manual review queue
- Always build exception paths for corrupted, oversized, or unclassifiable files

**5. Governance Considerations**
- Data Loss Prevention (DLP) policies apply to autonomous agents
- Audit logging captures all agent actions for compliance
- Sensitive document handling requires encryption at rest
- Reference: [Agent governance best practices](https://learn.microsoft.com/en-us/microsoft-copilot-studio/admin-data-loss-prevention)

**6. Monitoring and ROI**
- Agent health dashboard shows trigger counts, success rates, latency
- Track processing time reduction vs manual baseline
- Measure exception rates to identify training gaps
- Reference: [Monitor copilot analytics](https://learn.microsoft.com/en-us/microsoft-copilot-studio/analytics-improve-agent-health)

### Live Build Checklist

```
[ ] Agent triggers correctly on SharePoint file creation
[ ] AI Builder classification returns expected document types
[ ] Confidence thresholds route correctly (auto vs manual review)
[ ] Power Automate flows execute without errors
[ ] Teams notifications arrive within 60 seconds
[ ] Dataverse logging captures all processing events
[ ] Exception handling gracefully manages edge cases
```

### Hands-On Exercise: Identify Your Automation Targets

**Instructions for Learners (5 minutes):**

1. Think about your organization's document workflows
2. Identify THREE document types that arrive repeatedly (emails, uploads, forms)
3. For each document type, note:
   - Where documents arrive (email, SharePoint, shared drive)
   - What classification is needed (type, urgency, department)
   - Where documents should route (team, system, archive)
   - What metadata should be extracted (dates, amounts, names)

**Debrief:** Ask 2-3 participants to share their automation targets. Highlight patterns (invoices, contracts, and HR documents are universally applicable).

### Resources for Learners

- [Automated copilots triggered by events](https://learn.microsoft.com/en-us/microsoft-copilot-studio/authoring-triggers)
- [AI Builder document processing overview](https://learn.microsoft.com/en-us/ai-builder/document-processing-model-overview)
- [Agent health dashboard](https://learn.microsoft.com/en-us/microsoft-copilot-studio/analytics-improve-agent-health)
- [Power Automate document automation](https://learn.microsoft.com/en-us/power-automate/document-automation/overview)
- [DLP policies for Copilot Studio](https://learn.microsoft.com/en-us/microsoft-copilot-studio/admin-data-loss-prevention)
