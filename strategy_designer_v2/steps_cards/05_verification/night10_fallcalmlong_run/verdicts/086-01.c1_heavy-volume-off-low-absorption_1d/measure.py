import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    BAND = 2.0
    VOL_PERIOD = 20
    VOL_THR = 1.5

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            vol = pd.to_numeric(d["volume"], errors="coerce")
            base = vol.shift(1).rolling(VOL_PERIOD, min_periods=VOL_PERIOD).mean()
            volr = vol / base.replace(0, np.nan)
            hi = pd.to_numeric(d["high"], errors="coerce")
            lo = pd.to_numeric(d["low"], errors="coerce")
            cl = pd.to_numeric(d["close"], errors="coerce")
            rng = (hi - lo).replace(0, np.nan)
            cloc = (cl - lo) / rng
            fc = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0)
            regime = d["regime"].astype(str) if "regime" in d.columns else pd.Series([""] * len(d))
            heavy = volr >= VOL_THR
            # bars without 20 prior bars in the window: fall back on the detector's recorded decision
            heavy = heavy.where(volr.notna(), regime == "trending")
            situation = heavy & (cloc.fillna(0.0) > 0)
            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc > 0)).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)
    reading_base = ("Situation = volume >= 1.5x the mean of the prior 20 bars of the window and close above the low, "
                    "long side, with the recorded regime used where 20 prior bars are not in the window; ")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the active (non-zero forecast) bars are heavy-volume days (>=1.5x prior "
                           "20-day mean) closing above their low with a long forecast, as the Fidelity's situation "
                           "requires." if n_active > 0 else "The record has no active bar."),
            "reading": reading_base + "agreement is the share of non-zero forecast bars in that situation with a positive forecast.",
        }

    # ---------- 2. criterion ----------
    # normal 5-bar drift per coin over all windows (non-overlapping grid)
    drift = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            cl = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            for p in range(0, len(cl) - H, H):
                if np.isfinite(cl[p]) and np.isfinite(cl[p + H]) and cl[p] != 0:
                    rets.append(cl[p + H] / cl[p] - 1.0)
        drift[coin] = float(np.mean(rets)) if rets else np.nan

    cases = []  # (day, unusual, entry_forecast)
    for coin, wins in bars.items():
        if not np.isfinite(drift.get(coin, np.nan)):
            continue
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            fc = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0).to_numpy(dtype=float)
            cl = pd.to_numeric(d["close"], errors="coerce").to_numpy(dtype=float)
            ts = pd.to_datetime(d["timestamp"], utc=True, errors="coerce")
            n = len(d)
            # bet bars: rise of the long forecast of at least the band from its lowest level since the last bet
            bets = np.zeros(n, dtype=bool)
            ref = 0.0
            for i in range(n):
                f = fc[i]
                if f <= 0:
                    ref = 0.0
                    continue
                if f - ref >= BAND:
                    bets[i] = True
                    ref = f
                else:
                    ref = min(ref, f)
            # one case per 5-bar grid cell: the first bet bar in the cell
            seen = set()
            for i in range(n):
                if not bets[i]:
                    continue
                cell = i // H
                if cell in seen:
                    continue
                seen.add(cell)
                if i + H >= n:
                    continue
                if not (np.isfinite(cl[i]) and np.isfinite(cl[i + H]) and cl[i] != 0):
                    continue
                r = cl[i + H] / cl[i] - 1.0
                u = r - drift[coin]
                day = ts.iloc[i].floor("D") if pd.notna(ts.iloc[i]) else None
                cases.append((day, float(u), float(fc[i])))

    n_cases = len(cases)
    days = sorted({c[0] for c in cases if c[0] is not None})
    n_days = len(days)
    counts = {"cases": int(n_cases), "distinct days": int(n_days)}

    mean_u = None
    t_val = None
    if n_cases > 0:
        u = np.array([c[1] for c in cases])
        mean_u = float(u.mean())
        dev = pd.Series(u - mean_u).groupby(pd.Series([str(c[0]) for c in cases])).sum().to_numpy()
        D = len(dev)
        if D > 1:
            var_mean = (D / (D - 1.0)) * np.sum(dev ** 2) / (n_cases ** 2)
            se = np.sqrt(var_mean)
            t_val = float(mean_u / se) if se > 0 else None

    # supporting check
    sup_val = None
    sup_pass = None
    if n_cases > 1:
        f = np.array([c[2] for c in cases])
        u = np.array([c[1] for c in cases])
        med = np.median(f)
        up = u[f > med]
        lowh = u[f <= med]
        if len(up) > 0 and len(lowh) > 0:
            sup_val = float(up.mean() - lowh.mean())
            sup_pass = bool(sup_val > 0)
        else:
            sup_pass = False

    main = {
        "name": "mean unusual 5-bar move after each case, long, before costs",
        "value": mean_u,
        "statistic": {"name": "t of the mean, cases of one day clustered", "value": t_val} if t_val is not None else None,
        "threshold": "confirm: mean > 0 with t >= 2 (and check passes); reject: mean < 0 with t <= -2",
    }
    support = {"name": "mean unusual move, upper half minus lower half of entry forecast (> 0)",
               "value": sup_val, "passed": sup_pass}

    reading = (reading_base +
               "a case is the first bet bar (long forecast rise >= 2 points from its low since the last bet) in each "
               "5-bar cell of a window's grid; the minimum counts are read as at least 30 cases and at least 20 distinct "
               "days, either short giving not observable; the day-clustered t uses a D/(D-1) factor; the upper half is "
               "forecasts strictly above the median, the lower half the rest.")

    if n_cases < 30 or n_days < 20:
        status = "not observable"
        decided_by = (f"Minimum counts not reached: {n_cases} cases (need 30) on {n_days} distinct days (need 20).")
    elif t_val is None:
        status = "inconclusive"
        decided_by = "The t could not be computed, so neither the confirm nor the reject rule is met."
    elif mean_u > 0 and t_val >= 2:
        if sup_pass:
            status = "confirmed"
            decided_by = "Confirm rule: mean unusual move above 0 with t >= 2 and the upper-minus-lower half check above 0."
        else:
            status = "inconclusive"
            decided_by = "Inconclusive rule: a confirmed main measure with a failed supporting check."
    elif mean_u < 0 and t_val <= -2:
        status = "rejected"
        decided_by = "Reject rule: mean unusual move below 0 with t <= -2."
    else:
        status = "inconclusive"
        decided_by = "Inconclusive rule: the t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": support,
        "counts": counts,
        "decided_by": decided_by,
        "reading": reading,
    }
