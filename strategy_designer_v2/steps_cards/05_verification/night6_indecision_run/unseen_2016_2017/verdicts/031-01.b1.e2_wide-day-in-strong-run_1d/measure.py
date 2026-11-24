import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 3
    RISE_COL = "debug_info.components.rise_strength.last_history_value"

    def rise5_of(df):
        # 5-day return: the recorded raw value of rise_strength (PriceEvolution, period 5) where recorded,
        # else recomputed from the window's own closes (never across windows)
        close = df["close"].astype(float).reset_index(drop=True)
        from_prices = close / close.shift(5) - 1.0
        if RISE_COL in df.columns:
            rec = pd.to_numeric(df[RISE_COL], errors="coerce").reset_index(drop=True)
            return rec.where(rec.notna(), from_prices)
        return from_prices

    # ---------------- 1. situation check ----------------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce").reset_index(drop=True)
            r5 = rise5_of(df)
            active = fc.notna() & (fc != 0)
            situ = (r5 > 0) & (fc > 0)
            n_active += int(active.sum())
            n_agree += int((active & situ).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "3-day forward return minus the coin's normal 3-day drift, top-fifth forecast in-rise grid bars"
    main_thr = "confirm: mean > 0 with day-clustered t >= 2 (and top-minus-bottom > 0); reject: mean < 0 with t <= -2"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90 % of the bars with a non-zero forecast are long bars inside a 5-day rise "
                           "(5-day return above 0), which the Fidelity's situation and side require."
                           if n_active > 0 else "The record holds no active bar to compare with the plan's situation."),
            "reading": "none",
        }

    # ---------------- 2. criterion ----------------
    # normal 3-day drift per coin: mean of non-overlapping 3-bar returns over all its windows
    rows = []
    drift = {}
    for coin, wins in bars.items():
        all_rets = []
        coin_rows = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = d["close"].astype(float).values
            fc = pd.to_numeric(d["forecast"], errors="coerce").values
            r5 = rise5_of(d).values
            ts = pd.to_datetime(d["timestamp"], utc=True)
            n = len(d)
            for p in range(0, n, H):
                if p + H >= n:
                    continue
                if not (np.isfinite(close[p]) and np.isfinite(close[p + H]) and close[p] != 0):
                    continue
                ret = close[p + H] / close[p] - 1.0
                all_rets.append(ret)
                coin_rows.append({
                    "coin": coin, "ret": ret, "fc": fc[p], "r5": r5[p],
                    "day": ts.iloc[p].floor("D"),
                })
        drift[coin] = float(np.mean(all_rets)) if all_rets else np.nan
        for r in coin_rows:
            r["excess"] = r["ret"] - drift[coin]
        rows.extend(coin_rows)

    g = pd.DataFrame(rows)
    if len(g):
        g = g[np.isfinite(g["fc"]) & np.isfinite(g["r5"]) & np.isfinite(g["excess"])]
        inrise = g[g["r5"] > 0].copy()
    else:
        inrise = pd.DataFrame(columns=["coin", "ret", "fc", "r5", "day", "excess"])

    if len(inrise):
        q80 = float(np.quantile(inrise["fc"].values, 0.8))
        q20 = float(np.quantile(inrise["fc"].values, 0.2))
        top = inrise[inrise["fc"] >= q80]
        bot = inrise[inrise["fc"] <= q20]
    else:
        top = inrise
        bot = inrise

    n_top = int(len(top))
    n_top_days = int(top["day"].nunique()) if n_top else 0
    n_bot = int(len(bot))

    mean_top = float(top["excess"].mean()) if n_top else None
    t_top = None
    if n_top >= 2:
        x = top["excess"].values
        dev = pd.Series(x - x.mean(), index=top.index).groupby(top["day"]).sum().values
        G = len(dev)
        if G >= 2:
            var_mean = (G / (G - 1.0)) * np.sum(dev ** 2) / (n_top ** 2)
            if var_mean > 0:
                t_top = float(x.mean() / np.sqrt(var_mean))

    diff = None
    welch_t = None
    if n_top >= 1 and n_bot >= 1:
        diff = float(top["excess"].mean() - bot["excess"].mean())
        if n_top >= 2 and n_bot >= 2:
            wt = stats.ttest_ind(top["excess"].values, bot["excess"].values, equal_var=False).statistic
            welch_t = float(wt) if np.isfinite(wt) else None
    supp_passed = None if diff is None else bool(diff > 0)

    counts = {
        "top-fifth cases on separate days": n_top_days,
        "top-fifth cases": n_top,
        "bottom-fifth in-rise cases": n_bot,
        "in-rise grid bars": int(len(inrise)),
    }

    if n_top_days < 30:
        status = "not observable"
        decided = f"The minimum of 30 top-fifth cases on separate days is not reached ({n_top_days})."
    elif t_top is None or mean_top is None:
        status = "inconclusive"
        decided = "The day-clustered t of the main measure could not be computed, so neither confirm nor reject is met."
    elif mean_top > 0 and t_top >= 2:
        if supp_passed:
            status = "confirmed"
            decided = "The main-measure mean is above 0 with t >= 2 and the top-minus-bottom difference is above 0."
        else:
            status = "inconclusive"
            decided = "The main measure meets the confirm rule but the top-minus-bottom supporting check fails."
    elif mean_top < 0 and t_top <= -2:
        status = "rejected"
        decided = "The main-measure mean is below 0 with t <= -2."
    else:
        status = "inconclusive"
        decided = "The main-measure t lies between -2 and 2 (or the mean's sign disagrees with it), meeting neither rule."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_top,
            "statistic": None if t_top is None else {"name": "t of the mean, same-day cases taken together", "value": t_top},
            "threshold": main_thr,
        },
        "supporting_check": {
            "name": "mean excess top fifth minus bottom fifth in-rise" + ("" if welch_t is None else f" (Welch t {welch_t:.3f})"),
            "value": diff,
            "passed": supp_passed,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": ("The top and bottom fifths are the in-rise (5-day return > 0) bars of the 3-bar grid, pooled over all "
                    "coins and windows, with forecast at or above the 80th (at or below the 20th) percentile of those bars' "
                    "forecasts; the day-clustered t sums each day's deviations with a G/(G-1) correction, and the minimum "
                    "count missed makes the status not observable."),
    }
