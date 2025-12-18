# Quick-Start: Triggers and Flows for Employee Onboarding Agent

**What this guide does:** Walk you through 4 core triggers/flows, one step at a time.

**Time needed:** 30-45 minutes total (do one section at a time if needed)

**Prerequisite:** You have access to [copilotstudio.microsoft.com](https://copilotstudio.microsoft.com)

---

## How to Use This Guide

- Each step = ONE action
- Check the box when done
- Bold words = key terms explained on first use
- `Code formatting` = exact button/field names in the UI
- Take breaks between sections

---

## Section 1: Authentication Trigger (Require Sign-In)

**What you are building:** Force users to sign in before chatting with your agent.

**Why this matters:** You need to know WHO is asking questions to personalize responses.

**Time:** 5-10 minutes

---

### Steps

- [ ] **Step 1.** Open your browser. Go to [copilotstudio.microsoft.com](https://copilotstudio.microsoft.com)

- [ ] **Step 2.** Find your Employee Onboarding Agent in the list. Click to open it.

- [ ] **Step 3.** Look at the top-right of the screen. Click `Settings` (gear icon).

- [ ] **Step 4.** In the left sidebar, click `Security`.

- [ ] **Step 5.** Click `Authentication`.

- [ ] **Step 6.** You will see authentication options. Select `Authenticate manually`.

- [ ] **Step 7.** Find the checkbox labeled `Require users to sign in`. Check it.

- [ ] **Step 8.** Fill in the required fields:
  - **Service provider:** Select `Microsoft Entra ID`
  - **Client ID:** Your app registration ID (ask your admin if you do not have this)
  - **Scopes:** Type `User.Read profile openid`

- [ ] **Step 9.** Click `Save` at the bottom.

---

### Done! What You Built

Your agent now requires sign-in. When someone starts a conversation, they must authenticate first.

**Variables now available in your topics:**
| Variable | What it contains |
|----------|------------------|
| `User.DisplayName` | The person's name |
| `User.Id` | Unique user ID |
| `User.IsLoggedIn` | True or False |

---

## Section 2: Day 1 Checklist Topic Trigger

**What you are building:** A topic that starts when someone says "day 1 checklist" or similar.

**Why this matters:** New hires need a personalized first-day plan.

**Time:** 10 minutes

---

### Steps

- [ ] **Step 1.** In your agent, click `Topics` in the left sidebar.

- [ ] **Step 2.** Click `+ Add a topic` at the top.

- [ ] **Step 3.** Select `From blank`.

- [ ] **Step 4.** A new topic opens. You see a **Trigger** node at the top.

- [ ] **Step 5.** Click the `...` (three dots) on the Trigger node. Select `Properties`.

- [ ] **Step 6.** Find the `Phrases` section. This is where you add **trigger phrases** (words that start this topic).

- [ ] **Step 7.** Add these phrases (one per line). Click the `+` icon after each:
  ```
  day 1 checklist
  what do I do on my first day
  first day onboarding
  getting started
  new hire checklist
  start onboarding
  what should I do first
  onboarding steps
  ```

- [ ] **Step 8.** Click `Details` in the toolbar at the top.

- [ ] **Step 9.** Set the topic name to: `Day 1 Checklist`

  > **Warning:** Do NOT put a period in the topic name. Periods break exports.

- [ ] **Step 10.** Click `Save` in the top-right.

---

### Done! What You Built

You created a topic that activates when users say things like "day 1 checklist" or "getting started."

**What happens next:** Add Question nodes and a Generative Answers node to collect info and generate a plan. (See the full build guide in `topics/T01_Day1Checklist/topic.build.md`)

---

## Section 3: Request Access Flow (Power Automate Call)

**What you are building:** A topic that calls Power Automate to create an IT ticket.

**Why this matters:** Automating ticket creation saves HR and IT time.

**Time:** 15 minutes (split into 2 parts)

---

### Part A: Create the Topic

- [ ] **Step 1.** Click `Topics` in the left sidebar.

- [ ] **Step 2.** Click `+ Add a topic` then `From blank`.

- [ ] **Step 3.** Click `...` on the Trigger node. Select `Properties`.

- [ ] **Step 4.** Add these trigger phrases:
  ```
  I need access
  request access to an app
  need permissions
  can't log in
  access request
  I need VPN
  I need github access
  need microsoft 365 access
  ```

- [ ] **Step 5.** Click `Details`. Name it: `Request Access`

- [ ] **Step 6.** Click `Save`.

---

### Part B: Add the Flow Action

- [ ] **Step 7.** Below the Trigger node, click the `+` icon to add a node.

- [ ] **Step 8.** Select `Add a tool`.

- [ ] **Step 9.** Click the `Basic tools` tab.

- [ ] **Step 10.** Click `New Agent flow`. A new browser tab opens with Power Automate.

- [ ] **Step 11.** You see a flow with two nodes:
  - `When an agent calls the flow` (trigger)
  - `Respond to the agent` (output)

- [ ] **Step 12.** Click `When an agent calls the flow`. Add input parameters:
  | Name | Type |
  |------|------|
  | system | Text |
  | reason | Text |
  | manager | Text |

- [ ] **Step 13.** Between the two nodes, click `+` then `Add an action`.

- [ ] **Step 14.** Search for `Create a row` (Dataverse) or `Create item` (SharePoint). Add it.

- [ ] **Step 15.** Configure the action to save the access request data.

- [ ] **Step 16.** Click `Respond to the agent`. Add output:
  | Name | Type |
  |------|------|
  | ticketId | Text |

- [ ] **Step 17.** Click `Publish` in the top-right of Power Automate.

- [ ] **Step 18.** Click `Go back to agent` (link at top).

- [ ] **Step 19.** Back in Copilot Studio, click `Save`.

---

### Done! What You Built

You created a **Tool** node (previously called **Action** node) that calls a Power Automate flow.

**Key concept:** The flow uses the trigger `When an agent calls the flow` and must include `Respond to the agent` to return data.

---

## Section 4: Benefits FAQ with Knowledge Grounding

**What you are building:** A topic that answers benefits questions using your uploaded documents.

**Why this matters:** Grounded answers = accurate answers from YOUR data, not general AI knowledge.

**Time:** 10 minutes

---

### Steps

- [ ] **Step 1.** Click `Topics` in the left sidebar.

- [ ] **Step 2.** Click `+ Add a topic` then `From blank`.

- [ ] **Step 3.** Click `...` on the Trigger node. Select `Properties`.

- [ ] **Step 4.** Add these trigger phrases:
  ```
  benefits
  health insurance
  when do benefits start
  401k
  PTO
  vacation policy
  open enrollment
  dental and vision
  ```

- [ ] **Step 5.** Click `Details`. Name it: `Benefits FAQ`

- [ ] **Step 6.** Click `Save`.

---

### Add the Generative Answers Node

- [ ] **Step 7.** Below the Trigger, click `+` to add a node.

- [ ] **Step 8.** Select `Advanced`.

- [ ] **Step 9.** Select `Generative answers`.

- [ ] **Step 10.** The **Create generative answers** node appears.

- [ ] **Step 11.** Click `Edit` under `Data sources`.

- [ ] **Step 12.** You see knowledge source options. Your uploaded files should appear here.
  - If not, go to `Knowledge` in the left sidebar and upload your benefits documents first.

- [ ] **Step 13.** Select the knowledge sources you want to use:
  - `benefits-faq.yaml`
  - `Benefits-Overview.pdf`
  - `Health-Plans-Comparison.xlsx`
  - `401k-Guide.pdf`

- [ ] **Step 14.** Click `Save` on the data sources panel.

- [ ] **Step 15.** Click `Save` for the topic.

---

### Done! What You Built

You created a topic that uses **Generative answers** grounded in your uploaded knowledge files.

**Key concept:** The agent will ONLY use information from your documents to answer. This prevents hallucinations and ensures accuracy.

---

## Quick Reference: Node Types

| Node Type | When to Use | Icon/Location |
|-----------|-------------|---------------|
| **Message** | Send text to user | `+` > `Send a message` |
| **Question** | Ask user for input | `+` > `Ask a question` |
| **Condition** | Branch logic (if/else) | `+` > `Add a condition` |
| **Tool** | Call Power Automate | `+` > `Add a tool` |
| **Generative answers** | AI answers from knowledge | `+` > `Advanced` > `Generative answers` |

---

## Quick Reference: Variable Naming

| Scope | Prefix | Example | Persists |
|-------|--------|---------|----------|
| Topic | `Topic.` | `Topic.UserQuestion` | Only in this topic |
| Global | `Global.` | `Global.EmployeeName` | Across all topics |
| User (auth) | `User.` | `User.DisplayName` | From sign-in |

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Topic does not trigger | Add more phrase variations (aim for 8+) |
| Flow times out | Keep flow under 100 seconds |
| Auth variables empty | Check `Require users to sign in` is enabled |
| Generative answers wrong | Verify correct knowledge sources are selected |
| Export fails | Remove periods from topic names |

---

## Next Steps

1. Test each topic in the `Test` panel (bottom-right of Copilot Studio)
2. Review the full build guides in each `topics/T0X_*/topic.build.md` file
3. Add more topics as needed

---

## Documentation Links

- [Create and Edit Topics](https://learn.microsoft.com/en-us/microsoft-copilot-studio/authoring-create-edit-topics)
- [End-User Authentication](https://learn.microsoft.com/en-us/microsoft-copilot-studio/advanced-end-user-authentication)
- [Create Agent Flows](https://learn.microsoft.com/en-us/microsoft-copilot-studio/advanced-flow-create)
- [Generative Answers with Custom Data](https://learn.microsoft.com/en-us/microsoft-copilot-studio/nlu-generative-answers-custom-data)

---

*Last updated: December 2025 | Verified against Copilot Studio current UI*
