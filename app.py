"""
app.py — Carbon Footprint Calculator & Analytics Dashboard (v3)
Green Economy and Sustainability Club | Marmara University (YESK)
"""

from __future__ import annotations

import html
import json
import logging
import os
from pathlib import Path
from urllib.parse import parse_qs

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from streamlit.runtime.scriptrunner_utils.script_run_context import get_script_run_ctx

from yesk.calc import build_treemap_rows, compute_footprint
from yesk.charts import (
    build_category_bar_figure,
    build_category_box_figure,
    build_gauge_figure,
    build_radar_figure,
    build_total_histogram_figure,
    build_treemap_figure,
)
from yesk.data_io import DataLoadError, read_and_validate_cohort_csv, read_and_validate_factors
from yesk.i18n import DROPDOWN_TR, LANG
from yesk.plotly_theme import streamlit_theme_is_dark
from yesk.sidebar import render_inputs
from yesk.stats import cohort_percentile_strictly_higher
from yesk.ui.styles import APP_MAIN_CSS

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

_SIDEBAR_STATE_KEY = "_yesk_sidebar_initial_from_url"
_URL_LANG_KEY = "_yesk_url_lang_hint"
_LANG_RADIO_KEY = "_yesk_lang_radio_value"


def _page_locale_from_url() -> str:
    """Tarayıcı sekmesi başlığı için dil ipucu: ``?lang=tr`` veya ``?lang=en``.

    Streamlit ``set_page_config`` yalnızca ilk çağrıda çalıştığından, sekme başlığı
    URL parametresi (ve bir kez okunup saklanan değer) ile hizalanır. Yan panelden
    dil değiştirmek sekme başlığını güncellemez; paylaşım linklerinde ``?lang=tr``
    kullanılabilir.
    """
    ctx = get_script_run_ctx(suppress_warning=True)

    if ctx is not None and ctx.query_string:
        try:
            qs = ctx.query_string.lstrip("?")
            parsed = parse_qs(qs, keep_blank_values=True)
            vals = parsed.get("lang", [])
            if vals:
                v = (vals[0] or "").strip().lower()
                if v in ("tr", "turkce", "turkish"):
                    st.session_state[_URL_LANG_KEY] = "tr"
                    return "tr"
                if v in ("en", "english"):
                    st.session_state[_URL_LANG_KEY] = "en"
                    return "en"
        except Exception:
            pass

    if _URL_LANG_KEY in st.session_state:
        return str(st.session_state[_URL_LANG_KEY])

    return "en"


def _sidebar_layout_from_url() -> str:
    """URL'de initial_sidebar_state=collapsed ise yan panel kapalı başlar.

    ``st.set_page_config(initial_sidebar_state=...)`` ile aynı isimlendirme.
    Eski bağlantılar için ``sidebar=collapsed`` de kabul edilir.

    Yeniden çalıştırmalarda ``query_string`` çoğu kez boş olduğu için, bir kez
    URL'den okunan değer ``st.session_state`` ile korunur.

    ``st.query_params`` burada kullanılmaz; ``set_page_config`` ilk Streamlit
    çağrısı olmalıdır. Sorgu dizesi ScriptRunContext üzerinden okunur.
    """
    ctx = get_script_run_ctx(suppress_warning=True)

    if ctx is not None and ctx.query_string:
        try:
            qs = ctx.query_string.lstrip("?")
            parsed = parse_qs(qs, keep_blank_values=True)
            for key in ("initial_sidebar_state", "sidebar"):
                vals = parsed.get(key, [])
                if vals and vals[0] == "collapsed":
                    st.session_state[_SIDEBAR_STATE_KEY] = "collapsed"
                    return "collapsed"
        except Exception:
            pass

    if _SIDEBAR_STATE_KEY in st.session_state:
        return st.session_state[_SIDEBAR_STATE_KEY]

    return "expanded"


# ─────────────────────── config ───────────────────────
_locale_for_title = _page_locale_from_url()
st.set_page_config(
    page_title=str(LANG[_locale_for_title]["page_title_browser"]),
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state=_sidebar_layout_from_url(),
)

BASE = os.path.dirname(__file__)


@st.cache_data
def load_factors_cached(project_root: str) -> dict:
    """Faktör JSON (şema doğrulanmış)."""
    return read_and_validate_factors(Path(project_root) / "data" / "complex_factors.json")


