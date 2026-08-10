"""HTML/CSS/JS fragment builders for the glass UI.

Every function returns a string of markup destined for `shell.render`. Anything
that needs animation ships its behaviour in `VIZ_JS`, which pages append to the
shell's base script.
"""

import json

from utils.constants import SEGMENT_COLORS, SEGMENT_GLOW, SEGMENT_SHORT

VIZ_CSS = """
/* ---------- donut ---------- */
.donut-wrap { position: relative; display: grid; place-items: center; padding: 6px 0 2px; }
.donut { transform: rotate(-90deg); overflow: visible; }
.donut circle { fill: none; stroke-linecap: round; transition: stroke-width .35s ease, opacity .35s ease; }
.donut circle.seg { cursor: default; }
.donut-hole {
    position: absolute; text-align: center; pointer-events: none;
    display: flex; flex-direction: column; align-items: center; justify-content: center;
}
.donut-hole .big {
    font-family: 'Sora','Inter',sans-serif; font-size: 32px; font-weight: 800;
    color: #FFFFFF; letter-spacing: -.03em; line-height: 1;
}
.donut-hole .small {
    font-size: 10.5px; letter-spacing: .15em; text-transform: uppercase;
    color: #8B9AB4; font-weight: 800; margin-top: 8px;
}

/* ---------- horizontal bars ---------- */
.hbar { margin-bottom: 20px; }
.hbar:last-child { margin-bottom: 0; }
.hbar-head { display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 9px; }
.hbar-name { font-size: 13.5px; font-weight: 600; color: #E2E8F0; }
.hbar-val {
    font-family: 'Sora','Inter',sans-serif; font-size: 14px; font-weight: 800;
    color: #FFFFFF; font-variant-numeric: tabular-nums;
}
.hbar-track {
    height: 11px; border-radius: 999px; background: rgba(255,255,255,.055);
    overflow: hidden; box-shadow: inset 0 1px 3px rgba(0,0,0,.4);
}
.hbar-fill {
    height: 100%; width: 0; border-radius: 999px;
    transition: width 1.5s cubic-bezier(.2,.85,.25,1);
    position: relative; overflow: hidden;
}
.hbar-fill::after {
    content: ""; position: absolute; inset: 0;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,.42), transparent);
    transform: translateX(-100%);
    animation: shimmer 2.8s ease-in-out infinite;
}
@keyframes shimmer { 0% { transform: translateX(-100%); } 55%,100% { transform: translateX(220%); } }

/* ---------- comparison bars (revenue vs customers) ---------- */
.cmp-row { display: grid; grid-template-columns: 150px 1fr; gap: 16px; align-items: center; margin-bottom: 18px; }
.cmp-row:last-child { margin-bottom: 0; }
.cmp-label { font-size: 12.5px; color: #CBD5E1; font-weight: 600; line-height: 1.35; }
.cmp-bars { display: flex; flex-direction: column; gap: 7px; }
.cmp-line { display: flex; align-items: center; gap: 11px; }
.cmp-tag { font-size: 9.5px; letter-spacing: .12em; text-transform: uppercase; color: #64748B; width: 34px; font-weight: 800; }
.cmp-track { flex: 1; height: 8px; border-radius: 999px; background: rgba(255,255,255,.05); overflow: hidden; }
.cmp-fill { height: 100%; width: 0; border-radius: 999px; transition: width 1.4s cubic-bezier(.2,.85,.25,1); }
.cmp-num { font-size: 12px; font-weight: 700; color: #FFFFFF; width: 52px; text-align: right; font-variant-numeric: tabular-nums; }

/* ---------- 3D scatter ---------- */
.scatter-shell { position: relative; }
.scatter-shell canvas { cursor: grab; touch-action: none; }
.scatter-shell canvas:active { cursor: grabbing; }
.scatter-hint {
    position: absolute; left: 26px; bottom: 18px;
    font-size: 11px; color: #64748B; letter-spacing: .06em;
    display: flex; align-items: center; gap: 7px;
}
.scatter-hint .k {
    padding: 3px 8px; border-radius: 6px; background: rgba(255,255,255,.06);
    border: 1px solid rgba(255,255,255,.12); color: #94A3B8; font-weight: 700; font-size: 10px;
}
.axis-key { position: absolute; right: 26px; bottom: 18px; display: flex; gap: 16px; font-size: 10.5px; color: #64748B; }
.axis-key b { color: #94A3B8; font-weight: 800; letter-spacing: .1em; }

/* ---------- distribution curves ---------- */
.dist-title { font-size: 11px; letter-spacing: .14em; text-transform: uppercase; color: #8B9AB4; font-weight: 800; margin-bottom: 4px; }
.dist-meta { font-size: 12.5px; color: #64748B; margin-bottom: 12px; }
.dist-meta b { color: #FFFFFF; font-weight: 700; }
"""

