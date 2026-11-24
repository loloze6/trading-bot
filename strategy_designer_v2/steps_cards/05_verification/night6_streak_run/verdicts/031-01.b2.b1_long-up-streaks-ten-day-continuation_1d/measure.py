import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 10
    RAW = "debug_info.components.up_streak.last_history_value"

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.sort_values("timestamp").reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            close = pd.to_numeric(df["close"], errors="coerce")
            up_close = (close.diff() > 0)
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
                situation = np.where(raw.notna(), raw > 0, up_close)
            else:
                situation = up_close.values
            situation = pd.Series(situation, index=df.index).astype(bool)
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc > 0)).sum())
    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9

    main_name = "slope of 10-day excess return (over coin drift) on forecast, pooled non-overlapping grid"
    threshold = "confirm: slope t >= 2 with top-fifth difference > 0; reject: slope t <= -2; otherwise inconclusive"
    sup_name = "mean excess return of top fifth of positive-forecast cases minus rest of positive-forecast cases"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": "Fewer than 90% of non-zero forecast bars are long bars on an up-close streak (raw up-streak component > 0), as the plan's Fidelity requires.",
            "reading": "Situation taken as raw up-streak value > 0 (or close above previous close where unrecorded), expected side long.",
        }

    # ---------- 2. Criterion ----------
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            n = len(df)
            for t in range(0, n - H, H):
                c0, c1 = close[t], close[t + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                rows.append((coin, c1 / c0 - 1.0, fc[t]))
    cases = pd.DataFrame(rows, columns=["coin", "ret", "fc"])
    if len(cases) > 0:
        drift = cases.groupby("coin")["ret"].mean()
        cases["ex"] = cases["ret"] - cases["coin"].map(drift)
    else:
        cases["ex"] = []
    reg = cases.dropna(subset=["ex", "fc"])

    slope = None
    t_slope = None
    if len(reg) >= 3 and np.std(reg["fc"].values) > 0:
        lr = stats.linregress(reg["fc"].values, reg["ex"].values)
        slope = float(lr.slope)
        t_slope = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    pos = reg[reg["fc"] > 0].copy()
    n_pos = int(len(pos))
    n_top = int(round(n_pos / 5.0))
    diff = None
    if n_pos > 0 and 0 < n_top < n_pos:
        pos = pos.sort_values("fc", ascending=False, kind="mergesort")
        top = pos.iloc[:n_top]["ex"]
        rest = pos.iloc[n_top:]["ex"]
        diff = float(top.mean() - rest.mean())
    sup_passed = None if diff is None else bool(diff > 0)

    counts = {
        "grid cases": int(len(reg)),
        "grid cases with forecast above 0": n_pos,
        "top fifth": n_top,
    }

    if n_pos < 300:
        status = "not observable"
        decided = f"Only {n_pos} grid cases with forecast above 0, below the plan's minimum of 300."
    elif n_top < 30:
        status = "not observable"
        decided = f"Only {n_top} cases in the top fifth, below the plan's minimum of 30."
    elif t_slope is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif t_slope >= 2 and sup_passed:
        status = "confirmed"
        decided = "Slope t is 2 or more and the top-fifth minus rest difference is above 0 (confirm rule)."
    elif t_slope <= -2:
        status = "rejected"
        decided = "Slope t is -2 or less: longer streaks are followed by lower returns than the coin's drift (reject rule)."
    elif t_slope >= 2:
        status = "inconclusive"
        decided = "Slope t is 2 or more but the top-fifth difference is at or below 0 (inconclusive rule)."
    else:
        status = "inconclusive"
        decided = "Slope t lies between -2 and 2 (inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": slope,
            "statistic": None if t_slope is None else {"name": "OLS slope t", "value": t_slope},
            "threshold": threshold,
        },
        "supporting_check": {"name": sup_name, "value": diff, "passed": sup_passed},
        "counts": counts,
        "decided_by": decided,
        "reading": "Drift is each coin's mean 10-bar return over its grid cases in all windows, the slope comes from an OLS with intercept on all grid cases, and the top fifth is the round(n/5) highest-forecast positive cases (ties kept in time order).",
    }
