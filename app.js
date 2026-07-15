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

/** Highlight words in `after` that differ from `before`, and vice-versa. */
function diffHighlight(before, after) {
  const bWords = before.split(' ');
  const aWords = after.split(' ');
  const maxLen  = Math.max(bWords.length, aWords.length);

  const bOut = [];
  const aOut = [];
  for (let i = 0; i < maxLen; i++) {
    const b = bWords[i] ?? '';
    const a = aWords[i] ?? '';
    if (b.toLowerCase() !== a.toLowerCase()) {
      if (b) bOut.push(`<span class="error">${b}</span>`);
      if (a) aOut.push(`<span class="correct">${a}</span>`);
    } else {
      if (b) bOut.push(b);
      if (a) aOut.push(a);
    }
  }
  return { beforeHtml: bOut.join(' '), afterHtml: aOut.join(' ') };
}

function buildCard(demo) {
  const tmpl   = document.getElementById('card-template');
  const card   = tmpl.content.cloneNode(true).querySelector('.demo-card');
  card.dataset.fixType = demo.fix_type;

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
  beforeBlock.querySelector('.wer-chip').textContent      = `WER ${pct(demo.wer_before)}`;

  afterBlock.querySelector('.transcript-text').innerHTML  = afterHtml;
  afterBlock.querySelector('.wer-chip').textContent       = `WER ${pct(demo.wer_after)}`;

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
}

init();
