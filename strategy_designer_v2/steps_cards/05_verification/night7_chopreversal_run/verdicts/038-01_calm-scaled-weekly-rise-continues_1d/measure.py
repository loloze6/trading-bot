import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    RAW = "debug_info.components.scaled_rise.last_history_value"

    # ---------- 1. Situation check: calm bars (detector not on 'chop') with a 7-day rise, long side ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            regime = df["regime"].astype(str)
            calm = regime != "chop"
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            # fallback where the component is not recorded: 7-day return from prices, inside the window
            close = pd.to_numeric(df["close"], errors="coerce")
            ret7 = close / close.shift(7) - 1.0
            rise = raw.where(raw.notna(), ret7) > 0
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            n_agree += int((active & calm & rise & (fc > 0)).sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "t of the slope of the 5-day forward return net of the coin's drift on the forecast (grid, forecast > 0)"
    threshold = "confirm if slope t >= 2 and mean unusual move > 0; reject if slope t <= -2; at least 100 grid cases"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"grid cases with forecast > 0": None, "active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are calm bars (regime not 'chop') "
                           "with a positive 7-day scaled return and a long forecast, as the plan's Fidelity requires."
                           if n_active > 0 else "The record has no bar with a non-zero forecast."),
            "reading": "Calm is read from the recorded regime (not 'chop'), the rise from the raw component's sign.",
        }

    # ---------- 2. Criterion ----------
    xs, ys = [], []
    for coin, wins in bars.items():
        # coin's normal 5-day drift: mean of non-overlapping 5-bar returns over all its windows
        drift_rets = []
        coin_cases = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            n = len(df)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                drift_rets.append(r)
                if np.isfinite(fc[i]) and fc[i] > 0:
                    coin_cases.append((float(fc[i]), r))
        if not drift_rets:
            continue
        drift = float(np.mean(drift_rets))
        for f, r in coin_cases:
            xs.append(f)
            ys.append(r - drift)

    xs = np.asarray(xs, dtype=float)
    ys = np.asarray(ys, dtype=float)
    n_cases = int(len(xs))

    slope = None
    t_slope = None
    if n_cases >= 3 and np.std(xs) > 0:
        lr = stats.linregress(xs, ys)
        slope = float(lr.slope)
        if lr.stderr is not None and np.isfinite(lr.stderr) and lr.stderr > 0:
            t_slope = float(lr.slope / lr.stderr)
    mean_unusual = float(np.mean(ys)) if n_cases > 0 else None
    sup_pass = None if mean_unusual is None else bool(mean_unusual > 0)

    counts = {"grid cases with forecast > 0": n_cases}

    if n_cases < 100:
        status = "not observable"
        decided_by = f"Only {n_cases} grid cases with forecast > 0 across all coins, below the plan's minimum of 100."
    elif t_slope is None:
        status = "inconclusive"
        decided_by = "The slope's t could not be computed (no variation in the forecast), so neither rule is met."
    elif t_slope >= 2 and sup_pass:
        status = "confirmed"
        decided_by = "The slope's t is >= 2 and the mean unusual 5-day move is > 0 (confirm rule)."
    elif t_slope <= -2:
        status = "rejected"
        decided_by = "The slope's t is <= -2 (reject rule)."
    elif t_slope >= 2:
        status = "inconclusive"
        decided_by = "The slope's t is >= 2 but the mean unusual move is <= 0, which the plan calls inconclusive."
    else:
        status = "inconclusive"
        decided_by = "The slope's t lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": t_slope,
            "statistic": None if t_slope is None else {"name": "OLS slope t", "value": t_slope},
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "mean unusual 5-day move (net of coin drift) > 0",
            "value": mean_unusual,
            "passed": sup_pass,
        },
        "counts": counts,
        "decided_by": decided_by,
        "reading": ("Cases from all coins are pooled in one OLS regression of the drift-removed 5-day forward return "
                    "on the forecast at the grid bar (positions 0,5,10,... of each window with a full 5-bar return), "
                    "each coin's drift being the mean of its non-overlapping 5-bar returns over all its windows, and "
                    "the plan's 'fewer than 100 cases' is reported as 'not observable' per the minimum-count rule."),
    }
