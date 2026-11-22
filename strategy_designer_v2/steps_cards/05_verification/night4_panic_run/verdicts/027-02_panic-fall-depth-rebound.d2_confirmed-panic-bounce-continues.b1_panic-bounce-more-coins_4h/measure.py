import json
import numpy as np
import pandas as pd
from scipy import stats

H = 84


def _comp_value(df, comp_id, field):
    """Return a float Series of debug_info.components.<id>.<field>, NaN where not recorded."""
    flat = f"debug_info.components.{comp_id}.{field}"
    if flat in df.columns:
        return pd.to_numeric(df[flat], errors="coerce").astype(float)
    out = pd.Series(np.nan, index=df.index, dtype=float)
    if "debug_info.components" not in df.columns:
        return out
    vals = []
    for v in df["debug_info.components"].values:
        x = np.nan
        try:
            d = v
            if isinstance(d, str):
                d = json.loads(d)
            if isinstance(d, dict) and comp_id in d:
                c = d[comp_id]
                if isinstance(c, str):
                    c = json.loads(c)
                if isinstance(c, dict) and c.get(field) is not None:
                    x = float(c[field])
        except Exception:
            x = np.nan
        vals.append(x)
    return pd.Series(vals, index=df.index, dtype=float)


def _panic_situation(df):
    """Fidelity situation: the 6-bar stretch ending 6 bars before t (bars t-11..t-6) has a
    range >= 3x its 180-bar mean range and its close is below the close 6 bars before it."""
    high = df["high"].astype(float)
    low = df["low"].astype(float)
    close = df["close"].astype(float)
    rng = high.rolling(6, min_periods=6).max() - low.rolling(6, min_periods=6).min()
    base = rng.rolling(180, min_periods=30).mean()
    mult = rng / base
    fall = close < close.shift(6)
    mult_l = mult.shift(6)
    fall_l = fall.shift(6)
    computable = mult_l.notna() & fall_l.notna()
    sit = (mult_l >= 3.0 - 1e-9) & (fall_l == True)
    return sit.fillna(False).astype(bool), computable.astype(bool)


def measure(bars):
    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin in sorted(bars):
        for w in sorted(bars[coin]):
            df = bars[coin][w].reset_index(drop=True)
            if len(df) == 0:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            sit, comp = _panic_situation(df)
            active = (fc != 0) & comp
            n_active += int(active.sum())
            n_agree += int((active & sit & (fc > 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "OLS slope of 84-bar excess return on raw 24h bounce, pooled over coins and windows"
    threshold = "confirm: slope > 0 with t >= 2; reject: slope < 0 with t <= -2; at least 30 cases"
    reading = ("Panic recomputed as the 6-bar high-low range over its 180-bar mean (min 30 bars where history is short) "
               "for bars t-11..t-6 with close[t-6] < close[t-12], long side, on active bars where it is computable; "
               "cases are the first regime == 'mean_reversion' bar in each 84-bar grid cell from each window's first row, "
               "the coin's mean 84-bar return is taken on the non-overlapping grid of all its windows, the slope and its t "
               "are from ordinary least squares, and fewer than 30 cases is read as 'not observable'.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "cases": 0},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars on which the stretch that "
                           "ended 6 bars earlier was a panic fall (range >= 3x its 180-bar mean and a 6-bar fall)."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    xs, ys = [], []
    for coin in sorted(bars):
        # the coin's mean 84-bar return over all its windows (non-overlapping grid)
        grid_rets = []
        for w in sorted(bars[coin]):
            close = bars[coin][w]["close"].astype(float).values
            for p in range(0, len(close) - H, H):
                if np.isfinite(close[p]) and np.isfinite(close[p + H]) and close[p] != 0:
                    grid_rets.append(close[p + H] / close[p] - 1.0)
        if len(grid_rets) == 0:
            continue
        coin_mean = float(np.mean(grid_rets))

        for w in sorted(bars[coin]):
            df = bars[coin][w].reset_index(drop=True)
            n = len(df)
            if n == 0:
                continue
            close = df["close"].astype(float).values
            regime = df["regime"].astype(str).values
            bounce = _comp_value(df, "bounce", "last_history_value").values
            for start in range(0, n, H):
                end = min(start + H, n)
                idx = np.where(regime[start:end] == "mean_reversion")[0]
                if len(idx) == 0:
                    continue
                t = start + int(idx[0])
                if t + H >= n:
                    continue
                if not (np.isfinite(close[t]) and np.isfinite(close[t + H])) or close[t] == 0:
                    continue
                b = bounce[t]
                if not np.isfinite(b):
                    if t >= 6 and np.isfinite(close[t - 6]) and close[t - 6] != 0:
                        b = close[t] / close[t - 6] - 1.0
                    else:
                        continue
                fwd = close[t + H] / close[t] - 1.0
                xs.append(float(b))
                ys.append(float(fwd - coin_mean))

    n_cases = len(xs)
    counts = {"cases": int(n_cases)}

    if n_cases < 30:
        return {
            "status": "not observable",
            "situation_check": {"agreement": agreement, "passed": True},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": counts,
            "decided_by": f"Only {n_cases} cases, fewer than the plan's minimum of 30.",
            "reading": reading,
        }

    x = np.asarray(xs)
    y = np.asarray(ys)
    if np.std(x) == 0:
        slope, tval = 0.0, 0.0
    else:
        lr = stats.linregress(x, y)
        slope = float(lr.slope)
        tval = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else 0.0

    if slope > 0 and tval >= 2:
        status = "confirmed"
        decided = f"The slope is positive ({slope:.4g}) with t = {tval:.2f} >= 2 on {n_cases} cases (confirm rule)."
    elif slope < 0 and tval <= -2:
        status = "rejected"
        decided = f"The slope is negative ({slope:.4g}) with t = {tval:.2f} <= -2 on {n_cases} cases (reject rule)."
    else:
        status = "inconclusive"
        decided = f"t = {tval:.2f} lies between -2 and 2 on {n_cases} cases (inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": slope,
                         "statistic": {"name": "OLS slope t", "value": tval},
                         "threshold": threshold},
        "supporting_check": None,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
