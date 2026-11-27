import numpy as np
import pandas as pd


def measure(bars):
    RUN_COL = "debug_info.components.run_len.last_history_value"

    def prior_down_run(close):
        # number of consecutive down closes immediately before bar t, when bar t is an up close; else 0
        c = close.values.astype(float)
        n = len(c)
        out = np.full(n, np.nan)
        for t in range(1, n):
            if not (c[t] > c[t - 1]):
                out[t] = 0.0
                continue
            k = 0
            j = t - 1
            while j >= 1 and c[j] < c[j - 1] and k < 30:
                k += 1
                j -= 1
            # if the run reaches the window's first bar, the true run may be longer: still >= k
            out[t] = float(k)
        return out

    # coin mean daily return over all windows together
    coin_mean = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            d = df.sort_values("timestamp")
            c = d["close"].astype(float).values
            if len(c) > 1:
                rets.append(c[1:] / c[:-1] - 1.0)
        coin_mean[coin] = float(np.mean(np.concatenate(rets))) if rets else np.nan

    active_total = 0
    active_agree = 0
    cases = []  # (day, value, run)
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df.sort_values("timestamp").reset_index(drop=True)
            close = d["close"].astype(float)
            fc = d["forecast"].astype(float).fillna(0.0).values
            run_prices = prior_down_run(close)
            run_rec = d[RUN_COL].astype(float).values if RUN_COL in d.columns else np.full(len(d), np.nan)
            run = np.where(~np.isnan(run_rec), run_rec, run_prices)
            up = np.r_[np.nan, (close.values[1:] > close.values[:-1]).astype(float)]
            # falling profile: 60-bar price change in % below -10, else the detector's veto decision
            evo = (close / close.shift(60) - 1.0) * 100.0
            regime = d["regime"].astype(str).values if "regime" in d.columns else np.array(["unknown"] * len(d))
            falling = np.where(evo.notna().values, evo.values < -10, regime != "chop")
            fwd = close.shift(-1) / close - 1.0
            days = pd.to_datetime(d["timestamp"], utc=True).dt.strftime("%Y-%m-%d").values
            for t in range(len(d)):
                if fc[t] != 0:
                    active_total += 1
                    is_up = up[t] == 1.0 if not np.isnan(up[t]) else (not np.isnan(run_rec[t]) and run_rec[t] >= 1)
                    sit = (not np.isnan(run[t])) and run[t] >= 2 and is_up and bool(falling[t])
                    if sit and fc[t] < 0:
                        active_agree += 1
                if fc[t] < 0 and not np.isnan(fwd.iloc[t]) and not np.isnan(coin_mean[coin]):
                    v = -(fwd.iloc[t] - coin_mean[coin])
                    cases.append((days[t], float(v), float(run[t]) if not np.isnan(run[t]) else np.nan))

    agreement = active_agree / active_total if active_total > 0 else 0.0
    sit_passed = bool(active_total > 0 and agreement >= 0.9)
    reading = ("Falling profile recomputed as the 60-bar close change in percent below -10 (the detector's regime "
               "veto where 60 window bars are lacking), run length from run_len.last_history_value or recomputed from "
               "closes, t clustered by summing deviations per UTC day with a G/(G-1) correction, and the plan's "
               "'at least 30 cases on distinct days' read as the minimum count.")
    mm_name = "mean short-side next-day move minus coin drift"
    mm_thr = "confirm: positive with day-clustered t >= 2 and check passes; reject: t <= -2"

    if not sit_passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": mm_name, "value": None, "statistic": None, "threshold": mm_thr},
            "supporting_check": None,
            "counts": {"active bars": int(active_total), "cases": len(cases)},
            "decided_by": "Fewer than 90% of the bars with a non-zero forecast are short bars on a run-ending up close "
                          "(2+ prior down closes) in a falling profile.",
            "reading": reading,
        }

    n_cases = len(cases)
    distinct_days = len(set(c[0] for c in cases))
    vals = np.array([c[1] for c in cases]) if n_cases else np.array([])
    mean = float(vals.mean()) if n_cases else None
    t_stat = None
    if n_cases > 1:
        dev = vals - vals.mean()
        s = pd.Series(dev).groupby([c[0] for c in cases]).sum().values
        G = len(s)
        var = (s ** 2).sum() / n_cases ** 2
        if G > 1:
            var *= G / (G - 1)
        t_stat = float(mean / np.sqrt(var)) if var > 0 else None

    runs = np.array([c[2] for c in cases]) if n_cases else np.array([])
    g3 = vals[runs >= 3] if n_cases else np.array([])
    g2 = vals[runs == 2] if n_cases else np.array([])
    diff = float(g3.mean() - g2.mean()) if len(g3) and len(g2) else None
    sc_passed = (diff > 0) if diff is not None else None

    counts = {"cases": int(n_cases), "distinct days": int(distinct_days),
              "cases run >= 3": int(len(g3)), "cases run == 2": int(len(g2))}

    if distinct_days < 30:
        status = "not observable"
        decided = f"Only {distinct_days} distinct days with cases, below the plan's minimum of 30."
    elif t_stat is not None and mean > 0 and t_stat >= 2 and sc_passed is True:
        status = "confirmed"
        decided = "Main measure positive with t >= 2 and runs of 3+ stronger than runs of 2."
    elif t_stat is not None and t_stat <= -2:
        status = "rejected"
        decided = "Main measure t <= -2: next days are stronger than the coin's drift."
    else:
        status = "inconclusive"
        if t_stat is not None and t_stat >= 2:
            decided = "Confirming t but the supporting check failed, so neither confirm nor reject."
        else:
            decided = "t between -2 and 2: neither confirm nor reject."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {"name": mm_name, "value": mean,
                         "statistic": ({"name": "day-clustered t", "value": t_stat} if t_stat is not None else None),
                         "threshold": mm_thr},
        "supporting_check": {"name": "mean after runs >= 3 minus mean after runs == 2", "value": diff,
                             "passed": sc_passed},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
