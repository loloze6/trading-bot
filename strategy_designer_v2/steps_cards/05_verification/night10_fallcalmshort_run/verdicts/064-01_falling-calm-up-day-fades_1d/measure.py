import numpy as np
import pandas as pd


def measure(bars):
    H = 3
    BAND = 2.0
    RAW = "debug_info.components.scaled_rise.last_history_value"

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
            ret1 = np.full(len(d), np.nan)
            if len(d) > 1:
                ret1[1:] = close[1:] / close[:-1] - 1.0
            if RAW in d.columns:
                raw = pd.to_numeric(d[RAW], errors="coerce").values
            else:
                raw = np.full(len(d), np.nan)
            # sign of the raw value = sign of the day's return; recompute from prices where not recorded
            up = np.where(np.isnan(raw), ret1 > 0, raw > 0)
            calm_fall = (d["regime"].astype(str).values == "unknown")
            active = f != 0
            sit = calm_fall & up & (f < 0)
            n_active += int(active.sum())
            n_agree += int((active & sit).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "mean unusual 3-bar move of short cases (return minus coin's normal 3-bar drift, short direction)"
    thr = "t >= 2 with positive mean confirms; t <= -2 rejects; t clustered by day"
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "distinct case days": 0},
            "decided_by": ("Fewer than 90% of bars with a non-zero forecast are up days inside the falling calm "
                           "regime with a short forecast, as the Fidelity's situation and side require."),
            "reading": "Falling calm is read from the regime column ('unknown' = the profile passed both vetoes); an up day is a positive raw scaled return (or positive daily return where not recorded).",
        }

    # ---------- 2. criterion ----------
    # normal drift per coin: non-overlapping 3-bar returns on each window's grid, all windows together
    drift = {}
    for coin, wins in bars.items():
        rs = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            c = pd.to_numeric(df["close"], errors="coerce").values
            for i in range(0, len(c) - H, H):
                if np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] != 0:
                    rs.append(c[i + H] / c[i] - 1.0)
        drift[coin] = float(np.mean(rs)) if len(rs) else np.nan

    cases = []  # (day, unusual, |forecast|)
    for coin in sorted(bars.keys()):
        wins = bars[coin]
        for w in sorted(wins.keys(), key=lambda x: (len(str(x)), str(x))):
            df = wins[w]
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            f = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0).values
            c = pd.to_numeric(d["close"], errors="coerce").values
            ts = pd.to_datetime(d["timestamp"], utc=True)
            side = 0
            ref = 0.0
            bet = np.zeros(len(d), dtype=bool)
            for i in range(len(d)):
                s = int(np.sign(f[i]))
                if s == 0:
                    side, ref = 0, 0.0
                    continue
                if s != side:
                    side, ref = s, 0.0
                mag = abs(f[i])
                if mag - ref >= BAND - 1e-12:
                    if s < 0:
                        bet[i] = True
                    ref = mag
                else:
                    ref = min(ref, mag)
            for start in range(0, len(d), H):
                idx = [i for i in range(start, min(start + H, len(d))) if bet[i]]
                if not idx:
                    continue
                t = idx[0]
                if t + H >= len(d):
                    continue
                if not (np.isfinite(c[t]) and np.isfinite(c[t + H]) and c[t] != 0):
                    continue
                if not np.isfinite(drift.get(coin, np.nan)):
                    continue
                r = c[t + H] / c[t] - 1.0
                u = -(r - drift[coin])
                cases.append((ts.iloc[t].strftime("%Y-%m-%d"), float(u), float(abs(f[t]))))

    n_cases = len(cases)
    days = sorted(set(x[0] for x in cases))
    n_days = len(days)
    counts = {"distinct case days": int(n_days), "cases": int(n_cases)}

    mean_u = None
    tval = None
    if n_cases > 0:
        u = np.array([x[1] for x in cases])
        mean_u = float(u.mean())
        if n_days > 1:
            dev = pd.Series(u - mean_u).groupby([x[0] for x in cases]).sum().values
            var = (dev ** 2).sum() / (n_cases ** 2) * n_days / (n_days - 1)
            se = np.sqrt(var)
            tval = float(mean_u / se) if se > 0 else None

    sup_val = None
    sup_pass = None
    if n_cases >= 2:
        arr = sorted(cases, key=lambda x: -x[2])
        k = n_cases // 2
        big = np.mean([x[1] for x in arr[:k]])
        small = np.mean([x[1] for x in arr[k:]])
        sup_val = float(big - small)
        sup_pass = bool(sup_val > 0)

    if n_days < 30:
        status = "not observable"
        decided = f"Only {n_days} distinct case days, fewer than the plan's minimum of 30."
    elif tval is None:
        status = "inconclusive"
        decided = "The day-clustered t could not be computed, so neither the confirm nor the reject rule is met."
    elif tval >= 2 and mean_u > 0 and sup_pass:
        status = "confirmed"
        decided = "Main-measure t >= 2 with a positive mean unusual move, and the large-minus-small |forecast| half difference is above 0."
    elif tval <= -2:
        status = "rejected"
        decided = "Main-measure t <= -2: prices rose after the scaled up days relative to drift."
    else:
        status = "inconclusive"
        if tval >= 2:
            decided = "t >= 2 but the size check (large minus small |forecast| half) is not above 0 or the mean is not positive."
        else:
            decided = "The main-measure t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": mean_u,
                         "statistic": ({"name": "t of the mean, cases of one day summed together", "value": tval}
                                       if tval is not None else None),
                         "threshold": thr},
        "supporting_check": {"name": "mean unusual move, larger-|forecast| half minus smaller half",
                             "value": sup_val, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": ("Cases are short bets (forecast rise of >= 2 points on the short side) taken at the first bet bar of each "
                    "3-bar grid cell per window, measured from that bar's close over 3 bars, over all coins in the record; "
                    "the larger half is the top floor(n/2) cases by |forecast|; the plan's fewer-than-30-case-days rule is "
                    "applied as the minimum count giving 'not observable'."),
    }
