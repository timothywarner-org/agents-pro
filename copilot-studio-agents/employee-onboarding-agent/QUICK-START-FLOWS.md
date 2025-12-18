# Quick-Start: Power Automate Flows for Employee Onboarding Agent

**What this guide does:** Build ONE working approval flow, step by step.

**Time needed:** 20-30 minutes

**Your SharePoint site:** `https://timwinfo2.sharepoint.com/sites/CERTSTAR.NET/Shared Documents/employee-onboarding-agent`

---

## How to Use This Guide

- Each checkbox = ONE action
- Complete each step before moving to the next
- **Bold words** = key terms (explained on first use)
- `Code formatting` = exact text to type or click in the UI
- Take breaks whenever you need them

---

## What You Are Building

An **Access Request Approval Flow** that:
1. Receives a request from your Copilot Studio agent
2. Sends an approval to a manager
3. Notifies the employee via Teams

```
Agent Topic --> Power Automate Flow --> Approvals --> Teams Message
```

---

## Before You Start

**Required access:**
- [ ] Power Automate (included with Microsoft 365)
- [ ] Microsoft Teams
- [ ] Copilot Studio agent (Employee Onboarding Agent)

**Connectors used in this flow:**
| Connector | What it does | Auth needed |
|-----------|--------------|-------------|
| **Approvals** | Creates approval requests | Built-in, no setup |
| **Microsoft Teams** | Sends chat messages | Your M365 account |

---

## Part 1: Create the Flow

**Goal:** Create a new flow that your agent can call.

---

### Open Power Automate

