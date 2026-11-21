import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 72
    RAW72 = "debug_info.components.fall72.last_history_value"

    # ---------- 1. Situation check: 72-bar return <= 0, long side ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = df["close"].astype(float)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            ret72_px = close / close.shift(H) - 1.0
            if RAW72 in df.columns:
                raw = pd.to_numeric(df[RAW72], errors="coerce")
                ret72 = raw.where(raw.notna(), ret72_px)
            else:
                ret72 = ret72_px
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            agree = active & ret72.notna() & (ret72 <= 1e-12) & (fc > 0)
            n_agree += int(agree.sum())

    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the active bars (forecast not 0) are long bars with a 72-bar return "
                           "at or below 0, the situation the plan's Fidelity keeps"
                           if n_active > 0 else "No active bars in the record."),
            "reading": "The situation as kept is the 72-bar return at or below 0 (the 24-bar fall is a size, not a condition), on the long side.",
        }

    # ---------- 2. Criterion ----------
    # coin mean 72-bar return over all windows (non-overlapping grid, all grid bars)
    coin_rets = {}
    cases = []  # (coin, forecast, fwd)
    for coin, wins in bars.items():
        allr = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = df["close"].astype(float).values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            reg = df["regime"].astype(str).values
            n = len(df)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                r = close[i + H] / close[i] - 1.0
                if not np.isfinite(r):
                    continue
                allr.append(r)
                if reg[i] == "mean_reversion" and np.isfinite(fc[i]) and fc[i] > 0:
                    cases.append((coin, float(fc[i]), float(r)))
        coin_rets[coin] = float(np.mean(allr)) if allr else np.nan

    x = np.array([c[1] for c in cases], dtype=float)
    y = np.array([c[2] - coin_rets[c[0]] for c in cases], dtype=float)
    ok = np.isfinite(x) & np.isfinite(y)
    x, y = x[ok], y[ok]
    n_cases = int(len(x))

    slope, t_val = None, None
    if n_cases >= 3 and np.std(x) > 0:
        lr = stats.linregress(x, y)
        slope = float(lr.slope)
        t_val = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    check_val, check_pass = None, None
    if n_cases >= 2:
        med = np.median(x)
        hi, lo = y[x > med], y[x < med]
        if len(hi) > 0 and len(lo) > 0:
            check_val = float(hi.mean() - lo.mean())
            check_pass = bool(check_val > 0)

    if n_cases < 200:
        status = "not observable"
        decided = f"Only {n_cases} active grid cases, fewer than the plan's minimum of 200."
    elif t_val is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed (no spread in the forecast), so neither confirm nor reject is met."
    elif t_val >= 2 and check_pass:
        status = "confirmed"
        decided = "The slope's t is 2 or more and the high-minus-low median split is above 0, with at least 200 cases."
    elif t_val >= 2:
        status = "inconclusive"
        decided = "The slope's t is 2 or more but the supporting check is not above 0."
    elif t_val <= -2:
        status = "rejected"
        decided = "The slope's t is -2 or less, with at least 200 cases."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "t of OLS slope of excess 72-bar forward return on forecast, active grid bars",
            "value": t_val,
            "statistic": {"name": "OLS slope t", "value": t_val} if t_val is not None else None,
            "threshold": "confirm if t >= 2 (with check > 0), reject if t <= -2, at least 200 cases",
        },
        "supporting_check": {
            "name": "mean excess return above median forecast minus below median",
            "value": check_val,
            "passed": check_pass,
        },
        "counts": {"active grid cases": n_cases},
        "decided_by": decided,
        "reading": ("The coin's mean 72-bar return is the mean of all its non-overlapping grid 72-bar returns over all "
                    "windows, the regression is OLS with an intercept, and cases exactly at the median forecast are left "
                    "out of the median split."),
    }
