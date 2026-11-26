import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    RAW = "debug_info.components.range_pos.last_history_value"

    # ---------- 1. Situation check ----------
    # Situation: the choppy calm profile, i.e. the regime detector's default regime "unknown"
    # (the vetoes send every other bar to "chop", which has no strategy).
    # Expected side: the sign of the 20-day range position (long above the middle, short below).
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.sort_values("timestamp").reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            reg = df["regime"].astype(str).values
            hi20 = df["high"].rolling(20, min_periods=20).max()
            lo20 = df["low"].rolling(20, min_periods=20).min()
            rng = (hi20 - lo20).replace(0, np.nan)
            pos_px = ((2 * (df["close"] - lo20) / rng - 1) * 20).values
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce").values
            else:
                raw = np.full(len(df), np.nan)
            pos = np.where(np.isnan(raw), pos_px, raw)
            active = fc != 0
            n_active += int(active.sum())
            ok = (reg == "unknown") & ~np.isnan(pos) & (np.sign(pos) == np.sign(fc)) & active
            n_agree += int(ok.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.9

    main_name = "slope of excess 5-bar forward return on forecast (non-overlapping grid, nonzero forecast)"
    threshold = "confirm: slope > 0 with t >= 2; reject: slope < 0 with t <= -2; else inconclusive"
    reading = ("The situation is the bars whose regime is 'unknown' (the choppy calm profile) and the side is the sign "
               "of the recorded range position (rebuilt from the 20-bar high/low where not recorded); the coin's mean "
               "5-bar return is taken over all grid bars of all its windows; the slope is OLS of excess return on "
               "forecast with a day-clustered standard error (per-day sums of x-deviation times residual, with the "
               "G/(G-1) correction); the plan's minimum of 100 cases over 50 days is applied as 'not observable'.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a nonzero forecast are choppy calm ('unknown' regime) bars "
                           "whose forecast sign matches the side of the close in its 20-day range."),
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    xs, ys, days = [], [], []
    for coin, wins in bars.items():
        grid_rets = []
        cases = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            ts = pd.to_datetime(df["timestamp"], utc=True)
            n = len(df)
            for i in range(0, n - H, H):
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                grid_rets.append(r)
                f = fc[i]
                if np.isfinite(f) and f != 0:
                    cases.append((float(f), r, ts.iloc[i].strftime("%Y-%m-%d")))
        if len(grid_rets) == 0:
            continue
        mu = float(np.mean(grid_rets))
        for f, r, d in cases:
            xs.append(f)
            ys.append(r - mu)
            days.append(d)

    n_cases = len(xs)
    n_days = len(set(days))
    counts = {"grid cases with a nonzero forecast": int(n_cases), "distinct days": int(n_days)}

    slope = None
    tval = None
    if n_cases >= 3:
        x = np.asarray(xs, float)
        y = np.asarray(ys, float)
        xd = x - x.mean()
        sxx = float(np.sum(xd ** 2))
        if sxx > 0:
            b = float(np.sum(xd * (y - y.mean())) / sxx)
            a = y.mean() - b * x.mean()
            e = y - a - b * x
            s = pd.Series(xd * e).groupby(pd.Series(days)).sum().values
            G = len(s)
            corr = G / (G - 1) if G > 1 else 1.0
            var = corr * float(np.sum(s ** 2)) / sxx ** 2
            slope = b
            tval = float(b / np.sqrt(var)) if var > 0 else None

    stat = {"name": "slope t (day-clustered)", "value": tval} if tval is not None else None
    main = {"name": main_name, "value": slope, "statistic": stat, "threshold": threshold}
    sc = {"agreement": agreement, "passed": True}

    if n_cases < 100 or n_days < 50:
        return {
            "status": "not observable",
            "situation_check": sc,
            "main_measure": main,
            "supporting_check": None,
            "counts": counts,
            "decided_by": "The plan's minimum of 100 grid cases with a nonzero forecast over at least 50 distinct days is not reached.",
            "reading": reading,
        }

    if slope is None or tval is None:
        status = "inconclusive"
        decided = "The slope or its t could not be computed, so neither the confirm nor the reject rule is met."
    elif slope > 0 and tval >= 2:
        status = "confirmed"
        decided = "Confirm rule: the slope is positive with t >= 2 (excess 5-day return grows with range position)."
    elif slope < 0 and tval <= -2:
        status = "rejected"
        decided = "Reject rule: the slope is negative with t <= -2 (higher closes in the range are followed by smaller excess returns)."
    else:
        status = "inconclusive"
        decided = "Inconclusive rule: the slope's t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": sc,
        "main_measure": main,
        "supporting_check": None,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
