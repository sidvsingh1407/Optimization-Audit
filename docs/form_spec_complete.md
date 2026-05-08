# Complete Form Specification — WF-02
## AI Compliance + Productivity Audit Intake

**Platform Recommendation:** Tally.so (supports partial saves, conditional logic, webhook integrations)
**Fallback:** Google Forms (no partial saves, but universally accessible)

---

## Form Settings

| Setting | Value |
|---------|-------|
| Collect email addresses | Yes |
| Allow edit after submit | Yes (Tally only) |
| Show progress bar | Yes |
| Confirmation message | "Thank you! Your AI audit submission has been received. We'll contact you within 48 hours to schedule your debrief." |
| Webhook URL | [Orchestrator endpoint - TBD] |
| Export destination | Google Sheets + Airtable |

---

## Section 1: Company Context

### Q1.1: Company Name
- **Type:** Short text
- **Required:** Yes
- **Validation:** Min 2 characters

### Q1.2: Industry
- **Type:** Dropdown
- **Required:** Yes
- **Options:**
  - Marketing/Advertising
  - SaaS/Technology
  - Professional Services (Consulting, Legal, Accounting)
  - Healthcare/Medical
  - Finance/FinTech/Banking
  - E-commerce/Retail
  - Manufacturing/Industrial
  - Education/EdTech
  - Media/Entertainment
  - Hospitality/Travel
  - Real Estate/Construction
  - Transportation/Logistics
  - Energy/Utilities
  - Telecommunications
  - Government/Public Sector
  - Non-profit/NGO
  - Other

### Q1.3: Total Headcount
- **Type:** Dropdown
- **Required:** Yes
- **Options:**
  - 1-9 (Note: Below ICP threshold)
  - 10-49 (Note: Below ICP threshold)
  - 50-99
  - 100-249
  - 250-499
  - 500-999
  - 1000+

### Q1.4: Revenue Range (Optional)
- **Type:** Dropdown
- **Required:** No
- **Options:**
  - < €500K
  - €500K-€2M
  - €2M-€10M
  - €10M-€50M
  - €50M+
  - Prefer not to say

### Q1.5: Primary Markets / Countries of Operation
- **Type:** Multi-select with search
- **Required:** Yes
- **Options:** Searchable country list
- **Note:** Critical for compliance scoping

### Q1.6: Primary Contact Name
- **Type:** Short text
- **Required:** Yes

### Q1.7: Primary Contact Email
- **Type:** Email
- **Required:** Yes

### Q1.8: Job Title
- **Type:** Short text
- **Required:** Yes

---

## Section 2: Current AI Tool Stack

### Q2.1: List All AI Tools in Active Use
- **Type:** Long text (repeater field if Tally supports)
- **Required:** Yes
- **Format:** Tool name | Department | Use case
- **Placeholder:** "e.g., ChatGPT Enterprise | Marketing | Content drafting; GitHub Copilot | Engineering | Code completion"
- **Follow-up:** "How many departments use AI tools?"
  - Options: 1 / 2 / 3 / 4+ / Company-wide

### Q2.2: Tools Trialled But Abandoned
- **Type:** Long text
- **Required:** No
- **Placeholder:** "List any AI tools you tried but stopped using, and why"

### Q2.3: Estimated Monthly AI Spend
- **Type:** Dropdown
- **Required:** Yes
- **Options:**
  - < €500/month
  - €500-€2,000/month
  - €2,000-€10,000/month
  - €10,000+/month
  - Don't track AI spend separately

### Q2.4: Time Saved Per Tool (Self-Reported)
- **Type:** Long text
- **Required:** No
- **Placeholder:** "For each tool, estimate hours/week saved per active user"

### Q2.5: Can You Justify Cost Per Tool by Output?
- **Type:** Dropdown
- **Required:** Yes
- **Options:**
  - Yes, we track ROI per tool
  - Partially, we have a general sense
  - No, we don't track tool-level ROI
  - Not applicable (free tools only)

---

## Section 3: Workflow & Process

### Q3.1: Top 5 Repetitive Tasks Across Departments
- **Type:** Long text
- **Required:** Yes
- **Placeholder:** "List the most time-consuming repetitive tasks that could potentially be automated"

### Q3.2: Current Bottlenecks Where AI Could Help But Isn't
- **Type:** Long text
- **Required:** No
- **Placeholder:** "Where do you wish you had AI capabilities but don't currently?"

### Q3.3: Are AI Tools Integrated Into Core Workflows or Siloed?
- **Type:** Dropdown
- **Required:** Yes
- **Options:**
  - Deeply integrated (API connections, embedded in daily workflows)
  - Moderately integrated (some automated workflows)
  - Lightly integrated (standalone tools, manual copy/paste)
  - Not integrated (ad-hoc usage)

### Q3.4: Do AI Outputs Feed Into Downstream Processes Automatically?
- **Type:** Dropdown
- **Required:** Yes
- **Options:**
  - Yes, fully automated (AI output triggers next steps)
  - Partially (some workflows automated)
  - No, manual handoff required
  - Not applicable

