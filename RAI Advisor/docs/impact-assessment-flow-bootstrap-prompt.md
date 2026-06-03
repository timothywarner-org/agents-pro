# Impact Assessment Flow -- Bootstrap Prompt

Paste the prompt below into **Copilot Studio's "Describe it to build it"** flow box (or into Power Automate's Copilot designer) to generate the **RAI Impact Assessment** flow that the RAI Advisor agent calls. After it generates, follow `impact-assessment-workflow-guide.md` to wire it to the agent.

This flow is the repeatable workflow attached to the agent. It mirrors the proven "lab to SharePoint" pattern from the CKA Exam Prep Assistant: the agent collects inputs, the flow composes a structured governance document, saves it to SharePoint, and returns a share link.

---

## The bootstrap prompt (copy everything in the box)

```text
Build an automated cloud flow named "RAI Impact Assessment Generator".

TRIGGER
- Trigger: "Run a flow from Copilot" (the agent flow / "When an agent calls the flow" trigger).
- Input parameters (all text, all required):
  1. SystemName
  2. SystemDescription
  3. IntendedUse
  4. Owner

STEPS
1. Compose an action named "BuildAssessmentMarkdown" that produces a Markdown document with this exact structure, substituting the four inputs:

   # Responsible AI Impact Assessment: {SystemName}
   Owner: {Owner}
   Date: (use the flow's utcNow() formatted as yyyy-MM-dd)

   ## 1. System Overview
   {SystemDescription}

   ## 2. Intended Use and Out-of-Scope Uses
   {IntendedUse}

   ## 3. Assessment by Microsoft Responsible AI Principles
   A Markdown table with columns: Principle | Key Questions | Risk Level (Low/Medium/High) | Notes.
   Rows, in this order: Fairness; Reliability and Safety; Privacy and Security; Inclusiveness; Transparency; Accountability.
   Leave Risk Level and Notes as fill-in placeholders for the reviewer.

   ## 4. Mapping to the Responsible AI Standard v2 (17 goals)
   A checklist grouped by area, one checkbox line per goal:
   Accountability: A1 Impact assessment; A2 Oversight of significant adverse impacts; A3 Fit for purpose; A4 Data governance and management; A5 Human oversight and control.
   Transparency: T1 System intelligibility for decision making; T2 Communication to stakeholders; T3 Disclosure of AI interaction.
   Fairness: F1 Quality of service; F2 Allocation of resources and opportunities; F3 Minimization of stereotyping, demeaning, and erasing outputs.
   Reliability and Safety: RS1 Reliability and safety guidance; RS2 Failures and remediations; RS3 Ongoing monitoring, feedback, and evaluation.
   Privacy and Security: PS1 Privacy Standard compliance; PS2 Security Policy compliance.
   Inclusiveness: I1 Accessibility Standards compliance.
   (That is 17 goals total. Do not write 14.)

   ## 5. Risks and Mitigations
   A Markdown table with columns: Risk | Affected Principle | Likelihood | Impact | Mitigation | Owner.
   Seed it with one example row, then leave blank rows for the reviewer.

   ## 6. Human Oversight and Control
   Document who reviews outputs, how users correct or override the system, and the escalation path.

   ## 7. Review and Approval
   Reviewers, approval date, and the re-review schedule (at least annually, on any new intended use, and before each release stage).

   ## Sources
   - Microsoft Responsible AI hub (entry point to the Standard): https://aka.ms/RAI
   - Impact Assessment template: https://aka.ms/RAIImpactAssessmentTemplatePDF
   - Microsoft Responsible AI principles: https://www.microsoft.com/ai/principles-and-approach

2. A "Create file" action (SharePoint connector):
   - Site Address: the governance SharePoint site (a flow parameter or hard-coded for the demo).
   - Folder Path: /Shared Documents/RAI Impact Assessments
   - File Name: concat(SystemName, '-RAI-Impact-Assessment-', formatDateTime(utcNow(),'yyyyMMdd'), '.md')
   - File Content: the output of BuildAssessmentMarkdown.

3. A "Create sharing link for a file or folder" action (SharePoint) to produce a view link for the created file.

OUTPUT (return to the agent)
- AssessmentLink: the sharing link from step 3.
- FileName: the file name from step 2.

Add a Configure-run-after / error path: if "Create file" fails, return AssessmentLink = "" and FileName = "" so the agent can fall back to showing the assessment inline.
```

---

## Notes

- **Why Markdown, not Word:** Markdown keeps the flow connector-light for a live demo and renders fine in SharePoint preview. To produce a `.docx` instead, swap the "Create file" content through the **Word Online (Business) "Populate a Word template"** action with a template that has content controls for the seven sections.
- **The "17 goals" line is intentional and load-bearing.** The Standard v2 PDF documents 17 goals; one stale Microsoft Learn article says 14. The prompt forces 17 so the generated document is correct.
- **Connection reference:** once this flow exists, its connection reference logical name must be added to `RAI Advisor/connectionreferences.mcs.yml` (currently an empty `[]` shell). See the workflow guide.
- **Sources:** Impact Assessment template <https://aka.ms/RAIImpactAssessmentTemplatePDF> | Responsible AI hub (entry point to the Standard) <https://aka.ms/RAI>
