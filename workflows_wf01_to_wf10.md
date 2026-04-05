# Complete Workflow Specifications: WF-01 through WF-10
## AI Productivity Intelligence System

**Document Purpose:** Complete state machines, timeout rules, and handoff contracts for all 10 workflows

---

## WF-01: Client Intake & Qualification

**Trigger:** Prospect replies to outreach OR inbounds via website/form

**Owner:** Sales/BDR

### ICP Scoring (All Three Must Pass)

| Criterion | Pass | Borderline | Fail |
|-----------|------|------------|------|
| Company Size | 50-500 employees | 30-50 employees | <30 or >500 |
| AI Tool Footprint | ≥3 tools across ≥2 depts | 1-2 tools, single dept | No tools or ChatGPT only |
| Budget Signal | Previous consultant use / budget stated | No signal but size suggests capacity | Price-sensitive / free tools only |

**Automatic Qualification Upgrade:** Any company operating in EU, UK, US (CA/IL/CO/NY), or India with AI in HR, finance, or healthcare → **QUALIFY regardless of tool footprint** (compliance urgency overrides)

### State Machine

```
                    ┌──────────────┐
                    │    LEAD      │
                    │  (new inbound│
                    │   or reply)  │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
              ┌─────│   QUALIFY    │─────┐
              │     │  (ICP check) │     │
              │     └──────┬───────┘     │
              │            │              │
         fail ICP     pass all 3      borderline
              │            │              │
              ▼            ▼              ▼
       ┌──────────┐ ┌──────────┐  ┌──────────┐
       │REJECTED  │ │FORM_SENT │  │  STALLED │
       │(log why) │ │(schedule  │  │(follow-up│
       │          │ │  call)    │  │  in 7d)  │
       └──────────┘ └─────┬────┘  └────┬─────┘
                          │             │
                          │             │ (no response
                          │             │  after 2nd)
                          │             │
                          ▼             ▼
                    ┌──────────┐  ┌──────────┐
                    │  AUDIT   │  │   COLD   │
                    │ INTAKE   │  │(re-approach│
                    │ (WF-02)  │  │ in 30d)  │
                    └──────────┘  └──────────┘
```

### Timeout Rules

| Stage | Timeout | Action |
|-------|---------|--------|
| No response to qualification (first) | 5 days | Mark stalled, follow-up in 7 days |
| No response after second follow-up | 3 days | Mark cold, re-approach in 30 days |
| Form sent but not submitted | 7 days | Send "need help?" email |

### Data Collected

```json
{
  "lead_id": "uuid",
  "company_name": "string",
  "contact_name": "string",
  "contact_email": "string",
  "source": "outbound_reply | inbound_form | referral | linkedin",
  "icp_scores": {
    "company_size": "pass | borderline | fail",
    "tool_footprint": "pass | borderline | fail",
    "budget_signal": "pass | borderline | fail"
  },
  "auto_qualify": "boolean (compliance urgency override)",
  "status": "lead | qualified | form_sent | stalled | rejected | cold",
  "created_at": "ISO8601",
  "updated_at": "ISO8601"
}
```

### Email Templates

**Template: Qualification Request (Email)**
```
Subject: Quick questions about your AI usage

Hi {first_name},

Thanks for your interest in the AI Compliance + Productivity Audit.

Before we proceed, I'd like to confirm the audit will be valuable for your situation. Could you share:

1. Roughly how many employees at {company}?
2. Which AI tools are currently in use (if any)?
3. Which departments are using them?

This helps me ensure the audit is the right fit before we invest time on both sides.

Best,
{auditor_name}
```

**Template: Rejection (Soft)**
```
Subject: Following up on your audit request

Hi {first_name},

Thanks for considering the AI Compliance + Productivity Audit.

Based on what you've shared, it sounds like {company} may be earlier-stage than our audit is optimized for. We typically work best with companies that have:
- 50+ employees
- 3+ AI tools in active use across multiple departments

That said, compliance requirements (especially the EU AI Act) apply regardless of size. If you'd like to proceed anyway, I'm happy to discuss.

Alternatively, I can share some free resources on EU AI Act compliance if that's your primary concern.

Let me know how you'd like to proceed.

Best,
{auditor_name}
```

