"""
Günlük kg CO₂ tahmini: kategori toplamları ve treemap satırları.
Sentetik veri üretimi (generate_complex_data) ile aynı formülleri kullanır.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

import pandas as pd

# Kısa/orta mesafe uçuş başına yıllık ortalama CO₂ (kg); günlüğe /365 ile yayılır.
FLIGHT_CO2_KG_PER_TRIP: float = 250.0


@dataclass(frozen=True)
class FootprintResult:
    """Yan panel seçimlerinden türetilen günlük emisyonlar (kg CO₂)."""

    transport_co2: float
    tech_co2: float
    lifestyle_co2: float
    fashion_co2: float
    diet_co2: float

    @property
    def total_co2(self) -> float:
        """Beş kategorinin toplamı."""
        return (
            self.transport_co2
            + self.tech_co2
            + self.lifestyle_co2
            + self.fashion_co2
            + self.diet_co2
        )


def treemap_display_value(kg: float) -> float:
    """Treemap hücre boyutu için alt sınır (sıfır/negatif dilimleri görünür kılar)."""
    return max(kg, 0.001)


def diet_smoking_adjustment_kg(is_smoker: bool) -> float:
    """
    Sigara ile ilgili net düzeltme (sentetik veri setiyle uyumlu).
    İçmeyen profillerde −0.3 kg/gün kalibrasyon offset'i uygulanır.
    """
    return 0.3 if is_smoker else -0.3


def compute_footprint(
    factors: Mapping[str, Any],
    *,
    sel_route: str,
    sel_km: int,
    sel_flight: int,
    sel_pc: str,
    sel_gaming: float,
    sel_study: float,
    sel_phone: str,
    sel_charges: int,
    sel_heat: str,
    sel_dj: float,
    sel_board: int,
    sel_stream: float,
    sel_rec: str,
    sel_shower: int,
    sel_pet: str,
    sel_hw: str,
    sel_clothes: int,
    sel_style: str,
    sel_perf: str,
    sel_diet: str,
    sel_coffee: int,
    sel_smoke: bool,
    sel_del: str,
    sel_wat: str,
) -> FootprintResult:
    """Faktör sözlüğü ve seçimlere göre kategori bazlı günlük kg CO₂ döndürür."""
    grid: float = float(factors["grid_co2_kg_per_kwh"])

    transport_co2 = (
        float(factors["commute_co2_per_km"][sel_route]) * sel_km / 1000.0
        + (sel_flight * FLIGHT_CO2_KG_PER_TRIP) / 365.0
    )

    tech_co2 = (
        (float(factors["pc_watt"][sel_pc]) / 1000.0)
        * (sel_gaming + sel_study)
        * grid
        + float(factors["phone_charge_kwh"][sel_phone]) * sel_charges * grid
        + float(factors["heating_co2_kg_day"][sel_heat])
    )

    lifestyle_co2 = (
        sel_dj * 0.050 * grid
        + sel_board / 30.0 * 5.0
        + sel_stream * 0.055
        + float(factors["recycling_offset_kg"][sel_rec])
        + sel_shower * 0.1
        + float(factors["pet_co2_kg_day"][sel_pet])
        + float(factors["housework_co2_kg_day"][sel_hw])
    )

    fashion_co2 = (sel_clothes / 30.0) * 15.0 * float(
        factors["style_multiplier"][sel_style]
    ) + float(factors["perfume_shipping_kg_day"][sel_perf])

    diet_co2 = (
        float(factors["diet_base_kg_per_day"][sel_diet])
        + sel_coffee * 0.06
        + diet_smoking_adjustment_kg(sel_smoke)
        + float(factors["delivery_co2_kg_day"][sel_del])
        + float(factors["water_co2_kg_day"][sel_wat])
    )

    return FootprintResult(
        transport_co2=transport_co2,
        tech_co2=tech_co2,
        lifestyle_co2=lifestyle_co2,
        fashion_co2=fashion_co2,
        diet_co2=diet_co2,
    )


def build_treemap_rows(
    factors: Mapping[str, Any],
    labels: Mapping[str, str],
    *,
    sel_route: str,
    sel_km: int,
    sel_flight: int,
    sel_pc: str,
    sel_gaming: float,
    sel_study: float,
    sel_phone: str,
    sel_charges: int,
    sel_heat: str,
    sel_dj: float,
    sel_board: int,
    sel_stream: float,
    sel_rec: str,
    sel_shower: int,
    sel_pet: str,
    sel_hw: str,
    sel_clothes: int,
    sel_style: str,
    sel_perf: str,
    sel_diet: str,
    sel_coffee: int,
    sel_smoke: bool,
    sel_del: str,
    sel_wat: str,
) -> pd.DataFrame:
    """Treemap için kategori / kaynak / görüntü değeri sütunlu DataFrame üretir."""
    grid: float = float(factors["grid_co2_kg_per_kwh"])
    smoking_kg = diet_smoking_adjustment_kg(sel_smoke)

    sub_items: dict[str, list[tuple[str, float]]] = {
        f"🚗 {labels['card_transport']}": [
            (
                labels["sub_commute"],
                float(factors["commute_co2_per_km"][sel_route]) * sel_km / 1000.0,
            ),
            (
                labels["sub_flight"],
                (sel_flight * FLIGHT_CO2_KG_PER_TRIP) / 365.0,
            ),
        ],
        f"💻 {labels['card_tech']}": [
            (
                labels["sub_pc"],
                (float(factors["pc_watt"][sel_pc]) / 1000.0)
                * (sel_gaming + sel_study)
                * grid,
            ),
            (
                labels["sub_phone"],
                float(factors["phone_charge_kwh"][sel_phone]) * sel_charges * grid,
            ),
            (labels["sub_heating"], float(factors["heating_co2_kg_day"][sel_heat])),
        ],
        f"🎧 {labels['card_lifestyle']}": [
            (labels["sub_dj"], sel_dj * 0.050 * grid),
            (labels["sub_board"], sel_board / 30.0 * 5.0),
            (labels["sub_streaming"], sel_stream * 0.055),
            (
                labels["sub_recycle"],
                float(factors["recycling_offset_kg"][sel_rec]),
            ),
            (labels["sub_shower"], sel_shower * 0.1),
            (labels["sub_pets"], float(factors["pet_co2_kg_day"][sel_pet])),
            (labels["sub_housework"], float(factors["housework_co2_kg_day"][sel_hw])),
        ],
        f"👗 {labels['card_fashion']}": [
            (
                labels["sub_clothing"],
                (sel_clothes / 30.0) * 15.0 * float(factors["style_multiplier"][sel_style]),
            ),
            (
                labels["sub_perfume"],
                float(factors["perfume_shipping_kg_day"][sel_perf]),
            ),
        ],
        f"🥗 {labels['card_diet']}": [
            (
                labels["sub_food"],
                float(factors["diet_base_kg_per_day"][sel_diet]),
            ),
            (labels["sub_coffee"], sel_coffee * 0.06),
            (labels["sub_smoking"], smoking_kg),
            (
                labels["sub_delivery"],
                float(factors["delivery_co2_kg_day"][sel_del]),
            ),
            (labels["sub_water"], float(factors["water_co2_kg_day"][sel_wat])),
        ],
    }

    rows: list[dict[str, Any]] = []
    for cat, subs in sub_items.items():
        for name, raw_kg in subs:
            rows.append(
                {
                    "category": cat,
                    "source": name,
                    "co2": treemap_display_value(raw_kg),
                }
            )
    return pd.DataFrame(rows)
