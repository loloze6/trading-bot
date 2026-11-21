import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 18
    RAW = "debug_info.components.pullback.last_history_value"
    MIN_CASES = 100

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float)
            high = df["high"].astype(float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)

            # regime: 42-bar return > 0, from prices; fallback to recorded regime where history is short
            ret42 = close / close.shift(42) - 1.0
            reg_rec = df["regime"].astype(str).eq("trending") if "regime" in df.columns else pd.Series(False, index=df.index)
            regime_on = pd.Series(np.where(ret42.notna(), ret42 > 0, reg_rec), index=df.index).astype(bool)

            # pullback depth: raw recorded value where present, else recompute from prices
            prior_high = high.shift(1).rolling(12, min_periods=12).max()
            depth_px = (prior_high - close).clip(lower=0)
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
                depth = raw.where(raw.notna(), depth_px)
            else:
                depth = depth_px
            pull_on = (depth > 0).fillna(False)

            situation = regime_on & pull_on
            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc > 0)).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9

    reading = ("The 42-bar return is close[t]/close[t-42]-1 inside the window, with the recorded regime used on the "
               "first 42 bars of a window where prices cannot give it; the pullback depth is the recorded raw value, "
               "recomputed from prices where missing; the coin's normal drift is the mean 18-bar return over all grid "
               "bars of all its windows; the slope's t is the ordinary OLS t of the pooled regression of excess return "
               "on forecast with an intercept, and a case is a grid bar with forecast > 0 and a full 18-bar forward return.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars where the 42-bar return "
                           "is positive and the close sits below the prior 12-bar high, as the plan's Fidelity requires."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    xs, ys = [], []
    for coin, wins in bars.items():
        grid_rets = []
        rows = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float).values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            n = len(df)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 <= 0:
                    continue
                r = c1 / c0 - 1.0
                grid_rets.append(r)
                if np.isfinite(fc[i]) and fc[i] > 0:
                    rows.append((fc[i], r))
        if not grid_rets:
            continue
        drift = float(np.mean(grid_rets))
        for f, r in rows:
            xs.append(f)
            ys.append(r - drift)

    xs = np.asarray(xs, dtype=float)
    ys = np.asarray(ys, dtype=float)
    n_cases = int(len(xs))

    slope = None
    t = None
    if n_cases >= 3 and np.std(xs) > 0:
        lr = stats.linregress(xs, ys)
        slope = float(lr.slope)
        t = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None
    sup_val = float(np.mean(xs * ys)) if n_cases > 0 else None
    sup_pass = (sup_val > 0) if sup_val is not None else None

    main = {
        "name": "slope of 18-bar excess return on forecast (pooled, grid bars with forecast > 0)",
        "value": slope,
        "statistic": {"name": "OLS slope t", "value": t} if t is not None else None,
        "threshold": "t >= 2 confirms (with supporting check), t <= -2 rejects, at least 100 cases",
    }
    supporting = {"name": "mean of forecast x excess return > 0", "value": sup_val, "passed": sup_pass}
    counts = {"independent grid cases with forecast > 0": n_cases}

    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"Only {n_cases} independent grid cases with forecast > 0, below the plan's minimum of 100."
    elif t is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed (no variation in the forecast), so no rule is met."
    elif t >= 2 and sup_pass:
        status = "confirmed"
        decided = "The slope's t is 2 or more, the supporting check passes, with at least 100 cases."
    elif t >= 2:
        status = "inconclusive"
        decided = "The slope's t is 2 or more but the supporting check fails, which the plan calls inconclusive."
    elif t <= -2:
        status = "rejected"
        decided = "The slope's t is -2 or less, with at least 100 cases."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": supporting,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