---

## WF-02: Audit Intake

**Trigger:** Client qualified in WF-01

**Owner:** Audit Operations

### Primary Method: Conversational Scoring Agent

See `conversational_agent_prompt.md` for complete system prompt.

**Session Target:** 10-12 exchanges, 15-20 minutes

### Fallback Method: Google Form

See `form_spec_complete.md` for complete form structure.

**Form Settings:**
- Platform: Tally.so (preferred) or Google Forms
- Partial saves: Enabled (Tally only)
- Webhook: On submission → trigger WF-03

### Completeness Gate

```python
def check_completeness(responses):
    mandatory_fields = 24  # See form_spec_complete.md
    completed = sum(1 for f in mandatory_fields if responses.get(f))
    completeness_pct = (completed / len(mandatory_fields)) * 100
    
    if completeness_pct < 70:
        return "INCOMPLETE", completeness_pct
    elif completeness_pct < 100:
        return "PARTIAL", completeness_pct
    else:
        return "COMPLETE", completeness_pct
```

**Rule:** If >30% of mandatory fields missing after one chase → proceed with available data, flag all gaps in report

### State Machine

```
┌─────────────┐
│  FORM_SENT  │
│ (from WF-01)│
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  IN_PROGRESS│───┐
│ (client    │   │
│  filling)   │   │
└──────┬──────┘   │
       │          │ timeout (7 days)
       │          │
       ▼          ▼
┌─────────────┐ ┌─────────────┐
│  SUBMITTED  │ │   ABANDONED │
│             │ │ (log reason)│
└──────┬──────┘ └─────────────┘
       │
       ▼
┌─────────────┐
│COMPLETENESS │
│   CHECK     │
└──────┬──────┘
       │
   ┌───┴───┐
   │       │
   ▼       ▼
┌─────┐ ┌──────────┐
│OK   │ │INCOMPLETE│
│>70% │ │<30% miss │
└──┬──┘ └────┬─────┘
   │         │
   │         ▼
   │    ┌──────────┐
   │    │WF-03 CHASE│
   │    └────┬─────┘
   │         │
   │         ▼
   │    ┌──────────┐
   │    │RESPONSE? │
   │    └────┬─────┘
   │         │
   └────┬────┘
        │
        ▼
┌─────────────┐
│  WF-04      │
│  ANALYSIS   │
└─────────────┘
```

---

## WF-03: Data Collection & Chase

**Trigger:** Incomplete form submission OR vague conversational answers

**Owner:** Audit Operations

### Gap Identification

```python
def identify_gaps(responses):
    """Identify specific missing data points."""
    gaps = []
    
    # Check each mandatory field
    for field in MANDATORY_FIELDS:
        if not responses.get(field):
            gaps.append({
                "field": field,
                "question": FIELD_LABELS[field],
                "section": FIELD_SECTIONS[field]
            })
    
    # Check for vague answers
    if len(responses.get('tools_list', '')) < 10:
        gaps.append({
            "field": "tools_list_detailed",
            "question": "Please provide more detail on AI tools in use",
            "section": "Tool Stack"
        })
    
    return gaps
```

### Chase Email Template

```
Subject: Quick follow-up: Missing info for your AI audit

Hi {first_name},

Thanks for submitting your audit responses. I've reviewed them and just need a bit more detail on a few items to ensure the report is accurate:

{numbered list of specific gaps}

Could you reply with these details by {date = 3 business days}?

If I don't hear back, I'll proceed with the available data but will note in the report where information was not provided (findings may be incomplete as a result).

Best,
{auditor_name}
```

### Escalation Rule

**If >30% missing AND high-risk sector (healthcare, finance, HR tech):**
→ Escalate to client sponsor (not just initial contact)

