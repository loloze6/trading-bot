import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 10
    RAW = "debug_info.components.stretch_below.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            active = fc.notna() & (fc != 0)
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            calm = df["regime"].astype(str) == "unknown"
            below = raw < 0
            short = fc < 0
            situ = calm & below & short
            n_active += int(active.sum())
            n_agree += int((active & situ).sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = True if agreement is None else bool(agreement >= 0.9)
    situation_check = {"agreement": agreement, "passed": passed}

    reading = ("The calm market is read as the bars whose regime is 'unknown' (the detector's default, not vetoed "
               "to 'chop'), below the average as a raw stretch_below value under 0; the grid is pooled over all coins "
               "and windows, each coin's normal 10-bar drift is the mean of all its grid cells' 10-bar returns over all "
               "windows, the slope's t is the ordinary least-squares t of the pooled regression, and a count under the "
               "plan's 100-cell minimum is reported as 'not observable'.")

    main_name = "OLS t of the slope of drift-removed next-10-bar return on the forecast, negative-forecast grid cells"
    threshold = "t >= 2 confirms (with the supporting check), t <= -2 rejects, otherwise inconclusive; at least 100 cells"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": situation_check,
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": n_active, "active bars in the situation on the short side": n_agree},
            "decided_by": ("Fewer than 90 % of the bars with a non-zero forecast are calm-regime bars with the close "
                           "below its 20-day average and a short forecast, as the plan's Fidelity states."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    xs, ys = [], []
    for coin, wins in bars.items():
        cells = []  # (forecast, return)
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            n = len(df)
            for t in range(0, n, H):
                if t + H >= n:
                    break
                c0, c1 = close[t], close[t + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 <= 0:
                    continue
                cells.append((fc[t], c1 / c0 - 1.0))
        if not cells:
            continue
        rets = np.array([c[1] for c in cells], dtype=float)
        drift = float(np.mean(rets))
        for f, r in cells:
            if np.isfinite(f) and f < 0:
                xs.append(float(f))
                ys.append(float(r - drift))

    x = np.array(xs, dtype=float)
    y = np.array(ys, dtype=float)
    n_cells = int(len(x))
    counts = {"grid cells with a negative forecast": n_cells}

    slope = None
    t_slope = None
    if n_cells >= 3 and np.std(x) > 0:
        lr = stats.linregress(x, y)
        slope = float(lr.slope)
        if lr.stderr is not None and np.isfinite(lr.stderr) and lr.stderr > 0:
            t_slope = float(lr.slope / lr.stderr)

    sup_val = float(np.mean(-y)) if n_cells > 0 else None
    sup_pass = (sup_val > 0) if sup_val is not None else None

    main = {"name": main_name, "value": t_slope,
            "statistic": ({"name": "OLS t of the slope", "value": t_slope} if t_slope is not None else None),
            "threshold": threshold}
    supporting = {"name": "mean drift-removed 10-bar return in the signal's direction (short) > 0",
                  "value": sup_val, "passed": sup_pass}

    if n_cells < 100:
        status = "not observable"
        decided = f"Only {n_cells} grid cells with a negative forecast, under the plan's minimum of 100."
    elif t_slope is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed (no spread in the forecast), so it does not meet the confirm or reject rule."
    elif t_slope >= 2 and sup_pass:
        status = "confirmed"
        decided = "The slope's t is 2 or more and the mean drift-removed return in the short direction is above 0."
    elif t_slope >= 2:
        status = "inconclusive"
        decided = "The slope's t is 2 or more but the supporting check fails, which the plan calls inconclusive."
    elif t_slope <= -2:
        status = "rejected"
        decided = "The slope's t is -2 or less: a deeper stretch is followed by a larger rise."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": situation_check,
        "main_measure": main,
        "supporting_check": supporting,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
