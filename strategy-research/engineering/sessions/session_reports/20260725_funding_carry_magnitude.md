# Funding Carry Magnitude — Measured (Dispatch R2, 2026-07-25)

Read-only measurement. One new file (`strategy-research/tools/measure_funding_carry.py`),
one new report (this file). Nothing committed. Nothing under `trading-bot/` modified.
No backtest run.

---

## 1. Precondition manifest

`git log --oneline -1` (verbatim):

```
b542bb2 additive off-by-default funding-accrual mechanism per the 2026-07-24 design spec; flag off = byte-identical prior behavior; no protocol registered and no re-cost run yet.
```

`git status --porcelain` (verbatim):

```
?? strategy-research/docs/session_reports/20260725_funding_recost_feasibility.md
```

File existence:

| Manifest path | Result |
|---|---|
| `trading-bot/local_data/BTCUSDT_funding_8h.csv` | True |
| `trading-bot/local_data/ETHUSDT_funding_8h.csv` | True |
| `runs/run_059/artifacts/pass_rule_evaluation.yaml` | **repo-root-relative: False** |
| `strategy-research/runs/run_059/artifacts/pass_rule_evaluation.yaml` | True |

**Manifest resolution note.** The third path is written repo-root-relative in the dispatch
but the `runs/` tree lives under `strategy-research/`. A recursive search found exactly one
`artifacts/` copy — `strategy-research/runs/run_059/artifacts/pass_rule_evaluation.yaml` —
plus one superseded copy at `strategy-research/runs/run_059/superseded_20260718_tz_bug/`
which was **not** used. This is a path-convention resolution, not a substitution: the
required artifact exists and was read. Manifest **PASS**.

Drawdown-gate fact, recorded as instructed
(`strategy-research/runs/run_059/artifacts/pass_rule_evaluation.yaml:14-24`): criterion (b)
`max_abs_drawdown_pct` = **34.922** (BTCUSDT) / **49.606** (ETHUSDT) vs threshold **< 30**,
result FAIL on both. This gate fails independently of any cost assumption, so **no branch of
the decision rule below — including ESCALATE — revives run_059.**

---

## 2. Window bound (applied FIRST, before any statistic)

Bound: `2019-12-01 .. 2023-12-31` inclusive, UTC calendar days. Enforced inside the script at
`measure_funding_carry.py:55-58`, immediately after load and before any aggregation.
`build_daily_funding_series` applies no bound of its own (`trading-bot/data/feed_registry.py:63-71`),
which is why the bound is enforced in the measurement script.

| Symbol | Raw 8h rows | Raw range on disk | Kept | **Rows dropped by bound** |
|---|---|---|---|---|
| BTCUSDT | 7468 (`L1`) | 2019-09-10 08:00 .. 2026-07-05 08:00 (`L2`) | 4474 (`L3`) | **2994** (`L4`) |
| ETHUSDT | 7234 (`L1`) | 2019-11-27 08:00 .. 2026-07-05 08:00 (`L2`) | 4474 (`L3`) | **2760** (`L4`) |

The dropped rows include the FROZEN holdout `2026-01-01..2026-06-30`
(`strategy-research/config/campaign_data_policy.yaml:18`) and the SEALED Kraken Q1 tranche
(`:151-168`). No statistic in this report was computed on unbounded data.

---

## 3. Daily series and annualized carry

Daily aggregation replicates `build_daily_funding_series` exactly — `to_datetime` →
`dt.normalize()` → `groupby(day)["funding_rate"].sum()` (`measure_funding_carry.py:66-70`,
matching `feed_registry.py:67-69`).

| Symbol | N_days | Actual range | Missing days in span | N_days_lagged |
|---|---|---|---|---|
| BTCUSDT | 1492 (`L5`) | 2019-12-01 .. 2023-12-31 (`L6`) | 0 (`L7`) | 1491 (`L8`) |
| ETHUSDT | 1492 (`L5`) | 2019-12-01 .. 2023-12-31 (`L6`) | 0 (`L7`) | 1491 (`L8`) |

