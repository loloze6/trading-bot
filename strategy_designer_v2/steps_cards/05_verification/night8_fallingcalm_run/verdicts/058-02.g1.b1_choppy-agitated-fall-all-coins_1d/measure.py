import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    RAW = "debug_info.components.fall_depth.last_history_value"

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            active = f != 0
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce").values
            else:
                raw = np.full(len(df), np.nan)
            if "regime" in df.columns:
                reg = df["regime"].astype(str).values
            else:
                reg = np.array(["unknown"] * len(df))
            in_profile = reg != "chop"
            fall = np.where(np.isnan(raw), False, raw < 0)
            situ = active & in_profile & fall & (f < 0)
            n_active += int(active.sum())
            n_agree += int(situ.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.90)

    main_name = "|forecast|-weighted mean short-direction 5-bar excess return"
    main_thr = "above 0 with day-pooled t >= 2 to confirm; below 0 with t <= -2 to reject"
    sup_name = "mean short-direction excess return, top third minus bottom third of |forecast|"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None,
                             "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": n_active, "cases": None, "distinct days": None},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are short bars "
                           "after a 30-day fall (raw fall_depth < 0) inside the choppy agitated "
                           "profile, so the config does not do what the Fidelity says."),
            "reading": ("The situation is taken as raw fall_depth < 0 on a bar whose regime is "
                        "not 'chop', on the short side; a bar without a recorded raw value "
                        "counts as outside the situation."),
        }

    # ---------- 2. Criterion ----------
    # coin mean 5-bar return over all windows (non-overlapping grid)
    coin_mean = {}
    cases = []  # (day, |f|, x)
    for coin, wins in bars.items():
        all_r = []
        coin_cases = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").values
            f = pd.to_numeric(df["forecast"], errors="coerce").values
            ts = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
            n = len(df)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 <= 0:
                    continue
                r = c1 / c0 - 1.0
                all_r.append(r)
                fi = f[i]
                if np.isfinite(fi) and fi < 0 and not pd.isna(ts.iloc[i]):
                    coin_cases.append((ts.iloc[i].normalize(), abs(float(fi)), r))
        if len(all_r) == 0:
            continue
        m = float(np.mean(all_r))
        coin_mean[coin] = m
        for d, a, r in coin_cases:
            cases.append((d, a, -(r - m)))

    n_cases = len(cases)
    days = [c[0] for c in cases]
    n_days = int(len(set(days)))
    counts = {"cases": n_cases, "distinct days": n_days}

    wmean = None
    t = None
    if n_cases > 0:
        wts = np.array([c[1] for c in cases], dtype=float)
        x = np.array([c[2] for c in cases], dtype=float)
        sw = wts.sum()
        if sw > 0:
            wmean = float((wts * x).sum() / sw)
            dev = pd.Series(wts * (x - wmean)).groupby(pd.Index(days)).sum().values
            D = len(dev)
            if D > 1:
                var = (D / (D - 1.0)) * float((dev ** 2).sum()) / sw ** 2
                se = np.sqrt(var)
                t = float(wmean / se) if se > 0 else None

    sup_val = None
    sup_pass = None
    if n_cases >= 3:
        order = sorted(range(n_cases), key=lambda k: (cases[k][1], k))
        k3 = n_cases // 3
        bottom = [cases[k][2] for k in order[:k3]]
        top = [cases[k][2] for k in order[n_cases - k3:]]
        sup_val = float(np.mean(top) - np.mean(bottom))
        sup_pass = bool(sup_val > 0)

    reading = ("Situation: raw fall_depth < 0 on a non-'chop' regime bar, short side; cases are grid "
               "bars 0,5,10,... of each window with a full 5-bar return inside it; the coin's mean "
               "5-bar return is the mean over the same grid of all its windows; the day-pooled t "
               "uses the weighted mean's deviations (weight x (value - mean)) summed per UTC day "
               "with a D/(D-1) correction; thirds are the floor(n/3) cases with the smallest and "
               "the largest |forecast|, compared by their unweighted means.")

    stat = {"name": "day-pooled t of the weighted mean", "value": t} if t is not None else None
    main = {"name": main_name, "value": wmean, "statistic": stat, "threshold": main_thr}
    sup = {"name": sup_name, "value": sup_val, "passed": sup_pass}
    sc = {"agreement": agreement, "passed": True}

    if n_cases < 50 or n_days < 30:
        return {"status": "not observable", "situation_check": sc, "main_measure": main,
                "supporting_check": sup, "counts": counts,
                "decided_by": ("Minimum count not reached: the plan needs at least 50 cases on at "
                               "least 30 distinct days (got %d cases on %d days)." % (n_cases, n_days)),
                "reading": reading}

    if wmean is None or t is None:
        status = "inconclusive"
        decided = "The day-pooled t could not be computed, so neither the confirm nor the reject rule is met."
    elif wmean > 0 and t >= 2:
        if sup_pass:
            status = "confirmed"
            decided = ("Confirm: the weighted mean short-direction excess return is above 0 with t >= 2 "
                       "and the top-third minus bottom-third difference is above 0.")
        else:
            status = "inconclusive"
            decided = ("Inconclusive: a confirming main measure (above 0, t >= 2) whose supporting "
                       "check (top third minus bottom third above 0) fails.")
    elif wmean < 0 and t <= -2:
        status = "rejected"
        decided = ("Reject: the weighted mean short-direction excess return is below 0 with t <= -2.")
    else:
        status = "inconclusive"
        decided = "Inconclusive: the day-pooled t lies between -2 and 2."

    return {"status": status, "situation_check": sc, "main_measure": main,
            "supporting_check": sup, "counts": counts, "decided_by": decided,
            "reading": reading}
