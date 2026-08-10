import json

import streamlit as st

from components import viz
from components.layout import inset
from components.shell import render
from utils import ai_tools
from utils.constants import CLAUDE_MODEL

MAX_TOOL_ROUNDS = 6

STARTERS = [
    "Which segment should we prioritise next quarter, and why?",
    "How many customers spent more than £5,000, and what share of revenue is that?",
    "What would it be worth to move 10% of Recent Occasional customers up a tier?",
    "Show me the lapsed high-value customers we're at risk of losing.",
]


# --------------------------------------------------------------------------- #
# client
# --------------------------------------------------------------------------- #

def _get_api_key():
    try:
        key = st.secrets.get("ANTHROPIC_API_KEY", "")
    except Exception:
        key = ""
    if not key:
        import os
        key = os.environ.get("ANTHROPIC_API_KEY", "")
    return key


@st.cache_resource(show_spinner=False)
def _get_client(api_key):
    import anthropic
    return anthropic.Anthropic(api_key=api_key)


# --------------------------------------------------------------------------- #
# the agentic loop
# --------------------------------------------------------------------------- #

def _stream_turn(client, system, messages, placeholder, tool_log):
    """One request. Streams text into `placeholder`; returns the final message."""
    buffer = {"text": ""}

    def on_delta(chunk):
        buffer["text"] += chunk
        placeholder.markdown(buffer["text"] + " ▌")

    kwargs = dict(
        model=CLAUDE_MODEL,
        max_tokens=8000,
        system=[{
            "type": "text",
            "text": system,
            "cache_control": {"type": "ephemeral"},
        }],
        tools=ai_tools.TOOLS,
        messages=messages,
        thinking={"type": "adaptive"},
        output_config={"effort": "medium"},
    )

    with client.messages.stream(**kwargs) as stream:
        for chunk in stream.text_stream:
            on_delta(chunk)
        response = stream.get_final_message()

    placeholder.markdown(buffer["text"] or "")
    return response, buffer["text"]


def _run_analyst(client, system, messages, placeholder, rfm, cluster_profile):
    """Drive the tool-use loop until Claude stops calling tools."""
    tool_log = []
    answer = ""

    for _ in range(MAX_TOOL_ROUNDS):
        response, text = _stream_turn(client, system, messages, placeholder, tool_log)
        answer = text or answer

        if response.stop_reason == "refusal":
            return ("I wasn't able to answer that one. Try rephrasing it as a question "
                    "about the customer data."), tool_log

        messages.append({"role": "assistant", "content": response.content})

        if response.stop_reason != "tool_use":
            return answer, tool_log

        results = []
        for block in response.content:
            if block.type != "tool_use":
                continue
            payload, is_error = ai_tools.execute(
                block.name, block.input or {}, rfm, cluster_profile
            )
            tool_log.append({"tool": block.name, "input": block.input, "output": payload})
            results.append({
                "type": "tool_result",
                "tool_use_id": block.id,
                "content": payload,
                "is_error": is_error,
            })

        messages.append({"role": "user", "content": results})
        placeholder.markdown(
            (answer + "\n\n" if answer else "") + "_Querying the dataset…_"
        )

    return (answer or "I ran out of query steps before reaching an answer. "
                      "Try narrowing the question."), tool_log


# --------------------------------------------------------------------------- #
# offline fallback — keeps the deployed app usable without a key
# --------------------------------------------------------------------------- #

