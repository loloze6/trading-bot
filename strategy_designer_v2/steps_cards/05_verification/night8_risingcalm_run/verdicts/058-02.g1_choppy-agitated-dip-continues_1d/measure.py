import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    RAW = "debug_info.components.dip.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce")
            fc = pd.to_numeric(d["forecast"], errors="coerce")
            # The 5-bar closing high includes today, so the close is below it
            # exactly when the distance is negative.
            hi5 = close.rolling(5, min_periods=5).max()
            price_dist = (close - hi5) / hi5
            if RAW in d.columns:
                raw = pd.to_numeric(d[RAW], errors="coerce")
                dist = raw.where(raw.notna(), price_dist)
            else:
                dist = price_dist
            active = fc.notna() & (fc != 0)
            in_sit = dist.notna() & (dist < 0)
            ok = active & in_sit & (fc < 0)
            n_active += int(active.sum())
            n_agree += int(ok.sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    if agreement is not None and agreement < 0.9:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": n_active, "active bars in situation on short side": n_agree},
            "decided_by": "Fewer than 90% of the bars with a non-zero forecast are short bars with the close below "
                          "its 5-bar closing high, as the plan's Fidelity requires.",
            "reading": "none",
        }

    # ---------- 2. criterion ----------
    # The coin's normal drift is the mean 5-bar return on the non-overlapping grid of all its windows.
    rows = []
    for coin, wins in bars.items():
        coin_rets = []
        coin_rows = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").values
            fc = pd.to_numeric(d["forecast"], errors="coerce").values
            reg = d["regime"].astype(str).str.lower().values if "regime" in d.columns else np.array(["unknown"] * len(d))
            n = len(d)
            for i in range(0, n, H):
                if i + H >= n:
                    continue
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                coin_rets.append(r)
                coin_rows.append((r, fc[i], reg[i] != "chop"))
        if len(coin_rets) == 0:
            continue
        drift = float(np.mean(coin_rets))
        for r, f, inprof in coin_rows:
            if inprof and np.isfinite(f):
                rows.append((r - drift, float(f)))

    y = np.array([r[0] for r in rows], dtype=float)
    x = np.array([r[1] for r in rows], dtype=float)
    nz = x != 0
    n_nonzero = int(nz.sum())
    n_grid = int(len(x))

    slope = None
    t_val = None
    if n_grid >= 3 and np.std(x) > 0:
        lr = stats.linregress(x, y)
        slope = float(lr.slope)
        t_val = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    deep_mean = None
    if n_nonzero >= 3:
        xs = x[nz]
        ys = y[nz]
        order = np.argsort(xs, kind="mergesort")
        k = len(xs) // 3
        if k > 0:
            deep_mean = float(np.mean(ys[order[:k]]))
    deep_pass = (deep_mean < 0) if deep_mean is not None else None

    counts = {"grid cases inside the profile with a non-zero forecast": n_nonzero,
              "grid cases inside the profile": n_grid}

    if n_nonzero < 30 or t_val is None:
        status = "not observable"
        decided = (f"Fewer than 30 grid cases inside the profile with a non-zero forecast ({n_nonzero}), "
                   "the plan's minimum count.") if n_nonzero < 30 else "The slope's t could not be computed."
    elif t_val >= 2 and deep_pass:
        status = "confirmed"
        decided = "The slope's t is at least +2 with at least 30 non-zero grid cases and the deepest third's mean drift-adjusted return is below 0."
    elif t_val >= 2:
        status = "inconclusive"
        decided = "The slope's t is at least +2 but the deepest third's mean drift-adjusted return is not below 0."
    elif t_val <= -2:
        status = "rejected"
        decided = "The slope's t is at most -2 with at least 30 non-zero grid cases."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and +2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement) if agreement is not None else None,
                            "passed": agreement is not None},
        "main_measure": {
            "name": "OLS slope of drift-adjusted next-5-bar return on the forecast, profile bars, 5-bar grid, coins pooled",
            "value": slope,
            "statistic": {"name": "regression t", "value": t_val} if t_val is not None else None,
            "threshold": "confirm if t >= +2 (with deepest third below 0); reject if t <= -2; at least 30 non-zero grid cases",
        },
        "supporting_check": {"name": "mean drift-adjusted 5-bar return of the deepest third of the forecast",
                             "value": deep_mean, "passed": deep_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": ("The profile is the bars whose regime is not 'chop'. The regression uses every profile grid bar, "
                    "including those with a zero forecast. The drift is the coin's mean 5-bar grid return over all its "
                    "bars. The deepest third is the floor(n/3) most negative of the non-zero-forecast profile grid "
                    "cases. The situation side uses last_history_value, or the price-based 5-bar distance where that "
                    "value is missing."),
    }
