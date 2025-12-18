# Quick-Start: Triggers and Flows

**For:** Customer Service Assistant Agent
**Time:** 20-30 minutes
**Skill level:** Beginner

---

## What You Will Build

Four simple triggers that make your agent respond to users:

| Trigger | What It Does |
|---------|--------------|
| Greeting | Says hello when conversation starts |
| Returns and Refunds | Activates when user asks about returns |
| Order Status | Activates when user asks about orders |
| Escalate to Human | Activates when user wants a real person |

---

## Before You Start

You need:

- [ ] Microsoft 365 account with Copilot Studio access
- [ ] Your Customer Service Assistant agent already created
- [ ] About 20-30 minutes of focused time

---

## Key Terms (Read First)

| Term | Plain English |
|------|---------------|
| **Trigger** | The thing that makes a topic start. Like a doorbell that activates when pressed. |
| **Topic** | A conversation flow about one subject. Like a script for one type of question. |
| **Node** | One step in a conversation. Like a single line in a script. |
| **Trigger phrase** | Words the user might type that activate a topic. |

---

## Part 1: Greeting Trigger

**Goal:** Your agent says hello when users start chatting.

---

### Step 1: Open your agent

- [ ] Go to [copilotstudio.microsoft.com](https://copilotstudio.microsoft.com)
- [ ] Sign in with your Microsoft account
- [ ] Click on **Customer Service Assistant** to open it

---

### Step 2: Find the Greeting topic

- [ ] Look at the left sidebar
- [ ] Click `Topics`
- [ ] Find **Greeting** in the list (it already exists)
- [ ] Click on it to open

---

### Step 3: Check the trigger type

- [ ] Look at the top of the canvas
- [ ] Find the box labeled `Trigger`
- [ ] It should say **A message is received** or **The conversation changes**

**Why this trigger?**
Greetings fire when ANY message arrives or when someone joins. This is different from phrase-based triggers.

---

### Step 4: Customize the greeting message

- [ ] Find the `Message` node below the trigger
- [ ] Click on it
- [ ] Replace the text with:

```
Hello! Welcome to Contoso Electronics support.

I can help with:
- Product questions
- Order status
- Returns and refunds
- Warranty info

What can I help you with today?
```

- [ ] Click `Save` in the top-right corner

---

### Step 5: Test the greeting

- [ ] Click `Test` button (top-right corner)
- [ ] Type: `Hi`
- [ ] Verify: Your greeting message appears

**Checkpoint: Greeting complete.**

---

## Part 2: Returns and Refunds Trigger

**Goal:** Agent recognizes when users want to return something.

---

### Step 1: Create a new topic

- [ ] Click `Topics` in the left sidebar
- [ ] Click `Add a topic`
- [ ] Select `From blank`

---

### Step 2: Name the topic

- [ ] Click `Details` in the toolbar (top of screen)
- [ ] In the panel that opens:
  - **Name:** `Returns and Refunds`
  - **Description:** `Help customers with returns and refund requests`
- [ ] Close the details panel

**Important:** Do NOT put periods in topic names. They break exports.

---

### Step 3: Set up the trigger

- [ ] Click on the `Trigger` node at the top
- [ ] Click the three dots `...` on the node
- [ ] Select `Properties`
- [ ] In **On Recognized Intent properties**, click the `Phrases` area

---

### Step 4: Add trigger phrases

Type these phrases (press Enter after each one):

```
I want to return an item
start a return
refund my order
how do returns work
return policy
I need a refund
can I send this back
return a damaged product
```

- [ ] Add all 8 phrases
- [ ] Close the properties panel

**Why 8 phrases?**
Microsoft recommends 5-10 varied phrases. More helps the AI understand different ways users ask.

---

### Step 5: Add an intro message

- [ ] Click the `+` button below the Trigger node
- [ ] Select `Send a message`
- [ ] Type this message:

```
I can help with returns and refunds.

Let me ask you two quick questions.
```

---

### Step 6: Ask for the order number

- [ ] Click the `+` button below your message
- [ ] Select `Ask a question`
- [ ] In the question text, type:

```
What is your order number?
```

- [ ] In the `Identify` dropdown, select `User's entire response`
- [ ] Under `Save response as`, click `Create new variable`
- [ ] Name it: `t_order_number`

---

### Step 7: Ask for the reason

- [ ] Click the `+` button below the question
- [ ] Select `Ask a question`
- [ ] Type:

```
What is the reason for your return?

- Damaged product
- Wrong item received
- Changed my mind
- Other
```

- [ ] Save response to a new variable: `t_return_reason`

---

### Step 8: Add a response message

- [ ] Click the `+` button
- [ ] Select `Send a message`
- [ ] Type:

```
Thanks! Based on your order number and reason, here is what to do next:

1. Pack the item in original packaging
2. Print the return label from your confirmation email
3. Drop off at any shipping location

Refunds process in 5-7 business days.

Is there anything else I can help with?
```

---

### Step 9: End the topic

- [ ] Click the `+` button
- [ ] Select `Topic management`
- [ ] Select `End current topic`

---

### Step 10: Save and test

- [ ] Click `Save` (top-right)
- [ ] Click `Test`
- [ ] Type: `I want to return something`
- [ ] Verify: The Returns topic activates

**Checkpoint: Returns and Refunds complete.**

---

## Part 3: Order Status Flow

**Goal:** User asks about an order, agent collects info and responds.

---

### Step 1: Create the topic

- [ ] Click `Topics` > `Add a topic` > `From blank`
- [ ] Open `Details`
- [ ] **Name:** `Order Status`
- [ ] **Description:** `Help customers check order and delivery status`

---

### Step 2: Add trigger phrases

- [ ] Click on the `Trigger` node
- [ ] Open `Properties` via the `...` menu
- [ ] Add these phrases:

```
where is my order
order status
track my package
has my order shipped
delivery date
my order hasn't arrived
tracking number
shipment status
```

---

### Step 3: Add a question node

- [ ] Click `+` below the Trigger
- [ ] Select `Ask a question`
- [ ] Type:

```
Sure! What is your order number?

You can find it in your confirmation email or on your packing slip.
```

- [ ] Save to variable: `t_order_number`

---

### Step 4: Add a response message

- [ ] Click `+`
- [ ] Select `Send a message`
- [ ] Type:

```
Looking up order {Topic.t_order_number}...

Your order status: **Shipped**
Estimated delivery: 2-3 business days
Tracking: Click here to track on carrier website

Is there anything else you need help with?
```

**Note:** `{Topic.t_order_number}` inserts the variable value. This is how you show back what the user typed.

---

### Step 5: End and save

- [ ] Add `End current topic` node
- [ ] Click `Save`

---

### Step 6: Test it

- [ ] Click `Test`
- [ ] Type: `Where is my order?`
- [ ] Enter an order number when asked: `12345`
- [ ] Verify: Agent responds with status

**Checkpoint: Order Status complete.**

---

## Part 4: Escalate to Human Trigger

**Goal:** User can always reach a real person when needed.

---

### Step 1: Create the topic

- [ ] `Topics` > `Add a topic` > `From blank`
- [ ] **Name:** `Escalate to Human`
- [ ] **Description:** `Transfer customer to human support agent`

---

### Step 2: Add trigger phrases

- [ ] Open Trigger `Properties`
- [ ] Add these phrases:

```
talk to a person
human agent
representative
escalate this
this isn't working
complaint
supervisor
I need help now
```

---

### Step 3: Add an acknowledgment message

- [ ] Click `+` below Trigger
- [ ] Select `Send a message`
- [ ] Type:

```
I understand you'd like to speak with a person.

Let me connect you with a support specialist who can help.
```

---

### Step 4: Ask for context (optional but helpful)

- [ ] Click `+`
- [ ] Select `Ask a question`
- [ ] Type:

```
Before I transfer you, could you briefly describe your issue?

This helps the agent assist you faster.
```

- [ ] Save to variable: `t_issue_summary`

---

### Step 5: Add handoff message

- [ ] Click `+`
- [ ] Select `Send a message`
- [ ] Type:

```
Thanks for that context.

A support agent will be with you shortly.

Summary of your issue: {Topic.t_issue_summary}

Average wait time: 2-5 minutes
```

---

### Step 6: End the conversation

- [ ] Click `+`
- [ ] Select `Topic management`
- [ ] Select `End conversation`

**Note:** `End conversation` is different from `End current topic`. Use `End conversation` when handing off to a human.

---

### Step 7: Save and test

- [ ] Click `Save`
- [ ] Click `Test`
- [ ] Type: `I want to talk to a human`
- [ ] Verify: Escalation flow runs

**Checkpoint: Escalate to Human complete.**

---

## Quick Reference: Node Types

| Node | When to Use | Where to Find |
|------|-------------|---------------|
| `Send a message` | Show text to user | Click `+` > `Send a message` |
| `Ask a question` | Get info from user | Click `+` > `Ask a question` |
| `Condition` | Branch based on answer | Click `+` > `Add a condition` |
| `End current topic` | Finish this topic | Click `+` > `Topic management` |
| `End conversation` | End entire chat | Click `+` > `Topic management` |
| `Redirect to topic` | Jump to another topic | Click `+` > `Topic management` |

---

## Quick Reference: Trigger Types

| Trigger | Use When |
|---------|----------|
| **User says a phrase** | User types specific words (most common) |
| **A message is received** | Any message from user (good for greetings) |
| **The conversation changes** | User joins or leaves (Teams channels) |
| **The agent chooses** | Let AI decide based on description (generative mode) |
| **It's redirected to** | Called by another topic |

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Topic does not trigger | Add more varied trigger phrases (aim for 8+) |
| Wrong topic triggers | Check for overlapping phrases between topics |
| Variable shows as blank | Make sure variable name matches exactly |
| Save button grayed out | Check for errors in red on any node |
| Test panel does not open | Refresh the page and try again |

---

## What You Built

You now have four working triggers:

- [x] **Greeting** - Welcomes users
- [x] **Returns and Refunds** - Handles return questions
- [x] **Order Status** - Checks order info
- [x] **Escalate to Human** - Hands off to real agents

---

## Next Steps

When you are ready, you can enhance these flows:

1. **Add Generative Answers** - Let AI answer from knowledge sources
2. **Add Power Automate** - Look up real order data
3. **Add Conditions** - Branch based on user answers
4. **Publish to Teams** - Make it available to users

---

## Resources

- [Topics in Copilot Studio](https://learn.microsoft.com/en-us/microsoft-copilot-studio/authoring-create-edit-topics)
- [Trigger Types Reference](https://learn.microsoft.com/en-us/microsoft-copilot-studio/authoring-triggers)
- [Topic Authoring Best Practices](https://learn.microsoft.com/en-us/microsoft-copilot-studio/guidance/topic-authoring-best-practices)

---

**Document version:** 2025-01
**Last verified against:** Copilot Studio web app (December 2024)
