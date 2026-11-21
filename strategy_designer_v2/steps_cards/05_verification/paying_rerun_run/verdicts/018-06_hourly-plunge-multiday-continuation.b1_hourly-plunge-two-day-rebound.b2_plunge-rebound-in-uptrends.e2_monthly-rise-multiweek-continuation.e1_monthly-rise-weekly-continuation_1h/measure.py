import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 168
    RAW = "debug_info.components.ret30d.last_history_value"

    # ---------- 1. Situation check: raw 30-day return > 0, side long ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            close = pd.to_numeric(df["close"], errors="coerce")
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            # fallback inside the window only: 720-bar return from the prices
            fallback = close / close.shift(720) - 1.0
            raw = raw.where(raw.notna(), fallback)
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            agree = active & (raw > 0) & (fc > 0)
            n_agree += int(agree.sum())

    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are bars with a positive "
                           "720-bar return and a long forecast, so the config does not do what the "
                           "plan's situation (positive 30-day return, long) says."
                           if n_active > 0 else
                           "No bar has a non-zero forecast, so the plan's situation cannot be matched."),
            "reading": "none",
        }

    # ---------- 2. Criterion ----------
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) <= H:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            n = len(close)
            for p in range(0, n - H, H):
                c0, c1 = close[p], close[p + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 <= 0:
                    continue
                rows.append((coin, c1 / c0 - 1.0, fc[p]))

    grid = pd.DataFrame(rows, columns=["coin", "ret", "forecast"])
    if len(grid) > 0:
        stats_c = grid.groupby("coin")["ret"].agg(["mean", "std"])
        grid = grid.join(stats_c, on="coin")
        grid["strength"] = (grid["ret"] - grid["mean"]) / grid["std"]
        grid = grid[np.isfinite(grid["strength"]) & np.isfinite(grid["forecast"])]

    n_grid = int(len(grid))
    pos = grid[grid["forecast"] > 0] if n_grid else grid
    n_pos = int(len(pos))

    slope = None
    t_slope = None
    if n_grid >= 3 and grid["forecast"].nunique() > 1:
        lr = stats.linregress(grid["forecast"].to_numpy(), grid["strength"].to_numpy())
        slope = float(lr.slope)
        t_slope = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    mean_strength_pos = float(pos["strength"].mean()) if n_pos > 0 else None
    sup_passed = (mean_strength_pos > 0) if mean_strength_pos is not None else None

    counts = {"grid bars": n_grid, "grid bars with forecast > 0": n_pos}

    if n_pos < 300:
        status = "not observable"
        decided_by = (f"Only {n_pos} grid bars with forecast > 0, fewer than the plan's minimum of 300.")
    elif t_slope is None:
        status = "inconclusive"
        decided_by = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif t_slope >= 2 and sup_passed:
        status = "confirmed"
        decided_by = "The slope's t is 2 or more and the mean strength on forecast > 0 grid bars is above 0."
    elif t_slope <= -2:
        status = "rejected"
        decided_by = "The slope's t is -2 or less."
    elif t_slope >= 2:
        status = "inconclusive"
        decided_by = "The slope's t is 2 or more but the mean strength on forecast > 0 grid bars is at or below 0."
    else:
        status = "inconclusive"
        decided_by = "The slope's t is between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "slope of drift-adjusted 168-bar strength on forecast, all grid bars",
            "value": slope,
            "statistic": ({"name": "OLS slope t", "value": t_slope} if t_slope is not None else None),
            "threshold": "confirm if t >= 2 (with supporting check), reject if t <= -2",
        },
        "supporting_check": {
            "name": "mean strength on grid bars with forecast > 0 above 0",
            "value": mean_strength_pos,
            "passed": sup_passed,
        },
        "counts": counts,
        "decided_by": decided_by,
        "reading": ("The coin's normal drift and usual move are the mean and standard deviation of its forward "
                    "168-bar returns on the non-overlapping grid (positions 0, 168, ... of each window) pooled over "
                    "all its windows, grid bars without a full 168-bar forward return inside the window are dropped, "
                    "and the plan's '300 grid bars with forecast > 0' is treated as a minimum count giving "
                    "'not observable' when not reached."),
    }
