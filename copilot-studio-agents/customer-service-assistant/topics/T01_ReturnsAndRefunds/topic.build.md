# Build Steps — Returns and Refunds

## Goal
Capture an order number and reason, then produce an eligibility decision and next steps using your **Returns Policy** knowledge file.

## Steps in Copilot Studio
1. Open **Customer Service Assistant**.
2. Select **Topics**.
3. Select **+ New topic**.
4. Name it: **Returns and Refunds**.
5. In the trigger node, choose **User says a phrase**.
6. Add these trigger phrases (add at least 8):
   - I want to return an item
   - start a return
   - refund my order
   - how do returns work
   - return policy
   - I need a refund
   - can I send this back
   - return a damaged product
7. Add a **Message** node:
   - `I can help with returns and refunds. I’ll ask two quick questions.`
8. Add an **Ask a question** node:
   - Question: `What’s your **order number**?`
   - Save response to a **topic variable** named `t_order_number` (Text)
9. Add another **Ask a question** node:
   - Question: `What’s the **reason** for the return (damaged, wrong item, changed mind, other)?`
   - Save response to `t_return_reason` (Text)
10. Add a **Generative answers** node (or equivalent “AI response” node in your UI):
    - Paste the instructions from `topic.blueprint.yaml` under **Eligibility + next step**.
    - Configure outputs:
      - `t_is_eligible` (Boolean)
      - `t_next_step` (Text)
11. Add a **Condition** node:
    - If `t_is_eligible` is true:
      - Message: `✅ Eligible. Here’s what to do next:` then print `{t_next_step}`
    - Else:
      - Message: `⚠️ Not eligible under the standard return policy.` then print `{t_next_step}`
      - Optional: **Go to topic** → Warranty Inquiry
12. End the topic.

## Test scripts
Use `assets/test-chat.transcript.md`.

