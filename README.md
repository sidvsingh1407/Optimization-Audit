# AI Productivity Intelligence System

**A repeatable, data-driven AI audit + optimization system for B2B companies.**

---

## What This Is

- AI maturity auditing system (5 dimensions, 0-100 score)
- Automated compliance risk detection (EU AI Act + GDPR)
- Tool stack analysis and cost waste identification
- PDF report generator for client delivery
- Benchmark database foundation

---

## Quick Start

### Prerequisites
- Python 3.8+
- `pip install reportlab`

### Run an Audit

```bash
# 1. Create a form response file (see data/test_inputs/test_response.json for format)
# 2. Run the full audit pipeline
PYTHONPATH=. python backend/execution/orchestrator.py run data/test_inputs/test_response.json

# Output:
# - scores_YYYYMMDD-HHMMSS.json
# - audit_YYYYMMDD-HHMMSS.json
# - report_CompanyName_YYYYMMDD-HHMMSS.pdf
```

### Score Only (no report)
```bash
PYTHONPATH=. python backend/execution/orchestrator.py score data/test_inputs/test_response.json
```

---

## Project Structure

```
ai-productivity-os/
├── backend/                  # Core operational intelligence and execution
│   ├── audit_modules/        # Intelligence and scoring logic
│   ├── execution/            # Orchestration and pipeline
│   ├── config/               # Settings and prompts
│   ├── persistence/          # Database integration
│   ├── contracts/            # Pydantic data contracts
│   └── utils/                # Logging and helpers
├── frontend/                 # Streamlit UI
├── docs/                     # Specifications and architectural docs
├── tests/                    # Deterministic testing suites
├── data/                     # Output artifacts and runtime DB
│   ├── test_inputs/          # Sample forms
│   ├── runtime/              # SQLite database
│   ├── generated_outputs/    # JSON artifacts
│   └── generated_reports/    # PDF artifacts
├── requirements.txt
└── README.md
```

---

## Scoring Rubric

| Dimension | Weight | Description |
|-----------|--------|-------------|
| Awareness | 20 | Leadership AI understanding |
| Adoption | 20 | Breadth of AI tool usage |
| Integration | 20 | Depth of workflow integration |
| Governance | 20 | Policies, compliance, risk management |
| ROI | 20 | Measured business impact |

**Total: 0-100**

**Compliance Risk Flag:** Set to TRUE if governance is weak (no policy, no privacy oversight, or EU AI Act unaware).

---

## Output Files

### scores_*.json
```json
{
  "dimensions": {
    "awareness": 17,
    "adoption": 15,
    "integration": 13,
    "governance": 7,
    "roi": 13
  },
  "total_score": 65,
  "rating": "AI Adopting",
  "compliance_risk_flag": true,
  "compliance_risk_reasons": ["q4_1", "q4_3"]
}
```

### audit_*.json
Full audit results including agent findings.

### report_*.pdf
Client-facing PDF report with:
- Executive Summary
- AI Maturity Score (visual)
- Dimension Breakdown
- Compliance Alert (if flagged)
- Key Findings
- Top 5 Recommendations

---

## Next Steps (V2)

### 1. Set Up Tally Form
- Create form at https://tally.so using `docs/workflows/tally_form_structure.md`
- Enable Google Sheets export
- Test with internal team

### 2. Set Up Airtable
- Create base using `docs/architecture/database_schema.md`
- Get Base ID and API token
- Update orchestrator to write directly

### 3. Connect Claude API (Optional)
- Replace rule-based agents with actual API calls
- Use prompts from `backend/config/prompts/agent_prompts.md`

### 4. Build Benchmark Dashboard
- Google Sheets auto-populates from opt-in audits
- Create comparison views for client reports

---

## Sales Positioning

**Headline:** "We audit your AI usage, show where you're wasting money, and tell you exactly what to fix."

**Triggers:**
- EU AI Act compliance deadline (August 2026)
- CFO cost-cutting pressure
- AI tool sprawl

**Deliverable:** Professional PDF report with score, findings, and prioritized recommendations.

---

## License

@sidsvingh
