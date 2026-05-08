# Database Schema v1.0
## AI Productivity Intelligence System

---

## Storage Architecture

**MVP Stack:**
- **Google Sheets** → Benchmark database (anonymized aggregates)
- **Airtable** → Audit records (structured data, client info)
- **Local JSON** → Intermediate form exports

---

## Airtable Base: `ai_audits`

### Table 1: `companies`

| Field | Type | Description |
|-------|------|-------------|
| `id` | Auto-number | Unique company ID |
| `name` | Single line text | Company name |
| `industry` | Single select | Industry category |
| `employee_count` | Single select | Company size |
| `contact_name` | Single line text | Primary contact |
| `contact_email` | Email | Contact email |
| `created_at` | Created time | Record creation date |
| `benchmark_opt_in` | Checkbox | Allow anonymized benchmarking |

**Industry Options:**
- Marketing/Advertising
- SaaS/Technology
- Professional Services
- Healthcare
- Finance/FinTech
- E-commerce/Retail
- Manufacturing
- Education
- Other

**Employee Count Options:**
- 10-49
- 50-99
- 100-249
- 250-499
- 500+

---

### Table 2: `audits`

| Field | Type | Description |
|-------|------|-------------|
| `id` | Auto-number | Unique audit ID |
| `company_id` | Link to companies | Linked company |
| `audit_date` | Date | Audit completion date |
| `auditor` | Single line text | Who ran the audit |
| `status` | Single select | draft / completed / delivered |

**Score Fields:**
| Field | Type | Range |
|-------|------|-------|
| `score_awareness` | Number | 0-20 |
| `score_adoption` | Number | 0-20 |
| `score_integration` | Number | 0-20 |
| `score_governance` | Number | 0-20 |
| `score_roi` | Number | 0-20 |
| `score_total` | Number | 0-100 |
| `compliance_risk_flag` | Checkbox | TRUE if risk detected |

**Raw Response Fields:**
| Field | Type | Description |
|-------|------|-------------|
| `q1_1` | Single select | Leadership AI understanding |
| `q1_2` | Single select | AI strategy document |
| `q1_3` | Single select | AI decision making |
| `q2_1` | Single select | % employees using AI |
| `q2_2` | Single select | Number of AI tools |
| `q2_3` | Single select | Usage frequency |
| `q3_1` | Single select | Tech stack integration |
| `q3_2` | Single select | AI in core systems |
| `q3_3` | Single select | Workflow documentation |
| `q4_1` | Single select | AI policies |
| `q4_2` | Single select | Data privacy handling |
| `q4_3` | Single select | EU AI Act readiness |
| `q5_1` | Single select | ROI measurement |
| `q5_2` | Single select | Time savings estimate |
| `q5_3` | Single select | Business impact rating |

**Spend Data:**
| Field | Type | Description |
|-------|------|-------------|
| `monthly_spend` | Single select | Total monthly AI spend |
| `spend_breakdown` | Long text | Per-tool spend (optional) |

**Monthly Spend Options:**
- < $500
- $500-$2K
- $2K-$10K
- $10K+

**Tools Data:**
| Field | Type | Description |
|-------|------|-------------|
| `tools_used` | Long text | List of AI tools in use |
| `tool_count` | Number | Count of tools |

**Findings:**
| Field | Type | Description |
|-------|------|-------------|
| `cost_waste_estimate` | Currency | Estimated monthly waste |
| `top_findings` | Long text | Key findings summary |
| `recommendations` | Long text | Top 5 recommendations |
| `report_path` | Single line text | Path to generated PDF |

**Status Options:**
- draft
- in_progress
- completed
- delivered

---

### Table 3: `benchmarks` (Auto-populated from opt-in audits)

| Field | Type | Description |
|-------|------|-------------|
| `id` | Auto-number | Benchmark record ID |
| `industry` | Single select | Industry category |
| `employee_count` | Single select | Company size bracket |
| `score_total` | Number | 0-100 |
| `score_awareness` | Number | 0-20 |
| `score_adoption` | Number | 0-20 |
| `score_integration` | Number | 0-20 |
| `score_governance` | Number | 0-20 |
| `score_roi` | Number | 0-20 |
| `tool_count` | Number | Number of tools |
| `monthly_spend` | Single select | Spend bracket |
| `compliance_risk_flag` | Checkbox | Risk flag |
| `created_at` | Created time | Record date |

**Note:** This table contains ONLY anonymized data. No company names, contacts, or identifiable info.

---

## Google Sheets: `AI Audit Benchmarks`

