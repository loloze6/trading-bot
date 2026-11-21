import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    C_NEAR = "debug_info.components.near_high.last_history_value"
    C_OFF = "debug_info.components.offset.last_history_value"
    C_RET = "debug_info.components.ret20.last_history_value"
    P_NEAR = "debug_info.components.near_high.post_pipeline_value"
    P_OFF = "debug_info.components.offset.post_pipeline_value"
    P_RET = "debug_info.components.ret20.post_pipeline_value"

    def standardise(raw, window, min_periods, fallback):
        raw = pd.to_numeric(raw, errors="coerce").astype(float)
        denom = raw.abs().shift(1).rolling(window, min_periods=min_periods).mean()
        val = raw * 10.0 / denom
        val = val.where(denom != 0, 0.0).clip(-20, 20)
        # The record holds no warm-up bars: where the window's own history is too short,
        # use the engine's recorded value after transforms.
        if fallback is not None:
            fb = pd.to_numeric(fallback, errors="coerce").astype(float)
            val = val.where(denom.notna(), fb)
        return val

    def col(df, c):
        if c in df.columns:
            return df[c]
        return pd.Series(np.nan, index=df.index)

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            near = standardise(col(df, C_NEAR), 90, 22, col(df, P_NEAR))
            off = standardise(col(df, C_OFF), 60, 20, col(df, P_OFF))
            ret = standardise(col(df, C_RET), 60, 20, col(df, P_RET))
            expected = ((near + off + ret) / 3.0).clip(-20, 20)
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            ok = active & expected.notna() & (expected != 0) & (np.sign(expected) == np.sign(fc))
            n_agree += int(ok.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "pooled OLS slope of next 5-bar excess return on forecast (non-overlapping grid)"
    threshold = "confirm: t >= 2 with timing gain > 0; reject: t <= -2; else inconclusive; at least 200 grid cases with non-zero forecast"
    reading = ("The situation is rebuilt as the sign of the mean of the three standardised components "
               "(from raw values, using the recorded post-pipeline value where a window's own history is too short); "
               "the slope uses every grid bar (zero forecasts included) while the minimum count is the grid bars with "
               "non-zero forecast; the timing gain uses the before-cost position gain, allocation x next bar return, "
               "averaged over coins per day; fewer than 200 cases gives 'not observable' per the workflow rule.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast have the sign of the plan's graded "
                           "sum (nearness to the 90-day high + offset + 20-day return) / 3."),
            "reading": reading,
        }

    # ---------- 2. main measure ----------
    xs, ys = [], []
    for coin, wins in bars.items():
        grid = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            for i in range(0, len(df) - H, H):
                r = close[i + H] / close[i] - 1.0
                grid.append((fc[i], r))
        if not grid:
            continue
        g = np.array(grid, dtype=float)
        rets = g[:, 1]
        mu = np.nanmean(rets) if np.isfinite(rets).any() else np.nan
        for f, r in g:
            if np.isfinite(f) and np.isfinite(r) and np.isfinite(mu):
                xs.append(f)
                ys.append(r - mu)
    xs = np.array(xs, dtype=float)
    ys = np.array(ys, dtype=float)
    n_grid = int(len(xs))
    n_nonzero = int(np.sum(xs != 0))

    slope, t_val = None, None
    if n_grid >= 3 and np.std(xs) > 0:
        lr = stats.linregress(xs, ys)
        slope = float(lr.slope)
        t_val = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    # ---------- supporting check: timing gain ----------
    rows = []
    for coin, wins in bars.items():
        parts = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            nxt = close.shift(-1) / close - 1.0
            alloc = pd.to_numeric(df["postRebalance_current_allocation"], errors="coerce")
            parts.append(pd.DataFrame({"timestamp": df["timestamp"], "alloc": alloc, "r": nxt}))
        if not parts:
            continue
        d = pd.concat(parts, ignore_index=True).dropna(subset=["alloc", "r"])
        if d.empty:
            continue
        mu_d = d["r"].mean()
        d["gross"] = d["alloc"] * d["r"]
        d["market"] = d["alloc"] * mu_d
        d["coin"] = coin
        rows.append(d)
    timing = None
    if rows:
        allr = pd.concat(rows, ignore_index=True)
        daily = allr.groupby("timestamp")[["gross", "market"]].mean()
        timing = float(daily["gross"].mean() - daily["market"].mean())
    timing_pass = None if timing is None else bool(timing > 0)

    counts = {"grid cases with a non-zero forecast": n_nonzero, "grid cases": n_grid}

    if n_nonzero < 200 or t_val is None:
        status = "not observable"
        decided = (f"Only {n_nonzero} grid cases with a non-zero forecast, below the plan's minimum of 200."
                   if n_nonzero < 200 else "The slope's t could not be computed.")
    elif t_val >= 2 and timing_pass:
        status = "confirmed"
        decided = "The slope's t is 2 or more and the timing gain is above 0."
    elif t_val >= 2:
        status = "inconclusive"
        decided = "The slope's t is 2 or more but the timing gain is 0 or below."
    elif t_val <= -2:
        status = "rejected"
        decided = "The slope's t is -2 or less."
    else:
        status = "inconclusive"
        decided = "The slope's t is between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": slope,
                         "statistic": None if t_val is None else {"name": "OLS slope t", "value": t_val},
                         "threshold": threshold},
        "supporting_check": {"name": "book timing gain before costs (mean daily)", "value": timing,
                             "passed": timing_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
