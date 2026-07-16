# Copilot Studio Licensing: July 2026 Lay of the Land

> Last verified: July 2026. Pricing flagged inline with as-of dates. Numbers Microsoft can change without notice. Re-check the [Copilot Studio Licensing Guide](https://go.microsoft.com/fwlink/?linkid=2320995) before any delivery.

**TL;DR:** Building agents is free (the **maker license is $0**). The cost is **consumption** at runtime, metered in **Copilot Credits**. If your end users already hold a **Microsoft 365 Copilot** license, their agent usage inside M365 surfaces is **zero-rated** (free). Everything else burns credits.

---

## 1. Who Needs a License

Two distinct populations. Do not conflate them.

| Population | Who they are | What they need |
|-----------|-------------|----------------|
| **Makers** | People who build, edit, and publish agents | A **Copilot Studio User License** ($0) **or** an **M365 Copilot** license **or** the **Copilot Studio authors** role. Plus the tenant must have a prepaid Copilot Credit pack before the free user license can be granted. |
| **End users** | People who chat with a published agent | No per-seat license to *use* an agent. Their **runtime consumption** is what costs money (see Sections 3 and 4). |

**Publishing gate.** To publish an agent, the maker must meet **one** of these (trial licenses do **not** qualify):

1. Has an **M365 Copilot** license assigned.
2. Has a **Copilot Studio User License** assigned **and** credits allocated to the environment.
3. Has a **Copilot Studio User License** assigned **and** "Draw from tenant pool" enabled for the environment.
4. Has an **Office license only** **and** the agent uses **no generative AI** features.

**Trial license caveat.** Lets an individual build and test agents in the test chat panel, but **cannot publish**. Good for the classroom, useless for production.

---

## 2. How to Get Licenses (Purchase Paths)

| SKU / path | What it is | Price (as-of) | M365 tenant required? | Where to buy |
|-----------|-----------|---------------|----------------------|--------------|
| **Copilot Studio User License** | Maker seat. Build and publish rights. | **$0 / user / month** (verified July 2026; tenant must first hold a Copilot Credit pack) | Yes | Microsoft 365 admin center |
| **Copilot Credit Capacity Pack** (prepaid) | Tenant-pooled credits, monthly subscription, resets monthly | **$200 / pack / month = 25,000 Copilot Credits** (verified July 2026) | Yes | Microsoft 365 admin center |
| **Pay-as-you-go (PAYG) meter** | Consumption billed to an Azure subscription, no upfront commitment | **$0.01 / Copilot Credit** (verified July 2026) | Yes (M365 tenant + linked Azure subscription) | Azure subscription, via a Power Platform billing policy |
| **Copilot Credits Pre-Purchase Plan** | One-year prepaid pool (Copilot Credit Commit Units), tiered volume discounts | Tiered, **not publicly listed** (could not verify a flat number) | Yes | Azure portal; counts toward **MACC** |
| **Trial license** | Individual sign-up, build and test only, no publish | $0 | Yes | Self-service or admin-assigned |

**M365 Copilot license** ($30 / user / month list, widely reported; treat as the prerequisite for the Section 4 benefit) is a separate USL that *includes* limited Copilot Studio use rights. See Section 4.

**Recent change worth flagging:** Per Microsoft blog coverage, **starting April 20, 2026**, prepaid Copilot capacity packs work **without** a pay-as-you-go billing policy and **without** an Azure subscription. Buy packs, allocate credits, done. Pairing a pack *with* PAYG still gives you automatic overage spillover.

---

## 3. What Copilot Credits Are (The Metering Model)

**Copilot Credits** (renamed from **"messages"** on **September 1, 2025**; same plumbing, same rates, new label) are the **common currency** that meters agent runtime. Credits are **tenant-pooled**, **assigned to environments**, **reset monthly**, and **do not roll over**.

### Two ways to pay, both can coexist

| Model | How it bills | Overage behavior |
|-------|-------------|-----------------|
| **Prepaid capacity packs** | Buy 25,000-credit packs up front; consumed first | When exhausted, service stops **unless** PAYG is paired |
| **Pay-as-you-go** | Azure meter, billed in arrears at $0.01/credit | No hard stop. Overage flows to the Azure invoice |

When both are active, **prepaid is consumed first**, then PAYG covers the overage. With prepaid-only, hitting zero means **service denial** until the monthly reset.

### What consumes credits (billing rates)

Source: [Billing rates and management](https://learn.microsoft.com/microsoft-copilot-studio/requirements-messages-management#copilot-credits-billing-rates). Verified July 2026. Rightmost column is the Section 4 punchline.

| Agent feature | Credits | M365 Copilot-licensed user |
|--------------|--------:|----------------------------|
| **Classic answer** (authored topic) | 1 | No charge |
| **Generative answer** | 2 | No charge |
| **Agent action** (connector/tool call) | 5 | No charge |
| **Tenant graph grounding** per message | 10 | No charge |
| **Agent flow actions** per 100 actions | 13 | No charge |
| AI tools - basic (text/gen AI) per 10 responses | 1 | No charge |
| AI tools - standard | 15 | No charge |
| AI tools - premium | 100 | No charge |
| **Content processing** per page | 8 | No charge |
| **Basic voice** (classic orchestration) per min | 10 | Included |
| **Standard voice** (generative) per min | 35 | Included |
| **Premium voice** (real-time) per min | 75 | Included |

**Metering gotchas:**

- A **proactive greeting** counts as a **billed credit** (Classic Answer rate) even if the user never replies.
- An agent merely **triggered and ready** consumes a Classic Answer credit.
- **Bring-your-own-model** (Azure Foundry) processing is billed **separately** in Foundry by token, not by Copilot Credit (the invocation still counts as an agent action).
- Forecast before you commit with the [Copilot Credit Estimator](https://microsoft.github.io/copilot-studio-estimator/).

---

## 4. The M365 Copilot Benefit (The Most Important Takeaway)

**This is the practical headline.** If your end users **already hold an M365 Copilot license**, their agent usage inside M365 surfaces is **zero-rated**. You do **not** spin the Copilot Studio meter.

### What is free for an M365 Copilot-licensed user

When the agent runs under the **authenticated M365 Copilot user's identity**, inside **Microsoft 365 Copilot Chat, Microsoft Teams, or SharePoint**, the following are **no charge** (employee-facing / business-to-employee scenarios, subject to fair-use limits Microsoft can revise):

- **Classic answers**
- **Generative answers**
- **Microsoft Graph tenant grounding** (answers grounded only on the user's own M365 graph data)
- **SharePoint agents** and Copilot Chat agents built in Agent Builder
- The voice tiers' **core agent activity** (the per-minute voice rate still applies, but classic/generative/action activity within it is included)

### What still tips into metered / billed consumption

The free benefit has a hard edge. You pay credits the moment usage leaves the M365 fair-use lane:

| Stays free (M365 Copilot user, M365 surface) | Tips into billed credits |
|----------------------------------------------|--------------------------|
| Classic and generative answers in Copilot Chat / Teams / SharePoint | Agents on **external channels** (public website, custom app, Telephony, third-party messaging) |
| Microsoft Graph tenant grounding on the user's own data | End users **without** an M365 Copilot license (consumption hits the **Copilot Credits report** / meter) |
| SharePoint and Agent Builder agents | **Bring-your-own-model** Foundry processing (billed in Foundry) |
| Core agent activity within voice tiers | The **per-minute voice rate** itself (10 / 35 / 75 credits) |
| | Usage **beyond fair-use limits** |

**Rule of thumb for the course:** *Same data, same building, same user, inside Microsoft 365 = free for M365 Copilot holders. Cross the boundary (external channel, unlicensed user, your own model) and the meter spins.*

**Mixed-population reality:** A tenant typically has some M365 Copilot seats (free agent usage) and some users without (metered). The **Copilot Credits report** in the Microsoft 365 admin center surfaces credits burned by **unlicensed** users hitting metered agents, with an alert past **2,000 credits** per user.

---

## Sources

- Copilot Studio licensing (maker configs, M365 inclusion, currency rename) <https://learn.microsoft.com/microsoft-copilot-studio/billing-licensing>
- Billing rates and management (the credit rate table, overage enforcement) <https://learn.microsoft.com/microsoft-copilot-studio/requirements-messages-management>
- Copilot Credits overview (PAYG $0.01, pack $200/25,000, pre-purchase plan) <https://learn.microsoft.com/microsoft-copilot-studio/copilot-credits-overview>
- Quotas and limits (RPM/RPH per environment) <https://learn.microsoft.com/microsoft-copilot-studio/requirements-quotas>
- FAQ for billing and licensing (publish gate, proactive greeting) <https://learn.microsoft.com/microsoft-copilot-studio/faq-billing-licensing>
- Prepaid capacity packs for M365 Copilot Chat / SharePoint agents (pack reset, overage continuity, April 2026 no-Azure change) <https://learn.microsoft.com/microsoft-365/copilot/pay-as-you-go/copilot-capacity-packs>
- M365 Copilot credits report (unlicensed-user metering, 2,000-credit alert) <https://learn.microsoft.com/microsoft-365/admin/activity-reports/microsoft-365-copilot-credits>
- Power Platform licensing FAQ (Copilot Studio User License $0) <https://learn.microsoft.com/power-platform/admin/powerapps-flow-licensing-faq>
- Copilot Studio Licensing Guide (PDF, Feb 2026, authoritative) <https://go.microsoft.com/fwlink/?linkid=2320995>
- Copilot Credit Estimator <https://microsoft.github.io/copilot-studio-estimator/>
