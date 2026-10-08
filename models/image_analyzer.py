"""
Image Analysis Model for DeepFake Detection in Financial Documents.
Detects manipulated financial documents, forged signatures, and altered images.
"""
import math
import hashlib
from datetime import datetime


class ImageAnalyzer:
    """
    Image manipulation detection engine for financial documents.
    Analyzes document images for signs of tampering, forgery, and digital manipulation.
    """

    def __init__(self):
        self.name = "ImageAnalyzer"
        self.version = "1.5.0"

    def analyze(self, image_features=None, metadata=None):
        """
        Analyze image features for deepfake/manipulation detection.

        Args:
            image_features (dict): Pre-extracted image features for demo mode.
            metadata (dict): Additional image metadata.

        Returns:
            dict: Analysis results with manipulation probability.
        """
        if image_features is None:
            image_features = {}

        features = self._get_features(image_features)

        # Run analysis modules
        ela_score = self._error_level_analysis(features)
        metadata_score = self._analyze_metadata_consistency(features, metadata)
        font_score = self._analyze_font_consistency(features)
        edge_score = self._analyze_edge_artifacts(features)
        compression_score = self._analyze_compression_artifacts(features)

        raw_score = (
            ela_score * 0.30 +
            metadata_score * 0.20 +
            font_score * 0.20 +
            edge_score * 0.15 +
            compression_score * 0.15
        )

        deepfake_probability = self._sigmoid(raw_score * 5.5 - 2.2)

        findings = self._collect_findings(
            ela_score, metadata_score, font_score, edge_score, compression_score
        )

        return {
            "type": "image",
            "deepfake_probability": round(deepfake_probability, 4),
            "confidence": round(min(0.92, 0.48 + abs(deepfake_probability - 0.5) * 0.85), 4),
            "risk_level": self._get_risk_level(deepfake_probability),
            "sub_scores": {
                "error_level_analysis": round(ela_score, 4),
                "metadata_consistency": round(metadata_score, 4),
                "font_consistency": round(font_score, 4),
                "edge_artifacts": round(edge_score, 4),
                "compression_artifacts": round(compression_score, 4),
            },
            "findings": findings,
            "analyzed_at": datetime.now().isoformat(),
            "model_version": self.version,
        }

    def _get_features(self, image_features):
        defaults = {
            "ela_variance": 0.15,
            "ela_max_diff": 25,
            "jpeg_quality": 85,
            "compression_consistency": 0.9,
            "font_count": 1,
            "font_size_variance": 0.05,
            "edge_sharpness_variance": 0.1,
            "edge_discontinuities": 0,
            "noise_pattern_consistency": 0.85,
            "color_space_consistency": True,
            "exif_present": True,
            "modification_software": None,
            "resolution": (1920, 1080),
        }
        defaults.update(image_features)
        return defaults

    def _error_level_analysis(self, features):
        """Simulate Error Level Analysis (ELA) for tampering detection."""
        score = 0
        ela_var = features.get("ela_variance", 0.15)
        ela_max = features.get("ela_max_diff", 25)

        # High ELA variance indicates manipulation
        if ela_var > 0.35:
            score += 0.5 * min(1.0, (ela_var - 0.35) / 0.3)

        # Large ELA differences indicate splicing
        if ela_max > 60:
            score += 0.4 * min(1.0, (ela_max - 60) / 40)

        return min(1.0, score)

    def _analyze_metadata_consistency(self, features, metadata):
        """Analyze image metadata for inconsistencies."""
        score = 0

        if not features.get("exif_present", True):
            score += 0.2  # Stripped EXIF can be suspicious

        if features.get("modification_software"):
            sw = features["modification_software"].lower()
            suspicious_tools = ["photoshop", "gimp", "paint.net", "fakeapp"]
            for tool in suspicious_tools:
                if tool in sw:
                    score += 0.3
                    break

        if not features.get("color_space_consistency", True):
            score += 0.25

        return min(1.0, score)

    def _analyze_font_consistency(self, features):
        """Analyze font consistency in document images."""
        score = 0

        font_count = features.get("font_count", 1)
        if font_count > 3:
            score += 0.3  # Too many fonts is suspicious

        font_var = features.get("font_size_variance", 0.05)
        if font_var > 0.25:
            score += 0.35  # Inconsistent font sizing

        return min(1.0, score)

    def _analyze_edge_artifacts(self, features):
        """Detect edge artifacts from image splicing."""
        score = 0

        edge_var = features.get("edge_sharpness_variance", 0.1)
        if edge_var > 0.3:
            score += 0.4

        disc = features.get("edge_discontinuities", 0)
        if disc > 2:
            score += 0.3 * min(1.0, disc / 5)

        return min(1.0, score)

    def _analyze_compression_artifacts(self, features):
        """Analyze JPEG compression artifacts."""
        score = 0

        quality = features.get("jpeg_quality", 85)
        consistency = features.get("compression_consistency", 0.9)

        # Double compression detection
        if consistency < 0.7:
            score += 0.45

        # Very low quality might hide manipulation
        if quality < 50:
            score += 0.2

        return min(1.0, score)

    def _collect_findings(self, ela, metadata, font, edge, compression):
        findings = []

        if ela > 0.3:
            findings.append({
                "category": "Error Level Analysis",
                "severity": "HIGH" if ela > 0.6 else "MEDIUM",
                "detail": "ELA reveals inconsistent compression levels across the image, indicating possible digital manipulation or content splicing."
            })

        if metadata > 0.25:
            findings.append({
                "category": "Metadata Inconsistency",
                "severity": "HIGH" if metadata > 0.5 else "MEDIUM",
                "detail": "Image metadata shows signs of editing software or stripped EXIF data suggesting post-processing."
            })

        if font > 0.25:
            findings.append({
                "category": "Font Irregularities",
                "severity": "MEDIUM",
                "detail": "Document shows inconsistent typography that may indicate text overlay or document assembly from multiple sources."
            })

        if edge > 0.25:
            findings.append({
                "category": "Edge Artifacts",
                "severity": "HIGH" if edge > 0.5 else "MEDIUM",
                "detail": "Edge analysis reveals discontinuities consistent with image splicing or object insertion."
            })

        if compression > 0.3:
            findings.append({
                "category": "Compression Artifacts",
                "severity": "MEDIUM",
                "detail": "Double JPEG compression artifacts detected, suggesting the image has been edited and re-saved."
            })

        if not findings:
            findings.append({
                "category": "Clean",
                "severity": "LOW",
                "detail": "No significant image manipulation indicators detected."
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

    def _sigmoid(self, x):
        return 1 / (1 + math.exp(-max(-10, min(10, x))))
