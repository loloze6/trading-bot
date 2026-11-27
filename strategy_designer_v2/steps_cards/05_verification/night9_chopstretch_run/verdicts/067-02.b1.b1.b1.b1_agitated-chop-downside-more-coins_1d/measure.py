import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    BAND = 2.0
    RAW = "debug_info.components.stretch.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            raw = (pd.to_numeric(df[RAW], errors="coerce").values
                   if RAW in df.columns else np.full(len(df), np.nan))
            reg = df["regime"].astype(str).values
            # in profile: the detector did not veto to "chop"; the component is recorded only there
            in_profile = (reg != "chop") & ~np.isnan(raw)
            situation = in_profile & (np.nan_to_num(raw, nan=0.0) < 0)
            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc < 0)).sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = True if agreement is None else bool(agreement >= 0.9)
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on short side": int(n_agree)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are short bars with the close "
                           "below its 20-day average inside the choppy agitated profile, as the Fidelity requires."),
            "reading": "The profile is taken from the record's regime (not 'chop') and the stretch from its raw value.",
        }

    # ---------- 2. criterion ----------
    # normal drift per coin: mean of non-overlapping 5-bar returns over all windows
    drift = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            if df is None or len(df) <= H:
                continue
            c = pd.to_numeric(df["close"], errors="coerce").values
            for p in range(0, len(c) - H, H):
                if np.isfinite(c[p]) and np.isfinite(c[p + H]) and c[p] > 0:
                    rets.append(c[p + H] / c[p] - 1.0)
        drift[coin] = float(np.mean(rets)) if rets else np.nan

    cases = []  # (day, unusual move short, |forecast|)
    for coin, wins in bars.items():
        if not np.isfinite(drift.get(coin, np.nan)):
            continue
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            c = pd.to_numeric(df["close"], errors="coerce").values
            ts = pd.to_datetime(df["timestamp"], utc=True)
            days = ts.dt.strftime("%Y-%m-%d").values
            n = len(df)
            ref = 0.0
            seen_cells = set()
            for t in range(n):
                s = -fc[t] if fc[t] < 0 else 0.0
                bet = False
                if s == 0:
                    ref = 0.0
                else:
                    if s - ref >= BAND:
                        bet = True
                        ref = s
                    else:
                        ref = min(ref, s)
                if not bet:
                    continue
                cell = t // H
                if cell in seen_cells:
                    continue
                seen_cells.add(cell)
                if t + H >= n:
                    continue
                if not (np.isfinite(c[t]) and np.isfinite(c[t + H]) and c[t] > 0):
                    continue
                r = c[t + H] / c[t] - 1.0
                u = -(r - drift[coin])
                cases.append((days[t], float(u), float(abs(fc[t]))))

    n_cases = len(cases)
    n_days = len(set(d for d, _, _ in cases))
    counts = {"cases": int(n_cases), "distinct days": int(n_days)}
    threshold = "confirm: mean > 0 with t >= 2 and supporting check > 0; reject: mean < 0 with t <= -2"
    reading = ("A case is the first short bet (forecast magnitude rising at least 2 points above its lowest level "
               "since the last bet, from 0 after a flat) in each 5-bar grid cell of a window, needing 5 bars after it; "
               "the profile is the record's regime not 'chop'; the halves of |forecast| are its lower and upper n//2 "
               "ranked cases (the middle case dropped when n is odd); the day-clustered t uses the G/(G-1) correction.")

    mean_u = None
    t_stat = None
    if n_cases >= 2:
        u = np.array([x[1] for x in cases])
        mean_u = float(u.mean())
        dev = pd.Series(u - mean_u).groupby([x[0] for x in cases]).sum().values
        G = len(dev)
        if G >= 2:
            se = np.sqrt(np.sum(dev ** 2)) / n_cases * np.sqrt(G / (G - 1.0))
            t_stat = float(mean_u / se) if se > 0 else None
    elif n_cases == 1:
        mean_u = float(cases[0][1])

    sup_val = None
    if n_cases >= 2:
        order = sorted(range(n_cases), key=lambda i: (cases[i][2], i))
        k = n_cases // 2
        small = [cases[i][1] for i in order[:k]]
        large = [cases[i][1] for i in order[n_cases - k:]]
        sup_val = float(np.mean(large) - np.mean(small))
    sup_pass = None if sup_val is None else bool(sup_val > 0)

    main = {
        "name": "mean unusual 5-bar move in the short direction (day-clustered)",
        "value": mean_u,
        "statistic": None if t_stat is None else {"name": "t of the mean, cases of one day taken together", "value": t_stat},
        "threshold": threshold,
    }
    support = {"name": "mean unusual move, larger half of |forecast| minus smaller half",
               "value": sup_val, "passed": sup_pass}
    sc = {"agreement": None if agreement is None else float(agreement), "passed": passed}

    if n_cases < 30 or n_days < 20:
        status = "not observable"
        decided = (f"The plan's minimum counts are not reached ({n_cases} cases, need 30; "
                   f"{n_days} distinct days, need 20).")
    elif t_stat is None:
        status = "inconclusive"
        decided = "The t could not be computed, so neither the confirm nor the reject rule is met."
    elif mean_u > 0 and t_stat >= 2 and sup_pass:
        status = "confirmed"
        decided = "The mean unusual move in the short direction is positive with t >= 2 and the supporting check is above 0."
    elif mean_u > 0 and t_stat >= 2:
        status = "inconclusive"
        decided = "A confirm-level t whose supporting check is not above 0 is inconclusive."
    elif mean_u < 0 and t_stat <= -2:
        status = "rejected"
        decided = "The mean unusual move in the short direction is negative with t <= -2."
    else:
        status = "inconclusive"
        decided = "The t is between -2 and 2."

    return {
        "status": status,
        "situation_check": sc,
        "main_measure": main,
        "supporting_check": support,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
