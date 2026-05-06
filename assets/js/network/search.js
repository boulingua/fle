/* Materials Discovery Network — full-text search.

   Pagefind is built post-Hugo by CI (`npx pagefind --site public`)
   and lives at /fle/pagefind/pagefind.js. We dynamic-import it on
   first interaction so the cold-load JS payload stays small.

   The search reduces the visible set by URL: pagefind returns
   article URLs, we map those to article nodes, then expand to
   include each article's related[] (presentation + worksheet).
   The result is pushed to store.searchMatchIds as a Set; the
   filter rail's filteredNodeIds is intersected separately by
   the graph and list subscribers.

   Keyboard:
     /    focus the search input (unless already in a textarea/input)
     Esc  clear and blur
*/

const PAGEFIND_URL = '/fle/pagefind/pagefind.js';
const DEBOUNCE_MS = 80;

let pagefind = null;
let pagefindLoadPromise = null;

function loadPagefind() {
  if (pagefindLoadPromise) return pagefindLoadPromise;
  pagefindLoadPromise = (async () => {
    try {
      const mod = await import(/* @vite-ignore */ PAGEFIND_URL);
      pagefind = mod;
      if (mod.options) await mod.options({ excerptLength: 24 });
      return mod;
    } catch (err) {
      console.warn('[network] Pagefind unavailable:', err.message);
      return null;
    }
  })();
  return pagefindLoadPromise;
}

function debounce(fn, ms) {
  let t;
  return (...args) => {
    clearTimeout(t);
    t = setTimeout(() => fn(...args), ms);
  };
}

function urlToArticleId(url, urlToId) {
  if (!url) return null;
  // strip baseURL prefix and trailing slash for matching
  let u = url.replace(/^https?:\/\/[^/]+/, '');
  if (u.startsWith('/fle')) u = u.slice(4);
  if (!u.endsWith('/')) u += '/';
  return urlToId.get(u) || null;
}

export function mountSearch({ input, data, store }) {
  if (!input) return;
  // build url → article-id index once (only article nodes have stable URLs)
  const urlToId = new Map();
  for (const n of data.nodes) {
    if (n.type === 'article' && n.url) urlToId.set(n.url, n.id);
  }

  const idToRelated = new Map(
    data.nodes.filter(n => n.type === 'article')
      .map(n => [n.id, n.related || []])
  );

  async function runSearch(query) {
    const q = query.trim();
    if (!q) {
      store.set({ searchMatchIds: null, searchQuery: '' });
      return;
    }
    const pf = await loadPagefind();
    if (!pf) {
      // pagefind unavailable; fall back to local title search
      const ids = new Set();
      const needle = q.toLowerCase();
      for (const n of data.nodes) {
        if (n.type !== 'article') continue;
        if ((n.title || '').toLowerCase().includes(needle) ||
            (n.description || '').toLowerCase().includes(needle)) {
          ids.add(n.id);
          for (const r of (idToRelated.get(n.id) || [])) ids.add(r);
        }
      }
      store.set({ searchMatchIds: ids, searchQuery: q });
      return;
    }
    const search = await pf.search(q);
    if (!search || !search.results) {
      store.set({ searchMatchIds: new Set(), searchQuery: q });
      return;
    }
    // collect article ids from URLs (only top 50 to keep responsive)
    const ids = new Set();
    const promises = search.results.slice(0, 50).map(r => r.data());
    const datas = await Promise.all(promises);
    for (const d of datas) {
      const id = urlToArticleId(d.url, urlToId);
      if (id) {
        ids.add(id);
        for (const r of (idToRelated.get(id) || [])) ids.add(r);
      }
    }
    store.set({ searchMatchIds: ids, searchQuery: q });
  }

  const debounced = debounce(runSearch, DEBOUNCE_MS);
  input.addEventListener('input', e => debounced(e.target.value));
  input.disabled = false;

  // keyboard: '/' focus, Esc clear
  document.addEventListener('keydown', evt => {
    if (evt.key === '/' && !evt.ctrlKey && !evt.metaKey && !evt.altKey) {
      const tag = (document.activeElement?.tagName || '').toLowerCase();
      if (tag !== 'input' && tag !== 'textarea') {
        evt.preventDefault();
        input.focus();
        input.select();
      }
    } else if (evt.key === 'Escape' && document.activeElement === input) {
      input.value = '';
      input.blur();
      runSearch('');
    }
  });
}
