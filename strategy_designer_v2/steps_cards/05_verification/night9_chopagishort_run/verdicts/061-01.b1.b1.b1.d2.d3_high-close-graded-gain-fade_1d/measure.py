import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    BAND = 2.0
    RAW = "debug_info.components.small_gain.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    prepared = {}
    for coin, wins in bars.items():
        prepared[coin] = {}
        for w, df in wins.items():
            d = df.reset_index(drop=True).copy()
            d["timestamp"] = pd.to_datetime(d["timestamp"], utc=True)
            hi = d["high"].astype(float)
            lo = d["low"].astype(float)
            cl = d["close"].astype(float)
            rng = hi - lo
            loc = (cl - lo) / rng.where(rng > 0)
            ret1 = cl / cl.shift(1) - 1.0
            # first bar of a window: the day's return is read from the raw component
            # (raw = ret / mean abs ret - 1, so ret > 0 <=> raw > -1)
            if RAW in d.columns:
                raw = pd.to_numeric(d[RAW], errors="coerce")
                up_raw = raw > -1.0
                up = ret1.gt(0) | (ret1.isna() & up_raw)
            else:
                up = ret1.gt(0)
            # profile: the vetoes send the bar to "chop"; any other regime is in the profile
            reg = d["regime"].astype(str)
            profile = reg.ne("chop")
            situation = profile & loc.ge(0.8) & up
            f = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0)
            active = f.ne(0)
            n_active += int(active.sum())
            n_agree += int((active & situation & f.lt(0)).sum())
            d["_f"] = f
            prepared[coin][w] = d

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)
    situation_check = {"agreement": agreement, "passed": passed}

    main_name = "mean unusual 5-bar move of short bets (short direction), day-pooled t"
    threshold = "confirm: mean > 0 with t >= 2 and supporting check > 0; reject: mean < 0 with t <= -2"

    if n_active == 0:
        return {
            "status": "not observable",
            "situation_check": situation_check,
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"cases on distinct days": 0, "cases": 0},
            "decided_by": "The record holds no active bar, so fewer than 30 cases on distinct days.",
            "reading": "none",
        }

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": situation_check,
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {},
            "decided_by": ("Fewer than 90 % of the active bars are short bars on high-close (close location >= 0.8) "
                           "up days inside the choppy agitated profile, which the plan's Fidelity requires."),
            "reading": "Profile read as the recorded regime not being 'chop' (the vetoes' result).",
        }

    # ---------- 2. criterion ----------
    cases = []  # (day, unusual, absf)
    for coin, wins in prepared.items():
        # normal drift: mean of non-overlapping 5-bar returns over all windows of the coin
        grid_rets = []
        for w, d in wins.items():
            cl = d["close"].astype(float).values
            for i in range(0, len(cl) - H, H):
                if cl[i] > 0 and np.isfinite(cl[i]) and np.isfinite(cl[i + H]):
                    grid_rets.append(cl[i + H] / cl[i] - 1.0)
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))

        for w, d in wins.items():
            f = d["_f"].values
            cl = d["close"].astype(float).values
            ts = d["timestamp"]
            n = len(d)
            # bets on the short side: a rise of the short size of at least BAND
            ref = 0.0
            bet = np.zeros(n, dtype=bool)
            for i in range(n):
                if f[i] >= 0:
                    ref = 0.0
                    continue
                m = -f[i]
                if m - ref >= BAND:
                    bet[i] = True
                    ref = m
                else:
                    ref = min(ref, m)
            # one case per 5-bar grid cell: its first bet
            for start in range(0, n, H):
                idx = np.where(bet[start:start + H])[0]
                if len(idx) == 0:
                    continue
                t = start + int(idx[0])
                if t + H >= n:
                    continue
                if not (np.isfinite(cl[t]) and np.isfinite(cl[t + H]) and cl[t] > 0):
                    continue
                r = cl[t + H] / cl[t] - 1.0
                unusual = -(r - drift)
                cases.append((ts.iloc[t].normalize(), unusual, abs(f[t])))

    n_cases = len(cases)
    days = sorted(set(c[0] for c in cases))
    n_days = len(days)
    counts = {"cases on distinct days": n_days, "cases": n_cases}
    reading = ("Profile read as the recorded regime not being 'chop'; a case is the first short bet in each "
               "5-bar grid cell of a window; the day-pooled t sums deviations per signal day with a G/(G-1) "
               "correction; the larger-short half is |forecast| above the median, the smaller half at or below it; "
               "the plan's 'fewer than 30 cases on distinct days' is applied as the minimum count.")

    if n_days < 30:
        mean_u = float(np.mean([c[1] for c in cases])) if n_cases else None
        return {
            "status": "not observable",
            "situation_check": situation_check,
            "main_measure": {"name": main_name, "value": mean_u, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": counts,
            "decided_by": "Fewer than 30 cases on distinct days, the plan's minimum count.",
            "reading": reading,
        }

    u = np.array([c[1] for c in cases], dtype=float)
    a = np.array([c[2] for c in cases], dtype=float)
    dd = pd.Series([c[0] for c in cases])
    mean_u = float(u.mean())
    dev = pd.Series(u - mean_u)
    S = dev.groupby(dd.values).sum().values
    G = len(S)
    var_mean = (G / (G - 1.0)) * float(np.sum(S ** 2)) / (n_cases ** 2) if G > 1 else np.nan
    se = np.sqrt(var_mean) if np.isfinite(var_mean) else np.nan
    t_stat = float(mean_u / se) if (np.isfinite(se) and se > 0) else None

    med = float(np.median(a))
    big = u[a > med]
    small = u[a <= med]
    if len(big) > 0 and len(small) > 0:
        diff = float(big.mean() - small.mean())
        check_pass = bool(diff > 0)
    else:
        diff = None
        check_pass = None
    supporting = {"name": "mean unusual move, larger-short half minus smaller-short half",
                  "value": diff, "passed": check_pass}

    if t_stat is None:
        status = "inconclusive"
        decided = "The day-pooled t could not be computed, so the result meets neither rule."
    elif mean_u > 0 and t_stat >= 2:
        if check_pass:
            status = "confirmed"
            decided = "Mean unusual move positive with t >= 2 and the supporting check above 0 (confirm rule)."
        else:
            status = "inconclusive"
            decided = "t >= 2 but the supporting check is at 0 or below (or undefined): inconclusive by the plan."
    elif mean_u < 0 and t_stat <= -2:
        status = "rejected"
        decided = "Mean unusual move negative with t <= -2 (reject rule)."
    else:
        status = "inconclusive"
        decided = "t between -2 and 2: inconclusive by the plan."

    return {
        "status": status,
        "situation_check": situation_check,
        "main_measure": {"name": main_name, "value": mean_u,
                         "statistic": {"name": "t of the mean, cases pooled by day", "value": t_stat},
                         "threshold": threshold},
        "supporting_check": supporting,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
