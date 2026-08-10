"""Shared HTML shell for every page.

Each page is rendered as a single full-width `components.html` iframe. Because an
iframe cannot blur the parent document, every page carries its own animated
background layer — that is what the glass panels actually frost. The parent
document (styled in `theme.py`) uses a matching base colour so the seams between
iframes are invisible.
"""

import json

import streamlit.components.v1 as components

from utils.constants import SEGMENT_COLORS, SEGMENT_GLOW

FONTS = (
    "https://fonts.googleapis.com/css2?"
    "family=Inter:wght@400;500;600;700;800;900&"
    "family=Sora:wght@600;700;800&display=swap"
)

BASE_CSS = """
*, *::before, *::after { box-sizing: border-box; }

html, body {
    margin: 0;
    padding: 0;
    background: transparent;
    color: var(--ink);
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    -webkit-font-smoothing: antialiased;
    overflow-x: hidden;
}

:root {
    --bg-0: #070B14;
    --bg-1: #0C1322;
    --ink: #F1F5F9;
    --ink-dim: #CBD5E1;
    --muted: #8B9AB4;
    --stroke: rgba(255,255,255,.11);
    --stroke-hi: rgba(255,255,255,.22);
    --glass: rgba(255,255,255,.045);
    --glass-hi: rgba(255,255,255,.075);
    --amber: #F3A64A;
    --amber-deep: #D9822B;
    --violet: #8B5CF6;
    --cyan: #22D3EE;
    --radius: 26px;
    --shadow: 0 24px 60px rgba(0,0,0,.45);
}

/* ---------- background stack ---------- */
.bg-layer {
    position: fixed;
    inset: 0;
    z-index: 0;
    pointer-events: none;
}

#bgCanvas { position: fixed; inset: 0; z-index: 0; pointer-events: none; }

.bg-mesh {
    background:
        radial-gradient(58% 44% at 12% 8%,  rgba(139,92,246,.13), transparent 62%),
        radial-gradient(50% 40% at 88% 12%, rgba(243,166,74,.11), transparent 60%),
        radial-gradient(60% 50% at 72% 92%, rgba(34,211,238,.09), transparent 65%),
        linear-gradient(175deg, #070B14 0%, #0C1322 55%, #070B14 100%);
    animation: meshDrift 26s ease-in-out infinite alternate;
}

@keyframes meshDrift {
    0%   { transform: scale(1)    translate3d(0,0,0); }
    100% { transform: scale(1.14) translate3d(-2%, -1.5%, 0); }
}

.bg-grid {
    background-image:
        linear-gradient(rgba(255,255,255,.028) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,255,255,.028) 1px, transparent 1px);
    background-size: 62px 62px;
    mask-image: radial-gradient(72% 60% at 50% 40%, #000 20%, transparent 88%);
    -webkit-mask-image: radial-gradient(72% 60% at 50% 40%, #000 20%, transparent 88%);
}

/* Deliberately no vignette layer: a fixed-position darkening gradient anchors to
   the iframe viewport, which would paint a dark band at the foot of every page
   iframe and give away the join with the parent document. */

/* ---------- layout ---------- */
.stage {
    position: relative;
    z-index: 2;
    max-width: 1180px;
    margin: 0 auto;
    padding: 6px 26px 40px 26px;
    perspective: 1600px;
}

.row { display: grid; gap: 20px; }
.row-2 { grid-template-columns: repeat(2, minmax(0,1fr)); }
.row-3 { grid-template-columns: repeat(3, minmax(0,1fr)); }
.row-4 { grid-template-columns: repeat(4, minmax(0,1fr)); }
.row-12 { grid-template-columns: 1.15fr .85fr; }
.row-21 { grid-template-columns: .85fr 1.15fr; }
.mt-20 { margin-top: 20px; } .mt-32 { margin-top: 32px; } .mt-44 { margin-top: 44px; }

@media (max-width: 900px) {
    .row-2, .row-3, .row-4, .row-12, .row-21 { grid-template-columns: 1fr; }
}

/* ---------- glass surfaces ---------- */
.glass {
    position: relative;
    background: linear-gradient(150deg, var(--glass-hi), var(--glass));
    border: 1px solid var(--stroke);
    border-radius: var(--radius);
    backdrop-filter: blur(22px) saturate(150%);
    -webkit-backdrop-filter: blur(22px) saturate(150%);
    box-shadow: var(--shadow), inset 0 1px 0 rgba(255,255,255,.10);
    overflow: hidden;
    transform-style: preserve-3d;
}

/* the specular sheen that sells the 3D tilt */
.glass::after {
    content: "";
    position: absolute;
    inset: 0;
    border-radius: inherit;
    background: radial-gradient(
        420px circle at var(--mx, 50%) var(--my, 0%),
        rgba(255,255,255,.13), transparent 42%
    );
    opacity: 0;
    transition: opacity .35s ease;
    pointer-events: none;
}
.glass:hover::after { opacity: 1; }

.pad { padding: 26px 28px; }
.pad-lg { padding: 34px 36px; }

/* ---------- 3D tilt ---------- */
[data-tilt] {
    transition: transform .5s cubic-bezier(.2,.8,.25,1), box-shadow .5s ease,
                border-color .5s ease;
    will-change: transform;
}
[data-tilt]:hover {
    border-color: var(--stroke-hi);
    box-shadow: 0 38px 90px rgba(0,0,0,.58), inset 0 1px 0 rgba(255,255,255,.16);
}
[data-tilt] .lift { transform: translateZ(38px); transform-style: preserve-3d; }
[data-tilt] .lift-sm { transform: translateZ(18px); }

/* ---------- scroll reveal ---------- */
[data-reveal] {
    opacity: 0;
    transform: translate3d(0, 34px, -60px) rotateX(7deg);
    transition: opacity .85s cubic-bezier(.2,.8,.25,1),
                transform .85s cubic-bezier(.2,.8,.25,1);
}
[data-reveal].in { opacity: 1; transform: none; }

/* ---------- typography ---------- */
.eyebrow {
    display: inline-flex; align-items: center; gap: 9px;
    font-size: 11px; font-weight: 800; letter-spacing: .17em;
    text-transform: uppercase; color: var(--amber);
    padding: 7px 14px; border-radius: 999px;
    background: rgba(243,166,74,.10);
    border: 1px solid rgba(243,166,74,.26);
}
.eyebrow .dot {
    width: 6px; height: 6px; border-radius: 50%;
    background: var(--amber); box-shadow: 0 0 12px var(--amber);
    animation: pulse 2.4s ease-in-out infinite;
}
@keyframes pulse { 0%,100% { opacity: 1; } 50% { opacity: .35; } }

h1.display {
    font-family: 'Sora', 'Inter', sans-serif;
    font-size: clamp(34px, 4.6vw, 58px);
    line-height: 1.04; letter-spacing: -.035em;
    margin: 20px 0 0 0; font-weight: 800;
    background: linear-gradient(180deg, #FFFFFF 8%, #A7B4CC 96%);
    -webkit-background-clip: text; background-clip: text; color: transparent;
}
.grad-amber {
    background: linear-gradient(100deg, #FCD9A0, var(--amber), var(--amber-deep));
    -webkit-background-clip: text; background-clip: text; color: transparent;
}

h2.section {
    font-family: 'Sora', 'Inter', sans-serif;
    font-size: 27px; font-weight: 700; letter-spacing: -.025em;
    margin: 0 0 6px 0; color: #FFFFFF;
}
h3.card-title {
    font-family: 'Sora','Inter',sans-serif;
    font-size: 17px; font-weight: 700; letter-spacing: -.012em;
    margin: 0 0 10px 0; color: #FFFFFF;
}
p.lede { font-size: 17px; line-height: 1.66; color: var(--ink-dim); margin: 16px 0 0 0; max-width: 62ch; }
p.body { font-size: 14.5px; line-height: 1.72; color: var(--muted); margin: 0; }
p.body strong { color: var(--ink-dim); font-weight: 600; }
.section-sub { font-size: 14.5px; color: var(--muted); margin: 0 0 22px 0; }

/* ---------- KPI ---------- */
.kpi-label {
    font-size: 10.5px; font-weight: 800; letter-spacing: .15em;
    text-transform: uppercase; color: var(--muted); margin-bottom: 14px;
}
.kpi-value {
    font-family: 'Sora','Inter',sans-serif;
    font-size: 38px; font-weight: 800; letter-spacing: -.035em;
    line-height: 1; color: #FFFFFF;
}
.kpi-value .unit { font-size: 22px; color: var(--muted); margin-left: 3px; font-weight: 700; }
.kpi-foot { margin-top: 12px; font-size: 12.5px; color: var(--muted); line-height: 1.5; }
.kpi-spark { margin-top: 16px; height: 3px; border-radius: 999px; background: rgba(255,255,255,.08); overflow: hidden; }
.kpi-spark i { display: block; height: 100%; width: 0; border-radius: 999px; transition: width 1.5s cubic-bezier(.2,.8,.25,1); }

/* ---------- chips / pills ---------- */
.chip {
    display: inline-flex; align-items: center; gap: 8px;
    padding: 8px 14px; border-radius: 999px;
    background: rgba(255,255,255,.05);
    border: 1px solid var(--stroke);
    font-size: 12.5px; font-weight: 600; color: var(--ink-dim);
}
.chip .swatch { width: 9px; height: 9px; border-radius: 3px; }
.chips { display: flex; flex-wrap: wrap; gap: 10px; }

/* ---------- lists ---------- */
ul.ticks { list-style: none; margin: 0; padding: 0; }
ul.ticks li {
    position: relative; padding: 11px 0 11px 30px;
    font-size: 14.5px; color: var(--ink-dim); line-height: 1.55;
    border-bottom: 1px solid rgba(255,255,255,.055);
}
ul.ticks li:last-child { border-bottom: none; }
ul.ticks li::before {
    content: ""; position: absolute; left: 4px; top: 18px;
    width: 8px; height: 8px; border-radius: 50%;
    background: var(--amber); box-shadow: 0 0 12px rgba(243,166,74,.7);
}

/* ---------- table ---------- */
table.data { width: 100%; border-collapse: collapse; font-size: 13.5px; }
table.data th {
    text-align: left; font-size: 10.5px; letter-spacing: .13em;
    text-transform: uppercase; color: var(--muted); font-weight: 800;
    padding: 0 14px 14px 14px; border-bottom: 1px solid var(--stroke);
}
table.data td {
    padding: 15px 14px; color: var(--ink-dim);
    border-bottom: 1px solid rgba(255,255,255,.05);
}
table.data tr:last-child td { border-bottom: none; }
table.data tr { transition: background .3s ease; }
table.data tbody tr:hover { background: rgba(255,255,255,.035); }
table.data td.num { text-align: right; font-variant-numeric: tabular-nums; color: #FFFFFF; font-weight: 600; }
.seg-cell { display: flex; align-items: center; gap: 11px; }
.seg-cell .bar { width: 3px; height: 22px; border-radius: 2px; }

/* ---------- step / timeline ---------- */
.steps { position: relative; padding-left: 34px; }
.steps::before {
    content: ""; position: absolute; left: 11px; top: 8px; bottom: 8px; width: 2px;
    background: linear-gradient(180deg, var(--amber), rgba(139,92,246,.55), transparent);
}
.step { position: relative; padding: 0 0 26px 0; }
.step:last-child { padding-bottom: 0; }
.step::before {
    content: ""; position: absolute; left: -28px; top: 5px;
    width: 12px; height: 12px; border-radius: 50%;
    background: var(--bg-1); border: 2px solid var(--amber);
    box-shadow: 0 0 0 4px rgba(243,166,74,.13);
}
.step .st-title { font-size: 15px; font-weight: 700; color: #FFFFFF; margin-bottom: 5px; }
.step .st-body { font-size: 13.5px; color: var(--muted); line-height: 1.6; }

/* ---------- misc ---------- */
.divider { height: 1px; background: linear-gradient(90deg, transparent, var(--stroke), transparent); margin: 40px 0; }
.orbit-badge {
    position: absolute; right: 26px; top: 24px;
    font-size: 10.5px; font-weight: 800; letter-spacing: .13em;
    text-transform: uppercase; color: var(--muted);
}
canvas.viz { display: block; width: 100%; }

@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after { animation-duration: .001s !important; transition-duration: .001s !important; }
    [data-reveal] { opacity: 1; transform: none; }
}
"""

