/* Materials Discovery Network — facet rail + URL state.

   Renders four facet groups (type / topic / course / tags) into
   a pre-existing <aside class="network-filters"> scaffold,
   handles chip toggling, computes the cross-facet filter
   predicate, and syncs to ?type=...&topic=...&course=...&tags=...
   via history.replaceState.

   Within a facet: OR (selecting two chips shows union).
   Across facets: AND (a node must pass every facet).

   Live counts: each chip's count reflects the size of the set
   that would result if that chip were the *only* selection
   change in its facet — i.e. "counts ignore self-facet, AND all
   other facets". Standard facet-search semantics.
*/

const FACETS = [
  { key: 'type',   urlKey: 'type',   labelFr: 'Type' },
  { key: 'topic',  urlKey: 'topic',  labelFr: 'Sujet' },
  { key: 'course', urlKey: 'course', labelFr: 'Filière & classe' },
  { key: 'tags',   urlKey: 'tags',   labelFr: 'Étiquettes' },
];

function topicLabel(facetEntry) {
  return facetEntry.label_fr || facetEntry.label || facetEntry.id;
}

function courseLabel(facetEntry) {
  // "track-e-kl06" → "E · Classe 6"; "track-gm-kl09" → "G+M · Classe 9"
  const m = /^track-(e|gm)-kl(\d+)$/.exec(facetEntry.id);
  if (!m) return facetEntry.label || facetEntry.id;
  const filiere = m[1] === 'gm' ? 'G+M' : 'E';
  const klasse = parseInt(m[2], 10);
  return `${filiere} · Classe ${klasse}`;
}

function typeLabel(facetEntry) {
  return ({
    article: 'Article',
    presentation: 'Présentation',
    worksheet: 'Fiche',
  })[facetEntry.id] || facetEntry.id;
}

function typeGlyphHtml(id) {
  const cls = id === 'article' ? 'glyph-article'
            : id === 'presentation' ? 'glyph-presentation'
            : 'glyph-worksheet';
  return `<span class="${cls}" style="color: var(--network-fg);"></span>`;
}

// ---- index nodes by facet so re-counting is O(N) per change ----
function indexNodes(nodes) {
  const idx = {
    byType: new Map(),
    byTopic: new Map(),
    byCourse: new Map(),
    byTag: new Map(),
    byId: new Map(),
  };
  function push(map, k, v) {
    if (!map.has(k)) map.set(k, new Set());
    map.get(k).add(v);
  }
  for (const n of nodes) {
    idx.byId.set(n.id, n);
    push(idx.byType, n.type, n.id);
    if (n.topic) push(idx.byTopic, n.topic, n.id);
    if (n.course) push(idx.byCourse, n.course, n.id);
    for (const t of (n.tags || [])) push(idx.byTag, t, n.id);
  }
  return idx;
}

function setIntersect(a, b) {
  if (a == null) return new Set(b);
  const out = new Set();
  const [small, big] = a.size <= b.size ? [a, b] : [b, a];
  for (const x of small) if (big.has(x)) out.add(x);
  return out;
}

function setUnion(sets) {
  const out = new Set();
  for (const s of sets) for (const x of s) out.add(x);
  return out;
}

// ---- URL parse / serialise ----
function readUrl() {
  const sp = new URLSearchParams(location.search);
  const get = key => {
    const raw = sp.get(key);
    if (!raw) return new Set();
    return new Set(raw.split(',').filter(Boolean));
  };
  return {
    type: get('type'),
    topic: get('topic'),
    course: get('course'),
    tags: get('tags'),
  };
}

function writeUrl(state) {
  const sp = new URLSearchParams(location.search);
  for (const f of FACETS) {
    const sel = state[f.key];
    if (!sel || sel.size === 0) sp.delete(f.urlKey);
    else sp.set(f.urlKey, [...sel].join(','));
  }
  const qs = sp.toString();
  const next = location.pathname + (qs ? `?${qs}` : '') + location.hash;
  history.replaceState(null, '', next);
}

// ---- chip rendering ----
function renderChip({ id, label, count, swatchColor, glyphHtml, pressed }) {
  const btn = document.createElement('button');
  btn.type = 'button';
  btn.className = 'network-chip';
  btn.dataset.id = id;
  btn.setAttribute('aria-pressed', pressed ? 'true' : 'false');
  if (count === 0) btn.setAttribute('aria-disabled', 'true');
  const parts = [];
  if (glyphHtml) parts.push(glyphHtml);
  if (swatchColor) parts.push(`<span class="network-chip-swatch" style="background: ${swatchColor};"></span>`);
  parts.push(`<span class="network-chip-label">${label}</span>`);
  parts.push(`<span class="network-chip-count">${count}</span>`);
  btn.innerHTML = parts.join('');
  return btn;
}

// ---- count for each chip given the selection state -------------
// chip count = | {nodes passing every OTHER facet} ∩ {nodes in this chip} |
function countsFor(facetKey, selections, idx) {
  const otherFacets = FACETS.filter(f => f.key !== facetKey);
  let pool = null; // null = all nodes
  for (const f of otherFacets) {
    const sel = selections[f.key];
    if (!sel || sel.size === 0) continue;
    const map = ({
      type: idx.byType, topic: idx.byTopic,
      course: idx.byCourse, tags: idx.byTag,
    })[f.key];
    const sets = [];
    for (const v of sel) {
      const s = map.get(v);
      if (s) sets.push(s);
    }
    const facetUnion = sets.length ? setUnion(sets) : new Set();
    pool = pool ? setIntersect(pool, facetUnion) : new Set(facetUnion);
  }
  // map for this facet
  const map = ({
    type: idx.byType, topic: idx.byTopic,
    course: idx.byCourse, tags: idx.byTag,
  })[facetKey];
  const counts = new Map();
  for (const [k, set] of map) {
    const c = pool ? setIntersect(pool, set).size : set.size;
    counts.set(k, c);
  }
  return counts;
}

