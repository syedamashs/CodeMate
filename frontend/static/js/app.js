const languageMap = {
  'Python': { prism: 'python', ext: 'py' },
  'JavaScript': { prism: 'javascript', ext: 'js' },
  'Java': { prism: 'java', ext: 'java' },
  'C++': { prism: 'cpp', ext: 'cpp' },
  'C': { prism: 'c', ext: 'c' }
};

const $ = id => document.getElementById(id);

function toast(message) {
  const node = $('toast');
  if (!node) return;
  node.textContent = message;
  node.classList.add('show');
  setTimeout(() => node.classList.remove('show'), 3500);
}

function computeDiff(originalText, newText) {
  const orig = (originalText || '').replace(/\r\n/g, '\n').split('\n');
  const next = (newText || '').replace(/\r\n/g, '\n').split('\n');
  const n = orig.length;
  const m = next.length;

  const dp = Array.from({ length: n + 1 }, () => new Int32Array(m + 1));
  for (let i = 0; i < n; i++) {
    for (let j = 0; j < m; j++) {
      if (orig[i] === next[j]) {
        dp[i + 1][j + 1] = dp[i][j] + 1;
      } else {
        dp[i + 1][j + 1] = Math.max(dp[i + 1][j], dp[i][j + 1]);
      }
    }
  }

  let i = n, j = m;
  const ops = [];
  while (i > 0 || j > 0) {
    if (i > 0 && j > 0 && orig[i - 1] === next[j - 1]) {
      ops.push({ type: 'unchanged', text: orig[i - 1], origLine: i, newLine: j });
      i--;
      j--;
    } else if (j > 0 && (i === 0 || dp[i][j - 1] >= dp[i - 1][j])) {
      ops.push({ type: 'add', text: next[j - 1], origLine: null, newLine: j });
      j--;
    } else if (i > 0) {
      ops.push({ type: 'del', text: orig[i - 1], origLine: i, newLine: null });
      i--;
    }
  }
  ops.reverse();
  return ops;
}

function renderDiff(originalText, newText) {
  const container = $('diff-content');
  if (!container) return;
  container.innerHTML = '';
  const diffOps = computeDiff(originalText, newText);

  diffOps.forEach(op => {
    const row = document.createElement('div');
    row.className = `diff-row ${op.type}`;

    const num = document.createElement('div');
    num.className = 'diff-num';
    num.textContent = op.newLine !== null ? op.newLine : (op.origLine !== null ? op.origLine : '');

    const sign = document.createElement('div');
    sign.className = `diff-sign ${op.type}`;
    sign.textContent = op.type === 'add' ? '+' : (op.type === 'del' ? '-' : ' ');

    const code = document.createElement('div');
    code.className = 'diff-code';
    code.textContent = op.text;

    row.appendChild(num);
    row.appendChild(sign);
    row.appendChild(code);
    container.appendChild(row);
  });
}

function setViewTab(tab) {
  const codeView = $('code-view-container');
  const diffView = $('diff-view-container');
  const tabCodeBtn = $('tab-code-btn');
  const tabDiffBtn = $('tab-diff-btn');

  if (tab === 'diff') {
    if (codeView) codeView.hidden = true;
    if (diffView) diffView.hidden = false;
    if (tabCodeBtn) tabCodeBtn.classList.remove('active');
    if (tabDiffBtn) tabDiffBtn.classList.add('active');
  } else {
    if (diffView) diffView.hidden = true;
    if (codeView) codeView.hidden = false;
    if (tabDiffBtn) tabDiffBtn.classList.remove('active');
    if (tabCodeBtn) tabCodeBtn.classList.add('active');
  }
}

