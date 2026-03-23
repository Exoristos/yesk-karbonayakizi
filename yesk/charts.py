"""Plotly grafik üretimi (``apply_axis_theme`` ile tema uygulanır)."""

from __future__ import annotations

from typing import Mapping

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from yesk.plotly_theme import apply_axis_theme


def build_gauge_figure(
    total_co2: float,
    avg: Mapping[str, float],
    *,
    gauge_title: str,
    theme_dark: bool,
) -> go.Figure:
    """Toplam ayak izi gauge göstergesi."""
    ceiling = max(25.0, total_co2 * 1.4)
    ref_total = float(avg["total"])
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number+delta",
            value=total_co2,
            number={"suffix": " kg", "font": {"size": 36, "color": "#1b5e20"}},
            delta={
                "reference": ref_total,
                "increasing": {"color": "#c62828"},
                "decreasing": {"color": "#2e7d32"},
                "suffix": " kg",
            },
            title={"text": gauge_title, "font": {"size": 17}},
            gauge={
                "axis": {"range": [0, ceiling], "tickwidth": 1},
                "bar": {"color": "#2e7d32", "thickness": 0.22},
                "bgcolor": "rgba(200,200,200,0.1)",
                "borderwidth": 1,
                "bordercolor": "rgba(100,100,100,0.2)",
                "steps": [
                    {"range": [0, ref_total * 0.6], "color": "rgba(165, 214, 167, 0.4)"},
                    {"range": [ref_total * 0.6, ref_total], "color": "rgba(255, 245, 157, 0.4)"},
                    {"range": [ref_total, ceiling], "color": "rgba(239, 154, 154, 0.4)"},
                ],
                "threshold": {
                    "line": {"color": "#b71c1c", "width": 3},
                    "thickness": 0.8,
                    "value": ref_total,
                },
            },
        )
    )
    fig.update_layout(
        height=400,
        margin=dict(l=30, r=30, t=60, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
    )
    apply_axis_theme(fig, dark=theme_dark)
    return fig


def build_treemap_figure(
    df_tree: pd.DataFrame,
    *,
    treemap_title: str,
    theme_dark: bool,
) -> go.Figure:
    """Emisyon treemap."""
    fig = px.treemap(
        df_tree,
        path=["category", "source"],
        values="co2",
        color="co2",
        color_continuous_scale=["#c8e6c9", "#66bb6a", "#2e7d32", "#1b5e20"],
    )
    fig.update_traces(
        textinfo="label+value+percent parent",
        texttemplate="<b>%{label}</b><br>%{value:.3f} kg",
        hovertemplate=(
            "<b>%{label}</b><br>%{value:.3f} kg CO₂<br>%{percentParent:.1%}<extra></extra>"
        ),
    )
    fig.update_layout(
        title=dict(text=treemap_title, font=dict(size=17), x=0.5),
        height=420,
        margin=dict(l=10, r=10, t=55, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        coloraxis_showscale=False,
    )
    apply_axis_theme(fig, dark=theme_dark)
    return fig


def build_radar_figure(
    user_vals: list[float],
    avg_vals: list[float],
    radar_cats: list[str],
    *,
    legend_you: str,
    legend_avg: str,
    radar_title: str,
    theme_dark: bool,
) -> go.Figure:
    """Kullanıcı vs ortalama polar grafik."""
    fig = go.Figure()
    fig.add_trace(
        go.Scatterpolar(
            r=user_vals + [user_vals[0]],
            theta=radar_cats + [radar_cats[0]],
            fill="toself",
            name=legend_you,
            fillcolor="rgba(46,125,50,0.25)",
            line=dict(color="#1b5e20", width=2),
            marker=dict(size=6),
        )
    )
    fig.add_trace(
        go.Scatterpolar(
            r=avg_vals + [avg_vals[0]],
            theta=radar_cats + [radar_cats[0]],
            fill="toself",
            name=legend_avg,
            fillcolor="rgba(189,189,189,0.2)",
            line=dict(color="#9e9e9e", width=2, dash="dot"),
            marker=dict(size=5),
        )
    )
    mx = max(max(user_vals), max(avg_vals), 1e-9) * 1.3
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, mx], gridcolor="#e0e0e0"),
            angularaxis=dict(gridcolor="#e0e0e0"),
        ),
        title=dict(text=radar_title, font=dict(size=17), x=0.5),
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.22, xanchor="center", x=0.5),
        height=400,
        margin=dict(l=60, r=60, t=55, b=40),
        paper_bgcolor="rgba(0,0,0,0)",
    )
    apply_axis_theme(fig, dark=theme_dark)
    return fig