VIZ_JS = """
/* ---------- bar fills ---------- */
(function () {
    const fills = document.querySelectorAll('.hbar-fill, .cmp-fill');
    if (!fills.length) return;
    const io = new IntersectionObserver(es => {
        es.forEach(en => {
            if (!en.isIntersecting) return;
            const el = en.target;
            setTimeout(() => { el.style.width = el.dataset.w + '%'; },
                       parseInt(el.dataset.delay || '0', 10));
            io.unobserve(el);
        });
    }, { threshold: 0.01, rootMargin: '0px 0px 150px 0px' });
    fills.forEach(f => io.observe(f));
})();

/* ---------- donut arc draw-on ---------- */
(function () {
    const segs = document.querySelectorAll('.donut circle.seg');
    if (!segs.length) return;
    const io = new IntersectionObserver(es => {
        es.forEach(en => {
            if (!en.isIntersecting) return;
            const c = en.target;
            setTimeout(() => { c.style.strokeDashoffset = c.dataset.offset; },
                       parseInt(c.dataset.delay || '0', 10));
            io.unobserve(c);
        });
    }, { threshold: 0.01, rootMargin: '0px 0px 150px 0px' });
    segs.forEach(s => io.observe(s));

    // hover emphasis
    document.querySelectorAll('.donut').forEach(d => {
        const all = d.querySelectorAll('circle.seg');
        all.forEach(c => {
            c.addEventListener('mouseenter', () => {
                all.forEach(o => { if (o !== c) o.style.opacity = '.28'; });
                c.style.strokeWidth = (parseFloat(c.getAttribute('stroke-width')) + 6) + 'px';
                const hole = d.parentElement.querySelector('.donut-hole');
                if (hole) {
                    hole.querySelector('.big').textContent = c.dataset.value;
                    hole.querySelector('.small').textContent = c.dataset.name;
                }
            });
            c.addEventListener('mouseleave', () => {
                all.forEach(o => { o.style.opacity = '1'; o.style.strokeWidth = ''; });
                const hole = d.parentElement.querySelector('.donut-hole');
                if (hole) {
                    hole.querySelector('.big').textContent = hole.dataset.big;
                    hole.querySelector('.small').textContent = hole.dataset.small;
                }
            });
        });
    });
})();

/* ---------- 3D RFM point cloud ---------- */
function mountScatter(canvasId, points, opts) {
    const cv = document.getElementById(canvasId);
    if (!cv) return;
    const ctx = cv.getContext('2d');
    const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    const H = opts.height || 420;
    let W = 0;

    // normalise to a cube centred on the origin (log-scaled: RFM is heavily skewed)
    const lg = v => Math.log10(Math.max(v, 1));
    const ext = k => {
        const vals = points.map(p => lg(p[k]));
        return [Math.min(...vals), Math.max(...vals)];
    };
    const [rMin, rMax] = ext('Recency');
    const [fMin, fMax] = ext('Frequency');
    const [mMin, mMax] = ext('Monetary');
    const nrm = (v, a, b) => ((lg(v) - a) / (b - a || 1) - 0.5) * 2;

    const cloud = points.map(p => ({
        x: nrm(p.Recency, rMin, rMax),
        y: -nrm(p.Monetary, mMin, mMax),
        z: nrm(p.Frequency, fMin, fMax),
        c: PALETTE.colors[p.Segment] || '#94A3B8'
    }));

    // RFM is skewed even after the log transform, so the midrange is not the
    // centre of mass. Recentre on the mean so the cloud sits in the panel.
    const mean = k => cloud.reduce((s, p) => s + p[k], 0) / cloud.length;
    const [mx, my, mz] = [mean('x'), mean('y'), mean('z')];
    cloud.forEach(p => { p.x -= mx; p.y -= my; p.z -= mz; });

    let ry = 0.6, rx = -0.22, spin = 0.0022;
    let drag = false, lx = 0, ly = 0;

    function size() {
        W = cv.clientWidth;
        cv.width = W * dpr; cv.height = H * dpr;
        cv.style.height = H + 'px';
        ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    }

    function project(p) {
        const cy = Math.cos(ry), sy = Math.sin(ry);
        const cx = Math.cos(rx), sx = Math.sin(rx);
        let x = p.x * cy - p.z * sy;
        let z = p.x * sy + p.z * cy;
        let y = p.y * cx - z * sx;
        z = p.y * sx + z * cx;
        const d = 3.4;
        const s = d / (d + z);
        const scale = Math.min(W, H) * 0.34;
        return { sx: W / 2 + x * scale * s, sy: H / 2 + y * scale * s, s, z };
    }

    function grid() {
        const e = [[-1,-1,-1],[1,-1,-1],[1,-1,1],[-1,-1,1]];
        const pr = e.map(v => project({ x: v[0], y: v[1], z: v[2] }));
        ctx.strokeStyle = 'rgba(255,255,255,.08)';
        ctx.lineWidth = 1;
        ctx.beginPath();
        pr.forEach((p, i) => i ? ctx.lineTo(p.sx, p.sy) : ctx.moveTo(p.sx, p.sy));
        ctx.closePath(); ctx.stroke();

        for (let i = 1; i < 4; i++) {
            const t = -1 + (i / 2);
            const a = project({ x: t, y: -1, z: -1 }), b = project({ x: t, y: -1, z: 1 });
            const c = project({ x: -1, y: -1, z: t }), d2 = project({ x: 1, y: -1, z: t });
            ctx.strokeStyle = 'rgba(255,255,255,.045)';
            ctx.beginPath(); ctx.moveTo(a.sx, a.sy); ctx.lineTo(b.sx, b.sy); ctx.stroke();
            ctx.beginPath(); ctx.moveTo(c.sx, c.sy); ctx.lineTo(d2.sx, d2.sy); ctx.stroke();
        }
    }

    function frame() {
        if (!drag) ry += spin;
        ctx.clearRect(0, 0, W, H);
        grid();
        const pts = cloud.map(p => ({ p, q: project(p) })).sort((a, b) => b.q.z - a.q.z);
        for (const { p, q } of pts) {
            const r = Math.max(1.1, 3.1 * q.s);
            const alpha = Math.min(1, Math.max(0.16, (q.s - 0.62) * 2.1));
            ctx.fillStyle = p.c;
            ctx.globalAlpha = alpha;
            ctx.beginPath(); ctx.arc(q.sx, q.sy, r, 0, Math.PI * 2); ctx.fill();
            if (q.s > 1.02) {
                ctx.globalAlpha = alpha * 0.18;
                ctx.beginPath(); ctx.arc(q.sx, q.sy, r * 3.1, 0, Math.PI * 2); ctx.fill();
            }
        }
        ctx.globalAlpha = 1;
        if (!reduce) requestAnimationFrame(frame);
    }

    const down = e => { drag = true; lx = (e.touches ? e.touches[0] : e).clientX; ly = (e.touches ? e.touches[0] : e).clientY; };
    const move = e => {
        if (!drag) return;
        const t = e.touches ? e.touches[0] : e;
        ry += (t.clientX - lx) * 0.0072;
        rx += (t.clientY - ly) * 0.0052;
        rx = Math.max(-1.15, Math.min(0.75, rx));
        lx = t.clientX; ly = t.clientY;
        if (e.cancelable) e.preventDefault();
    };
    const up = () => { drag = false; };

    cv.addEventListener('mousedown', down);
    cv.addEventListener('touchstart', down, { passive: true });
    addEventListener('mousemove', move);
    cv.addEventListener('touchmove', move, { passive: false });
    addEventListener('mouseup', up);
    addEventListener('touchend', up);
    addEventListener('resize', size);

    size();
    if (reduce) { ctx.clearRect(0, 0, W, H); grid(); frame(); } else { requestAnimationFrame(frame); }
}

/* ---------- distribution curve (kernel-ish histogram, drawn as a smooth area) ---------- */
function mountCurve(canvasId, values, color, height) {
    const cv = document.getElementById(canvasId);
    if (!cv) return;
    const ctx = cv.getContext('2d');
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    const H = height || 150;
    let W = 0, progress = 0;

    const BINS = 42;
    const lo = Math.min(...values), hi = Math.max(...values);
    const bins = new Array(BINS).fill(0);
    values.forEach(v => {
        const i = Math.min(BINS - 1, Math.floor(((v - lo) / (hi - lo || 1)) * BINS));
        bins[i] += 1;
    });
    // light smoothing so the silhouette reads as a curve rather than a comb
    const sm = bins.map((_, i) => {
        let s = 0, n = 0;
        for (let k = -2; k <= 2; k++) {
            const j = i + k;
            if (j >= 0 && j < BINS) { const w = 3 - Math.abs(k); s += bins[j] * w; n += w; }
        }
        return s / n;
    });
    const peak = Math.max(...sm) || 1;

    function size() {
        W = cv.clientWidth;
        cv.width = W * dpr; cv.height = H * dpr;
        cv.style.height = H + 'px';
        ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    }

    function draw() {
        ctx.clearRect(0, 0, W, H);
        const pad = 8;
        const n = Math.max(2, Math.round(BINS * progress));
        const pt = i => [pad + (i / (BINS - 1)) * (W - pad * 2), H - 6 - (sm[i] / peak) * (H - 24)];

        ctx.beginPath();
        ctx.moveTo(pad, H - 6);
        for (let i = 0; i < n; i++) {
            const [x, y] = pt(i);
            if (i === 0) { ctx.lineTo(x, y); continue; }
            const [px, py] = pt(i - 1);
            ctx.bezierCurveTo((px + x) / 2, py, (px + x) / 2, y, x, y);
        }
        const lastX = pt(n - 1)[0];
        ctx.lineTo(lastX, H - 6);
        ctx.closePath();

        const g = ctx.createLinearGradient(0, 0, 0, H);
        g.addColorStop(0, color + '66');
        g.addColorStop(1, color + '05');
        ctx.fillStyle = g; ctx.fill();

        ctx.beginPath();
        for (let i = 0; i < n; i++) {
            const [x, y] = pt(i);
            if (i === 0) { ctx.moveTo(x, y); continue; }
            const [px, py] = pt(i - 1);
            ctx.bezierCurveTo((px + x) / 2, py, (px + x) / 2, y, x, y);
        }
        ctx.strokeStyle = color; ctx.lineWidth = 2.4; ctx.lineJoin = 'round';
        ctx.shadowColor = color; ctx.shadowBlur = 14;
        ctx.stroke();
        ctx.shadowBlur = 0;

        if (progress < 1) { progress = Math.min(1, progress + 0.028); requestAnimationFrame(draw); }
    }

    addEventListener('resize', () => { size(); progress = 1; draw(); });
    size();
    const io = new IntersectionObserver(es => {
        es.forEach(en => { if (en.isIntersecting) { draw(); io.unobserve(en.target); } });
    }, { threshold: 0.3 });
    io.observe(cv);
}
"""


