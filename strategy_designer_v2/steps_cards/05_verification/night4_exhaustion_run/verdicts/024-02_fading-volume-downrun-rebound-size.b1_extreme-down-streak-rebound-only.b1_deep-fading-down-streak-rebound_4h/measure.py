import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 18
    BAND = 2.0
    MIN_CASES = 30

    def down_streak_fade(close, volume):
        """Per bar: True if the bar closed down as part of a down-streak of >= 2 bars
        (inside the window) and the volume slope across the streak's bars is negative."""
        n = len(close)
        out = np.zeros(n, dtype=bool)
        streak = 0
        for i in range(n):
            if i > 0 and np.isfinite(close[i]) and np.isfinite(close[i - 1]) and close[i] < close[i - 1]:
                streak += 1
            else:
                streak = 0
            if streak >= 2:
                L = min(streak, 180)
                v = volume[i - L + 1:i + 1]
                if np.all(np.isfinite(v)):
                    x = np.arange(L, dtype=float)
                    xm = x - x.mean()
                    slope = np.sum(xm * (v - v.mean())) / np.sum(xm * xm)
                    out[i] = slope < 0
        return out

    # ---------- situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            close = df["close"].astype(float).to_numpy()
            vol = df["volume"].astype(float).to_numpy()
            fc = df["forecast"].astype(float).fillna(0.0).to_numpy()
            sit = down_streak_fade(close, vol)
            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & sit & (fc > 0)).sum())
    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9

    main_name = "mean 18-bar excess return (return minus the coin's normal 18-bar drift) over bet cases"
    threshold = "confirm: mean > 0 with t >= 2 on >= 30 cases and correlation > 0; reject: mean < 0 with t <= -2 on >= 30 cases"
    reading = ("Down-streak = consecutive closes below the previous close inside the window, volume slope = OLS slope of the "
               "streak's down bars' volumes; a bet is a rise of the forecast of >= 2 points above its lowest long level since "
               "the last bet (reset to 0 when flat), the first bet of each 18-bar grid cell (from the window's first row) is the "
               "case, cases without 18 bars ahead in the window are dropped, and the drift is the coin's mean return over "
               "non-overlapping 18-bar grid stretches of all its windows.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement) if agreement is not None else None, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"cases": 0},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars of a fading-volume down-streak "
                           "of at least two bars, as the plan's situation requires"
                           if n_active > 0 else "The forecast is never non-zero, so the plan's situation is never traded."),
            "reading": reading,
        }

    # ---------- drift per coin ----------
    drift = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            close = df["close"].astype(float).to_numpy()
            for p in range(0, len(close) - H, H):
                a, b = close[p], close[p + H]
                if np.isfinite(a) and np.isfinite(b) and a > 0:
                    rets.append(b / a - 1.0)
        drift[coin] = float(np.mean(rets)) if rets else np.nan

    # ---------- cases ----------
    excess = []
    fcs = []
    for coin, wins in bars.items():
        d = drift[coin]
        for w, df in wins.items():
            close = df["close"].astype(float).to_numpy()
            fc = df["forecast"].astype(float).fillna(0.0).to_numpy()
            n = len(fc)
            low = 0.0
            used_cells = set()
            for i in range(n):
                f = fc[i]
                if f <= 0:
                    low = 0.0
                    continue
                low = min(low, f)
                if f - low >= BAND:
                    low = f
                    cell = i // H
                    if cell in used_cells:
                        continue
                    used_cells.add(cell)
                    if i + H < n and np.isfinite(close[i]) and np.isfinite(close[i + H]) and close[i] > 0 and np.isfinite(d):
                        r = close[i + H] / close[i] - 1.0
                        excess.append(r - d)
                        fcs.append(f)

    excess = np.asarray(excess, dtype=float)
    fcs = np.asarray(fcs, dtype=float)
    n_cases = int(len(excess))

    mean_ex = float(np.mean(excess)) if n_cases > 0 else None
    t = None
    if n_cases > 1:
        sd = np.std(excess, ddof=1)
        t = float(mean_ex / (sd / np.sqrt(n_cases))) if sd > 0 else None
    corr = None
    if n_cases > 2 and np.std(fcs) > 0 and np.std(excess) > 0:
        corr = float(np.corrcoef(fcs, excess)[0, 1])

    if n_cases < MIN_CASES:
        status = "not observable"
        decided_by = f"Only {n_cases} cases, below the plan's minimum of 30 cases."
    elif t is not None and mean_ex > 0 and t >= 2:
        if corr is not None and corr > 0:
            status = "confirmed"
            decided_by = "The mean excess return is positive with t >= 2 on at least 30 cases and the forecast/excess-return correlation is above 0."
        else:
            status = "inconclusive"
            decided_by = "The mean excess return has t >= 2 but the supporting correlation is 0 or below, which the plan calls inconclusive."
    elif t is not None and mean_ex < 0 and t <= -2:
        status = "rejected"
        decided_by = "The mean excess return is negative with t <= -2 on at least 30 cases."
    else:
        status = "inconclusive"
        decided_by = "The t-statistic of the mean excess return lies between -2 and 2 (or is undefined), which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_ex,
            "statistic": {"name": "t of the mean", "value": t} if t is not None else None,
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "correlation of forecast at signal bar with 18-bar excess return",
            "value": corr,
            "passed": (bool(corr > 0) if corr is not None else None),
        },
        "counts": {"cases": n_cases},
        "decided_by": decided_by,
        "reading": reading,
    }
