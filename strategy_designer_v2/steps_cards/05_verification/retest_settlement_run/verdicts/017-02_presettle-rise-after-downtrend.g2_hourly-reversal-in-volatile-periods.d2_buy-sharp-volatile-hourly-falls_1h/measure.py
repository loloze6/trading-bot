import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 24
    BAND = 2.0
    MIN_CASES = 30
    RAW = "debug_info.components.scaled_fall.last_history_value"

    # ---------- 1. situation check: a falling hour (raw value < 0), long side ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            close = pd.to_numeric(df["close"], errors="coerce").values
            px_ret = np.full(len(close), np.nan)
            if len(close) > 1:
                px_ret[1:] = close[1:] / close[:-1] - 1.0
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce").values
            else:
                raw = np.full(len(df), np.nan)
            # raw value of the component; where it is not recorded, the hour's price return
            # (same sign: the return divided by a positive volatility mean)
            fall_val = np.where(np.isnan(raw), px_ret, raw)
            active = fc != 0
            situation = np.nan_to_num(fall_val, nan=0.0) < 0
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc > 0)).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "mean 24-bar excess return (minus the coin's normal drift) of the bets"
    threshold = "t >= 2 with at least 30 cases to confirm; t <= -2 with at least 30 cases to reject"
    reading = ("Situation bars are those whose raw scaled_fall value (or, where unrecorded, the hour's "
               "price return) is below 0 with a positive forecast; a bet is a forecast rise of at least 2 "
               "points above its lowest positive level since the last bet (from 0 after a flat), the first "
               "bet in each 24-bar grid cell from the window's first row counts, the drift is the coin's mean "
               "24-bar return on that grid over all its windows, and the median split puts cases strictly "
               "above the median entry forecast against those at or below it.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"cases": 0, "active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are falling hours with a long "
                           "forecast, so the config does not do what the plan's situation and side say."),
            "reading": reading,
        }

    # ---------- 2. coin drift: mean 24-bar return on the non-overlapping grid ----------
    drift = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").values
            for p in range(0, len(close) - H, H):
                r = close[p + H] / close[p] - 1.0
                if np.isfinite(r):
                    rets.append(r)
        drift[coin] = float(np.mean(rets)) if rets else np.nan

    # ---------- 3. cases: bets, once per 24-bar grid cell ----------
    excess = []
    entry_fc = []
    for coin, wins in bars.items():
        d = drift.get(coin, np.nan)
        if not np.isfinite(d):
            continue
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            close = pd.to_numeric(df["close"], errors="coerce").values
            n = len(fc)
            ref = 0.0
            used_cells = set()
            for t in range(n):
                f = fc[t]
                if f <= 0:
                    ref = 0.0
                    continue
                ref = min(ref, f)
                if f - ref >= BAND:
                    ref = f
                    cell = t // H
                    if cell in used_cells:
                        continue
                    used_cells.add(cell)
                    if t + H < n:
                        r = close[t + H] / close[t] - 1.0
                        if np.isfinite(r):
                            excess.append(r - d)
                            entry_fc.append(f)

    excess = np.asarray(excess, dtype=float)
    entry_fc = np.asarray(entry_fc, dtype=float)
    n_cases = int(len(excess))

    mean_ex = float(np.mean(excess)) if n_cases > 0 else None
    t_val = None
    if n_cases > 1:
        sd = float(np.std(excess, ddof=1))
        t_val = float(mean_ex / (sd / np.sqrt(n_cases))) if sd > 0 else None

    sup_val = None
    sup_pass = None
    n_hi = n_lo = 0
    if n_cases > 0:
        med = float(np.median(entry_fc))
        hi = excess[entry_fc > med]
        lo = excess[entry_fc <= med]
        n_hi, n_lo = int(len(hi)), int(len(lo))
        if n_hi > 0 and n_lo > 0:
            sup_val = float(np.mean(hi) - np.mean(lo))
            sup_pass = bool(sup_val > 0)

    # ---------- 4. decision ----------
    if n_cases < MIN_CASES:
        status = "not observable"
        decided_by = f"Only {n_cases} cases, fewer than the plan's minimum of 30."
    elif t_val is None:
        status = "inconclusive"
        decided_by = "The t of the mean could not be computed (no spread in the excess returns)."
    elif t_val >= 2:
        if sup_pass:
            status = "confirmed"
            decided_by = "The main t is 2 or more with at least 30 cases and the high-minus-low forecast difference is above 0."
        else:
            status = "inconclusive"
            decided_by = "The main t is 2 or more but the supporting check is at or below 0 (or not computable), which the plan calls inconclusive."
    elif t_val <= -2:
        status = "rejected"
        decided_by = "The main t is -2 or less with at least 30 cases."
    else:
        status = "inconclusive"
        decided_by = "The main t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_ex,
            "statistic": ({"name": "t of the mean", "value": t_val} if t_val is not None else None),
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "mean excess above median entry forecast minus below",
            "value": sup_val,
            "passed": sup_pass,
        },
        "counts": {"cases": n_cases, "cases above median": n_hi, "cases at or below median": n_lo},
        "decided_by": decided_by,
        "reading": reading,
    }
