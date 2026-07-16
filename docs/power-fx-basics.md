# Power Fx Basics for Copilot Studio Makers

> Last verified: July 2026 (Microsoft Learn `microsoft-copilot-studio/advanced-power-fx` and `power-platform/power-fx/formula-reference-copilot-studio`).

A quickstart for the **one expression language** you reach for when point-and-click runs out of road in Copilot Studio. This is not an Excel tutorial. Every example below is framed around how a real Copilot Studio maker wires up topics, variables, conditions, and Power Automate actions.

## 1. What Power Fx Is and Why Copilot Studio Uses It

**Power Fx** is Microsoft's **low-code, declarative, Excel-like expression language**. "Declarative" means you describe the result you want, not the steps to compute it. The same `Upper("contoso")` you would type in an Excel cell evaluates the same way in a Copilot Studio topic. That is the whole point: business makers already think in formulas, so Copilot Studio borrows the formula model instead of inventing a new one.

In Copilot Studio, Power Fx is the **escape hatch** that the graphical authoring canvas hands you when the no-code controls cannot express your logic. You meet it in five places:

| Where it appears | What you do there |
|------------------|-------------------|
| **Set a variable value node** | Compute a value with a formula instead of typing a literal. This is the most common entry point. |
| **Condition node** | Use **Change to formula** to branch on a boolean expression that the dropdown builder cannot express. |
| **Question / Message node** | Drop a formula into the message text to inject computed strings. |
| **Adaptive Card node** | Switch the card from JSON to **Formula** mode so card fields reference variables dynamically. |
| **Action (Power Automate flow) inputs** | Build the record or value you pass into a flow's input parameter. |

The **formula bar** is where you type. When you open the **Formula** tab (the **fx** box), Copilot Studio is already in formula context, so you type the expression directly, for example `Upper(Text(Topic.customerName))`. In the **graphical YAML / code editor** view, a Power Fx value is marked with a leading **`=`** prefix. That `=` is the signal "the rest of this is a formula, evaluate it" rather than "this is a literal string." Watch for it when you read or hand-edit the YAML.

One non-obvious rule: Power Fx formulas in Copilot Studio use **US-style numbering**. The decimal separator is a period (`12567.892`), so you **must** separate function parameters with **commas**, never semicolons.

## 2. Variables and Scope

Every variable reference in a formula needs a **scope prefix** so Power Fx knows where to look. Copilot Studio has four scopes. Three matter day to day.

| Scope prefix | Lives where | Lifetime | Use it for |
|--------------|-------------|----------|------------|
| **`Topic.`** | Inside the topic that created it (default scope) | The current topic run | Working values local to one conversation flow, for example `Topic.orderId` |
| **`Global.`** | Every topic in the agent (one user session) | Until the session ends or **Reset Conversation** fires | Values you reuse across topics, for example `Global.UserName` captured once and reused everywhere |
| **`System.`** | Built in, available everywhere, read-only | Managed by Copilot Studio | Conversation and user context, for example `System.User.DisplayName`, `System.Conversation.Id` |
| **`Environment.`** | Power Platform environment variables, read-only in Copilot Studio | Per environment | Config keys and values that change between dev and prod without editing topics |

Two things that trip people up:

- A **global** variable is just a topic variable whose scope you flipped to **Global (any topic can access)** in the Variable properties panel. In **classic / Teams** authoring the prefix shows as the older **`bot.`** (for example `bot.UserName`) instead of `Global.`. Same concept, older label.
- Some **system variables are hidden** from the `{x}` variable picker. The only way to reach them is a Power Fx formula with the `System.` prefix. So if you cannot find `User.DisplayName` in the dropdown, type `System.User.DisplayName` in a formula instead.

Referencing a variable in a formula is just the prefixed name:

```powerfx
=System.User.DisplayName
```

## 3. Core Syntax Quick-Reference

Every function below is listed on the **Copilot Studio formula reference** page, so it is part of the supported subset (not just generic Power Fx). The example column is Copilot-Studio-flavored.

### Text

