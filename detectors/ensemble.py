"""
Ensemble Detector - Combines all analysis modules for comprehensive detection.
"""
from datetime import datetime
from models.text_analyzer import TextAnalyzer
from models.audio_analyzer import AudioAnalyzer
from models.image_analyzer import ImageAnalyzer
from models.video_analyzer import VideoAnalyzer


class EnsembleDetector:
    """
    Ensemble deepfake detection system that combines results from
    multiple analysis modules for comprehensive financial communication verification.
    """

    def __init__(self):
        self.text_analyzer = TextAnalyzer()
        self.audio_analyzer = AudioAnalyzer()
        self.image_analyzer = ImageAnalyzer()
        self.video_analyzer = VideoAnalyzer()
        self.version = "3.1.0"

    def analyze_communication(self, communication):
        results = {}
        modalities_analyzed = []
        metadata = communication.get("metadata", {})

        # Text Analysis
        if communication.get("text"):
            results["text"] = self.text_analyzer.analyze(
                communication["text"], metadata
            )
            modalities_analyzed.append("text")

        # Audio Analysis
        if communication.get("audio_features"):
            results["audio"] = self.audio_analyzer.analyze(
                communication["audio_features"],
                communication.get("transcript") or communication.get("text"),
                metadata
            )
            modalities_analyzed.append("audio")

        # Image Analysis
        if communication.get("image_features"):
            results["image"] = self.image_analyzer.analyze(
                communication["image_features"], metadata
            )
            modalities_analyzed.append("image")

        # Video Analysis
        if communication.get("video_features"):
            results["video"] = self.video_analyzer.analyze(
                communication["video_features"], metadata
            )
            modalities_analyzed.append("video")

        overall = self._compute_overall(results, modalities_analyzed)

        return {
            "case_id": communication.get("case_id", f"CASE-{datetime.now().strftime('%Y%m%d%H%M%S')}"),
            "title": communication.get("title", "Financial Communication Analysis"),
            "overall": overall,
            "modality_results": results,
            "modalities_analyzed": modalities_analyzed,
            "action_plan": self._generate_action_plan(overall["risk_level"]),
            "analyzed_at": datetime.now().isoformat(),
            "engine_version": self.version,
        }

    def _compute_overall(self, results, modalities):
        if not results:
            return {
                "deepfake_probability": 0.0,
                "confidence": 0.0,
                "risk_level": "CLEAN",
                "all_findings": [],
            }

        probs = [results[m]["deepfake_probability"] for m in modalities]
        confidences = [results[m]["confidence"] for m in modalities]

        all_findings = []
        for m in modalities:
            for f in results[m].get("findings", []):
                f_copy = dict(f)
                f_copy["modality"] = m
                all_findings.append(f_copy)

        # Multi-modal fusion
        if len(modalities) == 1:
            overall_prob = probs[0]
            overall_conf = confidences[0]
        else:
            max_prob = max(probs)
            avg_prob = sum(probs) / len(probs)
            high_risk_count = sum(1 for p in probs if p >= 0.60)

            # In fraud detection, any strong compromised modality is critical
            if max_prob >= 0.75:
                if high_risk_count >= 2:
                    overall_prob = min(0.99, max_prob + 0.05)
                else:
                    overall_prob = max_prob * 0.85 + avg_prob * 0.15
            elif max_prob <= 0.25:
                overall_prob = avg_prob
            else:
                overall_prob = (max_prob * 0.6) + (avg_prob * 0.4)

            overall_conf = max(confidences) * 0.7 + (sum(confidences) / len(confidences)) * 0.3

        risk_level = self._get_risk_level(overall_prob)

        severity_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
        all_findings.sort(key=lambda f: severity_order.get(f.get("severity", "LOW"), 4))

        return {
            "deepfake_probability": round(overall_prob, 4),
            "confidence": round(overall_conf, 4),
            "risk_level": risk_level,
            "all_findings": all_findings,
        }

    def _generate_action_plan(self, risk_level):
        from config import ACTION_PLANS
        actions = ACTION_PLANS.get(risk_level, ACTION_PLANS["LOW"])

        return {
            "risk_level": risk_level,
            "immediate_actions": actions[:3] if len(actions) >= 3 else actions,
            "follow_up_actions": actions[3:] if len(actions) > 3 else [],
            "review_timeline": self._get_timeline(risk_level),
            "escalation_required": risk_level in ["CRITICAL", "HIGH"],
            "report_to_authorities": risk_level == "CRITICAL",
        }

    def _get_timeline(self, risk_level):
        timelines = {
            "CRITICAL": "Immediate - within 1 hour",
            "HIGH": "Urgent - within 24 hours",
            "MEDIUM": "Standard - within 72 hours",
            "LOW": "Routine - within 1 week",
            "CLEAN": "No action required",
        }
        return timelines.get(risk_level, "Standard review")

    def _get_risk_level(self, probability):
        if probability >= 0.85:
            return "CRITICAL"
        elif probability >= 0.65:
            return "HIGH"
        elif probability >= 0.40:
            return "MEDIUM"
        elif probability >= 0.15:
            return "LOW"
        return "CLEAN"
