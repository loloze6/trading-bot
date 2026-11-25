import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    BAND = 2.0
    MIN_DAYS = 30
    DEPTH_COL = "debug_info.components.depth_short.last_history_value"

    def prep(df):
        d = df.copy()
        d["timestamp"] = pd.to_datetime(d["timestamp"], utc=True)
        d = d.sort_values("timestamp").reset_index(drop=True)
        d["close"] = pd.to_numeric(d["close"], errors="coerce")
        d["forecast"] = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0)
        return d

    def depth_from_prices(close):
        # distance of the close below the prior 20-day closing high, in 20-day daily swings
        prior_high = close.shift(1).rolling(20, min_periods=20).max()
        vol = close.pct_change().rolling(20, min_periods=20).std()
        return (close - prior_high) / (vol * close)

    # ---------------- 1. situation check ----------------
    n_active = 0
    n_agree = 0
    prepared = {}
    for coin, wins in bars.items():
        prepared[coin] = {}
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = prep(df)
            prepared[coin][w] = d
            close = d["close"]
            if DEPTH_COL in d.columns:
                depth = pd.to_numeric(d[DEPTH_COL], errors="coerce")
            else:
                depth = pd.Series(np.nan, index=d.index)
            depth = depth.fillna(depth_from_prices(close))
            # 60-day price evolution in percent; choppy = within [-10, 10]
            evo = (close / close.shift(60) - 1.0) * 100.0
            choppy = evo.isna() | ((evo >= -10) & (evo <= 10))
            active = d["forecast"] != 0
            situ = (depth <= -2.0) & choppy & (d["forecast"] < 0)
            n_active += int(active.sum())
            n_agree += int((active & situ).sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = True if agreement is None else bool(agreement >= 0.9)

    main_name = "mean excess 5-bar fall of short bets vs coin's normal drift"
    threshold = "confirm: mean > 0 with t >= 2 and supporting check passed; reject: mean < 0 with t <= -2"
    supp_name = "mean excess fall of cases with |forecast| above median minus at/below median"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": n_active, "active bars in situation on short side": n_agree},
            "decided_by": "Fewer than 90% of the active bars are short bars with the close 2 or more 20-day swings "
                          "below the prior 20-day closing high in a flat 60-day trend (|evolution| <= 10%).",
            "reading": "Depth taken from the recorded depth_short raw value (recomputed from prices where missing); "
                       "the choppy profile recomputed as the 60-bar percent price change within +-10, untested where "
                       "fewer than 60 bars of the window precede the bar.",
        }

    # ---------------- 2. criterion ----------------
    cases = []  # (coin, date, excess_fall, abs_forecast)
    for coin, wins in prepared.items():
        # coin's normal 5-bar drift: non-overlapping grid of all windows together
        grid_rets = []
        for w, d in wins.items():
            c = d["close"].values
            for i in range(0, len(c) - H, H):
                if np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] > 0:
                    grid_rets.append(c[i + H] / c[i] - 1.0)
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))

        for w, d in wins.items():
            f = d["forecast"].values
            c = d["close"].values
            ts = d["timestamp"]
            n = len(d)
            # bets on the short side: forecast deepening below 0 by >= band from its lowest
            # level (in size) since its last bet, from 0 after a flat or a change of side
            is_bet = np.zeros(n, dtype=bool)
            ref = 0.0
            prev_short = False
            for i in range(n):
                if f[i] < 0:
                    a = -f[i]
                    if not prev_short:
                        ref = 0.0
                    if a - ref >= BAND - 1e-12:
                        is_bet[i] = True
                        ref = a
                    else:
                        ref = min(ref, a)
                    prev_short = True
                else:
                    prev_short = False
                    ref = 0.0
            # once per non-overlapping 5-bar grid cell: first bet in the cell
            for start in range(0, n, H):
                idx = np.where(is_bet[start:start + H])[0]
                if len(idx) == 0:
                    continue
                t = start + int(idx[0])
                if t + H >= n:
                    continue
                if not (np.isfinite(c[t]) and np.isfinite(c[t + H]) and c[t] > 0):
                    continue
                r = c[t + H] / c[t] - 1.0
                excess_fall = -(r - drift)
                cases.append((coin, ts.iloc[t].strftime("%Y-%m-%d"), excess_fall, abs(f[t])))

    n_cases = len(cases)
    days = sorted(set(x[1] for x in cases))
    n_days = len(days)

    mean_ex = None
    t_stat = None
    if n_cases > 0:
        vals = np.array([x[2] for x in cases], dtype=float)
        mean_ex = float(vals.mean())
        dev = pd.Series(vals - mean_ex).groupby([x[1] for x in cases]).sum().values
        D = len(dev)
        if D > 1:
            var_mean = (D / (D - 1.0)) * np.sum(dev ** 2) / (n_cases ** 2)
            se = np.sqrt(var_mean)
            t_stat = float(mean_ex / se) if se > 0 else None

    supp_value = None
    supp_pass = None
    if n_cases > 0:
        vals = np.array([x[2] for x in cases], dtype=float)
        mags = np.array([x[3] for x in cases], dtype=float)
        med = float(np.median(mags))
        hi = vals[mags > med]
        lo = vals[mags <= med]
        if len(hi) > 0 and len(lo) > 0:
            supp_value = float(hi.mean() - lo.mean())
            supp_pass = bool(supp_value > 0)
        else:
            supp_pass = False

    counts = {"independent case days across coins and windows": n_days, "cases": n_cases}

    if n_days < MIN_DAYS:
        status = "not observable"
        decided = f"Fewer than 30 independent case days across coins and windows ({n_days})."
    elif t_stat is not None and mean_ex > 0 and t_stat >= 2 and supp_pass:
        status = "confirmed"
        decided = "Mean excess fall above 0 with t >= 2, and the supporting check passes."
    elif t_stat is not None and mean_ex > 0 and t_stat >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the supporting check failed, which the plan calls inconclusive."
    elif t_stat is not None and mean_ex < 0 and t_stat <= -2:
        status = "rejected"
        decided = "Mean excess fall below 0 with t <= -2: the coin rises more than its drift after deep-below-high closes."
    else:
        status = "inconclusive"
        decided = "t between -2 and 2 (or not computable), which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_ex,
            "statistic": None if t_stat is None else {"name": "t of the mean, cases of one day taken together", "value": t_stat},
            "threshold": threshold,
        },
        "supporting_check": {"name": supp_name, "value": supp_value, "passed": supp_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": "A case is the first short bet (forecast deepening >= 2 points below 0 from its lowest size since the "
                   "last bet) in each non-overlapping 5-bar grid cell of a window, its 5-bar return taken from that bar's "
                   "close, drift is the coin's mean grid 5-bar return over all windows, the day-clustered t uses a D/(D-1) "
                   "correction, and the situation's choppy profile is the 60-bar percent change within +-10, untested "
                   "where fewer than 60 window bars precede the bar.",
    }
