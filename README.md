# 🛡️ FinShield AI — DeepFake Detection for Financial Communication

> **Hackathon Edition** | An end-to-end multi-modal deepfake detection and incident response planning system designed for financial institutions, wealth management firms, and corporate treasuries.

---

## 📌 Executive Summary & Problem Statement

Financial institutions and corporations are facing an escalating wave of **AI-orchestrated financial fraud**:
1. **CEO & Executive Video Cloning**: Deepfake video calls impersonating C-suite leaders authorizing emergency M&A transfers (such as the real-world $25M Hong Kong multinational fraud).
2. **Synthetic Voice Audio Impersonation**: Neural TTS models spoofing corporate officers or audit partners over phone lines requesting emergency banking routing updates.
3. **AI-Generated Business Email Compromise (BEC)**: Highly sophisticated, urgency-driven spear-phishing with automated typosquatting, impersonation signals, and coercive social engineering.
4. **Document & Wire Forgery**: Spliced signatures, altered invoice metadata, and modified SWIFT routing instructions.

**FinShield AI** solves this crisis by providing a multi-layered verification engine that analyzes financial communications across text, voice, video, and document modalities, yielding an instant risk score, granular anomaly breakdown, and an **automated, regulatory-compliant Action Plan** for freeze, review, SAR reporting, and escalation.

---

## 🚀 Key Features

- **Multi-Modal Detection Engine**:
  - 📝 **Text Analyzer**: Detects urgency manipulation, executive impersonation, social engineering, linguistic AI uniformity, typosquatting, and SPF/DKIM authentication failures.
  - 🎙️ **Audio Analyzer**: Identifies synthetic vocoder artifacts (spectral flatness, static formants, flat pitch modulation, absence of human breathing cadence).
  - 🎥 **Video Analyzer**: Flags face-swapping boundary warping, viseme-phoneme lip-sync misalignment, inter-frame flicker, and abnormal biological signals (hypo-blinking).
  - 📄 **Document / Image Forensics**: Detects Error Level Analysis (ELA) compression variance, spliced fonts, and altered metadata.
- **Ensemble Fusion Model**:
  - Dynamically weights available modalities and applies fraud-aware threat scaling.
  - Multi-vector correlation flags coordinated attacks where multiple channels are compromised simultaneously.
- **Automated Incident Response & Action Planning**:
  - Immediate operational instructions (e.g., immediate transaction freeze, forensic evidence quarantine, dual authorization callback).
  - Legal & regulatory compliance roadmap (SAR filing timeline under BSA/AML, FinCEN notice, CISO/CCO alerting).
- **Interactive Web Dashboard & REST API**:
  - Beautiful dark-mode UI with live SVG probability gauges, sub-score bars, and modal inspectors.
  - 100% pre-checked benchmark suite with 11 realistic cases (emails, phone calls, multi-modal incidents).
  - Ad-hoc verification portal for testing custom communication text and metadata.
- **Zero-Dependency Core**:
  - All detection models and report generation operate using Python's standard library for maximum portability, speed (<10ms execution), and resilience.

---

## 📊 Pre-Checked Benchmark Cases

The repository includes pre-loaded, verified benchmark datasets in `sample_data/`:

| Case ID | Channel | Scenario Description | Ground Truth | Detection Result | Risk Level | Status |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: |
| **EMAIL-001** | Email | CEO Urgent Wire ($2.45M Acquisition) | **DEEPFAKE** | **86.0%** | `CRITICAL` | `PASS` |
| **EMAIL-002** | Email | Q3 Compliance Documentation Review | **LEGITIMATE** | **2.0%** | `CLEAN` | `PASS` |
| **EMAIL-003** | Email | AWS Vendor Invoice Banking Update | **DEEPFAKE** | **75.0%** | `HIGH` | `PASS` |
| **EMAIL-004** | Email | CFO Early Dividend Directive | **DEEPFAKE** | **86.0%** | `CRITICAL` | `PASS` |
| **EMAIL-005** | Email | Chase Monthly Statement Alert | **LEGITIMATE** | **2.0%** | `CLEAN` | `PASS` |
| **CALL-001** | Voice Call | CEO Voice Clone at Airport ($2.45M Wire) | **DEEPFAKE** | **99.0%** | `CRITICAL` | `PASS` |
| **CALL-002** | Voice Call | Verified Client Routine Wire Inquiry | **LEGITIMATE** | **2.5%** | `CLEAN` | `PASS` |
| **CALL-003** | Voice Call | Deloitte Audit Partner Banking Update | **DEEPFAKE** | **86.1%** | `CRITICAL` | `PASS` |
| **MULTI-001** | Multi-Modal | Coordinated Video Call + Wire Email + Voice | **DEEPFAKE** | **99.0%** | `CRITICAL` | `PASS` |
| **MULTI-002** | Multi-Modal | Official TechCorp Quarterly Earnings Call | **LEGITIMATE** | **2.3%** | `CLEAN` | `PASS` |
| **MULTI-003** | Multi-Modal | Deepfake Emergency Board Video Resolution | **DEEPFAKE** | **99.0%** | `CRITICAL` | `PASS` |

