# Build Steps — Extract Metadata

## Goal
Turn a document into structured JSON fields (invoice number, total, dates, parties).

## Steps
1. Open **Document Processor Agent** → **Topics** → **+ New topic**.
2. Name it: **Extract Metadata**.
3. Trigger: **The agent chooses**.
4. Add a **Generative answers** node:
   - Paste the instructions in `topic.blueprint.yaml`.
   - Save output to `t_extracted_fields` (Text).
5. Add a **Message** node printing the JSON.
6. End.

## Teaching pattern
Run this topic immediately after **Classify and Route** by using a **Go to** node or by letting orchestration pick it next.

