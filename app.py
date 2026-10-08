"""
DeepFake Detection for Financial Communication - Flask Web Application
Main application with REST API and web dashboard.
"""
import json
import os
import sys
from datetime import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import SECRET_KEY, DEBUG, HOST, PORT, SAMPLE_DATA_DIR, RISK_LEVELS
from detectors.ensemble import EnsembleDetector
from utils.report_generator import ReportGenerator

app = Flask(__name__)
app.secret_key = SECRET_KEY

# Initialize detector and report generator
detector = EnsembleDetector()
report_gen = ReportGenerator()


def load_sample_data():
    """Load all sample data for the dashboard."""
    data = {"emails": [], "calls": [], "scenarios": []}

    # Load sample emails
    email_path = os.path.join(SAMPLE_DATA_DIR, "emails", "sample_emails.json")
    if os.path.exists(email_path):
        with open(email_path, 'r', encoding='utf-8') as f:
            data["emails"] = json.load(f)

    # Load sample calls
    calls_path = os.path.join(SAMPLE_DATA_DIR, "transcripts", "sample_calls.json")
    if os.path.exists(calls_path):
        with open(calls_path, 'r', encoding='utf-8') as f:
            data["calls"] = json.load(f)

    # Load multi-modal scenarios
    scenarios_path = os.path.join(SAMPLE_DATA_DIR, "multi_modal_scenarios.json")
    if os.path.exists(scenarios_path):
        with open(scenarios_path, 'r', encoding='utf-8') as f:
            data["scenarios"] = json.load(f)

    return data


# ─── Web Routes ───────────────────────────────────────────────────────────────

@app.route("/")
def index():
    """Main dashboard."""
    sample_data = load_sample_data()
    stats = {
        "total_samples": (len(sample_data["emails"]) +
                          len(sample_data["calls"]) +
                          len(sample_data["scenarios"])),
        "email_count": len(sample_data["emails"]),
        "call_count": len(sample_data["calls"]),
        "scenario_count": len(sample_data["scenarios"]),
    }
    return render_template("index.html", stats=stats, sample_data=sample_data,
                           risk_levels=RISK_LEVELS)


@app.route("/analyze", methods=["GET", "POST"])
def analyze():
    """Analysis page - submit new communication for analysis."""
    result = None
    report = None

    if request.method == "POST":
        comm_type = request.form.get("comm_type", "text")
        text = request.form.get("text_content", "")
        sender_email = request.form.get("sender_email", "")
        claimed_org = request.form.get("claimed_org", "")
        title = request.form.get("title", "Custom Analysis")

        metadata = {}
        if sender_email:
            metadata["sender_email"] = sender_email
        if claimed_org:
            metadata["claimed_organization"] = claimed_org

        communication = {
            "case_id": f"CUSTOM-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "title": title,
            "text": text,
            "metadata": metadata,
        }

        analysis = detector.analyze_communication(communication)
        report = report_gen.generate_report(analysis)
        report["formatted_text"] = report_gen.format_report_text(report)
        result = analysis

    return render_template("analyze.html", result=result, report=report,
                           risk_levels=RISK_LEVELS)


@app.route("/report/<case_id>")
def view_report(case_id):
    """View a specific analysis report."""
    return render_template("report.html", case_id=case_id, risk_levels=RISK_LEVELS)


# ─── API Routes ───────────────────────────────────────────────────────────────

