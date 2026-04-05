# WF-09: Repeat Audit & Benchmark Tracking Specification
## AI Productivity Intelligence System

**Version:** 1.0
**Created:** 2026-04-05
**Trigger:** 90 days after initial audit delivery OR after change management engagement completes

---

## Purpose

The repeat audit serves three purposes:
1. **Measure Progress:** Quantify improvement (or regression) since baseline
2. **Identify New Gaps:** Scaled AI usage creates new optimization opportunities
3. **Benchmark Contribution:** Each repeat audit adds longitudinal data to the benchmark database

---

## Key Design Decisions

| Question | Decision | Rationale |
|----------|----------|-----------|
| Is repeat audit discounted? | **Yes, 30% discount** | Rewards loyalty, encourages progress tracking |
| What data carries over? | Company profile, tool inventory, baseline scores | Avoids re-collecting static data |
| What is re-collected? | Current adoption %, new tools, progress on recommendations, compliance status | Measures change over time |
| How is progress tracked? | Delta from baseline score, recommendation completion % | Clear before/after comparison |
| Benchmark DB: new row or update? | **New row** (preserves historical snapshot) | Enables longitudinal analysis per company |

---

## Repeat Audit Data Model

### Data That Carries Over (Pre-Populated)

```json
{
  "company_profile": {
    "company_name": "string",
    "industry": "string",
    "headcount": "number",
    "countries": ["array"],
    "contact_name": "string",
    "contact_email": "string"
  },
  "baseline_audit": {
    "audit_id": "uuid",
    "audit_date": "ISO8601",
    "total_score": "number",
    "dimension_scores": {...},
    "top_recommendations": ["array"]
  }
}
```

### Data Re-Collected

```json
{
  "current_state": {
    "tools_in_use": "array (updated)",
    "adoption_pct": "number (current)",
    "departments_using_ai": "number (current)",
    "monthly_spend": "string (updated)",
    "abandoned_tools": "array (new since baseline)"
  },
  "recommendation_progress": {
    "recommendation_id": {
      "status": "complete | in_progress | not_started | abandoned",
      "completion_pct": "number (0-100)",
      "notes": "string"
    }
  },
  "compliance_progress": {
    "eu_ai_act": "status update",
    "gdpr": "status update",
    "dpdp": "status update",
    "iso_42001": "status update",
    "nist_ai_rmf": "status update"
  },
  "new_gaps": {
    "description": "Gaps identified at 90 days that weren't present at baseline"
  }
}
```

---

## Repeat Audit Scoring

### Score Delta Calculation

```python
def calculate_score_delta(baseline_scores, current_scores):
    """Calculate score changes across all dimensions."""
    delta = {}
    
    dimensions = ['awareness', 'adoption', 'integration', 'governance', 'roi', 'ethical']
    
    for dim in dimensions:
        baseline = baseline_scores.get(dim, 0) or 0
        current = current_scores.get(dim, 0) or 0
        delta[dim] = {
            'baseline': baseline,
            'current': current,
            'delta': current - baseline,
            'direction': 'improving' if current > baseline else ('stable' if current == baseline else 'declining')
        }
    
    # Overall delta
    baseline_total = sum(baseline_scores.values())
    current_total = sum(current_scores.values())
    delta['overall'] = {
        'baseline': baseline_total,
        'current': current_total,
        'delta': current_total - baseline_total,
        'direction': 'improving' if current_total > baseline_total else ('stable' if current_total == current_total else 'declining')
    }
    
    return delta
```

### Recommendation Completion Tracking

| Status | Definition |
|--------|------------|
| **Complete** | Recommendation fully implemented |
| **In Progress** | Work started, not yet complete |
| **Not Started** | No action taken yet |
| **Abandoned** | Work started but stopped |

**Completion Score:** (Complete count / Total recommendations) × 100

---

## Repeat Audit Form Structure

### Section 1: Baseline Review (Read-Only)

```
YOUR BASELINE AUDIT ({baseline_date}):
- Overall Score: {XX}/100
- Top 3 Recommendations:
  1. {recommendation_1}
  2. {recommendation_2}
  3. {recommendation_3}
```

### Section 2: Current State Assessment

**Q2.1: Current AI Tools in Use**
- Type: Long text (repeater)
- Pre-populated: Baseline tools list
- Instruction: "Update this list - remove tools you no longer use, add new tools"

**Q2.2: Current Adoption Rate**
- Type: Dropdown
- Options: 75%+ / 50-74% / 25-49% / 10-24% / <10% / 0%
- Comparison shown: "Baseline: {baseline_pct}%"

