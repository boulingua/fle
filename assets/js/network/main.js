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

  // Phase 5 will attach: search → store.set({ searchQuery })
  // Phase 5 will subscribe: list view re-renders from store
  store.subscribe(s => {
    if (s.filteredNodeIds == null) {
      graph.applyFilter(null);
    } else {
      graph.applyFilter(d => s.filteredNodeIds.has(d.id));
    }
  });

  // Phase 4: filter rail.
  const filterRail = document.querySelector('.network-filters');
  if (filterRail) {
    mountFilters({ root: filterRail, data, store });
  }

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