def build_category_bar_figure(
    user_vals: list[float],
    avg_vals: list[float],
    radar_cats: list[str],
    *,
    legend_you: str,
    legend_avg: str,
    bar_title: str,
    xaxis_label: str,
    theme_dark: bool,
) -> go.Figure:
    """Yatay çubuk: kategori karşılaştırması."""
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            name=legend_you,
            y=radar_cats,
            x=user_vals,
            orientation="h",
            marker=dict(color="#2e7d32"),
            text=[f"{v:.2f}" for v in user_vals],
            textposition="auto",
            textfont=dict(color="white", size=13),
        )
    )
    fig.add_trace(
        go.Bar(
            name=legend_avg,
            y=radar_cats,
            x=avg_vals,
            orientation="h",
            marker=dict(color="#bdbdbd"),
            text=[f"{v:.2f}" for v in avg_vals],
            textposition="auto",
            textfont=dict(color="white", size=13),
        )
    )
    fig.update_layout(
        barmode="group",
        title=dict(text=bar_title, font=dict(size=17), x=0.5),
        xaxis_title=xaxis_label,
        yaxis=dict(autorange="reversed"),
        height=400,
        margin=dict(l=20, r=20, t=55, b=40),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(gridcolor="rgba(150,150,150,0.1)"),
        legend=dict(orientation="h", yanchor="bottom", y=-0.22, xanchor="center", x=0.5),
    )
    apply_axis_theme(fig, dark=theme_dark)
    return fig


def build_total_histogram_figure(
    df: pd.DataFrame,
    total_co2: float,
    *,
    xaxis_label: str,
    hist_yaxis: str,
    vline_label: str,
    theme_dark: bool,
) -> go.Figure:
    """Kohort toplam dağılımı + kullanıcı çizgisi."""
    fig = px.histogram(
        df,
        x="total_daily_co2_kg",
        nbins=45,
        color_discrete_sequence=["#66bb6a"],
    )
    fig.update_traces(marker_line_width=0)
    fig.add_vline(
        x=total_co2,
        line_width=3,
        line_color="#b71c1c",
        annotation_text=vline_label,
        annotation_position="top",
    )
    fig.update_layout(
        showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=380,
        xaxis_title=xaxis_label,
        yaxis_title=hist_yaxis,
        margin=dict(l=40, r=20, t=40, b=40),
    )
    apply_axis_theme(fig, dark=theme_dark)
    return fig


def build_category_box_figure(
    df: pd.DataFrame,
    cat_cols: Mapping[str, str],
    *,
    box_title: str,
    y_axis_label: str,
    theme_dark: bool,
) -> go.Figure:
    """Kategori bazlı kutu grafikleri."""
    dm = df[list(cat_cols.keys())].rename(columns=dict(cat_cols)).melt(
        var_name="category", value_name="kg"
    )
    fig = px.box(
        dm,
        x="category",
        y="kg",
        color_discrete_sequence=["#81c784"],
    )
    fig.update_layout(
        title=dict(text=box_title, font=dict(size=17), x=0.5),
        height=420,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        yaxis_title=y_axis_label,
        xaxis_title="",
        showlegend=False,
        margin=dict(l=40, r=20, t=55, b=80),
    )
    fig.update_xaxes(tickangle=-25)
    apply_axis_theme(fig, dark=theme_dark)
    return fig
