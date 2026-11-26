import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    BAND = 2.0
    RAW = "debug_info.components.up_streak.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            f = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0).values
            close = pd.to_numeric(d["close"], errors="coerce").values
            up_price = np.zeros(len(d), dtype=bool)
            if len(d) > 1:
                up_price[1:] = close[1:] > close[:-1]
            if RAW in d.columns:
                raw = pd.to_numeric(d[RAW], errors="coerce").values
            else:
                raw = np.full(len(d), np.nan)
            situation = np.where(np.isnan(raw), up_price, raw > 0)
            active = f != 0
            n_active += int(active.sum())
            n_agree += int((active & situation & (f < 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.9

    main_name = "mean unusual 5-bar move after short cases, in the short direction"
    threshold = "confirm if day-pooled t >= 2 with supporting check > 0; reject if t <= -2"
    sup_name = "mean unusual move, upper half minus lower half of |forecast| at case"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "distinct case days": 0},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are up-close-streak bars "
                           "with a short (negative) forecast, as the Fidelity's situation and side require."),
            "reading": "The situation is a positive raw streak ratio (or, where unrecorded, a close above the previous close in the same window), on the short side.",
        }

    # ---------- 2. criterion ----------
    case_u = []
    case_absf = []
    case_day = []
    for coin, wins in bars.items():
        frames = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            frames.append(df.reset_index(drop=True))
        if not frames:
            continue
        # normal drift: mean of non-overlapping 5-bar returns over all windows of the coin
        grid_rets = []
        for d in frames:
            c = pd.to_numeric(d["close"], errors="coerce").values
            for p in range(0, len(d) - H, H):
                if np.isfinite(c[p]) and np.isfinite(c[p + H]) and c[p] > 0:
                    grid_rets.append(c[p + H] / c[p] - 1.0)
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))

        for d in frames:
            f = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0).values
            c = pd.to_numeric(d["close"], errors="coerce").values
            ts = pd.to_datetime(d["timestamp"], utc=True, errors="coerce")
            s = -f  # short strength
            ref = 0.0
            bets = np.zeros(len(d), dtype=bool)
            for i in range(len(d)):
                if s[i] <= 0:
                    ref = 0.0
                    continue
                ref = min(ref, s[i])
                if s[i] - ref >= BAND:
                    bets[i] = True
                    ref = s[i]
            taken = set()
            for i in np.where(bets)[0]:
                cell = i // H
                if cell in taken:
                    continue
                taken.add(cell)
                if i + H >= len(d):
                    continue
                if not (np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] > 0):
                    continue
                r = c[i + H] / c[i] - 1.0
                case_u.append(-(r - drift))
                case_absf.append(abs(f[i]))
                case_day.append(ts.iloc[i].strftime("%Y-%m-%d") if pd.notna(ts.iloc[i]) else str(i))

    u = np.array(case_u, dtype=float)
    absf = np.array(case_absf, dtype=float)
    n_cases = int(len(u))
    n_days = int(len(set(case_day)))

    value = float(np.mean(u)) if n_cases > 0 else None
    t = None
    if n_cases > 1 and n_days > 1:
        dev = pd.Series(u - u.mean()).groupby(pd.Series(case_day)).sum().values
        G = len(dev)
        var = (G / (G - 1)) * np.sum(dev ** 2) / (n_cases ** 2)
        if var > 0:
            t = float(u.mean() / np.sqrt(var))

    sup_val = None
    sup_pass = None
    if n_cases >= 2:
        med = np.median(absf)
        up = u[absf > med]
        lo = u[absf <= med]
        if len(up) > 0 and len(lo) > 0:
            sup_val = float(up.mean() - lo.mean())
            sup_pass = bool(sup_val > 0)

    reading = ("A case is the first short bet (forecast rising toward short by >= 2 points from its lowest short level "
               "since the last bet, from 0 after flat) in each 5-bar grid cell of its window; the day-pooled t uses "
               "per-day summed deviations with a G/(G-1) factor; the median split puts |forecast| above the median "
               "in the upper half and at or below it in the lower half; fewer than 100 case days gives 'not observable'.")

    counts = {"distinct case days": n_days, "cases": n_cases}

    if n_days < 100:
        status = "not observable"
        decided = f"Only {n_days} distinct case days, below the plan's minimum of 100."
    elif t is None:
        status = "inconclusive"
        decided = "The day-pooled t could not be computed."
    elif t >= 2 and sup_pass:
        status = "confirmed"
        decided = "Main-measure t >= 2 and the upper-minus-lower |forecast| half difference is above 0."
    elif t >= 2:
        status = "inconclusive"
        decided = "Main-measure t >= 2 but the supporting check is not positive, which the plan calls inconclusive."
    elif t <= -2:
        status = "rejected"
        decided = "Main-measure t <= -2: the price rose more than its drift after up streaks."
    else:
        status = "inconclusive"
        decided = "Main-measure t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": value,
            "statistic": ({"name": "t of the mean, cases of one day pooled", "value": t} if t is not None else None),
            "threshold": threshold,
        },
        "supporting_check": {"name": sup_name, "value": sup_val, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
