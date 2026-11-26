import numpy as np
import pandas as pd


def _to_time(s):
    if np.issubdtype(s.dtype, np.number):
        v = s.dropna()
        med = float(v.abs().median()) if len(v) else 0.0
        unit = "ms" if med > 1e11 else "s"
        return pd.to_datetime(s, unit=unit, utc=True, errors="coerce")
    return pd.to_datetime(s, utc=True, errors="coerce")


def measure(bars):
    H = 5
    RAW = "debug_info.components.ma_dist.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin in sorted(bars):
        for w in sorted(bars[coin]):
            df = bars[coin][w].reset_index(drop=True)
            if len(df) == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce")
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            # recompute the SMA-20 distance from prices inside the window, used only where the raw value is missing
            sma = close.rolling(20, min_periods=20).mean()
            dist_px = (close / sma - 1.0) * 100.0
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
                dist = raw.where(raw.notna(), dist_px)
            else:
                dist = dist_px
            profile = df["regime"].astype(str) == "unknown"  # rising-calm profile: not vetoed to chop
            situation = profile & (dist > 0)
            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc > 0)).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)
    main_name = "slope t of demeaned 5-bar return on forecast, grid bars with forecast > 0"
    threshold = "confirm: slope > 0 with t >= 2; reject: slope < 0 with t <= -2; else inconclusive"
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"grid cases with forecast > 0": None, "distinct days": None, "active bars": n_active},
            "decided_by": ("Fewer than 90% of bars with a nonzero forecast are long bars in the rising-calm regime "
                           "with the close above its 20-day SMA, so the config does not do what the Fidelity says."),
            "reading": ("The situation was taken as regime 'unknown' (the profile not vetoed) with a positive raw "
                        "ma_dist (recomputed from closes where missing), and the expected side was long."),
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin in sorted(bars):
        for w in sorted(bars[coin]):
            df = bars[coin][w].reset_index(drop=True)
            n = len(df)
            if n <= H:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            ts = _to_time(df["timestamp"])
            for t in range(0, n - H, H):
                r = close[t + H] / close[t] - 1.0
                if not np.isfinite(r):
                    continue
                d = ts.iloc[t]
                rows.append({"coin": coin, "ret": r, "fc": fc[t],
                             "day": d.strftime("%Y-%m-%d") if pd.notna(d) else None})
    g = pd.DataFrame(rows, columns=["coin", "ret", "fc", "day"])
    if len(g):
        coin_mean = g.groupby("coin")["ret"].mean()
        g["y"] = g["ret"] - g["coin"].map(coin_mean)
    else:
        g["y"] = []
    c = g[(g["fc"] > 0) & g["fc"].notna() & g["y"].notna() & g["day"].notna()].copy()
    n_cases = int(len(c))
    n_days = int(c["day"].nunique()) if n_cases else 0
    counts = {"grid cases with forecast > 0": n_cases, "distinct days": n_days}

    slope, tstat = None, None
    if n_cases >= 3:
        x = c["fc"].values.astype(float)
        y = c["y"].values.astype(float)
        xc = x - x.mean()
        sxx = float((xc ** 2).sum())
        if sxx > 0:
            b = float((xc * (y - y.mean())).sum() / sxx)
            e = y - y.mean() - b * xc
            sc = pd.Series(xc * e).groupby(c["day"].values).sum().values
            G = len(sc)
            corr = (G / (G - 1)) * ((n_cases - 1) / (n_cases - 2)) if G > 1 else np.nan
            var = corr * float((sc ** 2).sum()) / sxx ** 2
            slope = b
            tstat = float(b / np.sqrt(var)) if np.isfinite(var) and var > 0 else None

    reading = ("Cases on the same day were pooled across coins by a day-clustered standard error on the OLS slope; "
               "the coin's mean 5-bar return is over all its grid bars of all windows; the situation was regime "
               "'unknown' with a positive raw ma_dist, long side.")

    if n_cases < 100 or n_days < 60:
        status = "not observable"
        decided = (f"The plan's minimum counts were not reached ({n_cases} grid cases with forecast > 0 of 100, "
                   f"{n_days} distinct days of 60).")
    elif tstat is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif slope > 0 and tstat >= 2:
        status = "confirmed"
        decided = "The slope is positive with t >= 2: a larger distance above the average is followed by a larger rise beyond drift."
    elif slope < 0 and tstat <= -2:
        status = "rejected"
        decided = "The slope is negative with t <= -2: a larger distance is followed by a smaller rise or a fall."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name,
                         "value": slope,
                         "statistic": ({"name": "OLS slope t, day-clustered", "value": tstat}
                                       if tstat is not None else None),
                         "threshold": threshold},
        "supporting_check": None,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
