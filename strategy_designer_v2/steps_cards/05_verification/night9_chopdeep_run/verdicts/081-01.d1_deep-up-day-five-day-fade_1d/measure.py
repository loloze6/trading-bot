import numpy as np
import pandas as pd

H = 5
BAND = 2.0
DEPTH_COL = "debug_info.components.depth.last_history_value"


def _bet_flags(fc):
    """Short bets: a rise of the short forecast's size of at least BAND above its lowest
    size since the last bet (from 0 after a flat or a change of side)."""
    flags = np.zeros(len(fc), dtype=bool)
    ref = 0.0
    prev_side = 0
    for i, f in enumerate(fc):
        if not np.isfinite(f) or f == 0:
            ref = 0.0
            prev_side = 0
            continue
        side = 1 if f > 0 else -1
        if side != prev_side:
            ref = 0.0
        prev_side = side
        if side < 0:
            lvl = -f
            if lvl - ref >= BAND:
                flags[i] = True
                ref = lvl
            else:
                ref = min(ref, lvl)
        else:
            ref = 0.0
    return flags


def measure(bars):
    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin in sorted(bars):
        for w in sorted(bars[coin]):
            df = bars[coin][w].reset_index(drop=True)
            if len(df) == 0:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            close = pd.to_numeric(df["close"], errors="coerce").values
            ret1 = np.full(len(df), np.nan)
            ret1[1:] = close[1:] / close[:-1] - 1.0
            up = ret1 > 0
            # first bar of a window: no previous close inside the window, use the detector's regime
            if "regime" in df.columns:
                up[0] = str(df["regime"].iloc[0]) == "mean_reversion"
            if DEPTH_COL in df.columns:
                depth = pd.to_numeric(df[DEPTH_COL], errors="coerce").values
            else:
                depth = np.full(len(df), np.nan)
            below_high = depth < 0
            situation = up & below_high
            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc < 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.9

    main_name = "mean unusual 5-day move of the short bets, short direction"
    threshold = "confirm: mean > 0 with t >= 2 and the check passes; reject: mean < 0 with t <= -2"
    reading = ("Ret1 is recomputed from closes inside each window (the detector's regime is used on a window's first bar) "
               "and 'below the 20-day high' is a raw depth below 0; a case is the first short bet of each 5-bar grid cell "
               "(positions 0,5,10,... of each window) with a 5-bar return inside the window, the coin's drift is the mean of "
               "its 5-bar grid returns over all its windows, the t clusters cases by UTC day (deviations summed per day, "
               "G/(G-1) correction), and the deeper half is the cases with |forecast| above the median, the shallower half "
               "those at or below it.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"cases": None, "distinct days": None},
            "decided_by": ("Fewer than 90% of the active bars are up-close days below the 20-day high with a short "
                           "forecast (agreement %.3f over %d active bars)." % (agreement, n_active)),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin in sorted(bars):
        grid_rets = []
        coin_cases = []
        for w in sorted(bars[coin]):
            df = bars[coin][w].reset_index(drop=True)
            n = len(df)
            if n == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            ts = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
            # coin drift grid
            for p in range(0, n - H, H):
                r = close[p + H] / close[p] - 1.0
                if np.isfinite(r):
                    grid_rets.append(r)
            bets = _bet_flags(fc)
            seen = set()
            for i in np.where(bets)[0]:
                cell = i // H
                if cell in seen:
                    continue
                seen.add(cell)
                if i + H >= n:
                    continue
                r = close[i + H] / close[i] - 1.0
                if not np.isfinite(r) or pd.isna(ts.iloc[i]):
                    continue
                coin_cases.append((r, abs(fc[i]), ts.iloc[i].strftime("%Y-%m-%d")))
        if not coin_cases:
            continue
        drift = float(np.mean(grid_rets)) if grid_rets else np.nan
        if not np.isfinite(drift):
            continue
        for r, af, day in coin_cases:
            rows.append({"unusual": -(r - drift), "absf": af, "day": day})

    n_cases = len(rows)
    cdf = pd.DataFrame(rows, columns=["unusual", "absf", "day"])
    n_days = int(cdf["day"].nunique()) if n_cases else 0
    counts = {"cases": int(n_cases), "distinct days": n_days}

    mean = float(cdf["unusual"].mean()) if n_cases else None
    t = None
    if n_cases >= 2 and n_days >= 2:
        dev = cdf["unusual"] - cdf["unusual"].mean()
        s = dev.groupby(cdf["day"]).sum().values
        G = len(s)
        var = (G / (G - 1.0)) * float(np.sum(s ** 2)) / (n_cases ** 2)
        se = np.sqrt(var)
        t = float(mean / se) if se > 0 else None

    sup_val = None
    sup_pass = None
    if n_cases >= 2:
        med = float(cdf["absf"].median())
        deep = cdf.loc[cdf["absf"] > med, "unusual"]
        shallow = cdf.loc[cdf["absf"] <= med, "unusual"]
        if len(deep) > 0 and len(shallow) > 0:
            sup_val = float(deep.mean() - shallow.mean())
            sup_pass = bool(sup_val > 0)
        else:
            sup_pass = False

    main = {"name": main_name, "value": mean,
            "statistic": ({"name": "t of the mean, cases clustered by day", "value": t} if t is not None else None),
            "threshold": threshold}
    support = {"name": "deeper-half minus shallower-half mean unusual move (median |forecast| split)",
               "value": sup_val, "passed": sup_pass}

    if n_cases < 100 or n_days < 50:
        status = "not observable"
        decided = "Minimum counts not reached: %d cases (need 100) and %d distinct days (need 50)." % (n_cases, n_days)
    elif t is None:
        status = "inconclusive"
        decided = "The t could not be computed, so the result meets neither the confirm nor the reject rule."
    elif mean > 0 and t >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "The mean unusual move is positive with t >= 2 and the deeper half beats the shallower half."
        else:
            status = "inconclusive"
            decided = "A confirming t >= 2 with a failed supporting check is inconclusive."
    elif mean < 0 and t <= -2:
        status = "rejected"
        decided = "The mean unusual move is negative with t <= -2: deep up days rise more than the coin's drift."
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
