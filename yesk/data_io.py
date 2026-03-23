"""Veri dosyalarını yükleme, şema doğrulama ve ``logging`` (Streamlit dışı saf fonksiyonlar)."""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any, Mapping

import pandas as pd

logger = logging.getLogger(__name__)


class DataLoadError(Exception):
    """``complex_factors.json`` veya ``complex_emissions.csv`` yüklenemediğinde / şema hatalı."""

    pass


# Kohort CSV: histogram, kutu grafik ve yüzdelik dilim için gerekli sütunlar
REQUIRED_COHORT_COLUMNS: frozenset[str] = frozenset(
    {
        "total_daily_co2_kg",
        "transport_co2_kg",
        "tech_co2_kg",
        "lifestyle_co2_kg",
        "fashion_co2_kg",
        "diet_co2_kg",
    }
)

# Faktör JSON üst anahtarları (``compute_footprint`` + yan panel ile uyum)
REQUIRED_FACTOR_TOP_KEYS: frozenset[str] = frozenset(
    {
        "commute_co2_per_km",
        "pc_watt",
        "phone_charge_kwh",
        "grid_co2_kg_per_kwh",
        "heating_co2_kg_day",
        "recycling_offset_kg",
        "diet_base_kg_per_day",
        "style_multiplier",
        "perfume_shipping_kg_day",
        "delivery_co2_kg_day",
        "water_co2_kg_day",
        "pet_co2_kg_day",
        "housework_co2_kg_day",
        "averages",
    }
)

REQUIRED_AVERAGES_KEYS: frozenset[str] = frozenset(
    {"transport", "tech", "lifestyle", "fashion", "diet", "total"}
)


def project_data_dir(project_root: str | Path) -> Path:
    """Uygulama kökü altındaki ``data`` dizini."""
    return Path(project_root) / "data"


def validate_cohort_dataframe(df: pd.DataFrame) -> None:
    """Beklenen kohort sütunlarını doğrular; eksikse ``DataLoadError`` fırlatır."""
    missing = REQUIRED_COHORT_COLUMNS - set(df.columns)
    if missing:
        msg = f"Cohort CSV missing columns: {sorted(missing)}"
        logger.error(msg)
        raise DataLoadError(msg)


def validate_factors_dict(factors: Mapping[str, Any]) -> None:
    """Faktör sözlüğü şemasını doğrular."""
    missing = REQUIRED_FACTOR_TOP_KEYS - set(factors.keys())
    if missing:
        msg = f"Factors JSON missing keys: {sorted(missing)}"
        logger.error(msg)
        raise DataLoadError(msg)

    avg = factors.get("averages")
    if not isinstance(avg, Mapping):
        raise DataLoadError("Factors JSON 'averages' must be an object")
    a_miss = REQUIRED_AVERAGES_KEYS - set(avg.keys())
    if a_miss:
        msg = f"Factors JSON averages missing: {sorted(a_miss)}"
        logger.error(msg)
        raise DataLoadError(msg)


def read_and_validate_factors(path: str | Path) -> dict[str, Any]:
    """JSON faktör dosyasını okur ve doğrular."""
    p = Path(path)
    if not p.is_file():
        msg = f"Factors file not found: {p}"
        logger.error(msg)
        raise DataLoadError(msg)
    try:
        with p.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        msg = f"Invalid JSON in factors file: {p}: {e}"
        logger.error(msg)
        raise DataLoadError(msg) from e

    if not isinstance(data, dict):
        raise DataLoadError("Factors JSON root must be an object")

    validate_factors_dict(data)
    logger.info("Loaded and validated factors: %s", p)
    return data


def read_and_validate_cohort_csv(path: str | Path) -> pd.DataFrame:
    """Kohort CSV'yi okur ve sütun şemasını doğrular."""
    p = Path(path)
    if not p.is_file():
        msg = f"Cohort CSV not found: {p}"
        logger.error(msg)
        raise DataLoadError(msg)
    try:
        df = pd.read_csv(p, encoding="utf-8")
    except Exception as e:
        msg = f"Failed to read cohort CSV {p}: {e}"
        logger.exception(msg)
        raise DataLoadError(msg) from e

    validate_cohort_dataframe(df)
    logger.info("Loaded and validated cohort CSV: %s (%d rows)", p, len(df))
    return df
