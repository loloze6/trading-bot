import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    LHV = "debug_info.components.rsi_high.last_history_value"
    H = 5

    # ---------- 1. Situation check: RSI above 50 (raw value < 0), long side ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            f = pd.to_numeric(df["forecast"], errors="coerce")
            v = pd.to_numeric(df[LHV], errors="coerce") if LHV in df.columns else pd.Series(np.nan, index=df.index)
            active = f.notna() & (f != 0)
            n_active += int(active.sum())
            rsi_above_50 = v.notna() & (v < 0)  # RSI = 50 - v/0.4 > 50  <=>  v < 0
            n_agree += int((active & rsi_above_50 & (f > 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.9

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": "The plan's situation is a long position held while RSI is above 50 (raw RSIPullback value below 0), "
                          "but fewer than 90% of the bars with a non-zero forecast are long bars with RSI above 50.",
            "reading": "Situation taken as RSI > 50 (last_history_value < 0) with a positive forecast.",
        }

    # ---------- 2. Extreme threshold: top 20% of non-zero forecasts, pooled ----------
    nz = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            f = pd.to_numeric(df["forecast"], errors="coerce")
            nz.append(f[f.notna() & (f != 0)].values)
    nz = np.concatenate(nz) if nz else np.array([])
    thr = float(np.quantile(nz, 0.8)) if nz.size > 0 else np.nan

    # ---------- 3. Non-overlapping 5-bar forward returns ----------
    ext_all, neu_all = [], []
    per_coin = {}
    for coin, wins in bars.items():
        ext_c, neu_c = [], []
        for w, df in wins.items():
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").values
            f = pd.to_numeric(d["forecast"], errors="coerce").values
            n = len(d)
            for t in range(0, n - H, H):
                if np.isnan(close[t]) or np.isnan(close[t + H]) or np.isnan(f[t]) or close[t] == 0:
                    continue
                r = close[t + H] / close[t] - 1.0
                if not np.isnan(thr) and f[t] != 0 and f[t] >= thr:
                    ext_c.append(r)
                elif f[t] < 1:
                    neu_c.append(r)
        ext_all += ext_c
        neu_all += neu_c
        if len(ext_c) > 0 and len(neu_c) > 0:
            per_coin[coin] = float(np.mean(ext_c) - np.mean(neu_c))
        else:
            per_coin[coin] = None

    n_ext, n_neu = len(ext_all), len(neu_all)
    diff = float(np.mean(ext_all) - np.mean(neu_all)) if n_ext > 0 and n_neu > 0 else None
    if n_ext >= 2 and n_neu >= 2:
        t_stat = float(stats.ttest_ind(ext_all, neu_all, equal_var=False).statistic)
        if np.isnan(t_stat):
            t_stat = None
    else:
        t_stat = None
    n_coins_pos = int(sum(1 for v in per_coin.values() if v is not None and v > 0))

    # ---------- 4. Supporting: strategy minus exposure-scaled buy-and-hold, per coin ----------
    excess_total = 0.0
    any_excess = False
    for coin, wins in bars.items():
        allocs, strat_sum, coin_sum = [], 0.0, 0.0
        coin_rets_by_bar = []
        for w, df in wins.items():
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").values
            a = pd.to_numeric(d["postRebalance_current_allocation"], errors="coerce").values
            for t in range(len(d) - 1):
                if np.isnan(close[t]) or np.isnan(close[t + 1]) or np.isnan(a[t]) or close[t] == 0:
                    continue
                r = close[t + 1] / close[t] - 1.0
                allocs.append(a[t])
                strat_sum += a[t] * r
                coin_rets_by_bar.append(r)
        if allocs:
            avg_exp = float(np.mean(allocs))
            excess_total += strat_sum - avg_exp * float(np.sum(coin_rets_by_bar))
            any_excess = True
    excess = float(excess_total) if any_excess else None
    sup_passed = (excess > 0) if excess is not None else None

    # ---------- 5. Decision ----------
    counts = {
        "non-overlapping extreme cases pooled": int(n_ext),
        "neutral cases": int(n_neu),
        "coins with positive difference": n_coins_pos,
        "coins in record": int(len(bars)),
    }
    if n_ext < 30 or n_neu < 30 or t_stat is None:
        status = "inconclusive"
        decided = "Inconclusive: fewer than 30 non-overlapping extreme cases pooled or fewer than 30 neutral cases (or no t-statistic)."
    elif t_stat <= 0:
        status = "rejected"
        decided = ("Reject: the pooled difference is zero or negative (t <= 0)"
                   + ("; t <= -2 points to reversal." if t_stat <= -2 else "."))
    elif t_stat >= 2 and n_coins_pos >= 2 and sup_passed:
        status = "confirmed"
        decided = "Confirm: difference positive with t >= 2, positive in at least 2 coins, and the supporting excess positive pooled."
    else:
        status = "inconclusive"
        if t_stat < 2:
            decided = "Inconclusive: t between 0 and 2."
        else:
            decided = "Inconclusive: t >= 2 but fewer than 2 coins positive or the pooled supporting excess not positive, so the confirm rule is not fully met and the reject rule does not apply."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "mean 5-bar forward return after extreme minus after neutral bars",
            "value": diff,
            "statistic": {"name": "Welch t", "value": t_stat} if t_stat is not None else None,
            "threshold": "t >= 2 confirms (with >= 2 coins positive and positive pooled supporting excess); t <= 0 rejects",
        },
        "supporting_check": {
            "name": "strategy return minus exposure-scaled buy-and-hold, pooled",
            "value": excess,
            "passed": sup_passed,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": ("The 80th-percentile cut of non-zero forecasts is pooled over all coins and windows, neutral bars are forecast < 1 "
                    "(including 0) on the same 0,5,10,... grid, 'at least 2 of the 3 coins' is applied as at least 2 coins among those "
                    "in the record, and the supporting excess per coin is the summed daily strategy gain minus the coin's mean allocation "
                    "times its summed daily returns, added over coins."),
    }
