# Impact Assessment Workflow -- Step-by-Step Guide

This guide builds the **RAI Impact Assessment** flow and attaches it to the **RAI Advisor** agent so the agent can collect a system description, generate a governance document, save it to SharePoint, and return a share link. It is the repeatable workflow for the agent.

**Time:** about 20 minutes. **Prerequisites:** Copilot Studio access, Power Automate Premium, a SharePoint site you can write to, and the RAI Advisor agent already imported (the `RAI Advisor/` `.mcs.yml` files).

The agent's `T02_ImpactAssessment` topic currently generates the assessment **inline** as a placeholder. After this guide, you swap that placeholder for the real flow so the document lands in SharePoint.

---

## Part 1 -- Prepare the SharePoint destination

1. Open your governance SharePoint site in the browser.
2. Click **Documents** in the left nav.
3. Click **+ New**, then **Folder**.
4. In the name box, **type:** `RAI Impact Assessments`
5. Click **Create**. Leave this tab open; you will need the **Site Address** URL in Part 2.

---

## Part 2 -- Build the flow

1. Go to **<https://make.powerautomate.com>** and confirm you are in the **same environment** as your RAI Advisor agent (top-right environment picker).
2. In the left nav, click **Create**.
3. Click **Start from Copilot** (the "Describe it to build it" tile).
4. Open `impact-assessment-flow-bootstrap-prompt.md`, copy the entire prompt block, and **paste it** into the Copilot box. Press **Enter**.
5. When the flow outline appears, review the trigger and the three actions, then click **Next** and **Create flow**.
6. The designer opens. Fix up each action:
   - **Trigger:** confirm the four text inputs exist and are named exactly `SystemName`, `SystemDescription`, `IntendedUse`, `Owner`. If any is missing, click the trigger, then **+ Add an input**, choose **Text**, and type the name.
   - **Create file (SharePoint):** click the action. In **Site Address**, select your governance site. In **Folder Path**, click the folder icon and pick `/Shared Documents/RAI Impact Assessments`. Confirm **File Name** and **File Content** are wired to the dynamic values from the Compose step.
   - **Create sharing link:** confirm **Site Address** matches and the **File Identifier** is the **Id** output of the Create file action. Set **Link Type** to **View** and **Scope** to **Organization**.
7. Click the trigger again and confirm the flow's **outputs** (Respond to Copilot) return `AssessmentLink` and `FileName`.
8. Top-right, click **Save**.
9. Click **Test**, choose **Manually**, and supply sample values (for example, SystemName `Contoso Returns Bot`). Confirm a file appears in the SharePoint folder and the run returns a link. Fix any red steps before continuing.

---

## Part 3 -- Attach the flow to the RAI Advisor agent

1. Go to **<https://copilotstudio.microsoft.com>**, open the **RAI Advisor** agent.
2. Click the **Actions** tab (or **Tools**, depending on your tenant's label), then **+ Add an action**.
3. Choose **Flow**, then select **RAI Impact Assessment Generator**. Click **Add** and **Finish**. Copilot Studio creates the connection reference automatically.
4. Open the **T02_ImpactAssessment** topic (Topics tab).
5. Locate the placeholder node labeled **answerAi_assessment** (the inline `Generate answer` node that builds the assessment). Click the **...** menu on that node, then **Delete**.
6. In its place, click **+**, choose **Call an action**, and select **RAI Impact Assessment Generator**.
7. Map the inputs:
   - `SystemName` -> **type:** `Topic.SystemName`
   - `SystemDescription` -> **type:** `Topic.SystemDescription`
   - `IntendedUse` -> **type:** `Topic.IntendedUse`
   - `Owner` -> **type:** `System.User.DisplayName` (or a fixed reviewer name)
8. After the action node, edit the **Message** node so it returns the link. In the message text, **type:**
   `Your Responsible AI Impact Assessment is ready: {Topic.AssessmentLink}`
   (bind `Topic.AssessmentLink` to the flow's `AssessmentLink` output.)
9. Add a **Condition** right after the action for the fallback: condition **type:** `=IsBlank(Topic.AssessmentLink)`. In the **true** branch, send the inline assessment text so the agent degrades gracefully if SharePoint is unavailable.
10. Click **Save** on the topic.

---

## Part 4 -- Sync the connection reference into source (optional, for the repo)

When you exported or authored the agent in VS Code, `RAI Advisor/connectionreferences.mcs.yml` shipped as an empty `connectionReferences: []` shell. After attaching the flow:

1. In the Copilot Studio VS Code extension, **pull** the latest agent components, OR
2. Re-export the solution and copy the populated `connectionReferences` entry (it will carry a logical name like `cr84c_raiAdvisor.shared_...`) into `connectionreferences.mcs.yml`.

This keeps the repo's `.mcs.yml` in sync with the live agent. It is not required for the live demo, only for clean source control.

---

## Part 5 -- Test end to end

1. In Copilot Studio, open the **Test** pane.
2. **Type:** `run an impact assessment`
3. Answer the three prompts (name, description, intended use).
4. Confirm the agent returns a **SharePoint link**, and that opening the link shows the generated assessment with the six-principle table and the **17-goal** checklist.
5. To test the fallback, temporarily turn off the SharePoint connection and confirm the agent shows the assessment **inline** instead of erroring.

---

## Troubleshooting

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| Action not selectable in the topic | Flow not in the same environment as the agent | Rebuild the flow in the agent's environment |
| Agent returns a blank link | Create file or sharing-link step failed | Open the flow run history; check Site Address and folder path |
| Assessment text looks truncated | Model token limit on a long description | Shorten the description, or split section 4 into its own action |
| Answer silently disappears in Test | Content moderation blocked it | Lower the agent's moderation level; moderation events are only visible via Application Insights KQL (no user-facing message) |

**Sources:** Agent flows <https://learn.microsoft.com/microsoft-copilot-studio/flows-overview> | Add actions <https://learn.microsoft.com/microsoft-copilot-studio/advanced-plugin-actions> | Impact Assessment template <https://aka.ms/RAIImpactAssessmentTemplatePDF>
