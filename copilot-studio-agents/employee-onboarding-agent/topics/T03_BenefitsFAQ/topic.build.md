# Build Steps — Benefits FAQ

## Goal
Let the user ask a benefits question, then answer using your uploaded benefits knowledge files.

## Steps
1. Open **Employee Onboarding Agent** → **Topics** → **+ New topic**.
2. Name it: **Benefits FAQ**.
3. Trigger: **User says a phrase**.
4. Add trigger phrases:
   - benefits
   - health insurance
   - when do benefits start
   - 401k
   - PTO
   - vacation policy
   - open enrollment
   - dental and vision
5. Add **Ask a question**:
   - `What’s your benefits question?`
   - Save to `t_question`
6. Add **Generative answers**:
   - Paste the instructions from `topic.blueprint.yaml`.
   - Save output to `t_answer`.
7. Add **Message** printing `{t_answer}`.
8. End.

