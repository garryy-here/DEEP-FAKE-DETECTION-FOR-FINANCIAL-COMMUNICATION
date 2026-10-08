#!/usr/bin/env python3
"""
FinShield AI - Command Line Interface (CLI)
DeepFake Detection for Financial Communication
"""
import argparse
import json
import os
import sys

# Ensure UTF-8 output on Windows consoles
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

# Ensure root is in path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from detectors.ensemble import EnsembleDetector
from utils.report_generator import ReportGenerator
from config import SAMPLE_DATA_DIR


def print_banner():
    banner = """
======================================================================
     FinShield AI - DeepFake Detection for Financial Communication
         Multi-Modal Verification & Action Planning System
======================================================================
"""
    print(banner)


def load_all_samples():
    samples = []
    
    # Emails
    p = os.path.join(SAMPLE_DATA_DIR, "emails", "sample_emails.json")
    if os.path.exists(p):
        with open(p, "r", encoding="utf-8") as f:
            for item in json.load(f):
                item["_type"] = "Email"
                samples.append(item)

    # Calls
    p = os.path.join(SAMPLE_DATA_DIR, "transcripts", "sample_calls.json")
    if os.path.exists(p):
        with open(p, "r", encoding="utf-8") as f:
            for item in json.load(f):
                item["_type"] = "Voice Call"
                samples.append(item)

    # Multi-modal
    p = os.path.join(SAMPLE_DATA_DIR, "multi_modal_scenarios.json")
    if os.path.exists(p):
        with open(p, "r", encoding="utf-8") as f:
            for item in json.load(f):
                item["_type"] = "Multi-Modal"
                samples.append(item)

    return samples


def run_demo_mode():
    detector = EnsembleDetector()
    samples = load_all_samples()

    print(f"\n[*] Running Benchmark Suite across {len(samples)} financial communication cases...\n")
    print(f"{'ID':<11} | {'TYPE':<12} | {'GROUND TRUTH':<11} | {'PROBABILITY':<12} | {'RISK LEVEL':<10} | {'STATUS':<6}")
    print("-" * 75)

    passed_count = 0
    for s in samples:
        comm = {
            "case_id": s["id"],
            "title": s.get("category", s.get("title", "")),
            "text": s.get("body", s.get("text", s.get("transcript", ""))),
            "audio_features": s.get("audio_features"),
            "video_features": s.get("video_features"),
            "image_features": s.get("image_features"),
            "metadata": s.get("metadata", {}),
            "transcript": s.get("transcript"),
        }

        res = detector.analyze_communication(comm)
        prob = res["overall"]["deepfake_probability"]
        risk = res["overall"]["risk_level"]
        expected = s.get("expected_result", {})

        passed = True
        if "min_probability" in expected and prob < expected["min_probability"]:
            passed = False
        if "max_probability" in expected and prob > expected["max_probability"]:
            passed = False

        if passed:
            passed_count += 1
            status = "✓ PASS"
        else:
            status = "✗ FAIL"

        label = s.get("label", "UNKNOWN")
        print(f"{s['id']:<11} | {s['_type']:<12} | {label:<11} | {prob*100:>6.1f}%     | {risk:<10} | {status:<6}")

    print("-" * 75)
    accuracy = (passed_count / len(samples) * 100) if samples else 0
    print(f"\n[+] Benchmark Complete: {passed_count}/{len(samples)} cases passed ({accuracy:.1f}% accuracy)\n")


def inspect_sample(sample_id):
    detector = EnsembleDetector()
    report_gen = ReportGenerator()
    samples = load_all_samples()

    target = next((s for s in samples if s["id"].upper() == sample_id.upper()), None)
    if not target:
        print(f"[!] Error: Sample with ID '{sample_id}' not found.")
        print(f"    Available IDs: {', '.join(s['id'] for s in samples)}")
        return

    comm = {
        "case_id": target["id"],
        "title": target.get("category", target.get("title", "")),
        "text": target.get("body", target.get("text", target.get("transcript", ""))),
        "audio_features": target.get("audio_features"),
        "video_features": target.get("video_features"),
        "image_features": target.get("image_features"),
        "metadata": target.get("metadata", {}),
        "transcript": target.get("transcript"),
    }

    print(f"\n[*] Analyzing Case {target['id']}: {comm['title']}...")
    analysis = detector.analyze_communication(comm)
    report = report_gen.generate_report(analysis)

    print("\n" + report_gen.format_report_text(report))


def analyze_custom_text(text, sender=None, org=None):
    detector = EnsembleDetector()
    report_gen = ReportGenerator()

    metadata = {}
    if sender:
        metadata["sender_email"] = sender
    if org:
        metadata["claimed_organization"] = org

    comm = {
        "case_id": "CLI-CUSTOM",
        "title": "Ad-Hoc Financial Communication Check",
        "text": text,
        "metadata": metadata
    }

    print("\n[*] Analyzing submitted financial communication...")
    analysis = detector.analyze_communication(comm)
    report = report_gen.generate_report(analysis)

    print("\n" + report_gen.format_report_text(report))


def main():
    print_banner()
    parser = argparse.ArgumentParser(description="FinShield AI DeepFake Detection CLI")
    parser.add_argument("--demo", action="store_true", help="Run full benchmark test across all pre-checked samples")
    parser.add_argument("--sample", type=str, help="Inspect a specific pre-checked sample (e.g. EMAIL-001, CALL-001, MULTI-001)")
    parser.add_argument("--text", type=str, help="Analyze custom text for deepfake manipulation")
    parser.add_argument("--sender", type=str, help="Optional sender email for custom text")
    parser.add_argument("--org", type=str, help="Optional claimed organization name for custom text")

    args = parser.parse_args()

    if args.demo:
        run_demo_mode()
    elif args.sample:
        inspect_sample(args.sample)
    elif args.text:
        analyze_custom_text(args.text, args.sender, args.org)
    else:
        # Default behavior: run demo mode
        run_demo_mode()
        print("Tip: Use `python cli.py --sample EMAIL-001` or `python cli.py --help` for more options.")


if __name__ == "__main__":
    main()
