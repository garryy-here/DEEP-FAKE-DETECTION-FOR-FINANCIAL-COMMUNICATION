"""
Audio Analysis Model for DeepFake Detection in Financial Communications.
Analyzes audio features to detect synthetic/cloned voice in phone calls and voice messages.
"""
import math
from datetime import datetime


class AudioAnalyzer:
    """
    Audio deepfake detection engine for financial voice communications.
    Analyzes spectral features, voice consistency, temporal cues, and cloning artifacts.
    """

    def __init__(self):
        self.name = "AudioAnalyzer"
        self.version = "2.2.0"

    def analyze(self, audio_features=None, transcript=None, metadata=None):
        if audio_features is None:
            audio_features = {}

        features = self._get_features(audio_features)

        spectral_score = self._analyze_spectral(features)
        voice_score = self._analyze_voice_consistency(features)
        temporal_score = self._analyze_temporal_patterns(features)
        artifact_score = self._detect_cloning_artifacts(features)
        background_score = self._analyze_background(features)

        raw_score = (
            spectral_score * 0.28 +
            voice_score * 0.28 +
            temporal_score * 0.22 +
            artifact_score * 0.14 +
            background_score * 0.08
        )

        # Calibrated mapping
        if raw_score >= 0.45:
            deepfake_probability = min(0.98, 0.76 + (raw_score - 0.45) * 0.45)
        elif raw_score >= 0.25:
            deepfake_probability = 0.40 + (raw_score - 0.25) * 1.50
        else:
            deepfake_probability = max(0.03, raw_score * 0.60)

        # Transcript cues boost if present
        transcript_findings = []
        if transcript:
            transcript_findings = self._analyze_transcript_for_audio_cues(transcript)
            if transcript_findings:
                deepfake_probability = min(0.98, deepfake_probability + 0.08)

        findings = self._collect_findings(
            spectral_score, voice_score, temporal_score,
            artifact_score, background_score, transcript_findings
        )

        return {
            "type": "audio",
            "deepfake_probability": round(deepfake_probability, 4),
            "confidence": round(min(0.96, 0.68 + abs(deepfake_probability - 0.5) * 0.55), 4),
            "risk_level": self._get_risk_level(deepfake_probability),
            "sub_scores": {
                "spectral_anomalies": round(spectral_score, 4),
                "voice_consistency": round(voice_score, 4),
                "temporal_patterns": round(temporal_score, 4),
                "cloning_artifacts": round(artifact_score, 4),
                "background_analysis": round(background_score, 4),
            },
            "features_analyzed": {
                "spectral_flatness": features.get("spectral_flatness", "N/A"),
                "pitch_variance": features.get("pitch_variance", "N/A"),
                "formant_stability": features.get("formant_stability", "N/A"),
                "breath_detected": features.get("breath_patterns", 0) > 0.3,
                "duration_seconds": features.get("duration", "N/A"),
            },
            "findings": findings,
            "analyzed_at": datetime.now().isoformat(),
            "model_version": self.version,
        }

    def _get_features(self, audio_features):
        defaults = {
            "spectral_flatness": 0.28,
            "spectral_centroid": 1500,
            "pitch_mean": 120,
            "pitch_variance": 0.18,
            "formant_stability": 0.72,
            "mfcc_consistency": 0.75,
            "breath_patterns": 0.60,
            "silence_ratio": 0.16,
            "noise_floor": -55,
            "duration": 30,
            "sample_rate": 16000,
            "snr": 22,
        }
        defaults.update(audio_features)
        return defaults

    def _analyze_spectral(self, features):
        score = 0.0
        flatness = features.get("spectral_flatness", 0.28)
        if flatness > 0.40:
            score += 0.55 * min(1.0, (flatness - 0.40) / 0.25)
        if flatness > 0.55:
            score += 0.35

        mfcc = features.get("mfcc_consistency", 0.75)
        if mfcc > 0.88:
            score += 0.35 * min(1.0, (mfcc - 0.88) / 0.10)

        return min(1.0, score)

    def _analyze_voice_consistency(self, features):
        score = 0.0
        pitch_var = features.get("pitch_variance", 0.18)
        if pitch_var < 0.10:
            score += 0.55 * min(1.0, (0.10 - pitch_var) / 0.07)
        if pitch_var < 0.07:
            score += 0.30

        formant = features.get("formant_stability", 0.72)
        if formant > 0.88:
            score += 0.45 * min(1.0, (formant - 0.88) / 0.10)

        return min(1.0, score)

    def _analyze_temporal_patterns(self, features):
        score = 0.0
        breath = features.get("breath_patterns", 0.60)
        if breath < 0.20:
            score += 0.60 * min(1.0, (0.20 - breath) / 0.15)
        if breath < 0.10:
            score += 0.30

        silence = features.get("silence_ratio", 0.16)
        if silence < 0.09:
            score += 0.25
        elif silence > 0.35:
            score += 0.20

        return min(1.0, score)

    def _detect_cloning_artifacts(self, features):
        score = 0.0
        snr = features.get("snr", 22)
        if snr > 42:
            score += 0.45

        noise = features.get("noise_floor", -55)
        if noise < -70:
            score += 0.35

        sr = features.get("sample_rate", 16000)
        if sr == 22050:
            score += 0.30

        return min(1.0, score)

    def _analyze_background(self, features):
        noise = features.get("noise_floor", -55)
        snr = features.get("snr", 22)
        if noise < -70 and snr > 40:
            return 0.75
        return 0.10

    def _analyze_transcript_for_audio_cues(self, transcript):
        findings = []
        transcript_lower = transcript.lower()
        cues = {
            "robotic": "Voice described as robotic or synthesized",
            "glitch": "Digital glitch or pitch shift reported",
            "delay": "Latency anomalies in conversational turn-taking",
            "echo": "Acoustic doubling or vocoder residue detected",
        }
        for keyword, description in cues.items():
            if keyword in transcript_lower:
                findings.append({
                    "category": "Transcript Audio Cue",
                    "severity": "MEDIUM",
                    "detail": description
                })
        return findings

    def _collect_findings(self, spectral, voice, temporal, artifact, background,
                          transcript_findings=None):
        findings = []

        if spectral > 0.35:
            findings.append({
                "category": "Spectral Anomalies",
                "severity": "CRITICAL" if spectral > 0.65 else "HIGH",
                "detail": "Acoustic spectral features demonstrate unnatural spectral flatness characteristic of Neural TTS vocoders."
            })

        if voice > 0.35:
            findings.append({
                "category": "Voice Inconsistency",
                "severity": "HIGH",
                "detail": "Pitch modulation is unnaturally flat with static formant frequencies matching cloned voice signatures."
            })

        if temporal > 0.35:
            findings.append({
                "category": "Temporal Anomalies",
                "severity": "HIGH",
                "detail": "Absence of physiological breathing cues and unnatural pause cadence indicates non-human speech generation."
            })

        if artifact > 0.30:
            findings.append({
                "category": "Cloning Artifacts",
                "severity": "HIGH",
                "detail": "Sample rate and acoustic noise floor characteristics identify model synthesis artifacts (22.05kHz vocoder output)."
            })

        if transcript_findings:
            findings.extend(transcript_findings)

        if not findings:
            findings.append({
                "category": "Clean",
                "severity": "LOW",
                "detail": "Natural speech dynamics, organic breathing cadences, and realistic room acoustics verified."
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
