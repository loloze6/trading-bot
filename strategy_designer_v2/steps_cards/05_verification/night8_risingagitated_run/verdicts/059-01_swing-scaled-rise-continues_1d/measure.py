import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    RAW = "debug_info.components.scaled_move.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            close = pd.to_numeric(df["close"], errors="coerce")
            # Fallback when the raw value is missing: the sign of the 20-day return
            # inside the window, which is the sign of the scaled move.
            ret20 = close / close.shift(20) - 1.0
            situ = raw.where(raw.notna(), ret20)
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            agree = active & situ.notna() & (situ != 0) & (np.sign(situ) == np.sign(fc))
            n_agree += int(agree.sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": "Fewer than 90% of the bars with a non-zero forecast have a forecast whose "
                          "sign is the sign of the 20-day swing-scaled move, as the Fidelity's "
                          "situation and side require.",
            "reading": "The situation is a non-zero swing-scaled 20-day move, from the recorded raw "
                       "value or else the 20-day price return; the expected side is its sign.",
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            n = len(df)
            for i in range(0, n - H, H):
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                rows.append((coin, c1 / c0 - 1.0, fc[i]))

    g = pd.DataFrame(rows, columns=["coin", "ret", "fc"])
    if len(g):
        # Normal drift: the coin's mean 5-bar return over all its windows (same grid).
        drift = g.groupby("coin")["ret"].transform("mean")
        g["excess"] = g["ret"] - drift
        g = g[np.isfinite(g["fc"]) & np.isfinite(g["excess"])]
    n_cases = int(len(g))

    slope = None
    tval = None
    if n_cases >= 3 and g["fc"].std() > 0:
        lr = stats.linregress(g["fc"].values, g["excess"].values)
        slope = float(lr.slope)
        tval = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    main = {
        "name": "OLS slope of 5-bar excess return on forecast",
        "value": slope,
        "statistic": {"name": "slope t", "value": tval} if tval is not None else None,
        "threshold": "confirm: slope > 0 with t >= 2; reject: slope < 0 with t <= -2; "
                     "at least 300 grid cases",
    }
    counts = {"grid cases": n_cases}

    if n_cases < 300:
        status = "not observable"
        decided = f"Only {n_cases} grid cases, below the plan's minimum of 300."
    elif slope is None or tval is None:
        status = "inconclusive"
        decided = "The slope or its t could not be computed, so neither rule is met."
    elif slope > 0 and tval >= 2:
        status = "confirmed"
        decided = "The slope is positive with t >= 2 over at least 300 grid cases."
    elif slope < 0 and tval <= -2:
        status = "rejected"
        decided = "The slope is negative with t <= -2 over at least 300 grid cases."
    else:
        status = "inconclusive"
        decided = "The t is between -2 and 2, so the result neither confirms nor rejects."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": None,
        "counts": counts,
        "decided_by": decided,
        "reading": "All grid bars count as cases, flat forecasts included. Positions 0, 5, 10, ... "
                   "of each window are used where a 5-bar-ahead close exists. The drift is each "
                   "coin's mean grid return over all its windows. The t is the ordinary OLS slope "
                   "t, and fewer than 300 cases is reported as not observable.",
    }
