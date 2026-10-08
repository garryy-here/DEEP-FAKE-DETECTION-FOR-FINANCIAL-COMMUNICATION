"""
Report Generator - Creates detailed, actionable reports for financial communication analysis.
"""
import json
import os
from datetime import datetime


class ReportGenerator:
    """Generate comprehensive analysis reports with actionable recommendations."""

    def __init__(self, output_dir=None):
        if output_dir is None:
            from config import REPORTS_DIR
            output_dir = REPORTS_DIR
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def generate_report(self, analysis_result):
        """
        Generate a detailed report from analysis results.

        Args:
            analysis_result (dict): Results from EnsembleDetector.

        Returns:
            dict: Formatted report with all sections.
        """
        overall = analysis_result.get("overall", {})
        action_plan = analysis_result.get("action_plan", {})

        report = {
            "report_id": f"RPT-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            "case_id": analysis_result.get("case_id", "N/A"),
            "generated_at": datetime.now().isoformat(),
            "title": analysis_result.get("title", "DeepFake Detection Report"),

            "executive_summary": self._generate_executive_summary(overall),

            "risk_assessment": {
                "overall_risk_level": overall.get("risk_level", "UNKNOWN"),
                "deepfake_probability": f"{overall.get('deepfake_probability', 0) * 100:.1f}%",
                "confidence": f"{overall.get('confidence', 0) * 100:.1f}%",
                "modalities_analyzed": analysis_result.get("modalities_analyzed", []),
            },

            "detailed_findings": self._format_findings(overall.get("all_findings", [])),

            "modality_breakdown": self._format_modality_results(
                analysis_result.get("modality_results", {})
            ),

            "action_plan": {
                "risk_level": action_plan.get("risk_level", "UNKNOWN"),
                "review_timeline": action_plan.get("review_timeline", "N/A"),
                "escalation_required": action_plan.get("escalation_required", False),
                "report_to_authorities": action_plan.get("report_to_authorities", False),
                "immediate_actions": action_plan.get("immediate_actions", []),
                "follow_up_actions": action_plan.get("follow_up_actions", []),
            },

            "compliance_notes": self._generate_compliance_notes(overall.get("risk_level", "CLEAN")),

            "engine_version": analysis_result.get("engine_version", "N/A"),
        }

        return report

    def save_report(self, report, filename=None):
        """Save report to JSON file."""
        if filename is None:
            filename = f"{report['report_id']}.json"

        filepath = os.path.join(self.output_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        return filepath

    def format_report_text(self, report):
        """Format report as human-readable text."""
        lines = []
        lines.append("=" * 70)
        lines.append(f"  DEEPFAKE DETECTION REPORT")
        lines.append(f"  {report['title']}")
        lines.append("=" * 70)
        lines.append(f"  Report ID  : {report['report_id']}")
        lines.append(f"  Case ID    : {report['case_id']}")
        lines.append(f"  Generated  : {report['generated_at']}")
        lines.append("")

        # Executive Summary
        lines.append("-" * 70)
        lines.append("  EXECUTIVE SUMMARY")
        lines.append("-" * 70)
        lines.append(f"  {report['executive_summary']}")
        lines.append("")

        # Risk Assessment
        risk = report['risk_assessment']
        lines.append("-" * 70)
        lines.append("  RISK ASSESSMENT")
        lines.append("-" * 70)
        lines.append(f"  Risk Level          : {risk['overall_risk_level']}")
        lines.append(f"  DeepFake Probability: {risk['deepfake_probability']}")
        lines.append(f"  Confidence          : {risk['confidence']}")
        lines.append(f"  Modalities Analyzed : {', '.join(risk['modalities_analyzed'])}")
        lines.append("")

        # Findings
        lines.append("-" * 70)
        lines.append("  DETAILED FINDINGS")
        lines.append("-" * 70)
        for i, finding in enumerate(report['detailed_findings'], 1):
            lines.append(f"  [{finding['severity']}] {finding['category']}")
            lines.append(f"    Modality: {finding.get('modality', 'N/A')}")
            lines.append(f"    {finding['detail']}")
            lines.append("")

        # Action Plan
        plan = report['action_plan']
        lines.append("-" * 70)
        lines.append("  ACTION PLAN")
        lines.append("-" * 70)
        lines.append(f"  Review Timeline     : {plan['review_timeline']}")
        lines.append(f"  Escalation Required : {'Yes' if plan['escalation_required'] else 'No'}")
        lines.append(f"  Report to Authorities: {'Yes' if plan['report_to_authorities'] else 'No'}")
        lines.append("")
        lines.append("  Immediate Actions:")
        for action in plan['immediate_actions']:
            lines.append(f"    {action}")
        lines.append("")
        if plan['follow_up_actions']:
            lines.append("  Follow-up Actions:")
            for action in plan['follow_up_actions']:
                lines.append(f"    {action}")
            lines.append("")

        # Compliance
        lines.append("-" * 70)
        lines.append("  COMPLIANCE NOTES")
        lines.append("-" * 70)
        for note in report['compliance_notes']:
            lines.append(f"  • {note}")
        lines.append("")

        lines.append("=" * 70)
        lines.append(f"  Engine Version: {report['engine_version']}")
        lines.append("=" * 70)

        return "\n".join(lines)

    def _generate_executive_summary(self, overall):
        risk = overall.get("risk_level", "CLEAN")
        prob = overall.get("deepfake_probability", 0)
        findings_count = len(overall.get("all_findings", []))

        summaries = {
            "CRITICAL": f"CRITICAL ALERT: Analysis detected strong indicators of deepfake manipulation "
                        f"with {prob*100:.1f}% probability. {findings_count} significant anomalies were "
                        f"identified across multiple analysis dimensions. Immediate action is required to "
                        f"prevent potential financial fraud. All related transactions should be frozen pending investigation.",

            "HIGH": f"HIGH RISK: Analysis identified multiple indicators of potential manipulation "
                    f"with {prob*100:.1f}% probability. {findings_count} anomalies were detected. "
                    f"Enhanced due diligence and senior compliance review are recommended before "
                    f"proceeding with any related financial transactions.",

            "MEDIUM": f"MEDIUM RISK: Analysis found some suspicious indicators with {prob*100:.1f}% "
                      f"probability of manipulation. {findings_count} anomalies warrant further "
                      f"investigation. Recommend additional verification through independent channels.",

            "LOW": f"LOW RISK: Analysis detected minor anomalies with {prob*100:.1f}% probability. "
                   f"These may be natural variations. Standard monitoring procedures are sufficient.",

            "CLEAN": f"CLEAN: No significant manipulation indicators detected. Communication appears "
                     f"authentic with {(1-prob)*100:.1f}% confidence. Standard processing may proceed.",
        }
        return summaries.get(risk, summaries["LOW"])

    def _format_findings(self, findings):
        formatted = []
        for f in findings:
            formatted.append({
                "category": f.get("category", "Unknown"),
                "severity": f.get("severity", "LOW"),
                "modality": f.get("modality", "general"),
                "detail": f.get("detail", "No details available."),
            })
        return formatted

    def _format_modality_results(self, modality_results):
        breakdown = {}
        for modality, result in modality_results.items():
            breakdown[modality] = {
                "deepfake_probability": f"{result.get('deepfake_probability', 0) * 100:.1f}%",
                "confidence": f"{result.get('confidence', 0) * 100:.1f}%",
                "risk_level": result.get("risk_level", "UNKNOWN"),
                "sub_scores": result.get("sub_scores", {}),
            }
        return breakdown

    def _generate_compliance_notes(self, risk_level):
        notes = [
            "This analysis is provided as a decision-support tool and should not be the sole basis for action.",
            "All findings should be reviewed by qualified compliance personnel.",
            "Records of this analysis should be retained per organizational data retention policies.",
        ]

        if risk_level in ["CRITICAL", "HIGH"]:
            notes.extend([
                "Under BSA/AML regulations, suspicious activity may require SAR filing within 30 days.",
                "Preserve all evidence in compliance with litigation hold procedures.",
                "Document the chain of custody for all analyzed communications.",
                "Notify the designated compliance officer as per institutional policy.",
            ])

        if risk_level == "CRITICAL":
            notes.extend([
                "Consider engaging external forensic experts for independent verification.",
                "Federal law enforcement notification may be required under 18 U.S.C. § 1030.",
            ])

        return notes
