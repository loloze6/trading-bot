import numpy as np
import pandas as pd


def measure(bars):
    import json

    H = 3
    BAND = 2.0
    MIN_DAYS = 30

    def comp(df, cid, field="last_history_value"):
        col = "debug_info.components.%s.%s" % (cid, field)
        if col in df.columns:
            return pd.to_numeric(df[col], errors="coerce").reset_index(drop=True)
        out = np.full(len(df), np.nan)
        if "debug_info.components" in df.columns:
            vals = df["debug_info.components"].tolist()
            for i, v in enumerate(vals):
                d = v
                if isinstance(d, str):
                    try:
                        d = json.loads(d)
                    except Exception:
                        d = None
                if isinstance(d, dict):
                    c = d.get(cid)
                    if isinstance(c, dict):
                        x = c.get(field)
                        try:
                            out[i] = float(x) if x is not None else np.nan
                        except Exception:
                            out[i] = np.nan
        return pd.Series(out)

    def recompute_brk(close):
        prior_low = close.shift(1).rolling(30, min_periods=30).min()
        return (close / prior_low - 1.0) * 100.0

    def bets(fc):
        # A bet: a rise of the forecast on its own side of at least BAND,
        # from its lowest level on that side since the last bet (from 0 after flat or side change).
        res = np.zeros(len(fc), dtype=int)
        side, base = 0, 0.0
        for i, f in enumerate(fc):
            if not np.isfinite(f) or f == 0:
                side, base = 0, 0.0
                continue
            s = 1 if f > 0 else -1
            a = abs(f)
            if s != side:
                side, base = s, 0.0
            else:
                base = min(base, a)
            if a - base >= BAND - 1e-12:
                res[i] = s
                base = a
        return res

    # ---------- situation check and case collection ----------
    n_active = 0
    n_agree = 0
    cases = []  # (coin, day, ret, sign, depth)
    drift = {}

    for coin, wins in bars.items():
        grid_rets = []
        for w, df0 in wins.items():
            df = df0.reset_index(drop=True)
            if len(df) == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            regime = df["regime"].astype(str).str.lower().values
            depth = comp(df, "depth")
            brk = depth.copy()
            rec = recompute_brk(close)
            brk = brk.where(brk.notna(), rec)
            ts = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
            days = ts.dt.floor("D")

            n = len(df)
            # normal drift grid
            for p in range(0, n - H, H):
                c0, c1 = close.iloc[p], close.iloc[p + H]
                if np.isfinite(c0) and np.isfinite(c1) and c0 > 0:
                    grid_rets.append(c1 / c0 - 1.0)

            # situation check
            for i in range(n):
                if fc[i] != 0:
                    n_active += 1
                    b = brk.iloc[i]
                    in_sit = np.isfinite(b) and b < 0 and regime[i] != "chop"
                    if in_sit and fc[i] > 0:
                        n_agree += 1

            # cases: first bet in each 3-bar grid cell
            bt = bets(fc)
            for cs in range(0, n, H):
                for i in range(cs, min(cs + H, n)):
                    if bt[i] != 0:
                        if i + H < n:
                            c0, c1 = close.iloc[i], close.iloc[i + H]
                            if np.isfinite(c0) and np.isfinite(c1) and c0 > 0:
                                cases.append((coin, days.iloc[i], c1 / c0 - 1.0,
                                              int(bt[i]), float(depth.iloc[i])))
                        break
        drift[coin] = float(np.mean(grid_rets)) if grid_rets else np.nan

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = True if agreement is None else bool(agreement >= 0.9)

    reading = ("The falling agitated profile is read from the recorded regime (not 'chop', since the detector's "
               "trend and volatility components are not recorded and need more history than a window holds), the "
               "break from depth.last_history_value or, where missing, recomputed from the window's prior 30 closes; "
               "a case is the first bet in each 3-bar grid cell from the window's first row, its unusual move is a "
               "fraction (not percent), the t is clustered by UTC day with a D/(D-1) correction, and the median "
               "split puts cases strictly below the median depth in the deeper half and the rest in the shallower.")

    main_name = "mean unusual 3-day move of the cases (long side), before costs"
    threshold = "confirm: mean > 0 with t >= 2 and deeper half beats shallower; reject: mean < 0 with t <= -2"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "agreeing bars": int(n_agree)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars of a close below the "
                           "prior 30-day closing low inside the falling agitated profile, as the Fidelity states."),
            "reading": reading,
        }

    # ---------- main measure ----------
    u, dlist, dep = [], [], []
    for coin, day, r, s, d in cases:
        dr = drift.get(coin, np.nan)
        if not np.isfinite(dr):
            continue
        u.append(s * (r - dr))
        dlist.append(day)
        dep.append(d)
    u = np.array(u, dtype=float)
    dep = np.array(dep, dtype=float)
    n_cases = int(len(u))
    n_days = int(len(set(dlist))) if n_cases else 0

    mean_u = float(np.mean(u)) if n_cases else None
    t_val = None
    if n_cases >= 2 and n_days >= 2:
        dev = pd.Series(u - mean_u).groupby(pd.Series(dlist)).sum().values
        D = len(dev)
        se = np.sqrt(D / (D - 1.0) * np.sum(dev ** 2)) / n_cases
        if se > 0:
            t_val = float(mean_u / se)

    # ---------- supporting check ----------
    sup_val, sup_pass = None, None
    m = np.isfinite(dep)
    if m.sum() >= 2:
        med = np.median(dep[m])
        deeper = u[m][dep[m] < med]
        shallow = u[m][dep[m] >= med]
        if len(deeper) > 0 and len(shallow) > 0:
            sup_val = float(np.mean(deeper) - np.mean(shallow))
            sup_pass = bool(sup_val > 0)

    counts = {"distinct case days": n_days, "cases": n_cases}

    if n_days < MIN_DAYS:
        status = "not observable"
        decided = "Fewer than 30 distinct case days across coins and windows (%d)." % n_days
    elif t_val is None:
        status = "inconclusive"
        decided = "The t of the mean unusual move could not be computed, so neither rule is met."
    elif mean_u > 0 and t_val >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "Mean unusual move above 0 with t >= 2 and the deeper half beats the shallower half."
        else:
            status = "inconclusive"
            decided = "t >= 2 but the deeper half does not beat the shallower half."
    elif mean_u < 0 and t_val <= -2:
        status = "rejected"
        decided = "Mean unusual move below 0 with t <= -2: the coin keeps falling after the break."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": passed},
        "main_measure": {"name": main_name,
                         "value": mean_u,
                         "statistic": None if t_val is None else {"name": "t of the mean, cases pooled by day",
                                                                  "value": t_val},
                         "threshold": threshold},
        "supporting_check": {"name": "mean unusual move, deeper half minus shallower half (median depth split)",
                             "value": sup_val, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
