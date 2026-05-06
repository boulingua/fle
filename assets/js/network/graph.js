/* Materials Discovery Network — Cytoscape rendering.

   Why Cytoscape over D3-force / sigma / vis-network:
     - Handles 500–2000 nodes with `fcose` layout smoothly.
     - Themeable via stylesheet objects that read CSS variables
       at apply time → light/dark swap is one re-style, no rebuild.
     - First-class compound nodes (future: group by course).
     - Smaller and more actively maintained than D3-force for
       this exact pattern; sigma is faster but harder to style;
       vis-network has heavier visual defaults.

   Public API exposed via createGraph():
     - cy            : the Cytoscape instance
     - applyFilter() : (predicate: node => bool) → dim non-matching
     - destroy()     : clean teardown
*/

const TYPE_SHAPE = {
  article: 'ellipse',
  presentation: 'rectangle',
  worksheet: 'diamond',
};

const DIM_OPACITY = 0.12;
const TOPIC_FALLBACK = '#888888';

function topicColor(topicId) {
  if (!topicId) return TOPIC_FALLBACK;
  const v = getComputedStyle(document.documentElement)
    .getPropertyValue(`--topic-${topicId}`).trim();
  return v || TOPIC_FALLBACK;
}

function fgColor() {
  const v = getComputedStyle(document.documentElement)
    .getPropertyValue('--network-fg').trim();
  return v || '#23272b';
}

function highlightColor() {
  const v = getComputedStyle(document.documentElement)
    .getPropertyValue('--network-highlight').trim();
  return v || '#C9A227';
}

function buildStylesheet() {
  return [
    {
      selector: 'node',
      style: {
        'shape': ele => TYPE_SHAPE[ele.data('type')] || 'ellipse',
        'background-color': ele => topicColor(ele.data('topic')),
        'background-opacity': ele => ele.data('type') === 'article' ? 1 : 0.85,
        'width': ele => ele.data('type') === 'article' ? 18 : 13,
        'height': ele => ele.data('type') === 'article' ? 18 : 13,
        'border-width': 0,
        'label': '',
        'transition-property': 'opacity, width, height, border-width',
        'transition-duration': '160ms',
      },
    },
    {
      selector: 'node.dim',
      style: { 'opacity': DIM_OPACITY },
    },
    {
      selector: 'node:active, node.hover',
      style: {
        'border-width': 2,
        'border-color': highlightColor(),
        'overlay-opacity': 0,
        'width': ele => ele.data('type') === 'article' ? 22 : 17,
        'height': ele => ele.data('type') === 'article' ? 22 : 17,
      },
    },
    {
      selector: 'edge',
      style: {
        'curve-style': 'straight',
        'width': ele => Math.max(1, ele.data('weight') || 1) * 0.6,
        'line-color': ele => ele.data('kind') === 'same-article'
          ? fgColor()
          : topicColor(ele.source().data('topic')),
        'line-opacity': ele => ele.data('kind') === 'same-article' ? 0.30 : 0.20,
        'transition-property': 'opacity',
        'transition-duration': '160ms',
      },
    },
    {
      selector: 'edge.dim',
      style: { 'opacity': DIM_OPACITY * 0.5 },
    },
  ];
}

export function createGraph({ container, data }) {
  if (!window.cytoscape) {
    throw new Error('Cytoscape not loaded — check <script> in head.');
  }
  if (window.cytoscapeFcose) {
    window.cytoscape.use(window.cytoscapeFcose);
  }

  const cy = window.cytoscape({
    container,
    elements: {
      nodes: data.nodes.map(n => ({ data: n })),
      edges: data.edges.map((e, i) => ({
        data: { ...e, id: `e${i}-${e.source}-${e.target}` },
      })),
    },
    style: buildStylesheet(),
    wheelSensitivity: 0.25,
    minZoom: 0.2,
    maxZoom: 3,
    layout: window.cytoscapeFcose ? {
      name: 'fcose',
      quality: 'default',
      animate: false,
      randomize: true,
      nodeRepulsion: 4500,
      idealEdgeLength: 50,
      edgeElasticity: 0.45,
      gravity: 0.25,
      numIter: 2500,
    } : { name: 'cose', animate: false },
  });

  // Hover ↔ class. (Cytoscape keyboard support is a separate plugin;
  // we'll wire :focus + arrow keys in Phase 6 a11y pass.)
  cy.on('mouseover', 'node', evt => evt.target.addClass('hover'));
  cy.on('mouseout',  'node', evt => evt.target.removeClass('hover'));

  function applyFilter(predicate) {
    if (typeof predicate !== 'function') {
      cy.elements().removeClass('dim');
      return;
    }
    cy.batch(() => {
      cy.nodes().forEach(n => {
        n.toggleClass('dim', !predicate(n.data()));
      });
      cy.edges().forEach(e => {
        const src = e.source();
        const tgt = e.target();
        e.toggleClass('dim', src.hasClass('dim') || tgt.hasClass('dim'));
      });
    });
  }

  function applyTheme() {
    cy.style().fromJson(buildStylesheet()).update();
  }

  function destroy() { cy.destroy(); }

  return { cy, applyFilter, applyTheme, destroy };
}
