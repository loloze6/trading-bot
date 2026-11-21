import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 10
    RAW = "debug_info.components.scaled_fall.last_history_value"

    # ---------- 1. Situation check: a 1-day fall (raw value < 0), long side ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            ret1 = close / close.shift(1) - 1.0
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
                fall = raw.where(raw.notna(), ret1)
            else:
                fall = ret1
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            agree = active & (fall < 0) & (fc > 0)
            n_agree += int(agree.sum())

    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "t of the slope of excess 10-bar return regressed on forecast, over positive-forecast grid cells"
    threshold = "confirm if slope t >= 2 with mean excess > 0; reject if slope t <= -2; at least 100 cells"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on long side": int(n_agree)},
            "decided_by": ("fewer than 90% of the bars with a non-zero forecast are 1-day falls held long, "
                           "as the plan's situation (a coin's 1-day fall, expecting a rise) requires"
                           if n_active > 0 else "the forecast is never non-zero, so the plan's situation is never traded"),
            "reading": "the situation is a negative raw component value (1-day return over 20-day vol), or a negative 1-day close return where the raw value is missing, with a positive forecast.",
        }

    # ---------- 2. Criterion ----------
    xs, ys = [], []
    for coin, wins in bars.items():
        all_rets = []
        cells = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            n = len(df)
            for t in range(0, n, H):
                if t + H >= n:
                    break
                c0, c1 = close[t], close[t + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                all_rets.append(r)
                f = fc[t]
                if np.isfinite(f) and f > 0:
                    cells.append((f, r))
        if len(all_rets) == 0:
            continue
        drift = float(np.mean(all_rets))
        for f, r in cells:
            xs.append(f)
            ys.append(r - drift)

    xs = np.asarray(xs, dtype=float)
    ys = np.asarray(ys, dtype=float)
    n_cells = int(len(xs))

    slope = None
    t_slope = None
    if n_cells >= 3 and np.std(xs) > 0:
        lr = stats.linregress(xs, ys)
        slope = float(lr.slope)
        t_slope = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None
    mean_excess = float(np.mean(ys)) if n_cells > 0 else None
    sup_passed = (mean_excess > 0) if mean_excess is not None else None

    counts = {"cells with a positive forecast": n_cells}

    if n_cells < 100:
        status = "not observable"
        decided = f"fewer than 100 cells with a positive forecast ({n_cells}), the plan's minimum count."
    elif t_slope is None:
        status = "inconclusive"
        decided = "the slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif t_slope >= 2 and sup_passed:
        status = "confirmed"
        decided = "the slope's t is 2 or more and the mean excess return over the cells is positive, with at least 100 cells."
    elif t_slope <= -2:
        status = "rejected"
        decided = "the slope's t is -2 or less, with at least 100 cells."
    elif t_slope >= 2:
        status = "inconclusive"
        decided = "a slope t of 2 or more with a mean excess return of 0 or below is inconclusive."
    else:
        status = "inconclusive"
        decided = "a slope t between -2 and 2 is inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": slope,
            "statistic": ({"name": "OLS slope t", "value": t_slope} if t_slope is not None else None),
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "mean excess 10-bar return over the same cells above 0",
            "value": mean_excess,
            "passed": (bool(sup_passed) if sup_passed is not None else None),
        },
        "counts": counts,
        "decided_by": decided,
        "reading": ("cells are at positions 0, 10, 20, ... of each window with a full 10-bar forward return inside it; "
                    "each coin's normal drift is the mean of its 10-bar returns over all such cells of all its windows; "
                    "the regression pools the cells of all coins, and the main measure's value is the slope (excess return per forecast point)."),
    }
