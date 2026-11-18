import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 3
    MIN_CASES = 20

    def _num(df, col):
        if col in df.columns:
            return pd.to_numeric(df[col], errors="coerce")
        return pd.Series(np.nan, index=df.index)

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    n_active_unevaluable = 0

    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            o = _num(df, "open")
            h = _num(df, "high")
            l = _num(df, "low")
            c = _num(df, "close")
            v = _num(df, "volume")
            f = _num(df, "forecast").fillna(0.0)

            # ret component: 1-bar return over its 20-bar std (implementation variants tolerated)
            r1 = c.pct_change()
            sd_inc1 = r1.rolling(20, min_periods=20).std(ddof=1)
            sd_inc0 = r1.rolling(20, min_periods=20).std(ddof=0)
            sd_exc1 = r1.shift(1).rolling(20, min_periods=20).std(ddof=1)
            sd_exc0 = r1.shift(1).rolling(20, min_periods=20).std(ddof=0)
            z = pd.concat([r1 / sd_inc1, r1 / sd_inc0, r1 / sd_exc1, r1 / sd_exc0], axis=1)
            z_eval = z.notna().any(axis=1)
            ret_ok = (z <= -2.0).any(axis=1)

            # vol component: volume over median of the prior 20 bars
            med = v.shift(1).rolling(20, min_periods=20).median()
            vr = v / med
            vol_eval = vr.notna()
            vol_ok = vr >= 2.0

            # wick component: lower wick over range
            rng = h - l
            wick = (np.minimum(o, c) - l) / rng.replace(0, np.nan)
            wick_eval = wick.notna()
            wick_ok = wick >= 0.3

            evaluable = z_eval & vol_eval & wick_eval
            situation = ret_ok & vol_ok & wick_ok
            active = f != 0
            on_side = f > 0  # outcome: price rises -> long

            act_eval = active & evaluable
            n_active += int(act_eval.sum())
            n_agree += int((act_eval & situation & on_side).sum())
            n_active_unevaluable += int((active & ~evaluable).sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9

    reading = (
        "Detector components recomputed from each window's own prices (return z accepted under any of the "
        "std variants with/without the current bar and ddof 0/1; volume over the median of the prior 20 bars; "
        "lower wick = (min(open,close)-low)/(high-low)), active bars without 20 bars of in-window history left "
        "out of the agreement; the coin's mean 3-bar return is taken on the non-overlapping grid (positions 0,3,6,...) "
        "of all its windows pooled; flush cases are bars with regime mean_reversion and forecast > 0 and a 3-bar "
        "forward return inside the window, skipping any within 3 bars after a counted one in the same window, pooled "
        "across coins for one OLS; the plan's 'fewer than 20 independent flush cases' minimum is reported as not observable."
    )

    main_name = "OLS slope t of excess 3-bar forward return on forecast, flush bars"
    threshold = "confirm if slope t >= 2 with forecast-weighted mean excess > 0; reject if slope t <= -2"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars evaluated": n_active,
                       "active bars not evaluable": n_active_unevaluable},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are flush bars (return <= -2 usual moves, "
                           "volume >= 2x prior median, lower wick >= 0.3 of range) with a positive (long) forecast, "
                           "as the plan's Fidelity requires." if n_active > 0 else
                           "No evaluable bar with a non-zero forecast, so the forecast cannot be shown to follow the plan's flush situation."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    xs, ys = [], []
    for coin, wins in bars.items():
        # coin's mean 3-bar return over all windows (non-overlapping grid)
        grid = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            c = _num(df.reset_index(drop=True), "close").values
            for i in range(0, len(c) - H, H):
                if np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] != 0:
                    grid.append(c[i + H] / c[i] - 1.0)
        if len(grid) == 0:
            continue
        coin_mean = float(np.mean(grid))

        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            c = _num(df, "close").values
            f = _num(df, "forecast").values
            reg = df["regime"].astype(str).values if "regime" in df.columns else np.array([""] * len(df))
            last_counted = -10 ** 9
            n = len(df)
            for t in range(n):
                if not (reg[t] == "mean_reversion" and np.isfinite(f[t]) and f[t] > 0):
                    continue
                if t - last_counted <= H:
                    continue
                if t + H >= n:
                    continue
                if not (np.isfinite(c[t]) and np.isfinite(c[t + H]) and c[t] != 0):
                    continue
                fr = c[t + H] / c[t] - 1.0
                xs.append(float(f[t]))
                ys.append(fr - coin_mean)
                last_counted = t

    x = np.asarray(xs, dtype=float)
    y = np.asarray(ys, dtype=float)
    n_cases = int(len(x))

    slope = None
    t_slope = None
    if n_cases >= 3 and np.std(x) > 0:
        lr = stats.linregress(x, y)
        slope = float(lr.slope)
        if lr.stderr is not None and np.isfinite(lr.stderr) and lr.stderr > 0:
            t_slope = float(lr.slope / lr.stderr)

    wmean = float(np.sum(y * x) / np.sum(x)) if n_cases > 0 and np.sum(x) > 0 else None
    sup_passed = (wmean > 0) if wmean is not None else None

    counts = {"independent flush cases": n_cases}

    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"Only {n_cases} independent flush cases across all coins and windows, fewer than the plan's minimum of 20."
    elif t_slope is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed (no variation in the forecast), so neither confirm nor reject is met."
    elif t_slope >= 2 and sup_passed:
        status = "confirmed"
        decided = "The slope's t is 2 or more and the forecast-weighted mean excess return is above 0."
    elif t_slope <= -2:
        status = "rejected"
        decided = "The slope's t is -2 or less."
    elif t_slope >= 2:
        status = "inconclusive"
        decided = "The slope's t is 2 or more but the forecast-weighted mean excess return is at or below 0."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name,
                         "value": slope,
                         "statistic": ({"name": "OLS slope t", "value": t_slope} if t_slope is not None else None),
                         "threshold": threshold},
        "supporting_check": {"name": "forecast-weighted mean excess 3-bar return > 0",
                             "value": wmean, "passed": sup_passed},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