# --------------------------------------------------------------------------- #
# fragment builders
# --------------------------------------------------------------------------- #

def kpi(label, value, foot="", decimals=0, prefix="", suffix="",
        spark=60, color="#F3A64A", delay=0, tilt=8):
    """A glass KPI tile with an animated counter."""
    return f"""
<div class="glass pad" data-tilt="{tilt}" data-reveal="{delay}">
  <div class="lift">
    <div class="kpi-label">{label}</div>
    <div class="kpi-value">
      <span data-count="{value}" data-decimals="{decimals}"
            data-prefix="{prefix}" data-suffix="{suffix}">{prefix}0{suffix}</span>
    </div>
    {f'<div class="kpi-foot">{foot}</div>' if foot else ''}
    <div class="kpi-spark">
      <i data-w="{spark}" style="background:linear-gradient(90deg,{color},{color}55)"></i>
    </div>
  </div>
</div>"""


def donut(rows, center_big, center_small, size=248, stroke=26):
    """rows: list of (segment_name, percent). Animated SVG ring."""
    r = (size - stroke) / 2 - 6
    circ = 2 * 3.14159265 * r
    out, acc = [], 0.0

    for i, (name, pct) in enumerate(rows):
        color = SEGMENT_COLORS.get(name, "#94A3B8")
        gap = 1.4  # visual separation between arcs, in percent
        span = max(pct - gap, 0.4)
        dash = circ * span / 100
        offset = -circ * acc / 100
        acc += pct
        out.append(
            f'<circle class="seg" cx="{size/2}" cy="{size/2}" r="{r}" '
            f'stroke="{color}" stroke-width="{stroke}" '
            f'stroke-dasharray="{dash:.2f} {circ - dash:.2f}" '
            f'stroke-dashoffset="{circ:.2f}" data-offset="{offset:.2f}" '
            f'data-delay="{160 + i * 130}" data-name="{SEGMENT_SHORT.get(name, name)}" '
            f'data-value="{pct:.1f}%" '
            f'style="transition:stroke-dashoffset 1.4s cubic-bezier(.2,.85,.25,1),'
            f'opacity .35s ease,stroke-width .35s ease;'
            f'filter:drop-shadow(0 0 10px {color}55)"></circle>'
        )

    return f"""
<div class="donut-wrap">
  <svg class="donut" width="{size}" height="{size}" viewBox="0 0 {size} {size}">
    <circle cx="{size/2}" cy="{size/2}" r="{r}" stroke="rgba(255,255,255,.05)"
            stroke-width="{stroke}"></circle>
    {''.join(out)}
  </svg>
  <div class="donut-hole" data-big="{center_big}" data-small="{center_small}"
       style="width:{size}px;height:{size}px">
    <div class="big">{center_big}</div>
    <div class="small">{center_small}</div>
  </div>
</div>"""


