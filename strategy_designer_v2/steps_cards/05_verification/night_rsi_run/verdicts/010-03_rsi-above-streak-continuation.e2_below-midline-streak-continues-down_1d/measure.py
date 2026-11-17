import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 7
    RAW = "debug_info.components.rsi_below_age.last_history_value"

    # ---------- 1. Situation check ----------
    # Fidelity: situation = RSI(14) has stayed below 50 (raw run value < 0); outcome = lower return -> short side.
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            raw = pd.to_numeric(df[RAW], errors="coerce") if RAW in df.columns else pd.Series(np.nan, index=df.index)
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            agree = active & raw.notna() & (raw < 0) & (fc < 0)
            n_agree += int(agree.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.90

    main_name = "OLS t of the slope of excess 7-day return on run length below 50 (pooled grid bars, forecast < 0)"
    threshold = "confirm if t <= -2 with supporting check passing; reject if t >= +2; otherwise inconclusive; at least 100 grid cases with forecast < 0"
    sup_name = "mean of forecast/10 x excess 7-day return on the same grid bars > 0"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": n_active, "active bars in situation on short side": n_agree},
            "decided_by": ("No active bars were found" if agreement is None else
                           f"Only {agreement:.1%} of the active bars are short bars with RSI(14) below 50 (raw run value < 0), "
                           "below the 90% required by the plan's situation."),
            "reading": "none",
        }

    # ---------- 2. Criterion ----------
    xs, ys, fcs = [], [], []
    for coin, wins in bars.items():
        grid_rows = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(d["forecast"], errors="coerce").to_numpy(dtype=float)
            raw = (pd.to_numeric(d[RAW], errors="coerce").to_numpy(dtype=float)
                   if RAW in d.columns else np.full(len(d), np.nan))
            n = len(d)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                grid_rows.append((c1 / c0 - 1.0, fc[i], raw[i]))
        if not grid_rows:
            continue
        rets = np.array([r[0] for r in grid_rows])
        coin_mean = float(np.mean(rets))  # coin's mean 7-day return over all its windows (grid)
        for r, f, rv in grid_rows:
            if np.isfinite(f) and f < 0 and np.isfinite(rv):
                xs.append(-rv)
                ys.append(r - coin_mean)
                fcs.append(f)

    xs = np.array(xs, dtype=float)
    ys = np.array(ys, dtype=float)
    fcs = np.array(fcs, dtype=float)
    n_cases = int(len(xs))
    counts = {"grid cases with forecast < 0": n_cases}

    reading = ("The coin's mean 7-day return is taken over its non-overlapping 7-bar grid bars of all windows, grid bars "
               "without a full 7-bar return inside the window are dropped, the slope's t is the ordinary OLS t pooled over "
               "both coins, and the plan's 'fewer than 100 cases' rule is reported as not observable per the workflow.")

    sup_val = float(np.mean(fcs / 10.0 * ys)) if n_cases > 0 else None
    sup_pass = (sup_val is not None) and (sup_val > 0)

    slope = None
    t = None
    if n_cases >= 3 and np.std(xs) > 0:
        res = stats.linregress(xs, ys)
        slope = float(res.slope)
        t = float(res.slope / res.stderr) if res.stderr > 0 else None

    main = {"name": main_name, "value": slope,
            "statistic": ({"name": "OLS slope t", "value": t} if t is not None else None),
            "threshold": threshold}
    supporting = {"name": sup_name, "value": sup_val, "passed": bool(sup_pass) if sup_val is not None else None}

    if n_cases < 100:
        status = "not observable"
        decided = f"Only {n_cases} grid cases with forecast < 0, below the plan's minimum of 100."
    elif t is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed (no variation in run length), so it meets neither the confirm nor the reject rule."
    elif t <= -2 and sup_pass:
        status = "confirmed"
        decided = f"The slope's t ({t:.2f}) is <= -2 and the short side gained against holding the coin (supporting check passes)."
    elif t >= 2:
        status = "rejected"
        decided = f"The slope's t ({t:.2f}) is >= +2: longer stretches below 50 are followed by higher excess returns."
    elif t <= -2:
        status = "inconclusive"
        decided = f"The slope's t ({t:.2f}) is <= -2 but the supporting check fails, which the plan calls inconclusive."
    else:
        status = "inconclusive"
        decided = f"The slope's t ({t:.2f}) lies between -2 and +2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": supporting,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
