import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 48
    FC = "forecast"
    RAW = "debug_info.components.prior_rise.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            ts = pd.to_datetime(df["timestamp"], utc=True)
            close = df["close"].astype(float)
            fc = df[FC].astype(float).fillna(0.0)
            # Sunday's last close: bar starting Sunday 23:00 UTC (closes at Monday 00:00)
            is_sun_close = ((ts.dt.dayofweek == 6) & (ts.dt.hour == 23)).values
            wkend_ret = (close / close.shift(H) - 1.0).values
            prior_px = (close.shift(H) / close.shift(H + 120) - 1.0).values
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce").values
                prior = np.where(np.isnan(raw), prior_px, raw)
            else:
                prior = prior_px
            with np.errstate(invalid="ignore"):
                sit = is_sun_close & (wkend_ret < 0) & (prior > 0)
            active = (fc != 0).values
            n_active += int(active.sum())
            n_agree += int((active & sit & (fc.values < 0)).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)
    main_name = "mean short-side unusual 48-bar move per Sunday-close case"
    threshold = "mean > 0 with t >= 2 confirms (with slope > 0); t <= -2 rejects; at least 100 cases"
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"cases": 0, "active_bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are short bets at Sunday's last close "
                           "after a falling weekend and a rising prior five days" if n_active > 0 else
                           "The record has no bar with a non-zero forecast, so the config never takes the plan's situation"),
            "reading": "Sunday's last close is the bar starting Sunday 23:00 UTC; returns are counted in bar positions inside each window.",
        }

    # ---------- 2. criterion ----------
    unusual = []
    absfc = []
    for coin, wins in bars.items():
        # coin's normal 48-bar drift: non-overlapping grid of all its windows
        grid_rets = []
        for w, df in wins.items():
            c = df["close"].astype(float).values
            idx = np.arange(0, len(c) - H, H)
            if len(idx):
                r = c[idx + H] / c[idx] - 1.0
                grid_rets.extend(r[np.isfinite(r)].tolist())
        if not grid_rets:
            continue
        drift = float(np.mean(grid_rets))
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float).values
            fc = df[FC].astype(float).fillna(0.0).values
            seen_cells = set()
            for i in np.where(fc <= -2)[0]:
                cell = i // H
                if cell in seen_cells:
                    continue
                if i + H >= len(c):
                    continue
                r = c[i + H] / c[i] - 1.0
                if not np.isfinite(r):
                    continue
                seen_cells.add(cell)
                unusual.append(-(r - drift))
                absfc.append(abs(fc[i]))

    unusual = np.array(unusual, dtype=float)
    absfc = np.array(absfc, dtype=float)
    n = int(len(unusual))
    mean = float(unusual.mean()) if n > 0 else None
    t = None
    if n > 1:
        sd = unusual.std(ddof=1)
        t = float(mean / (sd / np.sqrt(n))) if sd > 0 else None
    slope = None
    if n > 2 and np.ptp(absfc) > 0:
        slope = float(stats.linregress(absfc, unusual).slope)
    slope_pass = None if slope is None else bool(slope > 0)

    if n < 100:
        status = "not observable"
        decided = f"Only {n} cases across all coins and windows, fewer than the plan's minimum of 100."
    elif t is not None and t >= 2 and mean > 0 and slope_pass:
        status = "confirmed"
        decided = "The mean short-side unusual move is above 0 with t >= 2 and the supporting slope is above 0."
    elif t is not None and t <= -2:
        status = "rejected"
        decided = "The mean short-side unusual move has t <= -2: after such weekends the coin rises more than its normal drift."
    elif t is not None and t >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the supporting slope is at or below 0 (or undefined), which the plan calls inconclusive."
    else:
        status = "inconclusive"
        decided = "The t of the mean short-side unusual move lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": mean,
                         "statistic": None if t is None else {"name": "t of the mean", "value": t},
                         "threshold": threshold},
        "supporting_check": {"name": "slope of short-side unusual move on |forecast|",
                             "value": slope, "passed": slope_pass},
        "counts": {"cases": n},
        "decided_by": decided,
        "reading": ("A case is every bar with forecast <= -2, at most one per 48-bar grid cell of its window, with its "
                    "48-bar return taken in bar positions inside the window; the drift is the coin's mean "
                    "non-overlapping 48-bar return over all its windows; Sunday's last close is the bar starting "
                    "Sunday 23:00 UTC; fewer than 100 cases is reported as not observable."),
    }
