import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    UP = "debug_info.components.up_move.last_history_value"

    # ---------- 1. Situation check ----------
    # Situation: the coin's 1-day return has a nonzero size, so |return| > 0.
    # Expected side: long, so forecast > 0.
    active_total = 0
    active_ok = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            ret1 = df["close"].astype(float).pct_change()
            if UP in df.columns:
                raw = pd.to_numeric(df[UP], errors="coerce")
                raw = raw.where(raw.notna(), ret1)
            else:
                raw = ret1
            active = fc.notna() & (fc != 0)
            situation = raw.notna() & (raw.abs() > 0)
            ok = active & situation & (fc > 0)
            active_total += int(active.sum())
            active_ok += int(ok.sum())
    agreement = float(active_ok / active_total) if active_total > 0 else 0.0
    passed = active_total > 0 and agreement >= 0.90

    main_name = "top-third minus bottom-third mean excess 5-day return"
    threshold = ("confirm if difference > 0 with Welch t >= 2 and top third beats holding; "
                 "reject if difference < 0 with Welch t <= -2")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None,
                             "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(active_total)},
            "decided_by": ("Fewer than 90% of the bars with a nonzero forecast have a nonzero "
                           "1-day move with a long (positive) forecast, as the plan's Fidelity "
                           "requires."),
            "reading": "The situation is taken as a nonzero 1-day return (raw component value) and the side as long.",
        }

    # ---------- 2. Criterion ----------
    rows = []
    for coin, wins in bars.items():
        coin_rows = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float).values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            n = len(df)
            for t in range(0, n, H):
                if t + H >= n:
                    continue
                c0, c1 = close[t], close[t + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                coin_rows.append((coin, w, t, float(fc[t]), c1 / c0 - 1.0))
        if not coin_rows:
            continue
        drift = float(np.mean([r[4] for r in coin_rows]))
        for (c, w, t, f, r) in coin_rows:
            if np.isfinite(f):
                rows.append((c, w, t, f, r - drift))

    total = len(rows)
    if total > 0:
        d = pd.DataFrame(rows, columns=["coin", "window", "pos", "forecast", "excess"])
        d = d.sort_values(["forecast", "coin", "window", "pos"], kind="mergesort").reset_index(drop=True)
        k = total // 3
        bottom = d["excess"].values[:k]
        top = d["excess"].values[total - k:] if k > 0 else np.array([])
    else:
        bottom = np.array([])
        top = np.array([])

    n_top, n_bot = int(len(top)), int(len(bottom))
    counts = {"grid cases in top third": n_top, "grid cases in bottom third": n_bot,
              "grid cases in total": int(total)}
    reading = ("Thirds are taken by rank of the pooled grid forecasts (stable sort, floor(n/3) cases each, "
               "ties broken by coin, window and position), grid points with forecast 0 included, and the drift is "
               "each coin's mean of its non-overlapping 5-day grid returns over all its windows.")

    if n_top < 100 or n_bot < 100:
        return {
            "status": "not observable",
            "situation_check": {"agreement": agreement, "passed": True},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": {"name": "top-third mean excess 5-day return > 0", "value": None, "passed": None},
            "counts": counts,
            "decided_by": "The plan's minimum of 100 grid cases in each of the top and bottom thirds is not reached.",
            "reading": reading,
        }

    diff = float(np.mean(top) - np.mean(bottom))
    tstat = float(stats.ttest_ind(top, bottom, equal_var=False).statistic)
    top_mean = float(np.mean(top))
    support = bool(top_mean > 0)

    if diff > 0 and tstat >= 2 and support:
        status = "confirmed"
        decided = "The top-minus-bottom difference is positive with Welch t >= 2 and the top third beats holding."
    elif diff < 0 and tstat <= -2:
        status = "rejected"
        decided = "The top-minus-bottom difference is negative with Welch t <= -2."
    elif diff > 0 and tstat >= 2 and not support:
        status = "inconclusive"
        decided = "Welch t >= 2 but the top third's mean excess return is not above 0, which the plan calls inconclusive."
    else:
        status = "inconclusive"
        decided = "Welch t lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": diff,
                         "statistic": {"name": "Welch t", "value": tstat},
                         "threshold": threshold},
        "supporting_check": {"name": "top-third mean excess 5-day return > 0",
                             "value": top_mean, "passed": support},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
