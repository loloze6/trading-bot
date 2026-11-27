import numpy as np
import pandas as pd


def measure(bars):
    H = 3
    BAND = 2.0
    MIN_DAYS = 30
    RAW_COL = "debug_info.components.scaled_fall.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = d["close"].astype(float).values
            fc = d["forecast"].astype(float).values
            regime = d["regime"].astype(str).values
            raw = d[RAW_COL].astype(float).values if RAW_COL in d.columns else np.full(len(d), np.nan)
            n = len(d)
            ret7 = np.full(n, np.nan)
            if n > 7:
                ret7[7:] = close[7:] / close[:-7] - 1.0
            for i in range(n):
                f = fc[i]
                if not np.isfinite(f) or f == 0:
                    continue
                n_active += 1
                if np.isfinite(ret7[i]):
                    fell = ret7[i] < 0
                elif np.isfinite(raw[i]):
                    fell = raw[i] < 0
                else:
                    fell = False
                in_profile = regime[i] == "trending"
                if fell and in_profile and f < 0:
                    n_agree += 1

    reading = ("Situation = 7-day close-to-close return below 0 inside the window (the raw scaled_fall sign where the 7 "
               "prior bars are not in the window) on bars whose regime is 'trending' (the profile vetoes give 'chop'), "
               "side short; cases are short-side bets of >= 2 forecast points, the first one per 3-bar grid cell from each "
               "window's first row; the mean unusual move is the mean over cases and its t is over per-day summed "
               "deviations; the median split puts |forecast| above the median in the larger half, the rest in the smaller.")

    if n_active == 0:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None, "passed": False},
            "main_measure": {"name": "mean unusual 3-bar move in the short direction", "value": None,
                             "statistic": None, "threshold": "mean > 0 with t >= 2 to confirm; mean < 0 with t <= -2 to reject"},
            "supporting_check": None,
            "counts": {"distinct case days": 0},
            "decided_by": "No active bars: fewer than 30 distinct case days.",
            "reading": reading,
        }

    agreement = n_agree / n_active
    if agreement < 0.9:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the active bars are short bars of the plan's situation (7-day fall in the "
                           "falling calm profile): the config's forecast does not follow the Fidelity's situation/side."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    cases = []  # (coin, timestamp, ret, absf)
    drift = {}
    for coin, wins in bars.items():
        grid_rets = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = d["close"].astype(float).values
            n = len(d)
            for p in range(0, n - H, H):
                r = close[p + H] / close[p] - 1.0
                if np.isfinite(r):
                    grid_rets.append(r)
        drift[coin] = float(np.mean(grid_rets)) if grid_rets else np.nan

        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = d["close"].astype(float).values
            fc = d["forecast"].astype(float).values
            ts = pd.to_datetime(d["timestamp"], utc=True)
            n = len(d)
            ref = 0.0
            bets = np.zeros(n, dtype=bool)
            for i in range(n):
                f = fc[i]
                if not np.isfinite(f) or f >= 0:
                    ref = 0.0
                    continue
                m = -f
                if m - ref >= BAND:
                    bets[i] = True
                    ref = m
                else:
                    ref = min(ref, m)
            seen_cells = set()
            for i in range(n):
                if not bets[i]:
                    continue
                cell = i // H
                if cell in seen_cells:
                    continue
                seen_cells.add(cell)
                if i + H >= n:
                    continue
                r = close[i + H] / close[i] - 1.0
                if not np.isfinite(r) or not np.isfinite(drift[coin]):
                    continue
                cases.append((coin, ts.iloc[i].normalize(), -(r - drift[coin]), abs(fc[i])))

    n_cases = len(cases)
    if n_cases:
        cdf = pd.DataFrame(cases, columns=["coin", "day", "dev", "absf"])
        day_sums = cdf.groupby("day")["dev"].sum().values
        n_days = int(len(day_sums))
        mean_dev = float(cdf["dev"].mean())
    else:
        cdf = None
        day_sums = np.array([])
        n_days = 0
        mean_dev = None

    t = None
    if n_days >= 2:
        sd = np.std(day_sums, ddof=1)
        if sd > 0:
            t = float(np.mean(day_sums) / (sd / np.sqrt(n_days)))

    sup_val = None
    sup_pass = None
    if cdf is not None and n_cases >= 2:
        med = cdf["absf"].median()
        big = cdf.loc[cdf["absf"] > med, "dev"]
        small = cdf.loc[cdf["absf"] <= med, "dev"]
        if len(big) and len(small):
            sup_val = float(big.mean() - small.mean())
            sup_pass = bool(sup_val > 0)
        else:
            sup_pass = False

    counts = {"distinct case days": n_days, "cases": int(n_cases)}
    main = {"name": "mean unusual 3-bar move in the short direction",
            "value": mean_dev,
            "statistic": {"name": "t of the mean (per-day summed deviations)", "value": t} if t is not None else None,
            "threshold": "mean > 0 with t >= 2 to confirm; mean < 0 with t <= -2 to reject"}
    sup = {"name": "mean unusual move, larger-|forecast| half minus smaller half", "value": sup_val, "passed": sup_pass}

    if n_days < MIN_DAYS:
        status = "not observable"
        decided = f"Only {n_days} distinct case days, fewer than the plan's minimum of 30."
    elif t is None:
        status = "inconclusive"
        decided = "The t of the mean unusual move cannot be computed (no dispersion), so no confirm or reject rule is met."
    elif mean_dev > 0 and t >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "Mean unusual move > 0 with t >= 2 over at least 30 case days, and the larger-forecast half beats the smaller."
        else:
            status = "inconclusive"
            decided = "Confirm-level main measure, but the supporting check (larger minus smaller half > 0) fails."
    elif mean_dev < 0 and t <= -2:
        status = "rejected"
        decided = "Mean unusual move < 0 with t <= -2 over at least 30 case days: a reversal against the short."
    else:
        status = "inconclusive"
        decided = "The t of the mean unusual move lies between -2 and 2 (or its sign disagrees with the mean)."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": main,
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
