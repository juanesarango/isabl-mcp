"""Render a knowledge tree as an interactive D3.js node-link diagram."""

from __future__ import annotations

import json

from isabl_knowledge.models import Document, TreeNode

HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Isabl Knowledge Tree</title>
<script src="https://d3js.org/d3.v7.min.js"></script>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background: #0d1117; color: #e6edf3; overflow: hidden;
  }
  #header {
    position: fixed; top: 0; left: 0; right: 0; z-index: 10;
    background: #0d1117ee; backdrop-filter: blur(8px);
    padding: 1rem 1.5rem; display: flex; align-items: center; gap: 1rem;
    border-bottom: 1px solid #21262d;
  }
  h1 { font-size: 1.2rem; white-space: nowrap; }
  .controls { display: flex; gap: 0.5rem; }
  .btn {
    padding: 0.3rem 0.7rem; background: #21262d; border: 1px solid #30363d;
    color: #8b949e; border-radius: 6px; cursor: pointer; font-size: 0.75rem;
  }
  .btn:hover { background: #30363d; color: #e6edf3; }
  .stats { color: #8b949e; font-size: 0.75rem; margin-left: auto; }
  #canvas { width: 100vw; height: 100vh; padding-top: 52px; }
  svg { width: 100%; height: 100%; }

  .link { fill: none; stroke: #30363d; stroke-width: 1.5; }
  .node-group { cursor: pointer; }
  .node-rect {
    rx: 6; ry: 6; stroke-width: 1.5;
    transition: filter 0.15s;
  }
  .node-group:hover .node-rect { filter: brightness(1.2); }
  .node-label {
    font-size: 11px; fill: #e6edf3; font-weight: 500;
    pointer-events: none;
  }
  .node-badge {
    font-size: 9px; fill: #8b949e; pointer-events: none;
  }
  .node-collapse {
    font-size: 10px; fill: #58a6ff; pointer-events: none;
  }

  /* Tooltip */
  #tooltip {
    position: fixed; pointer-events: none; z-index: 20;
    background: #161b22; border: 1px solid #30363d; border-radius: 8px;
    padding: 0.8rem 1rem; max-width: 350px; display: none;
    box-shadow: 0 4px 12px #00000066;
  }
  #tooltip .tt-title { font-weight: 600; font-size: 0.85rem; margin-bottom: 0.3rem; }
  #tooltip .tt-summary { color: #8b949e; font-size: 0.8rem; margin-bottom: 0.4rem; }
  #tooltip .tt-docs { font-size: 0.75rem; color: #58a6ff; }
  #tooltip .tt-hint { font-size: 0.7rem; color: #484f58; margin-top: 0.4rem; }

  /* Detail panel */
  #panel {
    position: fixed; top: 52px; right: 0; width: 380px; height: calc(100vh - 52px);
    background: #161b22; border-left: 1px solid #30363d; z-index: 15;
    overflow-y: auto; padding: 1.5rem; display: none;
  }
  #panel.open { display: block; }
  #panel .close {
    position: absolute; top: 0.8rem; right: 0.8rem; background: none;
    border: none; color: #8b949e; font-size: 1.2rem; cursor: pointer;
  }
  #panel h2 { font-size: 1rem; margin-bottom: 0.5rem; }
  #panel .p-summary { color: #8b949e; font-size: 0.85rem; margin-bottom: 1rem; }
  .doc-item {
    margin: 0.5rem 0; padding: 0.5rem 0.7rem; background: #0d1117;
    border-radius: 4px; border-left: 3px solid #1f6feb;
  }
  .doc-title { font-weight: 500; font-size: 0.8rem; }
  .doc-summary { font-size: 0.75rem; color: #8b949e; margin-top: 0.2rem; }
  .doc-tags { margin-top: 0.3rem; }
  .tag {
    display: inline-block; font-size: 0.65rem; background: #30363d;
    color: #8b949e; padding: 0.1rem 0.35rem; border-radius: 3px; margin: 0.1rem;
  }
  .doc-content {
    margin-top: 0.4rem; padding: 0.5rem; background: #0d1117;
    border: 1px solid #21262d; border-radius: 4px;
    font-size: 0.72rem; color: #c9d1d9; max-height: 200px;
    overflow-y: auto; white-space: pre-wrap; word-break: break-word;
    font-family: 'SFMono-Regular', Consolas, monospace; line-height: 1.4;
  }
  .doc-content-toggle {
    font-size: 0.7rem; color: #58a6ff; cursor: pointer;
    margin-top: 0.3rem; border: none; background: none; padding: 0;
  }
  .doc-content-toggle:hover { text-decoration: underline; }
  .doc-link {
    display: inline-block; margin-top: 0.3rem; font-size: 0.72rem;
    color: #58a6ff; text-decoration: none;
  }
  .doc-link:hover { text-decoration: underline; }
</style>
</head>
<body>

<div id="header">
  <h1>Isabl Knowledge Tree</h1>
  <div class="controls">
    <button class="btn" id="btn-expand">Expand All</button>
    <button class="btn" id="btn-collapse">Collapse All</button>
    <button class="btn" id="btn-fit">Fit View</button>
  </div>
  <span class="stats" id="stats"></span>
</div>

<div id="canvas"><svg id="svg"></svg></div>
<div id="tooltip"></div>
<div id="panel"><button class="close" id="panel-close">&times;</button><div id="panel-content"></div></div>

<script>
const TREE = __TREE_JSON__;
const DOCS = __DOCS_JSON__;

const COLORS = ['#1f6feb','#238636','#a371f7','#f0883e','#f85149','#79c0ff','#56d364','#d2a8ff'];

function countDocs(d) {
  let n = (d.documents || []).length;
  (d.children || []).forEach(c => n += countDocs(c));
  return n;
}

// Prepare hierarchy
const root = d3.hierarchy(TREE, d => d.children);
root.each(d => { d.data._docs = countDocs(d.data); });

// Store original children for collapse/expand
root.each(d => { d._children = d.children; });
// Start with first level expanded
root.children?.forEach(c => { c.children?.forEach(gc => collapse(gc)); });

function collapse(d) {
  if (d.children) {
    d._children = d.children;
    d._children.forEach(collapse);
    d.children = null;
  }
}
function expand(d) {
  if (d._children) {
    d.children = d._children;
    d.children.forEach(expand);
  }
}

const svg = d3.select('#svg');
const g = svg.append('g');
const zoom = d3.zoom().scaleExtent([0.1, 3]).on('zoom', e => g.attr('transform', e.transform));
svg.call(zoom);

const nodeW = 180, nodeH = 36, sepH = 8, sepV = 12;

function update(source) {
  const treemap = d3.tree().nodeSize([nodeH + sepH, nodeW + sepV]);
  const treeData = treemap(root);
  const nodes = treeData.descendants();
  const links = treeData.links();

  // Swap x/y for horizontal layout
  nodes.forEach(d => { const tmp = d.x; d.x = d.y; d.y = tmp; });

  // Links
  const link = g.selectAll('.link').data(links, d => d.target.data.id || d.target.data.title);
  link.exit().remove();
  const linkEnter = link.enter().append('path').attr('class', 'link');
  linkEnter.merge(link).transition().duration(300).attr('d', d => {
    return `M${d.source.x + nodeW/2},${d.source.y}
            C${(d.source.x + d.target.x + nodeW) / 2},${d.source.y}
             ${(d.source.x + d.target.x + nodeW) / 2},${d.target.y}
             ${d.target.x},${d.target.y}`;
  });

  // Nodes
  const node = g.selectAll('.node-group').data(nodes, d => d.data.id || d.data.title);
  node.exit().remove();

  const nodeEnter = node.enter().append('g').attr('class', 'node-group');

  nodeEnter.append('rect').attr('class', 'node-rect');
  nodeEnter.append('text').attr('class', 'node-label');
  nodeEnter.append('text').attr('class', 'node-badge');
  nodeEnter.append('text').attr('class', 'node-collapse');

  const nodeAll = nodeEnter.merge(node);

  nodeAll.transition().duration(300)
    .attr('transform', d => `translate(${d.x},${d.y - nodeH/2})`);

  nodeAll.select('.node-rect')
    .attr('width', nodeW).attr('height', nodeH)
    .attr('fill', d => {
      const idx = root.children ? root.children.indexOf(d.ancestors().find(a => a.depth === 1)) : 0;
      const c = COLORS[idx % COLORS.length];
      return d.depth === 0 ? '#1f6feb' : c + (d.children || d._children ? '33' : '1a');
    })
    .attr('stroke', d => {
      const idx = root.children ? root.children.indexOf(d.ancestors().find(a => a.depth === 1)) : 0;
      return d.depth === 0 ? '#58a6ff' : COLORS[idx % COLORS.length] + '88';
    });

  nodeAll.select('.node-label')
    .attr('x', 10).attr('y', nodeH/2 + 1)
    .attr('dominant-baseline', 'middle')
    .text(d => {
      const t = d.data.title;
      return t.length > 22 ? t.slice(0, 20) + '...' : t;
    });

  nodeAll.select('.node-badge')
    .attr('x', nodeW - 8).attr('y', nodeH/2 + 1)
    .attr('text-anchor', 'end').attr('dominant-baseline', 'middle')
    .text(d => d.data._docs ? d.data._docs : '');

  nodeAll.select('.node-collapse')
    .attr('x', nodeW - 8).attr('y', 11)
    .attr('text-anchor', 'end')
    .text(d => d._children && !d.children ? '+' : '');

  // Interactions
  nodeAll.on('click', (e, d) => {
    if (d.depth === 0) return;
    if (d.children) {
      d._children = d.children;
      d.children = null;
    } else if (d._children) {
      d.children = d._children;
    }
    update(d);
    e.stopPropagation();
  });

  nodeAll.on('mouseover', (e, d) => {
    const tt = document.getElementById('tooltip');
    tt.style.display = 'block';
    tt.innerHTML =
      '<div class="tt-title">' + d.data.title + '</div>' +
      (d.data.summary ? '<div class="tt-summary">' + d.data.summary + '</div>' : '') +
      (d.data._docs ? '<div class="tt-docs">' + d.data._docs + ' documents</div>' : '') +
      '<div class="tt-hint">Click to expand/collapse. Double-click for details.</div>';
  });

  nodeAll.on('mousemove', e => {
    const tt = document.getElementById('tooltip');
    tt.style.left = (e.clientX + 15) + 'px';
    tt.style.top = (e.clientY + 15) + 'px';
  });

  nodeAll.on('mouseout', () => {
    document.getElementById('tooltip').style.display = 'none';
  });

  nodeAll.on('dblclick', (e, d) => {
    showPanel(d.data);
    e.stopPropagation();
  });
}

function toggleContent(id) {
  const el = document.getElementById(id);
  const btn = el.previousElementSibling;
  if (el.style.display === 'none') {
    el.style.display = 'block';
    btn.textContent = 'Hide content';
  } else {
    el.style.display = 'none';
    btn.textContent = 'Show content';
  }
}

function showPanel(data) {
  const panel = document.getElementById('panel');
  const content = document.getElementById('panel-content');
  let html = '<h2>' + data.title + '</h2>';
  if (data.summary) html += '<p class="p-summary">' + data.summary + '</p>';

  const docIds = data.documents || [];
  if (docIds.length) {
    html += '<h3 style="font-size:0.85rem;margin-bottom:0.5rem;">Documents (' + docIds.length + ')</h3>';
    docIds.forEach(id => {
      const doc = DOCS[id];
      if (!doc) return;
      const cid = 'doc-content-' + id.replace(/[^a-zA-Z0-9]/g, '_');
      html += '<div class="doc-item">' +
        '<div class="doc-title">' + (doc.title || id) + '</div>' +
        (doc.source_url ? '<a class="doc-link" href="' + doc.source_url + '" target="_blank">View source</a>' : '') +
        (doc.summary ? '<div class="doc-summary">' + doc.summary + '</div>' : '') +
        (doc.tags?.length ? '<div class="doc-tags">' +
          doc.tags.map(t => '<span class="tag">' + t + '</span>').join('') + '</div>' : '') +
        (doc.content ? '<button class="doc-content-toggle" onclick="toggleContent(\'' + cid + '\')">Show content</button>' +
          '<div class="doc-content" id="' + cid + '" style="display:none">' +
          doc.content.replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;") + '</div>' : '') +
        '</div>';
    });
  }
  content.innerHTML = html;
  panel.classList.add('open');
}

document.getElementById('panel-close').onclick = () =>
  document.getElementById('panel').classList.remove('open');

document.getElementById('btn-expand').onclick = () => { root.each(d => { if (d._children) d.children = d._children; }); update(root); };
document.getElementById('btn-collapse').onclick = () => { root.children?.forEach(c => { collapse(c); }); update(root); };
document.getElementById('btn-fit').onclick = fitView;

function fitView() {
  const bounds = g.node().getBBox();
  const parent = svg.node().getBoundingClientRect();
  const scale = Math.min(
    parent.width / (bounds.width + 100),
    parent.height / (bounds.height + 100),
    1.5
  );
  const tx = parent.width / 2 - (bounds.x + bounds.width / 2) * scale;
  const ty = parent.height / 2 - (bounds.y + bounds.height / 2) * scale;
  svg.transition().duration(500).call(
    zoom.transform, d3.zoomIdentity.translate(tx, ty).scale(scale)
  );
}

// Init
update(root);
setTimeout(fitView, 100);

document.getElementById('stats').textContent =
  root.descendants().length + ' nodes \u00B7 ' + countDocs(TREE) + ' documents';
</script>
</body>
</html>"""


def render_tree_to_html(
    tree: TreeNode,
    documents: dict[str, Document],
) -> str:
    """Render tree as an interactive D3.js node-link diagram."""
    tree_json = json.dumps(tree.model_dump()).replace("</", r"<\/")
    docs_json = json.dumps({
        doc_id: {
            "title": doc.title,
            "summary": doc.summary,
            "tags": doc.tags,
            "content": doc.content,
            "source_url": doc.source_url,
        }
        for doc_id, doc in documents.items()
    }).replace("</", r"<\/")
    return (HTML_TEMPLATE
        .replace("__TREE_JSON__", tree_json)
        .replace("__DOCS_JSON__", docs_json))
