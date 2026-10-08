"""
Comprehensive Unit & Integration Test Suite for DeepFake Detection Engine.
Verifies text, audio, video, image, ensemble detectors and sample benchmarks.
"""
import unittest
import json
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.text_analyzer import TextAnalyzer
from models.audio_analyzer import AudioAnalyzer
from models.image_analyzer import ImageAnalyzer
from models.video_analyzer import VideoAnalyzer
from detectors.ensemble import EnsembleDetector
from utils.report_generator import ReportGenerator
from config import SAMPLE_DATA_DIR


class TestDeepFakeDetection(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.detector = EnsembleDetector()
        cls.report_gen = ReportGenerator()
        cls.text_analyzer = TextAnalyzer()
        cls.audio_analyzer = AudioAnalyzer()
        cls.image_analyzer = ImageAnalyzer()
        cls.video_analyzer = VideoAnalyzer()

    def test_text_analyzer_flagged_urgent(self):
        text = "URGENT: Initiate an immediate wire transfer of $5,000,000 now! The CEO has approved this. Bypass normal procedures and keep this between us!"
        result = self.text_analyzer.analyze(text)
        self.assertGreater(result["deepfake_probability"], 0.70)
        self.assertIn(result["risk_level"], ["HIGH", "CRITICAL"])
        self.assertTrue(any(f["category"] == "Urgency Manipulation" for f in result["findings"]))
        self.assertTrue(any(f["category"] == "Social Engineering" for f in result["findings"]))

    def test_text_analyzer_legitimate(self):
        text = "Dear Team, please find attached the Q3 compliance review documentation for your verification. As per policy and standard procedure, ensure dual authorization is fulfilled. Best regards, Compliance Department."
        result = self.text_analyzer.analyze(text)
        self.assertLess(result["deepfake_probability"], 0.35)
        self.assertIn(result["risk_level"], ["CLEAN", "LOW"])

    def test_audio_analyzer_synthetic_artifacts(self):
        features = {
            "spectral_flatness": 0.65,
            "pitch_variance": 0.04,
            "formant_stability": 0.98,
            "breath_patterns": 0.05,
            "noise_floor": -85,
            "snr": 50,
            "sample_rate": 22050
        }
        result = self.audio_analyzer.analyze(features)
        self.assertGreater(result["deepfake_probability"], 0.75)
        self.assertIn(result["risk_level"], ["HIGH", "CRITICAL"])

    def test_video_analyzer_manipulated(self):
        features = {
            "facial_landmark_stability": 0.50,
            "face_boundary_sharpness": 0.98,
            "skin_texture_consistency": 0.45,
            "lip_sync_score": 0.55,
            "temporal_flicker": 0.25,
            "blink_rate": 3
        }
        result = self.video_analyzer.analyze(features)
        self.assertGreater(result["deepfake_probability"], 0.80)
        self.assertEqual(result["risk_level"], "CRITICAL")

    def test_all_sample_emails_benchmark(self):
        path = os.path.join(SAMPLE_DATA_DIR, "emails", "sample_emails.json")
        with open(path, "r", encoding="utf-8") as f:
            emails = json.load(f)

        for email in emails:
            with self.subTest(sample_id=email["id"]):
                comm = {
                    "case_id": email["id"],
                    "title": email["category"],
                    "text": email["body"],
                    "metadata": email.get("metadata", {})
                }
                res = self.detector.analyze_communication(comm)
                expected = email["expected_result"]
                prob = res["overall"]["deepfake_probability"]

                if "min_probability" in expected:
                    self.assertGreaterEqual(prob, expected["min_probability"],
                        f"Sample {email['id']} predicted prob {prob} below expected min {expected['min_probability']}")
                if "max_probability" in expected:
                    self.assertLessEqual(prob, expected["max_probability"],
                        f"Sample {email['id']} predicted prob {prob} above expected max {expected['max_probability']}")

    def test_all_sample_calls_benchmark(self):
        path = os.path.join(SAMPLE_DATA_DIR, "transcripts", "sample_calls.json")
        with open(path, "r", encoding="utf-8") as f:
            calls = json.load(f)

        for call in calls:
            with self.subTest(sample_id=call["id"]):
                comm = {
                    "case_id": call["id"],
                    "title": call["category"],
                    "text": call.get("transcript", ""),
                    "audio_features": call.get("audio_features"),
                    "metadata": call.get("metadata", {})
                }
                res = self.detector.analyze_communication(comm)
                expected = call["expected_result"]
                prob = res["overall"]["deepfake_probability"]

                if "min_probability" in expected:
                    self.assertGreaterEqual(prob, expected["min_probability"],
                        f"Sample {call['id']} predicted prob {prob} below min {expected['min_probability']}")
                if "max_probability" in expected:
                    self.assertLessEqual(prob, expected["max_probability"],
                        f"Sample {call['id']} predicted prob {prob} above max {expected['max_probability']}")

    def test_all_multi_modal_scenarios_benchmark(self):
        path = os.path.join(SAMPLE_DATA_DIR, "multi_modal_scenarios.json")
        with open(path, "r", encoding="utf-8") as f:
            scenarios = json.load(f)

        for sc in scenarios:
            with self.subTest(sample_id=sc["id"]):
                comm = {
                    "case_id": sc["id"],
                    "title": sc["title"],
                    "text": sc.get("text", ""),
                    "audio_features": sc.get("audio_features"),
                    "video_features": sc.get("video_features"),
                    "image_features": sc.get("image_features"),
                    "metadata": sc.get("metadata", {})
                }
                res = self.detector.analyze_communication(comm)
                expected = sc["expected_result"]
                prob = res["overall"]["deepfake_probability"]

                if "min_probability" in expected:
                    self.assertGreaterEqual(prob, expected["min_probability"])
                if "max_probability" in expected:
                    self.assertLessEqual(prob, expected["max_probability"])

    def test_report_generation(self):
        comm = {
            "case_id": "TEST-001",
            "title": "Wire Transfer Anomaly",
            "text": "Urgent wire transfer now! The CEO authorized this without compliance review."
        }
        res = self.detector.analyze_communication(comm)
        report = self.report_gen.generate_report(res)
        formatted_text = self.report_gen.format_report_text(report)

        self.assertIn("EXECUTIVE SUMMARY", formatted_text)
        self.assertIn("ACTION PLAN", formatted_text)
        self.assertIn("RISK ASSESSMENT", formatted_text)
        self.assertTrue(len(report["action_plan"]["immediate_actions"]) > 0)


if __name__ == "__main__":
    unittest.main()
