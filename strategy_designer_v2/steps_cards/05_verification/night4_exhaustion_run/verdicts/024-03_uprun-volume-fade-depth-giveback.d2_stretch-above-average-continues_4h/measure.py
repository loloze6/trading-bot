import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 18
    RAW = "debug_info.components.dist_ma30d.last_history_value"

    # ---------- 1. Situation check: close above its 180-bar SMA, long side ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            # where the component is not recorded, recompute from prices inside the window
            close = pd.to_numeric(df["close"], errors="coerce")
            sma = close.rolling(180, min_periods=180).mean()
            recomputed = (close / sma - 1.0) * 100.0
            raw = raw.where(raw.notna(), recomputed)
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            n_agree += int((active & (raw > 0) & (fc > 0)).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.90)

    main_name = "t of OLS slope of excess 18-bar return on forecast (non-overlapping grid, pooled)"
    threshold = "confirm if t >= +2 (and positive-forecast cells' mean excess > 0); reject if t <= -2"
    sup_name = "mean excess 18-bar return of grid cells with forecast > 0"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of bars with a non-zero forecast are long bars with the close above its "
                           "180-bar average, so the config does not trade the plan's situation on its side."),
            "reading": "Situation taken as raw distance > 0 with a positive forecast; raw value recomputed from closes where not recorded.",
        }

    # ---------- 2. Criterion ----------
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            n = len(df)
            for t in range(0, n, H):
                if t + H >= n:
                    break
                c0, c1, f = close[t], close[t + H], fc[t]
                if not (np.isfinite(c0) and np.isfinite(c1) and np.isfinite(f)) or c0 == 0:
                    continue
                rows.append((coin, c1 / c0 - 1.0, f))

    g = pd.DataFrame(rows, columns=["coin", "ret", "fc"])
    n_cells = int(len(g))
    if n_cells > 0:
        g["excess"] = g["ret"] - g.groupby("coin")["ret"].transform("mean")
    pos = g[g["fc"] > 0] if n_cells > 0 else g
    n_pos = int(len(pos))

    slope = None
    tval = None
    if n_cells >= 3 and np.nanstd(g["fc"].values) > 0:
        res = stats.linregress(g["fc"].values, g["excess"].values)
        slope = float(res.slope)
        tval = float(res.slope / res.stderr) if res.stderr > 0 else None

    sup_val = float(pos["excess"].mean()) if n_pos > 0 else None
    sup_pass = bool(sup_val is not None and sup_val > 0) if sup_val is not None else None

    counts = {"grid cells": n_cells, "grid cells with forecast > 0": n_pos}

    if n_pos < 200:
        status = "not observable"
        decided = f"Only {n_pos} grid cells have forecast > 0, below the plan's minimum of 200."
    elif tval is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed."
    elif tval >= 2 and sup_pass:
        status = "confirmed"
        decided = "The slope's t is +2 or more and the positive-forecast cells' mean excess return is above 0."
    elif tval <= -2:
        status = "rejected"
        decided = "The slope's t is -2 or less."
    elif tval >= 2:
        status = "inconclusive"
        decided = "The slope's t is +2 or more but the positive-forecast cells' mean excess return is not above 0."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and +2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": tval,
            "statistic": {"name": "OLS slope t", "value": tval} if tval is not None else None,
            "threshold": threshold,
        },
        "supporting_check": {"name": sup_name, "value": sup_val, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": ("Grid cells are rows 0, 18, 36, ... of each window with the forecast at the cell's bar; the coin's "
                    "mean 18-bar return is the mean over its grid cells pooled across all its windows; the plan's "
                    "'fewer than 200 positive cells' is reported as not observable."),
    }
