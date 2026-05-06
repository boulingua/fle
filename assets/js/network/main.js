/* Materials Discovery Network — entry point.

   Boots the graph on /materiel/preview/ (Phase 3 surface; the
   canonical /materiel/ flips over to this in Phase 6+). Skipped
   on viewports below 768px — the graph is not useful there and
   the JS payload is wasted.

   Theme observer: Coder toggles light/dark via body classes
   (`colorscheme-light`, `colorscheme-dark`, `colorscheme-auto`).
   We watch for class changes on body + the OS preference media
   query and re-apply the Cytoscape stylesheet on every flip.
*/
import { createStore } from './store.js';
import { createGraph } from './graph.js';
import { mountFilters } from './filters.js';
import { mountList } from './list.js';
import { mountSearch } from './search.js';

const SMALL_VIEWPORT = '(max-width: 767px)';
const GRAPH_JSON_URL = '/fle/network/graph.json';

async function fetchGraph(url) {
  const res = await fetch(url, { credentials: 'same-origin' });
  if (!res.ok) throw new Error(`graph.json: HTTP ${res.status}`);
  return res.json();
}

function watchTheme(onChange) {
  const body = document.body;
  const mq = window.matchMedia('(prefers-color-scheme: dark)');
  const obs = new MutationObserver(onChange);
  obs.observe(body, { attributes: true, attributeFilter: ['class'] });
  if (mq.addEventListener) mq.addEventListener('change', onChange);
  else mq.addListener(onChange);
  return () => {
    obs.disconnect();
    if (mq.removeEventListener) mq.removeEventListener('change', onChange);
    else mq.removeListener(onChange);
  };
}

async function boot() {
  if (window.matchMedia(SMALL_VIEWPORT).matches) return;
  const container = document.getElementById('network-graph');
  if (!container) return;

  // Skeleton stays visible until first paint of the graph.
  const skeleton = container.querySelector('.network-graph-skeleton');

  let data;
  try {
    data = await fetchGraph(GRAPH_JSON_URL);
  } catch (err) {
    console.error('[network] failed to load graph.json:', err);
    if (skeleton) skeleton.textContent = '⚠ Graphe indisponible.';
    return;
  }

  const store = createStore({
    filteredNodeIds: null,
    hoveredNodeId: null,
    searchQuery: '',
  });

  // Wait one frame so the surrounding layout is sized — fcose
  // computes geometry from the container dimensions.
  await new Promise(r => requestAnimationFrame(r));

  const graph = createGraph({ container, data });
  if (skeleton) skeleton.style.display = 'none';

  watchTheme(() => graph.applyTheme());

  // graph subscriber: combine facet filter ∩ search match
  store.subscribe(s => {
    const fid = s.filteredNodeIds;
    const sid = s.searchMatchIds;
    if (fid == null && sid == null) {
      graph.applyFilter(null);
    } else {
      graph.applyFilter(d => {
        if (fid && !fid.has(d.id)) return false;
        if (sid && !sid.has(d.id)) return false;
        return true;
      });
    }
    // bidirectional hover sync: card hover -> graph node .hover class
    graph.cy.nodes().removeClass('hover');
    if (s.hoveredNodeId) {
      const node = graph.cy.getElementById(s.hoveredNodeId);
      if (node && node.length) node.addClass('hover');
    }
  });

  // Phase 4: filter rail.
  const filterRail = document.querySelector('.network-filters');
  if (filterRail) {
    mountFilters({ root: filterRail, data, store });
  }

  // Phase 5: list view (cards below the graph).
  const cardsRoot = document.getElementById('network-cards');
  if (cardsRoot) {
    mountList({ root: cardsRoot, data, store });
  }

  // Phase 5: search input + Pagefind.
  const searchInput = document.querySelector('.network-search-input');
  if (searchInput) {
    mountSearch({ input: searchInput, data, store });
  }

  // Phase 5: graph node hover -> store, so list scrolls / future
  // hover-targeting works in the other direction too.
  graph.cy.on('mouseover', 'node', evt => {
    store.set({ hoveredNodeId: evt.target.id() });
  });
  graph.cy.on('mouseout', 'node', () => {
    store.set({ hoveredNodeId: null });
  });

  // expose for debugging — non-enumerable
  Object.defineProperty(window, '__network', {
    value: { store, graph, data },
    enumerable: false,
  });
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', boot);
} else {
  boot();
}
