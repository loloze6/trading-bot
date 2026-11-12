import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    COMP = "debug_info.components.rsi_low.last_history_value"

    # ---------- 1. Situation check: RSI < 50 (raw value > 0), short side (forecast < 0) ----------
    n_active = 0
    n_agree = 0
    for coin in bars:
        for w in bars[coin]:
            df = bars[coin][w]
            if "forecast" not in df.columns or COMP not in df.columns:
                continue
            sub = df[["forecast", COMP]].dropna()
            active = sub["forecast"] != 0
            n_active += int(active.sum())
            # raw value = (50 - RSI) * 0.4 ; RSI < 50  <=> raw > 0
            situation = sub[COMP] > 0
            n_agree += int((active & situation & (sub["forecast"] < 0)).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.90)

    main_name = "mean forward 5-bar return after top-quintile |forecast| minus after neutral bars"
    threshold = "confirm if difference < 0 with Welch t <= -2; reject if difference > 0 with t >= +2"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of active bars have RSI below 50 with a short forecast, "
                           "so the config's positions do not follow the plan's graded short when RSI is below 50."),
            "reading": "none",
        }

    # ---------- 2. Non-overlapping 5-bar grid per window ----------
    rows = []
    for coin in bars:
        for w in bars[coin]:
            df = bars[coin][w].reset_index(drop=True)
            close = df["close"].astype(float)
            fwd = close.shift(-H) / close - 1.0
            for i in range(0, len(df), H):
                f = df.at[i, "forecast"]
                r = fwd.iloc[i]
                if pd.isna(f) or pd.isna(r):
                    continue
                rows.append((coin, float(f), float(r)))
    g = pd.DataFrame(rows, columns=["coin", "forecast", "ret"])

    absf = g["forecast"].abs() if len(g) else pd.Series(dtype=float)
    nz = absf[absf > 0]
    if len(nz) > 0:
        q20 = float(np.quantile(nz, 0.2))
        q80 = float(np.quantile(nz, 0.8))
        ext_mask = (absf > 0) & (absf >= q80)
        neu_mask = (absf == 0) | ((absf > 0) & (absf <= q20))
    else:
        ext_mask = pd.Series(False, index=g.index)
        neu_mask = absf == 0 if len(g) else pd.Series(dtype=bool)

    ext = g.loc[ext_mask, "ret"] if len(g) else pd.Series(dtype=float)
    neu = g.loc[neu_mask, "ret"] if len(g) else pd.Series(dtype=float)
    n_ext, n_neu = int(len(ext)), int(len(neu))

    diff = float(ext.mean() - neu.mean()) if n_ext > 0 and n_neu > 0 else None
    tval = None
    if n_ext >= 2 and n_neu >= 2:
        t = stats.ttest_ind(ext.values, neu.values, equal_var=False).statistic
        if np.isfinite(t):
            tval = float(t)

    # ---------- supporting check: same sign in at least 2 of the coins ----------
    coin_diffs = {}
    for coin in bars:
        e = g.loc[ext_mask & (g["coin"] == coin), "ret"]
        n = g.loc[neu_mask & (g["coin"] == coin), "ret"]
        if len(e) > 0 and len(n) > 0:
            coin_diffs[coin] = float(e.mean() - n.mean())
    if diff is not None and diff != 0:
        same = sum(1 for v in coin_diffs.values() if np.sign(v) == np.sign(diff))
        sup_passed = bool(same >= 2)
        sup_val = float(same)
    else:
        sup_passed, sup_val = None, None

    counts = {
        "non-overlapping extreme cases": n_ext,
        "non-overlapping neutral cases": n_neu,
        "coins": int(len(bars)),
    }

    if n_ext < 30:
        status = "not observable"
        decided = f"Only {n_ext} non-overlapping extreme cases, fewer than the plan's minimum of 30."
    elif tval is None or diff is None:
        status = "not observable"
        decided = "Too few neutral cases to compute the Welch t of the difference."
    elif diff < 0 and tval <= -2:
        status = "confirmed"
        decided = "The return after extremes minus after neutral readings is negative with t <= -2 (continuation)."
    elif diff > 0 and tval >= 2:
        status = "rejected"
        decided = "The difference is positive with t >= +2, meaning reversal rather than continuation."
    else:
        status = "inconclusive"
        decided = "The Welch t of the difference lies between -2 and +2."

    reading = ("Quintiles of |forecast| are taken over the nonzero-forecast grid bars pooled across coins and windows "
               "(extreme = at or above the 80th percentile, neutral = forecast 0 or at or below the 20th percentile), "
               "the supporting check counts the coins present (2 of the record's coins) whose difference has the pooled sign "
               "and is reported without entering the decision since the confirm rule does not name it, "
               "and a missing Welch t for lack of neutral cases is treated as not observable.")

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": diff,
            "statistic": {"name": "Welch t", "value": tval} if tval is not None else None,
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "coins whose difference has the pooled sign (need >= 2)",
            "value": sup_val,
            "passed": sup_passed,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
