// FinShield AI - Deepfake Detection Frontend Logic

function openModal() {
    const modal = document.getElementById('resultModal');
    if (modal) modal.style.display = 'flex';
}

function closeModal() {
    const modal = document.getElementById('resultModal');
    if (modal) modal.style.display = 'none';
}

function closeDemoResults() {
    const demo = document.getElementById('demoResults');
    if (demo) demo.style.display = 'none';
}

window.addEventListener('click', function(event) {
    const modal = document.getElementById('resultModal');
    if (event.target === modal) {
        closeModal();
    }
});

function analyzeSample(sampleId) {
    openModal();
    const modalTitle = document.getElementById('modalTitle');
    const modalBody = document.getElementById('modalBody');

    if (modalTitle) modalTitle.innerHTML = `<i class="fas fa-spinner fa-spin"></i> Analyzing ${sampleId}...`;
    if (modalBody) {
        modalBody.innerHTML = `
            <div class="loading">
                <div class="spinner"></div>
                <p>Running multi-modal analysis on ${sampleId}...</p>
            </div>
        `;
    }

    fetch(`/api/analyze/sample/${sampleId}`)
        .then(response => {
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            return response.json();
        })
        .then(data => {
            if (data.error) {
                modalBody.innerHTML = `<div class="alert alert-error">${data.error}</div>`;
                return;
            }
            if (modalTitle) {
                modalTitle.innerHTML = `<i class="fas fa-shield-halved"></i> Analysis: ${data.sample.id} - ${data.sample.category || data.sample.title || ''}`;
            }
            modalBody.innerHTML = renderFullResults(data);
        })
        .catch(err => {
            modalBody.innerHTML = `<div class="alert alert-error">Analysis failed: ${err.message}</div>`;
        });
}

function renderFullResults(data) {
    const analysis = data.analysis;
    const overall = analysis.overall;
    const plan = analysis.action_plan;
    const riskClass = overall.risk_level.toLowerCase();

    let findingsHtml = '';
    (overall.all_findings || []).forEach(f => {
        findingsHtml += `
            <div class="finding-card ${f.severity.toLowerCase()}">
                <div class="finding-header">
                    <span class="finding-severity ${f.severity.toLowerCase()}">${f.severity}</span>
                    <span class="finding-category">${f.category}</span>
                    <span class="finding-modality">${f.modality || 'General'}</span>
                </div>
                <div class="finding-detail">${f.detail}</div>
            </div>
        `;
    });

    let immediateHtml = '';
    (plan.immediate_actions || []).forEach(act => {
        immediateHtml += `<li>${act}</li>`;
    });

    let followUpHtml = '';
    (plan.follow_up_actions || []).forEach(act => {
        followUpHtml += `<li>${act}</li>`;
    });

    let subScoresHtml = '';
    for (const [modality, modResult] of Object.entries(analysis.modality_results || {})) {
        let barsHtml = '';
        for (const [scoreKey, scoreVal] of Object.entries(modResult.sub_scores || {})) {
            const pct = Math.round(scoreVal * 100);
            const color = scoreVal > 0.6 ? '#dc2626' : (scoreVal > 0.3 ? '#d97706' : '#16a34a');
            const cleanLabel = scoreKey.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
            barsHtml += `
                <div class="sub-score">
                    <div class="sub-score-label">${cleanLabel}</div>
                    <div class="sub-score-bar">
                        <div class="sub-score-fill" style="width: ${pct}%; background: ${color};"></div>
                    </div>
                    <div class="sub-score-value">${(scoreVal * 100).toFixed(1)}%</div>
                </div>
            `;
        }
        subScoresHtml += `
            <div class="modality-result" style="margin-top: 1rem;">
                <h4 style="margin-bottom: 0.75rem; text-transform: capitalize;">${modality} Analysis: <span class="risk-badge ${modResult.risk_level.toLowerCase()}">${modResult.risk_level}</span></h4>
                <div class="sub-scores-grid">${barsHtml}</div>
            </div>
        `;
    }

    return `
        <div class="risk-overview" style="margin-bottom: 1.5rem;">
            <div class="risk-gauge">
                <div class="gauge-circle ${riskClass}">
                    <span class="gauge-value">${(overall.deepfake_probability * 100).toFixed(1)}%</span>
                    <span class="gauge-label">Probability</span>
                </div>
            </div>
            <div class="risk-details">
                <div class="risk-level-display ${riskClass}">${overall.risk_level}</div>
                <div class="confidence-display">Confidence: ${(overall.confidence * 100).toFixed(1)}%</div>
                <div class="modalities-display">Analyzed: ${(analysis.modalities_analyzed || []).join(', ')}</div>
            </div>
        </div>

        <h4 style="margin: 1rem 0 0.5rem;"><i class="fas fa-layer-group"></i> Modality Signals</h4>
        ${subScoresHtml}

        <h4 style="margin: 1.5rem 0 0.5rem;"><i class="fas fa-search"></i> Detected Findings</h4>
        <div>${findingsHtml || '<p style="color:var(--text-muted)">No anomalies detected.</p>'}</div>

        <h4 style="margin: 1.5rem 0 0.5rem;"><i class="fas fa-clipboard-list"></i> Action Plan</h4>
        <div class="action-plan ${riskClass}">
            <div class="plan-header">
                <span class="plan-timeline"><i class="fas fa-clock"></i> Timeline: ${plan.review_timeline}</span>
                ${plan.escalation_required ? '<span class="plan-badge escalation">Escalation Required</span>' : ''}
                ${plan.report_to_authorities ? '<span class="plan-badge authorities">Report to Authorities</span>' : ''}
            </div>
            <div class="plan-section">
                <h5>Immediate Actions</h5>
                <ul class="action-list">${immediateHtml}</ul>
            </div>
            ${followUpHtml ? `
            <div class="plan-section" style="margin-top:1rem;">
                <h5>Follow-up Actions</h5>
                <ul class="action-list">${followUpHtml}</ul>
            </div>` : ''}
        </div>
    `;
}

