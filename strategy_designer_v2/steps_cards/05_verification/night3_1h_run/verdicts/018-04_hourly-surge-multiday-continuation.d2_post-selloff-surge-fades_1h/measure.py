import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 120
    BAND = 2.0
    MIN_CASES = 30
    LHV = "debug_info.components.fall_depth.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    n_active_uncomputable = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = df["close"].astype(float)
            fc = df["forecast"].astype(float)
            # surge: 24h return over the mean absolute 24h return of the last 720 bars (inside the window)
            r24 = close / close.shift(24) - 1.0
            denom = r24.abs().rolling(720, min_periods=720).mean()
            surge = r24 / denom.replace(0.0, np.nan)
            # prior7: 168-bar return ending 24 bars earlier; its sign equals the recorded fall_depth raw value's sign
            prior7_px = close.shift(24) / close.shift(24 + 168) - 1.0
            if LHV in df.columns:
                prior7 = df[LHV].astype(float).where(df[LHV].notna(), prior7_px)
            else:
                prior7 = prior7_px
            active = fc.notna() & (fc != 0)
            computable = surge.notna() & prior7.notna()
            n_active_uncomputable += int((active & ~computable).sum())
            use = active & computable
            situ = (surge >= 3.0) & (prior7 < 0.0)
            agree = use & situ & (fc < 0)
            n_active += int(use.sum())
            n_agree += int(agree.sum())

    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.90

    reading = ("Surge is recomputed from closes as the 24-bar return over the mean absolute 24-bar return of the "
               "last 720 bars inside the window, prior7 is the recorded fall_depth raw value (same component and "
               "parameters) or its price recomputation, active bars where surge cannot be computed are left out of "
               "the agreement; a case is the first short bet (forecast falling at least 2 points below its "
               "least-negative level since the last bet, reset at flat) in each 120-bar grid cell of a window, cases "
               "are pooled over all coins, the drift is each coin's mean non-overlapping 120-bar return over all its "
               "windows, the slope is an OLS slope of shortfall on |forecast|, and fewer than 30 cases is "
               "'not observable'.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars checked": n_active, "active bars not computable": n_active_uncomputable},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are short bars where the 24h return "
                           "is at least 3 usual daily moves and the lagged 7-day return is negative."
                           if agreement is not None else
                           "No active bar on which the plan's situation could be computed."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    shortfalls = []
    depths = []
    for coin, wins in bars.items():
        # normal drift: non-overlapping 120-bar returns over all windows of the coin
        grid_rets = []
        prepared = []
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = df["close"].astype(float).values
            n = len(close)
            for p in range(0, n - H, H):
                if np.isfinite(close[p]) and np.isfinite(close[p + H]) and close[p] != 0:
                    grid_rets.append(close[p + H] / close[p] - 1.0)
            prepared.append(df)
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))

        for df in prepared:
            close = df["close"].astype(float).values
            fc = df["forecast"].astype(float).fillna(0.0).values
            n = len(fc)
            ref = 0.0
            prev = 0.0
            seen_cells = set()
            for t in range(n):
                f = fc[t]
                bet = False
                if f >= 0:
                    ref = 0.0
                else:
                    if prev >= 0:
                        ref = 0.0
                    if ref - f >= BAND:
                        bet = True
                        ref = f
                    else:
                        ref = max(ref, f)
                prev = f
                if bet:
                    cell = t // H
                    if cell in seen_cells:
                        continue
                    seen_cells.add(cell)
                    if t + H < n and np.isfinite(close[t]) and np.isfinite(close[t + H]) and close[t] != 0:
                        ret = close[t + H] / close[t] - 1.0
                        shortfalls.append(-(ret - drift))
                        depths.append(abs(f))

    n_cases = len(shortfalls)
    sf = np.array(shortfalls, dtype=float)
    dp = np.array(depths, dtype=float)

    mean_sf = float(sf.mean()) if n_cases > 0 else None
    t_val = None
    if n_cases >= 2:
        sd = sf.std(ddof=1)
        if sd > 0:
            t_val = float(mean_sf / (sd / np.sqrt(n_cases)))
    slope = None
    if n_cases >= 3 and np.std(dp) > 0:
        slope = float(stats.linregress(dp, sf).slope)

    main = {
        "name": "mean 120-bar shortfall vs normal drift, short direction, before costs",
        "value": mean_sf,
        "statistic": {"name": "t of the mean", "value": t_val} if t_val is not None else None,
        "threshold": "confirm: mean > 0 with t >= 2 over at least 30 cases; reject: t <= -2 over at least 30 cases",
    }
    support = {
        "name": "slope of shortfall on absolute forecast (fall depth)",
        "value": slope,
        "passed": (slope > 0) if slope is not None else None,
    }
    counts = {"cases": n_cases}

    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"Only {n_cases} cases, fewer than the plan's minimum of 30."
    elif t_val is None:
        status = "inconclusive"
        decided = "The t of the mean could not be computed (no dispersion), meeting neither confirm nor reject."
    elif mean_sf > 0 and t_val >= 2:
        if slope is not None and slope > 0:
            status = "confirmed"
            decided = "Mean shortfall above 0 with t >= 2 over at least 30 cases, and the depth slope is above 0."
        else:
            status = "inconclusive"
            decided = "A confirming mean shortfall but a depth slope of 0 or below (or not computable)."
    elif t_val <= -2:
        status = "rejected"
        decided = "Mean shortfall has t <= -2 over at least 30 cases: the price rose more than its usual drift."
    else:
        status = "inconclusive"
        decided = "The t of the mean shortfall lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": support,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
