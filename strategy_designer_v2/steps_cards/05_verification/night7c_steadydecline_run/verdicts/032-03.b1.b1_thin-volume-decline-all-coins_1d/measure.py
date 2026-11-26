import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    RAW = "debug_info.components.rel_volume.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float).values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            raw = pd.to_numeric(df[RAW], errors="coerce").values if RAW in df.columns else np.full(len(df), np.nan)
            n = len(df)
            for t in range(n):
                f = fc[t]
                if not np.isfinite(f) or f == 0:
                    continue
                if t < 28:
                    continue  # 28-bar return not computable inside the window: left out
                n_active += 1
                r28 = close[t] / close[t - 28] - 1.0
                in_sit = np.isfinite(r28) and r28 < 0
                r = raw[t]
                side_ok = np.isfinite(r) and r != 0 and np.sign(f) == np.sign(r)
                if in_sit and side_ok:
                    n_agree += 1
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    reading = ("The situation is recomputed as close[t]/close[t-28]-1 < 0 inside each window (active bars with fewer "
               "than 28 prior bars in their window are left out of the agreement), the expected side is the sign of the "
               "raw log volume ratio (standardise keeps the sign, fall-side short when volume is thin); the coin's normal "
               "5-day drift is the mean of its non-overlapping 5-bar grid returns over all its windows, and the slope's t "
               "uses a day-clustered standard error (per-day summed score deviations, with G/(G-1) correction).")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a nonzero forecast are bars with a negative 28-bar return "
                           "whose forecast sign matches the sign of the raw log volume ratio."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    # coin drift over all windows (non-overlapping grid)
    drift = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            close = df["close"].astype(float).values
            for t in range(0, len(close) - H, H):
                r = close[t + H] / close[t] - 1.0
                if np.isfinite(r):
                    rets.append(r)
        drift[coin] = float(np.mean(rets)) if rets else np.nan

    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float).values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            reg = df["regime"].astype(str).values
            ts = pd.to_datetime(df["timestamp"], utc=True)
            for t in range(0, len(df) - H, H):
                if reg[t] != "trending":
                    continue
                f = fc[t]
                if not np.isfinite(f) or f == 0:
                    continue
                r = close[t + H] / close[t] - 1.0
                if not np.isfinite(r) or not np.isfinite(drift[coin]):
                    continue
                rows.append((ts.iloc[t].strftime("%Y-%m-%d"), float(f), float(r - drift[coin])))

    n_cases = len(rows)
    days = sorted(set(r[0] for r in rows))
    n_days = len(days)
    counts = {"cases": int(n_cases), "distinct days": int(n_days)}
    threshold = "slope > 0 with t >= 2 confirms (with supporting check); slope < 0 with t <= -2 rejects"
    mm_name = "slope of 5-day excess return on forecast (day-clustered t)"

    slope = None
    tval = None
    sup_val = None
    sup_pass = None
    if n_cases >= 3:
        d = np.array([r[0] for r in rows])
        x = np.array([r[1] for r in rows])
        y = np.array([r[2] for r in rows])
        xm, ym = x.mean(), y.mean()
        sxx = float(np.sum((x - xm) ** 2))
        if sxx > 0:
            b = float(np.sum((x - xm) * (y - ym)) / sxx)
            a = ym - b * xm
            e = y - a - b * x
            sc = pd.Series((x - xm) * e).groupby(d).sum().values
            G = len(sc)
            var = float(np.sum(sc ** 2)) / sxx ** 2
            if G > 1:
                var *= G / (G - 1)
            se = np.sqrt(var)
            slope = b
            tval = float(b / se) if se > 0 else None
        neg = y[x < 0]
        if len(neg) > 0:
            sup_val = float(neg.mean())
            sup_pass = bool(sup_val < 0)
        else:
            sup_pass = False

    main = {"name": mm_name, "value": slope,
            "statistic": {"name": "day-clustered t of slope", "value": tval} if tval is not None else None,
            "threshold": threshold}
    sup = {"name": "mean excess 5-day return of cases with forecast < 0 below 0",
           "value": sup_val, "passed": sup_pass}

    if n_cases < 150 or n_days < 100:
        status = "not observable"
        decided = (f"The plan's minimum of 150 cases over 100 distinct days is not reached "
                   f"({n_cases} cases, {n_days} days).")
    elif tval is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif slope > 0 and tval >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "The slope is positive with t >= 2 and thin-volume cases have a negative mean excess return."
        else:
            status = "inconclusive"
            decided = "The slope is positive with t >= 2 but the supporting check (mean excess of forecast<0 cases below 0) fails."
    elif slope < 0 and tval <= -2:
        status = "rejected"
        decided = "The slope is negative with t <= -2."
    else:
        status = "inconclusive"
        decided = "The slope's |t| is below 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
