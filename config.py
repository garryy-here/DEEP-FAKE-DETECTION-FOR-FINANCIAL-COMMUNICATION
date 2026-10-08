"""
Configuration for DeepFake Detection for Financial Communication
"""
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Flask config
SECRET_KEY = os.environ.get("SECRET_KEY", "deepfake-detect-hackathon-2026")
DEBUG = True
HOST = "127.0.0.1"
PORT = 5000

# Detection thresholds
THRESHOLDS = {
    "text": {
        "high_risk": 0.75,
        "medium_risk": 0.45,
        "low_risk": 0.20,
    },
    "audio": {
        "high_risk": 0.70,
        "medium_risk": 0.40,
        "low_risk": 0.15,
    },
    "image": {
        "high_risk": 0.72,
        "medium_risk": 0.42,
        "low_risk": 0.18,
    },
    "video": {
        "high_risk": 0.68,
        "medium_risk": 0.38,
        "low_risk": 0.12,
    },
}

# Risk level labels
RISK_LEVELS = {
    "CRITICAL": {"min": 0.85, "color": "#dc2626", "label": "Critical - Immediate Action Required"},
    "HIGH": {"min": 0.65, "color": "#ea580c", "label": "High Risk - Likely Manipulated"},
    "MEDIUM": {"min": 0.40, "color": "#d97706", "label": "Medium Risk - Suspicious Indicators"},
    "LOW": {"min": 0.15, "color": "#2563eb", "label": "Low Risk - Minor Anomalies"},
    "CLEAN": {"min": 0.0, "color": "#16a34a", "label": "Clean - No Manipulation Detected"},
}

# Sample data directory
SAMPLE_DATA_DIR = os.path.join(BASE_DIR, "sample_data")

# Report output directory
REPORTS_DIR = os.path.join(BASE_DIR, "sample_data", "reports")

# Feature weights for ensemble model
ENSEMBLE_WEIGHTS = {
    "linguistic_analysis": 0.25,
    "metadata_analysis": 0.20,
    "behavioral_analysis": 0.20,
    "statistical_analysis": 0.15,
    "pattern_analysis": 0.20,
}

# Action plan templates
ACTION_PLANS = {
    "CRITICAL": [
        "🚨 IMMEDIATELY freeze all related transactions",
        "🔒 Quarantine the communication and preserve evidence chain",
        "📞 Alert Chief Compliance Officer and CISO within 1 hour",
        "🏛️ File Suspicious Activity Report (SAR) with FinCEN",
        "👮 Notify law enforcement if fraud amount exceeds $50,000",
        "📋 Document all findings with timestamps for legal proceedings",
        "🔍 Launch full forensic investigation of related accounts",
        "📧 Issue internal alert to all financial operations teams",
    ],
    "HIGH": [
        "⚠️ Flag communication for senior compliance review",
        "🔍 Conduct enhanced due diligence on sender/source",
        "📊 Cross-reference with known deepfake pattern databases",
        "📞 Verify communication through independent callback",
        "📋 Create incident ticket with full analysis details",
        "🕐 Set 24-hour review deadline for compliance team",
        "📧 Notify department head and risk management",
    ],
    "MEDIUM": [
        "📋 Add to compliance review queue (Priority: Medium)",
        "🔍 Perform additional verification of sender identity",
        "📊 Compare against historical communication patterns",
        "📞 Conduct verbal verification with known contact number",
        "📝 Document anomalies and monitoring observations",
        "🕐 Schedule review within 72 hours",
    ],
    "LOW": [
        "📝 Log findings in monitoring system",
        "📊 Add to statistical baseline for future comparison",
        "🔍 Continue standard monitoring protocols",
        "📋 Include in weekly compliance summary report",
    ],
    "CLEAN": [
        "✅ Communication verified - proceed with standard workflow",
        "📝 Log verification result for audit trail",
        "📊 Update baseline communication profile",
    ],
}
