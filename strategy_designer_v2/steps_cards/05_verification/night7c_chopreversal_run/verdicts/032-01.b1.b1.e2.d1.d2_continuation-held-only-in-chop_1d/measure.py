import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 7
    ER_N = 30
    ER_MAX = 0.3
    RAW = "debug_info.components.scaled_week.last_history_value"
    POST = "debug_info.components.scaled_week.post_pipeline_value"

    # ---------- 1. situation check ----------
    n_active_checked = 0
    n_agree = 0
    n_active_total = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float).values
            fc = df["forecast"].astype(float).values
            n = len(df)
            # raw 30-day efficiency ratio from the prices, inside the window
            er = np.full(n, np.nan)
            absd = np.abs(np.diff(close, prepend=np.nan))
            for t in range(ER_N, n):
                den = np.nansum(absd[t - ER_N + 1:t + 1])
                net = abs(close[t] - close[t - ER_N])
                er[t] = net / den if den > 0 else np.nan
            # raw scaled 7-day move: recorded raw value, else from prices
            raw = df[RAW].astype(float).values if RAW in df.columns else np.full(n, np.nan)
            ret7 = np.full(n, np.nan)
            if n > H:
                ret7[H:] = close[H:] / close[:-H] - 1.0
            raw = np.where(np.isnan(raw), ret7, raw)
            for t in range(n):
                if not np.isfinite(fc[t]) or fc[t] == 0:
                    continue
                n_active_total += 1
                if np.isnan(er[t]) or np.isnan(raw[t]):
                    continue
                n_active_checked += 1
                in_sit = er[t] <= ER_MAX + 1e-9
                side_ok = np.sign(fc[t]) == np.sign(raw[t]) and raw[t] != 0
                if in_sit and side_ok:
                    n_agree += 1
    agreement = (n_agree / n_active_checked) if n_active_checked > 0 else None
    passed = agreement is not None and agreement >= 0.9

    reading = ("Active bars whose 30-day efficiency ratio cannot be computed inside their window (first 30 bars) "
               "are left out of the agreement share; the expected side is the sign of the raw scaled 7-day move "
               "(continuation); the coin's mean 7-bar return is the mean over all its windows' grid returns; "
               "the timing part is the mean daily (per-day mean over coins) of position x (coin's daily return "
               "minus its mean daily return over all windows), before costs; fewer than 100 grid cases gives "
               "'not observable'.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement) if agreement is not None else None, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active_total), "active bars checked": int(n_active_checked)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are bars with a raw 30-day "
                           "efficiency ratio at or below 0.3 and a forecast on the side of the 7-day move."),
            "reading": reading,
        }

    # ---------- 2. main measure ----------
    xs, ys = [], []
    for coin, wins in bars.items():
        grid = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float).values
            fc = df["forecast"].astype(float).values
            post = df[POST].astype(float).values if POST in df.columns else np.full(len(df), np.nan)
            for t in range(0, len(df), H):
                if t + H >= len(df):
                    break
                r = close[t + H] / close[t] - 1.0
                if not np.isfinite(r):
                    continue
                x = post[t] if np.isfinite(post[t]) else fc[t]
                grid.append((r, fc[t], x))
        if not grid:
            continue
        mean_r = np.mean([g[0] for g in grid])
        for r, f, x in grid:
            if np.isfinite(f) and f != 0 and np.isfinite(x):
                xs.append(x)
                ys.append(r - mean_r)
    n_cases = len(xs)
    slope = None
    tval = None
    if n_cases >= 3 and np.std(xs) > 0:
        res = stats.linregress(np.array(xs), np.array(ys))
        slope = float(res.slope)
        tval = float(res.slope / res.stderr) if res.stderr > 0 else None

    # ---------- supporting check: timing part ----------
    rows = []
    for coin, wins in bars.items():
        all_r = []
        per = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float).values
            alloc = df["postRebalance_current_allocation"].astype(float).values
            day = pd.to_datetime(df["timestamp"], utc=True).dt.floor("D").values
            r = close[1:] / close[:-1] - 1.0
            all_r.extend(list(r[np.isfinite(r)]))
            per.append((day[1:], alloc[:-1], r))
        if not all_r:
            continue
        mu = float(np.mean(all_r))
        for d, a, r in per:
            for di, ai, ri in zip(d, a, r):
                if np.isfinite(ai) and np.isfinite(ri):
                    rows.append((di, ai * (ri - mu)))
    timing = None
    if rows:
        tdf = pd.DataFrame(rows, columns=["day", "timing"])
        timing = float(tdf.groupby("day")["timing"].mean().mean())
    sup_pass = None if timing is None else bool(timing > 0)

    counts = {"grid cases with a non-zero forecast": int(n_cases)}
    main = {
        "name": "slope of demeaned 7-bar forward return on forecast, pooled",
        "value": slope,
        "statistic": {"name": "OLS slope t", "value": tval} if tval is not None else None,
        "threshold": "confirm: slope > 0 with t >= 2 and timing > 0; reject: slope < 0 with t <= -2",
    }
    supporting = {"name": "timing part of mean daily book return before costs", "value": timing, "passed": sup_pass}

    if n_cases < 100 or tval is None:
        status = "not observable"
        decided = f"Only {n_cases} grid cases with a non-zero forecast, fewer than the 100 the plan requires."
    elif slope > 0 and tval >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "The slope is positive with t >= 2 and the timing part is above 0."
        else:
            status = "inconclusive"
            decided = "The slope is positive with t >= 2 but the timing part is at or below 0."
    elif slope < 0 and tval <= -2:
        status = "rejected"
        decided = "The slope is negative with t <= -2."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": main,
        "supporting_check": supporting,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
