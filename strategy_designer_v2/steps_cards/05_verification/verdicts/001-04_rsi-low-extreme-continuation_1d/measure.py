import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    RAW = "debug_info.components.rsi_low.last_history_value"

    # ---------- 1. Situation check: RSI(14) < 50 (raw value > 0), expected side short ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if "forecast" not in df.columns or RAW not in df.columns:
                continue
            d = df[["forecast", RAW]].dropna()
            act = d["forecast"] != 0
            n_active += int(act.sum())
            # raw = (50 - RSI) * 0.4 -> RSI < 50 iff raw > 0
            situation = d[RAW] > 0
            n_agree += int((act & situation & (d["forecast"] < 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "mean forward 5-bar return after top-quintile |forecast| minus after neutral bars"
    threshold = "confirm if difference < 0 with Welch t <= -2; reject if difference > 0 with t >= +2"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": "Fewer than 90% of active bars are short bars with RSI(14) below 50, so the config does not "
                          "implement the plan's graded short on low RSI.",
            "reading": "none",
        }

    # ---------- 2. Non-overlapping 5-bar grid, forward returns within each window ----------
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            if "forecast" not in df.columns or "close" not in df.columns:
                continue
            close = df["close"].to_numpy(dtype=float)
            fc = df["forecast"].to_numpy(dtype=float)
            n = len(df)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                c0, c1, f = close[i], close[i + H], fc[i]
                if not (np.isfinite(c0) and np.isfinite(c1) and np.isfinite(f)) or c0 == 0:
                    continue
                rows.append((coin, f, c1 / c0 - 1.0))
    grid = pd.DataFrame(rows, columns=["coin", "forecast", "ret"])

    absf = grid["forecast"].abs() if len(grid) else pd.Series(dtype=float)
    active_abs = absf[absf > 0]
    if len(active_abs) > 0:
        q80 = float(np.quantile(active_abs, 0.8))
        q20 = float(np.quantile(active_abs, 0.2))
        ext_mask = (absf > 0) & (absf >= q80)
        neu_mask = (absf == 0) | ((absf > 0) & (absf <= q20) & ~ext_mask)
    else:
        ext_mask = pd.Series(False, index=grid.index)
        neu_mask = absf == 0 if len(grid) else pd.Series(dtype=bool)

    ext = grid.loc[ext_mask, "ret"].to_numpy() if len(grid) else np.array([])
    neu = grid.loc[neu_mask, "ret"].to_numpy() if len(grid) else np.array([])
    n_ext, n_neu = len(ext), len(neu)

    diff = None
    t = None
    if n_ext >= 2 and n_neu >= 2:
        diff = float(ext.mean() - neu.mean())
        tt = stats.ttest_ind(ext, neu, equal_var=False).statistic
        t = float(tt) if np.isfinite(tt) else None
    elif n_ext >= 1 and n_neu >= 1:
        diff = float(ext.mean() - neu.mean())

    # ---------- Supporting check: same sign in at least 2 of the 3 coins ----------
    coin_diffs = {}
    if len(grid):
        for coin in grid["coin"].unique():
            m = grid["coin"] == coin
            e = grid.loc[m & ext_mask, "ret"]
            nn = grid.loc[m & neu_mask, "ret"]
            if len(e) > 0 and len(nn) > 0:
                coin_diffs[coin] = float(e.mean() - nn.mean())
    sup_passed = None
    n_same = None
    if diff is not None and diff != 0:
        n_same = int(sum(1 for v in coin_diffs.values() if np.sign(v) == np.sign(diff)))
        sup_passed = bool(n_same >= 2)

    # ---------- Decision ----------
    if n_ext < 30:
        status = "inconclusive"
        decided = f"Fewer than 30 non-overlapping extreme cases in total ({n_ext}), so the result is inconclusive."
    elif t is None or diff is None:
        status = "inconclusive"
        decided = "The Welch t could not be computed, so the result is inconclusive."
    elif diff < 0 and t <= -2:
        status = "confirmed"
        decided = "The forward return after extremes minus after neutral readings is negative with t <= -2."
    elif diff > 0 and t >= 2:
        status = "rejected"
        decided = "The difference is positive with t >= +2, meaning reversal rather than continuation."
    else:
        status = "inconclusive"
        decided = "The t-statistic lies between -2 and +2, so the result is inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": diff,
            "statistic": {"name": "Welch t", "value": t} if t is not None else None,
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "coins with the same sign of the difference (need >= 2)",
            "value": n_same,
            "passed": sup_passed,
        },
        "counts": {
            "non-overlapping extreme cases": int(n_ext),
            "non-overlapping neutral cases": int(n_neu),
            "coins": int(len(coin_diffs)),
        },
        "decided_by": decided,
        "reading": "Quintiles of |forecast| are taken over the pooled non-zero-forecast bars on the 5-bar grid "
                   "(top = at or above the 80th percentile, neutral = forecast 0 or at or below the 20th percentile), "
                   "and the supporting check requires at least 2 coins with the pooled sign among the coins "
                   "present (both of the 2 here). It is reported but does not gate the plan's confirm/reject rule.",
    }
