import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 48
    BAND = 2.0
    MIN_CASES = 30
    RAW = "debug_info.components.drop24.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            ret24_px = close / close.shift(24) - 1.0
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
                raw = raw.where(raw.notna(), ret24_px)
            else:
                raw = ret24_px
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            # situation: a 24-bar fall (graded, any drop counts), expected side long
            agree = active & (raw < 0) & (fc > 0)
            n_agree += int(agree.sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = True if agreement is None else bool(agreement >= 0.9)
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"cases": None},
            "decided_by": "Fewer than 90% of the bars with a non-zero forecast are bars with a negative 24-bar "
                          "return and a long (positive) forecast, as the plan's situation and outcome require.",
            "reading": "The situation is read as any negative 24-bar return (graded threshold), on the long side.",
        }

    # ---------- 2. criterion ----------
    unusual_all = []
    fc_all = []
    for coin, wins in bars.items():
        # coin's normal 48-bar drift over all its windows (non-overlapping grid)
        grid_rets = []
        prepared = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float).values
            n = len(close)
            for p in range(0, n - H, H):
                if np.isfinite(close[p]) and np.isfinite(close[p + H]) and close[p] != 0:
                    grid_rets.append(close[p + H] / close[p] - 1.0)
            prepared.append(df)
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))

        for df in prepared:
            close = df["close"].astype(float).values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            n = len(close)
            # bet detection: long-side rise of >= BAND from the lowest level since the last bet
            trough = 0.0
            bets = []
            for i in range(n):
                f = fc[i]
                if not np.isfinite(f) or f <= 0:
                    trough = 0.0
                    continue
                trough = min(trough, f)
                if f - trough >= BAND:
                    bets.append(i)
                    trough = f
            # one case per 48-bar grid cell (the first bet of the cell)
            seen = set()
            for i in bets:
                cell = i // H
                if cell in seen:
                    continue
                seen.add(cell)
                if i + H >= n:
                    continue
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                unusual_all.append(r - drift)  # long direction
                fc_all.append(float(fc[i]))

    u = np.asarray(unusual_all, dtype=float)
    x = np.asarray(fc_all, dtype=float)
    n_cases = int(len(u))

    mean_u = float(np.mean(u)) if n_cases > 0 else None
    t_u = None
    if n_cases > 1:
        sd = float(np.std(u, ddof=1))
        t_u = float(mean_u / (sd / np.sqrt(n_cases))) if sd > 0 else None
    slope = None
    if n_cases > 2 and np.std(x) > 0:
        slope = float(stats.linregress(x, u).slope)

    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"Fewer than {MIN_CASES} cases ({n_cases}), the plan's minimum count, so the data cannot show the idea."
        sup_pass = None if slope is None else bool(slope > 0)
    else:
        sup_pass = None if slope is None else bool(slope > 0)
        if t_u is not None and mean_u > 0 and t_u >= 2:
            if sup_pass:
                status = "confirmed"
                decided = "Mean unusual move positive with t >= 2 over at least 30 cases, and the slope on the forecast is positive."
            else:
                status = "inconclusive"
                decided = "Mean unusual move positive with t >= 2, but the slope on the forecast is not positive."
        elif t_u is not None and mean_u < 0 and t_u <= -2:
            status = "rejected"
            decided = "Mean unusual move negative with t <= -2 over at least 30 cases."
        else:
            status = "inconclusive"
            decided = "The t of the mean unusual move lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": bool(passed)},
        "main_measure": {
            "name": "mean unusual 48-bar move on cases, pooled over coins",
            "value": mean_u,
            "statistic": None if t_u is None else {"name": "t of the mean", "value": t_u},
            "threshold": "confirm: mean > 0 with t >= 2 over >= 30 cases and positive slope; reject: mean < 0 with t <= -2 over >= 30 cases",
        },
        "supporting_check": {
            "name": "OLS slope of unusual move on forecast at signal bar",
            "value": slope,
            "passed": sup_pass,
        },
        "counts": {"cases": n_cases},
        "decided_by": decided,
        "reading": "A case is the first long bet (forecast rise >= 2 from its lowest level since the last bet, reset to 0 when flat) in each cell of the window's 48-bar grid counted from its first row, with its 48-bar return inside the window; the drift is the coin's mean 48-bar return on that grid over all its windows; the situation is any negative 24-bar return on the long side.",
    }