@st.cache_data
def load_cohort_cached(project_root: str) -> pd.DataFrame:
    """Kohort CSV (sütun şeması doğrulanmış)."""
    return read_and_validate_cohort_csv(Path(project_root) / "data" / "complex_emissions.csv")


try:
    F = load_factors_cached(BASE)
    df = load_cohort_cached(BASE)
except DataLoadError as exc:
    logger.exception("YESK data load failed: %s", exc)
    st.error(
        "**Data error / Veri hatası**\n\n"
        "Could not load or validate `data/complex_factors.json` or "
        "`data/complex_emissions.csv`.\n\n"
        f"`data/complex_factors.json` veya `data/complex_emissions.csv` "
        f"yüklenemedi veya şema hatalı.\n\n{exc}"
    )
    st.stop()

# ─────────────────────── CSS ───────────────────────
st.markdown(APP_MAIN_CSS, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
# SIDEBAR — dil + yaşam tarzı girdileri
# ═══════════════════════════════════════════════════════════
with st.sidebar:
    if _LANG_RADIO_KEY not in st.session_state:
        st.session_state[_LANG_RADIO_KEY] = (
            "Türkçe" if st.session_state.get(_URL_LANG_KEY) == "tr" else "English"
        )
    lang_choice = st.radio(
        str(LANG["en"]["lang_label"]),
        ["English", "Türkçe"],
        horizontal=True,
        label_visibility="visible",
        key=_LANG_RADIO_KEY,
    )
    lang = "tr" if lang_choice == "Türkçe" else "en"
    T = LANG[lang]

    def tr_opt(key: str) -> str:
        """Türkçe arayüzde faktör anahtarını çeviri etiketine çevirir."""
        return DROPDOWN_TR.get(key, key) if lang == "tr" else key

    vals = render_inputs(F, T, tr_opt)

theme_dark = streamlit_theme_is_dark()

# ═══════════════════════════════════════════════════════════
# CALCULATIONS
# ═══════════════════════════════════════════════════════════
fp = compute_footprint(F, **vals)
transport_co2 = fp.transport_co2
tech_co2 = fp.tech_co2
lifestyle_co2 = fp.lifestyle_co2
fashion_co2 = fp.fashion_co2
diet_co2 = fp.diet_co2
total_co2 = fp.total_co2
avg = F["averages"]

# ═══════════════════════════════════════════════════════════
# PRE-CALCULATIONS FOR GAMIFICATION
# ═══════════════════════════════════════════════════════════
# Kohortta kullanıcıdan yüksek toplam yüzdesi (sentetik veri tanımı).
percentile, pct_reason = cohort_percentile_strictly_higher(
    df["total_daily_co2_kg"], total_co2
)
if pct_reason:
    logger.warning("Percentile unavailable: %s", pct_reason)

if percentile is None:
    badge = T["badge_no_percentile"]
    pct_text = T["percentile_na"]
else:
    if percentile >= 80:
        badge = T["badge_eco_warrior"]
    elif percentile >= 50:
        badge = T["badge_green_citizen"]
    elif percentile >= 20:
        badge = T["badge_average"]
    else:
        badge = T["badge_high_impact"]

    pct_text = (
        T["percentile_wow"].format(percentile)
        if percentile >= 50
        else T["percentile_bad"].format(100 - percentile)
    )

cat_values = {
    "transport": transport_co2,
    "tech": tech_co2,
    "lifestyle": lifestyle_co2,
    "fashion": fashion_co2,
    "diet": diet_co2,
}
max_cat = max(cat_values, key=cat_values.get)
rec_text = T[f"rec_{max_cat}"]

# ═══════════════════════════════════════════════════════════
# HERO HEADER
# ═══════════════════════════════════════════════════════════
st.markdown(
    f"""
<div class="hero">
    <h1>{T["page_title"]}</h1>
    <p>{T["page_subtitle"]}</p>
    <div class="badge-container">
        <div class="badge">{T["badge_fmt"].format(len(df))}</div>
        <div class="badge" style="background: rgba(46,125,50,0.8); border:none;">{badge}</div>
    </div>
</div>
""",
    unsafe_allow_html=True,
)

# ═══════════════════════════════════════════════════════════
# METRIC CARDS HTML PREPARATION
# ═══════════════════════════════════════════════════════════
cats = [
    ("🚗", T["card_transport"], transport_co2),
    ("💻", T["card_tech"], tech_co2),
    ("🎧", T["card_lifestyle"], lifestyle_co2),
    ("👗", T["card_fashion"], fashion_co2),
    ("🥗", T["card_diet"], diet_co2),
]
cards_html = ""
for icon, label, val in cats:
    cards_html += f"""
    <div class="card">
        <div class="icon">{icon}</div>
        <div class="lbl">{label}</div>
        <div class="val">{val:.2f}</div>
        <div class="unit">{T["card_unit"]}</div>
    </div>"""

cards_html += f"""
    <div class="card total">
        <div class="icon">🌍</div>
        <div class="lbl">{T["card_total"]}</div>
        <div class="val">{total_co2:.2f}</div>
        <div class="unit">{T["card_unit"]}</div>
    </div>"""

# ═══════════════════════════════════════════════════════════
# TABBED LAYOUT
# ═══════════════════════════════════════════════════════════
tab1, tab2, tab3 = st.tabs([T["tab_dashboard"], T["tab_analytics"], T["tab_action"]])

with tab1:
    st.info(T["dashboard_howto"], icon="ℹ️")
    if percentile is None:
        st.warning(T["warn_percentile_body"], icon="⚠️")
    st.markdown(f'<div class="cards">{cards_html}</div>', unsafe_allow_html=True)
    _card_labels = {
        "transport": T["card_transport"],
        "tech": T["card_tech"],
        "lifestyle": T["card_lifestyle"],
        "fashion": T["card_fashion"],
        "diet": T["card_diet"],
    }
    _pct_top = (
        100.0 * cat_values[max_cat] / total_co2 if total_co2 > 1e-9 else 0.0
    )
    st.caption(
        T["summary_top_cat"].format(
            name=_card_labels[max_cat], pct=_pct_top
        )
    )

    st.markdown(
        f"""
    <div class="percentile-box">
        <h3>{pct_text}</h3>
    </div>
    """,
        unsafe_allow_html=True,
    )

    fig_g = build_gauge_figure(
        total_co2,
        avg,
        gauge_title=T["gauge_title"],
        theme_dark=theme_dark,
    )
    st.plotly_chart(fig_g, use_container_width=True)

    if percentile is not None and percentile >= 50:
        if not st.session_state.get("balloons_shown", False):
            st.balloons()
            st.session_state["balloons_shown"] = True
        st.success(T["msg_success"], icon="🎈")
    else:
        st.session_state["balloons_shown"] = False
        if percentile is not None:
            st.info(T["msg_motivate"], icon="💡")

with tab2:
    if percentile is None:
        st.warning(T["warn_percentile_analytics"], icon="⚠️")
    df_tree = build_treemap_rows(F, T, **vals)
    fig_tree = build_treemap_figure(
        df_tree, treemap_title=T["treemap_title"], theme_dark=theme_dark
    )
    st.plotly_chart(fig_tree, use_container_width=True)
    st.caption(T["treemap_summary"])

    st.markdown("<br><hr>", unsafe_allow_html=True)

    c3, c4 = st.columns(2)
    radar_cats = [
        T["card_transport"],
        T["card_tech"],
        T["card_lifestyle"],
        T["card_fashion"],
        T["card_diet"],
    ]
    user_vals = [transport_co2, tech_co2, lifestyle_co2, fashion_co2, diet_co2]
    avg_vals = [
        avg["transport"],
        avg["tech"],
        avg["lifestyle"],
        avg["fashion"],
        avg["diet"],
    ]

    with c3:
        fig_r = build_radar_figure(
            user_vals,
            avg_vals,
            radar_cats,
            legend_you=T["legend_you"],
            legend_avg=T["legend_avg"],
            radar_title=T["radar_title"],
            theme_dark=theme_dark,
        )
        st.plotly_chart(fig_r, use_container_width=True)

    with c4:
        fig_b = build_category_bar_figure(
            user_vals,
            avg_vals,
            radar_cats,
            legend_you=T["legend_you"],
            legend_avg=T["legend_avg"],
            bar_title=T["bar_title"],
            xaxis_label=T["xaxis_label"],
            theme_dark=theme_dark,
        )
        st.plotly_chart(fig_b, use_container_width=True)

    st.markdown("<br><hr>", unsafe_allow_html=True)
    with st.expander(T["methodology_title"], expanded=False):
        st.markdown(T["methodology_md"])

    st.markdown(f"### {T['hist_title']}")
    st.caption(T["hist_caption"])
    fig_hist = build_total_histogram_figure(
        df,
        total_co2,
        xaxis_label=T["xaxis_label"],
        hist_yaxis=T["hist_yaxis"],
        vline_label=T["hist_vline_label"],
        theme_dark=theme_dark,
    )
    st.plotly_chart(fig_hist, use_container_width=True)

    _numeric_totals = pd.to_numeric(df["total_daily_co2_kg"], errors="coerce").dropna()
    if not _numeric_totals.empty:
        _med = float(_numeric_totals.median())
        if total_co2 > _med * 1.02:
            _cmp = T["hist_cmp_above"]
        elif total_co2 < _med * 0.98:
            _cmp = T["hist_cmp_below"]
        else:
            _cmp = T["hist_cmp_equal"]
        st.caption(T["hist_summary"].format(med=_med, you=total_co2, cmp=_cmp))

    cat_cols = {
        "transport_co2_kg": T["card_transport"],
        "tech_co2_kg": T["card_tech"],
        "lifestyle_co2_kg": T["card_lifestyle"],
        "fashion_co2_kg": T["card_fashion"],
        "diet_co2_kg": T["card_diet"],
    }
    fig_box = build_category_box_figure(
        df,
        cat_cols,
        box_title=T["box_title"],
        y_axis_label=T["xaxis_label"],
        theme_dark=theme_dark,
    )
    st.plotly_chart(fig_box, use_container_width=True)
    st.caption(T["box_summary"])

with tab3:
    st.markdown(
        f"""
    <div class="recommendation">
        <strong>{T["rec_title"]}</strong><br>
        {rec_text}
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown(f"### {T['explorer_title_fmt'].format(len(df))}")
    all_cols = list(df.columns)
    _def_n = min(12, len(all_cols))
    chosen_cols = st.multiselect(
        T["explorer_cols"], all_cols, default=all_cols[:_def_n]
    )
    max_rows = st.slider(T["explorer_rows"], 10, min(500, len(df)), 50)
    if chosen_cols:
        st.dataframe(
            df[chosen_cols].head(max_rows),
            use_container_width=True,
            height=400,
        )
    else:
        st.info(T["explorer_empty"])

    st.markdown(f"### {T['share_title']}")
    st.caption(T["share_desc"])

    _svg_share = (
        '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" '
        'viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
        'stroke-linecap="round" stroke-linejoin="round">'
        '<circle cx="18" cy="5" r="3"></circle><circle cx="6" cy="12" r="3">'
        "</circle><circle cx=\"18\" cy=\"19\" r=\"3\"></circle>"
        '<line x1="8.59" y1="13.51" x2="15.42" y2="17.49"></line>'
        '<line x1="15.41" y1="6.51" x2="8.59" y2="10.49"></line></svg>'
    )
    _btn_idle_html = _svg_share + f"<span>{html.escape(T['story_share_btn'])}</span>"
    _js_btn_idle = json.dumps(_btn_idle_html)
    _js_btn_busy = json.dumps(f"<span>{html.escape(T['story_processing'])}</span>")
    _js_alert_dl = json.dumps(T["story_alert_download"])
    _js_alert_fail = json.dumps(T["story_alert_fail"])
    _js_share_title = json.dumps(T["story_share_native_title"])
    _js_share_text = json.dumps(T["story_share_native_text"])
    _safe_story_h2 = html.escape(T["story_brand_title"])
    _safe_card_lbl = html.escape(T["card_total"])
    _safe_unit = html.escape(T["card_unit"])
    _safe_badge = html.escape(badge)

    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700;800;900&display=swap');
    body {{ font-family: 'Inter', sans-serif; margin: 0; padding: 0; }}
    .story-card-wrapper {{ display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; background: transparent; }}
    .story-card {{
        background: linear-gradient(135deg, #111, #222);
        border-radius: 24px; padding: 30px; color: white;
        text-align: center; width: 300px;
        box-shadow: 0 20px 50px rgba(0,0,0,0.3);
        border: 1px solid rgba(255,255,255,0.1);
        position: relative; overflow: hidden; margin-bottom: 20px;
    }}
    .story-card::before {{
        content: ''; position: absolute; top: 0; left: 0; right: 0; height: 6px;
        background: linear-gradient(90deg, #4caf50, #81c784, #2e7d32);
    }}
    .story-card h2 {{ margin: 0 0 5px 0; font-size: 1.3rem; font-weight: 800; color: #81c784; }}
    .story-card .score-label {{ font-size: 0.85rem; text-transform: uppercase; letter-spacing: 1px; opacity: 0.7; }}
    .story-card .big-score {{ font-size: 4rem; font-weight: 900; margin: 5px 0; line-height: 1; letter-spacing: -2px; color: #fff; }}
    .story-card .unit {{ font-size: 1rem; opacity: 0.8; font-weight: 500; }}
    .story-card .badge-text {{ font-size: 1.1rem; font-weight: 700; padding: 6px 16px; background: rgba(255,255,255,0.1); border-radius: 20px; display: inline-block; margin: 15px 0; border: 1px solid rgba(255,255,255,0.2); }}
    .story-card .tag {{ font-size: 0.9rem; color: #aaa; margin-top: 10px; font-weight: 500; }}

    .cta-btn {{ display:flex; align-items:center; justify-content:center; gap:8px; background:linear-gradient(45deg, #2e7d32, #1b5e20); color:#fff; text-decoration:none; padding:14px 32px; border-radius:30px; font-weight:700; border:none; cursor:pointer; font-family: 'Inter', sans-serif; font-size: 1rem; box-shadow:0 8px 20px rgba(46,125,50,.4); }}
    </style>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
    </head>
    <body>
    <div class="story-card-wrapper">
        <div id="story-card" class="story-card">
            <h2>🌍 {_safe_story_h2}</h2>
            <div class="score-label">{_safe_card_lbl}</div>
            <div class="big-score">{total_co2:.1f}</div>
            <div class="unit">{_safe_unit}</div>
            <div class="badge-text">{_safe_badge}</div>
            <div class="tag">@marmarayesk</div>
        </div>
        <button type="button" id="share-btn" class="cta-btn"></button>
    </div>

    <script>
    const BTN_IDLE = {_js_btn_idle};
    const BTN_BUSY = {_js_btn_busy};
    const MSG_DL = {_js_alert_dl};
    const MSG_FAIL = {_js_alert_fail};
    const SHARE_TITLE = {_js_share_title};
    const SHARE_TEXT = {_js_share_text};
    const btn = document.getElementById("share-btn");
    const card = document.getElementById("story-card");

    if (btn) {{
        btn.innerHTML = BTN_IDLE;
        btn.addEventListener("click", async () => {{
            const originalText = btn.innerHTML;
            btn.innerHTML = BTN_BUSY;
            try {{
                const canvas = await html2canvas(card, {{
                    scale: 3,
                    useCORS: true,
                    backgroundColor: null
                }});

                canvas.toBlob(async (blob) => {{
                    const file = new File([blob], "yesk-footprint.png", {{ type: "image/png" }});

                    if (navigator.canShare && navigator.canShare({{ files: [file] }})) {{
                        await navigator.share({{
                            title: SHARE_TITLE,
                            text: SHARE_TEXT,
                            files: [file]
                        }});
                    }} else {{
                        const url = URL.createObjectURL(blob);
                        const a = document.createElement("a");
                        a.href = url;
                        a.download = "yesk-footprint.png";
                        document.body.appendChild(a);
                        a.click();
                        document.body.removeChild(a);
                        URL.revokeObjectURL(url);
                        alert(MSG_DL);
                    }}
                    btn.innerHTML = originalText;
                }}, "image/png");
            }} catch (err) {{
                console.error("Error sharing:", err);
                alert(MSG_FAIL);
                btn.innerHTML = originalText;
            }}
        }});
    }}
    </script>
    </body>
    </html>
    """

    components.html(html_code, height=720, scrolling=True)

    st.markdown(
        f"""
    <div class="cta-box">
        <h3>{T["cta_title"]}</h3>
        <p>{T["cta_text"]}</p>
        <a href="https://www.instagram.com/marmarayesk" target="_blank" class="cta-btn">{T["cta_button"]}</a>
    </div>
    """,
        unsafe_allow_html=True,
    )

st.markdown(
    f"<p style='text-align:center;color:#9e9e9e;font-size:0.8rem;margin-top:40px'>"
    f"{T['footer']}</p>",
    unsafe_allow_html=True,
)