def hbars(rows, value_fmt="{:.1f}%", max_value=None):
    """rows: list of (segment_name, value)."""
    top = max_value or max(v for _, v in rows) or 1
    out = []
    for i, (name, val) in enumerate(rows):
        c = SEGMENT_COLORS.get(name, "#94A3B8")
        g = SEGMENT_GLOW.get(name, "#CBD5E1")
        out.append(f"""
<div class="hbar">
  <div class="hbar-head">
    <span class="hbar-name">{SEGMENT_SHORT.get(name, name)}</span>
    <span class="hbar-val">{value_fmt.format(val)}</span>
  </div>
  <div class="hbar-track">
    <div class="hbar-fill" data-w="{val / top * 100:.1f}" data-delay="{i * 130}"
         style="background:linear-gradient(90deg,{c},{g});box-shadow:0 0 16px {c}66"></div>
  </div>
</div>""")
    return "".join(out)


def compare_bars(rows):
    """rows: list of (segment_name, customer_share, revenue_share)."""
    out = []
    for i, (name, cust, rev) in enumerate(rows):
        c = SEGMENT_COLORS.get(name, "#94A3B8")
        out.append(f"""
<div class="cmp-row">
  <div class="cmp-label">{SEGMENT_SHORT.get(name, name)}</div>
  <div class="cmp-bars">
    <div class="cmp-line">
      <span class="cmp-tag">Cust</span>
      <span class="cmp-track"><span class="cmp-fill" data-w="{cust:.1f}" data-delay="{i*110}"
        style="background:{c}55"></span></span>
      <span class="cmp-num">{cust:.1f}%</span>
    </div>
    <div class="cmp-line">
      <span class="cmp-tag">Rev</span>
      <span class="cmp-track"><span class="cmp-fill" data-w="{rev:.1f}" data-delay="{i*110+90}"
        style="background:linear-gradient(90deg,{c},{SEGMENT_GLOW.get(name,'#fff')});box-shadow:0 0 12px {c}77"></span></span>
      <span class="cmp-num">{rev:.1f}%</span>
    </div>
  </div>
</div>""")
    return "".join(out)