```
Subject: Important: Additional context needed for compliance audit

Hi {sponsor_name},

I'm working with {contact_name} on the AI compliance audit for {company}.

Given that {company} operates in {high_risk_sector}, there are specific compliance requirements under the EU AI Act that require detailed documentation.

Currently we're missing {X}% of the data needed for a complete assessment. This could mean the report misses critical compliance gaps.

Could you help ensure we get the following details by {date}?

{list of gaps}

Happy to jump on a 15-min call if that's easier.

Best,
{auditor_name}
```

### State Machine

```
┌─────────────┐
│  GAPS_ID'd  │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│CHASE_EMAIL_1│
│  (send)     │
└──────┬──────┘
       │
       │ timeout (3 business days)
       │
       ▼
┌─────────────┐
│  RESPONSE?  │
└──────┬──────┘
       │
   ┌───┴───┐
   │       │
   ▼       ▼
┌─────┐ ┌──────────┐
│YES  │ │NO RESPONSE│
│     │ │          │
└──┬──┘ └────┬─────┘
   │         │
   │         ▼
   │    ┌──────────┐
   │    │PROCEED   │
   │    │WITH DATA │
   │    │FLAG GAPS │
   │    └────┬─────┘
   │         │
   ▼         │
┌────────────┘
│
▼
┌─────────────┐
│  WF-04      │
│  ANALYSIS   │
└─────────────┘
```

---

## WF-04: Audit Analysis & Scoring

**Trigger:** Complete or partial intake data received

**Owner:** Analysis Engine (automated)

### Sequential Module Execution

```
┌─────────────┐
│  MODULE 1   │
│  MATURITY   │
│  SCORING    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  MODULE 2   │
│  GAP        │
│  ANALYSIS   │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  MODULE 3   │
│  TOOL       │
│  EVALUATION │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  MODULE 4   │
│  COMPLIANCE │
│  RISK       │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  MODULE 5   │
│  PEOPLE &   │
│  ADOPTION   │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  MODULE 6   │
│  RECOMMENDA-│
│  TION ENGINE│
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  WF-05      │
│  REPORT GEN │
└─────────────┘
```

### Failure Mode Handling

| Module | Failure Mode | Fallback |
|--------|--------------|----------|
| Module 1 | Insufficient tool data | Score with available data, flag gaps, set confidence to "low" |
| Module 2 | Vague bottleneck descriptions | Flag for human review, provide best-estimate ranking |
| Module 3 | Unknown tool | Search for tool category + use case, classify and proceed |
| Module 4 | Contradictory country data | Assume most restrictive framework, flag for clarification |
| Module 5 | Missing adoption data | Use tool activation as proxy, or mark "data not provided" |
| Module 6 | Contradictory signals | Surface contradiction, present two scenarios |

### Output Contract

```json
{
  "audit_id": "uuid",
  "company_name": "string",
  "analysis_complete": true,
  "analysis_timestamp": "ISO8601",
  "module_1_maturity": {...},
  "module_2_gaps": {...},
  "module_3_tools": {...},
  "module_4_compliance": {...},
  "module_5_people": {...},
  "module_6_recommendations": {...}
}
```

---

## WF-05: Report Generation

**Trigger:** WF-04 analysis complete

**Owner:** Report Generator (automated)

### Two Report Formats

| Report | Pages | Audience | Use Case |
|--------|-------|----------|----------|
| Executive Summary | 2 | C-suite | Initial review, decision to proceed |
| Full Audit Report | 8-12 | Working team | Implementation reference |

### Quality Gate (Founder Review Required)

**Checklist:**
- [ ] Compliance obligations accurately stated (not overstated)
- [ ] EU AI Act high-risk use cases correctly identified
- [ ] Framework applicability correct (in-scope vs out-of-scope)
- [ ] No hallucinated tool assessments
- [ ] Dimension scores sum correctly
- [ ] Recommendations align with gaps
- [ ] Data gaps explicitly noted
- [ ] Confidence level appropriate
- [ ] All charts render correctly
- [ ] Booking link functional

### State Machine

