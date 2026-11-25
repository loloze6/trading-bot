import json
import numpy as np
import pandas as pd


def _component_series(df, comp_id, field="last_history_value"):
    """Read a recorded component value, from a flattened column or from the debug_info.components dicts."""
    flat = f"debug_info.components.{comp_id}.{field}"
    if flat in df.columns:
        return pd.to_numeric(df[flat], errors="coerce")
    if "debug_info.components" not in df.columns:
        return pd.Series(np.nan, index=df.index)
    out = []
    for v in df["debug_info.components"].values:
        val = np.nan
        d = v
        if isinstance(d, str):
            try:
                d = json.loads(d)
            except Exception:
                d = None
        if isinstance(d, dict):
            c = d.get(comp_id)
            if isinstance(c, dict):
                x = c.get(field)
                try:
                    val = float(x) if x is not None else np.nan
                except Exception:
                    val = np.nan
        out.append(val)
    return pd.Series(out, index=df.index, dtype=float)


def _to_time(s):
    if np.issubdtype(s.dtype, np.number):
        mx = float(np.nanmax(s.values)) if len(s) else 0.0
        unit = "ms" if mx > 1e11 else "s"
        return pd.to_datetime(s, unit=unit, utc=True)
    return pd.to_datetime(s, utc=True)


def measure(bars):
    H = 5
    BAND = 2.0

    # ---------------- 1. situation check ----------------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            low = pd.to_numeric(df["low"], errors="coerce")
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            regime = df["regime"].astype(str)

            # ret30 from prices (inside the window, where 30 past bars exist)
            ret30 = close / close.shift(30) - 1.0
            # depth under the prior 30-bar low: recorded value, else recomputed from prices
            depth_rec = _component_series(df, "depth", "last_history_value")
            prior_low = low.shift(1).rolling(30, min_periods=30).min()
            depth_px = close / prior_low - 1.0
            depth = depth_rec.where(depth_rec.notna(), depth_px)

            in_regime = regime == "mean_reversion"
            ret_ok = (ret30 < 0) | ret30.isna()
            brk_ok = (depth < 0) | depth.isna()
            situation = in_regime & ret_ok & brk_ok

            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc > 0)).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "mean 5-bar unusual move of long cases (return minus normal 5-bar drift)"
    thr = "confirm: mean > 0 with t >= 2 and slope > 0; reject: mean < 0 with t <= -2"
    sup_name = "least-squares slope of per-case unusual move on forecast"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "agreeing bars": int(n_agree)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars of the plan's situation "
                           "(mean_reversion regime with 30-day return below 0, wide ranges, close below the prior "
                           "30-day low)" if n_active > 0 else "The record has no bar with a non-zero forecast."),
            "reading": ("The situation is the regime column 'mean_reversion' (the detector's three-condition decision, "
                        "since its 365-bar range ratio cannot be rebuilt inside a window), cross-checked with the 30-bar "
                        "return from prices and the recorded depth below the prior 30-bar low where available."),
        }

    # ---------------- 2. criterion ----------------
    cases = []  # (unusual, forecast, day)
    for coin, wins in bars.items():
        # normal drift: mean of non-overlapping 5-bar returns on each window's grid, all windows together
        grid_rets = []
        prepared = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            n = len(close)
            for p in range(0, n - H, H):
                r = close[p + H] / close[p] - 1.0
                if np.isfinite(r):
                    grid_rets.append(r)
            prepared.append(df)
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))

        for df in prepared:
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            ts = _to_time(df["timestamp"])
            days = ts.dt.strftime("%Y-%m-%d").values
            n = len(df)
            ref = 0.0
            used_cells = set()
            for t in range(n):
                f = fc[t]
                if f <= 0:
                    ref = 0.0
                    continue
                if f - ref >= BAND:
                    ref = f
                    cell = t // H
                    if cell in used_cells:
                        continue
                    used_cells.add(cell)
                    if t + H < n:
                        r = close[t + H] / close[t] - 1.0
                        if np.isfinite(r):
                            cases.append((r - drift, float(f), days[t]))
                else:
                    ref = min(ref, f)

    n_cases = len(cases)
    n_days = len(set(c[2] for c in cases))
    counts = {"cases": int(n_cases), "distinct days": int(n_days)}

    mean_u = None
    tval = None
    slope = None
    if n_cases > 0:
        u = np.array([c[0] for c in cases], dtype=float)
        f = np.array([c[1] for c in cases], dtype=float)
        d = np.array([c[2] for c in cases])
        mean_u = float(u.mean())
        dev = pd.Series(u - mean_u).groupby(d).sum().values
        D = len(dev)
        if D > 1:
            se = np.sqrt(D / (D - 1.0) * np.sum(dev ** 2)) / n_cases
            tval = float(mean_u / se) if se > 0 else None
        if n_cases > 1 and np.var(f) > 0:
            slope = float(np.polyfit(f, u, 1)[0])

    stat = {"name": "t of the mean, cases summed per day", "value": tval} if tval is not None else None
    sup_passed = (slope > 0) if slope is not None else None
    reading = ("Situation = regime 'mean_reversion' cross-checked with price-based 30-bar return and recorded depth; "
               "a case is a forecast rise of at least 2 above its lowest long level since the last bet (from 0 after a "
               "flat), the first per 5-bar grid cell from each window's first row, dropped if its 5-bar return leaves "
               "the window; the drift is each coin's mean grid 5-bar return over all its windows; t uses per-day summed "
               "deviations with a D/(D-1) factor; the plan's 'fewer is inconclusive' minimum is reported as 'not observable'.")

    if n_cases < 30 or n_days < 20:
        status = "not observable"
        decided = f"The plan's minimum of 30 cases on 20 distinct days is not reached ({n_cases} cases on {n_days} days)."
    elif tval is None:
        status = "inconclusive"
        decided = "The t of the mean unusual move could not be computed, so neither confirm nor reject is met."
    elif mean_u > 0 and tval >= 2 and slope is not None and slope > 0:
        status = "confirmed"
        decided = "The mean unusual move is above 0 with t >= 2 and the slope on the forecast is above 0."
    elif mean_u < 0 and tval <= -2:
        status = "rejected"
        decided = "The mean unusual move is below 0 with t <= -2."
    elif tval >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the slope of the unusual move on the forecast is at or below 0 (or undefined)."
    else:
        status = "inconclusive"
        decided = "t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": mean_u, "statistic": stat, "threshold": thr},
        "supporting_check": {"name": sup_name, "value": slope, "passed": sup_passed},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