**Purpose:** Real-time benchmark viewing, simple formulas, client-facing comparisons

### Sheet 1: `Raw Data`

| Column | Header |
|--------|--------|
| A | benchmark_id |
| B | industry |
| C | employee_count |
| D | score_total |
| E | score_awareness |
| F | score_adoption |
| G | score_integration |
| H | score_governance |
| I | score_roi |
| J | tool_count |
| K | monthly_spend |
| L | compliance_risk_flag |
| M | created_at |

### Sheet 2: `Dashboard`

**Auto-calculated metrics:**

| Metric | Formula |
|--------|---------|
| Avg Score (All) | `=AVERAGE(Raw_Data!D:D)` |
| Avg Score by Industry | `=AVERAGEIF(Raw_Data!B:B, "SaaS", Raw_Data!D:D)` |
| Avg Score by Size | `=AVERAGEIF(Raw_Data!C:C, "50-99", Raw_Data!D:D)` |
| % with Compliance Risk | `=COUNTIF(Raw_Data!L:L, TRUE)/COUNTA(Raw_Data!A:A)` |
| Avg Tools in Use | `=AVERAGE(Raw_Data!J:J)` |

### Sheet 3: `Client Comparison`

**For generating client-specific comparisons:**

| Input | Formula |
|-------|---------|
| Client Industry | Dropdown |
| Client Size | Dropdown |
| Client Score | Manual entry |
| Industry Avg | `=AVERAGEIF(Raw_Data!B:B, B2, Raw_Data!D:D)` |
| Size Avg | `=AVERAGEIF(Raw_Data!C:C, B3, Raw_Data!D:D)` |
| Percentile | `=PERCENTRANK(Raw_Data!D:D, B4)` |

---

## Data Flow

```
┌─────────────────┐
│   Tally Form    │  (Intake)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  JSON Export    │  (Google Drive / Local)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Scoring Engine  │  (Python script)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Airtable      │  (Structured audit record)
└────────┬────────┘
         │
         ├──────────────►┌─────────────────┐
         │               │  Google Sheets  │
         │               │  (Benchmarks)   │
         │               └─────────────────┘
         │
         ▼
┌─────────────────┐
│ Report Generator│  (PDF output)
└─────────────────┘
```

---

## API Endpoints (Airtable)

**Base ID:** `appXXXXXXXXXXXXXX` (to be created)

**Personal Access Token:** Required for API access

### Create Audit Record
```
POST /records
{
  "fields": {
    "company_id": ["recXXX"],
    "audit_date": "2026-04-05",
    "score_total": 72,
    "compliance_risk_flag": true,
    ...
  }
}
```

### Update Benchmark (Opt-in only)
```
POST /benchmarks/records
{
  "fields": {
    "industry": "SaaS",
    "employee_count": "50-99",
    "score_total": 72,
    ...
  }
}
```

---

## Local JSON Schema (Form Export)

```json
{
  "form_id": "tally_form_id",
  "submission_id": "submission_uuid",
  "submitted_at": "2026-04-05T10:30:00Z",
  "responses": {
    "company_name": "Acme Corp",
    "industry": "SaaS",
    "employee_count": "50-99",
    "contact_name": "John Doe",
    "contact_email": "john@acme.com",
    "benchmark_opt_in": true,
    "q1_1": "b",
    "q1_2": "a",
    "q1_3": "b",
    "q2_1": "b",
    "q2_2": "c",
    "q2_3": "a",
    "q3_1": "c",
    "q3_2": "b",
    "q3_3": "b",
    "q4_1": "c",
    "q4_2": "b",
    "q4_3": "c",
    "q5_1": "b",
    "q5_2": "c",
    "q5_3": "b",
    "monthly_spend": "$2K-$10K",
    "tools_used": "ChatGPT, Copilot, Jasper, Midjourney",
    "spend_breakdown": "ChatGPT: $200, Copilot: $1000, Jasper: $500"
  }
}
```

---

## Form → Score Mapping Reference

| Response | Points |
|----------|--------|
| a | 20 |
| b | 15 |
| c | 10 |
| d | 5 |
| e | 0 |

**Dimension Calculation:**
```python
awareness = round((q1_1 + q1_2 + q1_3) / 3)
adoption = round((q2_1 + q2_2 + q2_3) / 3)
integration = round((q3_1 + q3_2 + q3_3) / 3)
governance = round((q4_1 + q4_2 + q4_3) / 3)
roi = round((q5_1 + q5_2 + q5_3) / 3)
total = awareness + adoption + integration + governance + roi
```
