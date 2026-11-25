import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    BAND = 2.0
    MIN_CASES = 30

    def comp_series(df, cid, field="last_history_value"):
        col = f"debug_info.components.{cid}.{field}"
        if col in df.columns:
            return pd.to_numeric(df[col], errors="coerce")
        if "debug_info.components" in df.columns:
            out = []
            for v in df["debug_info.components"].values:
                val = np.nan
                try:
                    d = v
                    if isinstance(d, str):
                        import json
                        d = json.loads(d)
                    if isinstance(d, dict) and cid in d and isinstance(d[cid], dict):
                        x = d[cid].get(field, None)
                        if x is not None:
                            val = float(x)
                except Exception:
                    val = np.nan
                out.append(val)
            return pd.Series(out, index=df.index, dtype=float)
        return pd.Series(np.nan, index=df.index, dtype=float)

    # ---------- situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            high = pd.to_numeric(df["high"], errors="coerce")
            low = pd.to_numeric(df["low"], errors="coerce")
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)

            # condition 1: 30-day return < 0 (from prices, inside the window)
            ret30 = close / close.shift(30) - 1.0
            # condition 2: mean range over 365 bars / mean range over 30 bars < 1
            rng_bar = (high - low) / close
            long_m = rng_bar.rolling(365, min_periods=365).mean()
            short_m = rng_bar.rolling(30, min_periods=30).mean()
            rng = long_m / short_m
            # condition 3: close below the prior 30-bar extreme (recorded raw value, else from lows)
            depth = comp_series(df, "depth")
            prior_low = low.shift(1).rolling(30, min_periods=30).min()
            brk_price = close / prior_low - 1.0
            brk = depth.where(depth.notna(), brk_price)

            active = fc != 0
            for i in np.where(active.values)[0]:
                n_active += 1
                ok = True
                v = ret30.iloc[i]
                if pd.notna(v) and not (v < 0):
                    ok = False
                v = rng.iloc[i]
                if pd.notna(v) and not (v < 1.0):
                    ok = False
                v = brk.iloc[i]
                if pd.notna(v) and not (v < 0):
                    ok = False
                if not (fc.iloc[i] > 0):
                    ok = False
                if ok:
                    n_agree += 1

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = True if agreement is None else bool(agreement >= 0.9)

    reading = ("Each situation condition is checked only where it can be computed from the window's own bars "
               "(the 365-bar range ratio and the 30-bar return cannot be computed early in a window and are then not "
               "counted against the bar), the break uses the recorded depth value; a case is the first bet "
               "(forecast rise >= 2 from its lowest positive level since the last bet, from 0 after flat) in each "
               "5-bar grid cell of a window, its return runs from that bar's close 5 bars ahead inside the window, "
               "the normal drift is the coin's mean non-overlapping 5-bar return over all windows, and the t is "
               "day-clustered with a G/(G-1) correction.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": "mean unusual 5-bar move after a case", "value": None,
                             "statistic": None, "threshold": "mean > 0 with t >= 2 (confirm), mean < 0 with t <= -2 (reject)"},
            "supporting_check": None,
            "counts": {"cases": None},
            "decided_by": ("Fewer than 90% of the active bars are bars where the 30-day return is negative, the range "
                           "ratio is below 1 and the close is below the prior 30-day low with a long forecast."),
            "reading": reading,
        }

    # ---------- normal drift per coin ----------
    drift = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            c = pd.to_numeric(df["close"], errors="coerce").values
            for p in range(0, len(c) - H, H):
                if np.isfinite(c[p]) and np.isfinite(c[p + H]) and c[p] > 0:
                    rets.append(c[p + H] / c[p] - 1.0)
        drift[coin] = float(np.mean(rets)) if rets else np.nan

    # ---------- cases ----------
    cases = []  # (day, unusual, forecast)
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            c = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            ts = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
            base = 0.0
            bet = np.zeros(len(df), dtype=bool)
            for i in range(len(df)):
                f = fc[i]
                if f <= 0:
                    base = 0.0
                    continue
                if f - base >= BAND:
                    bet[i] = True
                    base = f
                else:
                    base = min(base, f)
            seen = set()
            for i in np.where(bet)[0]:
                cell = i // H
                if cell in seen:
                    continue
                seen.add(cell)
                j = i + H
                if j >= len(df):
                    continue
                if not (np.isfinite(c[i]) and np.isfinite(c[j]) and c[i] > 0):
                    continue
                d = drift.get(coin, np.nan)
                if not np.isfinite(d):
                    continue
                u = (c[j] / c[i] - 1.0) - d
                day = ts.iloc[i].strftime("%Y-%m-%d") if pd.notna(ts.iloc[i]) else f"{coin}-{w}-{i}"
                cases.append((day, u, float(fc[i])))

    n = len(cases)
    days = len(set(x[0] for x in cases))
    threshold = "confirm: mean > 0 with t >= 2 and slope > 0; reject: mean < 0 with t <= -2; at least 30 cases"
    mm_name = "mean unusual 5-bar move after a case (long, minus the coin's normal 5-bar drift)"

    if n < MIN_CASES:
        mean_u = float(np.mean([x[1] for x in cases])) if n else None
        return {
            "status": "not observable",
            "situation_check": {"agreement": agreement, "passed": True},
            "main_measure": {"name": mm_name, "value": mean_u, "statistic": None, "threshold": threshold},
            "supporting_check": {"name": "OLS slope of unusual move on forecast", "value": None, "passed": None},
            "counts": {"cases": int(n), "days": int(days)},
            "decided_by": f"Fewer than 30 cases ({n}), so the result is not observable whatever the t.",
            "reading": reading,
        }

    u = np.array([x[1] for x in cases])
    f = np.array([x[2] for x in cases])
    m = float(u.mean())
    dev = pd.Series(u - m).groupby([x[0] for x in cases]).sum().values
    G = len(dev)
    var = (np.sum(dev ** 2) / n ** 2) * (G / (G - 1)) if G > 1 else np.nan
    t = float(m / np.sqrt(var)) if np.isfinite(var) and var > 0 else float("nan")

    slope = None
    if np.std(f) > 0:
        slope = float(np.polyfit(f, u, 1)[0])
    slope_pass = bool(slope is not None and slope > 0)

    if np.isfinite(t) and m > 0 and t >= 2:
        if slope_pass:
            status = "confirmed"
            decided = "Mean unusual move above 0 with t >= 2 and a positive slope on the forecast: confirm rule met."
        else:
            status = "inconclusive"
            decided = "Mean unusual move above 0 with t >= 2 but the slope is not above 0: inconclusive."
    elif np.isfinite(t) and m < 0 and t <= -2:
        status = "rejected"
        decided = "Mean unusual move below 0 with t <= -2: reject rule met."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2 (or is undefined): inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": mm_name, "value": m,
                         "statistic": {"name": "t of the mean, cases of one day taken together",
                                       "value": t if np.isfinite(t) else None},
                         "threshold": threshold},
        "supporting_check": {"name": "OLS slope of unusual move on forecast", "value": slope, "passed": slope_pass},
        "counts": {"cases": int(n), "days": int(days)},
        "decided_by": decided,
        "reading": reading,
    }