function runAllDemos() {
    const demoResults = document.getElementById('demoResults');
    const demoBody = document.getElementById('demoBody');
    if (demoResults) demoResults.style.display = 'block';
    if (demoBody) {
        demoBody.innerHTML = `
            <div class="loading">
                <div class="spinner"></div>
                <p>Running verification test across all 11+ sample cases...</p>
            </div>
        `;
    }

    demoResults.scrollIntoView({ behavior: 'smooth' });

    fetch('/api/demo/run-all')
        .then(response => response.json())
        .then(data => {
            const summary = data.summary;
            let rowsHtml = '';
            data.results.forEach(item => {
                const badgeClass = item.test_passed ? 'clean' : 'critical';
                const passText = item.test_passed ? 'PASS' : 'FAIL';
                const prob = (item.actual_probability * 100).toFixed(1);
                rowsHtml += `
                    <tr style="border-bottom: 1px solid var(--border-color);">
                        <td style="padding: 0.75rem; font-family: monospace;">${item.id}</td>
                        <td style="padding: 0.75rem;"><span class="sample-label ${item.label.toLowerCase()}">${item.label}</span></td>
                        <td style="padding: 0.75rem;">${item.category}</td>
                        <td style="padding: 0.75rem; font-weight: bold;">${prob}%</td>
                        <td style="padding: 0.75rem;"><span class="risk-badge ${item.actual_risk_level.toLowerCase()}">${item.actual_risk_level}</span></td>
                        <td style="padding: 0.75rem;"><span class="risk-badge ${badgeClass}">${passText}</span></td>
                        <td style="padding: 0.75rem;">
                            <button class="btn btn-sm btn-secondary" onclick="analyzeSample('${item.id}')">Inspect</button>
                        </td>
                    </tr>
                `;
            });

            demoBody.innerHTML = `
                <div style="display: flex; gap: 2rem; margin-bottom: 1.5rem; background: var(--bg-card); padding: 1rem 1.5rem; border-radius: var(--border-radius-sm);">
                    <div><strong>Total Checked:</strong> ${summary.total}</div>
                    <div style="color: #34d399;"><strong>Passed:</strong> ${summary.passed}</div>
                    <div style="color: ${summary.failed > 0 ? '#f87171' : '#94a3b8'};"><strong>Failed:</strong> ${summary.failed}</div>
                    <div><strong>Accuracy:</strong> <span style="color: #60a5fa; font-weight: bold;">${summary.accuracy}</span></div>
                </div>
                <div style="overflow-x: auto;">
                    <table style="width: 100%; border-collapse: collapse; text-align: left; font-size: 0.9rem;">
                        <thead>
                            <tr style="border-bottom: 2px solid var(--border-color); color: var(--text-secondary);">
                                <th style="padding: 0.75rem;">Case ID</th>
                                <th style="padding: 0.75rem;">Ground Truth</th>
                                <th style="padding: 0.75rem;">Type / Scenario</th>
                                <th style="padding: 0.75rem;">Predicted Prob</th>
                                <th style="padding: 0.75rem;">Risk Assessment</th>
                                <th style="padding: 0.75rem;">Test Match</th>
                                <th style="padding: 0.75rem;">Action</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${rowsHtml}
                        </tbody>
                    </table>
                </div>
            `;
        })
        .catch(err => {
            demoBody.innerHTML = `<div class="alert alert-error">Error running demo suite: ${err.message}</div>`;
        });
}