```
┌─────────────┐
│  ANALYSIS   │
│  COMPLETE   │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  GENERATE   │
│  EXEC SUMMARY│
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  GENERATE   │
│  FULL REPORT│
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  FOUNDER    │
│  REVIEW     │
└──────┬──────┘
       │
   ┌───┴───┐
   │       │
   ▼       ▼
┌─────┐ ┌──────────┐
│PASS │ │REVISION  │
│     │ │REQUIRED  │
└──┬──┘ └────┬─────┘
   │         │
   │         ▼
   │    ┌──────────┐
   │    │EDIT &    │
   │    │RE-REVIEW │
   │    └────┬─────┘
   │         │
   ▼         │
┌────────────┘
│
▼
┌─────────────┐
│  WF-06      │
│  DELIVERY   │
└─────────────┘
```

---

## WF-06: Report Delivery & Debrief

**Trigger:** Report approved in WF-05

**Owner:** Audit Operations

### Delivery Sequence

```
Day 0: Email report with scheduling link
Day 3: Check if booked → if not, send reminder
Day 5: Second reminder
Day 8: Final "did anything resonate?" email
Day 11: Mark ghosted, schedule 30-day re-approach
```

### Email Template: Report Delivery

```
Subject: Your AI Compliance + Productivity Audit Report

Hi {first_name},

Your audit report is ready. Attached is the Executive Summary (2 pages), and you can access the Full Report here: {link}

KEY FINDINGS AT A GLANCE:
- Overall Score: {XX}/100 ({rating})
- Compliance Risk: {HIGH | MEDIUM | LOW}
- Estimated Waste: €{X}/month (€{Y}/year)
- Benchmark Position: {NN}th percentile vs {industry}

NEXT STEP:
Book your 45-minute debrief call using this link: {booking_link}

Deadline: {date = 5 business days from now}

On the call we'll:
1. Walk through findings (20 min)
2. Discuss which gaps are most urgent (10 min)
3. Review implementation options (10 min)
4. Book follow-up if needed (5 min)

Looking forward to walking through this together.

Best,
{auditor_name}
```

### Ghosted Recovery (30 days later)

```
Subject: Following up on your AI audit findings

Hi {first_name},

I wanted to circle back on the audit findings from last month.

Given what we found about {specific_high_risk_finding} and the EU AI Act deadline (August 2026), I thought it was worth checking in.

Has anything changed since the audit? Happy to jump on a quick call if you have questions.

Best,
{auditor_name}
```

### State Machine

```
┌─────────────┐
│  REPORT     │
│  DELIVERED  │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  DEBRIEF    │
│  BOOKED?    │
└──────┬──────┘
       │
   ┌───┴───┐
   │       │
   ▼       ▼
┌─────┐ ┌──────────┐
│YES  │ │NO (8 days)│
│     │ │          │
└──┬──┘ └────┬─────┘
   │         │
   │         ▼
   │    ┌──────────┐
   │    │GHOSTED   │
   │    │(30-day   │
   │    │re-approach)│
   │    └──────────┘
   │
   ▼
┌─────────────┐
│  DEBRIEF    │
│  CALL       │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  WF-07      │
│  UPSELL     │
└─────────────┘
```

---

## WF-07: Upsell — Change Management Engagement

**Trigger:** Debrief call shows client interest in acting

**Owner:** Sales/Account Executive

### Proposal Structure (Send within 24h of debrief)

```
PROPOSAL: AI Change Management Engagement

Client: {company_name}
Date: {date}
Prepared by: {auditor_name}

SCOPE:
Based on the audit findings, we recommend focusing on these 3 priority gaps:
1. {gap_1}
2. {gap_2}
3. {gap_3}

DELIVERABLES:
1. AI Training Program Design
   - Department-specific curricula
   - Training materials and exercises
   - Adoption metrics dashboard

2. Adoption Nudge System
   - Behavioral intervention design
   - Weekly nudge cadence
   - Success tracking

3. 90-Day Implementation Support
   - Weekly check-in calls
   - Tool implementation guidance
   - Compliance documentation support

TIMELINE:
Week 1-2: Training program design
Week 3-6: Nudge system deployment
Week 7-12: Implementation support

INVESTMENT:
{tier} engagement: €{X}/month
Total (3 months): €{Y}

Payment Terms: 50% upfront, 50% at day 45

NEXT STEPS:
1. Review proposal
2. Sign service agreement
3. Pay 50% deposit
4. Kickoff call scheduled
```

