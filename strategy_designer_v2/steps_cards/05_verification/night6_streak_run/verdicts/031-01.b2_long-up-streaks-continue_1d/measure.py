import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 3
    RAW = "debug_info.components.up_streak_rel.last_history_value"

    # ---------- 1. Situation check: an up-close streak (raw > 0), expected side long ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            close = pd.to_numeric(df["close"], errors="coerce")
            up_close = close > close.shift(1)
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
                situation = np.where(raw.notna(), raw > 0, up_close)
            else:
                situation = up_close.values
            situation = pd.Series(situation, index=df.index).astype(bool)
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc > 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.90

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars on an up-close streak "
                           "(raw streak value > 0), as the plan's Fidelity requires"
                           if n_active > 0 else "The record has no bar with a non-zero forecast."),
            "reading": "The situation is a bar whose raw up-streak value is positive (closing up when the raw value is missing), on the long side.",
        }

    # ---------- 2. Non-overlapping 3-bar grid, per window ----------
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            n = len(df)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                rows.append((coin, w, c1 / c0 - 1.0, fc[i]))
    g = pd.DataFrame(rows, columns=["coin", "window", "ret", "forecast"])

    # Normal drift: coin's mean 3-bar return over all its windows' grid
    if len(g):
        g["drift"] = g.groupby("coin")["ret"].transform("mean")
        g["excess"] = g["ret"] - g["drift"]
    m = g.dropna(subset=["forecast", "excess"]) if len(g) else g

    n_pos = int((m["forecast"] > 0).sum()) if len(m) else 0
    n_grid = int(len(m))

    # OLS slope of excess return on forecast
    slope, t = None, None
    if n_grid >= 3:
        x = m["forecast"].values.astype(float)
        y = m["excess"].values.astype(float)
        xm = x - x.mean()
        sxx = float((xm ** 2).sum())
        if sxx > 0:
            b = float((xm * (y - y.mean())).sum() / sxx)
            a = y.mean() - b * x.mean()
            resid = y - a - b * x
            s2 = float((resid ** 2).sum() / (n_grid - 2))
            se = np.sqrt(s2 / sxx)
            slope = b
            t = float(b / se) if se > 0 else None

    # Supporting check: forecast >= 10, mean excess > 0
    hi = m[m["forecast"] >= 10] if len(m) else m
    n_hi = int(len(hi))
    sup_val = float(hi["excess"].mean()) if n_hi > 0 else None
    sup_pass = (sup_val > 0) if sup_val is not None else False

    counts = {
        "grid bars with forecast > 0": n_pos,
        "grid bars (all, in the regression)": n_grid,
        "grid bars with forecast >= 10": n_hi,
    }

    # ---------- 3. Decide ----------
    if n_pos < 300:
        status = "not observable"
        decided_by = f"Only {n_pos} grid bars with forecast > 0, below the plan's minimum of 300."
    elif slope is None or t is None:
        status = "inconclusive"
        decided_by = "The slope or its t could not be computed."
    elif slope > 0 and t >= 2 and sup_pass:
        status = "confirmed"
        decided_by = "The slope is positive with t >= 2 and the mean excess 3-bar return on grid bars with forecast >= 10 is above 0."
    elif slope < 0 and t <= -2:
        status = "rejected"
        decided_by = "The slope is negative with t <= -2."
    elif slope > 0 and t >= 2:
        status = "inconclusive"
        decided_by = "The slope is positive with t >= 2 but the supporting check fails."
    else:
        status = "inconclusive"
        decided_by = "The slope has |t| < 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "OLS slope of 3-bar forward return minus coin's normal drift on forecast, pooled non-overlapping grid",
            "value": slope,
            "statistic": {"name": "OLS slope t", "value": t} if t is not None else None,
            "threshold": "confirm: slope > 0 with t >= 2 and check passes; reject: slope < 0 with t <= -2; else inconclusive; at least 300 grid bars with forecast > 0",
        },
        "supporting_check": {
            "name": "mean 3-bar return minus normal drift on grid bars with forecast >= 10, above 0",
            "value": sup_val,
            "passed": bool(sup_pass),
        },
        "counts": counts,
        "decided_by": decided_by,
        "reading": ("The slope is an ordinary least-squares regression with intercept of the excess return on the forecast over all "
                    "pooled grid bars (forecast 0 included), the normal drift is each coin's mean 3-bar grid return over all its windows, "
                    "a supporting check with no grid bar at forecast >= 10 counts as failed, and the plan's minimum of 300 yields "
                    "'not observable' as the workflow requires."),
    }
