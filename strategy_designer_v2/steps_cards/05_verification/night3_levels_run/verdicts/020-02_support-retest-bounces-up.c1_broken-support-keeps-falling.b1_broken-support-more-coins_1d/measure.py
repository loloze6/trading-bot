import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    RAW = "debug_info.components.support_above.last_history_value"

    # ---------- 1. Situation check ----------
    # Situation: a swing-low cluster lies above the close (raw value > 0).
    # Expected side: short (forecast < 0).
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            active = fc.notna() & (fc != 0)
            situation = raw.notna() & (raw > 0)
            agree = active & situation & (fc < 0)
            n_active += int(active.sum())
            n_agree += int(agree.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "pooled OLS slope of excess 5-bar return on forecast (grid bars, before costs)"
    threshold = "confirm: slope t >= 2 with supporting check; reject: slope t <= -2"
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None,
                             "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of bars with a non-zero forecast are short bars with a "
                           "swing-low cluster above the close (raw component > 0), as the Fidelity's "
                           "situation and short side require."),
            "reading": "Situation taken as raw component value > 0 (a swing low lies above the close); side short.",
        }

    # ---------- 2. Criterion ----------
    rows = []
    for coin, wins in bars.items():
        coin_rows = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            n = len(df)
            for t in range(0, n, H):
                if t + H >= n:
                    break
                c0, c1, f = close[t], close[t + H], fc[t]
                if not (np.isfinite(c0) and np.isfinite(c1) and c0 > 0):
                    continue
                coin_rows.append((f, c1 / c0 - 1.0))
        if not coin_rows:
            continue
        arr = np.array(coin_rows, dtype=float)
        coin_mean = float(np.nanmean(arr[:, 1]))
        for f, r in arr:
            if np.isfinite(f) and np.isfinite(r):
                rows.append((f, r - coin_mean))

    data = np.array(rows, dtype=float) if rows else np.zeros((0, 2))
    x = data[:, 0]
    y = data[:, 1]
    n_grid = int(len(x))
    neg = x < 0
    n_neg = int(neg.sum())

    slope = None
    tval = None
    if n_grid >= 3 and np.var(x) > 0:
        res = stats.linregress(x, y)
        slope = float(res.slope)
        tval = float(res.slope / res.stderr) if res.stderr and res.stderr > 0 else None

    sup_val = float(np.mean(y[neg])) if n_neg > 0 else None
    sup_pass = (sup_val < 0) if sup_val is not None else None

    counts = {"grid bars with forecast below 0": n_neg, "grid bars": n_grid}

    if n_neg < 200:
        status = "not observable"
        decided = f"Only {n_neg} grid bars with forecast below 0, fewer than the plan's minimum of 200."
    elif tval is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed (no variation in the forecast)."
    elif tval >= 2 and sup_pass:
        status = "confirmed"
        decided = "Slope t >= 2 and mean excess return on forecast<0 grid bars is below 0 (confirm rule)."
    elif tval <= -2:
        status = "rejected"
        decided = "Slope t <= -2: a more negative forecast is followed by a higher excess return (reject rule)."
    elif tval >= 2:
        status = "inconclusive"
        decided = "Slope t >= 2 but the supporting check fails (inconclusive rule)."
    else:
        status = "inconclusive"
        decided = "Slope t lies between -2 and 2 (inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": slope,
            "statistic": {"name": "OLS slope t", "value": tval} if tval is not None else None,
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "mean excess 5-bar return on grid bars with forecast < 0 below 0",
            "value": sup_val,
            "passed": None if sup_pass is None else bool(sup_pass),
        },
        "counts": counts,
        "decided_by": decided,
        "reading": ("Grid bars at positions 0,5,10,... of each window with the 5-bar return inside the window; "
                    "coin mean is the mean of those grid returns over all its windows; the regression is OLS with "
                    "an intercept over all grid bars including forecast 0; situation taken as raw component > 0 "
                    "on the short side; the 200-bar minimum yields 'not observable' per the workflow."),
    }
