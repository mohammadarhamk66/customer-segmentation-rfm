import plotly.express as px
import plotly.graph_objects as go

from utils.constants import SEGMENT_COLORS

# Revenue Distribution & Customer Distribution
def revenue_share_chart(cluster_profile):
    data = cluster_profile.sort_values(
        "Revenue_Share_%",
        ascending=True
    ).copy()

    fig = go.Figure()

    for _, row in data.iterrows():

        segment = row["Segment"]
        value = row["Revenue_Share_%"]

        # Lollipop line
        fig.add_trace(
            go.Scatter(
                x=[0, value],
                y=[segment, segment],
                mode="lines",
                line=dict(
                    color=SEGMENT_COLORS[segment],
                    width=8,
                ),
                showlegend=False,
                hoverinfo="skip",
            )
        )

        # Marker + value
        fig.add_trace(
            go.Scatter(
                x=[value],
                y=[segment],
                mode="markers+text",
                marker=dict(
                    color=SEGMENT_COLORS[segment],
                    size=18,
                    line=dict(
                        color="#FFFFFF",
                        width=2,
                    ),
                ),
                text=[f"{value:.2f}%"],
                textposition="middle right",
                cliponaxis=False,
                textfont=dict(
                    family="Inter",
                    size=12,
                    color="#111827",
                ),
                showlegend=False,
                hovertemplate="<b>%{y}</b><br>Revenue Share: %{x:.2f}%<extra></extra>",
            )
        )

    fig.update_layout(
        title=dict(
            text="Revenue Distribution",
            font=dict(
                family="Inter",
                size=17,
            ),
            x=0.02,
        ),
        xaxis_title="Revenue Share (%)",
        yaxis_title="",
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#FFFFFF",
        font=dict(
            family="Inter",
            color="#111827",
        ),
        margin=dict(
            l=185,
            r=110,
            t=60,
            b=45,
        ),
        height=420,
        transition=dict(
            duration=700,
            easing="cubic-in-out",
        ),
    )

    fig.update_xaxes(
        gridcolor="#E5E7EB",
        zeroline=False,
        title_font=dict(
            size=12,
            color="#6B7280",
        ),
        tickfont=dict(
            size=11,
            color="#6B7280",
        ),
    )

    fig.update_yaxes(
        automargin=True,
        tickfont=dict(
            size=11,
            color="#6B7280",
        ),
    )

    return fig

def customer_share_chart(cluster_profile):
    fig = go.Figure(
        data=[
            go.Pie(
                labels=cluster_profile["Segment"],
                values=cluster_profile["Customer_Share_%"],
                hole=0.58,
                marker=dict(
                    colors=[SEGMENT_COLORS[s] for s in cluster_profile["Segment"]],
                    line=dict(color="#FFFFFF", width=3),
                ),
                textinfo="percent",
                textposition="inside",
                hovertemplate="<b>%{label}</b><br>Customer Share: %{value:.2f}%<extra></extra>",
            )
        ]
    )

    fig.update_layout(
        title=dict(
            text="Customer Distribution",
            font=dict(size=16, family="Inter"),
            x=0.02,
        ),
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#FFFFFF",
        font=dict(family="Inter", color="#111827"),
        margin=dict(l=20, r=20, t=55, b=70),
        height=420,
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.08,
            xanchor="center",
            x=0.5,
            title="",
            font=dict(size=10),
            itemwidth=30,
        ),
        transition=dict(duration=700, easing="cubic-in-out"),
    )

    return fig

# RFM Distribution Charts
def recency_distribution_chart(rfm, selected_segment):
    data = rfm[rfm["Segment"] == selected_segment]

    fig = px.histogram(
        data,
        x="Recency",
        nbins=30,
        color_discrete_sequence=["#166534"],
    )

    fig.update_layout(
        title=dict(text="Recency Distribution", font=dict(size=16, family="Inter"), x=0),
        xaxis_title="Recency (Days)",
        yaxis_title="Customer Count",
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#FFFFFF",
        font=dict(family="Inter", color="#111827"),
        margin=dict(l=30, r=20, t=50, b=40),
        bargap=0.08,
        showlegend=False,
        transition=dict(duration=700, easing="cubic-in-out"),
    )

    fig.update_yaxes(gridcolor="#E5E7EB")

    return fig


def frequency_distribution_chart(rfm, selected_segment):
    data = rfm[rfm["Segment"] == selected_segment]

    fig = px.histogram(
        data,
        x="Frequency",
        nbins=30,
        color_discrete_sequence=["#2563EB"],
    )

    fig.update_layout(
        title=dict(text="Frequency Distribution", font=dict(size=16, family="Inter"), x=0),
        xaxis_title="Purchase Frequency",
        yaxis_title="Customer Count",
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#FFFFFF",
        font=dict(family="Inter", color="#111827"),
        margin=dict(l=30, r=20, t=50, b=40),
        bargap=0.08,
        showlegend=False,
        transition=dict(duration=700, easing="cubic-in-out"),
    )

    fig.update_yaxes(gridcolor="#E5E7EB")

    return fig


def monetary_distribution_chart(rfm, selected_segment):
    data = rfm[rfm["Segment"] == selected_segment]

    fig = px.histogram(
        data,
        x="Monetary",
        nbins=30,
        color_discrete_sequence=["#C97A28"],
    )

    fig.update_layout(
        title=dict(text="Monetary Distribution", font=dict(size=16, family="Inter"), x=0),
        xaxis_title="Monetary Value (£)",
        yaxis_title="Customer Count",
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#FFFFFF",
        font=dict(family="Inter", color="#111827"),
        margin=dict(l=30, r=20, t=50, b=40),
        bargap=0.08,
        showlegend=False,
        transition=dict(duration=700, easing="cubic-in-out"),
    )

    fig.update_yaxes(gridcolor="#E5E7EB")

    return fig

def frequency_monetary_scatter(rfm, selected_segments):
    """
    Create scatter plot showing Frequency vs Monetary Value
    for the selected customer segments.
    """

    data = rfm[rfm["Segment"].isin(selected_segments)]

    fig = px.scatter(
        data,
        x="Frequency",
        y="Monetary",
        color="Segment",
        color_discrete_map=SEGMENT_COLORS,
        hover_data=[
            "CustomerID",
            "Recency",
            "Frequency",
            "Monetary",
        ],
    )

    fig.update_layout(
        title=dict(
            text="Customer Behaviour Comparison",
            font=dict(size=16, family="Inter"),
            x=0,
        ),
        xaxis_title="Purchase Frequency",
        yaxis_title="Monetary Value (£)",
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#FFFFFF",
        font=dict(family="Inter", color="#111827"),
        margin=dict(l=30, r=20, t=50, b=40),
        transition=dict(duration=700, easing="cubic-in-out"),
        legend=dict(
            title="",
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0,
        ),
    )

    fig.update_xaxes(gridcolor="#E5E7EB")
    fig.update_yaxes(gridcolor="#E5E7EB", type="log")

    return fig