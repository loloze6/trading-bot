import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    BAND = 2.0
    LHV = "debug_info.components.heavy_volume.last_history_value"

    # ---------- per-window preparation ----------
    prepared = []  # (coin, window, df)
    for coin in sorted(bars.keys()):
        for w in sorted(bars[coin].keys(), key=lambda s: (len(str(s)), str(s))):
            df = bars[coin][w]
            if df is None or len(df) == 0:
                continue
            df = df.copy().reset_index(drop=True)
            df["ts"] = pd.to_datetime(df["timestamp"], utc=True)
            df["fc"] = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            close = pd.to_numeric(df["close"], errors="coerce")
            vol = pd.to_numeric(df["volume"], errors="coerce")
            df["close_"] = close
            reg_tr = df["regime"].astype(str).str.lower().eq("trending")
            df["reg_tr"] = reg_tr

            # volume ratio: recorded raw value + 1 where present, else from prices (prior 20 bars)
            vr_price = vol / vol.shift(1).rolling(20, min_periods=20).mean()
            if LHV in df.columns:
                lhv = pd.to_numeric(df[LHV], errors="coerce")
            else:
                lhv = pd.Series(np.nan, index=df.index)
            vr = (lhv + 1.0).where(lhv.notna(), vr_price)
            df["vr"] = lhv + 1.0
            vr_ok = (vr >= 1.5).where(vr.notna(), reg_tr)

            # up close: 1-day return > 0 (inside the window)
            r1 = close / close.shift(1) - 1.0
            up_ok = (r1 > 0).where(r1.notna(), reg_tr)

            # falling: 60-bar return below -10 % (percent units), inside the window
            r60 = (close / close.shift(60) - 1.0) * 100.0
            fall_ok = (r60 < -10).where(r60.notna(), reg_tr)

            # calm (volatility percentile over 365 bars cannot be rebuilt in a window):
            # the detector's decision (no veto fired <=> regime trending)
            calm_ok = reg_tr

            df["situation"] = (vr_ok.astype(bool) & up_ok.astype(bool)
                               & fall_ok.astype(bool) & calm_ok.astype(bool))
            prepared.append((coin, w, df))

    # ---------- situation check ----------
    n_active = 0
    n_agree = 0
    for coin, w, df in prepared:
        act = df["fc"] != 0
        n_active += int(act.sum())
        n_agree += int((act & df["situation"] & (df["fc"] > 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "mean unusual 5-bar move per case (long), cases of one day together"
    threshold = "confirm: mean > 0 with t >= 2 and supporting check > 0; reject: mean < 0 with t <= -2"
    sup_name = "mean unusual move, heavier half minus lighter half (median volume ratio)"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars of the plan's situation "
                           "(falling calm market, up close, volume >= 1.5x its prior 20-day mean)"
                           if n_active > 0 else "The record has no bar with a non-zero forecast."),
            "reading": "The calm part of the profile is read from the detector's regime (its 365-bar volatility "
                       "percentile cannot be rebuilt inside a window); other parts from prices and recorded raw values, "
                       "falling back on the regime where a window lacks the history.",
        }

    # ---------- normal drift per coin (non-overlapping grid, all windows) ----------
    drift = {}
    for coin in sorted(set(c for c, _, _ in prepared)):
        rets = []
        for c, w, df in prepared:
            if c != coin:
                continue
            cl = df["close_"].values
            for p in range(0, len(df) - H, H):
                a, b = cl[p], cl[p + H]
                if np.isfinite(a) and np.isfinite(b) and a > 0:
                    rets.append(b / a - 1.0)
        drift[coin] = float(np.mean(rets)) if rets else np.nan

    # ---------- cases ----------
    cases = []  # dict(u, day, vr)
    for coin, w, df in prepared:
        fc = df["fc"].values
        cl = df["close_"].values
        n = len(df)
        low = 0.0
        bet = np.zeros(n, dtype=bool)
        for i in range(n):
            f = fc[i]
            if f > 0:
                if f - low >= BAND:
                    bet[i] = True
                    low = f
                else:
                    low = min(low, f)
            else:
                low = 0.0
        for start in range(0, n, H):
            idx = [i for i in range(start, min(start + H, n)) if bet[i]]
            if not idx:
                continue
            t = idx[0]
            if t + H >= n:
                continue
            a, b = cl[t], cl[t + H]
            if not (np.isfinite(a) and np.isfinite(b) and a > 0) or not np.isfinite(drift[coin]):
                continue
            u = (b / a - 1.0) - drift[coin]
            cases.append({"u": u, "day": df["ts"].iloc[t].strftime("%Y-%m-%d"),
                          "vr": float(df["vr"].iloc[t]) if np.isfinite(df["vr"].iloc[t]) else np.nan})

    n_cases = len(cases)
    days = sorted(set(c["day"] for c in cases))
    n_days = len(days)
    counts = {"cases": int(n_cases), "distinct days": int(n_days)}

    mean_u = None
    t_val = None
    if n_cases > 0:
        u = np.array([c["u"] for c in cases])
        mean_u = float(u.mean())
        if n_days > 1:
            dev = pd.Series(u - mean_u).groupby([c["day"] for c in cases]).sum().values
            var = (n_days / (n_days - 1)) * float(np.sum(dev ** 2)) / (n_cases ** 2)
            se = np.sqrt(var)
            t_val = float(mean_u / se) if se > 0 else None

    # supporting check
    sup_val = None
    sup_pass = None
    vr_cases = [(c["vr"], c["u"]) for c in cases if np.isfinite(c["vr"])]
    if len(vr_cases) >= 2:
        v = np.array([x[0] for x in vr_cases])
        uu = np.array([x[1] for x in vr_cases])
        med = np.median(v)
        heavy = uu[v > med]
        light = uu[v <= med]
        if len(heavy) > 0 and len(light) > 0:
            sup_val = float(heavy.mean() - light.mean())
            sup_pass = bool(sup_val > 0)
        else:
            sup_pass = False

    reading = ("A case is the first long bet (forecast rise >= 2 points from its low since the last bet) in each "
               "5-bar grid cell from each window's first row; the t clusters deviations by UTC day with a G/(G-1) "
               "correction; the heavier half is volume ratio above the median, the lighter half at or below it; "
               "the plan's 'fewer than 30 cases or 20 days' is reported as not observable; calm is read from the "
               "detector's regime.")

    main = {"name": main_name, "value": mean_u,
            "statistic": {"name": "t of the mean, cases of one day together", "value": t_val} if t_val is not None else None,
            "threshold": threshold}
    sup = {"name": sup_name, "value": sup_val, "passed": sup_pass}

    if n_cases < 30 or n_days < 20:
        status = "not observable"
        decided = (f"Minimum counts not reached: {n_cases} cases (need 30) and {n_days} distinct days (need 20).")
    elif t_val is None:
        status = "inconclusive"
        decided = "The t of the mean could not be computed, so neither the confirm nor the reject rule is met."
    elif mean_u > 0 and t_val >= 2 and sup_pass is True:
        status = "confirmed"
        decided = "The mean unusual move is above 0 with t >= 2 and the heavier-minus-lighter difference is above 0."
    elif mean_u > 0 and t_val >= 2:
        status = "inconclusive"
        decided = "The main measure meets the confirm rule but the supporting check fails, which the plan calls inconclusive."
    elif mean_u < 0 and t_val <= -2:
        status = "rejected"
        decided = "The mean unusual move is below 0 with t <= -2."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