No day inside the window is absent from either series, so no partial-day or gap handling was
needed and none was applied.

| Symbol | S1 (lagged) | S0 (sum \|f_D\|) | **A1 (%/yr)** | A0 (%/yr, upper bound) |
|---|---|---|---|---|
| BTCUSDT | 0.63057912 (`L9`) | 0.68684566 (`L10`) | **15.4367** (`L11`) | 16.8029 (`L12`) |
| ETHUSDT | 0.78580003 (`L9`) | 0.84004649 (`L10`) | **19.2366** (`L11`) | 20.5507 (`L12`) |

`S1 = Σ_D sign(f_{D-1})·f_D` (`measure_funding_carry.py:101-102`);
`S0 = Σ_D |f_D|` (`:104`); `A = (365/N)·S·100` (`:106-107`). The first day of each series has
no predecessor and is excluded from S1; S0 uses all 1492 days. The lag is a one-row shift on
the daily series (`:95-97`); since there are zero missing days, one row = one calendar day.

---

## 4. R — required annualized carry (pre-registered formula, unaltered)

`R = (|net_expectancy_bps| − perp_fee_saving_bps) × trades_per_day × 365 / 100`

**Inputs, all read from run_059's own artifacts and `cost_model.yaml`:**

| Input | Value | Source |
|---|---|---|
| `net_expectancy_bps` (pooled mean) | −38.4665 | `strategy-research/runs/run_059/artifacts/protocol_result.yaml:3042` |
| pooled trade count `n` | 699 | `protocol_result.yaml:3045` (independently confirmed: sum of `core.trade_count` over all 98 window×symbol slots = 699) |
| day count | 2886 symbol-days | sum of `per_regime.unknown.bar_count` over all 98 slots in `protocol_result.yaml` (98 slots = 49 monthly windows × 2 symbols) |
| run_059 assumed RT cost | BTCUSDT 17.0, ETHUSDT 17.5 | `strategy-research/runs/run_059/artifacts/validation_protocol.yaml:47-49` |
| perp `round_trip_cost_bps` (default) | 10.0 | `strategy-research/config/cost_model.yaml:161-162` |

`trades_per_day = 699 / 2886 = 0.2422037` trades per symbol-day.

`perp_fee_saving_bps` = run_059 assumed RT − perp RT:
BTCUSDT `17.0 − 10.0 = 7.0`; ETHUSDT `17.5 − 10.0 = 7.5`.

Arithmetic:

```
R_BTCUSDT = (38.4665 − 7.0) × 0.2422037 × 365 / 100
          = 31.4665 × 0.2422037 × 3.65
          = 7.62130 × 3.65
          = 27.8178 %/yr

R_ETHUSDT = (38.4665 − 7.5) × 0.2422037 × 365 / 100
          = 30.9665 × 0.2422037 × 3.65
          = 7.50020 × 3.65
          = 27.3757 %/yr
```

**Per-symbol input availability — no estimate was substituted.** `net_expectancy_bps` exists
in the artifacts **only pooled** across both symbols (`protocol_result.yaml:3041-3045`). The
per-symbol trade counts in `artifacts/research_decision.yaml:21,29` are explicitly labelled
`"~340 (estimated from 699 pooled / 2 symbols)"` and `"~359 (estimated…)"` — these are
estimates by the artifact's own admission, so per the no-substitution constraint they were
**not used**. Both R values therefore use the pooled expectancy and the pooled per-symbol-day
trade rate; the only per-symbol term is `perp_fee_saving_bps`, which is genuinely per-symbol
in the source. This is stated rather than silently averaged: R is a pooled-expectancy figure
labelled per symbol.

---

## 5. Branch fired

| Symbol | A1 (%/yr) | R (%/yr) | **A1 / R** | Branch |
|---|---|---|---|---|
| BTCUSDT | 15.4367 | 27.8178 | **0.555** | **CLOSE-NULL** (A1 < R) |
| ETHUSDT | 19.2366 | 27.3757 | **0.703** | **CLOSE-NULL** (A1 < R) |

