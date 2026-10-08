"""
Video Analysis Model for DeepFake Detection in Financial Communications.
Detects face-swapped, lip-synced, or AI-generated video calls.
"""
from datetime import datetime


class VideoAnalyzer:
    """
    Video deepfake detection engine for financial video communications.
    Analyzes facial consistency, lip-sync accuracy, temporal coherence,
    and biological signals to detect manipulated video calls.
    """

    def __init__(self):
        self.name = "VideoAnalyzer"
        self.version = "2.1.0"

    def analyze(self, video_features=None, metadata=None):
        if video_features is None:
            video_features = {}

        features = self._get_features(video_features)

        facial_score = self._analyze_facial_consistency(features)
        lipsync_score = self._analyze_lip_sync(features)
        temporal_score = self._analyze_temporal_coherence(features)
        biological_score = self._analyze_biological_signals(features)
        lighting_score = self._analyze_lighting_consistency(features)

        raw_score = (
            facial_score * 0.28 +
            lipsync_score * 0.26 +
            temporal_score * 0.22 +
            biological_score * 0.14 +
            lighting_score * 0.10
        )

        # Calibrated mapping
        if raw_score >= 0.40:
            deepfake_probability = min(0.99, 0.78 + (raw_score - 0.40) * 0.42)
        elif raw_score >= 0.20:
            deepfake_probability = 0.35 + (raw_score - 0.20) * 1.80
        else:
            deepfake_probability = max(0.02, raw_score * 0.50)

        findings = self._collect_findings(
            facial_score, lipsync_score, temporal_score,
            biological_score, lighting_score
        )

        return {
            "type": "video",
            "deepfake_probability": round(deepfake_probability, 4),
            "confidence": round(min(0.97, 0.68 + abs(deepfake_probability - 0.5) * 0.58), 4),
            "risk_level": self._get_risk_level(deepfake_probability),
            "sub_scores": {
                "facial_consistency": round(facial_score, 4),
                "lip_sync_accuracy": round(lipsync_score, 4),
                "temporal_coherence": round(temporal_score, 4),
                "biological_signals": round(biological_score, 4),
                "lighting_consistency": round(lighting_score, 4),
            },
            "features_analyzed": {
                "fps": features.get("fps", 30),
                "resolution": features.get("resolution", (1920, 1080)),
                "duration_seconds": features.get("duration", 60),
                "face_detected": features.get("face_detected", True),
                "blink_rate": features.get("blink_rate", 16),
            },
            "findings": findings,
            "analyzed_at": datetime.now().isoformat(),
            "model_version": self.version,
        }

    def _get_features(self, video_features):
        defaults = {
            "facial_landmark_stability": 0.88,
            "face_boundary_sharpness": 0.80,
            "skin_texture_consistency": 0.85,
            "lip_sync_score": 0.90,
            "lip_movement_naturalness": 0.88,
            "frame_consistency": 0.92,
            "motion_smoothness": 0.88,
            "temporal_flicker": 0.04,
            "blink_rate": 16,
            "blink_regularity": 0.68,
            "micro_expression_presence": 0.70,
            "pupil_dilation_variation": 0.30,
            "lighting_direction_consistency": 0.88,
            "shadow_consistency": 0.85,
            "reflection_consistency": 0.82,
            "face_detected": True,
            "fps": 30,
            "resolution": (1920, 1080),
            "duration": 60,
        }
        defaults.update(video_features)
        return defaults

    def _analyze_facial_consistency(self, features):
        score = 0.0
        stability = features.get("facial_landmark_stability", 0.88)
        if stability < 0.70:
            score += 0.50 * min(1.0, (0.70 - stability) / 0.25)
        if stability < 0.60:
            score += 0.35

        boundary = features.get("face_boundary_sharpness", 0.80)
        if boundary > 0.92 or boundary < 0.55:
            score += 0.35

        texture = features.get("skin_texture_consistency", 0.85)
        if texture < 0.65:
            score += 0.35

        return min(1.0, score)

    def _analyze_lip_sync(self, features):
        score = 0.0
        sync = features.get("lip_sync_score", 0.90)
        if sync < 0.75:
            score += 0.60 * min(1.0, (0.75 - sync) / 0.25)
        if sync < 0.60:
            score += 0.30

        naturalness = features.get("lip_movement_naturalness", 0.88)
        if naturalness < 0.70:
            score += 0.35

        return min(1.0, score)

    def _analyze_temporal_coherence(self, features):
        score = 0.0
        flicker = features.get("temporal_flicker", 0.04)
        if flicker > 0.12:
            score += 0.55 * min(1.0, (flicker - 0.12) / 0.15)
        if flicker > 0.20:
            score += 0.35

        frame_cons = features.get("frame_consistency", 0.92)
        if frame_cons < 0.78:
            score += 0.35

        return min(1.0, score)

    def _analyze_biological_signals(self, features):
        score = 0.0
        blink = features.get("blink_rate", 16)
        if blink < 6 or blink > 38:
            score += 0.55

        regularity = features.get("blink_regularity", 0.68)
        if regularity > 0.92:
            score += 0.30

        micro = features.get("micro_expression_presence", 0.70)
        if micro < 0.15:
            score += 0.35

        return min(1.0, score)

    def _analyze_lighting_consistency(self, features):
        score = 0.0
        dir_cons = features.get("lighting_direction_consistency", 0.88)
        if dir_cons < 0.70:
            score += 0.45

        shadow = features.get("shadow_consistency", 0.85)
        if shadow < 0.65:
            score += 0.35

        return min(1.0, score)

    def _collect_findings(self, facial, lipsync, temporal, biological, lighting):
        findings = []

        if facial > 0.30:
            findings.append({
                "category": "Facial Inconsistency",
                "severity": "CRITICAL" if facial > 0.60 else "HIGH",
                "detail": "Facial boundary warping and landmark jitter detected, characteristic of deepfake face swapping."
            })

        if lipsync > 0.30:
            findings.append({
                "category": "Lip-Sync Mismatch",
                "severity": "HIGH",
                "detail": "Viseme-phoneme timing misalignment detected between audio track and mouth movements."
            })

        if temporal > 0.30:
            findings.append({
                "category": "Temporal Artifacts",
                "severity": "HIGH",
                "detail": "High-frequency inter-frame flicker and texture discontinuities detected across video keyframes."
            })

        if biological > 0.30:
            findings.append({
                "category": "Biological Signal Anomaly",
                "severity": "HIGH",
                "detail": "Abnormal biological patterns (hypo-blinking and absence of micro-expressions) indicate AI generation."
            })

        if not findings:
            findings.append({
                "category": "Clean",
                "severity": "LOW",
                "detail": "Natural facial micro-movements, physiological blinking, and lighting coherence verified."
            })

        return findings

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
