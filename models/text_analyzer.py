"""
Text Analysis Model for DeepFake Detection in Financial Communications.
Uses NLP techniques to detect AI-generated or manipulated text.
"""
import re
import math
from collections import Counter
from datetime import datetime


class TextAnalyzer:
    """
    Multi-layered text analysis engine that detects deepfake / AI-generated
    financial communications using linguistic, statistical, and behavioral signals.
    """

    URGENCY_KEYWORDS = [
        "immediate", "urgently", "urgent", "immediate action", "wire transfer",
        "act now", "time sensitive", "expires today", "do not delay",
        "must be completed", "deadline", "within the hour", "within 24 hours",
        "within 4 hours", "asap", "emergency transfer", "emergency acquisition",
        "confidential", "keep this between us", "bypass", "override",
        "skip verification", "avoid service disruption", "suspended",
        "market open", "effective immediately"
    ]

    IMPERSONATION_SIGNALS = [
        "as discussed", "phone conversation", "as i mentioned", "following up",
        "as we agreed", "ceo has approved", "ceo explained", "board has authorized",
        "board resolution", "management directive", "executive order",
        "chairman has personally approved", "chairman's request",
        "audit engagement partner", "corner office", "escrow account",
        "strategic restructuring"
    ]

    SOCIAL_ENGINEERING_PATTERNS = [
        "don't mention this to", "keep this confidential", "only you and i",
        "only you can handle", "i trust you", "don't involve anyone",
        "don't involve", "this is between us", "keep this between us", "between us",
        "special authorization", "override the usual", "i'll explain later", "no time to explain",
        "skip the normal", "bypass normal", "bypass procedures", "bypass the vendor verification",
        "waived", "no need for the standard", "do not reply to previous"
    ]

    LEGITIMATE_MARKERS = [
        "please verify", "compliance review", "audit trail",
        "dual authorization", "per standard procedure",
        "attached documentation", "reference number",
        "regulatory requirement", "as per policy",
        "monthly statement", "online banking portal",
        "will never ask you for your password", "quarterly compliance review",
        "press release", "investor relations", "regulation fd"
    ]

    def __init__(self):
        self.name = "TextAnalyzer"
        self.version = "2.2.0"

    def analyze(self, text, metadata=None):
        if not text or not text.strip():
            return self._empty_result()

        text_lower = text.lower()
        words = text_lower.split()

        urgency_score = self._analyze_urgency(text_lower)
        impersonation_score = self._analyze_impersonation(text_lower)
        social_eng_score = self._analyze_social_engineering(text_lower)
        linguistic_score = self._analyze_linguistic_quality(text, words)
        statistical_score = self._analyze_statistical_patterns(words)
        consistency_score = self._analyze_consistency(text, metadata)
        legitimacy_score = self._analyze_legitimacy_markers(text_lower)

        # Base composite score
        if metadata:
            threat_score = (
                urgency_score * 0.28 +
                impersonation_score * 0.24 +
                social_eng_score * 0.28 +
                consistency_score * 0.20
            )
        else:
            threat_score = (
                urgency_score * 0.35 +
                impersonation_score * 0.30 +
                social_eng_score * 0.35
            )

        style_score = linguistic_score * 0.5 + statistical_score * 0.5

        raw_score = threat_score * 0.75 + style_score * 0.25

        # Factor in legitimacy markers
        if legitimacy_score > 0.25:
            raw_score = max(0.0, raw_score - (legitimacy_score * 0.65))

        # Calibrated mapping
        if raw_score >= 0.50:
            deepfake_probability = min(0.98, 0.75 + (raw_score - 0.50) * 0.46)
        elif raw_score >= 0.25:
            deepfake_probability = 0.45 + (raw_score - 0.25) * 1.20
        else:
            deepfake_probability = max(0.02, raw_score * 0.8)

        # Hard guardrails for obvious flags
        if threat_score > 0.45 and legitimacy_score < 0.2:
            deepfake_probability = max(deepfake_probability, 0.75)
        if threat_score > 0.65:
            deepfake_probability = max(deepfake_probability, 0.86)
        if legitimacy_score >= 0.35 and threat_score < 0.2:
            deepfake_probability = min(deepfake_probability, 0.14)

        findings = self._collect_findings(
            text_lower, urgency_score, impersonation_score,
            social_eng_score, linguistic_score, statistical_score,
            consistency_score, legitimacy_score
        )

        return {
            "type": "text",
            "deepfake_probability": round(deepfake_probability, 4),
            "confidence": round(min(0.96, 0.65 + abs(deepfake_probability - 0.5) * 0.6), 4),
            "risk_level": self._get_risk_level(deepfake_probability),
            "sub_scores": {
                "urgency_manipulation": round(urgency_score, 4),
                "impersonation_signals": round(impersonation_score, 4),
                "social_engineering": round(social_eng_score, 4),
                "linguistic_anomalies": round(linguistic_score, 4),
                "statistical_deviation": round(statistical_score, 4),
                "consistency_issues": round(consistency_score, 4),
                "legitimacy_markers": round(legitimacy_score, 4),
            },
            "findings": findings,
            "word_count": len(words),
            "analyzed_at": datetime.now().isoformat(),
            "model_version": self.version,
        }

    def _analyze_urgency(self, text):
        score = 0.0
        matches = 0
        for kw in self.URGENCY_KEYWORDS:
            if kw in text:
                matches += 1

        if matches >= 1:
            score += 0.30
        if matches >= 2:
            score += 0.30
        if matches >= 3:
            score += 0.25
        if matches >= 4:
            score += 0.15

        exclamation_count = text.count("!")
        if exclamation_count >= 1:
            score += min(0.2, exclamation_count * 0.08)

        return min(1.0, score)

    def _analyze_impersonation(self, text):
        score = 0.0
        matches = 0
        for signal in self.IMPERSONATION_SIGNALS:
            if signal in text:
                matches += 1

        if matches >= 1:
            score += 0.35
        if matches >= 2:
            score += 0.35
        if matches >= 3:
            score += 0.20

        titles = ["ceo", "cfo", "chairman", "board", "director", "partner"]
        title_count = sum(1 for t in titles if t in text)
        if title_count >= 2:
            score += 0.2

        return min(1.0, score)

    def _analyze_social_engineering(self, text):
        score = 0.0
        matches = 0
        for pat in self.SOCIAL_ENGINEERING_PATTERNS:
            if pat in text:
                matches += 1

        if matches >= 1:
            score += 0.40
        if matches >= 2:
            score += 0.35
        if matches >= 3:
            score += 0.25

        bypass_words = ["bypass", "override", "skip", "waive", "ignore", "don't involve"]
        for bw in bypass_words:
            if bw in text:
                score += 0.20
                break

        return min(1.0, score)

    def _analyze_linguistic_quality(self, text, words):
        score = 0.0
        sentences = [s.strip() for s in re.split(r'[.!?]+', text) if s.strip()]
        if len(sentences) > 2:
            lengths = [len(s.split()) for s in sentences]
            avg_len = sum(lengths) / len(lengths)
            variance = sum((l - avg_len) ** 2 for l in lengths) / len(lengths)
            if variance < 5 and avg_len > 6:
                score += 0.35

        formal_markers = ["hereby", "aforementioned", "henceforth", "pursuant to", "notwithstanding"]
        formal_count = sum(1 for m in formal_markers if m in text.lower())
        if formal_count >= 1:
            score += 0.25
        if formal_count >= 2:
            score += 0.25

        return min(1.0, score)

    def _analyze_statistical_patterns(self, words):
        if len(words) < 5:
            return 0.0

        score = 0.0
        freq = Counter(words)
        sorted_freq = sorted(freq.values(), reverse=True)
        if len(sorted_freq) > 5:
            expected_ratio = sorted_freq[0] / max(sorted_freq[1], 1)
            if expected_ratio < 1.1 or expected_ratio > 9:
                score += 0.25

        char_freq = Counter(c.lower() for c in ''.join(words) if c.isalpha())
        total_chars = sum(char_freq.values())
        if total_chars > 0:
            expected = {'e': 0.127, 't': 0.091, 'a': 0.082, 'o': 0.075, 'i': 0.070}
            deviation = sum(abs((char_freq.get(k, 0) / total_chars) - v) for k, v in expected.items())
            if deviation > 0.14:
                score += 0.30

        return min(1.0, score)

    def _analyze_consistency(self, text, metadata):
        score = 0.0
        if not metadata:
            return score

        sender = metadata.get("sender_email", "")
        claimed_org = metadata.get("claimed_organization", "")

        # Typosquatting / domain impersonation detection
        if sender and claimed_org:
            clean_claimed = re.sub(r'[^a-zA-Z0-9]', '', claimed_org).lower()
            sender_domain = sender.split("@")[-1].lower() if "@" in sender else ""
            clean_domain = sender_domain.split(".")[0]

            # Detect digit substitution e.g., 'financ1al', 'amaz0n'
            digit_subs = any(c.isdigit() for c in clean_domain)
            if digit_subs:
                score += 0.50

            if clean_claimed not in clean_domain and clean_domain not in clean_claimed:
                score += 0.35

        # Email auth check (SPF / DKIM failure is a major spoofing indicator)
        if metadata.get("spf_pass") is False:
            score += 0.35
        if metadata.get("dkim_pass") is False:
            score += 0.35

        # Irregular hour check
        ts = metadata.get("timestamp", "")
        if ts:
            try:
                dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
                if dt.hour < 5 or dt.hour > 21:
                    score += 0.15
            except Exception:
                pass

        return min(1.0, score)

    def _analyze_legitimacy_markers(self, text):
        score = 0.0
        matches = 0
        for marker in self.LEGITIMATE_MARKERS:
            if marker in text:
                matches += 1

        if matches >= 1:
            score += 0.35
        if matches >= 2:
            score += 0.35
        if matches >= 3:
            score += 0.30

        return min(1.0, score)

    def _collect_findings(self, text, urgency, impersonation, social_eng,
                          linguistic, statistical, consistency, legitimacy):
        findings = []

        if urgency > 0.25:
            findings.append({
                "category": "Urgency Manipulation",
                "severity": "HIGH" if urgency > 0.55 else "MEDIUM",
                "detail": "Detected artificial urgency tactics designed to pressure immediate fund execution without customary verification."
            })

        if impersonation > 0.25:
            findings.append({
                "category": "Impersonation Signals",
                "severity": "HIGH" if impersonation > 0.55 else "MEDIUM",
                "detail": "Communication contains executive impersonation signals, claiming unauthorized managerial or board mandates."
            })

        if social_eng > 0.25:
            findings.append({
                "category": "Social Engineering",
                "severity": "CRITICAL" if social_eng > 0.55 else "HIGH",
                "detail": "Detected explicit coercion to bypass dual authorization, avoid compliance teams, or enforce secrecy."
            })

        if consistency > 0.30:
            findings.append({
                "category": "Consistency Issues",
                "severity": "CRITICAL" if consistency > 0.6 else "HIGH",
                "detail": "Sender domain irregularities, typosquatting, or failing SPF/DKIM verification checks detected."
            })

        if linguistic > 0.30:
            findings.append({
                "category": "Linguistic Anomalies",
                "severity": "MEDIUM",
                "detail": "Text exhibits robotic/template phrasing consistent with AI generation and synthetic templates."
            })

        if legitimacy > 0.40 and not findings:
            findings.append({
                "category": "Clean",
                "severity": "LOW",
                "detail": "Communication contains established corporate authentication protocols, dual authorizations, and official disclosure language."
            })

        if not findings:
            findings.append({
                "category": "Clean",
                "severity": "LOW",
                "detail": "No significant manipulation indicators detected in this communication."
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

    def _empty_result(self):
        return {
            "type": "text",
            "deepfake_probability": 0.0,
            "confidence": 0.0,
            "risk_level": "CLEAN",
            "sub_scores": {},
            "findings": [{"category": "Error", "severity": "LOW", "detail": "No text provided for analysis."}],
            "word_count": 0,
            "analyzed_at": datetime.now().isoformat(),
            "model_version": self.version,
        }
