# AI Productivity Intelligence System
## Scoring Rubric v1.0

**Total Score: 0-100** (5 dimensions × 20 points each)

---

## Dimension 1: AWARENESS (20 points)

*Measures: Leadership understanding of AI capabilities, limitations, and strategic implications*

| Question | Answer Options | Points |
|----------|----------------|--------|
| **1.1: How would you rate leadership's understanding of AI?** | a) Very high - can articulate specific use cases<br>b) High - general understanding<br>c) Moderate - aware but vague<br>d) Low - minimal understanding<br>e) None - no AI awareness | a=20, b=15, c=10, d=5, e=0 |
| **1.2: Does your company have an AI strategy document?** | a) Yes, documented and communicated<br>b) Yes, but not formally documented<br>c) In progress<br>d) No, but planning to<br>e) No | a=20, b=15, c=10, d=5, e=0 |
| **1.3: How are AI decisions made?** | a) Dedicated AI committee + executive sponsor<br>b) Executive-led with team input<br>c) Ad-hoc by department heads<br>d) Individual employees decide<br>e) No coordination | a=20, b=15, c=10, d=5, e=0 |

**Awareness Score = Average of 1.1, 1.2, 1.3** (rounded to nearest integer)

---

## Dimension 2: ADOPTION (20 points)

*Measures: Breadth and depth of AI tool usage across the organization*

| Question | Answer Options | Points |
|----------|----------------|--------|
| **2.1: What % of employees actively use AI tools?** | a) 75%+<br>b) 50-74%<br>c) 25-49%<br>d) 10-24%<br>e) <10% | a=20, b=15, c=10, d=5, e=0 |
| **2.2: How many AI tools are in active use?** | a) 6+ tools (diverse stack)<br>b) 4-5 tools<br>c) 2-3 tools<br>d) 1 tool<br>e) None | a=20, b=15, c=10, d=5, e=0 |
| **2.3: How frequently do employees use AI?** | a) Daily<br>b) Several times/week<br>c) Weekly<br>d) Monthly<br>e) Rarely/Never | a=20, b=15, c=10, d=5, e=0 |

**Adoption Score = Average of 2.1, 2.2, 2.3** (rounded to nearest integer)

---

## Dimension 3: INTEGRATION (20 points)

*Measures: How deeply AI is embedded in workflows and systems*

| Question | Answer Options | Points |
|----------|----------------|--------|
| **3.1: How is AI integrated into your tech stack?** | a) Deeply integrated (API, custom workflows)<br>b) Moderate integration (some automation)<br>c) Light integration (standalone tools)<br>d) Minimal (copy/paste usage)<br>e) No integration | a=20, b=15, c=10, d=5, e=0 |
| **3.2: Do you have AI in core business systems?** | a) Yes - CRM, ERP, or core platform<br>b) Yes - some systems<br>c) Planning integration<br>d) No, but considering<br>e) No | a=20, b=15, c=10, d=5, e=0 |
| **3.3: How are AI workflows documented?** | a) Fully documented + training provided<br>b) Documented but informal training<br>c) Partial documentation<br>d) Ad-hoc knowledge sharing<br>e) No documentation | a=20, b=15, c=10, d=5, e=0 |

**Integration Score = Average of 3.1, 3.2, 3.3** (rounded to nearest integer)

---

## Dimension 4: GOVERNANCE (20 points)

*Measures: Policies, compliance, risk management around AI*

| Question | Answer Options | Points |
|----------|----------------|--------|
| **4.1: Do you have AI usage policies?** | a) Comprehensive policy + enforcement<br>b) Basic guidelines<br>c) Draft policy<br>d) Informal guidelines<br>e) No policy | a=20, b=15, c=10, d=5, e=0 |
| **4.2: How do you handle data privacy with AI?** | a) Formal review + approved tools only<br>b) Guidelines provided<br>c) Ad-hoc review<br>d) Employee discretion<br>e) No oversight | a=20, b=15, c=10, d=5, e=0 |
| **4.3: EU AI Act readiness?** | a) Fully assessed + compliant<br>b) Assessment in progress<br>c) Aware but not started<br>d) Heard of it, no action<br>e) Unaware | a=20, b=15, c=10, d=5, e=0 |

**Governance Score = Average of 4.1, 4.2, 4.3** (rounded to nearest integer)

**COMPLIANCE RISK FLAG:** Set to TRUE if:
- 4.1 = d or e (no policy or informal only), OR
- 4.2 = d or e (employee discretion or no oversight), OR
- 4.3 = d or e (unaware or no action on EU AI Act)

---

## Dimension 5: ROI (20 points)

*Measures: Measured impact and business value from AI*

| Question | Answer Options | Points |
|----------|----------------|--------|
| **5.1: Do you measure AI ROI?** | a) Yes, formal metrics + regular review<br>b) Yes, informal tracking<br>c) Basic measurement<br>d) No, but planning to<br>e) No measurement | a=20, b=15, c=10, d=5, e=0 |
| **5.2: Estimated time savings from AI?** | a) 25%+ across knowledge work<br>b) 15-24%<br>c) 5-14%<br>d) <5%<br>e) No measurable savings | a=20, b=15, c=10, d=5, e=0 |
| **5.3: How would you rate AI's business impact?** | a) Transformational<br>b) Significant<br>c) Moderate<br>d) Minimal<br>e) Negative/No impact | a=20, b=15, c=10, d=5, e=0 |

**ROI Score = Average of 5.1, 5.2, 5.3** (rounded to nearest integer)

---

## Edge Cases & Missing Data Handling

### Missing Responses
- If 1 question missing in a dimension: Average the remaining 2 questions, multiply by 1.5
- If 2+ questions missing in a dimension: Dimension score = 0, flag in report

### Contradictory Responses
- If adoption claims "75%+" but frequency is "Rarely/Never": Use lower score
- If integration claims "Deep" but tools = "None": Flag for manual review

### Score Boundaries
- Minimum score: 0 (all dimensions can floor at 0)
- Maximum score: 100 (all dimensions cap at 20)
- No partial points within questions (only use defined point values)

### Rounding
- Dimension averages rounded to nearest integer
- Total score = sum of 5 dimension scores (no further rounding)

---

## Score Interpretation

| Total Score | Rating | Description |
|-------------|--------|-------------|
| 80-100 | AI Mature | Leading edge, optimization focus |
| 60-79 | AI Adopting | Solid foundation, improvement opportunities |
| 40-59 | AI Emerging | Basic usage, significant gaps |
| 20-39 | AI Initial | Early stages, foundational work needed |
| 0-19 | AI Nascent | Minimal to no AI usage |

---

## Compliance Risk Flag

**Displayed prominently in report if TRUE**

Triggers:
- No AI policy OR only informal guidelines
- No data privacy oversight
- EU AI Act: unaware or no action

**Sales implication:** "You scored X, but you have a compliance risk flag that needs addressing before August 2026."
