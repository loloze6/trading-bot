import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    BAND = 2.0
    MIN_CASES = 30
    MIN_DAYS = 30

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            c = d["close"].astype(float)
            hi = d["high"].astype(float)
            lo = d["low"].astype(float)
            fc = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0)
            up = (c / c.shift(1) - 1.0) > 0
            prior_fall = c.shift(1) < c.shift(4)
            rng = hi - lo
            loc = (c - lo) / rng.where(rng > 0)
            top_q = loc >= 0.75
            computable = c.shift(4).notna() & loc.notna()
            situ = up & prior_fall & top_q
            active = (fc != 0) & computable
            n_active += int(active.sum())
            n_agree += int((active & situ & (fc < 0)).sum())
    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.90)

    main_name = "mean short-direction 5-bar excess return over drift per case"
    threshold = "confirm: mean > 0 with t >= 2 over >= 30 cases (and supporting check); reject: t <= -2 over >= 30 cases"
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "agreeing bars": int(n_agree)},
            "decided_by": "Fewer than 90% of the bars with a non-zero forecast are short bars of the plan's situation "
                          "(up day, close[t-1] below close[t-4], close in the top quarter of the range).",
            "reading": "The situation is rebuilt from prices with its three stated conditions; bars without four prior "
                       "bars in the window or with a zero range are left out of the check.",
        }

    # ---------- 2. criterion ----------
    # normal 5-bar drift per coin: non-overlapping grid returns over all its windows
    drift = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            c = df["close"].astype(float).to_numpy()
            for p in range(0, len(c) - H, H):
                if np.isfinite(c[p]) and np.isfinite(c[p + H]) and c[p] > 0:
                    rets.append(c[p + H] / c[p] - 1.0)
        drift[coin] = float(np.mean(rets)) if rets else np.nan

    cases = []  # (excess_short, size, day)
    for coin, wins in bars.items():
        if not np.isfinite(drift.get(coin, np.nan)):
            continue
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            c = d["close"].astype(float).to_numpy()
            fc = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0).to_numpy()
            ts = pd.to_datetime(d["timestamp"], utc=True)
            days = ts.dt.floor("D").astype(str).to_numpy()
            ref = 0.0
            seen_cells = set()
            for i in range(len(d)):
                f = fc[i]
                if f >= 0:
                    ref = 0.0
                    continue
                depth = -f
                if depth - ref >= BAND:
                    ref = depth
                    cell = i // H
                    if cell in seen_cells:
                        continue
                    seen_cells.add(cell)
                    if i + H < len(d) and np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] > 0:
                        r = c[i + H] / c[i] - 1.0
                        cases.append((-(r - drift[coin]), depth, days[i]))
                else:
                    ref = min(ref, depth)

    n = len(cases)
    n_days = len(set(x[2] for x in cases))
    counts = {"cases": int(n), "distinct days": int(n_days)}

    mean = None
    tval = None
    if n > 0:
        x = np.array([a[0] for a in cases], dtype=float)
        mean = float(x.mean())
        dev = pd.Series(x - mean).groupby([a[2] for a in cases]).sum().to_numpy()
        G = len(dev)
        if G > 1:
            var = (G / (G - 1.0)) * float(np.sum(dev ** 2)) / (n ** 2)
            se = np.sqrt(var)
            tval = float(mean / se) if se > 0 else None

    sup_val = None
    sup_pass = None
    if n >= 2:
        order = sorted(range(n), key=lambda k: (cases[k][1], k))
        h = n // 2
        small = [cases[k][0] for k in order[:h]]
        large = [cases[k][0] for k in order[n - h:]]
        sup_val = float(np.mean(large) - np.mean(small))
        sup_pass = bool(sup_val >= 0)

    reading = ("A case is the first short bet (forecast deepening by >= 2 points from its shallowest short level since "
               "the last bet, reset at flat) in each 5-bar grid cell of a window with 5 bars ahead in that window; "
               "the minimum requires both 30 cases and 30 distinct days; the halves are by |forecast| on the case bar, "
               "the middle case dropped when the count is odd; the day-clustered t uses a G/(G-1) correction.")

    stat = {"name": "t of the mean, cases of one day summed", "value": tval} if tval is not None else None
    main = {"name": main_name, "value": mean, "statistic": stat, "threshold": threshold}
    support = {"name": "larger-half minus smaller-half mean excess (by forecast size)",
               "value": sup_val, "passed": sup_pass}

    if n < MIN_CASES or n_days < MIN_DAYS:
        status = "not observable"
        decided = "Fewer than 30 cases or fewer than 30 distinct days: the plan's minimum count is not reached."
    elif tval is None:
        status = "inconclusive"
        decided = "The t could not be computed, so neither the confirm nor the reject rule is met."
    elif mean > 0 and tval >= 2 and sup_pass:
        status = "confirmed"
        decided = "Mean short-direction excess return above 0 with t >= 2 over at least 30 cases, and the supporting check passes."
    elif tval <= -2:
        status = "rejected"
        decided = "The mean short-direction excess return has t <= -2 over at least 30 cases."
    elif tval >= 2:
        status = "inconclusive"
        decided = "The t is at least 2 but the supporting check fails."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": main,
        "supporting_check": support,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
