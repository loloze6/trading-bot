import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 72
    FC = "forecast"

    # ---------- 1. Situation check: 72-bar fall regime, short side ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df[FC], errors="coerce").to_numpy(dtype=float)
            n = len(close)
            fall = np.full(n, np.nan)
            if n > H:
                fall[H:] = close[H:] / close[:-H] - 1.0
            active = np.isfinite(fc) & (fc != 0) & np.isfinite(fall)
            n_active += int(active.sum())
            n_agree += int((active & (fall < 0) & (fc < 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "pooled OLS slope of 72-bar excess forward return on forecast, trending grid bars"
    threshold = "confirm: slope > 0 with t >= 2; reject: slope < 0 with t <= -2; otherwise inconclusive; at least 200 grid cases"
    reading = ("Situation bars are those whose 72-bar close-to-close return inside the window is below zero "
               "(active bars without 72 bars of window history are left out) and the expected side is short; "
               "grid bars are positions 0, 72, 144, ... of each window whose recorded regime is 'trending', "
               "the coin's mean 72-bar return is the mean over all grid bars of all its windows, and the "
               "plan's 'fewer than 200 grid cases' is treated as the minimum count (not observable).")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"grid cases in the fallen regime": None},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are short bars inside a 72-bar fall "
                           f"(agreement {agreement:.3f}), so the config does not do what the plan's situation says."),
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    xs, ys = [], []
    for coin, wins in bars.items():
        all_rets = []
        rows = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df[FC], errors="coerce").to_numpy(dtype=float)
            reg = df["regime"].astype(str).to_numpy()
            n = len(close)
            for i in range(0, n - H, H):
                r = close[i + H] / close[i] - 1.0
                if not np.isfinite(r):
                    continue
                all_rets.append(r)
                if reg[i] == "trending" and np.isfinite(fc[i]):
                    rows.append((fc[i], r))
        if len(all_rets) == 0:
            continue
        mu = float(np.mean(all_rets))
        for f, r in rows:
            xs.append(f)
            ys.append(r - mu)

    n_cases = len(xs)
    counts = {"grid cases in the fallen regime": int(n_cases)}

    if n_cases < 200:
        return {
            "status": "not observable",
            "situation_check": {"agreement": agreement, "passed": True},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": counts,
            "decided_by": f"Only {n_cases} grid cases in the fallen regime, fewer than the plan's minimum of 200.",
            "reading": reading,
        }

    x = np.asarray(xs, dtype=float)
    y = np.asarray(ys, dtype=float)
    slope, t = None, None
    if np.std(x) > 0:
        lr = stats.linregress(x, y)
        slope = float(lr.slope)
        if lr.stderr is not None and np.isfinite(lr.stderr) and lr.stderr > 0:
            t = float(lr.slope / lr.stderr)

    if slope is None or t is None or not np.isfinite(t):
        status = "inconclusive"
        decided = "The forecast does not vary over the grid cases, so no slope t can be formed; neither rule is met."
    elif slope > 0 and t >= 2:
        status = "confirmed"
        decided = f"The slope is positive with t = {t:.2f} >= 2 over {n_cases} grid cases (confirm rule)."
    elif slope < 0 and t <= -2:
        status = "rejected"
        decided = f"The slope is negative with t = {t:.2f} <= -2 over {n_cases} grid cases (reject rule)."
    else:
        status = "inconclusive"
        decided = f"The slope's t = {t:.2f} lies between -2 and 2 over {n_cases} grid cases (inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": slope,
            "statistic": {"name": "OLS slope t", "value": t} if t is not None else None,
            "threshold": threshold,
        },
        "supporting_check": None,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
