# Build Steps — Day 1 Checklist

## Goal
Gather role + start date + location and return a tailored Day 1 plan using the onboarding knowledge files.

## Steps
1. Open **Employee Onboarding Agent** → **Topics** → **+ New topic**.
2. Name it: **Day 1 Checklist**.
3. Trigger: **User says a phrase**.
4. Add trigger phrases (at least 8):
   - day 1 checklist
   - what do I do on my first day
   - first day onboarding
   - getting started
   - new hire checklist
   - start onboarding
   - what should I do first
   - onboarding steps
5. Add three **Ask a question** nodes:
   - Role → `t_role`
   - Start date → `t_start_date`
   - Location → `t_location`
6. Add a **Generative answers** node:
   - Paste the plan instructions from `topic.blueprint.yaml`.
   - Save output to `t_plan`.
7. Add a **Message** node that prints `{t_plan}`.
8. End.

## Teaching tip
If learners struggle, have them open the uploaded knowledge sources and read two lines from each before testing.
That helps them “feel” that the agent is grounded in data instead of vibes.

