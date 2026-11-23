import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    RAW = "debug_info.components.excess_power.last_history_value"
    MIN_CASES = 30

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            close = pd.to_numeric(df["close"], errors="coerce")
            ret20 = close / close.shift(20) - 1.0
            if "regime" in df.columns:
                reg_trend = df["regime"].astype(str) == "trending"
            else:
                reg_trend = pd.Series(False, index=df.index)
            down = ret20 < 0
            # In the first 20 bars of a window, the earlier prices are not
            # recorded, so the regime detector's recorded decision is used.
            down = down.where(ret20.notna(), reg_trend)
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            # The reading implies a rise when raw > 0 (standardise keeps the
            # sign); the expected side is short.
            situ = down & (raw > 0)
            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & situ & (fc < 0)).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)
    reading = ("Cases are grid bars (positions 0,5,10,... of each window) with "
               "forecast <= -2 and a 5-bar return inside the window, the coin's "
               "mean 5-bar return is over the same grid across all its windows, "
               "each case's value is -(excess return) x |forecast|/10 and the t is "
               "the ordinary t of their mean; the supporting check uses unweighted "
               "excess falls with cases equal to the median left out; and for the "
               "situation check, the 20-day return is taken from prices, or from "
               "the recorded regime on a window's first 20 bars.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": ("Fewer than 90% of active bars are short bars where the "
                           "raw excess-power reading is positive and the 20-day "
                           "return is negative."),
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    case_f = []
    case_excess = []
    for coin, wins in bars.items():
        grid = []
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            n = len(df)
            for i in range(0, n - H, H):
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 <= 0:
                    continue
                grid.append((c1 / c0 - 1.0, fc[i]))
        if not grid:
            continue
        rets = np.array([g[0] for g in grid])
        drift = float(np.mean(rets))
        for r, f in grid:
            if np.isfinite(f) and f <= -2:
                case_f.append(abs(f))
                case_excess.append(r - drift)

    case_f = np.array(case_f, dtype=float)
    case_excess = np.array(case_excess, dtype=float)
    n_cases = int(len(case_f))
    gains = -case_excess * case_f / 10.0

    mean_val = float(np.mean(gains)) if n_cases > 0 else None
    t_val = None
    if n_cases >= 2:
        sd = float(np.std(gains, ddof=1))
        if sd > 0:
            t_val = float(mean_val / (sd / np.sqrt(n_cases)))

    sup_val = None
    sup_pass = None
    if n_cases > 0:
        med = float(np.median(case_f))
        hi = case_f > med
        lo = case_f < med
        if hi.sum() > 0 and lo.sum() > 0:
            sup_val = float(np.mean(-case_excess[hi]) - np.mean(-case_excess[lo]))
            sup_pass = bool(sup_val > 0)
        else:
            sup_pass = False

    if n_cases < MIN_CASES:
        status = "not observable"
        decided_by = "Fewer than 30 cases with forecast <= -2 on the 5-bar grid (the plan's minimum)."
    elif t_val is None:
        status = "inconclusive"
        decided_by = "The t could not be computed (zero spread), so neither the confirm nor the reject rule is met."
    elif t_val >= 2 and sup_pass:
        status = "confirmed"
        decided_by = "Main-measure t is 2 or more with at least 30 cases and the supporting check is above 0."
    elif t_val >= 2:
        status = "inconclusive"
        decided_by = "A t of 2 or more with a failed supporting check is inconclusive."
    elif t_val <= -2:
        status = "rejected"
        decided_by = "Main-measure t is -2 or less with at least 30 cases: the weighted short cases rose more than the coin's drift."
    else:
        status = "inconclusive"
        decided_by = "A t between -2 and 2 is inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "mean |forecast|/10-weighted short gain over coin drift, 5-bar grid cases with forecast <= -2",
            "value": mean_val,
            "statistic": {"name": "t of the mean", "value": t_val} if t_val is not None else None,
            "threshold": "t >= 2 confirms (with >= 30 cases and supporting check > 0); t <= -2 rejects (with >= 30 cases)",
        },
        "supporting_check": {
            "name": "mean excess fall of above-median |forecast| cases minus below-median cases",
            "value": sup_val,
            "passed": sup_pass,
        },
        "counts": {"cases": n_cases},
        "decided_by": decided_by,
        "reading": reading,
    }
