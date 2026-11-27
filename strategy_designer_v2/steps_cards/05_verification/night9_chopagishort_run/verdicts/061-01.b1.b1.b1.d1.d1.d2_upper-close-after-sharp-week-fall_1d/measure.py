import numpy as np
import pandas as pd


def measure(bars):
    H = 3
    BAND = 2.0
    LOC_MIN = 0.5
    FALL_MAX = -1.0
    MIN_DAYS = 30
    RAW = "debug_info.components.fall_depth.last_history_value"

    def fall5_from_prices(close):
        # fallback only: 5-bar return over (20-bar std of 1-bar returns * sqrt(5))
        r1 = close.pct_change()
        r5 = close / close.shift(5) - 1.0
        vol = r1.rolling(20, min_periods=20).std(ddof=1) * np.sqrt(5)
        return r5 / vol.replace(0, np.nan)

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            f = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0)
            hi = pd.to_numeric(d["high"], errors="coerce")
            lo = pd.to_numeric(d["low"], errors="coerce")
            cl = pd.to_numeric(d["close"], errors="coerce")
            rng = (hi - lo).replace(0, np.nan)
            loc = (cl - lo) / rng
            if RAW in d.columns:
                fall = pd.to_numeric(d[RAW], errors="coerce")
            else:
                fall = pd.Series(np.nan, index=d.index)
            fb = fall5_from_prices(cl)
            fall = fall.where(fall.notna(), fb)
            active = f != 0
            sit = (loc >= LOC_MIN - 1e-12) & (fall <= FALL_MAX + 1e-12) & (f < 0)
            n_active += int(active.sum())
            n_agree += int((active & sit.fillna(False)).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "mean short-direction 3-bar return minus the coin's normal 3-bar drift"
    main_thr = "mean > 0 with day-pooled t >= 2 confirms; mean < 0 with t <= -2 rejects"
    sup_name = "excess return of cases with |forecast| above median minus below median"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "agreeing bars": int(n_agree)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are short bars with a close location "
                           ">= 0.5 and a 5-day scaled return <= -1, the plan's situation and side."),
            "reading": "Close location is (close-low)/(high-low) from prices; the 5-day scaled return is the recorded fall_depth raw value (same component as the detector's fall5), recomputed from prices only where missing.",
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin, wins in bars.items():
        # normal drift: mean of non-overlapping 3-bar returns over all windows of the coin
        grid_rets = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(float)
            for i in range(0, len(c) - H, H):
                if np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] > 0:
                    grid_rets.append(c[i + H] / c[i] - 1.0)
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))

        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            f = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0).to_numpy(float)
            c = pd.to_numeric(d["close"], errors="coerce").to_numpy(float)
            ts = pd.to_datetime(d["timestamp"], utc=True, errors="coerce")
            n = len(d)
            # bets on the short side
            is_bet = np.zeros(n, dtype=bool)
            ref = 0.0
            for i in range(n):
                if f[i] < 0:
                    mag = -f[i]
                    if mag - ref >= BAND - 1e-12:
                        is_bet[i] = True
                        ref = mag
                    else:
                        ref = min(ref, mag)
                else:
                    ref = 0.0
            # first bet in each non-overlapping 3-bar grid cell
            for start in range(0, n, H):
                idx = [i for i in range(start, min(start + H, n)) if is_bet[i]]
                if not idx:
                    continue
                i = idx[0]
                if i + H >= n:
                    continue
                if not (np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] > 0):
                    continue
                r = c[i + H] / c[i] - 1.0
                ex = -(r - drift)
                if pd.isna(ts.iloc[i]):
                    continue
                rows.append({"coin": coin, "day": ts.iloc[i].strftime("%Y-%m-%d"),
                             "ex": ex, "absf": abs(f[i])})

    cases = pd.DataFrame(rows, columns=["coin", "day", "ex", "absf"])
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0

    mean_ex = float(cases["ex"].mean()) if n_cases else None
    t_val = None
    if n_cases >= 2 and n_days >= 2:
        dev = cases["ex"] - mean_ex
        s = dev.groupby(cases["day"]).sum().to_numpy(float)
        D = len(s)
        var = (D / (D - 1.0)) * np.sum(s ** 2) / (n_cases ** 2)
        se = np.sqrt(var)
        t_val = float(mean_ex / se) if se > 0 else None

    sup_val, sup_pass = None, None
    n_above = n_below = 0
    if n_cases:
        med = cases["absf"].median()
        above = cases.loc[cases["absf"] > med, "ex"]
        below = cases.loc[cases["absf"] < med, "ex"]
        n_above, n_below = int(len(above)), int(len(below))
        if n_above and n_below:
            sup_val = float(above.mean() - below.mean())
            sup_pass = bool(sup_val > 0)
        else:
            sup_pass = False

    counts = {"cases": n_cases, "cases on distinct days": n_days,
              "cases above median |forecast|": n_above, "cases below median |forecast|": n_below}

    if n_days < MIN_DAYS:
        status = "not observable"
        decided = f"Only {n_days} distinct case days, fewer than the plan's minimum of 30 cases on distinct days."
    elif t_val is None:
        status = "inconclusive"
        decided = "The day-pooled t could not be computed, so neither the confirm nor the reject rule is met."
    elif mean_ex > 0 and t_val >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "Mean short-direction excess return above 0 with t >= 2 and the above-median minus below-median difference above 0."
        else:
            status = "inconclusive"
            decided = "Mean short-direction excess return above 0 with t >= 2 but the supporting check fails: a confirming main measure whose supporting check fails."
    elif mean_ex < 0 and t_val <= -2:
        status = "rejected"
        decided = "Mean short-direction excess return below 0 with t <= -2: the price rises after these closes."
    else:
        status = "inconclusive"
        decided = "The day-pooled t lies between -2 and 2 (or its sign disagrees with the mean's), meeting neither rule."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": mean_ex,
                         "statistic": ({"name": "t of the mean, cases pooled by day", "value": t_val}
                                       if t_val is not None else None),
                         "threshold": main_thr},
        "supporting_check": {"name": sup_name, "value": sup_val, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": ("A case is the first short bet (forecast magnitude rising >= 2 points from its lowest level since the last bet, "
                    "reset at flat) in each non-overlapping 3-bar grid cell of a window, measured from its close to the close 3 bars later "
                    "within the window, drift being the coin's mean non-overlapping 3-bar return over all its windows; the t uses day-clustered "
                    "deviations with a D/(D-1) correction; median ties are left out of the supporting check; and the plan's 'fewer than 30 cases "
                    "on distinct days' is applied as the minimum count giving 'not observable'."),
    }
