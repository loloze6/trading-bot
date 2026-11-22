import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    P = 30
    FCOL = "forecast"
    RAW = "debug_info.components.fall10.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = df["close"].astype(float)
            high = df["high"].astype(float)
            low = df["low"].astype(float)
            fc = pd.to_numeric(df[FCOL], errors="coerce")
            hh = high.rolling(P, min_periods=P).max()
            ll = low.rolling(P, min_periods=P).min()
            rng = hh - ll
            net = (close - close.shift(P)).abs()
            nm = net / rng.replace(0, np.nan)
            mid = (hh + ll) / 2.0
            below = close < mid
            if RAW in df.columns:
                f10 = pd.to_numeric(df[RAW], errors="coerce")
            else:
                f10 = pd.Series(np.nan, index=df.index)
            f10 = f10.where(f10.notna(), close / close.shift(10) - 1.0)
            computable = nm.notna() & mid.notna() & f10.notna()
            situation = (nm >= 0.5) & below & (f10 < 0)
            active = fc.notna() & (fc != 0) & computable
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc > 0)).sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    reading = ("Net move to range taken as |close[t]-close[t-30]| over the 30-bar high-low range, the Ichimoku "
               "position as close minus the 30-bar high-low midpoint, the 10-day fall from fall10's raw value "
               "(else recomputed from closes), active bars whose 30-bar history is not inside the window left out "
               "of the agreement; the coin's mean 5-bar return is the mean over all grid cells of all its windows, "
               "and the slope t is the OLS slope t of the pooled regression of excess return on forecast.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars checked": n_active},
            "decided_by": ("Fewer than 90% of the active bars are long bars where the 30-bar net move/range >= 0.5, "
                           "the close is below the 30-bar range midpoint and the coin fell over 10 days."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    xs, ys = [], []
    for coin, wins in bars.items():
        cells = []
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = df["close"].astype(float).values
            fc = pd.to_numeric(df[FCOL], errors="coerce").values
            n = len(df)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                r = close[i + H] / close[i] - 1.0
                if np.isfinite(r):
                    cells.append((r, fc[i]))
        if not cells:
            continue
        rets = np.array([c[0] for c in cells])
        fcs = np.array([c[1] for c in cells], dtype=float)
        mu = rets.mean()
        sel = np.isfinite(fcs) & (fcs > 0)
        xs.extend(fcs[sel].tolist())
        ys.extend((rets[sel] - mu).tolist())

    x = np.array(xs)
    y = np.array(ys)
    n_cells = int(len(x))
    counts = {"grid cells with a forecast above 0, pooled over coins": n_cells}
    thr = "confirm if slope t >= 2 (with mean excess > 0), reject if slope t <= -2"
    name = "pooled slope of 5-bar excess return on forecast, cells with forecast > 0"

    if n_cells < 30:
        return {
            "status": "not observable",
            "situation_check": {"agreement": agreement, "passed": True},
            "main_measure": {"name": name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": {"name": "mean excess 5-bar return over those cells",
                                 "value": float(y.mean()) if n_cells else None, "passed": None},
            "counts": counts,
            "decided_by": "Fewer than 30 grid cells with a forecast above 0, pooled over coins.",
            "reading": reading,
        }

    mean_ex = float(y.mean())
    if np.std(x) == 0:
        slope, t = None, None
    else:
        lr = stats.linregress(x, y)
        slope = float(lr.slope)
        t = float(lr.slope / lr.stderr) if lr.stderr > 0 else None
    sup_pass = bool(mean_ex > 0)

    if t is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed (no variation in the forecast), so neither rule is met."
    elif t >= 2 and sup_pass:
        status = "confirmed"
        decided = "The slope's t is 2 or more and the mean excess return is above 0."
    elif t >= 2:
        status = "inconclusive"
        decided = "A confirming t with a mean excess return of 0 or below."
    elif t <= -2:
        status = "rejected"
        decided = "The slope's t is -2 or less."
    else:
        status = "inconclusive"
        decided = "A slope t between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": name, "value": slope,
                         "statistic": {"name": "OLS slope t", "value": t} if t is not None else None,
                         "threshold": thr},
        "supporting_check": {"name": "mean excess 5-bar return over those cells", "value": mean_ex,
                             "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
