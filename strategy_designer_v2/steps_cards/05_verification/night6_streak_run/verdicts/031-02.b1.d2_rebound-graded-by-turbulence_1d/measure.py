import numpy as np
import pandas as pd


def measure(bars):
    RAW = "debug_info.components.fall_volratio.last_history_value"
    H = 2

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").astype(float)
            fc = pd.to_numeric(d["forecast"], errors="coerce").astype(float)
            ret = close / close.shift(1) - 1.0  # inside the window only
            if RAW in d.columns:
                raw = pd.to_numeric(d[RAW], errors="coerce").astype(float)
            else:
                raw = pd.Series(np.nan, index=d.index)
            # Recompute the product from prices where the raw value is missing.
            sd10 = ret.rolling(10, min_periods=10).std()
            sd60 = ret.rolling(60, min_periods=60).std()
            prod = (np.maximum(0.0, -ret) / sd60) * (sd10 / sd60)
            raw_f = raw.where(raw.notna(), prod)
            fall_from_price = ret < 0
            # The situation: a fall today, with a positive fall x turbulence product.
            situation = (raw_f > 0) & (fall_from_price | ret.isna())
            situation = situation.fillna(False)
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc > 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.90)

    main_name = "OLS slope of excess 2-bar return on forecast, grid bars with forecast > 0"
    threshold = "confirm: slope t >= 2 and mean excess > 0; reject: slope t <= -2"
    reading = ("Situation = bars whose raw component value (or its recomputation from prices when missing) is > 0 "
               "on a down close, long side; grid = rows 0,2,4,... of each window; the coin's mean 2-bar return is "
               "the mean over all its windows' grid returns; the slope's t uses a day-clustered standard error "
               "(per-day sums of the score, factor G/(G-1)); the plan's minimum counts, when not reached, give "
               "'not observable'.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars after a fall with a "
                           "positive fall x turbulence product, as the plan's Fidelity requires."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    xs, ys, days = [], [], []
    for coin, wins in bars.items():
        recs = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").astype(float).values
            fc = pd.to_numeric(d["forecast"], errors="coerce").astype(float).values
            ts = pd.to_datetime(d["timestamp"], utc=True)
            n = len(d)
            for i in range(0, n, H):
                if i + H >= n:
                    continue
                if not (np.isfinite(close[i]) and np.isfinite(close[i + H]) and close[i] != 0):
                    continue
                r = close[i + H] / close[i] - 1.0
                recs.append((r, fc[i], ts.iloc[i].strftime("%Y-%m-%d")))
        if not recs:
            continue
        rets = np.array([x[0] for x in recs])
        mu = float(np.mean(rets))
        for r, f, dy in recs:
            if np.isfinite(f) and f > 0:
                xs.append(float(f))
                ys.append(r - mu)
                days.append(dy)

    x = np.array(xs, dtype=float)
    y = np.array(ys, dtype=float)
    days = np.array(days)
    n_cases = int(len(x))
    n_days = int(len(np.unique(days))) if n_cases else 0
    counts = {"grid bars with forecast > 0": n_cases, "distinct days": n_days}

    mean_ex = float(np.mean(y)) if n_cases else None
    slope, t = None, None
    if n_cases >= 3 and np.var(x) > 0:
        xc = x - x.mean()
        sxx = float(np.sum(xc ** 2))
        slope = float(np.sum(xc * y) / sxx)
        a = float(y.mean() - slope * x.mean())
        e = y - a - slope * x
        s = pd.Series(xc * e).groupby(days).sum().values
        G = len(s)
        if G > 1:
            var = float(np.sum(s ** 2)) / sxx ** 2 * G / (G - 1)
            if var > 0:
                t = float(slope / np.sqrt(var))

    sup_pass = None if mean_ex is None else bool(mean_ex > 0)
    out = {
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": slope,
                         "statistic": None if t is None else {"name": "slope t, day-clustered", "value": t},
                         "threshold": threshold},
        "supporting_check": {"name": "mean excess 2-bar return on forecast > 0 grid bars",
                             "value": mean_ex, "passed": sup_pass},
        "counts": counts,
        "reading": reading,
    }

    if n_cases < 300 or n_days < 150:
        out["status"] = "not observable"
        out["decided_by"] = (f"Minimum counts not reached: {n_cases} grid bars with forecast > 0 (300 needed) "
                             f"across {n_days} distinct days (150 needed).")
        return out
    if t is None:
        out["status"] = "inconclusive"
        out["decided_by"] = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
        return out
    if t >= 2 and sup_pass:
        out["status"] = "confirmed"
        out["decided_by"] = "Confirm: the slope's t is 2 or more and the mean excess 2-bar return on forecast > 0 bars is above 0."
    elif t <= -2:
        out["status"] = "rejected"
        out["decided_by"] = "Reject: the slope's t is -2 or less; larger turbulence-weighted falls are followed by smaller 2-day returns."
    elif t >= 2:
        out["status"] = "inconclusive"
        out["decided_by"] = "Inconclusive: the slope's t is 2 or more but the mean excess return is at or below 0."
    else:
        out["status"] = "inconclusive"
        out["decided_by"] = "Inconclusive: the slope's t is between -2 and 2."
    return out
