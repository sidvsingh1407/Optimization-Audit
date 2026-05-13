# WF-10: Client Offboarding Specification
## AI Productivity Intelligence System

**Version:** 1.0
**Created:** 2026-04-05
**Trigger:** Client churns after audit OR after change management engagement

---

## Purpose

Client offboarding serves four purposes:
1. **Capture Feedback:** Understand why client churned (product improvement)
2. **Preserve Benchmark Data:** Anonymized maturity data adds to database moat
3. **Maintain Relationship:** Re-approach opportunity at 6 and 12 months
4. **Document Learnings:** Product team flags patterns across churned clients

---

## Churn Classification

### Churn Point

| Stage | Churn Label | Implication |
|-------|-------------|-------------|
| Post-audit, no debrief booked | `churn_audit_no_debrief` | Low engagement, report didn't resonate |
| Post-debrief, no proposal sent | `churn_debrief_no_followup` | Scheduling friction or low urgency |
| Post-proposal, no signature | `churn_proposal_declined` | Price objection or timing issue |
| Mid-engagement (change management) | `churn_mid_engagement` | Delivery issue or priority shift |
| Post-engagement, no repeat audit | `churn_post_engagement` | Natural end, may re-engage later |

### Churn Reason Taxonomy

| Category | Codes |
|----------|-------|
| **Price** | `budget_constraints`, `roi_not_clear`, `cheaper_alternative` |
| **Timing** | `wrong_time`, `leadership_change`, `reorg_in_progress` |
| **Fit** | `too_early_stage`, `too_advanced`, `wrong_industry_focus` |
| **Delivery** | `report_quality`, `communication_issues`, `timeline_missed` |
| **Other** | `competitor`, `internal_solution`, `no_longer_relevant` |

---

## Minimum Offboarding Actions

### 1. Exit Survey (3 Questions Max)

**Delivery:** Email with Typeform/Tally link OR reply-to-email

**Questions:**

```
1. What worked well about the audit/change management program?
   [Open text]

2. What didn't meet your expectations?
   [Open text]

3. Would you refer us to a peer?
   ○ Yes — Why? [Open text]
   ○ No — Why not? [Open text]
```

**Incentive:** None (keep it short, respect their time)

**Timeout:** 7 days, then mark `survey_not_completed`

### 2. Benchmark Data Capture

**Action:** Anonymize and add final state to benchmark database

**Data Preserved:**
```json
{
  "audit_id": "uuid",
  "audit_date": "ISO8601",
  "industry": "string",
  "headcount_band": "enum",
  "maturity_overall": "integer",
  "dim_awareness": "integer",
  "dim_adoption": "integer",
  "dim_integration": "integer",
  "dim_governance": "integer",
  "dim_roi": "integer",
  "dim_ethical": "integer|null",
  "tool_count_active": "integer",
  "adoption_pct_reported": "integer",
  "compliance_euai": "enum",
  "compliance_dpdp": "enum",
  "compliance_gdpr": "enum",
  "compliance_iso42001": "enum",
  "top_gap_1": "text (anonymized)",
  "top_gap_2": "text (anonymized)",
  "top_gap_3": "text (anonymized)",
  "upsell_converted": "boolean",
  "churned": "boolean",
  "churn_stage": "string",
  "churn_reason_primary": "string",
  "churn_reason_secondary": "string|null"
}
```

**Data Removed:**
- Company name
- Contact name
- Contact email
- Specific tool names (replace with categories)
- Country-specific data (keep region only)

### 3. Re-Outreach Schedule

| Timeline | Message Type | Owner |
|----------|--------------|-------|
| 6 months | "See how you've progressed?" | BDR |
| 12 months | Final check-in | Account Management |

**6-Month Email Template:**
```
Subject: Quick check-in on AI progress

Hi {first_name},

It's been 6 months since we ran your AI audit. I was reviewing your file and noticed {specific_finding_from_audit}.

Have you made progress on any of the recommendations? I'd be happy to offer you a discounted repeat audit (30% off) to measure where you are now.

No pressure — just wanted to check in.

Best,
{auditor_name}
```

**12-Month Email Template:**
```
Subject: 1 year since your AI audit

Hi {first_name},

It's been a year since your AI audit with us. A lot has changed in AI compliance since then:
- EU AI Act is now in force (August 2026 deadline passed)
- ISO 42001 certification is becoming a procurement requirement
- New state AI laws in the US

If you're still thinking about AI strategy or compliance, I'd be happy to reconnect.

If not, no worries — just wanted to say hello.

Best,
{auditor_name}
```

### 4. Churn Documentation

**Internal Log Fields:**
```json
{
  "client_id": "uuid",
  "company_name": "string",
  "churn_date": "ISO8601",
  "churn_stage": "enum",
  "churn_reason_primary": "enum",
  "churn_reason_secondary": "enum|null",
  "churn_notes": "text",
  "product_feedback_flag": "boolean",
  "product_feedback_summary": "text|null",
  "referral_likelihood": "promoter|passive|detractor",
  "re_approach_6mo_scheduled": "boolean",
  "re_approach_12mo_scheduled": "boolean"
}
```

---

## Offboarding Workflow State Machine