**Q2.3: New Tools Trialled (Then Abandoned)**
- Type: Long text
- Instruction: "List any tools you tried since the baseline audit but stopped using"

**Q2.4: Current Monthly AI Spend**
- Type: Dropdown
- Options: <€500 / €500-€2K / €2K-€10K / €10K+
- Comparison shown: "Baseline: {baseline_spend}"

### Section 3: Recommendation Progress

For each baseline recommendation:

```
RECOMMENDATION 1: {recommendation_text}
Status: ○ Complete ○ In Progress ○ Not Started ○ Abandoned
Completion: {slider 0-100%} (if In Progress)
Notes: {text field}
```

### Section 4: Compliance Progress

**Q4.1: EU AI Act Status**
- Type: Dropdown
- Options:
  - Conformity assessment completed
  - Assessment in progress
  - Legal counsel engaged
  - Aware but not started
  - No action taken
- Comparison shown: "Baseline: {baseline_status}"

**Q4.2: ISO 42001 Status**
- Type: Dropdown
- Options:
  - Certified
  - In progress (implementation started)
  - Gap analysis completed
  - Aware but not started
  - No action taken

**Q4.3: New Compliance Obligations**
- Type: Multi-select
- Options:
  - UK AI Safety Framework
  - US State AI Laws (specify states)
  - Canada AIDA
  - China AI Regulations
  - None of the above

### Section 5: New Gaps & Challenges

**Q5.1: New Bottlenecks as AI Usage Scaled**
- Type: Long text
- Instruction: "As you've used AI more, what new challenges have emerged?"

**Q5.2: Unexpected AI Use Cases**
- Type: Long text
- Instruction: "Have any departments found unexpected ways to use AI since the baseline?"

### Section 6: Goals for Next 90 Days

**Q6.1: Target Score for Next Audit**
- Type: Number input
- Pre-populated: Baseline score + 10 points (suggested)
- Instruction: "What's your target overall score?"

**Q6.2: Priority Focus Areas**
- Type: Multi-select
- Options:
  - Increase adoption rate
  - Deepen workflow integration
  - Improve governance/compliance
  - Better ROI measurement
  - Tool consolidation
  - Training program expansion

---

## Repeat Audit Output

### Progress Report Structure (4 Pages)

**Page 1: Score Delta Visualization**

```
┌─────────────────────────────────────────────────────────┐
│              90-DAY PROGRESS REPORT                     │
│                  {company_name}                         │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  SCORE DELTA                                            │
│                                                         │
│  Baseline:  {XX}/100  ({baseline_date})                 │
│  Current:   {YY}/100  ({current_date})                  │
│  ─────────────────────                                  │
│  Delta:     {+/–Z} points                               │
│                                                         │
│  ┌────────────────────────────────────────────┐        │
│  │  [Before/After Bar Chart by Dimension]     │        │
│  │                                             │        │
│  │  Awareness   ████░░░░░░ → █████░░░░░       │        │
│  │  Adoption    ███░░░░░░░ → █████░░░░░       │        │
│  │  Integration ██░░░░░░░░ → ████░░░░░░       │        │
│  │  Governance  ████░░░░░░ → ██████░░░░       │        │
│  │  ROI         ███░░░░░░░ → ████░░░░░░       │        │
│  └────────────────────────────────────────────┘        │
│                                                         │
│  Rating Change: {baseline_rating} → {current_rating}   │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

**Page 2: Recommendation Completion**

```
┌─────────────────────────────────────────────────────────┐
│  RECOMMENDATION PROGRESS                                │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Completion Rate: {X}% ({complete_count}/{total_count})│
│                                                         │
│  ✅ COMPLETE                                            │
│  - {Recommendation 1}                                   │
│  - {Recommendation 2}                                   │
│                                                         │
│  🔄 IN PROGRESS                                         │
│  - {Recommendation 3} ({X}% complete)                   │
│  - {Recommendation 4} ({Y}% complete)                   │
│                                                         │
│  ⏸️  NOT STARTED                                         │
│  - {Recommendation 5}                                   │
│  - {Recommendation 6}                                   │
│                                                         │
│  ❌ ABANDONED                                           │
│  - {Recommendation 7}                                   │
│    Reason: {abandonment_reason}                         │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

**Page 3: Compliance Progress & New Gaps**