def legend(names):
    out = []
    for n in names:
        c = SEGMENT_COLORS.get(n, "#94A3B8")
        out.append(
            f'<span class="chip"><span class="swatch" '
            f'style="background:{c};box-shadow:0 0 10px {c}"></span>'
            f'{SEGMENT_SHORT.get(n, n)}</span>'
        )
    return f'<div class="chips">{"".join(out)}</div>'


def scatter_3d(points, height=430, canvas_id="rfmCloud"):
    """Rotating, draggable 3D point cloud of real customers."""
    body = f"""
<div class="scatter-shell">
  <canvas class="viz" id="{canvas_id}"></canvas>
  <div class="scatter-hint"><span class="k">drag</span> to rotate the cloud</div>
  <div class="axis-key">
    <span><b>X</b> Recency</span><span><b>Y</b> Monetary</span><span><b>Z</b> Frequency</span>
  </div>
</div>"""
    js = (
        f"mountScatter('{canvas_id}', {json.dumps(points)}, "
        f"{{height:{height}}});"
    )
    return body, js


def curve(canvas_id, title, meta, values, color, height=150):
    body = f"""
<div>
  <div class="dist-title">{title}</div>
  <div class="dist-meta">{meta}</div>
  <canvas class="viz" id="{canvas_id}"></canvas>
</div>"""
    js = f"mountCurve('{canvas_id}', {json.dumps(values)}, '{color}', {height});"
    return body, js


def page_head(eyebrow, title_html, lede):
    return f"""
<div data-reveal="0" style="padding:34px 4px 10px 4px">
  <span class="eyebrow"><span class="dot"></span>{eyebrow}</span>
  <h1 class="display">{title_html}</h1>
  <p class="lede">{lede}</p>
</div>"""


def section(title, sub=""):
    return f"""
<div data-reveal="0" style="margin:44px 4px 0 4px">
  <h2 class="section">{title}</h2>
  {f'<p class="section-sub">{sub}</p>' if sub else ''}
</div>"""
