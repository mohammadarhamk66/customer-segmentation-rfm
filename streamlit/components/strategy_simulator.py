"""Business Strategy Simulator.

Ported from the original `animated_business_insights` implementation into the
glass design system. The strategies, impact ranges, actions and outcome copy are
kept verbatim — only the presentation changed. Colours are remapped from the old
light-theme palette to the dark-theme segment colours in `constants.py`.
"""

import json

from utils.constants import SEGMENT_COLORS, SEGMENT_GLOW

STRATEGIES = {
    "retain": {
        "color": SEGMENT_COLORS["High-Value Loyal Customers"],
        "glow": SEGMENT_GLOW["High-Value Loyal Customers"],
        "tab": "Retain",
        "label": "Retention Priority",
        "name": "Retain High-Value Loyal Customers",
        "objective": (
            "Protect the customer group generating the majority of revenue by "
            "strengthening loyalty and reducing churn risk."
        ),
        "impactLabels": ["Revenue Stability", "Customer Lifetime Value", "Churn Risk"],
        "impacts": ["+10–15%", "+8–12%", "-10–15%"],
        "table": [
            ["Revenue Stability", "+10–15%",
             "Protects the largest revenue-driving segment from decline."],
            ["Customer Lifetime Value", "+8–12%",
             "Encourages continued spending from the most valuable customers."],
            ["Churn Risk", "-10–15%",
             "Reduces the chance of losing the business-critical group."],
        ],
        "actions": [
            "Offer loyalty rewards and exclusive benefits.",
            "Provide early access to new products.",
            "Use personalized recommendations.",
            "Monitor signs of reduced purchase activity.",
        ],
        "outcome": (
            "Success means the business protects its highest-value customers, keeps "
            "revenue stable, and reduces dependence on acquiring replacement customers."
        ),
    },
    "grow": {
        "color": SEGMENT_COLORS["Mid-Value Regular Customers"],
        "glow": SEGMENT_GLOW["Mid-Value Regular Customers"],
        "tab": "Grow",
        "label": "Growth Opportunity",
        "name": "Grow Mid-Value Regular Customers",
        "objective": (
            "Increase revenue from customers who already purchase regularly but have "
            "not yet reached high-value behavior."
        ),
        "impactLabels": ["Basket Size", "Revenue Share", "Repeat Purchase"],
        "impacts": ["+8–12%", "+6–10%", "+5–8%"],
        "table": [
            ["Basket Size", "+8–12%",
             "Bundles and cross-sell offers can increase average spend."],
            ["Revenue Share", "+6–10%",
             "Mid-value customers can contribute more without requiring new acquisition."],
            ["Repeat Purchase", "+5–8%",
             "Regular buyers become more consistent and higher value."],
        ],
        "actions": [
            "Promote product bundles.",
            "Use cross-sell campaigns.",
            "Encourage larger basket sizes.",
            "Send targeted upgrade offers.",
        ],
        "outcome": (
            "Success means more mid-value customers move toward high-value behavior "
            "through larger purchases and stronger repeat activity."
        ),
    },
    "convert": {
        "color": SEGMENT_COLORS["Recent Occasional Customers"],
        "glow": SEGMENT_GLOW["Recent Occasional Customers"],
        "tab": "Convert",
        "label": "Conversion Strategy",
        "name": "Convert Recent Occasional Customers",
        "objective": (
            "Turn recently active customers into repeat buyers before they become "
            "inactive."
        ),
        "impactLabels": ["Repeat Purchase", "Customer Activation", "Dormancy Risk"],
        "impacts": ["+12–18%", "+10–15%", "-8–12%"],
        "table": [
            ["Repeat Purchase", "+12–18%",
             "Second-purchase incentives can convert active customers into repeat buyers."],
            ["Customer Activation", "+10–15%",
             "Onboarding and recommendations can increase engagement."],
            ["Dormancy Risk", "-8–12%",
             "Timely follow-up reduces the chance of customers becoming inactive."],
        ],
        "actions": [
            "Send second-purchase incentives.",
            "Recommend related products.",
            "Use welcome campaigns.",
            "Create onboarding journeys.",
        ],
        "outcome": (
            "Success means recent customers build stronger buying habits and begin "
            "moving toward regular customer behavior."
        ),
    },
    "reengage": {
        "color": SEGMENT_COLORS["Inactive Low-Value Customers"],
        "glow": SEGMENT_GLOW["Inactive Low-Value Customers"],
        "tab": "Re-engage",
        "label": "Cost-Control Strategy",
        "name": "Re-engage Inactive Low-Value Customers",
        "objective": (
            "Reactivate customers cautiously while avoiding excessive marketing spend "
            "on low-return groups."
        ),
        "impactLabels": ["Recovery Rate", "Marketing Cost", "Campaign Efficiency"],
        "impacts": ["+3–6%", "-15–25%", "+8–12%"],
        "table": [
            ["Recovery Rate", "+3–6%",
             "A small share of inactive customers may return through low-cost campaigns."],
            ["Marketing Cost", "-15–25%",
             "Automation reduces spend on low-return customers."],
            ["Campaign Efficiency", "+8–12%",
             "Suppressing unresponsive users improves campaign quality."],
        ],
        "actions": [
            "Use low-cost automated campaigns.",
            "Test limited-time offers.",
            "Suppress customers who remain unresponsive.",
            "Avoid expensive personalized campaigns.",
        ],
        "outcome": (
            "Success means the business recovers some inactive customers while "
            "preventing unnecessary spend on low-value, low-response segments."
        ),
    },
}

