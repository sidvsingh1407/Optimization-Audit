# Architecture

The system uses a SIMPLE MONOLITHIC MODULAR ARCHITECTURE.

- **Backend:** Contains business logic (`services`, `scoring`, `reports`, `compliance`), config (`config`), and utility models/helpers. It exposes entry points via CLI.
- **Frontend:** Streamlit app that imports backend modules directly.
- **Data flow:** User inputs data -> Orchestrator orchestrates logic -> Scoring engine calculates AI maturity -> Compliance analyzer spots risk -> Report generator creates PDF -> Streamlit displays / user downloads.
