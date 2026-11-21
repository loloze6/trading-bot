import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 36
    BAND = 2.0
    BRK = "debug_info.components.break.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            close = pd.to_numeric(df["close"], errors="coerce").values
            high = pd.to_numeric(df["high"], errors="coerce").values
            n = len(df)
            # 42-bar return from prices, inside the window
            ret42 = np.full(n, np.nan)
            if n > 42:
                ret42[42:] = close[42:] / close[:-42] - 1.0
            regime = df["regime"].astype(str).values if "regime" in df.columns else np.array([""] * n)
            rising = np.where(np.isnan(ret42), regime == "trending", ret42 > 0)
            # breakout: recorded raw value, else recomputed from prices
            prior_hh = pd.Series(high).shift(1).rolling(12, min_periods=12).max().values
            brk_px = np.where(np.isnan(prior_hh), np.nan, (close > prior_hh).astype(float))
            if BRK in df.columns:
                raw = pd.to_numeric(df[BRK], errors="coerce").values
                brk = np.where(~np.isnan(raw), (raw > 0).astype(float), brk_px)
            else:
                brk = brk_px
            brk_ok = np.nan_to_num(brk, nan=0.0) > 0
            active = f != 0
            n_active += int(active.sum())
            n_agree += int((active & brk_ok & rising & (f > 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "mean unusual 36-bar move of long bets, before costs"
    thr = "confirm: mean > 0 with t >= 2 over >= 30 independent cases; reject: mean < 0 with t <= -2 over >= 30"
    reading = ("Situation = recorded break raw value > 0 (or close above the prior 12-bar high from prices) and 42-bar "
               "close return > 0 from prices (the regime 'trending' where the window's first 42 bars leave it "
               "uncomputable), long side; a case is the first long bet (forecast rise >= 2 points from its lowest long "
               "level since the last bet, from 0 after flat) in each 36-bar grid cell from each window's first row, "
               "pooled over all coins, with the coin's drift the mean of its grid 36-bar returns over all windows; the "
               "median split excludes cases equal to the median.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"independent cases": 0, "active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars of a close above the "
                           "prior 12-bar high while the 42-bar return is positive."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    unusual = []
    fc = []
    for coin, wins in bars.items():
        # drift: mean of non-overlapping 36-bar returns over all windows
        grid_rets = []
        for w, df in wins.items():
            c = pd.to_numeric(df["close"], errors="coerce").values
            for i in range(0, len(c) - H, H):
                r = c[i + H] / c[i] - 1.0
                if np.isfinite(r):
                    grid_rets.append(r)
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            c = pd.to_numeric(df["close"], errors="coerce").values
            n = len(df)
            bet = np.zeros(n, dtype=bool)
            low = 0.0
            for t in range(n):
                ft = f[t]
                if ft <= 0:
                    low = 0.0
                    continue
                if ft - low >= BAND:
                    bet[t] = True
                    low = ft
                else:
                    low = min(low, ft)
            for start in range(0, n, H):
                idx = np.where(bet[start:start + H])[0]
                if len(idx) == 0:
                    continue
                t = start + int(idx[0])
                if t + H >= n:
                    continue
                r = c[t + H] / c[t] - 1.0
                if not np.isfinite(r):
                    continue
                unusual.append(r - drift)
                fc.append(f[t])

    u = np.array(unusual, dtype=float)
    fcs = np.array(fc, dtype=float)
    ncase = int(len(u))
    mean_u = float(u.mean()) if ncase > 0 else None
    tval = None
    if ncase > 1:
        sd = u.std(ddof=1)
        tval = float(mean_u / (sd / np.sqrt(ncase))) if sd > 0 else None

    supp_val = None
    supp_pass = None
    if ncase > 0:
        med = np.median(fcs)
        a = u[fcs > med]
        b = u[fcs < med]
        if len(a) > 0 and len(b) > 0:
            supp_val = float(a.mean() - b.mean())
            supp_pass = bool(supp_val > 0)
        else:
            supp_pass = False

    if ncase < 30:
        status = "not observable"
        decided = f"Only {ncase} independent cases, below the plan's minimum of 30."
    elif tval is None:
        status = "inconclusive"
        decided = "The t of the mean could not be computed (zero dispersion), so neither rule is met."
    elif mean_u > 0 and tval >= 2:
        if supp_pass:
            status = "confirmed"
            decided = "Mean unusual move above 0 with t >= 2 over at least 30 cases, and the above-minus-below-median difference is above 0."
        else:
            status = "inconclusive"
            decided = "A confirming t whose supporting check fails neither confirms nor rejects."
    elif mean_u < 0 and tval <= -2:
        status = "rejected"
        decided = "Mean unusual move below 0 with t <= -2 over at least 30 independent cases."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2 (or its sign disagrees with the mean's), so neither rule is met."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": mean_u,
                         "statistic": ({"name": "ordinary t of the mean", "value": tval} if tval is not None else None),
                         "threshold": thr},
        "supporting_check": {"name": "mean unusual move above minus below forecast median",
                             "value": supp_val, "passed": supp_pass},
        "counts": {"independent cases": ncase},
        "decided_by": decided,
        "reading": reading,
    }
