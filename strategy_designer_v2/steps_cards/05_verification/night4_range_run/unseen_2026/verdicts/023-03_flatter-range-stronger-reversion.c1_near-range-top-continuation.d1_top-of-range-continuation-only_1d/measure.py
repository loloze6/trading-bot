import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 10
    RAW = "debug_info.components.range_top.last_history_value"

    # ---------- 1. Situation check ----------
    # Situation: the close is in the upper half of its 30-day closing range. Expected side: long.
    raws = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            if RAW in df.columns:
                raws.append(pd.to_numeric(df[RAW], errors="coerce").values)
    allraw = np.concatenate(raws) if raws else np.array([])
    allraw = allraw[np.isfinite(allraw)]
    if allraw.size == 0:
        mid = 0.0
    else:
        lo, hi = float(np.min(allraw)), float(np.max(allraw))
        if lo < 0:
            mid = 0.0          # centred scale, e.g. -1..1
        elif hi <= 1.0 + 1e-9:
            mid = 0.5          # 0..1 scale
        else:
            mid = 50.0         # 0..100 scale

    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            if RAW in df.columns:
                r = pd.to_numeric(df[RAW], errors="coerce").values
            else:
                r = np.full(len(df), np.nan)
            active = f != 0
            n_active += int(active.sum())
            situ = np.isfinite(r) & (r > mid)
            n_agree += int((active & situ & (f > 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars where the close "
                           "is in the upper half of its 30-day closing range (raw range position above its middle)."),
            "reading": ("The middle of the range is read on the raw component's own scale "
                        "(0 for a centred scale, 0.5 for 0..1)."),
        }

    # ---------- 2. Criterion ----------
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            close = pd.to_numeric(df["close"], errors="coerce").values
            f = pd.to_numeric(df["forecast"], errors="coerce").values
            n = len(df)
            for t in range(0, n, H):
                if t + H >= n:
                    continue
                c0, c1 = close[t], close[t + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                rows.append((coin, w, c1 / c0 - 1.0, f[t]))
    grid = pd.DataFrame(rows, columns=["coin", "window", "ret", "forecast"])

    if len(grid):
        drift = grid.groupby("coin")["ret"].mean()
        grid["excess"] = grid["ret"] - grid["coin"].map(drift)
        cells = grid[np.isfinite(grid["forecast"]) & (grid["forecast"] > 0) & np.isfinite(grid["excess"])]
    else:
        cells = grid
    n_cells = int(len(cells))

    slope = None
    tval = None
    wmean = None
    if n_cells >= 3:
        x = cells["forecast"].values.astype(float)
        y = cells["excess"].values.astype(float)
        if np.std(x) > 0:
            lr = stats.linregress(x, y)
            slope = float(lr.slope)
            if lr.stderr and lr.stderr > 0:
                tval = float(lr.slope / lr.stderr)
        if x.sum() > 0:
            wmean = float(np.sum(y * x) / np.sum(x))
    elif n_cells > 0:
        x = cells["forecast"].values.astype(float)
        y = cells["excess"].values.astype(float)
        if x.sum() > 0:
            wmean = float(np.sum(y * x) / np.sum(x))

    sup_pass = None if wmean is None else bool(wmean > 0)
    main = {
        "name": "t of the slope of 10-day excess return on forecast (non-overlapping grid, forecast > 0)",
        "value": tval,
        "statistic": {"name": "OLS slope t", "value": tval} if tval is not None else None,
        "threshold": "confirm if t >= 2 (with weighted mean excess > 0); reject if t <= -2",
    }
    supporting = {"name": "forecast-weighted mean excess 10-day return", "value": wmean, "passed": sup_pass}
    counts = {"grid cells with a forecast above 0": n_cells}
    reading = ("The normal drift is each coin's mean 10-day return over all non-overlapping grid cells of all its "
               "windows; the regression pools all coins and windows; the plan's '<100 cells is inconclusive' is "
               "applied as the minimum count, giving 'not observable'.")

    if n_cells < 100:
        status = "not observable"
        decided = f"Only {n_cells} grid cells have a forecast above 0, fewer than the plan's minimum of 100."
    elif tval is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif tval >= 2 and sup_pass:
        status = "confirmed"
        decided = "The slope's t is 2 or more and the weighted mean excess return is above 0."
    elif tval <= -2:
        status = "rejected"
        decided = "The slope's t is -2 or less."
    elif tval >= 2:
        status = "inconclusive"
        decided = "The slope's t is 2 or more but the weighted mean excess return is 0 or below."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": supporting,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
