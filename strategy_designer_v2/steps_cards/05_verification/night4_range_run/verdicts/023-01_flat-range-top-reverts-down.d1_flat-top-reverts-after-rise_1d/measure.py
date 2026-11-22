import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    RAW = "debug_info.components.flat_range_top.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)

            # 90-bar return condition: recomputed from closes where 90 past bars
            # exist inside the window, otherwise the detector's recorded decision.
            ret90 = close / close.shift(90) - 1.0
            regime_mr = df["regime"].astype(str) == "mean_reversion"
            cond90 = pd.Series(np.where(ret90.notna(), ret90 >= 0.0, regime_mr), index=df.index)

            # Graded range position x flatness: raw value when recorded,
            # otherwise recomputed from the 30-bar closing range.
            hi = close.rolling(30, min_periods=30).max()
            lo = close.rolling(30, min_periods=30).min()
            rng = hi - lo
            pos = (2.0 * (close - lo) / rng - 1.0).where(rng > 0)
            net = (close - close.shift(29)).abs()
            flat = (1.0 - net / rng).where(rng > 0)
            recomputed = pos * flat
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
                raw = raw.where(raw.notna(), recomputed)
            else:
                raw = recomputed
            above_mid = raw > 0

            situation = cond90 & above_mid
            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc < 0)).sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": ("Fewer than 90 % of the active bars are short bars with the close above the "
                           "middle of its 30-bar closing range while the 90-bar return is at or above 0"
                           if n_active > 0 else "No active bars: the forecast is never non-zero."),
            "reading": "The 90-bar return is recomputed from closes where 90 past bars exist in the window, "
                       "otherwise read from the recorded regime; 'above the middle' is the component's raw value above 0.",
        }

    # ---------- 2. criterion ----------
    case_ret, case_fc, case_coin = [], [], []
    drift = {}
    for coin, wins in bars.items():
        grid_rets = []
        coin_cases = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            n = len(df)
            for i in range(0, n - H, H):
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 <= 0:
                    continue
                r = c1 / c0 - 1.0
                grid_rets.append(r)
                if np.isfinite(fc[i]) and fc[i] <= -2:
                    coin_cases.append((r, fc[i]))
        drift[coin] = float(np.mean(grid_rets)) if grid_rets else np.nan
        for r, f in coin_cases:
            if np.isfinite(drift[coin]):
                case_ret.append(-(r - drift[coin]))
                case_fc.append(f)
                case_coin.append(coin)

    u = np.array(case_ret, dtype=float)
    f = np.array(case_fc, dtype=float)
    n_cases = int(len(u))

    mean_u = float(np.mean(u)) if n_cases > 0 else None
    t = None
    if n_cases > 1:
        sd = float(np.std(u, ddof=1))
        if sd > 0:
            t = float(mean_u / (sd / np.sqrt(n_cases)))

    diff = None
    check_passed = None
    n_strong = n_weak = 0
    if n_cases > 1:
        med = float(np.median(f))
        strong = f <= med
        weak = f > med
        n_strong, n_weak = int(strong.sum()), int(weak.sum())
        if n_strong > 0 and n_weak > 0:
            diff = float(u[strong].mean() - u[weak].mean())
            check_passed = bool(diff > 0)
        else:
            check_passed = False

    reading = ("Cases are the bars at positions 0, 5, 10, ... of each window with a 5-bar return inside the window "
               "and forecast <= -2; the drift is the coin's mean 5-bar return on that grid over all its windows; "
               "the stronger half is the cases with forecast at or below the median forecast, the weaker half those above it.")

    main = {
        "name": "mean unusual 5-bar move in the short direction",
        "value": mean_u,
        "statistic": {"name": "t of the mean", "value": t} if t is not None else None,
        "threshold": "confirm: mean > 0 with t >= 2 over at least 30 cases; reject: mean < 0 with t <= -2 over at least 30 cases",
    }
    support = {"name": "stronger-half minus weaker-half mean unusual move", "value": diff, "passed": check_passed}
    counts = {"cases": n_cases, "stronger half": n_strong, "weaker half": n_weak}

    if n_cases < 30:
        status = "not observable"
        decided = f"Only {n_cases} cases with forecast -2 or lower on the 5-bar grid, below the plan's minimum of 30."
    elif t is None:
        status = "inconclusive"
        decided = "The t of the mean cannot be computed (zero dispersion), which meets neither the confirm nor the reject rule."
    elif mean_u > 0 and t >= 2 and check_passed:
        status = "confirmed"
        decided = "Mean unusual move positive with t >= 2 over at least 30 cases, and the stronger half shows the larger move."
    elif mean_u > 0 and t >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the stronger half does not show the larger move, which the plan calls inconclusive."
    elif mean_u < 0 and t <= -2:
        status = "rejected"
        decided = "Mean unusual move negative with t <= -2 over at least 30 cases."
    else:
        status = "inconclusive"
        decided = "t between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": passed},
        "main_measure": main,
        "supporting_check": support,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
