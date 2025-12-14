# Build Steps — Classify and Route

## Goal
Teach the agent to classify and route documents using the routing rules CSV.

## Recommended trigger
Use **The agent chooses** trigger so generative orchestration can select this topic when an event comes in.

## Steps
1. Open **Document Processor Agent** → **Topics** → **+ New topic**.
2. Name it: **Classify and Route**.
3. In the trigger node, select **The agent chooses**.
4. In the trigger description, paste:
   - `Classify an uploaded document and decide routing using routing-rules.csv. Use this when you have a file URL/name from an event trigger.`
5. Add a **Message** node:
   - `Okay. I’ll classify the document and decide where it should go.`
6. Create topic variables:
   - `t_file_url` (Text)
   - `t_file_name` (Text)
   - `t_library` (Text)
   - `t_doc_type` (Text)
   - `t_route_to` (Text)
   - `t_confidence` (Number)
7. Add a **Set variable** node (optional but recommended for event-trigger runs):
   - Map fields from the trigger payload into `t_file_url`, `t_file_name`, and `t_library`.
8. Add a **Generative answers** node:
   - Paste the instructions under “Classify + route” from `topic.blueprint.yaml`.
   - Save outputs to `t_doc_type`, `t_route_to`, `t_confidence`.
9. Add a **Condition** node:
   - If `t_route_to` equals `ManualReview`:
     - post a message and optionally call a flow to notify reviewers
   - Else:
     - confirm classification and destination and optionally call a flow to move the file
10. End.

## Testing
Use the sample payload in `assets/sharepoint-file-created.sample.json`.
Pretend the file content is the text in `assets/sample-invoice.txt`.

