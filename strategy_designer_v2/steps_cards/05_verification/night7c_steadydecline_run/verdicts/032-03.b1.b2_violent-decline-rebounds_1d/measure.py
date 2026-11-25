import numpy as np
import pandas as pd
from scipy import stats


def _component_value(df, comp_id, field="last_history_value"):
    """Return a float Series of a strategy component's recorded value (NaN where not recorded)."""
    flat = f"debug_info.components.{comp_id}.{field}"
    if flat in df.columns:
        return pd.to_numeric(df[flat], errors="coerce").astype(float)
    out = pd.Series(np.nan, index=df.index, dtype=float)
    if "debug_info.components" in df.columns:
        vals = []
        for v in df["debug_info.components"].values:
            x = np.nan
            if isinstance(v, dict):
                c = v.get(comp_id)
                if isinstance(c, dict) and c.get(field) is not None:
                    try:
                        x = float(c.get(field))
                    except (TypeError, ValueError):
                        x = np.nan
            vals.append(x)
        out = pd.Series(vals, index=df.index, dtype=float)
    return out


def measure(bars):
    H = 5
    MIN_CASES = 100

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin in sorted(bars.keys()):
        for w in sorted(bars[coin].keys()):
            df = bars[coin][w].reset_index(drop=True)
            if len(df) == 0:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).astype(float)
            close = pd.to_numeric(df["close"], errors="coerce").astype(float)
            fall = _component_value(df, "fall_depth", "last_history_value")
            # where the component is not recorded, recompute the 28-day return from prices in the window
            recomputed = close / close.shift(28) - 1.0
            fall = fall.where(fall.notna(), recomputed)
            regime = df["regime"].astype(str) if "regime" in df.columns else pd.Series("", index=df.index)
            wide_range = regime == "mean_reversion"
            situation = (fall < 0) & wide_range
            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc > 0)).sum())

    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "pooled OLS slope of in-regime 5-day excess return on forecast"
    threshold = "slope t >= 2 confirms (with mean excess > 0); t <= -2 rejects; otherwise inconclusive"
    reading = ("The 28-day fall is read from fall_depth's last_history_value (recomputed from closes where missing), "
               "while the wide-range condition (28-day vs 365-day mean range) cannot be rebuilt from ~120-bar windows "
               "so it is taken from the recorded regime 'mean_reversion'; grid bars at positions 0,5,10,... of each "
               "window with close[t+5] inside the window, in-regime meaning forecast > 0, coin mean 5-day return over "
               "all its grid bars in all windows, slope t from ordinary least squares with intercept.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on long side": int(n_agree)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars where the 28-day "
                           "return is below 0 in a wide-range regime, so the config does not do what the Fidelity says."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin in sorted(bars.keys()):
        coin_rets = []
        coin_cases = []
        for w in sorted(bars[coin].keys()):
            df = bars[coin][w].reset_index(drop=True)
            n = len(df)
            if n == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").astype(float).values
            fc = pd.to_numeric(df["forecast"], errors="coerce").astype(float).values
            for t in range(0, n, H):
                if t + H >= n:
                    break
                c0, c1 = close[t], close[t + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 <= 0:
                    continue
                r = c1 / c0 - 1.0
                coin_rets.append(r)
                if np.isfinite(fc[t]) and fc[t] > 0:
                    coin_cases.append((fc[t], r))
        if len(coin_rets) == 0:
            continue
        mu = float(np.mean(coin_rets))
        for f, r in coin_cases:
            rows.append((f, r - mu))

    n_cases = len(rows)
    counts = {"in-regime grid cases pooled over coins and windows": int(n_cases)}

    if n_cases < MIN_CASES:
        return {
            "status": "not observable",
            "situation_check": {"agreement": float(agreement), "passed": True},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": {"name": "mean in-regime 5-day excess return > 0", "value": None, "passed": None},
            "counts": counts,
            "decided_by": f"Fewer than {MIN_CASES} in-regime grid cases pooled over coins and windows ({n_cases}).",
            "reading": reading,
        }

    arr = np.array(rows, dtype=float)
    x, y = arr[:, 0], arr[:, 1]
    mean_excess = float(np.mean(y))
    sup_pass = bool(mean_excess > 0)

    if np.ptp(x) == 0:
        slope, t_slope = None, None
    else:
        lr = stats.linregress(x, y)
        slope = float(lr.slope)
        t_slope = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    if t_slope is None or not np.isfinite(t_slope):
        status = "inconclusive"
        decided = "The slope's t could not be computed (no spread in the forecast), which meets neither confirm nor reject."
    elif t_slope >= 2 and sup_pass:
        status = "confirmed"
        decided = "Confirm: the slope's t is 2 or more and the mean excess 5-day return is above 0."
    elif t_slope <= -2:
        status = "rejected"
        decided = "Reject: the slope's t is -2 or less."
    elif t_slope >= 2:
        status = "inconclusive"
        decided = "Inconclusive: the slope's t is 2 or more but the mean excess return is 0 or below."
    else:
        status = "inconclusive"
        decided = "Inconclusive: the slope's t is between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": slope,
            "statistic": ({"name": "OLS slope t", "value": t_slope} if t_slope is not None else None),
            "threshold": threshold,
        },
        "supporting_check": {"name": "mean in-regime 5-day excess return > 0", "value": mean_excess,
                             "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
