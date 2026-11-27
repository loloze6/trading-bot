import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    BAND = 2.0
    MIN_CASES = 30
    BRK_COL = "debug_info.components.break.last_history_value"
    MOM_COL = "debug_info.components.rise30.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            close = pd.to_numeric(df["close"], errors="coerce").values
            brk = (pd.to_numeric(df[BRK_COL], errors="coerce").values
                   if BRK_COL in df.columns else np.full(len(df), np.nan))
            mom = (pd.to_numeric(df[MOM_COL], errors="coerce").values
                   if MOM_COL in df.columns else np.full(len(df), np.nan))
            # recompute the 30-day return from prices where it is not recorded (inside the window only)
            mom_px = np.full(len(df), np.nan)
            if len(df) > 30:
                mom_px[30:] = close[30:] / close[:-30] - 1.0
            mom_use = np.where(np.isnan(mom), mom_px, mom)
            active = f != 0
            situ = (np.nan_to_num(brk, nan=-np.inf) > 0) & (np.nan_to_num(mom_use, nan=-np.inf) > 0)
            ok = active & situ & (f > 0)
            n_active += int(active.sum())
            n_agree += int(ok.sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": "mean excess 5-bar return after long bets",
                             "value": None, "statistic": None,
                             "threshold": "t >= 2 (confirm) or t <= -2 (reject) over at least 30 cases"},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "cases": None},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars where the break "
                           "measure is above 0 and the 30-day return is above 0, as the plan's Fidelity requires."
                           if n_active > 0 else "The record has no bar with a non-zero forecast."),
            "reading": "The 30-day return is the recorded rise30 raw value, recomputed from closes inside the window where missing; a bar with no recorded break value is not counted as a situation bar.",
        }

    # ---------- 2. criterion ----------
    excess = []
    entry_fc = []
    for coin, wins in bars.items():
        # coin's mean 5-bar return over all its windows, non-overlapping grid
        grid_rets = []
        coin_cases = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            n = len(df)
            for p in range(0, n - H, H):
                r = close[p + H] / close[p] - 1.0
                if np.isfinite(r):
                    grid_rets.append(r)
            # long bets
            ref = 0.0
            bet = np.zeros(n, dtype=bool)
            for t in range(n):
                ft = f[t]
                if ft > 0:
                    if ft - ref >= BAND:
                        bet[t] = True
                        ref = ft
                    else:
                        ref = min(ref, ft)
                else:
                    ref = 0.0
            # once per 5-bar grid cell: the first bet in the cell
            for c0 in range(0, n, H):
                idx = np.where(bet[c0:min(c0 + H, n)])[0]
                if len(idx) == 0:
                    continue
                t = c0 + int(idx[0])
                if t + H >= n:
                    continue
                r = close[t + H] / close[t] - 1.0
                if np.isfinite(r):
                    coin_cases.append((r, float(f[t])))
        if len(grid_rets) == 0 or len(coin_cases) == 0:
            continue
        drift = float(np.mean(grid_rets))
        for r, fc in coin_cases:
            excess.append(r - drift)
            entry_fc.append(fc)

    excess = np.array(excess, dtype=float)
    entry_fc = np.array(entry_fc, dtype=float)
    n_cases = int(len(excess))

    mean_ex = float(np.mean(excess)) if n_cases > 0 else None
    t_stat = None
    if n_cases > 1:
        sd = float(np.std(excess, ddof=1))
        t_stat = float(mean_ex / (sd / np.sqrt(n_cases))) if sd > 0 else 0.0

    diff = None
    n_up = n_lo = 0
    if n_cases > 1:
        med = float(np.median(entry_fc))
        up = excess[entry_fc > med]
        lo = excess[entry_fc <= med]
        n_up, n_lo = int(len(up)), int(len(lo))
        if n_up > 0 and n_lo > 0:
            diff = float(np.mean(up) - np.mean(lo))
    sup_pass = (diff > 0) if diff is not None else None

    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"Only {n_cases} cases, fewer than the plan's minimum of 30 independent cases."
    elif mean_ex > 0 and t_stat is not None and t_stat >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "Mean excess return positive with t >= 2 over at least 30 cases, and the upper-half-minus-lower-half difference is above 0."
        else:
            status = "inconclusive"
            decided = "t >= 2 but the upper-half-minus-lower-half size check is not above 0."
    elif mean_ex < 0 and t_stat is not None and t_stat <= -2:
        status = "rejected"
        decided = "Mean excess return negative with t <= -2 over at least 30 cases."
    else:
        status = "inconclusive"
        decided = "The t-statistic lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": "mean excess 5-bar return after long bets (return minus coin's mean 5-bar return)",
                         "value": mean_ex,
                         "statistic": ({"name": "t of the mean", "value": t_stat} if t_stat is not None else None),
                         "threshold": "confirm: positive with t >= 2 over at least 30 cases; reject: negative with t <= -2 over at least 30 cases"},
        "supporting_check": {"name": "upper-half minus lower-half mean excess return (median split of entry forecast)",
                             "value": diff, "passed": sup_pass},
        "counts": {"cases": n_cases, "upper half cases": n_up, "lower half cases": n_lo},
        "decided_by": decided,
        "reading": ("A case is the first long bet (forecast rise >= 2 points from its lowest level since the last bet, from 0 after flat) "
                    "in each 5-bar grid cell counted from the window's first row, entered at that bar's close, with cases whose 5 bars run past "
                    "the window dropped; the coin's mean 5-bar return uses the same grid pooled over its windows; the median split puts ties "
                    "at the median in the lower half."),
    }
