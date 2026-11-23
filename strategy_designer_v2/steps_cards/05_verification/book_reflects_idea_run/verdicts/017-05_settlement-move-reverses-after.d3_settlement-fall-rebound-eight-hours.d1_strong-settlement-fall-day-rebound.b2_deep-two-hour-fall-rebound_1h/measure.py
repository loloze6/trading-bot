import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 24
    RAW = "debug_info.components.fall2h.last_history_value"
    PPV = "debug_info.components.fall2h.post_pipeline_value"

    # ---------- 1. Situation check: a negative 2-hour return, long side ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float)
            ret2 = close / close.shift(2) - 1.0
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
                raw = raw.where(raw.notna(), ret2)
            else:
                raw = ret2
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            n_agree += int((active & (raw < 0) & (fc > 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.90)

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": "OLS slope of excess 24-bar return on forecast",
                             "value": None, "statistic": None,
                             "threshold": "slope > 0 with t >= 2 confirms; slope < 0 with t <= -2 rejects"},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars after a "
                           "negative 2-hour return, as the plan's situation requires."),
            "reading": "The situation is a negative raw 2-bar scaled return (last_history_value < 0) with a positive forecast.",
        }

    # ---------- 2. Criterion ----------
    xs, ys = [], []
    for coin, wins in bars.items():
        # normal drift: mean 24-bar return over all non-overlapping grid bars of all the coin's windows
        all_fwd = []
        cases = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float).values
            n = len(df)
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            if PPV in df.columns:
                x = pd.to_numeric(df[PPV], errors="coerce").values
            else:
                x = np.full(n, np.nan)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 <= 0:
                    continue
                r = c1 / c0 - 1.0
                all_fwd.append(r)
                if np.isfinite(fc[i]) and fc[i] > 0:
                    xv = x[i] if np.isfinite(x[i]) else np.nan
                    if np.isfinite(xv):
                        cases.append((xv, r))
        if len(all_fwd) == 0:
            continue
        drift = float(np.mean(all_fwd))
        for xv, r in cases:
            xs.append(float(xv))
            ys.append(float(r - drift))

    xs = np.asarray(xs, dtype=float)
    ys = np.asarray(ys, dtype=float)
    n_cases = int(len(xs))

    if n_cases > 0:
        q80 = float(np.quantile(xs, 0.8))
        top = xs >= q80
        n_top = int(top.sum())
    else:
        top = np.zeros(0, dtype=bool)
        n_top = 0

    slope = None
    tval = None
    if n_cases >= 3 and np.std(xs) > 0:
        lr = stats.linregress(xs, ys)
        slope = float(lr.slope)
        tval = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    top_mean = float(np.mean(ys[top])) if n_top > 0 else None
    sup_pass = (top_mean > 0) if top_mean is not None else None

    if n_cases < 300:
        status = "not observable"
        decided = f"Only {n_cases} pooled cases, below the plan's minimum of 300."
    elif n_top < 60:
        status = "not observable"
        decided = f"Only {n_top} cases in the top quintile, below the plan's minimum of 60."
    elif slope is None or tval is None:
        status = "inconclusive"
        decided = "The slope or its t could not be computed, so neither the confirm nor the reject rule is met."
    elif slope > 0 and tval >= 2 and sup_pass:
        status = "confirmed"
        decided = "The slope is positive with t >= 2 and the top-quintile mean excess return is above 0."
    elif slope < 0 and tval <= -2:
        status = "rejected"
        decided = "The slope is negative with t <= -2."
    elif slope > 0 and tval >= 2:
        status = "inconclusive"
        decided = "The slope has t >= 2 but the top-quintile mean excess return is at or below 0."
    else:
        status = "inconclusive"
        decided = "The slope t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "OLS slope of excess 24-bar return on forecast (post_pipeline_value)",
            "value": slope,
            "statistic": {"name": "OLS slope t", "value": tval} if tval is not None else None,
            "threshold": "slope > 0 with t >= 2 (and top-quintile mean > 0) confirms; slope < 0 with t <= -2 rejects",
        },
        "supporting_check": {
            "name": "top-quintile mean excess 24-bar return, long",
            "value": top_mean,
            "passed": None if sup_pass is None else bool(sup_pass),
        },
        "counts": {"cases pooled": n_cases, "cases in the top quintile": n_top},
        "decided_by": decided,
        "reading": ("The drift is each coin's mean 24-bar return over the non-overlapping grid of all its windows, "
                    "the top quintile is the cases with post_pipeline_value at or above the 80th percentile of the "
                    "pooled cases, and the plan's minimum counts, if missed, give 'not observable' as the workflow requires."),
    }
