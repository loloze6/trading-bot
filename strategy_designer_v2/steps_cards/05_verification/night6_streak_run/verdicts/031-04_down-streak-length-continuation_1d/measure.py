import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    BAND = 2.0
    RAW = "debug_info.components.down_streak.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            close = pd.to_numeric(df["close"], errors="coerce").values
            down_price = np.r_[False, close[1:] < close[:-1]]
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce").values
                situ = np.where(np.isnan(raw), down_price, raw > 0)
            else:
                situ = down_price
            active = f != 0
            n_active += int(active.sum())
            n_agree += int((active & situ.astype(bool) & (f < 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.9

    main_name = "mean short-direction unusual 5-bar move of short bets (vs coin's normal 5-bar drift)"
    main_thr = "confirm: mean > 0 with t >= 2 over >= 30 distinct days and supporting check passes; reject: mean < 0 with t <= -2 over >= 30 distinct days"
    sup_name = "mean unusual move, |forecast| above median minus at/below median"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "distinct case days": 0},
            "decided_by": "Fewer than 90% of the bars with a non-zero forecast are down-close bars (down streak > 0) with a short forecast, so the config does not do what the Fidelity's situation and short side say.",
            "reading": "Situation = the recorded raw down-streak value > 0 (falling back to close below previous close where it is missing); expected side short.",
        }

    # ---------- 2. criterion ----------
    cases = []  # (coin, day, unusual, absf)
    for coin, wins in bars.items():
        # normal drift: mean 5-bar return on non-overlapping grid of all windows
        rets = []
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            c = pd.to_numeric(df["close"], errors="coerce").values
            for i in range(0, len(c) - H, H):
                r = c[i + H] / c[i] - 1
                if np.isfinite(r):
                    rets.append(r)
        if len(rets) == 0:
            continue
        drift = float(np.mean(rets))

        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            c = pd.to_numeric(df["close"], errors="coerce").values
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            ts = pd.to_datetime(df["timestamp"], utc=True)
            n = len(df)
            # short bets: rise of |forecast| on the short side of >= band from its lowest level since last bet
            bet = np.zeros(n, dtype=bool)
            ref = 0.0
            on_short = False
            for i in range(n):
                if f[i] < 0:
                    lvl = -f[i]
                    if not on_short:
                        ref = 0.0
                        on_short = True
                    if lvl - ref >= BAND:
                        bet[i] = True
                        ref = lvl
                    else:
                        ref = min(ref, lvl)
                else:
                    on_short = False
                    ref = 0.0
            # once per 5-bar grid cell: first bet bar in the cell
            for start in range(0, n, H):
                idx = [i for i in range(start, min(start + H, n)) if bet[i]]
                if not idx:
                    continue
                i = idx[0]
                if i + H >= n:
                    continue
                r = c[i + H] / c[i] - 1
                if not np.isfinite(r):
                    continue
                u = -(r - drift)
                cases.append((coin, ts.iloc[i].floor("D"), u, abs(f[i])))

    n_cases = len(cases)
    if n_cases > 0:
        cdf = pd.DataFrame(cases, columns=["coin", "day", "u", "absf"])
        n_days = int(cdf["day"].nunique())
        mean_u = float(cdf["u"].mean())
        dev = cdf["u"] - mean_u
        day_sums = dev.groupby(cdf["day"]).sum().values
        D = len(day_sums)
        if D > 1:
            var_mean = (D / (D - 1)) * np.sum(day_sums ** 2) / n_cases ** 2
            se = np.sqrt(var_mean)
            t = float(mean_u / se) if se > 0 else float("nan")
        else:
            t = float("nan")
        med = cdf["absf"].median()
        big = cdf.loc[cdf["absf"] > med, "u"]
        small = cdf.loc[cdf["absf"] <= med, "u"]
        if len(big) > 0 and len(small) > 0:
            diff = float(big.mean() - small.mean())
            sup_pass = bool(diff > 0)
        else:
            diff = None
            sup_pass = False
    else:
        n_days, mean_u, t, diff, sup_pass = 0, None, float("nan"), None, None

    counts = {"cases": int(n_cases), "distinct case days": int(n_days)}
    t_out = None if (t is None or not np.isfinite(t)) else float(t)

    if n_days < 30:
        status = "not observable"
        decided = "Fewer than 30 distinct case days, the plan's minimum count."
    elif t_out is not None and mean_u > 0 and t_out >= 2 and sup_pass:
        status = "confirmed"
        decided = "Mean short-direction unusual move positive with t >= 2 over at least 30 distinct days, and the larger-|forecast| half's mean exceeds the smaller half's."
    elif t_out is not None and mean_u < 0 and t_out <= -2:
        status = "rejected"
        decided = "Mean short-direction unusual move negative with t <= -2 over at least 30 distinct days: down streaks are followed by rises beyond the drift."
    elif t_out is not None and mean_u > 0 and t_out >= 2:
        status = "inconclusive"
        decided = "A confirming t whose supporting check fails (larger-|forecast| half does not exceed the smaller half)."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": mean_u,
                         "statistic": {"name": "t of the mean, same-day cases summed", "value": t_out},
                         "threshold": main_thr},
        "supporting_check": {"name": sup_name, "value": diff, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": "A case is the first short bet (|forecast| rising >= 2 points from its lowest short level since the last bet, from 0 after flat/side change) in each 5-bar grid cell from each window's first row, needing 5 bars ahead in its window; the drift is the coin's mean 5-bar return on that grid over all windows; the t uses a day-clustered standard error (deviations summed per UTC day); the median split puts |forecast| above the median in the larger half and at or below in the smaller.",
    }
