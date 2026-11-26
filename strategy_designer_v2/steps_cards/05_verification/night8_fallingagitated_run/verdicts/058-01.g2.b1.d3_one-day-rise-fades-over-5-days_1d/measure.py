import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    BAND = 2.0
    MIN_DAYS = 30
    RAW = "debug_info.components.scaled_rise.last_history_value"

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            fc = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0).values
            close = pd.to_numeric(d["close"], errors="coerce").values
            ret1 = np.full(len(d), np.nan)
            if len(d) > 1:
                ret1[1:] = close[1:] / close[:-1] - 1.0
            if RAW in d.columns:
                raw = pd.to_numeric(d[RAW], errors="coerce").values
            else:
                raw = np.full(len(d), np.nan)
            # Use the raw component value; if it is missing, use the day's return from the prices.
            rise_val = np.where(np.isnan(raw), ret1, raw)
            regime = d["regime"].astype(str).values
            in_profile = regime == "unknown"
            situation = in_profile & (np.nan_to_num(rise_val, nan=0.0) > 0)
            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc < 0)).sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = (agreement is not None) and (agreement >= 0.9)

    main_name = "mean unusual 5-bar move of short bets, in the short direction"
    thr = "confirm: mean > 0 with t >= 2 (and supporting check > 0); reject: mean < 0 with t <= -2"
    sup_name = "mean unusual move, larger-|forecast| half minus smaller half"
    reading = ("Profile read from the recorded regime ('unknown' = falling agitated, the config's only active regime); "
               "a case is the first short bet (forecast magnitude rising >= 2 points from its lowest level since the last bet) "
               "in each 5-bar grid cell of a window, measured from that bet's close over 5 bars within the window; "
               "the larger half is |forecast| strictly above the median; the day-clustered t uses deviations from the mean "
               "summed per UTC day with a D/(D-1) correction; the plan's 'fewer than 30 distinct case days' minimum "
               "is reported as 'not observable'.")

    if n_active == 0:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": {"name": sup_name, "value": None, "passed": None},
            "counts": {"distinct case days": 0, "cases": 0},
            "decided_by": "No active bar in the record: fewer than 30 distinct case days.",
            "reading": reading,
        }

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are positive-return days inside the "
                           "falling agitated profile with a short forecast, as the Fidelity requires."),
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    cases = []  # (day, unusual, absf)
    for coin, wins in bars.items():
        # normal drift for the coin: mean of non-overlapping 5-bar returns over all windows
        grid_rets = []
        prepared = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").values
            n = len(d)
            for p in range(0, n - H, H):
                r = close[p + H] / close[p] - 1.0
                if np.isfinite(r):
                    grid_rets.append(r)
            prepared.append(d)
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))

        for d in prepared:
            close = pd.to_numeric(d["close"], errors="coerce").values
            fc = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0).values
            ts = pd.to_datetime(d["timestamp"], utc=True)
            n = len(d)
            # bets on the short side
            bet = np.zeros(n, dtype=bool)
            ref = 0.0
            prev_short = False
            for i in range(n):
                f = fc[i]
                if f < 0:
                    mag = -f
                    if not prev_short:
                        ref = 0.0
                    if mag - ref >= BAND - 1e-12:
                        bet[i] = True
                        ref = mag
                    else:
                        ref = min(ref, mag)
                    prev_short = True
                else:
                    prev_short = False
                    ref = 0.0
            # one case per grid cell: first bet in the cell
            for start in range(0, n, H):
                idx = np.where(bet[start:start + H])[0]
                if len(idx) == 0:
                    continue
                i = start + int(idx[0])
                if i + H >= n:
                    continue
                r = close[i + H] / close[i] - 1.0
                if not np.isfinite(r):
                    continue
                unusual = -(r - drift)
                cases.append((ts.iloc[i].strftime("%Y-%m-%d"), float(unusual), float(abs(fc[i]))))

    n_cases = len(cases)
    days = sorted(set(c[0] for c in cases))
    n_days = len(days)

    mean_u = None
    t_val = None
    if n_cases > 0:
        x = np.array([c[1] for c in cases])
        mean_u = float(x.mean())
        dev = x - mean_u
        s = pd.Series(dev).groupby([c[0] for c in cases]).sum().values
        D = len(s)
        if D > 1:
            var = (D / (D - 1.0)) * np.sum(s ** 2) / (n_cases ** 2)
            se = float(np.sqrt(var))
            t_val = float(mean_u / se) if se > 0 else None

    sup_val = None
    sup_pass = None
    if n_cases > 0:
        x = np.array([c[1] for c in cases])
        a = np.array([c[2] for c in cases])
        med = np.median(a)
        big = x[a > med]
        small = x[a <= med]
        if len(big) > 0 and len(small) > 0:
            sup_val = float(big.mean() - small.mean())
            sup_pass = bool(sup_val > 0)
        else:
            sup_pass = False

    counts = {"distinct case days": int(n_days), "cases": int(n_cases)}
    stat = {"name": "t of the mean, cases of one day taken together", "value": t_val} if t_val is not None else None

    if n_days < MIN_DAYS:
        status = "not observable"
        decided = f"Fewer than 30 distinct case days ({n_days}): the plan's minimum is not reached."
    elif t_val is None:
        status = "inconclusive"
        decided = "The t could not be computed, so neither the confirm nor the reject rule is met."
    elif mean_u > 0 and t_val >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "The mean unusual move is positive with t >= 2 and the supporting check is positive."
        else:
            status = "inconclusive"
            decided = "Confirm-strength main measure but the supporting check is not positive: inconclusive."
    elif mean_u < 0 and t_val <= -2:
        status = "rejected"
        decided = "The mean unusual move is negative with t <= -2: after a scaled rise the coin rose more than its drift."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2 (or sign and t disagree): inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {"name": main_name, "value": mean_u, "statistic": stat, "threshold": thr},
        "supporting_check": {"name": sup_name, "value": sup_val, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
