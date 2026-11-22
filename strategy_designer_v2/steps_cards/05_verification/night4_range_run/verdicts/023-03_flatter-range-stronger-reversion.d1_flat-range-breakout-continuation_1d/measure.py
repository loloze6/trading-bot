import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    RAW = "debug_info.components.flat_range_pos.last_history_value"
    MIN_CASES = 300

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = df["close"].astype(float)
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            # Rebuild the raw value from the closes where it is missing.
            # The window and the formula match the plan: 31 closes, period 30.
            hi = close.rolling(31, min_periods=31).max()
            lo = close.rolling(31, min_periods=31).min()
            rng = hi - lo
            pos = (close - lo) / rng
            flat = 1 - (close - close.shift(30)).abs() / rng
            recomputed = (2 * pos - 1) * flat
            raw = raw.where(raw.notna(), recomputed)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            # Situation: the close is above or below the middle of its range
            # (raw != 0). Expected side: continuation, so sign(forecast) == sign(raw).
            agree = active & raw.notna() & (raw != 0) & (np.sign(fc) == np.sign(raw))
            n_agree += int(agree.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "OLS slope of drift-removed 5-bar return on forecast, non-overlapping grid, coins pooled"
    thr = "confirm: slope > 0 with t >= 2 (and timing gain > 0); reject: slope < 0 with t <= -2"
    sup_name = "timing gain: book mean daily return before costs minus gain from market's rise"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": "Fewer than 90% of active bars have a forecast sign matching the side of the middle of the "
                          "30-day closing range that the close sits on, which is the continuation side the Fidelity states.",
            "reading": "The situation is a raw value != 0. The expected side is the sign of the raw value "
                       "(close above the middle means long).",
        }

    # ---------- 2. Main measure ----------
    grid_rows = []  # (coin, ret, forecast)
    daily_rows = []  # (timestamp, coin, pos, r1)
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = df["close"].astype(float).values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            n = len(df)
            for i in range(0, n - H, H):
                r = close[i + H] / close[i] - 1
                grid_rows.append((coin, r, fc[i]))
            alloc = pd.to_numeric(df["postRebalance_current_allocation"], errors="coerce").values
            ts = pd.to_datetime(df["timestamp"], utc=True)
            for i in range(n - 1):
                r1 = close[i + 1] / close[i] - 1
                daily_rows.append((ts.iloc[i].floor("D"), coin, alloc[i], r1))

    g = pd.DataFrame(grid_rows, columns=["coin", "ret", "fc"])
    g = g[np.isfinite(g["ret"])]
    # Normal drift: the mean of each coin's non-overlapping 5-bar returns over all windows.
    drift = g.groupby("coin")["ret"].mean()
    g["ex"] = g["ret"] - g["coin"].map(drift)
    g = g[np.isfinite(g["fc"]) & np.isfinite(g["ex"])]
    n_cases = int(len(g))

    slope = None
    tval = None
    if n_cases >= 3 and g["fc"].std() > 0:
        lr = stats.linregress(g["fc"].values, g["ex"].values)
        slope = float(lr.slope)
        tval = float(lr.slope / lr.stderr) if lr.stderr > 0 else None

    # ---------- Supporting check: timing gain ----------
    d = pd.DataFrame(daily_rows, columns=["day", "coin", "pos", "r1"])
    d = d[np.isfinite(d["r1"])]
    mu = d.groupby("coin")["r1"].mean()
    d = d[np.isfinite(d["pos"])]
    timing = None
    if len(d) > 0:
        d["gain"] = d["pos"] * d["r1"]
        d["mkt"] = d["pos"] * d["coin"].map(mu)
        per_day = d.groupby("day")[["gain", "mkt"]].mean()
        timing = float(per_day["gain"].mean() - per_day["mkt"].mean())
    sup_pass = None if timing is None else bool(timing > 0)

    counts = {"grid cases": n_cases}
    reading = ("All grid bars count as cases, including bars with forecast 0. The regression has an intercept. "
               "The drift is each coin's mean grid 5-bar return over all windows. The timing gain uses per-bar "
               "position x next-bar return, averaged over coins per UTC day, minus position x the coin's mean "
               "daily return.")

    if n_cases < MIN_CASES or slope is None or tval is None:
        status = "not observable"
        decided = f"Only {n_cases} grid cases, fewer than the plan's minimum of 300 across coins and windows."
    elif slope > 0 and tval >= 2 and sup_pass:
        status = "confirmed"
        decided = "The slope is positive with t >= 2 and the timing gain is above zero."
    elif slope < 0 and tval <= -2:
        status = "rejected"
        decided = "The slope is negative with t <= -2: price reverts toward the middle in proportion to the forecast."
    elif slope > 0 and tval >= 2:
        status = "inconclusive"
        decided = "The slope is positive with t >= 2 but the timing gain is not above zero."
    else:
        status = "inconclusive"
        decided = "The slope's |t| < 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": slope,
            "statistic": None if tval is None else {"name": "OLS slope t", "value": tval},
            "threshold": thr,
        },
        "supporting_check": {"name": sup_name, "value": timing, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
