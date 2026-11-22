import numpy as np
import pandas as pd


def measure(bars):
    H = 18
    BAND = 2.0
    MIN_CASES = 30
    SL = "debug_info.components.streak_loss.last_history_value"
    VF = "debug_info.components.volume_fade.last_history_value"

    def _wkey(w):
        try:
            return int(str(w).lstrip("w"))
        except Exception:
            return 0

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin in sorted(bars):
        for w in sorted(bars[coin], key=_wkey):
            df = bars[coin][w].reset_index(drop=True)
            if len(df) == 0:
                continue
            close = df["close"].astype(float).values
            fc = df["forecast"].astype(float).values
            down = np.zeros(len(df), dtype=bool)
            down[1:] = close[1:] < close[:-1]
            # first bar of a window: no previous close inside the window, use the raw streak loss
            if SL in df.columns:
                v0 = df[SL].iloc[0]
                down[0] = bool(pd.notna(v0) and float(v0) != 0.0)
            active = np.isfinite(fc) & (fc != 0)
            n_active += int(active.sum())
            n_agree += int((active & down & (fc > 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    sit_passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "mean 18-bar excess return of long bets over the coin's normal 18-bar drift"
    threshold = "confirm: mean > 0 with t >= 2 over >= 30 cases; reject: mean < 0 with t <= -2 over >= 30 cases"

    if not sit_passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"cases": 0, "active_bars": n_active},
            "decided_by": ("The plan's situation is a running down-streak (bar closes down) with a long forecast, "
                           "but fewer than 90% of the bars with a non-zero forecast are down-streak bars with a "
                           "positive forecast."),
            "reading": "Situation taken as any bar closing below the previous close (graded dead zone, so no size cut-off), expected side long.",
        }

    # ---------- 2. criterion ----------
    excess = []
    fades = []
    for coin in sorted(bars):
        wins = sorted(bars[coin], key=_wkey)
        # normal drift: mean of non-overlapping 18-bar returns over all windows
        grid_rets = []
        for w in wins:
            close = bars[coin][w]["close"].astype(float).values
            for p in range(0, len(close) - H, H):
                a, b = close[p], close[p + H]
                if np.isfinite(a) and np.isfinite(b) and a > 0:
                    grid_rets.append(b / a - 1.0)
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))

        for w in wins:
            df = bars[coin][w].reset_index(drop=True)
            close = df["close"].astype(float).values
            fc = df["forecast"].astype(float).fillna(0.0).values
            vf = df[VF].astype(float).values if VF in df.columns else np.full(len(df), np.nan)
            ref = 0.0
            used_cells = set()
            for t in range(len(df)):
                f = fc[t]
                if f <= 0:
                    ref = 0.0
                    continue
                if f - ref >= BAND:
                    ref = f
                    cell = t // H
                    if cell in used_cells:
                        continue
                    used_cells.add(cell)
                    if t + H < len(df):
                        a, b = close[t], close[t + H]
                        if np.isfinite(a) and np.isfinite(b) and a > 0:
                            excess.append((b / a - 1.0) - drift)
                            fades.append(vf[t])
                else:
                    ref = min(ref, f)

    excess = np.array(excess, dtype=float)
    fades = np.array(fades, dtype=float)
    n = int(len(excess))

    mean = float(np.mean(excess)) if n > 0 else None
    tstat = None
    if n > 1:
        sd = float(np.std(excess, ddof=1))
        if sd > 0:
            tstat = float(mean / (sd / np.sqrt(n)))

    # supporting check
    sup_val = None
    sup_pass = None
    n_above = n_below = 0
    ok = np.isfinite(fades)
    if ok.sum() > 0:
        fv = fades[ok]
        ex = excess[ok]
        med = float(np.median(fv))
        above = ex[fv > med]
        below = ex[fv < med]
        n_above, n_below = int(len(above)), int(len(below))
        if n_above > 0 and n_below > 0:
            sup_val = float(np.mean(above) - np.mean(below))
            sup_pass = bool(sup_val > 0)

    counts = {"cases": n, "above_median_cases": n_above, "below_median_cases": n_below,
              "active_bars": n_active}

    if n < MIN_CASES:
        status = "not observable"
        decided = f"Only {n} cases, fewer than the plan's minimum of 30."
    elif tstat is not None and mean > 0 and tstat >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "Mean excess return above 0 with t >= 2 over at least 30 cases, and the above-minus-below-median fade difference is above 0."
        else:
            status = "inconclusive"
            decided = "The main measure confirms (mean > 0, t >= 2, >= 30 cases) but the volume-fade check fails."
    elif tstat is not None and mean < 0 and tstat <= -2:
        status = "rejected"
        decided = "Mean excess return below 0 with t <= -2 over at least 30 cases."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2 (or is undefined), meeting neither the confirm nor the reject rule."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": mean,
                         "statistic": ({"name": "ordinary t of the mean", "value": tstat} if tstat is not None else None),
                         "threshold": threshold},
        "supporting_check": {"name": "mean excess return above-median minus below-median raw volume_fade",
                             "value": sup_val, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": ("Situation = bar closing below the previous close with a positive forecast; a case is the first long bet "
                    "(forecast rise >= 2 from its lowest positive level since the last bet, reset at 0) in each 18-bar cell "
                    "counted from each window's first row, with its 18-bar return inside the window; drift = mean of the coin's "
                    "non-overlapping 18-bar returns over all windows; the median split puts cases strictly above vs strictly "
                    "below the median and drops ties; fewer than 30 cases is reported as not observable per the workflow."),
    }
