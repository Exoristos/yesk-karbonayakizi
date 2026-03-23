"""Plotly şekillerinde Streamlit açık/koyu temaya göre eksen ve yazı rengi ayarı."""

from __future__ import annotations

from typing import Any

import streamlit as st


def streamlit_theme_is_dark() -> bool:
    """Streamlit tema tabanı koyu mu (yoksa False)."""
    try:
        return st.get_option("theme.base") == "dark"
    except Exception:
        return False


def apply_axis_theme(fig: Any, *, dark: bool) -> None:
    """Koyu temada eksen ve grid renklerini okunaklı yap."""
    if not dark:
        return
    fg = "#e6e6e6"
    grid = "rgba(255,255,255,0.12)"
    fig.update_layout(font_color=fg, title_font_color=fg, legend_font_color=fg)
    fig.update_xaxes(
        gridcolor=grid,
        zerolinecolor=grid,
        color=fg,
        title_font_color=fg,
    )
    fig.update_yaxes(
        gridcolor=grid,
        zerolinecolor=grid,
        color=fg,
        title_font_color=fg,
    )
    upd_polars = getattr(fig, "update_polars", None)
    if callable(upd_polars):
        try:
            upd_polars(
                bgcolor="rgba(0,0,0,0)",
                radialaxis=dict(gridcolor=grid, linecolor=grid, color=fg),
                angularaxis=dict(gridcolor=grid, linecolor=grid, color=fg),
            )
        except Exception:
            pass