```
┌─────────────────────────────────────────────────────────┐
│  COMPLIANCE PROGRESS                                    │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Framework      │ Baseline    │ Current     │ Delta    │
│  ─────────────────────────────────────────────────────  │
│  EU AI Act      │ not_started │ in_progress │ +1 stage │
│  GDPR           │ partial     │ compliant   │ +1 stage │
│  DPDP           │ out_of_scope│ out_of_scope│ —        │
│  ISO 42001      │ not_started │ not_started │ —        │
│  NIST AI RMF    │ not_started │ aware       │ +1 stage │
│                                                         │
├─────────────────────────────────────────────────────────┤
│  NEW GAPS IDENTIFIED                                    │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  1. {New gap description}                               │
│     Why emerged: {reason - e.g., "New tool created gap"}│
│     Priority: {high | medium | low}                     │
│                                                         │
│  2. {New gap description}                               │
│     {Same structure}                                    │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

**Page 4: Next 90-Day Recommendations**

```
┌─────────────────────────────────────────────────────────┐
│  NEXT 90-DAY ACTION PLAN                                │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  TARGET SCORE: {XX}/100 (current: {YY}/100)            │
│                                                         │
│  PRIORITY RECOMMENDATIONS                               │
│                                                         │
│  1. {Recommendation}                                    │
│     Effort: {low | medium | high}                       │
│     Impact: {low | medium | high}                       │
│     Owner: {role}                                       │
│     Timeline: {weeks}                                   │
│                                                         │
│  2. {Recommendation}                                    │
│     {Same structure}                                    │
│                                                         │
│  3. {Recommendation}                                    │
│     {Same structure}                                    │
│                                                         │
│  SUCCESS METRICS (180 days from baseline)               │
│  - Overall score: {target}                              │
│  - Recommendation completion: {target}%                 │
│  - Adoption rate: {target}%                             │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## Benchmark Database Contribution

### Schema for Repeat Audit Row

| Field | Value |
|-------|-------|
| `audit_id` | New UUID (different from baseline) |
| `audit_date` | Current audit date |
| `is_repeat_audit` | `true` |
| `baseline_audit_id` | Reference to initial audit |
| `days_since_baseline` | Integer |
| `score_delta` | Integer (+/–) |
| `recommendation_completion_pct` | Integer (0-100) |
| All other fields | Same as baseline schema |

### Longitudinal Analysis Queries

```sql
-- Average improvement at 90 days
SELECT AVG(score_delta) as avg_improvement
FROM benchmarks
WHERE is_repeat_audit = true AND days_since_baseline = 90;

-- Improvement by industry
SELECT industry, AVG(score_delta) as avg_improvement
FROM benchmarks
WHERE is_repeat_audit = true
GROUP BY industry;

-- Recommendation completion correlation with score improvement
SELECT recommendation_completion_pct, score_delta
FROM benchmarks
WHERE is_repeat_audit = true;
```

---

## Pricing

| Engagement | Initial Audit Price | Repeat Audit Price (30% off) |
|------------|--------------------|------------------------------|
| Small (50-100 emp) | €2,000-€3,500 | €1,400-€2,450 |
| Medium (100-250 emp) | €3,500-€5,500 | €2,450-€3,850 |
| Large (250-500 emp) | €5,500-€8,000 | €3,850-€5,600 |

**Change Management Completion Discount:** If client completed 90-day change management engagement, repeat audit is **included** in final month deliverable.

---

## Email Templates

### Template 1: 90-Day Check-In (Automated)

```
Subject: 90-day progress check-in

Hi {first_name},

It's been 90 days since your AI audit on {baseline_date}.

I'd like to offer you a repeat audit at a 30% existing-client discount (€{discounted_price} vs. €{original_price}).

The repeat audit will:
✓ Measure progress against your baseline score of {baseline_score}/100
✓ Track which of the 6 recommendations you've completed
✓ Identify new gaps as you've scaled AI usage
✓ Update your EU AI Act compliance status

Timeline: 7 business days from data collection

Interested in seeing how far you've come?

Best,
{auditor_name}
```

### Template 2: Change Management Completion (Included Audit)

```
Subject: Your 90-day progress audit

Hi {first_name},

As we wrap up our 90-day change management engagement, I want to measure the progress you've made.

I'll be sending over a brief progress audit form (15 minutes to complete). This will:
- Measure your score delta from baseline
- Document recommendation completion
- Identify new gaps for the next 90 days

This progress audit is included as part of your engagement.

I'll send the form by {date}. Looking forward to seeing the progress you've made!

Best,
{auditor_name}
```

---

## Validation Checklist

Before running first repeat audit:

- [ ] Baseline audit data accessible by audit_id
- [ ] Pre-population logic working for carry-over fields
- [ ] Score delta calculation tested
- [ ] Recommendation progress tracking implemented
- [ ] Progress report template built
- [ ] Benchmark database schema updated for repeat audits
- [ ] Pricing discount applied correctly
- [ ] Email automation configured for 90-day trigger
