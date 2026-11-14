import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    VAL = "debug_info.components.rsi_high.last_history_value"

    # ---------- 1. Situation check ----------
    # Fidelity: situation = RSI above 50 (graded long), so raw value (50 - RSI) * 0.4 < 0; expected side = long.
    n_active = 0
    n_agree = 0
    for coin in bars:
        for w in bars[coin]:
            df = bars[coin][w]
            f = pd.to_numeric(df["forecast"], errors="coerce")
            v = pd.to_numeric(df[VAL], errors="coerce")
            active = f.notna() & (f != 0)
            n_active += int(active.sum())
            agree = active & v.notna() & (v < 0) & (f > 0)
            n_agree += int(agree.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": "Fewer than 90% of bars with a non-zero forecast are long bars with RSI above 50 "
                          "(raw component value below 0), so the config does not trade the plan's situation on its side.",
            "reading": "none",
        }

    # ---------- 2. Criterion ----------
    # Pooled cut-off for "top 20% of positive forecasts" over all bars of all coins and windows.
    pos_all = []
    for coin in bars:
        for w in bars[coin]:
            f = pd.to_numeric(bars[coin][w]["forecast"], errors="coerce")
            pos_all.append(f[f > 0].values)
    pos_all = np.concatenate(pos_all) if pos_all else np.array([])
    cut = float(np.quantile(pos_all, 0.8)) if len(pos_all) > 0 else np.inf

    ext_all, neu_all = [], []
    per_coin = {}
    supp = {}
    for coin in bars:
        ce, cn = [], []
        strat_sum, bh_sum = 0.0, 0.0
        for w in bars[coin]:
            df = bars[coin][w].reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            f = pd.to_numeric(df["forecast"], errors="coerce")
            v = pd.to_numeric(df[VAL], errors="coerce")
            alloc = pd.to_numeric(df["postRebalance_current_allocation"], errors="coerce")
            fwd = close.shift(-H) / close - 1.0
            grid = (np.arange(len(df)) % H) == 0
            ext = grid & (f > 0) & (f >= cut) & fwd.notna()
            neu = grid & v.notna() & (v.abs() <= 4) & fwd.notna()
            ce.extend(fwd[ext].tolist())
            cn.extend(fwd[neu].tolist())
            # supporting check: bars with non-zero forecast
            r1 = close.shift(-1) / close - 1.0
            m = f.notna() & (f != 0) & r1.notna() & alloc.notna()
            strat_sum += float((alloc[m] * r1[m]).sum())
            bh_sum += float(r1[m].sum())
        ext_all.extend(ce)
        neu_all.extend(cn)
        if len(ce) > 0 and len(cn) > 0:
            per_coin[coin] = float(np.mean(ce) - np.mean(cn))
        else:
            per_coin[coin] = None
        supp[coin] = strat_sum - bh_sum

    n_ext = len(ext_all)
    n_neu = len(neu_all)
    diff = float(np.mean(ext_all) - np.mean(neu_all)) if n_ext > 0 and n_neu > 0 else None
    t = None
    if n_ext >= 2 and n_neu >= 2:
        tt = stats.ttest_ind(ext_all, neu_all, equal_var=False).statistic
        t = float(tt) if np.isfinite(tt) else None
    coins_pos = int(sum(1 for c in per_coin if per_coin[c] is not None and per_coin[c] > 0))

    supp_pos = int(sum(1 for c in supp if supp[c] > 0))
    supp_passed = bool(supp_pos >= 2)

    counts = {
        "non-overlapping extreme cases": int(n_ext),
        "neutral cases": int(n_neu),
        "coins with positive difference": coins_pos,
        "coins": int(len(bars)),
    }

    if n_ext < 30 or n_neu < 30:
        status = "not observable"
        decided = (f"Minimum count not reached: {n_ext} non-overlapping extreme cases and {n_neu} neutral cases "
                   f"(the plan needs at least 30 of each).")
    elif t is not None and diff is not None and diff > 0 and t >= 2 and coins_pos >= 2:
        status = "confirmed"
        decided = "Confirm rule met: the extreme-minus-neutral difference is positive with t >= 2 and positive in at least 2 coins."
    elif t is not None and diff is not None and diff < 0 and t <= -2:
        status = "rejected"
        decided = "Reject rule met: the extreme-minus-neutral difference is negative with t <= -2."
    else:
        status = "inconclusive"
        if t is None or (-2 < t < 2):
            decided = "Inconclusive rule met: t lies between -2 and 2."
        else:
            decided = "Inconclusive rule met: the positive result is supported in fewer than 2 coins."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": passed},
        "main_measure": {
            "name": "forward 5-bar return after extreme bars minus after neutral bars (pooled, before costs)",
            "value": diff,
            "statistic": {"name": "Welch t", "value": t} if t is not None else None,
            "threshold": "positive with t >= 2 and positive in at least 2 of the coins to confirm; negative with t <= -2 to reject",
        },
        "supporting_check": {
            "name": "coins where strategy minus buy-and-hold return on non-zero-forecast bars is positive",
            "value": supp_pos,
            "passed": supp_passed,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": ("The top 20% cut-off is the 80th percentile of all positive forecasts pooled over coins and windows "
                    "(extreme = forecast at or above it), neutral bars have |raw value| <= 4, both groups are then taken "
                    "on the 0,5,10,... grid of each window, the 'at least 2 of the 3 coins' rules are applied as at least 2 "
                    "of the coins present, and the supporting check is reported but not used in the decision since the "
                    "confirm rule does not name it."),
    }
