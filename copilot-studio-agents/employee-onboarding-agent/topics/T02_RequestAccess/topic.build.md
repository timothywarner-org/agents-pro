# Build Steps — Request Access

## Goal
Collect what system they need, why, and manager approval, then submit the request (optionally via Power Automate).

## Steps
1. Open **Employee Onboarding Agent** → **Topics** → **+ New topic**.
2. Name it: **Request Access**.
3. Trigger: **User says a phrase**.
4. Add trigger phrases:
   - I need access
   - request access to an app
   - need permissions
   - can't log in
   - access request
   - I need VPN
   - I need github access
   - need microsoft 365 access
5. Add **Ask a question** nodes to capture:
   - `t_app_or_system`
   - `t_reason`
   - `t_manager`
6. Add a **Generative answers** node to format a clean request summary.
   - Save to `t_request_summary`.
7. Add a **Message** node printing `{t_request_summary}`.
8. Optional: add an **Action** node calling an agent flow named `CreateITTicket`.

## Testing
Use `assets/sample-request.json` as your “fake payload” to keep demos consistent.