| Function | What it does | Copilot Studio example |
|----------|--------------|------------------------|
| **Concatenate** | Joins strings (the `&` operator does the same) | `Concatenate("Hi ", Topic.firstName, "!")` |
| **Substitute** | Replaces matched text | `Substitute(Topic.phone, "-", "")` to strip dashes |
| **Lower** / **Upper** / **Proper** | Change case | `Lower(System.User.Email)` to normalize an email |
| **Trim** | Removes leading, trailing, and interior extra spaces | `Trim(Topic.rawInput)` |
| **Len** | Length of a string | `Len(Topic.accountNumber)` to validate length |

### Logic

| Function | What it does | Copilot Studio example |
|----------|--------------|------------------------|
| **If** | Branches on a condition | `If(Topic.amount > 500, "Approval needed", "Auto-approve")` |
| **Switch** | Matches a value against cases | `Switch(Topic.region, "EMEA", "London", "AMER", "Dallas", "HQ")` |
| **And** / **Or** | Boolean combine (`&&` / `\|\|` operators too) | `And(System.User.IsLoggedIn, Topic.consentGiven)` |
| **IsBlank** | True when a value is blank or unset | `IsBlank(Topic.orderId)` |
| **IsEmpty** | True when a table has no rows | `IsEmpty(Topic.lineItems)` |

### Tables and Records

| Function | What it does | Copilot Studio example |
|----------|--------------|------------------------|
| **First** | First record of a table | `First(Topic.searchResults).Title` |
| **Last** | Last record of a table | `Last(Topic.history).Text` |
| **CountRows** | Number of rows in a table | `CountRows(Topic.cartItems)` |
| **Filter** | Rows matching a criterion | `Filter(Topic.tickets, Priority = "High")` |
| **Patch** | Creates or merges a record | `Patch(Topic.customer, {Status: "Active"})` |
| **ForAll** | Evaluates an expression over every row | `ForAll(Topic.orders, Value(Amount))` |

### Date and Time

| Function | What it does | Copilot Studio example |
|----------|--------------|------------------------|
| **Now** | Current date and time in the user's time zone | `Now()` |
| **Today** | Current date, no time component | `Today()` |
| **DateAdd** | Adds an interval to a date | `DateAdd(Today(), 14, TimeUnit.Days)` |
| **Text** (date formatting) | Formats a date into a friendly string | `Text(Today(), "dddd, mmmm d, yyyy")` |

### Type Conversion

| Function | What it does | Copilot Studio example |
|----------|--------------|------------------------|
| **Value** | Parses a string into a number | `Value(Topic.quantityText)` |
| **Text** | Converts any value to a string (and formats numbers and dates) | `Text(Topic.total, "$#,##0.00")` |

## 4. Worked Examples

Realistic snippets you would paste into a **Set a variable value** node, a **Condition** formula, or an action input. Comments explain the **why**.

**Build a personalized greeting from the signed-in user.** Falls back gracefully when the identity provider does not return a name, because `User.DisplayName` is not guaranteed to have a value.

```powerfx
// Coalesce-style guard: never greet "Hello, " with an empty name
=Concatenate("Hello, ", If(IsBlank(System.User.DisplayName), "there", System.User.DisplayName), "! How can I help?")
```

**Normalize a messy order ID before lookup.** Users paste order IDs with stray spaces and lowercase letters. Trim first, then uppercase, so the downstream system match is deterministic.

```powerfx
// Trim handles copy-paste whitespace; Upper makes the match case-insensitive
=Upper(Trim(Topic.rawOrderId))
```

**Branch when a required value is missing.** Put this in a **Condition** node via **Change to formula**. If the order ID is still blank, route to a re-prompt path instead of calling the API with garbage.

```powerfx
// True path = we are missing data and must ask again before calling the flow
=IsBlank(Topic.orderId)
```

**Format today's date into a friendly confirmation string.** Raw `Today()` renders as a machine date. The format string turns it into something a customer wants to read.

```powerfx
// "Tuesday, June 3, 2026" reads better than "6/3/2026" in a confirmation message
=Text(Today(), "dddd, mmmm d, yyyy")
```

