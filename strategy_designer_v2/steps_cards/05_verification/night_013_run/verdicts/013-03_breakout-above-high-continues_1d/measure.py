import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 30
    MIN_CASES = 30
    RAW = "debug_info.components.break_dist.last_history_value"

    # ---------- 1. Situation check: close above prior 365-bar high (raw distance > 0), long side ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0 or "forecast" not in df.columns:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            raw = pd.to_numeric(df[RAW], errors="coerce") if RAW in df.columns else pd.Series(np.nan, index=df.index)
            active = fc.notna() & (fc != 0) & raw.notna()
            n_active += int(active.sum())
            n_agree += int((active & (raw > 0) & (fc > 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.90

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {
                "name": "OLS slope of 30-bar excess return on forecast (forecast > 0 grid bars)",
                "value": None, "statistic": None,
                "threshold": "slope t >= 2 confirms (with mean excess > 0), t <= -2 rejects, at least 30 cases",
            },
            "supporting_check": None,
            "counts": {"active_bars": n_active},
            "decided_by": ("Fewer than 90% of bars with a non-zero forecast are bars where the close is above the "
                           "prior 365-bar high with a positive (long) forecast; "
                           + ("no active bars were found." if n_active == 0 else
                              f"agreement is {agreement:.3f}.")),
            "reading": "Situation taken as the recorded raw distance above the prior 365-bar high being > 0; active bars with a missing raw value were left out.",
        }

    # ---------- 2. Criterion ----------
    xs, ys = [], []
    for coin, wins in bars.items():
        rows = []  # (forecast, fwd return) on all grid bars of this coin
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            n = len(df)
            for p in range(0, n, H):
                if p + H >= n:
                    break
                c0, c1 = close[p], close[p + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                rows.append((fc[p], c1 / c0 - 1.0))
        if not rows:
            continue
        arr = np.array(rows, dtype=float)
        coin_mean = float(np.nanmean(arr[:, 1]))
        sel = np.isfinite(arr[:, 0]) & (arr[:, 0] > 0)
        for f, r in arr[sel]:
            xs.append(f)
            ys.append(r - coin_mean)

    x = np.array(xs, dtype=float)
    y = np.array(ys, dtype=float)
    n_cases = int(len(x))

    slope = None
    t_stat = None
    if n_cases >= 3 and np.var(x) > 0:
        res = stats.linregress(x, y)
        slope = float(res.slope)
        if res.stderr is not None and np.isfinite(res.stderr) and res.stderr > 0:
            t_stat = float(res.slope / res.stderr)
    mean_excess = float(np.mean(y)) if n_cases > 0 else None
    support_passed = (mean_excess > 0) if mean_excess is not None else None

    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"Only {n_cases} grid bars with forecast above 0, fewer than the plan's minimum of 30 cases."
    elif t_stat is None:
        status = "inconclusive"
        decided = "The slope t could not be computed (no spread in the forecast), so neither confirm nor reject rule is met."
    elif t_stat >= 2 and support_passed:
        status = "confirmed"
        decided = "Slope t is 2 or more and the mean excess return on break bars is above 0, with at least 30 cases."
    elif t_stat <= -2:
        status = "rejected"
        decided = "Slope t is -2 or less, with at least 30 cases."
    elif t_stat >= 2:
        status = "inconclusive"
        decided = "Slope t is 2 or more but the mean excess return on break bars is 0 or less."
    else:
        status = "inconclusive"
        decided = "Slope t is between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "OLS slope of 30-bar excess return on forecast (forecast > 0 grid bars)",
            "value": slope,
            "statistic": {"name": "OLS slope t", "value": t_stat} if t_stat is not None else None,
            "threshold": "slope t >= 2 with mean excess > 0 confirms; t <= -2 rejects; at least 30 cases",
        },
        "supporting_check": {
            "name": "mean excess 30-bar return on break bars (minus coin's mean 30-bar return) > 0",
            "value": mean_excess,
            "passed": support_passed,
        },
        "counts": {"grid bars where the forecast is above 0": n_cases},
        "decided_by": decided,
        "reading": ("The coin's mean 30-bar return is the mean over all its windows' non-overlapping 30-bar grid "
                    "returns (positions 0, 30, 60, ... with a full 30 bars ahead), and the plan's fewer-than-30-cases "
                    "rule is reported as 'not observable' per the workflow's minimum-count rule."),
    }