### Follow-up Cadence

| Day | Action |
|-----|--------|
| 0 | Proposal sent (within 24h of debrief) |
| 5 | First chase if no response |
| 10 | Mark closed_lost_upsell if no response, log objection reason |

### State Machine

```
┌─────────────┐
│  DEBRIEF    │
│  COMPLETE   │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  PROPOSAL   │
│  SENT       │
└──────┬──────┘
       │
       │ (5 days)
       │
       ▼
┌─────────────┐
│  RESPONSE?  │
└──────┬──────┘
       │
   ┌───┴───┐
   │       │
   ▼       ▼
┌─────┐ ┌──────────┐
│YES  │ │NO (day 5)│
│     │ │          │
└──┬──┘ └────┬─────┘
   │         │
   │         ▼
   │    ┌──────────┐
   │    │CHASE #1  │
   │    └────┬─────┘
   │         │
   │         │ (5 more days)
   │         │
   ▼         ▼
┌─────┐ ┌──────────┐
│SIGN │ │CLOSED_   │
│     │ │LOST_UPSELL│
└──┬──┘ └──────────┘
   │
   ▼
┌─────────────┐
│  WF-08      │
│  PAYMENT    │
└─────────────┘
```

---

## WF-08: Payment & Contract

**Trigger:** Proposal accepted in WF-07

**Owner:** Finance/Ops

### Contract Process

1. Send standard service agreement via DocuSign or PDF
2. Payment terms: 50% upfront, 50% on report delivery (for audit) or day 45 (for retainer)
3. Processors: Stripe (global), Razorpay (India-based clients)

### Timeout Rules

| Milestone | Timeout | Action |
|-----------|---------|--------|
| Contract unsigned | 3 business days | Send reminder |
| Contract unsigned (after reminder) | 3 more days | Escalate to client contact |
| Payment not received | Net-7 | Send invoice reminder |
| Payment not received (after reminder) | 7 more days | Pause work, escalate |

### State Machine

```
┌─────────────┐
│  PROPOSAL   │
│  ACCEPTED   │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  CONTRACT   │
│  SENT       │
└──────┬──────┘
       │
       │ (3 business days)
       │
       ▼
┌─────────────┐
│  SIGNED?    │
└──────┬──────┘
       │
   ┌───┴───┐
   │       │
   ▼       ▼
┌─────┐ ┌──────────┐
│YES  │ │NO        │
│     │ │          │
└──┬──┘ └────┬─────┘
   │         │
   │         ▼
   │    ┌──────────┐
   │    │REMINDER  │
   │    └────┬─────┘
   │         │
   │         │ (3 more days)
   │         │
   ▼         ▼
┌─────┐ ┌──────────┐
│     │ │ESCALATE  │
│     │ │TO CLIENT │
│     │ └──────────┘
│     │
│     ▼
│ ┌─────────────┐
│ │  INVOICE    │
│ │  SENT       │
│ └──────┬──────┘
│        │
│        │ (net-7)
│        │
│        ▼
│ ┌─────────────┐
│ │  PAID?      │
│ └──────┬──────┘
│        │
│    ┌───┴───┐
│    │       │
│    ▼       ▼
│ ┌─────┐ ┌──────────┐
│ │YES  │ │NO        │
│ └──┬──┘ └────┬─────┘
│    │         │
│    │         ▼
│    │    ┌──────────┐
│    │    │REMINDER  │
│    │    └────┬─────┘
│    │         │
│    │         │ (7 more days)
│    │         │
│    │         ▼
│    │    ┌──────────┐
│    │    │PAUSE WORK│
│    │    │ESCALATE  │
│    │    └──────────┘
│    │
│    ▼
│ ┌─────────────┐
│ │  KICKOFF    │
│ │  SCHEDULED  │
│ └─────────────┘
│
└─────────────────────────────────┘
```

