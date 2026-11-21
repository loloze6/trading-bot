import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    BAND = 2.0
    MIN_CASES = 30
    RAW = "debug_info.components.support_touches.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            close = pd.to_numeric(df["close"], errors="coerce")
            raw = pd.to_numeric(df[RAW], errors="coerce") if RAW in df.columns else pd.Series(np.nan, index=df.index)
            fell = close < close.shift(H)
            lag_ok = close.shift(H).notna() & close.notna()
            active = fc.notna() & (fc != 0) & lag_ok & raw.notna()
            situ = fell & (raw > 0)
            agree = active & situ & (fc > 0)
            n_active += int(active.sum())
            n_agree += int(agree.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    reading = ("Situation = close below its close 5 bars earlier in the same window and the raw swing-low nearness "
               "count > 0, side long, with active bars lacking the 5-bar-earlier close or the raw value left out; "
               "a case is the first long bet (forecast rise >= 2 points from its lowest level since the last bet, "
               "from 0 after flat) in each 5-bar grid cell of a window, weighted by its forecast, the drift is the "
               "coin's mean 5-bar return on the grid of all its windows, and the t of the weighted mean uses the "
               "weighted (sandwich) standard error with n/(n-1) correction.")

    main_name = "forecast-weighted mean 5-bar excess return of cases"
    thr = "confirm: mean > 0 with t >= 2 and Spearman > 0; reject: t <= -2"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of active bars are long bars where the close is below its close 5 bars "
                           "ago with swing lows near the close (agreement %.3f)." % agreement),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    xs, ws = [], []
    for coin, wins in bars.items():
        # normal drift over all windows of the coin
        grid_rets = []
        for w, df in wins.items():
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            for p in range(0, len(c) - H, H):
                if np.isfinite(c[p]) and np.isfinite(c[p + H]) and c[p] > 0:
                    grid_rets.append(c[p + H] / c[p] - 1.0)
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))

        for w, df in wins.items():
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            n = len(fc)
            base = 0.0
            bets = np.zeros(n, dtype=bool)
            for i in range(n):
                f = fc[i]
                if not np.isfinite(f) or f <= 0:
                    base = 0.0
                    continue
                if f - base >= BAND:
                    bets[i] = True
                    base = f
                else:
                    base = min(base, f)
            seen = set()
            for i in range(n):
                if not bets[i]:
                    continue
                cell = i // H
                if cell in seen:
                    continue
                seen.add(cell)
                if i + H >= n:
                    continue
                if not (np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] > 0):
                    continue
                xs.append(c[i + H] / c[i] - 1.0 - drift)
                ws.append(fc[i])

    x = np.asarray(xs, dtype=float)
    wt = np.asarray(ws, dtype=float)
    ncases = int(len(x))
    counts = {"independent cases": ncases}

    mean_w = None
    tval = None
    rho = None
    if ncases >= 2 and wt.sum() > 0:
        mean_w = float(np.sum(x * wt) / np.sum(wt))
        var = np.sum(wt ** 2 * (x - mean_w) ** 2) / (np.sum(wt) ** 2) * ncases / (ncases - 1)
        se = float(np.sqrt(var))
        tval = float(mean_w / se) if se > 0 else None
        if np.std(wt) > 0 and np.std(x) > 0:
            r = stats.spearmanr(wt, x).correlation
            rho = float(r) if np.isfinite(r) else None
    elif ncases == 1 and wt.sum() > 0:
        mean_w = float(x[0])

    stat = {"name": "t of the forecast-weighted mean", "value": tval} if tval is not None else None
    sup_pass = None if rho is None else bool(rho > 0)
    sup = {"name": "Spearman(forecast, 5-bar excess return)", "value": rho, "passed": sup_pass}

    if ncases < MIN_CASES:
        status = "not observable"
        decided = "Fewer than 30 independent cases in total (%d), too few to judge." % ncases
    elif tval is None:
        status = "inconclusive"
        decided = "The t of the weighted mean could not be computed, so neither confirm nor reject is met."
    elif tval >= 2 and mean_w > 0 and sup_pass:
        status = "confirmed"
        decided = "The forecast-weighted mean excess return is positive with t >= 2 and the Spearman correlation is above 0."
    elif tval <= -2:
        status = "rejected"
        decided = "The forecast-weighted mean excess return has t <= -2."
    elif tval >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the Spearman correlation is 0 or below, which the plan calls inconclusive."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": mean_w, "statistic": stat, "threshold": thr},
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
