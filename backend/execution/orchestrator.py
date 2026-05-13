import json
import sys
import uuid
import time
from datetime import datetime
from pathlib import Path

# Original logic functions
from scoring_engine import calculate_scores, format_score_report, load_form_responses

# To prevent circular dependency, import locally inside the function instead of global
# from orchestrator import analyze_tools, analyze_workflows, analyze_compliance, generate_analytics_report

# New Observability/Persistence contracts
from backend.contracts.events import (
    AuditStartedEvent, AuditValidatedEvent, WorkflowAnalyzedEvent,
    GovernanceMappedEvent, RiskScoredEvent, ReportGeneratedEvent,
    PersistenceCompletedEvent, AuditFailedEvent
)
from backend.persistence.database import (
    init_db, log_event, init_execution_metrics, update_execution_metrics, save_execution_summary
)
from backend.utils.logger import setup_logger, ExecutionTracer

def run_audit(form_response_path: str):
    # System init
    init_db()
    setup_logger()

    execution_id = str(uuid.uuid4())
    tracer = ExecutionTracer(execution_id)
    start_time = datetime.utcnow().isoformat() + "Z"
    start_time_ts = time.time()

    init_execution_metrics(execution_id, start_time)

    tracer.log_trace("Starting execution pipeline", stage="initialization")

    try:
        # Step 1: Load form responses
        data = load_form_responses(form_response_path)
        company_name = data.get('company_name') or data.get('responses', {}).get('company_name', 'Unknown')
        audit_data = data.get('responses', data)

        # Log AuditStarted Event
        log_event(AuditStartedEvent(execution_id=execution_id, company_name=company_name))
        tracer.log_trace(f"Loaded responses for {company_name}", stage="data_load")

        # Log Validation Event
        log_event(AuditValidatedEvent(execution_id=execution_id))

        # Step 2: Calculate scores
        tracer.log_trace("Calculating AI maturity scores", stage="scoring")
        scores = calculate_scores(audit_data)

        # Event: Risk Scored
        risk_level = "high" if scores.get("compliance_risk_flag") else "low"
        log_event(RiskScoredEvent(execution_id=execution_id, risk_level=risk_level, metadata={"total_score": scores.get("total_score")}))

        # Import analyzers dynamically to avoid circular import issues with wrapper root scripts
        from orchestrator import analyze_tools, analyze_workflows, analyze_compliance, generate_analytics_report

        # Step 3: Run agent analyses
        tracer.log_trace("Running agent analyses", stage="analysis")
        tool_analysis = analyze_tools(audit_data, data)

        workflow_analysis = analyze_workflows(audit_data, scores)
        log_event(WorkflowAnalyzedEvent(execution_id=execution_id))

        compliance_analysis = analyze_compliance(audit_data, scores)
        log_event(GovernanceMappedEvent(execution_id=execution_id))

        analytics_report = generate_analytics_report(scores, tool_analysis, workflow_analysis, compliance_analysis, data)

        # Step 4: Save intermediate results
        output_dir = Path(form_response_path).parent
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")

        scores_path = output_dir / f"scores_{timestamp}.json"
        with open(scores_path, 'w') as f:
            json.dump(scores, f, indent=2)

        audit_result = {
            'execution_id': execution_id,
            'company_name': company_name,
            'audit_date': datetime.now().isoformat(),
            'scores': scores,
            'agent_findings': {
                'tool_evaluator': tool_analysis,
                'workflow_optimizer': workflow_analysis,
                'compliance_auditor': compliance_analysis,
                'analytics_reporter': analytics_report,
            }
        }

        audit_path = output_dir / f"audit_{timestamp}.json"
        with open(audit_path, 'w') as f:
            json.dump(audit_result, f, indent=2)

        # Write to execution summary table
        save_execution_summary(
            execution_id=execution_id,
            company_name=company_name,
            total_score=scores.get("total_score", 0),
            compliance_risk_flag=scores.get("compliance_risk_flag", False),
            created_at=start_time
        )
        log_event(PersistenceCompletedEvent(execution_id=execution_id))

        # Step 5: Generate PDF report
        tracer.log_trace("Generating PDF report", stage="reporting")
        pdf_path_str = None
        try:
            from report_generator import generate_report
            pdf_path = output_dir / f"report_{company_name.replace(' ', '_')}_{timestamp}.pdf"
            generate_report(data, scores, audit_result['agent_findings'], str(pdf_path))
            pdf_path_str = str(pdf_path)
            log_event(ReportGeneratedEvent(execution_id=execution_id, report_path=pdf_path_str))
        except ImportError as e:
            tracer.log_trace(f"report_generator not available ({e})", level="WARNING", stage="reporting")

        # Update end metrics
        end_time_ts = time.time()
        end_time = datetime.utcnow().isoformat() + "Z"
        duration_ms = (end_time_ts - start_time_ts) * 1000

        # Hardcoding warning/error counts to 0 for MVP demo tracing
        update_execution_metrics(execution_id, {
            "status": "completed",
            "end_time": end_time,
            "duration_ms": duration_ms,
            "warning_counts": 0,
            "error_counts": 0,
            "governance_flags": 1 if scores.get("compliance_risk_flag") else 0,
            "relationship_counts": 0
        })

        tracer.log_trace(f"Pipeline completed in {duration_ms:.2f}ms", stage="completion")

        return {
            'execution_id': execution_id,
            'scores_path': str(scores_path),
            'audit_path': str(audit_path),
            'pdf_path': pdf_path_str,
            'scores': scores,
        }

    except Exception as e:
        end_time_ts = time.time()
        duration_ms = (end_time_ts - start_time_ts) * 1000

        tracer.log_trace(f"Audit failed: {str(e)}", level="ERROR", stage="execution")
        log_event(AuditFailedEvent(execution_id=execution_id, error_message=str(e)))

        update_execution_metrics(execution_id, {
            "status": "failed",
            "end_time": datetime.utcnow().isoformat() + "Z",
            "duration_ms": duration_ms,
            "error_counts": 1
        })
        raise
