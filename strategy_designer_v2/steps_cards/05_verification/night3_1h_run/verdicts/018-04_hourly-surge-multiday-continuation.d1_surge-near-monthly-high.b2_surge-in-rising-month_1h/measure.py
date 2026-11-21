import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 240
    BAND = 2.0
    RAW = "debug_info.components.surge.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float).values
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            n = len(df)
            # 720-bar (30-day) return recomputed from prices inside the window
            ret30 = np.full(n, np.nan)
            if n > 720:
                ret30[720:] = close[720:] / close[:-720] - 1.0
            # where the window is too short to recompute, use the detector's recorded decision
            reg = df["regime"].astype(str).values if "regime" in df.columns else np.array([""] * n)
            rising = np.where(np.isnan(ret30), reg == "trending", ret30 > 0)
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce").values
            else:
                raw = np.full(n, np.nan)
            surge_up = np.nan_to_num(raw, nan=-np.inf) > 0
            active = fc != 0
            situ = rising & surge_up & (fc > 0)
            n_active += int(active.sum())
            n_agree += int((active & situ).sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "t of mean 240-bar excess return (return minus normal 240-bar drift) after forecast rises of >= 2 points"
    threshold = "confirm: mean > 0 with t >= 2 over >= 30 cases and positive slope; reject: mean < 0 with t <= -2 over >= 30 cases"
    reading = ("The situation is a positive 720-bar close-to-close return (recomputed from prices, the recorded regime "
               "used only on the first 720 bars of a window) with a positive raw surge value and a positive forecast; "
               "a case is the first bet (forecast rise >= 2 points from its lowest positive level since the last bet, "
               "from 0 after a flat) in each 240-bar grid cell counted from each window's first row, and the normal "
               "drift is the coin's mean non-overlapping 240-bar return over all its windows.")

    if agreement is not None and not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"cases": 0},
            "decided_by": ("Fewer than 90% of the active bars are bars with a positive 30-day return and an upside "
                           "surge on the long side, as the plan's Fidelity requires."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    excess = []
    fcs = []
    for coin, wins in bars.items():
        # normal drift: mean non-overlapping 240-bar return over all windows of the coin
        grid_rets = []
        for w, df in wins.items():
            c = df["close"].astype(float).values
            for p in range(0, len(c) - H, H):
                grid_rets.append(c[p + H] / c[p] - 1.0)
        grid_rets = [r for r in grid_rets if np.isfinite(r)]
        if not grid_rets:
            continue
        drift = float(np.mean(grid_rets))

        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float).values
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            n = len(df)
            # bets: rises of the forecast on the long side of at least the band
            bets = np.zeros(n, dtype=bool)
            low = 0.0
            for i in range(n):
                f = fc[i]
                if f <= 0:
                    low = 0.0
                    continue
                if f - low >= BAND:
                    bets[i] = True
                    low = f
                else:
                    low = min(low, f)
            # one case per grid cell: the first bet in the cell
            for start in range(0, n, H):
                idx = np.where(bets[start:start + H])[0]
                if len(idx) == 0:
                    continue
                t = start + int(idx[0])
                if t + H >= n:
                    continue
                r = c[t + H] / c[t] - 1.0
                if not np.isfinite(r):
                    continue
                excess.append(r - drift)
                fcs.append(float(fc[t]))

    excess = np.array(excess, dtype=float)
    fcs = np.array(fcs, dtype=float)
    ncases = int(len(excess))

    mean_ex = float(excess.mean()) if ncases > 0 else None
    tval = None
    if ncases > 1:
        sd = excess.std(ddof=1)
        tval = float(mean_ex / (sd / np.sqrt(ncases))) if sd > 0 else None
    slope = None
    if ncases > 2 and np.std(fcs) > 0:
        slope = float(stats.linregress(fcs, excess).slope)
    slope_pass = None if slope is None else bool(slope > 0)

    if ncases < 30:
        status = "not observable"
        decided = f"Fewer than 30 cases ({ncases}), the plan's minimum, so the data cannot show the idea."
    elif tval is not None and mean_ex > 0 and tval >= 2:
        if slope_pass:
            status = "confirmed"
            decided = "Mean excess return positive with t >= 2 over at least 30 cases and a positive supporting slope."
        else:
            status = "inconclusive"
            decided = "Confirming t >= 2 but the slope of excess return on forecast is not positive."
    elif tval is not None and mean_ex < 0 and tval <= -2:
        status = "rejected"
        decided = "Mean excess return negative with t <= -2 over at least 30 cases."
    else:
        status = "inconclusive"
        decided = "t lies between -2 and 2 (or cannot be computed), which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": passed},
        "main_measure": {
            "name": main_name,
            "value": mean_ex,
            "statistic": None if tval is None else {"name": "t of the mean", "value": tval},
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "slope of excess return on forecast at signal bar",
            "value": slope,
            "passed": slope_pass,
        },
        "counts": {"cases": ncases},
        "decided_by": decided,
        "reading": reading,
    }