`STOP-REFUTED` (A1 ≤ −2.0 %/yr) did **not** fire — both A1 are positive, so the sign
derivation is not contradicted by the data.

The zero-lag upper bound also falls short: A0 = 16.80 / 20.55 %/yr vs R = 27.82 / 27.38 %/yr.
Even a hypothetical perfect-foresight, zero-lag funding credit — an unattainable ceiling —
does not reach the required carry on either symbol. **The gap does not close, and it does not
close under the most generous assumption available.**

Reported, not acted on. And per §1, criterion (b) fails independently at 34.9 / 49.6 vs < 30,
so run_059 stays dead regardless.

---

## 6. Empirical sign-flip rate

| Symbol | Flips | Transitions | Fraction | Zero-rate days |
|---|---|---|---|---|
| BTCUSDT | 180 (`L13`) | 1491 | 0.1207 (`L14`) | 0 (`L15`) |
| ETHUSDT | 152 (`L13`) | 1491 | 0.1019 (`L14`) | 0 (`L15`) |

Brief's figures: BTCUSDT **228**, ETHUSDT **220**
(`strategy-research/docs/session_reports/20260725_funding_recost_feasibility.md:381-384`,
sourcing `FUNDING_MR_DAILY_RETEST.md:240-244`).

**MISMATCH.** Measured 180 / 152 vs brief 228 / 220 — 21% and 31% below the brief's counts.
The window is not the explanation: the brief's counts are stated against the same 1,492 days,
which is exactly what was measured here. Cause is **undetermined and not investigated** under
this dispatch's read-only scope. One candidate worth recording, flagged as unverified: the
brief's counts may derive from the forward-filled 8h *signal* feed (`FundingRateFetcher` +
`merge_asof`) rather than the daily-*summed cost* series measured here — `feed_registry.py:41-46`
states those are deliberately distinct series. That is a hypothesis, not a finding.

The mismatch does not affect §5. R and A1 are computed from the funding series and run_059's
artifacts directly; neither uses the brief's flip counts.

---

## 7. A1 by calendar year — carry decays across the window

`measure_funding_carry.py:124-127`.

| Year | BTCUSDT A1 (%/yr) | ETHUSDT A1 (%/yr) | n_days |
|---|---|---|---|
| 2019 (Dec only) | 4.6894 | 10.2332 | 30 |
| 2020 | 19.3438 | 27.1763 | 366 |
| 2021 | 31.2850 | 37.5817 | 365 |
| 2022 | 4.3878 | 4.6791 | 365 |
| 2023 | 7.6029 | 8.2273 | 365 |

**Yes — carry decays materially across the window, and the decay is a level shift, not a
drift.** Both symbols peak in 2021 (31.3 / 37.6 %/yr) and collapse by roughly 7x / 8x to
4.4 / 4.7 %/yr in 2022, recovering only partially to 7.6 / 8.2 %/yr in 2023. The whole-window
A1 (15.4 / 19.2) is therefore carried by the 2020–2021 bull-market regime and is **not**
representative of the window's later years: on 2022–2023 alone, carry runs at roughly a third
of the headline figure.

This bears on the **separate carry-harvesting hypothesis, not on run_059**. Two consequences
for that separate line, recorded without acting on either: (i) any carry-harvesting backtest
whose window includes 2020–2021 inherits a regime that has not recurred since, and (ii) the
most recent in-sample years — the ones closest to live conditions — show the *weakest* carry,
which is the adverse direction for that hypothesis. If a carry-harvesting hypothesis is ever
opened, it should be pre-registered against the 2022–2023 level, not the whole-window mean.

---

## 8. Distribution of daily funding

`measure_funding_carry.py:130-133`. Values are daily decimal rates (sum of that day's
settlements); daily carry = `sign(f_{D-1})·f_D`.

| Symbol | mean \|f_D\| (`L17`) | carry median (`L18`) | carry p10 (`L19`) | carry p90 (`L20`) |
|---|---|---|---|---|
| BTCUSDT | 0.00046035 | 0.00030000 | −0.00003789 | 0.00111877 |
| ETHUSDT | 0.00056303 | 0.00030000 | −0.00000211 | 0.00138634 |

