import numpy as np
import pandas as pd


def measure(bars):
    H = 5

    def _comp_series(df, comp_id, field="last_history_value"):
        col = "debug_info.components.%s.%s" % (comp_id, field)
        if col in df.columns:
            return pd.to_numeric(df[col], errors="coerce")
        if "debug_info.components" in df.columns:
            vals = []
            for v in df["debug_info.components"].values:
                out = np.nan
                try:
                    if isinstance(v, dict) and comp_id in v and isinstance(v[comp_id], dict):
                        x = v[comp_id].get(field, None)
                        if x is not None:
                            out = float(x)
                except Exception:
                    out = np.nan
                vals.append(out)
            return pd.Series(vals, index=df.index, dtype=float)
        return pd.Series(np.nan, index=df.index, dtype=float)

    # ---------- situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            close = pd.to_numeric(df["close"], errors="coerce").values
            raw = _comp_series(df, "ret5").values
            rec = np.full(len(df), np.nan)
            if len(df) > H:
                rec[H:] = close[H:] / close[:-H] - 1.0
            ret5 = np.where(np.isnan(raw), rec, raw)
            regime = df["regime"].astype(str).values if "regime" in df.columns else np.array(["unknown"] * len(df))
            for i in range(len(df)):
                if fc[i] == 0 or np.isnan(fc[i]):
                    continue
                n_active += 1
                in_profile = regime[i] == "unknown"
                r = ret5[i]
                if in_profile and not np.isnan(r) and r != 0 and np.sign(r) == np.sign(fc[i]):
                    n_agree += 1
    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "OLS slope of next 5-bar return minus coin mean 5-bar return on forecast/10 (grid, forecast != 0)"
    threshold = "confirm: slope > 0 with t >= 2; reject: slope < 0 with t <= -2; else inconclusive; needs >= 100 grid cases and >= 60 distinct days"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("fewer than 90% of active bars are in the falling calm profile (regime not vetoed) with the "
                           "forecast's sign equal to the past 5-day return's sign (continuation)"
                           if n_active > 0 else "no active bars: the config never takes the plan's situation"),
            "reading": "The profile is read from the recorded regime ('unknown' = not vetoed by the falling/calm vetoes) and the side from the sign of the ret5 raw value (recomputed from closes where missing).",
        }

    # ---------- main measure ----------
    xs, ys, days = [], [], []
    for coin, wins in bars.items():
        all_r = []
        cases = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            ts = pd.to_datetime(df["timestamp"], utc=True)
            for i in range(0, len(df), H):
                if i + H >= len(df):
                    break
                r = close[i + H] / close[i] - 1.0
                if not np.isfinite(r):
                    continue
                all_r.append(r)
                f = fc[i]
                if np.isfinite(f) and f != 0:
                    cases.append((f / 10.0, r, ts.iloc[i].strftime("%Y-%m-%d")))
        if not all_r:
            continue
        mu = float(np.mean(all_r))
        for x, r, d in cases:
            xs.append(x)
            ys.append(r - mu)
            days.append(d)

    n_cases = len(xs)
    n_days = len(set(days))
    counts = {"grid cases": int(n_cases), "distinct days": int(n_days)}

    slope = None
    tval = None
    if n_cases >= 3:
        x = np.asarray(xs, float)
        y = np.asarray(ys, float)
        xm, ym = x.mean(), y.mean()
        sxx = float(np.sum((x - xm) ** 2))
        if sxx > 0:
            slope = float(np.sum((x - xm) * (y - ym)) / sxx)
            a = ym - slope * xm
            e = y - a - slope * x
            s = pd.Series((x - xm) * e).groupby(pd.Series(days)).sum().values
            G = len(s)
            if G > 1:
                var_b = (G / (G - 1.0)) * float(np.sum(s ** 2)) / sxx ** 2
                if var_b > 0:
                    tval = float(slope / np.sqrt(var_b))

    reading = ("Profile read from the recorded regime ('unknown' = not vetoed) and side from the sign of ret5; the slope is "
               "ordinary least squares with an intercept, the coin's mean 5-bar return is taken over all grid bars of all its "
               "windows, and the t uses a day-clustered standard error (per-day sums of score, G/(G-1) correction).")

    if n_cases < 100 or n_days < 60:
        status = "not observable"
        decided = "minimum counts not reached: %d grid cases (need 100) and %d distinct days (need 60)." % (n_cases, n_days)
    elif slope is None or tval is None:
        status = "inconclusive"
        decided = "the slope or its t could not be computed, so neither the confirm nor the reject rule is met."
    elif slope > 0 and tval >= 2:
        status = "confirmed"
        decided = "confirm rule: the slope is positive with t >= 2."
    elif slope < 0 and tval <= -2:
        status = "rejected"
        decided = "reject rule: the slope is negative with t <= -2."
    else:
        status = "inconclusive"
        decided = "inconclusive rule: the slope's t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": slope,
            "statistic": ({"name": "t of slope, day-clustered", "value": tval} if tval is not None else None),
            "threshold": threshold,
        },
        "supporting_check": None,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
