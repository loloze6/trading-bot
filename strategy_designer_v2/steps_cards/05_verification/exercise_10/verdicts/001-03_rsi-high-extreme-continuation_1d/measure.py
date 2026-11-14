import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    VCOL = "debug_info.components.rsi_high.last_history_value"
    NEUTRAL_BAND = 4.0  # |raw value| <= 4  <=>  RSI in [40, 60]

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            f = pd.to_numeric(df["forecast"], errors="coerce")
            v = pd.to_numeric(df[VCOL], errors="coerce")
            ok = f.notna() & v.notna()
            active = ok & (f != 0)
            rsi = 50.0 - v / 0.4
            agree = active & (f > 0) & (rsi > 50)
            n_active += int(active.sum())
            n_agree += int(agree.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.9

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of bars with a non-zero forecast are long bars with RSI(14) above 50, "
                           "so the config's position does not follow the plan's situation of a long that grows as RSI rises above 50."),
            "reading": "Situation taken as forecast > 0 on bars where RSI = 50 - raw value / 0.4 is above 50.",
        }

    # ---------- 2. Extreme threshold: top 20% of positive forecasts, pooled ----------
    pos_vals = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            f = pd.to_numeric(df["forecast"], errors="coerce")
            pos_vals.append(f[f > 0].dropna().values)
    pos_vals = np.concatenate(pos_vals) if pos_vals else np.array([])
    thr = float(np.quantile(pos_vals, 0.8)) if pos_vals.size > 0 else np.inf

    # ---------- 3. Non-overlapping forward returns on the grid ----------
    ext_all, neu_all = [], []
    per_coin = {}
    supp = {}
    for coin, wins in bars.items():
        ce, cn = [], []
        strat_sum, bh_sum = 0.0, 0.0
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            f = pd.to_numeric(df["forecast"], errors="coerce").values
            v = pd.to_numeric(df[VCOL], errors="coerce").values
            alloc = pd.to_numeric(df["postRebalance_current_allocation"], errors="coerce").values
            n = len(df)
            for t in range(0, n, H):
                if t + H >= n:
                    break
                r = close[t + H] / close[t] - 1.0
                if not np.isfinite(r):
                    continue
                if np.isfinite(f[t]) and f[t] > 0 and f[t] >= thr:
                    ce.append(r)
                if np.isfinite(v[t]) and abs(v[t]) <= NEUTRAL_BAND:
                    cn.append(r)
            # supporting check: per-bar gains on non-zero forecast bars
            for t in range(n - 1):
                r1 = close[t + 1] / close[t] - 1.0
                if not (np.isfinite(f[t]) and f[t] != 0 and np.isfinite(r1) and np.isfinite(alloc[t])):
                    continue
                strat_sum += alloc[t] * r1
                bh_sum += r1
        ext_all += ce
        neu_all += cn
        d = float(np.mean(ce) - np.mean(cn)) if (len(ce) > 0 and len(cn) > 0) else None
        per_coin[coin] = {"diff": d, "n_ext": len(ce), "n_neu": len(cn)}
        supp[coin] = strat_sum - bh_sum

    n_ext, n_neu = len(ext_all), len(neu_all)
    diff = float(np.mean(ext_all) - np.mean(neu_all)) if (n_ext > 0 and n_neu > 0) else None
    tval = None
    if n_ext >= 2 and n_neu >= 2:
        tt = stats.ttest_ind(ext_all, neu_all, equal_var=False)
        tval = float(tt.statistic) if np.isfinite(tt.statistic) else None
    coins_pos = int(sum(1 for c in per_coin.values() if c["diff"] is not None and c["diff"] > 0))
    supp_pos = int(sum(1 for x in supp.values() if x > 0))
    supp_passed = supp_pos >= 2

    counts = {
        "non-overlapping extreme cases": int(n_ext),
        "neutral cases": int(n_neu),
        "coins with positive difference": coins_pos,
        "coins in record": int(len(per_coin)),
    }

    if n_ext < 30 or n_neu < 30:
        status = "not observable"
        decided = (f"Minimum count not reached: {n_ext} non-overlapping extreme cases and {n_neu} neutral cases "
                   "against the plan's minimum of 30 each.")
    elif diff is not None and tval is not None and diff > 0 and tval >= 2 and coins_pos >= 2:
        status = "confirmed"
        decided = "Confirm rule met: the extreme-minus-neutral difference is positive with t >= 2 and positive in at least 2 coins."
    elif diff is not None and tval is not None and diff < 0 and tval <= -2:
        status = "rejected"
        decided = "Reject rule met: the extreme-minus-neutral difference is negative with t <= -2."
    else:
        status = "inconclusive"
        if tval is None or -2 < tval < 2:
            decided = "Inconclusive rule met: t lies between -2 and 2."
        else:
            decided = "Inconclusive rule met: t clears 2 but the difference is positive in fewer than 2 coins."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "pooled forward 5-bar return after extreme bars minus after neutral bars",
            "value": diff,
            "statistic": {"name": "Welch t", "value": tval} if tval is not None else None,
            "threshold": "confirm if positive with t >= 2 and positive in at least 2 of the coins; reject if negative with t <= -2",
        },
        "supporting_check": {
            "name": "coins where strategy minus buy-and-hold return on non-zero-forecast bars is positive",
            "value": supp_pos,
            "passed": bool(supp_passed),
        },
        "counts": counts,
        "decided_by": decided,
        "reading": ("Extreme bars are grid bars whose forecast is at or above the 80th percentile of all positive forecasts pooled over coins and windows, "
                    "neutral bars are grid bars with |raw RSI component| <= 4, the 'at least 2 of the 3 coins' rules are applied as at least 2 of the coins present (only 2 are in the record), "
                    "per-coin support uses each coin's extreme-minus-neutral difference, and the supporting check sums per-bar returns and is reported without entering the decision."),
    }
