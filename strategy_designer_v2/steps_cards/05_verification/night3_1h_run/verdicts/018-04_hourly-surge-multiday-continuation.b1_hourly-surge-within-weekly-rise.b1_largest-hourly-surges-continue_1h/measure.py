import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 120
    BAND = 2.0
    SURGE_COL = "debug_info.components.surge.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = df["close"].astype(float)
            fc = df["forecast"].astype(float).fillna(0.0)

            # 168-bar return, inside the window only
            week = close / close.shift(168) - 1.0
            # where it cannot be recomputed (first 168 bars), use the detector's own decision
            week_pos = (week > 0) & week.notna()
            week_pos = week_pos | (week.isna() & (df["regime"].astype(str) == "trending"))

            # 24-bar return: raw component value, recomputed from prices if missing
            if SURGE_COL in df.columns:
                surge = df[SURGE_COL].astype(float)
            else:
                surge = pd.Series(np.nan, index=df.index)
            surge_px = close / close.shift(24) - 1.0
            surge = surge.where(surge.notna(), surge_px)
            surge_pos = (surge > 0) & surge.notna()

            active = fc != 0
            ok = active & (fc > 0) & week_pos & surge_pos
            n_active += int(active.sum())
            n_agree += int(ok.sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "mean 120-bar excess return over the coin's normal drift, per bet case"
    threshold = "mean > 0 with t >= 2 and >= 30 cases (confirm); mean < 0 with t <= -2 and >= 30 cases (reject)"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"cases": 0, "active_bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars with a positive "
                           "24-bar return while the 168-bar return is positive, which the plan's Fidelity requires."
                           if n_active > 0 else "The forecast is never non-zero, so no bar shows the plan's situation."),
            "reading": "The situation is a positive 24-bar return (raw surge value) with a positive 168-bar return "
                       "recomputed from closes (the regime column where 168 prior bars are not recorded), on the long side.",
        }

    # ---------- 2. criterion ----------
    excess_all = []
    fc_all = []
    for coin, wins in bars.items():
        # normal drift: mean non-overlapping 120-bar return over all windows of the coin
        grid_rets = []
        for w, df in wins.items():
            close = df.sort_values("timestamp")["close"].astype(float).to_numpy()
            for k in range(0, len(close) - H, H):
                if np.isfinite(close[k]) and np.isfinite(close[k + H]) and close[k] > 0:
                    grid_rets.append(close[k + H] / close[k] - 1.0)
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))

        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = df["close"].astype(float).to_numpy()
            fc = df["forecast"].astype(float).fillna(0.0).to_numpy()
            n = len(df)

            # bets: rises of the long forecast of at least BAND from its low since last bet
            bets = []
            low = 0.0
            for i in range(n):
                f = fc[i]
                if f <= 0:
                    low = 0.0
                    continue
                if f - low >= BAND:
                    bets.append(i)
                    low = f
                else:
                    low = min(low, f)

            # one case per 120-bar grid cell: the first bet in the cell
            seen = set()
            for i in bets:
                cell = i // H
                if cell in seen:
                    continue
                seen.add(cell)
                if i + H >= n:
                    continue
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 <= 0:
                    continue
                excess_all.append((c1 / c0 - 1.0) - drift)
                fc_all.append(fc[i])

    ex = np.asarray(excess_all, dtype=float)
    fcs = np.asarray(fc_all, dtype=float)
    n_cases = int(len(ex))

    mean_ex = float(np.mean(ex)) if n_cases > 0 else None
    t_val = None
    if n_cases >= 2:
        sd = float(np.std(ex, ddof=1))
        t_val = float(mean_ex / (sd / np.sqrt(n_cases))) if sd > 0 else None

    hi = ex[fcs >= 10]
    lo = ex[fcs < 10]
    n_hi, n_lo = int(len(hi)), int(len(lo))
    diff = None
    welch_t = None
    sup_passed = None
    if n_hi > 0 and n_lo > 0:
        diff = float(np.mean(hi) - np.mean(lo))
        sup_passed = bool(diff > 0)
        if n_hi >= 2 and n_lo >= 2:
            r = stats.ttest_ind(hi, lo, equal_var=False)
            if np.isfinite(r.statistic):
                welch_t = float(r.statistic)

    counts = {"cases": n_cases, "cases_forecast_ge_10": n_hi, "cases_forecast_lt_10": n_lo}

    if n_cases < 30:
        status = "not observable"
        decided = f"Only {n_cases} cases, fewer than the plan's minimum of 30."
    elif t_val is None:
        status = "inconclusive"
        decided = "The t of the mean could not be computed (no spread), so neither confirm nor reject is met."
    elif mean_ex > 0 and t_val >= 2:
        if sup_passed:
            status = "confirmed"
            decided = "Mean excess above 0 with t >= 2 on at least 30 cases, and cases with forecast >= 10 beat those below 10."
        else:
            status = "inconclusive"
            decided = "Mean excess above 0 with t >= 2, but the supporting check fails, which the plan calls inconclusive."
    elif mean_ex < 0 and t_val <= -2:
        status = "rejected"
        decided = "Mean excess below 0 with t <= -2 on at least 30 cases."
    else:
        status = "inconclusive"
        decided = "The t of the mean lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_ex,
            "statistic": {"name": "t of the mean", "value": t_val} if t_val is not None else None,
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "mean excess (forecast >= 10) minus mean excess (forecast < 10), Welch",
            "value": diff,
            "welch_t": welch_t,
            "passed": sup_passed,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": ("A case is the first bet (forecast rise >= 2 from its long-side low since the last bet) in each "
                    "120-bar grid cell counted from the window's first row, its forecast is the forecast at that bar, "
                    "the drift is the coin's mean non-overlapping 120-bar return over all its windows, and the supporting "
                    "check passes when the difference of means is above 0 (the Welch t is reported, not thresholded)."),
    }