SIM_CSS = """
.sim-tabs {
    display: grid; grid-template-columns: repeat(4, minmax(0,1fr));
    gap: 10px; margin-bottom: 26px;
}
@media (max-width: 760px) { .sim-tabs { grid-template-columns: repeat(2, 1fr); } }

.sim-tab {
    position: relative; cursor: pointer; user-select: none;
    padding: 15px 16px; border-radius: 17px;
    background: rgba(255,255,255,.035);
    border: 1px solid rgba(255,255,255,.10);
    transition: transform .35s cubic-bezier(.2,.8,.25,1), background .35s ease,
                border-color .35s ease, box-shadow .35s ease;
    text-align: left;
}
.sim-tab:hover {
    transform: translateY(-4px) translateZ(0);
    background: rgba(255,255,255,.07);
    box-shadow: 0 16px 34px rgba(0,0,0,.36);
}
.sim-tab .t-name {
    font-family: 'Sora','Inter',sans-serif; font-size: 15px;
    font-weight: 700; color: #FFFFFF; margin-bottom: 5px;
}
.sim-tab .t-label {
    font-size: 10.5px; letter-spacing: .12em; text-transform: uppercase;
    color: #64748B; font-weight: 800;
}
.sim-tab .t-bar {
    position: absolute; left: 16px; right: 16px; bottom: 9px; height: 3px;
    border-radius: 999px; background: currentColor; opacity: 0;
    transform: scaleX(.3); transform-origin: left;
    transition: opacity .35s ease, transform .45s cubic-bezier(.2,.8,.25,1);
}
.sim-tab.active .t-bar { opacity: 1; transform: scaleX(1); }

.sim-panel { transition: opacity .4s ease, transform .4s cubic-bezier(.2,.8,.25,1); }
.sim-panel.swap { opacity: 0; transform: translate3d(0, 14px, -30px); }

.sim-objective { font-size: 15px; line-height: 1.7; color: #CBD5E1; margin: 0 0 4px 0; }

.impact-grid { display: grid; grid-template-columns: repeat(3, minmax(0,1fr)); gap: 16px; }
@media (max-width: 760px) { .impact-grid { grid-template-columns: 1fr; } }

.impact-tile {
    padding: 20px 22px; border-radius: 19px;
    background: rgba(255,255,255,.04);
    border: 1px solid rgba(255,255,255,.10);
    transition: transform .4s cubic-bezier(.2,.8,.25,1), border-color .4s ease;
}
.impact-tile:hover { transform: translateY(-5px) translateZ(0); }
.impact-tile .i-label {
    font-size: 10px; letter-spacing: .14em; text-transform: uppercase;
    color: #8B9AB4; font-weight: 800; margin-bottom: 12px;
}
.impact-tile .i-value {
    font-family: 'Sora','Inter',sans-serif; font-size: 27px;
    font-weight: 800; letter-spacing: -.03em; line-height: 1;
}

.sim-note {
    margin-top: 22px; font-size: 12.5px; line-height: 1.6; color: #64748B;
    padding-top: 18px; border-top: 1px solid rgba(255,255,255,.07);
}
"""


