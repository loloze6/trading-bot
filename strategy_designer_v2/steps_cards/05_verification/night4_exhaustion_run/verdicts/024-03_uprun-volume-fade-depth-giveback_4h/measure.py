import numpy as np
import pandas as pd


def measure(bars):
    H = 18
    BAND = 2.0
    MIN_CASES = 30
    RG = "debug_info.components.run_gain.last_history_value"
    VF = "debug_info.components.vol_fade.last_history_value"

    def _num(df, col):
        if col in df.columns:
            return pd.to_numeric(df[col], errors="coerce").to_numpy(dtype=float)
        return np.full(len(df), np.nan)

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.sort_values("timestamp").reset_index(drop=True)
            f = _num(df, "forecast")
            close = _num(df, "close")
            rg = _num(df, RG)
            prev = np.concatenate([[np.nan], close[:-1]])
            closed_up = np.where(np.isnan(prev), False, close > prev)
            in_streak = closed_up | (np.nan_to_num(rg, nan=0.0) > 0)
            active = np.nan_to_num(f, nan=0.0) != 0
            n_active += int(active.sum())
            n_agree += int((active & in_streak & (f < 0)).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "mean unusual 18-bar move in the short direction over the short bets"
    main_thr = "mean > 0 with t >= 2 over at least 30 cases to confirm; t <= -2 over at least 30 cases to reject"
    reading = ("The situation is a bar inside a current up-streak (the bar closed above the previous close, "
               "or run_gain's raw value is positive) with a short forecast; a case is the first short bet "
               "(forecast falling at least 2 points below its highest level on the short side since its last bet, "
               "from 0 after a flat or a side change) in each 18-bar grid cell of a window, with a full 18-bar "
               "return inside the window; the drift is the coin's mean 18-bar return on the grid of all its windows; "
               "the high-fade half is cases with vol_fade raw value above the median and the low-fade half those at "
               "or below it.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"cases": 0, "active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are short bars inside a current "
                           "up-streak, as the plan's Fidelity situation and side require."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    # coin drift over all windows (non-overlapping grid)
    drift = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = _num(df, "close")
            for i in range(0, len(close) - H, H):
                a, b = close[i], close[i + H]
                if np.isfinite(a) and np.isfinite(b) and a > 0:
                    rets.append(b / a - 1.0)
        drift[coin] = float(np.mean(rets)) if rets else np.nan

    cases_u = []
    cases_vf = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.sort_values("timestamp").reset_index(drop=True)
            f = np.nan_to_num(_num(df, "forecast"), nan=0.0)
            close = _num(df, "close")
            vf = _num(df, VF)
            n = len(df)
            bets = np.zeros(n, dtype=bool)
            ref = 0.0
            short_state = False
            for t in range(n):
                if f[t] < 0:
                    d = -f[t]
                    if not short_state:
                        ref = 0.0
                        short_state = True
                    if d - ref >= BAND - 1e-12:
                        bets[t] = True
                        ref = d
                    else:
                        ref = min(ref, d)
                else:
                    short_state = False
                    ref = 0.0
            seen = set()
            for t in np.where(bets)[0]:
                cell = t // H
                if cell in seen:
                    continue
                seen.add(cell)
                if t + H >= n:
                    continue
                a, b = close[t], close[t + H]
                if not (np.isfinite(a) and np.isfinite(b) and a > 0) or not np.isfinite(drift.get(coin, np.nan)):
                    continue
                r = b / a - 1.0
                cases_u.append(-(r - drift[coin]))
                cases_vf.append(vf[t])

    u = np.array(cases_u, dtype=float)
    vfa = np.array(cases_vf, dtype=float)
    n_cases = int(len(u))

    mean_u = float(np.mean(u)) if n_cases > 0 else None
    t_stat = None
    if n_cases > 1:
        sd = float(np.std(u, ddof=1))
        t_stat = float(mean_u / (sd / np.sqrt(n_cases))) if sd > 0 else None

    # supporting check
    diff = None
    n_high = n_low = 0
    ok = np.isfinite(vfa)
    if ok.sum() > 0:
        med = float(np.median(vfa[ok]))
        hi = ok & (vfa > med)
        lo = ok & (vfa <= med)
        n_high, n_low = int(hi.sum()), int(lo.sum())
        if n_high > 0 and n_low > 0:
            diff = float(np.mean(u[hi]) - np.mean(u[lo]))
    sup_passed = None if diff is None else bool(diff > 0)

    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"Only {n_cases} cases, below the plan's minimum of 30."
    elif t_stat is None:
        status = "inconclusive"
        decided = "The t of the mean could not be computed (no spread), so neither rule is met."
    elif mean_u > 0 and t_stat >= 2:
        if sup_passed:
            status = "confirmed"
            decided = ("The mean unusual fall is positive with t >= 2 over at least 30 cases and the "
                       "high-fade minus low-fade difference is above 0.")
        else:
            status = "inconclusive"
            decided = ("The main measure meets the confirm rule but the high-fade minus low-fade difference "
                       "is at or below 0 (or not computable).")
    elif t_stat <= -2:
        status = "rejected"
        decided = "The mean unusual move in the short direction has t <= -2 over at least 30 cases."
    else:
        status = "inconclusive"
        decided = "The t of the mean unusual fall lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_u,
            "statistic": None if t_stat is None else {"name": "t of the mean", "value": t_stat},
            "threshold": main_thr,
        },
        "supporting_check": {
            "name": "high-fade minus low-fade mean unusual fall (median split of vol_fade raw)",
            "value": diff,
            "passed": sup_passed,
        },
        "counts": {"cases": n_cases, "high-fade cases": n_high, "low-fade cases": n_low},
        "decided_by": decided,
        "reading": reading,
    }
