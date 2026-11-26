import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    FC = "forecast"
    RAW = "debug_info.components.near_low.last_history_value"
    PPV = "debug_info.components.near_low.post_pipeline_value"

    # ---------- 1. Situation check: down day (close < prior close), long side ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = df["close"].astype(float)
            prev = close.shift(1)
            down = close < prev
            # first bar of a window: prior close not in the window; fall back on the detector's decision
            first_mask = prev.isna()
            if "regime" in df.columns:
                down = down.where(~first_mask, df["regime"] == "mean_reversion")
            fc = df[FC].astype(float)
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            n_agree += int((active & down & (fc > 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.90)

    main_name = "Welch t of next-day return, top minus bottom tercile of near_low on down days"
    threshold = "confirm: difference > 0 with Welch t >= 2 and supporting check passes; reject: Welch t <= -2, or top-tercile minus holding t <= -2"
    reading = ("Down days are recomputed as close[t] < close[t-1] inside each window (the regime column is used for a window's first bar only); "
               "terciles are taken per coin over all its windows on down-day bars (regime mean_reversion) having both near_low post_pipeline_value and a next-day return, ranked with ties broken by order; "
               "holding is the coin's mean next-day return over all its bars and windows, the supporting check is the mean of (top-tercile return minus its coin's holding) > 0 with its one-sample t used for the reject alternative; "
               "fewer than 300 cases in any tercile is reported as not observable.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90 % of the bars with a non-zero forecast are down days (close below the prior close) "
                           "with a long forecast, as the plan's Fidelity requires."),
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    top_rets, bot_rets, top_excess = [], [], []
    for coin, wins in bars.items():
        all_rets = []
        cases = []
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = df["close"].astype(float)
            nxt = close.shift(-1) / close - 1.0  # inside the window only
            all_rets.append(nxt.dropna().values)
            if PPV not in df.columns:
                continue
            m = (df["regime"] == "mean_reversion") & df[PPV].notna() & nxt.notna()
            sub = pd.DataFrame({"x": df.loc[m, PPV].astype(float).values,
                                "r": nxt[m].values})
            cases.append(sub)
        all_r = np.concatenate(all_rets) if all_rets else np.array([])
        if len(all_r) == 0 or not cases:
            continue
        hold = float(np.mean(all_r))
        c = pd.concat(cases, ignore_index=True)
        if len(c) < 3:
            continue
        ranks = c["x"].rank(method="first")
        terc = pd.qcut(ranks, 3, labels=[0, 1, 2]).astype(int)
        top = c.loc[terc == 2, "r"].values
        bot = c.loc[terc == 0, "r"].values
        top_rets.append(top)
        bot_rets.append(bot)
        top_excess.append(top - hold)

    top = np.concatenate(top_rets) if top_rets else np.array([])
    bot = np.concatenate(bot_rets) if bot_rets else np.array([])
    exc = np.concatenate(top_excess) if top_excess else np.array([])
    n_top, n_bot = int(len(top)), int(len(bot))
    counts = {"top tercile down-day cases": n_top, "bottom tercile down-day cases": n_bot}

    diff = float(np.mean(top) - np.mean(bot)) if n_top > 0 and n_bot > 0 else None
    t_diff = None
    if n_top > 1 and n_bot > 1:
        t_diff = float(stats.ttest_ind(top, bot, equal_var=False).statistic)
    exc_mean = float(np.mean(exc)) if len(exc) > 0 else None
    t_exc = None
    if len(exc) > 1 and np.std(exc, ddof=1) > 0:
        t_exc = float(exc_mean / (np.std(exc, ddof=1) / np.sqrt(len(exc))))
    sup_passed = None if exc_mean is None else bool(exc_mean > 0)

    main = {"name": main_name, "value": diff,
            "statistic": None if t_diff is None else {"name": "Welch t", "value": t_diff},
            "threshold": threshold}
    support = {"name": "top tercile mean next-day return minus holding the coin (t: %s)" %
                       (None if t_exc is None else round(t_exc, 3)),
               "value": exc_mean, "passed": sup_passed}

    if n_top < 300 or n_bot < 300:
        status = "not observable"
        decided = "The plan's minimum of 300 down-day cases in each tercile, pooled over coins and windows, is not reached."
    elif t_diff is None:
        status = "not observable"
        decided = "The Welch t could not be computed on the tercile cases."
    elif t_diff <= -2:
        status = "rejected"
        decided = "The top-minus-bottom difference has a Welch t of -2 or less (reject rule)."
    elif t_exc is not None and t_exc <= -2:
        status = "rejected"
        decided = "The top tercile's next-day return minus holding has a t of -2 or less (reject rule: closes at the low are followed by further falls)."
    elif diff is not None and diff > 0 and t_diff >= 2 and sup_passed:
        status = "confirmed"
        decided = "The top-minus-bottom difference is positive with a Welch t of 2 or more and the top tercile beats holding (confirm rule)."
    elif diff is not None and diff > 0 and t_diff >= 2:
        status = "inconclusive"
        decided = "The difference meets the confirm rule but the supporting check fails (inconclusive rule)."
    else:
        status = "inconclusive"
        decided = "The Welch t lies between -2 and 2 (inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": support,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