def sim_js():
    payload = json.dumps(STRATEGIES)
    return """
(function () {
    const S = %s;
    const order = ['retain', 'grow', 'convert', 'reengage'];
    const tabs = document.querySelectorAll('.sim-tab');
    const panel = document.getElementById('simPanel');
    if (!panel || !tabs.length) return;

    const esc = t => String(t).replace(/[&<>]/g, c =>
        ({ '&': '&amp;', '<': '&lt;', '>': '&gt;' }[c]));

    function render(key) {
        const s = S[key];
        panel.innerHTML = `
          <div class="kpi-label" style="color:${s.color}">${esc(s.label)}</div>
          <h3 class="card-title" style="font-size:22px;margin-top:8px">${esc(s.name)}</h3>
          <p class="sim-objective">${esc(s.objective)}</p>

          <div class="impact-grid" style="margin-top:26px">
            ${s.impacts.map((v, i) => `
              <div class="impact-tile">
                <div class="i-label">${esc(s.impactLabels[i])}</div>
                <div class="i-value" style="color:${s.color}">${esc(v)}</div>
              </div>`).join('')}
          </div>

          <div class="row row-12 mt-32" style="gap:20px">
            <div>
              <h3 class="card-title">Estimated commercial impact</h3>
              <table class="data" style="margin-top:14px">
                <thead><tr><th>Measure</th><th style="text-align:right">Change</th>
                  <th>Why</th></tr></thead>
                <tbody>
                  ${s.table.map(r => `
                    <tr>
                      <td style="color:#FFF;font-weight:600">${esc(r[0])}</td>
                      <td class="num" style="color:${s.color}">${esc(r[1])}</td>
                      <td>${esc(r[2])}</td>
                    </tr>`).join('')}
                </tbody>
              </table>
            </div>
            <div>
              <h3 class="card-title">Recommended actions</h3>
              <ul class="ticks" style="margin-top:8px">
                ${s.actions.map(a => `<li>${esc(a)}</li>`).join('')}
              </ul>
            </div>
          </div>

          <div class="glass pad mt-32" style="background:linear-gradient(120deg,${s.color}1c,rgba(139,92,246,.07))">
            <div class="kpi-label">What success looks like</div>
            <p class="body" style="margin-top:10px;color:#CBD5E1">${esc(s.outcome)}</p>
          </div>

          <div class="sim-note">
            Impact ranges are directional planning estimates based on the segment
            behaviour observed in this dataset. They are intended to compare strategies
            against one another, not to forecast a specific financial outcome.
          </div>`;
    }

    function select(key) {
        tabs.forEach(t => t.classList.toggle('active', t.dataset.key === key));
        panel.classList.add('swap');
        setTimeout(() => { render(key); panel.classList.remove('swap'); }, 200);
    }

    tabs.forEach(t => {
        t.addEventListener('click', () => select(t.dataset.key));
        t.addEventListener('keydown', e => {
            if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); select(t.dataset.key); }
        });
    });

    render(order[0]);
    tabs[0].classList.add('active');
})();
""" % payload


def render_simulator():
    """Markup for the simulator. Behaviour ships in `sim_js()`."""
    tabs = "".join(f"""
<div class="sim-tab" data-key="{key}" tabindex="0" role="button"
     style="color:{s['color']}">
  <div class="t-name">{s['tab']}</div>
  <div class="t-label">{s['label']}</div>
  <span class="t-bar"></span>
</div>""" for key, s in STRATEGIES.items())

    return f"""
<div class="glass pad-lg mt-20" data-reveal="0">
  <div class="kpi-label">Business scenario</div>
  <h3 class="card-title" style="font-size:20px;margin-top:10px">
    Marketing resources are limited, but every customer segment presents a
    different opportunity.
  </h3>
  <p class="body" style="margin-top:12px;max-width:74ch">
    High-value loyal customers generate the strongest revenue contribution.
    Mid-value regular customers show growth potential. Recent occasional customers
    may be converted into repeat buyers, while inactive low-value customers require
    careful cost control. <strong>Based on these customer behaviours, which strategy
    should the business prioritise?</strong>
  </p>
</div>

<div class="mt-32" data-reveal="0">
  <div class="kpi-label" style="margin-bottom:14px">Select a strategy</div>
  <div class="sim-tabs">{tabs}</div>
  <div class="glass pad-lg">
    <div class="sim-panel" id="simPanel"></div>
  </div>
</div>"""