### Q3.5: Data Flow Between AI Tools and Existing Systems
- **Type:** Dropdown
- **Required:** Yes
- **Options:**
  - Yes, bidirectional sync (CRM ↔ AI, ERP ↔ AI, etc.)
  - One-way export (AI → systems)
  - One-way import (systems → AI)
  - No integration, manual transfer only

---

## Section 4: People & Adoption

### Q4.1: Are Employees Aware AI Tools Are Available to Them?
- **Type:** Dropdown
- **Required:** Yes
- **Options:**
  - Yes, formally communicated with training
  - Yes, informally known
  - Some employees aware, others not
  - No, no formal communication

### Q4.2: Percentage of Employees Actively Using ≥1 AI Tool Weekly
- **Type:** Dropdown
- **Required:** Yes
- **Options:**
  - 75%+
  - 50-74%
  - 25-49%
  - 10-24%
  - <10%
  - 0%

### Q4.3: Training Received
- **Type:** Dropdown
- **Required:** Yes
- **Options:**
  - Formal training program (structured curriculum)
  - Informal training (peer learning, lunch & learns)
  - Self-directed only (no company training)
  - No training provided

### Q4.4: Resistance or Blockers Reported by Employees
- **Type:** Multi-select
- **Required:** No
- **Options:**
  - Don't understand how AI helps their role
  - Don't trust AI outputs
  - Don't have time to learn new tools
  - Concerned about job displacement
  - Concerned about data privacy
  - Tools don't fit existing workflows
  - No resistance reported
  - Other (specify)

---

## Section 5: Compliance Context

### Q5.1: Does the Company Operate In or Serve Customers In:
- **Type:** Multi-select
- **Required:** Yes
- **Options:**
  - European Union
  - United Kingdom
  - United States (specify states if possible)
  - India
  - Canada
  - China
  - None of the above

### Q5.2: Does the Company Use AI In:
- **Type:** Multi-select
- **Required:** Yes
- **Options:**
  - Hiring / CV screening / candidate scoring
  - Credit scoring / loan decisioning
  - Healthcare diagnosis support
  - Employee monitoring / performance evaluation
  - Educational assessment
  - Biometric identification
  - Customer recommendation engines
  - Content moderation
  - None of the above
  - Other (specify)

### Q5.3: Has the Company Completed Any AI Compliance Assessment Previously?
- **Type:** Dropdown
- **Required:** Yes
- **Options:**
  - Yes, comprehensive assessment (specify framework)
  - Yes, partial/internal review
  - No, but aware of requirements
  - No, unaware of requirements

### Q5.4: Does the Company Have an AI Usage Policy?
- **Type:** Dropdown
- **Required:** Yes
- **Options:**
  - Yes, documented and communicated to all employees
  - Yes, but not formally documented
  - In progress / draft
  - No, but planning to create one
  - No

### Q5.5: Data Privacy Implications Documented for AI Tools?
- **Type:** Dropdown
- **Required:** Yes
- **Options:**
  - Yes, formal DPIA completed for all AI tools
  - Yes, informal assessment
  - In progress
  - No, not documented
  - Don't know what DPIA is

---

## Section 6: Goals & Concerns

### Q6.1: What Would Productivity Improvement Look Like in 6 Months?
- **Type:** Long text
- **Required:** Yes
- **Placeholder:** "Describe your ideal outcome from this audit"

### Q6.2: Biggest Concern About AI Adoption
- **Type:** Long text
- **Required:** Yes

### Q6.3: Have You Heard Of:
- **Type:** Multi-select with awareness level
- **Required:** No
- **Options:**
  - EU AI Act (effective August 2026)
  - ISO 42001 (AI management system certification)
  - NIST AI Risk Management Framework
  - India DPDP Act 2023
  - Canada AIDA (Bill C-27)
  - None of the above

---

## Section 7: Consent & Benchmarking

### Q7.1: May We Contact You to Discuss Your Audit Results?
- **Type:** Dropdown
- **Required:** Yes
- **Options:**
  - Yes, happy to discuss
  - Prefer to receive report only
  - Contact only if there are critical findings

### Q7.2: Allow Anonymized Data for Benchmarking?
- **Type:** Checkbox
- **Required:** No
- **Text:** "I consent to having my company's anonymized audit data used for industry benchmarking. No company name or contact information will be shared."

---

## Conditional Logic

| Trigger | Action |
|---------|--------|
| Q1.3 = "1-9" or "10-49" | Show warning: "Our audit is optimized for companies with 50+ employees. Continue anyway?" |
| Q2.1 = "None" or empty | Skip Sections 3-4, show AI readiness assessment path |
| Q5.2 contains "Hiring / CV screening" OR "Credit scoring" OR "Healthcare" | Flag for EU AI Act high-risk assessment, show info box about August 2026 deadline |
| Q5.1 contains "India" | Show DPDP Act info box |
| Q5.1 contains "European Union" | Show EU AI Act info box |
| Q5.4 = "No" or "In progress" | Flag governance gap in report |

---

## Form → Score Mapping Reference

