import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 120          # horizon in bars
    WEEK = 168       # weekly gate
    BAND = 2.0       # bet band, forecast points
    SURGE_COL = "debug_info.components.surge.last_history_value"

    # ---------------- 1. situation check ----------------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            close = df["close"].astype(float).reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).reset_index(drop=True)
            week = close / close.shift(WEEK) - 1.0
            regime = df["regime"].astype(str).reset_index(drop=True)
            # weekly gate: recomputed from closes; where 168 past closes are not in the window, the regime's decision
            week_pos = np.where(week.notna(), week > 0, regime == "trending")
            if SURGE_COL in df.columns:
                surge = pd.to_numeric(df[SURGE_COL], errors="coerce").reset_index(drop=True)
            else:
                surge = pd.Series(np.nan, index=close.index)
            surge_re = close / close.shift(24) - 1.0
            surge_val = surge.where(surge.notna(), surge_re)
            surge_pos = (surge_val > 0).fillna(False).values
            active = (fc != 0).values
            ok = active & week_pos & surge_pos & (fc > 0).values
            n_active += int(active.sum())
            n_agree += int(ok.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "mean unusual 120-bar move of the bets (return minus the coin's normal 120-bar drift)"
    main_thr = "confirm: mean > 0 with t >= 2 over at least 30 cases; reject: t <= -2 over at least 30 cases"
    sup_name = "above-median minus below-median 168-bar-return half, in unusual move (Welch t)"
    reading = ("Situation bars are those with a positive 168-bar return recomputed from closes (the recorded regime where "
               "fewer than 168 past closes exist in the window) and a positive 24-bar surge, on the long side; cases are "
               "the first bet of each 120-bar grid cell per window, pooled over all coins with each coin's own drift; "
               "the halves are cases with 168-bar return strictly above the median versus at or below it; the plan's "
               "minimum counts (30 cases, 15 per half) not reached give 'not observable' as the workflow requires.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars with a positive 168-bar "
                           "return and a positive 24-bar surge, as the plan's situation requires."),
            "reading": reading,
        }

    # ---------------- 2. criterion ----------------
    unusual = []
    week_at = []
    for coin, wins in bars.items():
        # normal drift: mean of non-overlapping 120-bar returns over all windows of the coin
        grid_rets = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            c = df["close"].astype(float).values
            for p in range(0, len(c) - H, H):
                if c[p] > 0 and np.isfinite(c[p]) and np.isfinite(c[p + H]):
                    grid_rets.append(c[p + H] / c[p] - 1.0)
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))

        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            c = df["close"].astype(float).values
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            n = len(c)
            # bets: a rise of the long forecast of at least BAND from its lowest level since the last bet
            bets = []
            low = 0.0
            for t in range(n):
                f = fc[t]
                if f > 0:
                    if f - low >= BAND:
                        bets.append(t)
                        low = f
                    else:
                        low = min(low, f)
                else:
                    low = 0.0
            # once per 120-bar grid cell
            seen = set()
            for t in bets:
                cell = t // H
                if cell in seen:
                    continue
                seen.add(cell)
                if t + H >= n:
                    continue
                if not (np.isfinite(c[t]) and np.isfinite(c[t + H]) and c[t] > 0):
                    continue
                r = c[t + H] / c[t] - 1.0
                unusual.append(r - drift)
                if t >= WEEK and np.isfinite(c[t - WEEK]) and c[t - WEEK] > 0:
                    week_at.append(c[t] / c[t - WEEK] - 1.0)
                else:
                    week_at.append(np.nan)

    u = np.array(unusual, dtype=float)
    wk = np.array(week_at, dtype=float)
    n_cases = int(len(u))
    mean_u = float(np.mean(u)) if n_cases > 0 else None
    t_main = None
    if n_cases >= 2:
        sd = np.std(u, ddof=1)
        t_main = float(mean_u / (sd / np.sqrt(n_cases))) if sd > 0 else None

    mask = np.isfinite(wk)
    n_above = n_below = 0
    diff = None
    t_w = None
    if mask.sum() > 0:
        med = np.median(wk[mask])
        above = u[mask][wk[mask] > med]
        below = u[mask][wk[mask] <= med]
        n_above, n_below = int(len(above)), int(len(below))
        if n_above > 0 and n_below > 0:
            diff = float(np.mean(above) - np.mean(below))
        if n_above >= 2 and n_below >= 2:
            tw = stats.ttest_ind(above, below, equal_var=False).statistic
            t_w = float(tw) if np.isfinite(tw) else None

    counts = {"cases": n_cases, "above-median half": n_above, "below-median half": n_below}

    if n_cases < 30 or n_above < 15 or n_below < 15:
        status = "not observable"
        decided = ("A minimum count is not reached: %d cases (30 needed), %d above-median and %d below-median "
                   "(15 needed in each half)." % (n_cases, n_above, n_below))
        sup_pass = None
    else:
        sup_pass = bool(diff is not None and diff > 0)
        if (t_main is not None and t_main <= -2) or (t_w is not None and t_w <= -2):
            status = "rejected"
            if t_main is not None and t_main <= -2:
                decided = "Reject rule: the mean unusual move has t <= -2 over at least 30 cases."
            else:
                decided = "Reject rule: the supporting difference has Welch t <= -2."
        elif mean_u is not None and mean_u > 0 and t_main is not None and t_main >= 2 and sup_pass:
            status = "confirmed"
            decided = ("Confirm rule: the mean unusual move is positive with t >= 2 over at least 30 cases, "
                       "and the supporting difference is positive.")
        else:
            status = "inconclusive"
            if t_main is not None and t_main >= 2:
                decided = ("Inconclusive rule: main t >= 2 but the supporting difference is at or below 0 "
                           "with Welch t above -2.")
            else:
                decided = "Inconclusive rule: the main t is between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name,
                         "value": mean_u,
                         "statistic": ({"name": "t of the mean", "value": t_main} if t_main is not None else None),
                         "threshold": main_thr},
        "supporting_check": {"name": sup_name,
                             "value": diff,
                             "passed": sup_pass,
                             "welch_t": t_w},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
