import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    MIN_CASES = 30

    # Collect the non-zero forecasts of the whole record to set the pooled top-20% cut-off.
    nonzero = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            f = pd.to_numeric(df["forecast"], errors="coerce")
            f = f[f.notna() & (f != 0)]
            nonzero.extend(f.tolist())
    q80 = float(np.quantile(np.array(nonzero), 0.8)) if len(nonzero) > 0 else None

    ext_all, neu_all = [], []
    per_coin = {}
    support_per_coin = {}

    for coin, wins in bars.items():
        ext_c, neu_c = [], []
        strat_sum = 0.0
        coin_sum = 0.0
        alloc_list = []
        coin_rets = []
        strat_rets = []
        for w, df in wins.items():
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(d["forecast"], errors="coerce").to_numpy(dtype=float)
            alloc = pd.to_numeric(d["postRebalance_current_allocation"], errors="coerce").to_numpy(dtype=float)
            n = len(d)

            # Main measure: greedy non-overlapping 5-bar forward returns, separately per category, inside the window.
            if q80 is not None:
                next_ext, next_neu = 0, 0
                for t in range(n - H):
                    c0, c1, f = close[t], close[t + H], fc[t]
                    if not (np.isfinite(c0) and np.isfinite(c1) and np.isfinite(f)) or c0 == 0:
                        continue
                    r = c1 / c0 - 1.0
                    is_ext = (f != 0) and (f >= q80)
                    is_neu = (f < 1.0) and not is_ext
                    if is_ext and t >= next_ext:
                        ext_c.append(r)
                        next_ext = t + H
                    elif is_neu and t >= next_neu:
                        neu_c.append(r)
                        next_neu = t + H

            # Supporting check: per-bar strategy gain vs coin return, inside the window.
            for t in range(n - 1):
                a, c0, c1 = alloc[t], close[t], close[t + 1]
                if not (np.isfinite(a) and np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r1 = c1 / c0 - 1.0
                alloc_list.append(a)
                coin_rets.append(r1)
                strat_rets.append(a * r1)

        ext_all.extend(ext_c)
        neu_all.extend(neu_c)
        diff_c = (float(np.mean(ext_c)) - float(np.mean(neu_c))) if (len(ext_c) > 0 and len(neu_c) > 0) else None
        per_coin[coin] = {"diff": diff_c, "n_extreme": len(ext_c), "n_neutral": len(neu_c)}

        if len(alloc_list) > 0:
            avg_exp = float(np.mean(alloc_list))
            strat_sum = float(np.sum(strat_rets))
            coin_sum = float(np.sum(coin_rets))
            support_per_coin[coin] = strat_sum - avg_exp * coin_sum

    n_e, n_n = len(ext_all), len(neu_all)
    diff, tstat = None, None
    if n_e >= 2 and n_n >= 2:
        e = np.array(ext_all)
        u = np.array(neu_all)
        diff = float(e.mean() - u.mean())
        se = np.sqrt(e.var(ddof=1) / n_e + u.var(ddof=1) / n_n)
        tstat = float(diff / se) if se > 0 else (np.inf if diff > 0 else (-np.inf if diff < 0 else 0.0))
    elif n_e >= 1 and n_n >= 1:
        diff = float(np.mean(ext_all) - np.mean(neu_all))

    coins_positive = sum(1 for v in per_coin.values() if v["diff"] is not None and v["diff"] > 0)
    support_val = float(np.sum(list(support_per_coin.values()))) if support_per_coin else None
    support_pass = (support_val > 0) if support_val is not None else None

    if n_e < MIN_CASES or n_n < MIN_CASES or tstat is None:
        status = "inconclusive"
        decided_by = (f"Inconclusive: fewer than {MIN_CASES} non-overlapping extreme cases ({n_e}) "
                      f"or neutral cases ({n_n}) pooled.")
    elif tstat <= 0:
        status = "rejected"
        decided_by = ("Rejected: the pooled extreme-minus-neutral difference is zero or negative (t <= 0)"
                      + (", with t <= -2 pointing to reversal." if tstat <= -2 else "."))
    elif tstat >= 2 and coins_positive >= 2 and support_pass:
        status = "confirmed"
        decided_by = ("Confirmed: pooled difference positive with t >= 2, positive in at least 2 coins, "
                      "and pooled supporting excess positive.")
    else:
        status = "inconclusive"
        if tstat < 2:
            decided_by = "Inconclusive: t is between 0 and 2."
        else:
            decided_by = ("Inconclusive: t >= 2 but the confirm rule's other conditions (positive in at least "
                          "2 coins, positive pooled supporting excess) are not all met.")

    t_out = None if tstat is None else (float(tstat) if np.isfinite(tstat) else (1e9 if tstat > 0 else -1e9))

    return {
        "status": status,
        "main_measure": {
            "name": "mean 5-bar forward return, extreme minus neutral bars (pooled), t-statistic",
            "value": t_out,
            "threshold": "t >= 2 confirms (with other conditions); t <= 0 rejects; 0 < t < 2 inconclusive",
        },
        "supporting_check": {
            "name": "strategy return minus exposure-scaled buy-and-hold, summed over coins, before costs",
            "value": support_val,
            "passed": support_pass,
        },
        "cases": int(n_e),
        "decided_by": decided_by,
        "reading": (
            "The top-20% cut-off is the 80th percentile of all non-zero forecasts pooled over the record; "
            "non-overlapping samples are taken greedily per category inside each window (a bar is used only if "
            "it starts at least 5 bars after the previous sample of its category); the t-statistic is Welch's "
            "two-sample t; 'positive in at least 2 of the 3 coins' is applied as at least 2 positive coins among "
            "those present; the supporting excess per coin is the sum of per-bar strategy gains minus the coin's "
            "mean allocation times the sum of its per-bar returns, pooled as the sum over coins; cases counts the "
            f"non-overlapping extreme samples (neutral samples: {n_n}; diff: {diff}; per-coin: "
            + str({k: v['diff'] for k, v in per_coin.items()}) + ")."
        ),
    }
