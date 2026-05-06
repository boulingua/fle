/* Materials Discovery Network — card grid below the graph.

   Subscribes to the shared store and re-renders the visible card
   set whenever the filter or search state changes. Hover on a
   card pushes hoveredNodeId to the store; the graph subscriber
   adds a `.hover` class to the matching node, growing it and
   showing its highlight ring. Clicking presentation / worksheet
   cards triggers download via the <a download> attribute.

   Article cards span 2 grid columns; presentations / worksheets
   stay compact. Sort: deterministic, by article slug then by
   type within the same article.
*/

const TYPE_RANK = { article: 0, presentation: 1, worksheet: 2 };

function typeGlyph(type) {
  const cls = type === 'article' ? 'glyph-article'
            : type === 'presentation' ? 'glyph-presentation'
            : 'glyph-worksheet';
  return `<span class="${cls}" style="color: var(--topic-${type === 'article' ? '' : ''}var(--network-fg));"></span>`;
}

function typeLabel(type) {
  return ({ article: 'Article', presentation: 'Présentation', worksheet: 'Fiche' })[type] || type;
}

function courseLabel(courseId) {
  const m = /^track-(e|gm)-kl(\d+)$/.exec(courseId || '');
  if (!m) return courseId || '';
  return `${m[1] === 'gm' ? 'G+M' : 'E'} · Classe ${parseInt(m[2], 10)}`;
}

function topicLabel(topicId, topicLabels) {
  return topicLabels.get(topicId) || topicId || '';
}

function renderCard(node, topicLabels) {
  const li = document.createElement('li');
  li.className = `network-card is-${node.type}`;
  li.dataset.nodeId = node.id;
  li.dataset.topic = node.topic || '';

  const meta = [
    typeLabel(node.type),
    courseLabel(node.course),
    node.topic ? topicLabel(node.topic, topicLabels) : null,
  ].filter(Boolean).join(' · ');

  const tags = (node.tags || []).slice(0, 4).map(t =>
    `<span class="network-card-tag">${escapeHtml(t)}</span>`
  ).join('');

  const isFile = node.type !== 'article' && node.url;
  const action = isFile
    ? `<a href="${escapeAttr(node.url)}" download class="network-card-download">Télécharger</a>`
    : node.url
      ? `<a href="${escapeAttr(node.url)}">Ouvrir l'article</a>`
      : '';

  li.innerHTML = `
    <div class="network-card-meta">
      <span class="glyph-${node.type}" style="color: var(--topic-${node.topic || 'leseverstehen'});"></span>
      ${escapeHtml(meta)}
    </div>
    <h3 class="network-card-title">${escapeHtml(node.title || node.id)}</h3>
    ${node.description ? `<p class="network-card-desc">${escapeHtml(node.description)}</p>` : ''}
    ${tags ? `<div class="network-card-tags">${tags}</div>` : ''}
    ${action ? `<div class="network-card-actions">${action}</div>` : ''}
  `;
  return li;
}

function escapeHtml(s) {
  return String(s).replace(/[&<>"']/g, c => (
    { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]
  ));
}
function escapeAttr(s) { return escapeHtml(s); }

export function mountList({ root, data, store }) {
  const byId = new Map(data.nodes.map(n => [n.id, n]));
  const topicLabels = new Map(
    (data.facets.topics || []).map(t => [t.id, t.label_fr || t.label || t.id])
  );

  // delegated hover sync
  root.addEventListener('mouseover', evt => {
    const card = evt.target.closest('.network-card');
    if (!card) return;
    store.set({ hoveredNodeId: card.dataset.nodeId });
  });
  root.addEventListener('mouseout', evt => {
    const card = evt.target.closest('.network-card');
    if (!card) return;
    if (store.get().hoveredNodeId === card.dataset.nodeId) {
      store.set({ hoveredNodeId: null });
    }
  });

  function visibleNodes() {
    const s = store.get();
    let pool = data.nodes;
    if (s.filteredNodeIds) {
      pool = pool.filter(n => s.filteredNodeIds.has(n.id));
    }
    if (s.searchMatchIds) {
      pool = pool.filter(n => s.searchMatchIds.has(n.id));
    }
    return pool.slice().sort((a, b) => {
      // group: article and its pres/ws stay adjacent
      const ka = a.parent_article || a.id;
      const kb = b.parent_article || b.id;
      if (ka < kb) return -1;
      if (ka > kb) return 1;
      return (TYPE_RANK[a.type] ?? 9) - (TYPE_RANK[b.type] ?? 9);
    });
  }

  function render() {
    const nodes = visibleNodes();
    root.innerHTML = '';
    if (nodes.length === 0) {
      const empty = document.createElement('li');
      empty.className = 'network-empty';
      empty.style.gridColumn = '1 / -1';
      empty.innerHTML = `
        <svg viewBox="0 0 64 64" fill="none" stroke="currentColor"
             stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"
             aria-hidden="true">
          <circle cx="27" cy="27" r="14"></circle>
          <line x1="38" y1="38" x2="52" y2="52"></line>
        </svg>
        <p>Aucun matériau ne correspond à la sélection actuelle.</p>
        <p style="font-size:0.85rem;">Détendez un filtre ou videz la recherche.</p>
      `;
      root.appendChild(empty);
      return;
    }
    const frag = document.createDocumentFragment();
    for (const n of nodes) frag.appendChild(renderCard(n, topicLabels));
    root.appendChild(frag);
  }

  store.subscribe(render);
  render();

  return { render };
}
