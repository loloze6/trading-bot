import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 10
    BAND = 2.0
    LH = "debug_info.components.rise.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.sort_values("timestamp").reset_index(drop=True)
            close = d["close"].astype(float).values
            fc = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0).values
            n = len(d)
            # 90-day return from prices inside the window; fall back to the detector's recorded regime
            r90 = np.full(n, np.nan)
            if n > 90:
                r90[90:] = close[90:] / close[:-90] - 1.0
            reg = d["regime"].astype(str).values if "regime" in d.columns else np.array([""] * n)
            trending = np.where(np.isnan(r90), reg == "trending", r90 > 0)
            # one-day rise: the component's raw value when recorded, else the price return
            r1 = np.full(n, np.nan)
            if n > 1:
                r1[1:] = close[1:] / close[:-1] - 1.0
            if LH in d.columns:
                lh = pd.to_numeric(d[LH], errors="coerce").values
                rise_sig = np.where(np.isnan(lh), r1, lh)
            else:
                rise_sig = r1
            rise = np.nan_to_num(rise_sig, nan=0.0) > 0
            situation = trending & rise
            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc > 0)).sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = True if agreement is None else bool(agreement >= 0.9)
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": "mean unusual 10-bar move over cases", "value": None,
                             "statistic": None, "threshold": "t >= 2 confirm, t <= -2 reject"},
            "supporting_check": None,
            "counts": {"cases": None},
            "decided_by": "Fewer than 90% of the bars with a non-zero forecast are long bars of an up day in a coin "
                          "with a positive 90-day return, so the config does not trade the plan's situation.",
            "reading": "The 90-day return was recomputed from closes inside each window where 90 prior bars exist, "
                       "else the recorded regime 'trending' was used; the rise is the sign of the component's raw value.",
        }

    # ---------- 2. criterion ----------
    case_moves, case_fc = [], []
    for coin, wins in bars.items():
        # coin's normal 10-bar drift over all windows, non-overlapping grid
        grid_rets = []
        prepared = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.sort_values("timestamp").reset_index(drop=True)
            close = d["close"].astype(float).values
            fc = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0).values
            n = len(d)
            for p in range(0, n - H, H):
                if np.isfinite(close[p]) and np.isfinite(close[p + H]) and close[p] > 0:
                    grid_rets.append(close[p + H] / close[p] - 1.0)
            prepared.append((close, fc, n))
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))

        for close, fc, n in prepared:
            # bets: forecast rise of >= BAND on its side from its lowest level since the last bet
            side = 0
            trough = 0.0
            bet = np.zeros(n, dtype=int)
            for i in range(n):
                f = fc[i]
                s = 1 if f > 0 else (-1 if f < 0 else 0)
                if s == 0:
                    side, trough = 0, 0.0
                    continue
                if s != side:
                    side, trough = s, 0.0
                a = abs(f)
                trough = min(trough, a)
                if a - trough >= BAND:
                    bet[i] = s
                    trough = a
            # one case per 10-bar grid cell: the first bet in the cell
            for start in range(0, n, H):
                idx = [i for i in range(start, min(start + H, n)) if bet[i] != 0]
                if not idx:
                    continue
                t = idx[0]
                if t + H >= n:
                    continue
                if not (np.isfinite(close[t]) and np.isfinite(close[t + H]) and close[t] > 0):
                    continue
                ret = close[t + H] / close[t] - 1.0
                case_moves.append(bet[t] * (ret - drift))
                case_fc.append(float(fc[t]))

    ncase = len(case_moves)
    x = np.array(case_moves, dtype=float)
    mean = float(np.mean(x)) if ncase > 0 else None
    tstat = None
    if ncase > 1:
        sd = float(np.std(x, ddof=1))
        tstat = float(mean / (sd / np.sqrt(ncase))) if sd > 0 else None
    slope = None
    if ncase > 2 and np.std(case_fc) > 0:
        slope = float(stats.linregress(np.array(case_fc), x).slope)

    if ncase < 30:
        status = "not observable"
        decided = f"Only {ncase} cases across coins and windows, fewer than the plan's minimum of 30."
    elif tstat is not None and mean > 0 and tstat >= 2 and slope is not None and slope > 0:
        status = "confirmed"
        decided = "The mean unusual move is positive with t >= 2 and the slope on the forecast is positive."
    elif tstat is not None and mean < 0 and tstat <= -2:
        status = "rejected"
        decided = "The mean unusual move is negative with t <= -2: sharp rises in rising coins are faded."
    elif tstat is not None and tstat >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the slope on the forecast is not positive."
    else:
        status = "inconclusive"
        decided = "t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": passed},
        "main_measure": {"name": "mean unusual 10-bar move over cases",
                         "value": mean,
                         "statistic": None if tstat is None else {"name": "t of the mean", "value": tstat},
                         "threshold": "confirm: mean > 0 with t >= 2 (and positive slope); reject: mean < 0 with t <= -2"},
        "supporting_check": {"name": "slope of unusual move on case forecast",
                             "value": slope,
                             "passed": None if slope is None else bool(slope > 0)},
        "counts": {"cases": ncase},
        "decided_by": decided,
        "reading": "A case is the first bet (forecast rise of >= 2 points from its lowest level on its side since "
                   "the last bet) in each 10-bar grid cell of a window, its size in the regression is the forecast "
                   "on the signal bar, the drift is the mean of the coin's non-overlapping 10-bar grid returns over "
                   "all windows, and the 90-day return is recomputed from closes where 90 prior bars exist in the "
                   "window, else read from the recorded regime.",
    }
