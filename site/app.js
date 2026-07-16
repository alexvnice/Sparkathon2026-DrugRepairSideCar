// Drug Repair Sidecar — demo page logic
// Loads data/demos.json, renders cards, handles filter buttons.

const FIX_LABELS = {
  'text-postprocess': 'Text Post-process',
  'term-boost':       'Term Boost',
  'redecode':         'Re-decode',
  'prompt-history':   'Prompt / History',
};

async function loadData() {
  const res = await fetch('data/demos.json');
  if (!res.ok) throw new Error(`Failed to load demos.json: ${res.status}`);
  return res.json();
}

function pct(wer) {
  return (wer * 100).toFixed(1) + '%';
}

/** Highlight words that differ between before and after using LCS word diff.
 *  Handles word-count changes correctly — only the actual changed words are
 *  highlighted, not everything that follows a substitution. */
function diffHighlight(before, after) {
  const bWords = before.split(' ');
  const aWords = after.split(' ');
  const m = bWords.length, n = aWords.length;

  // Build LCS table
  const dp = Array.from({length: m + 1}, () => new Array(n + 1).fill(0));
  for (let i = 1; i <= m; i++) {
    for (let j = 1; j <= n; j++) {
      dp[i][j] = bWords[i-1].toLowerCase() === aWords[j-1].toLowerCase()
        ? dp[i-1][j-1] + 1
        : Math.max(dp[i-1][j], dp[i][j-1]);
    }
  }

  // Backtrack to produce aligned output
  const bOut = [], aOut = [];
  let i = m, j = n;
  while (i > 0 || j > 0) {
    if (i > 0 && j > 0 && bWords[i-1].toLowerCase() === aWords[j-1].toLowerCase()) {
      bOut.unshift(bWords[i-1]);
      aOut.unshift(aWords[j-1]);
      i--; j--;
    } else if (j > 0 && (i === 0 || dp[i][j-1] >= dp[i-1][j])) {
      aOut.unshift(`<span class="correct">${aWords[j-1]}</span>`);
      j--;
    } else {
      bOut.unshift(`<span class="error">${bWords[i-1]}</span>`);
      i--;
    }
  }
  return { beforeHtml: bOut.join(' '), afterHtml: aOut.join(' ') };
}

function buildCard(demo) {
  const tmpl   = document.getElementById('card-template');
  const card   = tmpl.content.cloneNode(true).querySelector('.demo-card');
  card.dataset.fixType = demo.fix_type;
  card.dataset.caseId  = demo.id;

  // Badge
  const badge = card.querySelector('.fix-badge');
  badge.textContent      = FIX_LABELS[demo.fix_type] ?? demo.fix_type;
  badge.dataset.type     = demo.fix_type;

  // Case ID
  card.querySelector('.case-id').textContent = demo.id;

  // Audio
  const src = card.querySelector('audio source');
  src.src   = demo.audio;

  // Transcripts with diff highlighting
  const { beforeHtml, afterHtml } = diffHighlight(demo.before, demo.after);
  const [beforeBlock, afterBlock] = card.querySelectorAll('.transcript-block');

  beforeBlock.querySelector('.transcript-text').innerHTML = beforeHtml;
  beforeBlock.querySelector('.wer-chip').textContent      = `Recall ${pct(demo.wer_before)}`;

  afterBlock.querySelector('.transcript-text').innerHTML  = afterHtml;
  afterBlock.querySelector('.wer-chip').textContent       = `Recall ${pct(demo.wer_after)}`;

  // Fix details
  card.querySelector('.fix-payload').textContent =
    JSON.stringify(demo.fix_detail, null, 2);

  return card;
}

function renderSummary(summary) {
  document.getElementById('wer-before').textContent      = pct(summary.wer_before);
  document.getElementById('wer-after').textContent       = pct(summary.wer_after);
  document.getElementById('drug-wer-before').textContent = pct(summary.drug_wer_before);
  document.getElementById('drug-wer-after').textContent  = pct(summary.drug_wer_after);
}

function applyFilter(filter) {
  document.querySelectorAll('.demo-card').forEach(card => {
    card.style.display =
      (filter === 'all' || card.dataset.fixType === filter) ? '' : 'none';
  });

  document.querySelectorAll('.filter-btn').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.filter === filter);
  });
}

async function init() {
  const grid = document.getElementById('demo-grid');

  let data;
  try {
    data = await loadData();
  } catch (err) {
    grid.innerHTML = `<p style="color:red">Error loading demo data: ${err.message}</p>`;
    return;
  }

  renderSummary(data.summary);

  data.cases.forEach(demo => grid.appendChild(buildCard(demo)));

  // Filter button wiring
  document.querySelectorAll('.filter-btn').forEach(btn => {
    btn.addEventListener('click', () => applyFilter(btn.dataset.filter));
  });

  // Problem-strip pill wiring — click scrolls to and highlights the matching demo card
  document.querySelectorAll('.problem-pill[data-card]').forEach(pill => {
    pill.addEventListener('click', () => {
      const target = document.querySelector(`.demo-card[data-case-id="${pill.dataset.card}"]`);
      if (!target) return;
      applyFilter('all');
      target.scrollIntoView({ behavior: 'smooth', block: 'center' });
      target.classList.add('card--highlight');
      setTimeout(() => target.classList.remove('card--highlight'), 2000);
    });
  });
}

init();

// Back-to-top button
const backToTop = document.getElementById('back-to-top');
window.addEventListener('scroll', () => {
  backToTop.classList.toggle('visible', window.scrollY > 300);
});
backToTop.addEventListener('click', () => {
  window.scrollTo({ top: 0, behavior: 'smooth' });
});
