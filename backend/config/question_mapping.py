QUESTIONS = {
    "awareness": [
        {
            "id": "q1_1",
            "label": "How would you rate leadership's understanding of AI capabilities and limitations?",
            "options": [
                "a) Deep understanding with clear strategic vision",
                "b) Good understanding of capabilities, still learning limitations",
                "c) Basic understanding, mostly driven by hype",
                "d) Minimal understanding, delegating to others",
                "e) No understanding or active resistance"
            ]
        },
        {
            "id": "q1_2",
            "label": "Does your company have a documented AI strategy?",
            "options": [
                "a) Yes, comprehensive strategy tied to business goals",
                "b) Yes, basic strategy for specific departments",
                "c) In development / draft stage",
                "d) Informal guidelines only",
                "e) No strategy"
            ]
        },
        {
            "id": "q1_3",
            "label": "How are AI-related decisions made in your organization?",
            "options": [
                "a) Cross-functional committee with clear framework",
                "b) IT/Tech leadership approval",
                "c) Department heads independently",
                "d) Ad-hoc based on individual requests",
                "e) No formal process / shadow IT"
            ]
        }
    ],
    "adoption": [
        {
            "id": "q2_1",
            "label": "What percentage of employees actively use AI tools in their work?",
            "options": [
                "a) 75%+ (Widespread)",
                "b) 50-74% (Majority)",
                "c) 25-49% (Significant minority)",
                "d) 10-24% (Early adopters)",
                "e) <10% (Isolated usage)"
            ]
        },
        {
            "id": "q2_2",
            "label": "How many AI tools are currently in active use at your company?",
            "options": [
                "a) 10+ tools",
                "b) 6-9 tools",
                "c) 3-5 tools",
                "d) 1-2 tools",
                "e) 0 tools"
            ]
        },
        {
            "id": "q2_3",
            "label": "How frequently do employees use AI tools?",
            "options": [
                "a) Daily (Core to workflow)",
                "b) Several times a week",
                "c) Weekly",
                "d) Monthly / Ad-hoc",
                "e) Rarely or never"
            ]
        }
    ],
    "integration": [
        {
            "id": "q3_1",
            "label": "How is AI integrated into your technology stack?",
            "options": [
                "a) API-level integration into custom workflows",
                "b) Automated connections (Zapier/Make) between tools",
                "c) Native integrations in existing platforms (e.g., Copilot in Office)",
                "d) Standalone web interfaces (copy/paste)",
                "e) No integration"
            ]
        },
        {
            "id": "q3_2",
            "label": "Is AI integrated into your core business systems (CRM, ERP, etc.)?",
            "options": [
                "a) Yes, deeply integrated across multiple systems",
                "b) Yes, in 1-2 primary systems",
                "c) Testing/Pilot phase",
                "d) Planning phase",
                "e) No integration"
            ]
        },
        {
            "id": "q3_3",
            "label": "How are AI workflows and best practices documented?",
            "options": [
                "a) Centralized, regularly updated knowledge base",
                "b) Department-level documentation",
                "c) Shared prompt library / informal docs",
                "d) Individual knowledge (siloed)",
                "e) Not documented"
            ]
        }
    ],
    "governance": [
        {
            "id": "q4_1",
            "label": "Does your company have policies governing AI usage?",
            "options": [
                "a) Comprehensive policy with enforcement mechanisms",
                "b) Basic guidelines provided to employees",
                "c) Draft policy in development",
                "d) Informal guidelines only",
                "e) No AI usage policy"
            ]
        },
        {
            "id": "q4_2",
            "label": "How does your company handle data privacy when using AI tools?",
            "options": [
                "a) Formal review process + approved tools only",
                "b) Guidelines provided to employees",
                "c) Ad-hoc review on request",
                "d) Left to employee discretion",
                "e) No oversight"
            ]
        },
        {
            "id": "q4_3",
            "label": "What is your organization's status regarding EU AI Act compliance?",
            "options": [
                "a) Fully assessed and compliant",
                "b) Assessment in progress",
                "c) Aware of requirements but not started",
                "d) Heard of it but taken no action",
                "e) Unaware of EU AI Act"
            ]
        }
    ],
    "roi": [
        {
            "id": "q5_1",
            "label": "Does your company measure ROI from AI investments?",
            "options": [
                "a) Yes, formal metrics with regular review",
                "b) Yes, informal tracking",
                "c) Basic measurement (time savings estimates)",
                "d) No, but planning to",
                "e) No measurement"
            ]
        },
        {
            "id": "q5_2",
            "label": "What is your estimated time savings from AI usage?",
            "options": [
                "a) 25% or more across knowledge work",
                "b) 15-24%",
                "c) 5-14%",
                "d) Less than 5%",
                "e) No measurable time savings"
            ]
        },
        {
            "id": "q5_3",
            "label": "How would you rate AI's overall business impact?",
            "options": [
                "a) Transformational - fundamentally changing how we operate",
                "b) Significant - measurable positive impact",
                "c) Moderate - some positive impact",
                "d) Minimal - limited visible impact",
                "e) Negative or no impact"
            ]
        }
    ]
}

def get_all_questions():
    """Returns a flat list of all questions."""
    all_qs = []
    for section in QUESTIONS.values():
        all_qs.extend(section)
    return all_qs

def get_question_by_id(question_id):
    """Returns a specific question by ID."""
    for q in get_all_questions():
        if q["id"] == question_id:
            return q
    return None