- [ ] **Step 1.** Open your browser. Go to [make.powerautomate.com](https://make.powerautomate.com)

- [ ] **Step 2.** Sign in with your Microsoft 365 account.

- [ ] **Step 3.** Look at the left sidebar. Click `My flows`.

---

### Create a New Flow

- [ ] **Step 4.** Click `+ New flow` (top-left area).

- [ ] **Step 5.** Click `Instant cloud flow`.

- [ ] **Step 6.** A dialog appears. In the `Flow name` field, type:
  ```
  Onboard-AccessRequestApproval
  ```

- [ ] **Step 7.** Scroll down in the trigger list. Find and click `When an agent calls the flow (V2)`.

  > **Note:** This is a **Copilot connector** trigger. It allows your Copilot Studio agent to call this flow directly.

- [ ] **Step 8.** Click `Create`.

---

### Done with Part 1

You created a new flow with the correct trigger. The flow canvas now shows one node: `When an agent calls the flow (V2)`.

---

## Part 2: Add Input Parameters

**Goal:** Tell the flow what information to receive from the agent.

---

### Configure the Trigger

- [ ] **Step 9.** Click the trigger node `When an agent calls the flow (V2)` to expand it.

- [ ] **Step 10.** Click `+ Add an input`.

- [ ] **Step 11.** Select `Text`.

- [ ] **Step 12.** In the field that appears, type this name:
  ```
  EmployeeName
  ```

- [ ] **Step 13.** Click `+ Add an input` again.

- [ ] **Step 14.** Select `Text`.

- [ ] **Step 15.** Type this name:
  ```
  SystemRequested
  ```

- [ ] **Step 16.** Click `+ Add an input` again.

- [ ] **Step 17.** Select `Text`.

- [ ] **Step 18.** Type this name:
  ```
  BusinessReason
  ```

- [ ] **Step 19.** Click `+ Add an input` one more time.

- [ ] **Step 20.** Select `Text`.

- [ ] **Step 21.** Type this name:
  ```
  ApproverEmail
  ```

---

### Done with Part 2

Your trigger now has 4 input parameters:
- EmployeeName
- SystemRequested
- BusinessReason
- ApproverEmail

---

## Part 3: Add the Approval Action

**Goal:** Create an approval request that goes to the manager.

---

### Add the Approvals Action

- [ ] **Step 22.** Below the trigger, click `+` (the plus icon).

- [ ] **Step 23.** Click `Add an action`.

- [ ] **Step 24.** In the search box, type:
  ```
  Start and wait for an approval
  ```

- [ ] **Step 25.** Click `Start and wait for an approval` from the **Approvals** connector.

  > **What is the Approvals connector?** A built-in Microsoft 365 connector that creates approval requests. Approvers can respond in Teams, Outlook, or the Approvals app. No extra setup needed.

---

### Configure the Approval

- [ ] **Step 26.** In the `Approval type` dropdown, select:
  ```
  Approve/Reject - First to respond
  ```

- [ ] **Step 27.** Click in the `Title` field. Type:
  ```
  Access Request:
  ```
  (include the space after the colon)

- [ ] **Step 28.** With your cursor still in the `Title` field, look for the lightning bolt icon (Dynamic content). Click it.

- [ ] **Step 29.** A panel opens showing available **dynamic content** (data from previous steps). Click `SystemRequested`.

  > **What is dynamic content?** Values that come from earlier steps in your flow. They appear as blue tags and get replaced with real data when the flow runs.

- [ ] **Step 30.** Your Title field should now show:
  ```
  Access Request: SystemRequested
  ```
  (where SystemRequested appears as a blue tag)

- [ ] **Step 31.** Click in the `Assigned to` field. Click the lightning bolt icon.

- [ ] **Step 32.** Click `ApproverEmail` from the dynamic content panel.

- [ ] **Step 33.** Click in the `Details` field. Type:
  ```
  Employee:
  ```

- [ ] **Step 34.** Click the lightning bolt. Click `EmployeeName`.

- [ ] **Step 35.** Press Enter to make a new line. Type:
  ```
  System:
  ```

- [ ] **Step 36.** Click the lightning bolt. Click `SystemRequested`.

- [ ] **Step 37.** Press Enter. Type:
  ```
  Reason:
  ```

- [ ] **Step 38.** Click the lightning bolt. Click `BusinessReason`.

---

### Done with Part 3

Your approval action is configured. When this step runs, it will:
1. Send an approval request to the manager
2. Wait for them to respond (Approve or Reject)
3. Continue the flow once they respond

---

## Part 4: Add the Teams Notification

**Goal:** Send a Teams message to the employee with the result.

---

### Add the Teams Action

- [ ] **Step 39.** Below the approval action, click `+`.

- [ ] **Step 40.** Click `Add an action`.

- [ ] **Step 41.** In the search box, type:
  ```
  Post message in a chat or channel
  ```

- [ ] **Step 42.** Click `Post message in a chat or channel` from the **Microsoft Teams** connector.

---

### Configure the Teams Message

- [ ] **Step 43.** In the `Post as` dropdown, select:
  ```
  Flow bot
  ```

- [ ] **Step 44.** In the `Post in` dropdown, select:
  ```
  Chat with Flow bot
  ```

- [ ] **Step 45.** Click in the `Recipient` field. Click the lightning bolt.

- [ ] **Step 46.** Scroll down in the dynamic content panel. Under the trigger section, click `EmployeeName`.

  > **Important:** For a real deployment, you would pass the employee's email address instead of their name. For this MVP, we use the name for simplicity.

- [ ] **Step 47.** Click in the `Message` field. Type:
  ```
  Your access request for
  ```

- [ ] **Step 48.** Click the lightning bolt. Click `SystemRequested`.

- [ ] **Step 49.** Continue typing:
  ```
   has been reviewed. Result:
  ```
  (include the spaces)

- [ ] **Step 50.** Click the lightning bolt. Scroll down to find the Approvals section. Click `Outcome`.

  > **What is Outcome?** The result of the approval (Approve or Reject). This comes from the approval action you added earlier.

---

### Done with Part 4

Your Teams notification is configured. It will send a message like:
> "Your access request for GitHub has been reviewed. Result: Approve"

---

## Part 5: Add the Response to Agent

**Goal:** Send data back to your Copilot Studio agent.

---

### Add the Response Action

- [ ] **Step 51.** Below the Teams action, click `+`.

- [ ] **Step 52.** Click `Add an action`.

- [ ] **Step 53.** In the search box, type:
  ```
  Respond to the agent
  ```

- [ ] **Step 54.** Click `Respond to the agent` from the **Copilot** connector.

---

### Configure the Response

- [ ] **Step 55.** Click `+ Add an output`.

- [ ] **Step 56.** Select `Text`.

- [ ] **Step 57.** In the name field, type:
  ```
  ApprovalResult
  ```

- [ ] **Step 58.** Click in the value field. Click the lightning bolt.

- [ ] **Step 59.** Click `Outcome` from the Approvals section.

- [ ] **Step 60.** Click `+ Add an output` again.

- [ ] **Step 61.** Select `Text`.

- [ ] **Step 62.** In the name field, type:
  ```
  ApprovalID
  ```

- [ ] **Step 63.** Click in the value field. Click the lightning bolt.

- [ ] **Step 64.** Click `Approval ID` from the Approvals section.

---

### Done with Part 5

Your flow will now return two values to the agent:
- ApprovalResult (Approve or Reject)
- ApprovalID (unique identifier)

---

## Part 6: Save and Publish

**Goal:** Make the flow available to your agent.

---

### Save the Flow

- [ ] **Step 65.** Click `Save` in the top-right corner.

- [ ] **Step 66.** Wait for the green "Your flow is ready" message.

---

### Test the Flow (Optional but Recommended)

- [ ] **Step 67.** Click `Test` in the top-right corner.

- [ ] **Step 68.** Select `Manually`.

- [ ] **Step 69.** Click `Test`.

- [ ] **Step 70.** Enter test values:
  - EmployeeName: `Test User`
  - SystemRequested: `GitHub`
  - BusinessReason: `Need to review code`
  - ApproverEmail: `your-own-email@domain.com`

- [ ] **Step 71.** Click `Run flow`.

- [ ] **Step 72.** Check your email or Teams for the approval request. Approve it.

- [ ] **Step 73.** Verify the flow completed successfully (green checkmarks on all steps).

---

### Done with Part 6

Your flow is saved and tested. You can now connect it to your Copilot Studio agent.

---

## Part 7: Connect Flow to Agent

**Goal:** Add the flow as a tool in your Request Access topic.

---

### Open Copilot Studio

- [ ] **Step 74.** Open a new browser tab. Go to [copilotstudio.microsoft.com](https://copilotstudio.microsoft.com)

- [ ] **Step 75.** Open your Employee Onboarding Agent.

- [ ] **Step 76.** Click `Topics` in the left sidebar.

- [ ] **Step 77.** Click the `Request Access` topic to open it.

---

### Add the Flow as a Tool

- [ ] **Step 78.** Find the location in your topic where you want to call the flow (after collecting user input).

- [ ] **Step 79.** Click `+` to add a new node.

- [ ] **Step 80.** Click `Add a tool`.

- [ ] **Step 81.** Click the `Flows` tab.

- [ ] **Step 82.** Find `Onboard-AccessRequestApproval` in the list. Click it.

- [ ] **Step 83.** The flow node appears. Map the inputs:
  - EmployeeName: Select `User.DisplayName` or a topic variable
  - SystemRequested: Select `Topic.t_app_or_system`
  - BusinessReason: Select `Topic.t_reason`
  - ApproverEmail: Select `Topic.t_manager`

- [ ] **Step 84.** Click `Save` in the top-right.

---

### Done with Part 7

Your agent can now call the approval flow. When a user requests access, the flow will:
1. Send an approval to their manager
2. Notify them via Teams when approved/rejected
3. Return the result to the conversation

---

## Complete Flow Summary

```
+----------------------------------+
| When an agent calls the flow     |
| Inputs: EmployeeName,            |
|         SystemRequested,         |
|         BusinessReason,          |
|         ApproverEmail            |
+----------------------------------+
              |
              v
+----------------------------------+
| Start and wait for an approval   |
| Type: Approve/Reject             |
| Assigned to: ApproverEmail       |
+----------------------------------+
              |
              v
+----------------------------------+
| Post message in Teams            |
| Recipient: EmployeeName          |
| Message: Result notification     |
+----------------------------------+
              |
              v
+----------------------------------+
| Respond to the agent             |
| Outputs: ApprovalResult,         |
|          ApprovalID              |
+----------------------------------+
```

---

## Troubleshooting

| Problem | Likely Cause | Solution |
|---------|--------------|----------|
| Flow does not appear in Copilot Studio | Flow not published in same environment | Check environment in Power Automate matches Copilot Studio |
| "Connection not configured" error | Missing connector permission | Click the error, sign in to authorize the connector |
| Approval never arrives | Wrong email format | Verify ApproverEmail is a valid email address |
| Teams message not received | Recipient not found | Use email address instead of display name for Recipient |
| Flow times out | Approval takes too long | Approvals connector waits up to 30 days by default |
| Dynamic content panel is empty | Panel not expanded | Click the lightning bolt icon again |
| "Respond to agent" missing | Wrong trigger used | Ensure trigger is `When an agent calls the flow (V2)` |
| Test fails immediately | Missing required inputs | Fill in ALL input fields before clicking Run |

---

## Connector Authentication Notes

| Connector | First-Time Setup |
|-----------|------------------|
| **Approvals** | No setup required. Works automatically with your M365 account. |
| **Microsoft Teams** | Click `Sign in` when prompted. Use your M365 account. |
| **Copilot** | Automatic. No separate sign-in needed. |

---

## SharePoint Integration (Future Enhancement)

To log requests to SharePoint at `https://timwinfo2.sharepoint.com/sites/CERTSTAR.NET/Shared Documents/employee-onboarding-agent`:

1. Add a `Create item` action (SharePoint connector)
2. Site: `https://timwinfo2.sharepoint.com/sites/CERTSTAR.NET`
3. Library: `Shared Documents/employee-onboarding-agent`
4. Create columns for: EmployeeName, SystemRequested, ApprovalResult, Timestamp

This is not included in the MVP flow above to keep it simple.

---

## Next Steps

After completing this flow:

1. **Test end-to-end:** Chat with your agent, request access, verify approval arrives
2. **Add error handling:** Use `Configure run after` to handle approval failures
3. **Add email notifications:** Include Outlook connector for email backup
4. **Log to SharePoint:** Track all requests for compliance

---

## Documentation Links

- [Approvals Connector Reference](https://learn.microsoft.com/en-us/connectors/approvals/)
- [Microsoft Teams Connector Reference](https://learn.microsoft.com/en-us/connectors/teams/)
- [Create Agent Flows](https://learn.microsoft.com/en-us/microsoft-copilot-studio/advanced-flow-create)
- [Power Automate Dynamic Content](https://learn.microsoft.com/en-us/power-automate/use-expressions-in-conditions)

---

*Last updated: December 2025*