**Benchmark Accuracy: 11/11 (100.0%)**

---

## 🛠️ Project Architecture

```
deepfake-detection/
├── app.py                      # Flask web application & REST API
├── cli.py                      # Command-line interface for judges & automated testing
├── config.py                   # System thresholds, action plan templates, risk levels
├── requirements.txt            # Python dependencies
├── models/                     # Multi-modal detection engines
│   ├── __init__.py
│   ├── text_analyzer.py        # NLP, urgency, impersonation, typosquatting detection
│   ├── audio_analyzer.py       # Spectral, voice consistency, vocoder artifact analysis
│   ├── video_analyzer.py       # Face-swap, lip-sync, biological signal detection
│   └── image_analyzer.py       # ELA tampering, font, and metadata forensics
├── detectors/
│   ├── __init__.py
│   └── ensemble.py             # Multi-modal ensemble fusion & risk scoring
├── utils/
│   ├── __init__.py
│   └── report_generator.py     # Generates executive summaries & compliance action plans
├── sample_data/                # Pre-checked ground truth datasets
│   ├── emails/sample_emails.json
│   ├── transcripts/sample_calls.json
│   ├── multi_modal_scenarios.json
│   └── reports/                # Exported forensic analysis reports
├── templates/                  # Frontend HTML templates
│   ├── base.html               # Shared layout, navbar, branding
│   ├── index.html              # Main dashboard with sample cards & demo suite
│   ├── analyze.html            # Custom communication submission & gauge visualization
│   └── report.html             # Standalone case report viewer
├── static/
│   ├── css/style.css           # Modern dark-mode UI stylesheet
│   └── js/app.js               # Async analysis, modal triggers, demo table renderer
└── tests/
    └── test_detection.py       # Automated unit & integration benchmark test suite
```

---

## ⚡ Quick Start Guide

### 1. Prerequisites
- Python 3.9+ (Python 3.14 compatible)

### 2. Run the Benchmark Test Suite
Verify that all unit tests and pre-checked examples pass:
```bash
python -m unittest discover -s tests -p "test_*.py"
```

### 3. Run via Command Line (CLI)
Run the full 11-case benchmark in the terminal:
```bash
python cli.py --demo
```

Inspect a specific pre-checked case and view its compliance Action Plan:
```bash
python cli.py --sample EMAIL-001
```

Analyze any ad-hoc text:
```bash
python cli.py --text "Urgent wire transfer of $2,000,000 to new account. Skip compliance."
```

### 4. Launch the Web Application
Start the local dashboard:
```bash
python app.py
```
Open your browser and navigate to:
```
http://127.0.0.1:5000
```

---

## 🌐 REST API Reference

### `POST /api/analyze`
Analyze multi-modal communications via JSON payload.
```json
{
  "title": "Suspected Wire Instruction",
  "text": "Please transfer $1,000,000 immediately as CEO approved...",
  "metadata": {
    "sender_email": "ceo@imposter-bank.com",
    "claimed_organization": "Official Bank",
    "spf_pass": false
  }
}
```

### `GET /api/demo/run-all`
Executes real-time verification across all sample cases and returns testing metrics and pass/fail statuses.

### `GET /api/analyze/sample/<sample_id>`
Retrieves pre-loaded sample data, runs the analysis pipeline, and outputs risk metrics with recommended actions.

---

## 🏆 Hackathon Pitch & Value Proposition

- **Institutional Safety**: Prevents multi-million-dollar wire fraud losses before transfers leave the bank.
- **Regulatory Alignment**: Automated action plan generates the exact evidentiary audit trail required for FinCEN SAR filings under BSA/AML rules within statutory deadlines.
- **Human-in-the-Loop Decision Support**: Not a black box; provides clear, human-understandable findings (e.g. "Missing breathing cadence", "Typosquatted domain with digit substitution", "Viseme mismatch").
- **Speed & Scale**: Sub-10ms response times suitable for real-time integration into corporate email gateways, SWIFT messaging hubs, and call center screening systems.

---

## 📜 License
Developed for Hackathon 2026. Released under the MIT License.
