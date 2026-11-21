import numpy as np
import pandas as pd


def measure(bars):
    H = 168
    LHV = "debug_info.components.ret_30d.last_history_value"

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            active = fc.notna() & (fc != 0)
            if not active.any():
                continue
            # year condition: the regime detector's decision on the 8760-bar return (> 0 -> "trending")
            regime_ok = df["regime"].astype(str) == "trending"
            if LHV in df.columns:
                r30 = pd.to_numeric(df[LHV], errors="coerce")
            else:
                r30 = pd.Series(np.nan, index=df.index)
            # fallback: recompute the 720-bar return from prices inside the window where not recorded
            close = pd.to_numeric(df["close"], errors="coerce")
            r30_px = close / close.shift(720) - 1.0
            r30 = r30.where(r30.notna(), r30_px)
            situ = regime_ok & (r30 > 0)
            side_ok = fc > 0
            n_active += int(active.sum())
            n_agree += int((active & situ & side_ok).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "mean unusual 168-bar move of grid bars with forecast > 0 (return minus coin's mean 168-bar return)"
    threshold = "confirm: mean > 0 with t >= 2 over >= 100 independent cases and supporting check > 0; reject: mean < 0 with t <= -2 over >= 100 cases"
    sup_name = "mean unusual move of upper half minus lower half, split at median forecast"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"independent cases": None, "active bars": n_active},
            "decided_by": ("No active bars: the forecast is never non-zero, so the plan's long side in the trending, positive-30-day-return situation cannot be compared."
                           if n_active == 0 else
                           f"Only {agreement:.3f} of active bars are long bars in the 'trending' regime (1-year return > 0) with a positive 720-bar return, below 0.90."),
            "reading": "The year condition is read from the recorded regime ('trending' = 8760-bar return > 0), since the detector's component is not recorded.",
        }

    # ---------- 2. Criterion ----------
    case_ret, case_fc, case_coin = [], [], []
    coin_means = {}
    for coin, wins in bars.items():
        all_rets = []
        coin_cases = []
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
                r = c1 / c0 - 1.0
                all_rets.append(r)
                if np.isfinite(fc[p]) and fc[p] > 0:
                    coin_cases.append((r, fc[p]))
        if len(all_rets) == 0:
            continue
        mu = float(np.mean(all_rets))
        coin_means[coin] = mu
        for r, f in coin_cases:
            case_ret.append(r - mu)
            case_fc.append(f)
            case_coin.append(coin)

    u = np.asarray(case_ret, dtype=float)
    f = np.asarray(case_fc, dtype=float)
    n_cases = int(len(u))

    mean_u = float(np.mean(u)) if n_cases > 0 else None
    t_u = None
    if n_cases > 1:
        sd = float(np.std(u, ddof=1))
        if sd > 0:
            t_u = float(mean_u / (sd / np.sqrt(n_cases)))

    sup_val = None
    n_up = n_lo = 0
    if n_cases > 0:
        med = float(np.median(f))
        up = f > med
        lo = ~up
        n_up, n_lo = int(up.sum()), int(lo.sum())
        if n_up > 0 and n_lo > 0:
            sup_val = float(np.mean(u[up]) - np.mean(u[lo]))
    sup_pass = None if sup_val is None else bool(sup_val > 0)

    counts = {"independent cases": n_cases, "upper half cases": n_up, "lower half cases": n_lo}

    if n_cases < 100:
        status = "not observable"
        decided = f"Fewer than 100 independent cases ({n_cases}), so the plan's minimum count is not reached."
    elif t_u is None:
        status = "inconclusive"
        decided = "The t-statistic cannot be computed (zero dispersion), which meets neither the confirm nor the reject rule."
    elif mean_u > 0 and t_u >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "Mean unusual move above 0 with t >= 2 over at least 100 independent cases, and the upper-minus-lower half difference is above 0."
        else:
            status = "inconclusive"
            decided = "t >= 2 but the supporting check (upper minus lower half) is not above 0, which the plan calls inconclusive."
    elif mean_u < 0 and t_u <= -2:
        status = "rejected"
        decided = "Mean unusual move below 0 with t <= -2 over at least 100 independent cases."
    else:
        status = "inconclusive"
        decided = "The t-statistic lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_u,
            "statistic": None if t_u is None else {"name": "t of the mean", "value": t_u},
            "threshold": threshold,
        },
        "supporting_check": {"name": sup_name, "value": sup_val, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": ("Cases are pooled over all coins, each coin's drift is the mean 168-bar return over its grid bars in all windows, "
                    "the upper half is forecast strictly above the median (ties go to the lower half), and the year condition "
                    "is read from the recorded 'trending' regime."),
    }
