# Build Steps — Order Status

## Goal
Get an order number and return a simple status summary.

## Steps in Copilot Studio
1. Open **Customer Service Assistant** → **Topics** → **+ New topic**.
2. Name it: **Order Status**.
3. Trigger: **User says a phrase**.
4. Add these trigger phrases:
   - where is my order
   - order status
   - track my package
   - has my order shipped
   - delivery date
   - my order hasn't arrived
   - tracking number
   - shipment status
5. Add **Ask a question**:
   - `Sure. What’s your **order number**?`
   - Save to `t_order_number` (Text)
6. Add an **Action** node that calls an **agent flow** named `GetOrderStatus`.
   - Input: `orderNumber` = `t_order_number`
   - Output: `statusSummary` → `t_status_summary`
7. Add a **Message** node:
   - `Here’s what I see:` then include `{t_status_summary}`
8. End the topic.

## If you’re teaching without Power Automate
Swap step 6 for a **Generative answers** node and have it produce a *plausible* status summary and a “what to do next” suggestion.