// ---- predicate for current selection (used by graph.applyFilter)
// Returns a Set of node ids that pass all facets, or null if no
// facet has any selection (=> no filter active).
function filteredIds(selections, idx) {
  const haveAny = FACETS.some(f => selections[f.key] && selections[f.key].size > 0);
  if (!haveAny) return null;
  let pool = null;
  for (const f of FACETS) {
    const sel = selections[f.key];
    if (!sel || sel.size === 0) continue;
    const map = ({
      type: idx.byType, topic: idx.byTopic,
      course: idx.byCourse, tags: idx.byTag,
    })[f.key];
    const sets = [];
    for (const v of sel) {
      const s = map.get(v);
      if (s) sets.push(s);
    }
    const facetUnion = sets.length ? setUnion(sets) : new Set();
    pool = pool ? setIntersect(pool, facetUnion) : new Set(facetUnion);
  }
  return pool || new Set();
}

// ---- main mount ------------------------------------------------
export function mountFilters({ root, data, store }) {
  const idx = indexNodes(data.nodes);
  // initial selection from URL
  const selections = readUrl();

  // assemble chip metadata once: array per facet of {id, label, swatch, glyph, totalCount}
  const facetMeta = {};

  // type
  facetMeta.type = (data.facets.types || []).map(f => ({
    id: f.id,
    label: typeLabel(f),
    glyphHtml: typeGlyphHtml(f.id),
    swatchColor: null,
  }));

  // topic — pull color from CSS variable to keep palette single-sourced
  facetMeta.topic = (data.facets.topics || []).map(f => ({
    id: f.id,
    label: topicLabel(f),
    glyphHtml: null,
    swatchColor: getComputedStyle(document.documentElement)
      .getPropertyValue(`--topic-${f.id}`).trim() || f.color || '#888',
  }));

  // course
  facetMeta.course = (data.facets.courses || []).map(f => ({
    id: f.id,
    label: courseLabel(f),
    glyphHtml: null,
    swatchColor: null,
  }));

  // tags
  facetMeta.tags = (data.facets.tags || []).map(f => ({
    id: f.id,
    label: f.id,
    glyphHtml: null,
    swatchColor: null,
  }));

  // wipe scaffold and rebuild
  root.innerHTML = '';
  const groupContainers = {};
  for (const f of FACETS) {
    const grp = document.createElement('div');
    grp.className = 'network-filter-group';
    grp.dataset.facet = f.key;
    const h3 = document.createElement('h3');
    h3.textContent = f.labelFr;
    grp.appendChild(h3);
    const chips = document.createElement('div');
    chips.className = 'network-chips';
    grp.appendChild(chips);
    root.appendChild(grp);
    groupContainers[f.key] = chips;
  }

  // reset button
  const resetWrap = document.createElement('div');
  resetWrap.className = 'network-filter-group';
  const resetBtn = document.createElement('button');
  resetBtn.type = 'button';
  resetBtn.className = 'network-counter-reset';
  resetBtn.textContent = 'Réinitialiser';
  resetBtn.style.marginTop = '0.5rem';
  resetWrap.appendChild(resetBtn);
  root.appendChild(resetWrap);

  function rerender() {
    for (const f of FACETS) {
      const counts = countsFor(f.key, selections, idx);
      const wrap = groupContainers[f.key];
      wrap.innerHTML = '';
      for (const meta of facetMeta[f.key]) {
        const cnt = counts.get(meta.id) ?? 0;
        const chip = renderChip({
          id: meta.id,
          label: meta.label,
          count: cnt,
          swatchColor: meta.swatchColor,
          glyphHtml: meta.glyphHtml,
          pressed: selections[f.key].has(meta.id),
        });
        wrap.appendChild(chip);
      }
    }
  }

  function publish() {
    const ids = filteredIds(selections, idx);
    store.set({ filteredNodeIds: ids });
    writeUrl(selections);
    rerender();
    updateCounter(ids ? ids.size : data.nodes.length, data.nodes.length);
  }

  // delegated click handler
  root.addEventListener('click', evt => {
    const chip = evt.target.closest('.network-chip');
    if (chip) {
      const facetEl = chip.closest('.network-filter-group');
      const fkey = facetEl?.dataset.facet;
      if (!fkey) return;
      const id = chip.dataset.id;
      const sel = selections[fkey];
      if (sel.has(id)) sel.delete(id); else sel.add(id);
      publish();
      return;
    }
    if (evt.target === resetBtn) {
      for (const f of FACETS) selections[f.key].clear();
      publish();
    }
  });

  // first paint
  publish();

  return { selections };
}

function updateCounter(shown, total) {
  const el = document.getElementById('network-counter-text');
  if (!el) return;
  el.innerHTML = shown === total
    ? `<strong>${total}</strong> matériaux affichés`
    : `<strong>${shown}</strong> matériaux affichés (sur ${total})`;
}