The median daily carry on both symbols is exactly 0.00030000 — three settlements at the
0.0001 baseline rate — i.e. the typical day sits at the funding floor, and the mean is pulled
above the median entirely by a positive right tail (p90 ≈ 3.7x / 4.6x the median). The p10 is
near zero and only slightly negative, consistent with the low flip rates in §6.

---

## Appendix — script read-back

Read back from disk after writing, verbatim (`strategy-research/tools/measure_funding_carry.py`,
139 lines):

```python
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
        print(f"[L6] actual date range      : {f.index.min().date()} .. {f.index.max().date()}")

        # calendar-gap diagnostic: days absent from the series (no settlement)
        span_days = (f.index.max() - f.index.min()).days + 1
        print(f"[L7] calendar span (days)   : {span_days}  (missing days: {span_days - n_days})")

        prev = f.shift(1)
        lagged = f.iloc[1:]           # days with a defined predecessor
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
```

## Appendix — raw script output

```
===== BTCUSDT =====
[L1] raw 8h rows            : 7468
[L2] raw range              : 2019-09-10 08:00:00 .. 2026-07-05 08:00:00.001000
[L3] rows kept after bound  : 4474
[L4] ROWS DROPPED BY BOUND  : 2994
[L5] N_days                 : 1492
[L6] actual date range      : 2019-12-01 .. 2023-12-31
[L7] calendar span (days)   : 1492  (missing days: 0)
[L8] N_days_lagged (S1 base): 1491
[L9] S1 (lagged sum)        : 0.63057912
[L10] S0 (sum |f_D|)        : 0.68684566
[L11] A1 (lagged, %/yr)     : 15.4367
[L12] A0 (zero-lag, %/yr)   : 16.8029
[L13] sign flips (count)    : 180 of 1491 transitions
[L14] sign-flip fraction    : 0.1207
[L15] zero-rate days        : 0
[L16] A1 by calendar year:
       2019: A1=  4.6894 %/yr   (n_days=30)
       2020: A1= 19.3438 %/yr   (n_days=366)
       2021: A1= 31.2850 %/yr   (n_days=365)
       2022: A1=  4.3878 %/yr   (n_days=365)
       2023: A1=  7.6029 %/yr   (n_days=365)
[L17] mean |f_D|            : 0.00046035
[L18] daily carry median    : 0.00030000
[L19] daily carry p10       : -0.00003789
[L20] daily carry p90       : 0.00111877

===== ETHUSDT =====
[L1] raw 8h rows            : 7234
[L2] raw range              : 2019-11-27 08:00:00 .. 2026-07-05 08:00:00.001000
[L3] rows kept after bound  : 4474
[L4] ROWS DROPPED BY BOUND  : 2760
[L5] N_days                 : 1492
[L6] actual date range      : 2019-12-01 .. 2023-12-31
[L7] calendar span (days)   : 1492  (missing days: 0)
[L8] N_days_lagged (S1 base): 1491
[L9] S1 (lagged sum)        : 0.78580003
[L10] S0 (sum |f_D|)        : 0.84004649
[L11] A1 (lagged, %/yr)     : 19.2366
[L12] A0 (zero-lag, %/yr)   : 20.5507
[L13] sign flips (count)    : 152 of 1491 transitions
[L14] sign-flip fraction    : 0.1019
[L15] zero-rate days        : 0
[L16] A1 by calendar year:
       2019: A1= 10.2332 %/yr   (n_days=30)
       2020: A1= 27.1763 %/yr   (n_days=366)
       2021: A1= 37.5817 %/yr   (n_days=365)
       2022: A1=  4.6791 %/yr   (n_days=365)
       2023: A1=  8.2273 %/yr   (n_days=365)
[L17] mean |f_D|            : 0.00056303
[L18] daily carry median    : 0.00030000
[L19] daily carry p10       : -0.00000211
[L20] daily carry p90       : 0.00138634
```
