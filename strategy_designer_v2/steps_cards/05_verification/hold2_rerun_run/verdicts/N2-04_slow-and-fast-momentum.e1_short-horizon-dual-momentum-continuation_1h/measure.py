import numpy as np
import pandas as pd


def measure(bars):
    H = 72
    MIN_CASES = 100
    SLOW_COL = "debug_info.components.slow.last_history_value"
    FAST_COL = "debug_info.components.fast.last_history_value"

    def ret_from_close(close, period):
        # Percent return over `period` bars, computed inside one window only.
        c = close.astype(float)
        return c / c.shift(period) - 1.0

    # ---------------- 1. Situation check ----------------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.sort_values("timestamp").reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            if SLOW_COL in df.columns:
                slow = pd.to_numeric(df[SLOW_COL], errors="coerce")
            else:
                slow = pd.Series(np.nan, index=df.index)
            if FAST_COL in df.columns:
                fast = pd.to_numeric(df[FAST_COL], errors="coerce")
            else:
                fast = pd.Series(np.nan, index=df.index)
            # Bars where a component is not recorded: recompute it from the prices.
            slow = slow.fillna(ret_from_close(df["close"], 1440))
            fast = fast.fillna(ret_from_close(df["close"], 480))
            situation = (slow > 0) & (fast > 0)
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc > 0)).sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.90

    main_name = "mean excess 72-bar forward return over the coin's mean 72-bar return, at forecast > 0 grid bars"
    main_thr = "t >= 2 over at least 100 cases confirms; t <= -2 over at least 100 cases rejects"
    sup_name = "mean daily timing gain of the book over trending days"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None,
                             "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars on which "
                           "both the 60-day and 20-day returns are positive, as the plan's situation requires."
                           if n_active > 0 else
                           "The record holds no bar with a non-zero forecast, so the plan's situation cannot be matched."),
            "reading": "none",
        }

    # ---------------- 2. Main measure ----------------
    excess_all = []
    for coin, wins in bars.items():
        grid_rets = []   # all grid bars, all windows: the coin's holding mean
        grid_fc = []
        for w, df in wins.items():
            if df is None or len(df) <= H:
                continue
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            for i in range(0, len(df) - H, H):
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                grid_rets.append(c1 / c0 - 1.0)
                grid_fc.append(fc[i])
        if len(grid_rets) == 0:
            continue
        grid_rets = np.asarray(grid_rets, dtype=float)
        grid_fc = np.asarray(grid_fc, dtype=float)
        hold_mean = float(np.mean(grid_rets))
        sel = np.isfinite(grid_fc) & (grid_fc > 0)
        excess_all.extend(list(grid_rets[sel] - hold_mean))

    excess_all = np.asarray(excess_all, dtype=float)
    n_cases = int(len(excess_all))
    mean_ex = float(np.mean(excess_all)) if n_cases > 0 else None
    if n_cases >= 2:
        sd = float(np.std(excess_all, ddof=1))
        t_stat = float(mean_ex / (sd / np.sqrt(n_cases))) if sd > 0 else None
    else:
        t_stat = None

    # ---------------- 3. Supporting check: timing gain ----------------
    per_coin_daily = []
    for coin, wins in bars.items():
        # coin's mean daily return over all windows (holding)
        coin_daily_rets = []
        prepared = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.sort_values("timestamp").reset_index(drop=True).copy()
            ts = pd.to_datetime(df["timestamp"], utc=True)
            df["_day"] = ts.dt.floor("D")
            df["_alloc_held"] = pd.to_numeric(df["postRebalance_current_allocation"],
                                              errors="coerce").shift(1)
            df["_trend"] = (df["regime"].astype(str) == "trending")
            g = df.groupby("_day", sort=True)
            last = g.tail(1).set_index("_day")
            close_d = pd.to_numeric(last["close"], errors="coerce")
            val_d = pd.to_numeric(last["postRebalance_total_value"], errors="coerce")
            coin_ret = close_d / close_d.shift(1) - 1.0
            book_ret = val_d / val_d.shift(1) - 1.0
            alloc_d = g["_alloc_held"].mean()
            trend_d = g["_trend"].any()
            coin_daily_rets.extend(list(coin_ret.dropna().values))
            prepared.append(pd.DataFrame({"book": book_ret, "alloc": alloc_d,
                                          "trend": trend_d}).iloc[1:])
        if len(coin_daily_rets) == 0 or len(prepared) == 0:
            continue
        mu = float(np.mean(coin_daily_rets))
        d = pd.concat(prepared)
        d = d[d["trend"]].dropna(subset=["book", "alloc"])
        d = d.assign(timing=d["book"] - d["alloc"] * mu)
        per_coin_daily.append(d["timing"].rename(coin))

    if per_coin_daily:
        timing_by_day = pd.concat(per_coin_daily, axis=1).mean(axis=1, skipna=True).dropna()
        timing_mean = float(timing_by_day.mean()) if len(timing_by_day) > 0 else None
        n_days = int(len(timing_by_day))
    else:
        timing_mean, n_days = None, 0
    sup_passed = (timing_mean is not None) and (timing_mean > 0)

    # ---------------- 4. Decision ----------------
    if n_cases < MIN_CASES:
        status = "not observable"
        decided_by = (f"Only {n_cases} non-overlapping in-situation 72-bar cases, "
                      f"below the plan's minimum of {MIN_CASES}.")
    elif t_stat is None:
        status = "inconclusive"
        decided_by = "The t of the mean excess return could not be computed (zero dispersion)."
    elif t_stat >= 2 and sup_passed:
        status = "confirmed"
        decided_by = ("The mean excess 72-bar return has t >= 2 over at least 100 cases and "
                      "the mean daily timing gain over trending days is above 0.")
    elif t_stat >= 2:
        status = "inconclusive"
        decided_by = ("The mean excess 72-bar return has t >= 2 but the timing gain is 0 or below, "
                      "which the plan calls inconclusive.")
    elif t_stat <= -2:
        status = "rejected"
        decided_by = "The mean excess 72-bar return has t <= -2 over at least 100 cases."
    else:
        status = "inconclusive"
        decided_by = "The t of the mean excess 72-bar return lies between -2 and 2."

    reading = ("Cases are the bars at positions 0, 72, 144, ... of each window with forecast > 0 and a "
               "close 72 bars later in the same window, the holding mean is the coin's mean 72-bar return "
               "over all grid bars of all its windows, and the timing check uses the days containing at "
               "least one trending bar, with the position held over the day taken as the mean "
               "allocation carried into each of the day's bars.")

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": mean_ex,
                         "statistic": ({"name": "t of the mean", "value": t_stat}
                                       if t_stat is not None else None),
                         "threshold": main_thr},
        "supporting_check": {"name": sup_name, "value": timing_mean,
                             "passed": bool(sup_passed) if timing_mean is not None else None},
        "counts": {"non-overlapping in-situation cases": n_cases,
                   "trending days in the timing check": n_days,
                   "active bars": n_active},
        "decided_by": decided_by,
        "reading": reading,
    }