function downloadCode() {
  const code = $('corrected-code')?.textContent || '';
  if (!code.trim()) {
    toast('No corrected code to download.');
    return;
  }
  const lang = $('language')?.value || 'Python';
  const langInfo = languageMap[lang] || { ext: 'txt' };
  const filename = `codemate_corrected.${langInfo.ext}`;
  const blob = new Blob([code], { type: 'text/plain;charset=utf-8' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
  toast(`Downloaded ${filename}`);
}

function exportReport() {
  const bugType = $('bug-type')?.textContent || 'N/A';
  const severity = $('severity-badge')?.textContent || 'N/A';
  const detectedIssue = $('detected-issue')?.textContent || 'N/A';
  const explanation = $('explanation')?.textContent || 'N/A';
  const suggestedFix = $('suggested-fix')?.textContent || 'N/A';
  const correctedCode = $('corrected-code')?.textContent || '';
  const reason = $('reason')?.textContent || 'N/A';
  const originalCode = $('code')?.value || '';
  const lang = $('language')?.value || 'Python';

  if (!correctedCode.trim()) {
    toast('No analysis results available to export.');
    return;
  }

  const report = `# CodeMate Analysis & Review Report
**Generated On:** ${new Date().toLocaleString()}
**Workbench:** CodeMate Code Intelligence & Automated Review

---

## 1. Defect Overview
- **Language:** ${lang}
- **Bug Classification:** ${bugType}
- **Severity Level:** ${severity}

---

## 2. Technical Findings
### Detected Issue
${detectedIssue}

### Explanation
${explanation}

### Recommended Fix
${suggestedFix}

### Technical Rationale
${reason}

---

## 3. Source Code Comparison

### Original Code
\`\`\`${lang.toLowerCase()}
${originalCode}
\`\`\`

### Corrected Code
\`\`\`${lang.toLowerCase()}
${correctedCode}
\`\`\`

---
*Report generated automatically by CodeMate Code Intelligence Workbench.*
`;

  const blob = new Blob([report], { type: 'text/markdown;charset=utf-8' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `CodeMate_Review_Report_${Date.now()}.md`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
  toast('Exported review report (.md)');
}

async function analyze() {
  const code = $('code')?.value || '';
  if (!code.trim()) {
    toast('Enter code before analyzing.');
    return;
  }
  if ($('empty-result')) $('empty-result').hidden = true;
  if ($('result-content')) $('result-content').hidden = true;
  if ($('loading')) $('loading').hidden = false;
  if ($('result-state')) $('result-state').textContent = 'Analyzing';
  if ($('analyze-btn')) $('analyze-btn').disabled = true;

  try {
    const lang = $('language')?.value || 'Python';
    const response = await fetch('/api/analyze', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        language: lang,
        code,
        error_message: $('error-message')?.value || ''
      })
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || 'Analysis failed');

    const result = data.result;

    // Populate text cards
    for (const key of ['bug-type', 'detected-issue', 'explanation', 'suggested-fix', 'reason']) {
      const el = $(key);
      if (el) el.textContent = result[key.replaceAll('-', '_')] || 'N/A';
    }

    // Populate corrected code & syntax highlight
    const codeEl = $('corrected-code');
    if (codeEl) {
      codeEl.textContent = result.corrected_code || '';
      const langInfo = languageMap[lang] || { prism: 'python' };
      codeEl.className = `language-${langInfo.prism}`;
      if (window.Prism) {
        Prism.highlightElement(codeEl);
      }
    }

    // Render diff
    renderDiff(code, result.corrected_code || '');

    // Reset view to Code view tab
    setViewTab('code');

    // Severity badge
    const sevBadge = $('severity-badge');
    if (sevBadge) {
      const sev = result.severity || 'CRITICAL';
      sevBadge.textContent = sev;
      sevBadge.className = `severity-badge ${result.severity_class || ('severity-' + sev.toLowerCase())}`;
    }

    // Print report in browser console (F12)
    console.log(
      "%c=================================================================\n" +
      "               CODEMATE ANALYSIS REPORT\n" +
      "=================================================================\n" +
      `Mode     : ${data.mode.toUpperCase()}\n` +
      `Language : ${lang}\n` +
      `Latency  : ${data.latency}s\n` +
      `Severity : ${result.severity || 'N/A'}\n` +
      `Bug Type : ${result.bug_type || 'N/A'}\n` +
      "-----------------------------------------------------------------\n" +
      `[DETECTED ISSUE(S)]:\n${result.detected_issue || 'None'}\n` +
      "-----------------------------------------------------------------\n" +
      `[EXPLANATION]:\n${result.explanation || 'None'}\n` +
      "-----------------------------------------------------------------\n" +
      `[SUGGESTED FIX]:\n${result.suggested_fix || 'None'}\n` +
      "-----------------------------------------------------------------\n" +
      `[CORRECTED CODE]:\n${result.corrected_code || 'None'}\n` +
      "-----------------------------------------------------------------\n" +
      `[REASON]:\n${result.reason || 'None'}\n` +
      "=================================================================",
      "color: #0e766c; font-weight: bold; font-family: monospace;"
    );

    if ($('result-content')) $('result-content').hidden = false;
    if ($('result-state')) $('result-state').textContent = `${data.mode.toUpperCase()} · ${data.latency}s`;
  } catch (error) {
    toast(error.message);
    if ($('empty-result')) $('empty-result').hidden = false;
    if ($('result-state')) $('result-state').textContent = 'Unable to analyze';
  } finally {
    if ($('loading')) $('loading').hidden = true;
    if ($('analyze-btn')) $('analyze-btn').disabled = false;
  }
}

// Event Listeners initialization
if ($('analyze-btn')) {
  $('analyze-btn').addEventListener('click', analyze);

  $('clear-btn')?.addEventListener('click', () => {
    $('code').value = '';
    $('error-message').value = '';
    if ($('empty-result')) $('empty-result').hidden = false;
    if ($('result-content')) $('result-content').hidden = true;
    if ($('result-state')) $('result-state').textContent = 'Waiting for input';
    setViewTab('code');
  });

  $('copy-btn')?.addEventListener('click', async () => {
    const code = $('corrected-code')?.textContent || '';
    if (code) {
      await navigator.clipboard.writeText(code);
      toast('Corrected code copied');
    }
  });

  $('tab-code-btn')?.addEventListener('click', () => setViewTab('code'));
  $('tab-diff-btn')?.addEventListener('click', () => setViewTab('diff'));
  $('download-btn')?.addEventListener('click', downloadCode);
  $('export-report-btn')?.addEventListener('click', exportReport);
}

/* ========================================================
   Code Health & Security Audit Handler
   ======================================================== */
async function runAudit() {
  const code = $('audit-code')?.value || '';
  const lang = $('audit-language')?.value || 'Python';

  if (!code.trim()) {
    toast('Enter code to audit.');
    return;
  }

  if ($('audit-empty-result')) $('audit-empty-result').hidden = true;
  if ($('audit-result-content')) $('audit-result-content').hidden = true;
  if ($('audit-loading')) $('audit-loading').hidden = false;
  if ($('run-audit-btn')) $('run-audit-btn').disabled = true;
  if ($('audit-result-state')) $('audit-result-state').textContent = 'Auditing...';

  try {
    const response = await fetch('/api/audit', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ code, language: lang })
    });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.error || 'Audit request failed.');
    }

    const res = data.result || {};

    // 1. Health Score
    const scoreEl = $('audit-health-score');
    if (scoreEl) scoreEl.textContent = res.health_score ?? 'N/A';

    const healthBadge = $('audit-health-badge');
    if (healthBadge) {
      healthBadge.textContent = res.health_label || 'Good';
      healthBadge.className = `health-badge ${res.health_class || 'health-good'}`;
    }

    // 2. Complexity Pills
    const timeEl = $('audit-time-complexity');
    if (timeEl) timeEl.textContent = res.time_complexity || 'O(N)';

    const spaceEl = $('audit-space-complexity');
    if (spaceEl) spaceEl.textContent = res.space_complexity || 'O(1)';

    // 3. Security Status
    const secBadge = $('audit-security-badge');
    const secStatus = (res.security_status || 'Safe').toUpperCase();
    if (secBadge) {
      secBadge.textContent = secStatus;
      secBadge.className = `security-status-badge status-${secStatus.toLowerCase()}`;
    }

    const secSummary = $('audit-security-summary');
    if (secSummary) {
      const count = (res.security_findings || []).length;
      secSummary.textContent = count === 0 ? 'No vulnerabilities detected' : `${count} issue(s) identified`;
    }

    // 4. Complexity Explanation
    const compExp = $('audit-complexity-exp');
    if (compExp) compExp.textContent = res.complexity_explanation || 'Standard runtime performance.';

    // 5. Populate Lists (Security, Smells, Tips)
    const populateList = (id, items, emptyText) => {
      const ul = $(id);
      if (!ul) return;
      ul.innerHTML = '';
      if (!items || items.length === 0) {
        const li = document.createElement('li');
        li.textContent = emptyText;
        ul.appendChild(li);
      } else {
        items.forEach(item => {
          const li = document.createElement('li');
          li.textContent = item;
          ul.appendChild(li);
        });
      }
    };

    populateList('audit-security-list', res.security_findings, 'No vulnerabilities or injection risks detected.');
    populateList('audit-smells-list', res.code_smells, 'Code adheres to readability and structure standards.');
    populateList('audit-tips-list', res.optimization_tips, 'Operating at optimal algorithmic efficiency.');

    // 6. Optimized Code & Prism Highlighting
    const optCodeEl = $('audit-optimized-code');
    if (optCodeEl) {
      optCodeEl.textContent = res.optimized_code || code;
      const langInfo = languageMap[lang] || { prism: 'python' };
      optCodeEl.className = `language-${langInfo.prism}`;
      if (window.Prism) {
        Prism.highlightElement(optCodeEl);
      }
    }

    // 7. DevTools (F12) Console Log
    console.log(
      "%c=================================================================\n" +
      "               CODEMATE HEALTH & SECURITY AUDIT\n" +
      "=================================================================\n" +
      `Mode             : ${data.mode.toUpperCase()}\n` +
      `Language         : ${lang}\n` +
      `Latency          : ${data.latency}s\n` +
      `Health Score     : ${res.health_score}/100 (${res.health_label})\n` +
      `Time Complexity  : ${res.time_complexity}\n` +
      `Space Complexity : ${res.space_complexity}\n` +
      `Security Status  : ${res.security_status}\n` +
      "-----------------------------------------------------------------\n" +
      `[COMPLEXITY RATIONALE]:\n${res.complexity_explanation}\n` +
      "-----------------------------------------------------------------\n" +
      `[SECURITY FINDINGS]:\n${(res.security_findings || []).join('\n') || 'None'}\n` +
      "-----------------------------------------------------------------\n" +
      `[CODE SMELLS]:\n${(res.code_smells || []).join('\n') || 'None'}\n` +
      "-----------------------------------------------------------------\n" +
      `[OPTIMIZATION TIPS]:\n${(res.optimization_tips || []).join('\n') || 'None'}\n` +
      "=================================================================",
      "color: #0369a1; font-weight: bold; font-family: monospace;"
    );

    if ($('audit-result-content')) $('audit-result-content').hidden = false;
    if ($('audit-result-state')) $('audit-result-state').textContent = `${data.mode.toUpperCase()} · ${data.latency}s`;

  } catch (error) {
    toast(error.message);
    if ($('audit-empty-result')) $('audit-empty-result').hidden = false;
    if ($('audit-result-state')) $('audit-result-state').textContent = 'Unable to complete audit';
  } finally {
    if ($('audit-loading')) $('audit-loading').hidden = true;
    if ($('run-audit-btn')) $('run-audit-btn').disabled = false;
  }
}

// Audit Event Listeners
if ($('run-audit-btn')) {
  $('run-audit-btn').addEventListener('click', runAudit);

  $('audit-clear-btn')?.addEventListener('click', () => {
    $('audit-code').value = '';
    if ($('audit-empty-result')) $('audit-empty-result').hidden = false;
    if ($('audit-result-content')) $('audit-result-content').hidden = true;
    if ($('audit-result-state')) $('audit-result-state').textContent = 'Waiting for input';
  });

  $('audit-copy-btn')?.addEventListener('click', async () => {
    const code = $('audit-optimized-code')?.textContent || '';
    if (code) {
      await navigator.clipboard.writeText(code);
      toast('Optimized code copied');
    }
  });

  $('audit-download-btn')?.addEventListener('click', () => {
    const code = $('audit-optimized-code')?.textContent || '';
    if (!code.trim()) {
      toast('No optimized code to download.');
      return;
    }
    const lang = $('audit-language')?.value || 'Python';
    const langInfo = languageMap[lang] || { ext: 'txt' };
    const filename = `codemate_optimized.${langInfo.ext}`;
    const blob = new Blob([code], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    toast(`Downloaded ${filename}`);
  });
}

