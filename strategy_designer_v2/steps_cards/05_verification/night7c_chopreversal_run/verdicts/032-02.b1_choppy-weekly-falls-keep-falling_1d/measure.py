import numpy as np
import pandas as pd


def measure(bars):
    H = 7
    BAND = 2.0
    ER_COL = "debug_info.components.chop.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float)
            fc = df["forecast"].astype(float)
            ret7 = close / close.shift(7) - 1.0
            diff_abs = close.diff().abs()
            er_px = (close - close.shift(30)).abs() / diff_abs.rolling(30).sum()
            er = df[ER_COL].astype(float) if ER_COL in df.columns else pd.Series(np.nan, index=df.index)
            er = er.where(er.notna(), er_px)
            regime_mr = df["regime"].astype(str) == "mean_reversion"
            for i in range(len(df)):
                f = fc.iloc[i]
                if not np.isfinite(f) or f == 0:
                    continue
                n_active += 1
                r7 = ret7.iloc[i]
                cond_ret = (r7 < 0) if np.isfinite(r7) else bool(regime_mr.iloc[i])
                e = er.iloc[i]
                cond_er = (e < 0.3) if np.isfinite(e) else bool(regime_mr.iloc[i])
                # volatility percentile needs ~135 bars of history, unavailable in a window: taken from the detector's regime
                cond_vol = bool(regime_mr.iloc[i])
                if cond_ret and cond_er and cond_vol and f < 0:
                    n_agree += 1
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.9
    reading = ("Situation = 7-bar close return < 0 (from prices) and chop.last_history_value < 0.3 (prices if missing) "
               "and the volatility-percentile condition read from regime == mean_reversion (it cannot be rebuilt from a "
               "window's prices), short side expected; cases = first short bet (forecast magnitude rising >= 2 points "
               "from its lowest level since the last bet) per 7-bar grid cell of each window, drift = coin's mean "
               "non-overlapping 7-bar grid return over all its windows, day-clustered t with G/(G-1) correction, "
               "forecast size = |forecast| at the signal bar.")
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the active bars are short bars of the plan's situation "
                           "(7-day fall, 30-bar ER < 0.3, agitated volatility percentile)."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin, wins in bars.items():
        # coin's normal drift: mean 7-bar return on the grid of all its windows
        grid_rets = []
        for w, df in wins.items():
            c = df["close"].astype(float).values
            for p in range(0, len(c) - H, H):
                if np.isfinite(c[p]) and np.isfinite(c[p + H]) and c[p] > 0:
                    grid_rets.append(c[p + H] / c[p] - 1.0)
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float).values
            fc = df["forecast"].astype(float).fillna(0.0).values
            ts = pd.to_datetime(df["timestamp"], utc=True)
            ref = 0.0
            bets = []
            for i in range(len(df)):
                s = -fc[i] if fc[i] < 0 else 0.0
                if fc[i] >= 0:
                    ref = 0.0
                    continue
                if s - ref >= BAND:
                    bets.append(i)
                    ref = s
                else:
                    ref = min(ref, s)
            seen = set()
            for i in bets:
                cell = i // H
                if cell in seen:
                    continue
                seen.add(cell)
                if i + H >= len(c) or not (np.isfinite(c[i]) and np.isfinite(c[i + H])) or c[i] <= 0:
                    continue
                r = c[i + H] / c[i] - 1.0
                rows.append({"day": ts.iloc[i].floor("D"), "unusual": -(r - drift), "size": abs(fc[i])})

    cases = pd.DataFrame(rows, columns=["day", "unusual", "size"])
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0
    counts = {"cases": n_cases, "distinct days": n_days}
    thr = "mean > 0 with t >= 2 (and supporting check) confirms; mean < 0 with t <= -2 rejects"

    mean = float(cases["unusual"].mean()) if n_cases else None
    t = None
    if n_cases >= 2 and n_days >= 2:
        dev = cases["unusual"] - mean
        g = dev.groupby(cases["day"]).sum().values
        G = len(g)
        var = (G / (G - 1)) * np.sum(g ** 2) / n_cases ** 2
        se = float(np.sqrt(var))
        t = float(mean / se) if se > 0 else None

    sup_val, sup_pass = None, None
    if n_cases >= 2:
        med = cases["size"].median()
        strong = cases.loc[cases["size"] > med, "unusual"]
        weak = cases.loc[cases["size"] <= med, "unusual"]
        if len(strong) > 0 and len(weak) > 0:
            sup_val = float(strong.mean() - weak.mean())
            sup_pass = bool(sup_val > 0)
        else:
            sup_pass = False

    main = {"name": "mean unusual 7-bar move of short cases (short direction)",
            "value": mean,
            "statistic": {"name": "day-clustered t", "value": t} if t is not None else None,
            "threshold": thr}
    support = {"name": "stronger minus weaker (above vs at/below median forecast size) mean unusual move",
               "value": sup_val, "passed": sup_pass}

    if n_cases < 30 or n_days < 30:
        status = "not observable"
        decided = f"Minimum counts not reached: {n_cases} cases and {n_days} distinct days (30 of each needed)."
    elif t is None:
        status = "inconclusive"
        decided = "The t could not be computed, so neither the confirm nor the reject rule is met."
    elif mean > 0 and t >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "Mean unusual move positive with t >= 2 and the supporting check passes."
        else:
            status = "inconclusive"
            decided = "Mean unusual move positive with t >= 2 but the supporting check fails, which the plan calls inconclusive."
    elif mean < 0 and t <= -2:
        status = "rejected"
        decided = "Mean unusual move negative with t <= -2."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": support,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