**Parse a number out of a text variable.** Question nodes that capture "User's entire response" hand you a **string**. Convert before doing math, or comparisons silently misbehave.

```powerfx
// Value() turns the captured text "12" into the number 12 so arithmetic works
=Value(Topic.quantityText) * Topic.unitPrice
```

**Construct a record to pass into a Power Automate action.** Action inputs that expect structured data take a Power Fx record. Build it inline so the flow receives clean, typed fields.

```powerfx
// One record, typed fields, ready to hand to the "Create ServiceNow ticket" flow input
={ requesterEmail: System.User.Email, summary: Trim(Topic.issueSummary), priority: If(Topic.isUrgent, "1 - Critical", "3 - Moderate") }
```

## 5. Gotchas

Power Fx in Copilot Studio is a **subset** of the language used in Power Apps canvas apps. The differences below are the ones that actually bite makers.

- **No UI controls exist.** Canvas-app formulas constantly reference controls like `TextInput1.Text` or navigation like `Navigate(...)`. None of that exists in Copilot Studio. There is no screen, no gallery, no control tree. Your only inputs are **variables** (`Topic.`, `Global.`, `System.`, `Environment.`) and **literals**.

- **The leading `=` is required in the YAML / code view.** A value without `=` is a literal string. `Hello` is the five-letter word; `=Hello` is a reference to something named `Hello`. In the **fx** formula box the editor is already in formula context, but the moment you hand-edit YAML, a missing `=` turns your formula into plain text.

- **It is a supported subset, not all of Power Fx.** Functions tied to app behavior or local storage, for example **`SaveData`**, **`LoadData`**, **`Navigate`**, **`Set`** / **`UpdateContext`**, and **`PDF`**, are **not available**. If a function is not on the Copilot Studio formula reference page, do not assume it works. The supported list is the source of truth.

- **Some working functions are undocumented.** The reverse also happens. A few functions (community reports cite **`Sequence`**) execute correctly even though they are not on the reference page. Treat these as **unverified**: useful in a pinch, but do not build a learner demo on them without testing in your own environment first.

- **String interpolation (`$"Hello {Name}"`) is unreliable here.** The dollar-brace syntax collides with how Copilot Studio's underlying YAML embeds variables, and it can error or behave oddly. **Use `Concatenate` or the `&` operator instead.** This is a Copilot-Studio-specific hazard, not a general Power Fx one.

- **Arrays are single-column tables of records.** `[1, 2, 3]` is not a list of bare integers. Power Fx stores it as a table of records `[{Value: 1}, {Value: 2}, {Value: 3}]`. To read an element you go through the `.Value` column, for example `First([10, 20, 30]).Value` returns `10`. Forgetting `.Value` is the most common table-handling mistake.

- **Commas, not semicolons, separate parameters.** Because Copilot Studio uses US-style numbering (period as the decimal point), the parameter separator is the **comma**. `DateAdd(Today(), 14, TimeUnit.Days)` is correct; semicolons will fail.

- **Captured responses are strings until you convert them.** A Question node saving "User's entire response" gives you text. Wrap numeric input in `Value()` and date input in `DateValue()` before comparing or computing, or your conditions will quietly compare strings.

## Sources

- Create expressions using Power Fx (Copilot Studio): <https://learn.microsoft.com/microsoft-copilot-studio/advanced-power-fx>
- Formula reference (the supported function subset): <https://learn.microsoft.com/power-platform/power-fx/formula-reference-copilot-studio>
- Variables overview (Topic, Global, System, Environment scope and the full system variable list): <https://learn.microsoft.com/microsoft-copilot-studio/authoring-variables-about>
- Work with global variables: <https://learn.microsoft.com/microsoft-copilot-studio/authoring-variables-bot>
- Ask with Adaptive Cards (Power Fx Formula mode on cards): <https://learn.microsoft.com/microsoft-copilot-studio/authoring-ask-with-adaptive-card>
- Power Fx overview: <https://learn.microsoft.com/power-platform/power-fx/overview>
