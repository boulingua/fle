/* Materials Discovery Network — selection store.

   Tiny pub/sub. No framework. Single source of truth for which
   nodes are currently in the filtered set, which is hovered, and
   the live search query. The graph and the (Phase 5) list view
   both subscribe; one mutation triggers one render pass.
*/
export function createStore(initial = {}) {
  const state = {
    filteredNodeIds: null,   // null = no filter active (everything passes)
    hoveredNodeId: null,
    searchQuery: '',
    ...initial,
  };
  const subs = new Set();
  return {
    get() { return state; },
    set(patch) {
      Object.assign(state, patch);
      subs.forEach(fn => fn(state));
    },
    subscribe(fn) {
      subs.add(fn);
      return () => subs.delete(fn);
    },
  };
}