BASE_JS = """
/* ---------- self-sizing: trim the iframe to its real content height ----------
   The `height` passed to components.html is a fallback for the moment before
   this runs (and for the case where the host ignores the message). */
(function () {
    let last = 0;
    const send = () => {
        const h = Math.ceil(document.body.scrollHeight);
        if (Math.abs(h - last) < 2) return;
        last = h;
        try {
            window.parent.postMessage(
                { type: 'streamlit:setFrameHeight', height: h }, '*'
            );
        } catch (e) { /* different host, keep the fallback height */ }
    };
    if ('ResizeObserver' in window) new ResizeObserver(send).observe(document.body);
    addEventListener('load', send);
    setTimeout(send, 60);
    send();
})();

/* ---------- ambient background: drifting orbs + particle field ---------- */
(function () {
    const cv = document.getElementById('bgCanvas');
    if (!cv) return;
    const ctx = cv.getContext('2d');
    const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
    let W = 0, H = 0, dpr = Math.min(window.devicePixelRatio || 1, 2);

    const ORBS = [
        { x: .18, y: .16, r: .34, c: [139, 92, 246], s: .00013, p: 0 },
        { x: .84, y: .22, r: .30, c: [243, 166, 74], s: .00017, p: 2.1 },
        { x: .62, y: .86, r: .32, c: [34, 211, 238], s: .00011, p: 4.2 }
    ];

    let dots = [];
    function build() {
        const n = Math.round(Math.min(90, (W * H) / 22000));
        dots = Array.from({ length: n }, () => ({
            x: Math.random(), y: Math.random(),
            z: 0.35 + Math.random() * 0.65,
            vx: (Math.random() - .5) * 0.00013,
            vy: (Math.random() - .5) * 0.00013
        }));
    }

    function size() {
        W = cv.clientWidth; H = cv.clientHeight;
        cv.width = W * dpr; cv.height = H * dpr;
        ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
        build();
    }

    function frame(t) {
        ctx.clearRect(0, 0, W, H);
        ctx.globalCompositeOperation = 'lighter';
        for (const o of ORBS) {
            const dx = Math.sin(t * o.s + o.p) * 0.075;
            const dy = Math.cos(t * o.s * 1.3 + o.p) * 0.055;
            const cx = (o.x + dx) * W, cy = (o.y + dy) * H, r = o.r * Math.max(W, H);
            const g = ctx.createRadialGradient(cx, cy, 0, cx, cy, r);
            g.addColorStop(0, `rgba(${o.c[0]},${o.c[1]},${o.c[2]},0.16)`);
            g.addColorStop(1, `rgba(${o.c[0]},${o.c[1]},${o.c[2]},0)`);
            ctx.fillStyle = g;
            ctx.beginPath(); ctx.arc(cx, cy, r, 0, Math.PI * 2); ctx.fill();
        }
        ctx.globalCompositeOperation = 'source-over';
        for (const d of dots) {
            d.x += d.vx; d.y += d.vy;
            if (d.x < 0) d.x += 1; if (d.x > 1) d.x -= 1;
            if (d.y < 0) d.y += 1; if (d.y > 1) d.y -= 1;
            ctx.fillStyle = `rgba(255,255,255,${0.05 + d.z * 0.16})`;
            ctx.beginPath();
            ctx.arc(d.x * W, d.y * H, d.z * 1.35, 0, Math.PI * 2);
            ctx.fill();
        }
        if (!reduce) requestAnimationFrame(frame);
    }

    addEventListener('resize', size);
    size();
    if (reduce) { frame(0); } else { requestAnimationFrame(frame); }
})();

/* ---------- 3D tilt with specular tracking ---------- */
(function () {
    if (matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    if (matchMedia('(hover: none)').matches) return;

    document.querySelectorAll('[data-tilt]').forEach(el => {
        const max = parseFloat(el.dataset.tilt) || 7;
        let raf = null;

        el.addEventListener('mousemove', e => {
            const r = el.getBoundingClientRect();
            const px = (e.clientX - r.left) / r.width;
            const py = (e.clientY - r.top) / r.height;
            el.style.setProperty('--mx', (px * 100) + '%');
            el.style.setProperty('--my', (py * 100) + '%');
            if (raf) return;
            raf = requestAnimationFrame(() => {
                el.style.transform =
                    `perspective(1100px) rotateX(${(0.5 - py) * max}deg) ` +
                    `rotateY(${(px - 0.5) * max}deg) translate3d(0,-6px,26px)`;
                el.style.transition = 'transform .12s ease-out, box-shadow .5s ease, border-color .5s ease';
                raf = null;
            });
        });

        el.addEventListener('mouseleave', () => {
            el.style.transition = 'transform .75s cubic-bezier(.2,.9,.25,1), box-shadow .5s ease, border-color .5s ease';
            el.style.transform = '';
        });
    });
})();

/* ---------- scroll reveal ---------- */
(function () {
    const items = document.querySelectorAll('[data-reveal]');
    if (!items.length) return;

    const show = el => {
        const d = parseInt(el.dataset.reveal || '0', 10);
        setTimeout(() => el.classList.add('in'), d);
    };

    if (!('IntersectionObserver' in window)) { items.forEach(show); return; }

    // The implicit root here is the *top-level* viewport, not the iframe's own
    // box, and cross-document intersection updates can lag a fast scroll. A low
    // threshold plus a generous bottom margin starts the reveal before the card
    // reaches the fold, so the animation is never caught half-finished.
    const io = new IntersectionObserver((entries) => {
        entries.forEach(en => {
            if (en.isIntersecting) { show(en.target); io.unobserve(en.target); }
        });
    }, { threshold: 0.01, rootMargin: '0px 0px 180px 0px' });

    items.forEach(el => io.observe(el));
})();

/* ---------- animated counters ---------- */
(function () {
    const nodes = document.querySelectorAll('[data-count]');
    if (!nodes.length) return;

    const fmt = (v, dec, pre, suf) =>
        pre + v.toLocaleString(undefined, {
            minimumFractionDigits: dec, maximumFractionDigits: dec
        }) + suf;

    const run = el => {
        const end = parseFloat(el.dataset.count);
        const dec = parseInt(el.dataset.decimals || '0', 10);
        const pre = el.dataset.prefix || '';
        const suf = el.dataset.suffix || '';
        const dur = 1400;
        const t0 = performance.now();
        const tick = now => {
            const p = Math.min((now - t0) / dur, 1);
            const e = 1 - Math.pow(1 - p, 4);
            el.textContent = fmt(end * e, dec, pre, suf);
            if (p < 1) requestAnimationFrame(tick);
        };
        requestAnimationFrame(tick);
    };

    if (!('IntersectionObserver' in window)) { nodes.forEach(run); return; }
    const io = new IntersectionObserver(es => {
        es.forEach(en => { if (en.isIntersecting) { run(en.target); io.unobserve(en.target); } });
    }, { threshold: 0.01, rootMargin: '0px 0px 150px 0px' });
    nodes.forEach(n => io.observe(n));
})();

/* ---------- spark bars ---------- */
(function () {
    const bars = document.querySelectorAll('.kpi-spark i');
    if (!bars.length) return;
    const io = new IntersectionObserver(es => {
        es.forEach(en => {
            if (en.isIntersecting) {
                en.target.style.width = (en.target.dataset.w || '50') + '%';
                io.unobserve(en.target);
            }
        });
    }, { threshold: 0.01, rootMargin: '0px 0px 150px 0px' });
    bars.forEach(b => io.observe(b));
})();
"""


def render(body, height, css="", js="", scrolling=True):
    """Render one page inside its own iframe document.

    `height` is tuned to the content at desktop width. `scrolling=True` is the
    safety net: below the 900px breakpoint the grids stack and the content grows
    past that height, and an internal scrollbar is better than silently clipping
    the bottom of the page. At desktop width nothing overflows, so no scrollbar
    appears.
    """
    palette = {
        "colors": SEGMENT_COLORS,
        "glow": SEGMENT_GLOW,
    }

    doc = f"""
<!DOCTYPE html>
<html><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="{FONTS}" rel="stylesheet">
<style>{BASE_CSS}
{css}</style>
</head>
<body>
<div class="bg-layer bg-mesh"></div>
<canvas id="bgCanvas"></canvas>
<div class="bg-layer bg-grid"></div>
<div class="stage">
{body}
</div>
<script>const PALETTE = {json.dumps(palette)};</script>
<script>{BASE_JS}
{js}</script>
</body></html>
"""
    components.html(doc, height=height, scrolling=scrolling)