def _offline_answer(question, rfm, cluster_profile):
    overview = ai_tools._segment_overview(rfm, cluster_profile)
    lines = [
        "**Running without an API key**, so I'm answering from the pre-computed "
        "segment profile rather than reasoning over your question.",
        "",
        "| Segment | Customers | Customer share | Revenue share | Avg value |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    for s in overview["segments"]:
        lines.append(
            f"| {s['segment']} | {s['customers']:,} | {s['customer_share_pct']:.1f}% | "
            f"{s['revenue_share_pct']:.1f}% | £{s['avg_monetary_gbp']:,.0f} |"
        )
    lines += [
        "",
        f"Across **{overview['total_customers']:,} customers** and "
        f"**£{overview['total_revenue_gbp']:,.0f}** in value. Add an "
        "`ANTHROPIC_API_KEY` to enable the full analyst.",
    ]
    return "\n".join(lines)


# --------------------------------------------------------------------------- #
# view
# --------------------------------------------------------------------------- #

def show_ai_analyst(rfm, cluster_profile, kpis, sample):
    api_key = _get_api_key()

    hero = f"""
{viz.page_head(
    "AI Analyst",
    'Ask the <span class="grad-amber">dataset</span> anything',
    "Connected live to all 4,338 customers. It filters the data, computes the "
    "statistics and explains the result in commercial terms — every number it "
    "quotes is computed on request, not recalled."
)}
<div class="row row-3 mt-32">
  <div class="glass pad" data-tilt="7" data-reveal="0"><div class="lift">
    <div class="kpi-label">Tool 1</div>
    <h3 class="card-title" style="margin-top:8px">Segment overview</h3>
    <p class="body">Pulls the full profile of all four segments — size, share, revenue
    and average RFM behaviour.</p>
  </div></div>
  <div class="glass pad" data-tilt="7" data-reveal="110"><div class="lift">
    <div class="kpi-label">Tool 2</div>
    <h3 class="card-title" style="margin-top:8px">Customer query</h3>
    <p class="body">Filters the customer table on any combination of recency,
    frequency, spend and segment.</p>
  </div></div>
  <div class="glass pad" data-tilt="7" data-reveal="220"><div class="lift">
    <div class="kpi-label">Tool 3</div>
    <h3 class="card-title" style="margin-top:8px">Statistics</h3>
    <p class="body">Computes medians, percentiles, standard deviations and
    correlations across the RFM fields.</p>
  </div></div>
</div>
"""
    render(hero, height=540, css=viz.VIZ_CSS, js=viz.VIZ_JS)

    if "chat" not in st.session_state:
        st.session_state.chat = []
    if "api_messages" not in st.session_state:
        st.session_state.api_messages = []

    box = inset()
    with box:
        _chat_surface(api_key, rfm, cluster_profile, kpis)


def _chat_surface(api_key, rfm, cluster_profile, kpis):
    if not api_key:
        st.info(
            "No `ANTHROPIC_API_KEY` found — the analyst is running in offline mode. "
            "Add the key to `.streamlit/secrets.toml` locally, or under "
            "**Settings → Secrets** on Streamlit Community Cloud, to enable it."
        )

    # suggested prompts
    pending = None
    if not st.session_state.chat:
        cols = st.columns(2)
        for i, s in enumerate(STARTERS):
            if cols[i % 2].button(s, key=f"starter_{i}", use_container_width=True):
                pending = s

    for msg in st.session_state.chat:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg.get("tools"):
                with st.expander(f"Dataset queries run ({len(msg['tools'])})"):
                    for call in msg["tools"]:
                        st.markdown(f"**`{call['tool']}`**")
                        st.code(json.dumps(call["input"], indent=2), language="json")
                        st.code(call["output"][:1600], language="json")

    typed = st.chat_input("Ask about segments, customers, revenue or what to do next…")
    question = typed or pending

    if not question:
        return

    st.session_state.chat.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        placeholder = st.empty()

        if not api_key:
            answer, tool_log = _offline_answer(question, rfm, cluster_profile), []
            placeholder.markdown(answer)
        else:
            try:
                client = _get_client(api_key)
                system = ai_tools.build_system_prompt(cluster_profile, kpis)
                st.session_state.api_messages.append(
                    {"role": "user", "content": question}
                )
                placeholder.markdown("_Thinking…_")
                answer, tool_log = _run_analyst(
                    client, system, st.session_state.api_messages,
                    placeholder, rfm, cluster_profile,
                )
            except Exception as exc:
                tool_log = []
                answer = (
                    f"The analyst hit an error: `{type(exc).__name__}: {exc}`\n\n"
                    "Check that `ANTHROPIC_API_KEY` is valid and that the `anthropic` "
                    "package is installed."
                )
                placeholder.markdown(answer)

        if tool_log:
            with st.expander(f"Dataset queries run ({len(tool_log)})"):
                for call in tool_log:
                    st.markdown(f"**`{call['tool']}`**")
                    st.code(json.dumps(call["input"], indent=2), language="json")
                    st.code(call["output"][:1600], language="json")

    st.session_state.chat.append(
        {"role": "assistant", "content": answer, "tools": tool_log}
    )

    if pending:
        st.rerun()
