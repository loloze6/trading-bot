import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    RAW = "debug_info.components.lagged_scaled_fall.last_history_value"
    H = 2

    # ---------- 1. Situation check ----------
    # Situation (Fidelity): the previous day's return, scaled by the 30-day std of daily returns, is a fall (< 0),
    # in an agitated market (regime not vetoed to "chop"); expected side: long (a rise).
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = df["close"].astype(float)
            ret = close.pct_change()
            # recompute raw value from prices where the component is not recorded
            std30 = ret.rolling(30, min_periods=30).std()
            recomputed = (ret / std30).shift(1)
            if RAW in df.columns:
                raw = df[RAW].astype(float).where(df[RAW].notna(), recomputed)
            else:
                raw = recomputed
            fc = df["forecast"].astype(float)
            active = fc.notna() & (fc != 0)
            agitated = df["regime"].astype(str) != "chop"
            situ = (raw < 0) & agitated
            agree = active & situ & (fc > 0)
            n_active += int(active.sum())
            n_agree += int(agree.sum())

    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "t of slope of 2-bar excess return on forecast, forecast>0 grid cells"
    threshold = "confirm: slope > 0 with t >= 2 and weighted mean excess > 0; reject: slope < 0 with t <= -2"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": "Fewer than 90% of bars with a non-zero forecast are long bars after a scaled one-day fall "
                          "in an agitated (non-chop) regime, so the config does not do what the Fidelity says.",
            "reading": "Agitated is read as the recorded regime not being 'chop' (the profile veto); the fall as the "
                       "recorded raw value below 0, recomputed from prices where missing.",
        }

    # ---------- 2. Criterion ----------
    xs, ys = [], []
    for coin, wins in bars.items():
        cells = []
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = df["close"].astype(float).values
            fc = df["forecast"].astype(float).values
            n = len(df)
            for i in range(0, n - H, H):
                r = close[i + H] / close[i] - 1.0
                if np.isfinite(r):
                    cells.append((r, fc[i]))
        if not cells:
            continue
        arr = np.array(cells, dtype=float)
        coin_mean = float(np.mean(arr[:, 0]))
        for r, f in arr:
            if np.isfinite(f) and f > 0:
                xs.append(f)
                ys.append(r - coin_mean)

    xs = np.array(xs, dtype=float)
    ys = np.array(ys, dtype=float)
    n_cells = int(len(xs))
    counts = {"grid cells with a positive forecast": n_cells}

    slope = None
    t_slope = None
    wmean = None
    if n_cells >= 3 and np.std(xs) > 0:
        lr = stats.linregress(xs, ys)
        slope = float(lr.slope)
        t_slope = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None
    if n_cells > 0 and xs.sum() > 0:
        wmean = float(np.sum(ys * xs) / np.sum(xs))

    sup_pass = None if wmean is None else bool(wmean > 0)
    supporting = {"name": "forecast-weighted mean excess 2-bar return", "value": wmean, "passed": sup_pass}
    main = {"name": main_name, "value": slope,
            "statistic": {"name": "OLS slope t", "value": t_slope} if t_slope is not None else None,
            "threshold": threshold}

    reading = ("Grid cells start at positions 0, 2, 4, ... of each window and need t+2 inside it; the coin's mean "
               "2-bar return is the mean over all its grid cells in all windows; the regression pools all coins; "
               "agitated is the recorded regime not being 'chop'.")

    if n_cells < 100:
        status = "not observable"
        decided = f"Only {n_cells} grid cells with a positive forecast, below the plan's minimum of 100."
    elif t_slope is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed (no variation in the forecast)."
    elif slope > 0 and t_slope >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "The slope is positive with t >= 2 and the forecast-weighted mean excess return is above 0."
        else:
            status = "inconclusive"
            decided = "A confirming slope (t >= 2) but a forecast-weighted mean excess of 0 or below."
    elif slope < 0 and t_slope <= -2:
        status = "rejected"
        decided = "The slope is negative with t <= -2."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": supporting,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
