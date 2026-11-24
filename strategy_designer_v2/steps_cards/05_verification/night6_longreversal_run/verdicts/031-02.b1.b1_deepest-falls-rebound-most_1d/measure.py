import numpy as np
import pandas as pd


def measure(bars):
    H = 30
    BAND = 2.0
    COMP = "debug_info.components.depth.last_history_value"

    # ---------- 1. Situation check: fall90 <= -1, long side ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0 or "forecast" not in df.columns:
                continue
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            if COMP in df.columns:
                v = pd.to_numeric(df[COMP], errors="coerce").values
            else:
                v = np.full(len(df), np.nan)
            active = f != 0
            n_active += int(active.sum())
            ok = active & np.isfinite(v) & (v <= -1.0) & (f > 0)
            n_agree += int(ok.sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = True if n_active == 0 else (agreement >= 0.9)

    main_name = "mean unusual 30-bar move per bet (return minus coin's normal 30-bar drift, before costs)"
    thr = "mean > 0 with day-clustered t >= 2 confirms (with deeper half > shallower half); mean < 0 with t <= -2 rejects"
    sup_name = "mean unusual move of upper half minus lower half, split at median forecast"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on long side": int(n_agree)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars where the recorded "
                           "90-day return in usual 90-day moves is -1 or lower, so the config does not trade the "
                           "plan's situation on its side."),
            "reading": ("Active bars without a recorded depth value are counted as outside the situation, since "
                        "the 455-bar history it needs is not in the record to recompute it."),
        }

    # ---------- 2. Criterion ----------
    cases = []  # (unusual, forecast, day)
    for coin, wins in bars.items():
        # normal drift: mean 30-bar return on the non-overlapping grid of all windows
        grid_rets = []
        prepared = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.copy()
            d["timestamp"] = pd.to_datetime(d["timestamp"], utc=True)
            d = d.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").values
            n = len(d)
            for p in range(0, n, H):
                if p + H < n and np.isfinite(close[p]) and np.isfinite(close[p + H]) and close[p] > 0:
                    grid_rets.append(close[p + H] / close[p] - 1.0)
            prepared.append(d)
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))

        for d in prepared:
            close = pd.to_numeric(d["close"], errors="coerce").values
            f = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0).values
            n = len(d)
            # bet detection (holding-period definition)
            side = 0
            low = 0.0
            bets = []  # (index, direction)
            for i in range(n):
                fi = f[i]
                s = int(np.sign(fi))
                if s == 0:
                    side = 0
                    low = 0.0
                    continue
                if s != side:
                    side = s
                    low = 0.0
                mag = abs(fi)
                if mag >= low + BAND:
                    bets.append((i, s))
                    low = mag
                else:
                    low = min(low, mag)
            # read once per 30-bar grid cell: first bet in each cell
            seen = set()
            for i, s in bets:
                cell = i // H
                if cell in seen:
                    continue
                seen.add(cell)
                if i + H >= n:
                    continue
                if not (np.isfinite(close[i]) and np.isfinite(close[i + H]) and close[i] > 0):
                    continue
                r = close[i + H] / close[i] - 1.0
                unusual = s * (r - drift)
                cases.append((unusual, float(f[i]), d["timestamp"].iloc[i].normalize()))

    n_cases = len(cases)
    days = sorted(set(c[2] for c in cases))
    n_days = len(days)

    mean_u = None
    t = None
    diff = None
    sup_pass = None
    if n_cases > 0:
        u = np.array([c[0] for c in cases])
        fc = np.array([c[1] for c in cases])
        dd = pd.Series([c[2] for c in cases])
        mean_u = float(u.mean())
        if n_days > 1:
            e = pd.Series(u - mean_u)
            g = e.groupby(dd.values).sum().values
            G = len(g)
            var = (G / (G - 1.0)) * np.sum(g ** 2) / (n_cases ** 2)
            se = np.sqrt(var)
            t = float(mean_u / se) if se > 0 else None
        med = np.median(fc)
        up = u[fc > med]
        lo = u[fc <= med]
        if len(up) > 0 and len(lo) > 0:
            diff = float(up.mean() - lo.mean())
            sup_pass = bool(diff > 0)
        else:
            sup_pass = False

    counts = {"cases": int(n_cases), "distinct days": int(n_days)}

    if n_cases < 30 or n_days < 20:
        status = "not observable"
        decided = (f"The plan's minimum of 30 cases on 20 distinct days is not reached "
                   f"({n_cases} cases on {n_days} days).")
    elif t is None:
        status = "inconclusive"
        decided = "The clustered t could not be computed, so neither the confirm nor the reject rule is met."
    elif mean_u > 0 and t >= 2:
        if sup_pass:
            status = "confirmed"
            decided = ("The mean unusual move is positive with t >= 2 and the deeper half's mean unusual move "
                       "exceeds the shallower half's.")
        else:
            status = "inconclusive"
            decided = "The mean unusual move is positive with t >= 2 but the depth check fails."
    elif mean_u < 0 and t <= -2:
        status = "rejected"
        decided = ("The mean unusual move is negative with t <= -2: the falls keep falling relative to "
                   "holding the coin.")
    else:
        status = "inconclusive"
        decided = "The day-clustered t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": (float(agreement) if agreement is not None else None),
                            "passed": bool(passed)},
        "main_measure": {"name": main_name, "value": mean_u,
                         "statistic": ({"name": "t of the mean, clustered by day", "value": t}
                                       if t is not None else None),
                         "threshold": thr},
        "supporting_check": {"name": sup_name, "value": diff, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": ("A case is the first bet (forecast rise of at least 2 points from its low since the last bet, "
                    "from 0 at each window start) in each 30-bar grid cell from the window's first row, with its "
                    "30-bar forward return inside the window; the upper half is forecasts strictly above the median "
                    "and the lower half the rest; the clustered t uses the G/(G-1) small-sample factor; fewer than "
                    "the minimum cases is reported as not observable.")
    }
