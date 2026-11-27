import numpy as np
import pandas as pd


def _component_series(df, comp_id, field="last_history_value"):
    col = f"debug_info.components.{comp_id}.{field}"
    if col in df.columns:
        return pd.to_numeric(df[col], errors="coerce")
    if "debug_info.components" in df.columns:
        def _get(v):
            try:
                if isinstance(v, dict):
                    c = v.get(comp_id)
                    if isinstance(c, dict):
                        return c.get(field, np.nan)
            except Exception:
                pass
            return np.nan
        return pd.to_numeric(df["debug_info.components"].map(_get), errors="coerce")
    return pd.Series(np.nan, index=df.index)


def _clustered_t(values, days):
    values = np.asarray(values, dtype=float)
    n = len(values)
    if n < 2:
        return None
    m = values.mean()
    dev = pd.Series(values - m).groupby(np.asarray(days)).sum().values
    D = len(dev)
    if D < 2:
        return None
    var = (dev ** 2).sum() / n ** 2 * D / (D - 1)
    if not np.isfinite(var) or var <= 0:
        return None
    return float(m / np.sqrt(var))


def measure(bars):
    H = 10
    BAND = 2.0

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            close = pd.to_numeric(df["close"], errors="coerce")
            trend = (close / close.shift(60) - 1.0) * 100.0
            depth = _component_series(df, "depth")
            regime = df["regime"].astype(str) if "regime" in df.columns else pd.Series("", index=df.index)
            trend_ok = trend.between(-10.0, 10.0)
            # where the 60-day return cannot be computed inside the window, fall back to the detector's regime
            trend_ok = trend_ok.where(trend.notna(), regime == "trending")
            depth_ok = depth <= -2.0
            situ = trend_ok & depth_ok.fillna(False)
            active = f != 0
            n_active += int(active.sum())
            n_agree += int((active & situ & (f < 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.9

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": "mean short-direction 10-day excess return", "value": None,
                             "statistic": None, "threshold": "above 0 with day-clustered t >= 2 (reject: below 0 with t <= -2)"},
            "supporting_check": None,
            "counts": {"cases": 0, "distinct case days": 0, "active bars": n_active},
            "decided_by": ("Fewer than 90 % of the active bars are short bars in the plan's situation "
                           "(60-day return within -10 %..+10 % and 30-day depth <= -2 usual moves)."
                           if n_active > 0 else "The record has no active bar, so the forecast does not show the plan's situation."),
            "reading": "The 60-day return is recomputed from closes inside each window, and on bars where 60 earlier bars are not in the window the detector's regime stands in for it; depth is the recorded raw value of the 'depth' component; any nonzero forecast that is not negative counts as disagreement.",
        }

    # ---------- 2. criterion ----------
    vals, days, absf = [], [], []
    for coin, wins in bars.items():
        # normal 10-day drift of the coin over all windows (non-overlapping grid)
        grid_rets = []
        for w, df in wins.items():
            c = pd.to_numeric(df["close"], errors="coerce").values
            for p in range(0, len(c) - H, H):
                if np.isfinite(c[p]) and np.isfinite(c[p + H]) and c[p] > 0:
                    grid_rets.append(c[p + H] / c[p] - 1.0)
        if not grid_rets:
            continue
        drift = float(np.mean(grid_rets))

        for w, df in wins.items():
            df = df.reset_index(drop=True)
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            c = pd.to_numeric(df["close"], errors="coerce").values
            ts = pd.to_datetime(df["timestamp"], utc=True)
            ref = 0.0
            taken_cells = set()
            for t in range(len(df)):
                bet = False
                if f[t] < 0:
                    mag = -f[t]
                    if mag - ref >= BAND:
                        bet = True
                        ref = mag
                    else:
                        ref = min(ref, mag)
                else:
                    ref = 0.0
                if not bet:
                    continue
                cell = t // H
                if cell in taken_cells:
                    continue
                taken_cells.add(cell)
                if t + H >= len(df):
                    continue
                if not (np.isfinite(c[t]) and np.isfinite(c[t + H]) and c[t] > 0):
                    continue
                r = c[t + H] / c[t] - 1.0
                vals.append(-(r - drift))
                days.append(ts.iloc[t].strftime("%Y-%m-%d"))
                absf.append(abs(f[t]))

    n = len(vals)
    n_days = len(set(days))
    counts = {"cases": n, "distinct case days": n_days}
    mean_val = float(np.mean(vals)) if n > 0 else None
    tval = _clustered_t(vals, days) if n > 1 else None

    diff = None
    if n > 1:
        a = np.asarray(absf)
        v = np.asarray(vals)
        med = np.median(a)
        deep = v[a > med]
        shallow = v[a <= med]
        if len(deep) > 0 and len(shallow) > 0:
            diff = float(deep.mean() - shallow.mean())
    sup_pass = None if diff is None else bool(diff > 0)

    reading = ("Cases are short bets (forecast magnitude rising >= 2 points from its lowest short level since the last bet, "
               "from 0 after flat or long), the first bet in each 10-bar grid cell of a window, measured from its bar's close; "
               "the deeper half is |forecast| above the median and the shallower half at or below it; on bars without 60 in-window "
               "earlier bars the detector's regime stands in for the 60-day-return condition in the situation check.")

    main = {"name": "mean short-direction 10-day excess return", "value": mean_val,
            "statistic": None if tval is None else {"name": "day-clustered t of the mean", "value": tval},
            "threshold": "above 0 with t >= 2 to confirm; below 0 with t <= -2 to reject"}
    support = {"name": "deeper-half minus shallower-half mean excess return (median |forecast| split)",
               "value": diff, "passed": sup_pass}
    sc = {"agreement": agreement, "passed": True}

    if n < 30 or n_days < 20:
        status = "not observable"
        decided = f"Minimum counts not reached: {n} cases (need 30) and {n_days} distinct case days (need 20)."
    elif tval is None or mean_val is None:
        status = "inconclusive"
        decided = "The t-statistic could not be computed, so neither the confirm nor the reject rule is met."
    elif mean_val > 0 and tval >= 2 and sup_pass:
        status = "confirmed"
        decided = "Mean short-direction excess return above 0 with t >= 2 and the deeper-minus-shallower difference above 0."
    elif mean_val < 0 and tval <= -2:
        status = "rejected"
        decided = "Mean short-direction excess return below 0 with t <= -2."
    elif mean_val > 0 and tval >= 2:
        status = "inconclusive"
        decided = "A confirming t with the depth check failed (deeper-minus-shallower difference not above 0) is inconclusive."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2 (or its sign disagrees with the mean's), meeting neither confirm nor reject."

    return {
        "status": status,
        "situation_check": sc,
        "main_measure": main,
        "supporting_check": support,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
