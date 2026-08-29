"""Measure realized funding carry magnitude on the in-sample window ONLY.

Dispatch R2 (2026-07-25). Read-only measurement. Reads exactly two files:
    trading-bot/local_data/BTCUSDT_funding_8h.csv
    trading-bot/local_data/ETHUSDT_funding_8h.csv

WINDOW BOUND IS MANDATORY AND APPLIED INTERNALLY (see WINDOW_START/WINDOW_END).
The CSVs on disk extend to 2026-07-05 and physically contain the FROZEN holdout
2026-01-01..2026-06-30 (config/campaign_data_policy.yaml:18) and the SEALED
Kraken Q1 tranche (:151-168). data/feed_registry.py::build_daily_funding_series
applies no bound of its own (feed_registry.py:63-71), so the bound is enforced
here, before any statistic is computed.

Daily aggregation replicates build_daily_funding_series exactly:
    timestamp -> to_datetime -> dt.normalize() -> groupby(day)["funding_rate"].sum()

No repair, no imputation, no widening. Malformed input -> raise.
"""

import os
import sys

import pandas as pd

WINDOW_START = pd.Timestamp("2019-12-01")
WINDOW_END = pd.Timestamp("2023-12-31")  # inclusive, UTC calendar days

SYMBOLS = ["BTCUSDT", "ETHUSDT"]
DATA_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "trading-bot",
    "local_data",
)


def load_bounded(symbol):
    """Load the 8h CSV and IMMEDIATELY restrict to the in-sample window."""
    # venue-fixed-binance: does not go through FundingRateFetcher.cache_key()'s
    # venue qualification (trading-bot/data/fetchers/funding_rate_fetcher.py:
    # 117-118) -- will not resolve a kraken funding cache once one exists.
    path = os.path.join(DATA_DIR, f"{symbol}_funding_8h.csv")
    if not os.path.exists(path):
        raise SystemExit(f"STOP: missing CSV {path}")

    raw = pd.read_csv(path, usecols=["timestamp", "funding_rate"])
    if raw.empty:
        raise SystemExit(f"STOP: empty CSV {path}")

    raw["timestamp"] = pd.to_datetime(raw["timestamp"])
    if raw["timestamp"].isna().any():
        raise SystemExit(f"STOP: unparseable timestamps in {path}")
    if raw["funding_rate"].isna().any():
        raise SystemExit(f"STOP: NaN funding_rate in {path}")

    n_raw = len(raw)
    raw_min, raw_max = raw["timestamp"].min(), raw["timestamp"].max()

    # --- WINDOW BOUND (step 2) -------------------------------------------
    day = raw["timestamp"].dt.normalize()
    bounded = raw[(day >= WINDOW_START) & (day <= WINDOW_END)].copy()
    # ---------------------------------------------------------------------

    if bounded.empty:
        raise SystemExit(f"STOP: window bound left no rows for {symbol}")

    return raw, bounded, n_raw, raw_min, raw_max


def daily_series(bounded):
    """Sum 8h settlements to daily f_D exactly as build_daily_funding_series does."""
    df = bounded.copy()
    df["day"] = df["timestamp"].dt.normalize()
    return df.groupby("day")["funding_rate"].sum().sort_index()


def main():
    for symbol in SYMBOLS:
        raw, bounded, n_raw, raw_min, raw_max = load_bounded(symbol)
        n_bounded = len(bounded)
        n_dropped = n_raw - n_bounded

        print(f"===== {symbol} =====")
        print(f"[L1] raw 8h rows            : {n_raw}")
        print(f"[L2] raw range              : {raw_min} .. {raw_max}")
        print(f"[L3] rows kept after bound  : {n_bounded}")
        print(f"[L4] ROWS DROPPED BY BOUND  : {n_dropped}")

        # ---- step 3: daily series ---------------------------------------
        f = daily_series(bounded)
        n_days = len(f)
        print(f"[L5] N_days                 : {n_days}")
        print(
            f"[L6] actual date range      : {f.index.min().date()} .. {f.index.max().date()}"
        )

        # calendar-gap diagnostic: days absent from the series (no settlement)
        span_days = (f.index.max() - f.index.min()).days + 1
        print(
            f"[L7] calendar span (days)   : {span_days}  (missing days: {span_days - n_days})"
        )

        prev = f.shift(1)
        lagged = f.iloc[1:]  # days with a defined predecessor
        prev_lagged = prev.iloc[1:]
        n_lagged = len(lagged)

        # LAGGED (as implemented): S1 = sum_D sign(f_{D-1}) * f_D
        carry_daily = prev_lagged.apply(lambda x: (x > 0) - (x < 0)) * lagged
        S1 = float(carry_daily.sum())
        # ZERO-LAG (upper bound): S0 = sum_D |f_D|
        S0 = float(f.abs().sum())

        A1 = (365.0 / n_lagged) * S1 * 100.0
        A0 = (365.0 / n_days) * S0 * 100.0

        print(f"[L8] N_days_lagged (S1 base): {n_lagged}")
        print(f"[L9] S1 (lagged sum)        : {S1:.8f}")
        print(f"[L10] S0 (sum |f_D|)        : {S0:.8f}")
        print(f"[L11] A1 (lagged, %/yr)     : {A1:.4f}")
        print(f"[L12] A0 (zero-lag, %/yr)   : {A0:.4f}")

        # ---- step 6: empirical sign-flip rate ---------------------------
        sgn = f.apply(lambda x: (x > 0) - (x < 0))
        sgn_prev = sgn.shift(1).iloc[1:]
        flips = int((sgn.iloc[1:] != sgn_prev).sum())
        print(f"[L13] sign flips (count)    : {flips} of {n_lagged} transitions")
        print(f"[L14] sign-flip fraction    : {flips / n_lagged:.4f}")
        print(f"[L15] zero-rate days        : {int((f == 0).sum())}")

        # ---- step 7: A1 per calendar year -------------------------------
        print("[L16] A1 by calendar year:")
        for year, grp in carry_daily.groupby(carry_daily.index.year):
            a_y = (365.0 / len(grp)) * float(grp.sum()) * 100.0
            print(f"       {year}: A1={a_y:8.4f} %/yr   (n_days={len(grp)})")

        # ---- step 8: distribution ---------------------------------------
        print(f"[L17] mean |f_D|            : {float(f.abs().mean()):.8f}")
        print(f"[L18] daily carry median    : {float(carry_daily.median()):.8f}")
        print(f"[L19] daily carry p10       : {float(carry_daily.quantile(0.10)):.8f}")
        print(f"[L20] daily carry p90       : {float(carry_daily.quantile(0.90)):.8f}")
        print()


if __name__ == "__main__":
    sys.exit(main())
