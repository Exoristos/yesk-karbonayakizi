"""Kohort karşılaştırması için saf pandas yardımcıları (Streamlit bağımlılığı yok)."""

from __future__ import annotations

import pandas as pd


def cohort_percentile_strictly_higher(
    total_series: pd.Series,
    user_total: float,
) -> tuple[float | None, str | None]:
    """
    Kohortta günlük toplamı kullanıcıdan **kesin olarak büyük** olan satırların yüzdesi.

    Sentetik veri seti ile `app.py`'deki tanım uyumludur: (df[col] > user_total).mean()*100

    Args:
        total_series: ``total_daily_co2_kg`` sütunu (veya eşdeğeri).
        user_total: Kullanıcının günlük toplam kg CO₂ tahmini.

    Returns:
        (yüzde, None) başarıda; veri uygun değilse (None, kısa sebep kodu).

    Note:
        NaN değerler düşürülür; hiç geçerli satır kalmazsa başarısız döner.
    """
    numeric = pd.to_numeric(total_series, errors="coerce").dropna()
    if numeric.empty:
        return None, "no_valid_rows"
    pct = float((numeric > float(user_total)).mean() * 100.0)
    return pct, None