@app.route("/api/analyze", methods=["POST"])
def api_analyze():
    """
    REST API endpoint for deepfake analysis.

    Accepts JSON with:
        - text: Text content to analyze
        - audio_features: Pre-extracted audio features (dict)
        - video_features: Pre-extracted video features (dict)
        - image_features: Pre-extracted image features (dict)
        - metadata: Communication metadata (dict)
        - title: Optional title for the analysis
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    communication = {
        "case_id": data.get("case_id", f"API-{datetime.now().strftime('%Y%m%d%H%M%S')}"),
        "title": data.get("title", "API Analysis"),
        "text": data.get("text", ""),
        "audio_features": data.get("audio_features"),
        "video_features": data.get("video_features"),
        "image_features": data.get("image_features"),
        "metadata": data.get("metadata", {}),
        "transcript": data.get("transcript"),
    }

    analysis = detector.analyze_communication(communication)
    report = report_gen.generate_report(analysis)

    return jsonify({
        "analysis": analysis,
        "report": report,
    })


@app.route("/api/analyze/text", methods=["POST"])
def api_analyze_text():
    """Quick text-only analysis endpoint."""
    data = request.get_json()
    if not data or not data.get("text"):
        return jsonify({"error": "No text provided"}), 400

    from models.text_analyzer import TextAnalyzer
    analyzer = TextAnalyzer()
    result = analyzer.analyze(data["text"], data.get("metadata"))
    return jsonify(result)


@app.route("/api/analyze/sample/<sample_id>", methods=["GET"])
def api_analyze_sample(sample_id):
    """Analyze a specific sample by ID."""
    sample_data = load_sample_data()

    # Search all sample collections
    sample = None
    for collection in [sample_data["emails"], sample_data["calls"], sample_data["scenarios"]]:
        for item in collection:
            if item["id"] == sample_id:
                sample = item
                break
        if sample:
            break

    if not sample:
        return jsonify({"error": f"Sample '{sample_id}' not found"}), 404

    # Build communication object
    communication = {
        "case_id": sample["id"],
        "title": sample.get("category", sample.get("title", "Sample Analysis")),
        "text": sample.get("body", sample.get("text", sample.get("transcript", ""))),
        "audio_features": sample.get("audio_features"),
        "video_features": sample.get("video_features"),
        "image_features": sample.get("image_features"),
        "metadata": sample.get("metadata", {}),
        "transcript": sample.get("transcript"),
    }

    analysis = detector.analyze_communication(communication)
    report = report_gen.generate_report(analysis)

    return jsonify({
        "sample": sample,
        "analysis": analysis,
        "report": report,
        "expected": sample.get("expected_result", {}),
    })


@app.route("/api/samples", methods=["GET"])
def api_list_samples():
    """List all available sample data."""
    sample_data = load_sample_data()
    samples = []
    for collection_name, collection in sample_data.items():
        for item in collection:
            samples.append({
                "id": item["id"],
                "label": item.get("label", "UNKNOWN"),
                "category": item.get("category", item.get("title", "N/A")),
                "collection": collection_name,
            })
    return jsonify({"samples": samples, "total": len(samples)})


@app.route("/api/demo/run-all", methods=["GET"])
def api_run_all_demos():
    """Run analysis on all sample data and return results."""
    sample_data = load_sample_data()
    results = []

    all_samples = (
        [(s, "email") for s in sample_data["emails"]] +
        [(s, "call") for s in sample_data["calls"]] +
        [(s, "scenario") for s in sample_data["scenarios"]]
    )

    for sample, stype in all_samples:
        communication = {
            "case_id": sample["id"],
            "title": sample.get("category", sample.get("title", "")),
            "text": sample.get("body", sample.get("text", sample.get("transcript", ""))),
            "audio_features": sample.get("audio_features"),
            "video_features": sample.get("video_features"),
            "image_features": sample.get("image_features"),
            "metadata": sample.get("metadata", {}),
            "transcript": sample.get("transcript"),
        }

        analysis = detector.analyze_communication(communication)

        expected = sample.get("expected_result", {})
        actual_prob = analysis["overall"]["deepfake_probability"]
        actual_risk = analysis["overall"]["risk_level"]

        # Check if detection matches expected
        passed = True
        if "min_probability" in expected:
            passed = passed and actual_prob >= expected["min_probability"]
        if "max_probability" in expected:
            passed = passed and actual_prob <= expected["max_probability"]

        results.append({
            "id": sample["id"],
            "type": stype,
            "label": sample.get("label", "UNKNOWN"),
            "category": sample.get("category", sample.get("title", "")),
            "actual_probability": actual_prob,
            "actual_risk_level": actual_risk,
            "expected": expected,
            "test_passed": passed,
            "findings_count": len(analysis["overall"]["all_findings"]),
            "action_plan": analysis["action_plan"],
        })

    passed_count = sum(1 for r in results if r["test_passed"])

    return jsonify({
        "results": results,
        "summary": {
            "total": len(results),
            "passed": passed_count,
            "failed": len(results) - passed_count,
            "accuracy": f"{passed_count/len(results)*100:.1f}%" if results else "N/A",
        }
    })


# ─── Error Handlers ──────────────────────────────────────────────────────────

@app.errorhandler(404)
def not_found(e):
    if request.path.startswith("/api/"):
        return jsonify({"error": "Endpoint not found"}), 404
    return render_template("index.html", error="Page not found"), 404


@app.errorhandler(500)
def server_error(e):
    if request.path.startswith("/api/"):
        return jsonify({"error": "Internal server error"}), 500
    return render_template("index.html", error="Server error"), 500


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("  🛡️  DeepFake Detection for Financial Communication")
    print("  " + "=" * 56)
    print(f"  Server: http://{HOST}:{PORT}")
    print(f"  API:    http://{HOST}:{PORT}/api/")
    print(f"  Demo:   http://{HOST}:{PORT}/api/demo/run-all")
    print("=" * 60 + "\n")
    app.run(host=HOST, port=PORT, debug=DEBUG)