---

## WF-09: Repeat Audit & Benchmark Tracking

**Trigger:** 90 days after audit delivery OR after change management engagement completes

**Owner:** Account Management

### Key Design Questions (To Be Resolved Before First Audit Hits 90 Days)

| Question | Recommended Answer |
|----------|-------------------|
| Is repeat audit discounted? | Yes, 30% discount for existing clients |
| What data carries over? | Company profile, tool inventory, baseline scores |
| What is re-collected? | Current adoption %, new tools, progress on recommendations |
| How is progress tracked? | Delta from baseline score, recommendation completion % |
| Benchmark DB: new row or update? | New row (preserves historical snapshot) |

### Repeat Audit Structure

```
REPEAT AUDIT FOCUS:
1. Score delta from baseline (overall + per dimension)
2. Recommendation completion status
3. New tools adopted / abandoned
4. Compliance progress (frameworks addressed)
5. New gaps identified

OUTPUT:
- Progress Report (4 pages)
- Updated benchmark data
- Next 90-day recommendations
```

### Email Template: Repeat Audit Offer

```
Subject: 90-day progress check-in

Hi {first_name},

It's been 90 days since your AI audit. I'd like to offer you a repeat audit at a 30% existing-client discount.

The repeat audit will:
- Measure progress against your baseline score
- Track recommendation completion
- Identify new gaps as you've scaled AI usage
- Update compliance status (especially EU AI Act)

Investment: €{X} (normally €{Y})
Timeline: 7 business days from data collection

Interested in seeing how far you've come?

Best,
{auditor_name}
```

---

## WF-10: Client Offboarding

**Trigger:** Client churns after audit or change management engagement

**Owner:** Account Management

### Minimum Actions

1. **Exit Survey (3 questions max)**
   - What worked well?
   - What didn't meet expectations?
   - Would you refer us? (Y/N + why/why not)

2. **Benchmark Data Capture**
   - Anonymize final maturity data
   - Add to benchmark database
   - Tag as "churned" for segmentation

3. **Re-outreach Schedule**
   - 6 months: "Would you like to see how you've progressed?"
   - 12 months: Final check-in

4. **Churn Documentation**
   - Reason: price / timing / fit / other
   - Product feedback flag (if applicable)

### Exit Survey Template

```
Subject: Quick feedback request

Hi {first_name},

As we wrap up our engagement, I'd appreciate 2 minutes of your time for 3 quick questions:

1. What worked well about the audit/change management program?

2. What didn't meet your expectations?

3. Would you refer us to a peer? (Y/N)
   If yes: Why?
   If no: Why not?

Your feedback directly shapes how we improve the product.

Best,
{auditor_name}
```

### State Machine

```
┌─────────────┐
│  CHURN      │
│  DETECTED   │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  EXIT       │
│  SURVEY     │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  BENCHMARK  │
│  DATA CAPTURE│
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  RE-OUTREACH│
│  SCHEDULED  │
│  (6 months) │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  CHURN      │
│  LOGGED     │
└─────────────┘
```

---

## Workflow Handoff Summary

| From | To | Trigger | Data Passed |
|------|-----|---------|-------------|
| WF-01 | WF-02 | ICP pass | Company info, contact details |
| WF-02 | WF-03 | Incomplete submission | Response data, gap list |
| WF-02 | WF-04 | Complete submission | Full response data |
| WF-03 | WF-04 | Chase complete | Response data (partial or full) |
| WF-04 | WF-05 | Analysis complete | Six-module output JSON |
| WF-05 | WF-06 | Report approved | Final PDF, booking link |
| WF-06 | WF-07 | Debrief complete | Interest level, priority gaps |
| WF-07 | WF-08 | Proposal accepted | Signed proposal, scope |
| WF-08 | WF-09 | Engagement complete | Final state, recommendation completion |
| WF-08 | WF-10 | Churn detected | Churn reason, final state |
