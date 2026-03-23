"""Yan panel yaşam tarzı girdileri: widget anahtarları ve sıfırlama."""

from __future__ import annotations

from typing import Any, Callable, Mapping

import streamlit as st

# Sıfırlama, widget oluşmadan önce session_state yazılmalı (Streamlit kuralı).
_RESET_INPUTS_FLAG = "_yesk_pending_inputs_reset"


def _first_key(d: Mapping[str, Any]) -> str:
    """Sözlükteki ilk anahtar (JSON sırası)."""
    return next(iter(d.keys()))


def reset_defaults(F: Mapping[str, Any]) -> dict[str, Any]:
    """Tüm yan panel widget anahtarlarının başlangıç değerleri."""
    return {
        "w_route": _first_key(F["commute_co2_per_km"]),
        "w_km_s": 18,
        "w_km_n": 18,
        "w_fl_s": 1,
        "w_fl_n": 1,
        "w_pc": "Mid-Range Gaming Laptop",
        "w_gaming": 2.5,
        "w_study": 4.0,
        "w_phone": "Mid-Range Phone (4500 mAh)",
        "w_charges": 1,
        "w_heat": "Dormitory (Shared)",
        "w_dj": 0.0,
        "w_board": 1,
        "w_stream": 3.0,
        "w_rec": "Sometimes",
        "w_shower": 12,
        "w_pet": "None",
        "w_hw": "Dormitory / Outsourced",
        "w_clothes": 3,
        "w_style": "Fast Fashion",
        "w_perf": "Never",
        "w_diet": "Moderate Meat",
        "w_coffee": 2,
        "w_smoke": False,
        "w_del": "Rarely (1-2/month)",
        "w_wat": "Tap / Filtered (0)",
        "w_precise_tf": False,
    }


def ensure_session_defaults(F: Mapping[str, Any]) -> None:
    """Eksik widget anahtarlarını doldurur."""
    for k, v in reset_defaults(F).items():
        if k not in st.session_state:
            st.session_state[k] = v