```
┌─────────────┐
│  CHURN      │
│  DETECTED   │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  LOG CHURN  │
│  (classify) │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  EXIT       │
│  SURVEY     │
│  SENT       │
└──────┬──────┘
       │
       │ (7 days)
       │
       ▼
┌─────────────┐
│  SURVEY     │
│  COMPLETE?  │
└──────┬──────┘
       │
   ┌───┴───┐
   │       │
   ▼       ▼
┌─────┐ ┌──────────────┐
│YES  │ │NO (mark as   │
│     │ │not_completed)│
└──┬──┘ └──────┬───────┘
   │           │
   └─────┬─────┘
         │
         ▼
┌─────────────────┐
│  BENCHMARK DATA │
│  CAPTURE &      │
│  ANONYMIZE      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  RE-OUTREACH    │
│  SCHEDULED      │
│  (6mo + 12mo)   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  PRODUCT TEAM   │
│  NOTIFIED       │
│  (if feedback   │
│   flag set)     │
└─────────────────┘
```

---

## Product Feedback Loop

### When to Flag Product Team

| Churn Reason | Flag Product? | Summary Format |
|--------------|---------------|----------------|
| `report_quality` | Yes | "Client reported: {specific_issue}" |
| `communication_issues` | Yes | "Client reported: {specific_issue}" |
| `timeline_missed` | Yes | "Missed deadline: {date}, reason: {reason}" |
| `too_early_stage` | Maybe | Pattern detection (3+ similar churns) |
| `roi_not_clear` | Yes | "Value prop unclear: {client_quote}" |
| `cheaper_alternative` | Yes | "Competitor: {name}, price: {amount}" |

### Monthly Churn Review

**Attendees:** Product Lead, Sales Lead, Audit Operations

**Agenda:**
1. Review churn count by stage (5 min)
2. Review top 3 churn reasons (10 min)
3. Identify patterns (10 min)
4. Action items for product improvement (10 min)

**Metrics Tracked:**
- Churn rate by stage
- Churn rate by industry
- Churn rate by auditor
- Top 3 churn reasons (rolling 90 days)

---

## Benchmark Database Considerations

### Why Preserve Churned Client Data?

1. **Selection Bias Prevention:** If we only keep successful audits, benchmark becomes inflated
2. **Segmentation Value:** Churned clients may cluster in certain industries/stages
3. **Longitudinal Tracking:** Some churned clients return at 12+ months

### Churn Tag Usage

```sql
-- Compare churned vs. non-churned clients
SELECT 
  churned,
  AVG(maturity_overall) as avg_score,
  COUNT(*) as count
FROM benchmarks
GROUP BY churned;

-- Identify industries with high churn
SELECT 
  industry,
  SUM(CASE WHEN churned THEN 1 ELSE 0 END) * 1.0 / COUNT(*) as churn_rate
FROM benchmarks
GROUP BY industry
ORDER BY churn_rate DESC;
```

---

## Email Templates

### Template 1: Exit Survey Request

```
Subject: Quick feedback request (2 minutes)

Hi {first_name},

As we wrap up our engagement, I'd appreciate 2 minutes of your time for 3 quick questions.

Your feedback directly shapes how we improve the product for future clients.

Survey link: {typeform_link}

Alternatively, just reply to this email with:
1. What worked well?
2. What didn't meet expectations?
3. Would you refer us? (Y/N + why)

Best,
{auditor_name}
```

### Template 2: Offboarding Confirmation

```
Subject: Wrapping up our engagement

Hi {first_name},

I'm confirming that we've wrapped up your {audit | change management engagement}.

Key details:
- Final report delivered: {date}
- Engagement end date: {date}
- Benchmark data: Anonymized and stored (per your consent)

I've also scheduled a check-in for {6-month date} to see how you've progressed. No obligation — just a friendly touchpoint.

If you need anything before then (access to reports, introductions to partners, etc.), just let me know.

Best,
{auditor_name}
```

### Template 3: Internal Churn Notification

```
Subject: Churn logged: {company_name}

Team,

Churn has been logged for {company_name}:

- Stage: {churn_stage}
- Primary reason: {churn_reason_primary}
- Secondary reason: {churn_reason_secondary}
- Product feedback flag: {yes|no}
- Feedback summary: {summary}

Benchmark data has been anonymized and added to database.

Re-approach scheduled for {6-month date}.

Full details in CRM: {link}
```

---

## Compliance & Data Retention

### GDPR Considerations

| Data Type | Retention Period | Action |
|-----------|------------------|--------|
| Personal data (name, email) | 24 months from churn | Delete or anonymize |
| Company data (name, industry) | Indefinite (legitimate interest) | Keep in benchmark |
| Audit results (anonymized) | Indefinite (legitimate interest) | Keep in benchmark |
| Communication history | 24 months from churn | Archive, then delete |

### Right to Be Forgotten

If churned client requests data deletion:
1. Delete all personal data from CRM
2. Remove company name from benchmark (keep anonymized row)
3. Confirm deletion in writing
4. Document request in compliance log

---

## Validation Checklist

Before first churn event:

- [ ] Exit survey form created (Typeform/Tally)
- [ ] Benchmark anonymization script tested
- [ ] Re-outreach calendar invites created (6mo + 12mo)
- [ ] CRM churn fields configured
- [ ] Internal notification template ready
- [ ] Monthly churn review meeting scheduled (recurring)
- [ ] GDPR data retention policy documented
- [ ] Right to be forgotten process documented