| Question | Dimension | Criterion | Points Available |
|----------|-----------|-----------|------------------|
| Q5.4 | Governance | AI usage policy exists | 0-3 |
| Q5.5 | Governance | GDPR/data privacy documented | 0-3 |
| Q5.1 + Q5.2 | Governance | EU AI Act assessment | 0-4 |
| Q5.1 contains India | Governance | DPDP compliance | 0-3 |
| Q5.3 | Governance | Risk management framework | 0-4 |
| Q5.2 high-risk use | Governance | Ethical AI review | 0-3 |
| Q4.1 | Awareness | Employee awareness | 0-5 |
| Q2.3 | Awareness | Spend tracked | 0-5 |
| Q6.1 | Awareness | AI in planning | 0-5 |
| Q4.2 | Adoption | % employees using AI | 0-8 |
| Q2.1 dept count | Adoption | ≥3 departments | 0-6 |
| Q2.2 | Adoption | Abandoned tools <30% | 0-6 |
| Q3.3 | Integration | Core workflow integration | 0-8 |
| Q3.4 | Integration | Downstream automation | 0-7 |
| Q3.5 | Integration | Data flow between systems | 0-5 |
| Q2.4 | ROI | Time saved quantified | 0-7 |
| Q6.1 | ROI | Investment tracked | 0-7 |
| Q2.5 | ROI | Cost justified | 0-6 |

---

## Validation Rules

| Field | Validation |
|-------|------------|
| Q1.7 (Email) | Valid email format |
| Q2.1 | Cannot be empty unless "None" selected |
| Q4.2 | Must be consistent with Q2.1 (if tools = none, adoption = 0%) |
| Q5.1 | At least one region must be selected |

---

## Export Schema (Google Sheets Columns)

```
A: submission_id (UUID)
B: submitted_at (ISO 8601)
C: q1_1_company_name
D: q1_2_industry
E: q1_3_headcount
F: q1_4_revenue (optional)
G: q1_5_countries (array)
H: q1_6_contact_name
I: q1_7_contact_email
J: q1_8_job_title
K: q2_1_tools_list
L: q2_1_dept_count
M: q2_2_abandoned_tools
N: q2_3_monthly_spend
O: q2_4_time_saved
P: q2_5_cost_justified
Q: q3_1_top_tasks
R: q3_2_bottlenecks
S: q3_3_workflow_integration
T: q3_4_downstream_auto
U: q3_5_data_flow
V: q4_1_employee_awareness
W: q4_2_adoption_pct
X: q4_3_training_status
Y: q4_4_resistance_blockers
Z: q5_1_countries_operation
AA: q5_2_high_risk_uses
AB: q5_3_prev_compliance_review
AC: q5_4_ai_policy
AD: q5_5_dpia
AE: q6_1_goals
AF: q6_2_concerns
AG: q6_3_framework_awareness
AH: q7_1_contact_preference
AI: q7_2_benchmark_opt_in
AJ: completeness_score (0-100, auto-calculated)
AK: compliance_flag_euai (auto-calculated)
AL: compliance_flag_dpdp (auto-calculated)
AM: compliance_flag_gdpr (auto-calculated)
```

---

## Completeness Gate Logic

```python
def calculate_completeness(responses):
    mandatory_fields = [
        'q1_1', 'q1_2', 'q1_3', 'q1_5', 'q1_6', 'q1_7', 'q1_8',
        'q2_1', 'q2_3', 'q2_5',
        'q3_1', 'q3_3', 'q3_4', 'q3_5',
        'q4_1', 'q4_2', 'q4_3',
        'q5_1', 'q5_2', 'q5_4', 'q5_5',
        'q6_1', 'q6_2',
        'q7_1'
    ]
    optional_fields = ['q1_4', 'q2_2', 'q2_4', 'q3_2', 'q4_4', 'q5_3', 'q6_3', 'q7_2']
    
    completed_mandatory = sum(1 for f in mandatory_fields if responses.get(f))
    completeness_pct = (completed_mandatory / len(mandatory_fields)) * 100
    
    if completeness_pct < 70:
        return "INCOMPLETE", completeness_pct
    elif completeness_pct < 100:
        return "PARTIAL", completeness_pct
    else:
        return "COMPLETE", completeness_pct
```

---

## Info Box Copy

### EU AI Act Info Box (triggered by Q5.1 = EU or Q5.2 = high-risk)
> **Important:** The EU AI Act is effective August 2026. Companies using AI for hiring, credit decisioning, healthcare, or employee monitoring face mandatory conformity assessments. Non-compliance penalties: up to €35M or 7% global revenue. Your audit report will include a detailed EU AI Act exposure assessment.

### DPDP Act Info Box (triggered by Q5.1 = India)
> **Important:** India's Digital Personal Data Protection Act 2023 applies to any company processing personal data of Indian users or employees, regardless of where your company is based. Your audit will assess DPDP compliance gaps.

### ISO 42001 Info Box (triggered by Q5.3 = No or Q6.3 = unaware)
> **Did you know?** ISO 42001 is the certifiable AI management system standard — the AI equivalent of ISO 9001 (quality) and ISO 27001 (security). It's becoming a procurement requirement in enterprise B2B sales. Your audit will assess ISO 42001 readiness.