def render_inputs(
    F: Mapping[str, Any],
    T: Mapping[str, Any],
    tr_opt: Callable[[str], str],
) -> dict[str, Any]:
    """
    Yan panel içeriğini çizer (çağıran `with st.sidebar` kullanmalı).
    Dönen sözlük compute_footprint için gerekli sel_* anahtarlarını içerir.
    """
    ensure_session_defaults(F)

    if st.session_state.pop(_RESET_INPUTS_FLAG, False):
        for k, v in reset_defaults(F).items():
            st.session_state[k] = v
        st.session_state.balloons_shown = False
        st.toast(T["ui_reset_done"])

    st.caption(T["sidebar_methodology_hint"])
    st.caption(T["url_sidebar_tip"])
    st.divider()

    st.checkbox(T["use_precise_transport"], key="w_precise_tf")
    precise = st.session_state.w_precise_tf

    if st.button(T["ui_reset"], use_container_width=True):
        st.session_state[_RESET_INPUTS_FLAG] = True
        st.rerun()

    st.divider()
    st.markdown(f"**{T['ui_progress_title']}**")
    st.caption(T["ui_progress_hint"])
    st.divider()

    st.markdown(f"## {T['sidebar_title']}")
    st.caption(T["sidebar_caption"])

    # ── 1. Transportation ──
    with st.expander(T["exp_transport"], expanded=True):
        sel_route = st.selectbox(
            T["lbl_route"],
            list(F["commute_co2_per_km"].keys()),
            format_func=tr_opt,
            key="w_route",
            help=T["help_route"],
        )
        if precise:
            sel_km = int(
                st.number_input(
                    T["lbl_km"],
                    min_value=0,
                    max_value=150,
                    step=1,
                    key="w_km_n",
                    help=T["help_km"],
                )
            )
            sel_flight = int(
                st.number_input(
                    T["lbl_flights"],
                    min_value=0,
                    max_value=20,
                    step=1,
                    key="w_fl_n",
                    help=T["help_flights"],
                )
            )
        else:
            sel_km = int(
                st.slider(
                    T["lbl_km"],
                    0,
                    150,
                    key="w_km_s",
                    help=T["help_km"],
                )
            )
            sel_flight = int(
                st.slider(
                    T["lbl_flights"],
                    0,
                    20,
                    key="w_fl_s",
                    help=T["help_flights"],
                )
            )

    # ── 2. Tech ──
    with st.expander(T["exp_tech"], expanded=False):
        sel_pc = st.selectbox(
            T["lbl_pc"],
            list(F["pc_watt"].keys()),
            format_func=tr_opt,
            key="w_pc",
            help=T["help_pc"],
        )
        sel_gaming = st.slider(T["lbl_gaming"], 0.0, 14.0, key="w_gaming", step=0.5)
        sel_study = st.slider(T["lbl_study"], 0.0, 12.0, key="w_study", step=0.5)
        sel_phone = st.selectbox(
            T["lbl_phone"],
            list(F["phone_charge_kwh"].keys()),
            format_func=tr_opt,
            key="w_phone",
        )
        sel_charges = int(st.slider(T["lbl_charges"], 1, 4, key="w_charges"))
        sel_heat = st.selectbox(
            T["lbl_heating"],
            list(F["heating_co2_kg_day"].keys()),
            format_func=tr_opt,
            key="w_heat",
            help=T["help_heating"],
        )

    # ── 3. Lifestyle ──
    with st.expander(T["exp_lifestyle"], expanded=False):
        sel_dj = st.slider(T["lbl_dj"], 0.0, 6.0, key="w_dj", step=0.5)
        sel_board = int(st.slider(T["lbl_board"], 0, 8, key="w_board"))
        sel_stream = st.slider(T["lbl_stream"], 0.0, 10.0, key="w_stream", step=0.5)
        sel_rec = st.selectbox(
            T["lbl_recycle"],
            list(F["recycling_offset_kg"].keys()),
            format_func=tr_opt,
            key="w_rec",
            help=T["help_recycle"],
        )
        sel_shower = int(st.slider(T["lbl_shower"], 3, 40, key="w_shower"))
        sel_pet = st.selectbox(
            T["lbl_pets"],
            list(F["pet_co2_kg_day"].keys()),
            format_func=tr_opt,
            key="w_pet",
        )
        sel_hw = st.selectbox(
            T["lbl_housework"],
            list(F["housework_co2_kg_day"].keys()),
            format_func=tr_opt,
            key="w_hw",
        )

    # ── 4. Fashion ──
    with st.expander(T["exp_fashion"], expanded=False):
        sel_clothes = int(st.slider(T["lbl_clothes"], 0, 15, key="w_clothes"))
        sel_style = st.selectbox(
            T["lbl_style"],
            list(F["style_multiplier"].keys()),
            format_func=tr_opt,
            key="w_style",
        )
        sel_perf = st.selectbox(
            T["lbl_perfume"],
            list(F["perfume_shipping_kg_day"].keys()),
            format_func=tr_opt,
            key="w_perf",
        )

    # ── 5. Diet ──
    with st.expander(T["exp_diet"], expanded=False):
        sel_diet = st.selectbox(
            T["lbl_diet"],
            list(F["diet_base_kg_per_day"].keys()),
            format_func=tr_opt,
            key="w_diet",
            help=T["help_diet"],
        )
        sel_coffee = int(st.slider(T["lbl_coffee"], 0, 8, key="w_coffee"))
        sel_smoke = st.checkbox(T["lbl_smoke"], key="w_smoke")
        sel_del = st.selectbox(
            T["lbl_delivery"],
            list(F["delivery_co2_kg_day"].keys()),
            format_func=tr_opt,
            key="w_del",
        )
        sel_wat = st.selectbox(
            T["lbl_water"],
            list(F["water_co2_kg_day"].keys()),
            format_func=tr_opt,
            key="w_wat",
        )

    return {
        "sel_route": sel_route,
        "sel_km": sel_km,
        "sel_flight": sel_flight,
        "sel_pc": sel_pc,
        "sel_gaming": sel_gaming,
        "sel_study": sel_study,
        "sel_phone": sel_phone,
        "sel_charges": sel_charges,
        "sel_heat": sel_heat,
        "sel_dj": sel_dj,
        "sel_board": sel_board,
        "sel_stream": sel_stream,
        "sel_rec": sel_rec,
        "sel_shower": sel_shower,
        "sel_pet": sel_pet,
        "sel_hw": sel_hw,
        "sel_clothes": sel_clothes,
        "sel_style": sel_style,
        "sel_perf": sel_perf,
        "sel_diet": sel_diet,
        "sel_coffee": sel_coffee,
        "sel_smoke": sel_smoke,
        "sel_del": sel_del,
        "sel_wat": sel_wat,
    }
