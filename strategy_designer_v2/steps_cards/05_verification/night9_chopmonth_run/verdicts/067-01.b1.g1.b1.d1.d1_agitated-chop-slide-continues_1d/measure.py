import numpy as np
import pandas as pd


def measure(bars):
    H = 10
    BAND = 2.0
    RAW = "debug_info.components.month_fall.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            fc = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0).values
            close = pd.to_numeric(d["close"], errors="coerce")
            ret30 = (close / close.shift(30) - 1.0).values
            if RAW in d.columns:
                raw = pd.to_numeric(d[RAW], errors="coerce").values
                raw = np.where(np.isnan(raw), ret30, raw)
            else:
                raw = ret30
            reg = d["regime"].astype(str).values if "regime" in d.columns else np.array([""] * len(d))
            active = fc != 0
            in_sit = (reg == "unknown") & (~np.isnan(raw)) & (raw < 0) & (fc < 0)
            n_active += int(active.sum())
            n_agree += int((active & in_sit).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.90)

    main_name = "mean unusual 10-bar move of short bets, before costs, in the short direction"
    thr = "confirm: mean > 0 with day-clustered t >= 2 and supporting check passed; reject: mean < 0 with t <= -2"
    reading = ("The profile is read from the recorded regime ('unknown' = the choppy agitated profile, the only regime "
               "with a strategy) since its 365-bar volatility percentile cannot be rebuilt from the windows, the 30-day "
               "fall from last_history_value (or close/close[-30]-1 where missing); a case is the first short bet in each "
               "10-bar grid cell of a window, the deeper half is |forecast| strictly above the median, the day-clustered "
               "t uses a G/(G-1) correction, and 'fewer than 30 cases on fewer than 20 distinct days' is read as two "
               "minimums (30 cases and 20 distinct days), either one unmet giving 'not observable'.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "cases": None, "distinct days": None},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are short bars inside the choppy "
                           "agitated profile with a negative 30-day return, as the plan's Fidelity requires."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    cases = []  # (coin, day, forward return, |forecast|)
    drift = {}
    for coin, wins in bars.items():
        grid_rets = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").values
            n = len(d)
            for p in range(0, n - H, H):
                if np.isfinite(close[p]) and np.isfinite(close[p + H]) and close[p] > 0:
                    grid_rets.append(close[p + H] / close[p] - 1.0)
        drift[coin] = float(np.mean(grid_rets)) if grid_rets else np.nan

        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            fc = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0).values
            close = pd.to_numeric(d["close"], errors="coerce").values
            ts = pd.to_datetime(d["timestamp"], utc=True)
            n = len(d)
            ref = 0.0
            side = 0
            taken_cells = set()
            for i in range(n):
                f = fc[i]
                s = int(np.sign(f))
                if s != side:
                    ref = 0.0
                    side = s
                bet = False
                if s != 0:
                    m = abs(f)
                    if m - ref >= BAND:
                        bet = True
                        ref = m
                    else:
                        ref = min(ref, m)
                if bet and s < 0:
                    cell = i // H
                    if cell in taken_cells:
                        continue
                    taken_cells.add(cell)
                    if i + H < n and np.isfinite(close[i]) and np.isfinite(close[i + H]) and close[i] > 0:
                        r = close[i + H] / close[i] - 1.0
                        cases.append((coin, ts.iloc[i].strftime("%Y-%m-%d"), r, abs(f)))

    rows = [(c, day, -(r - drift[c]), af) for (c, day, r, af) in cases if np.isfinite(drift.get(c, np.nan))]
    n_cases = len(rows)
    days = sorted(set(r[1] for r in rows))
    n_days = len(days)
    counts = {"cases": int(n_cases), "distinct days": int(n_days)}

    mean_u = None
    t = None
    if n_cases > 0:
        u = np.array([r[2] for r in rows], dtype=float)
        mean_u = float(u.mean())
        dev = u - mean_u
        dser = pd.Series(dev).groupby([r[1] for r in rows]).sum()
        G = len(dser)
        if G > 1:
            var = (G / (G - 1.0)) * float((dser.values ** 2).sum()) / (n_cases ** 2)
            se = np.sqrt(var)
            t = float(mean_u / se) if se > 0 else None

    sup_val = None
    sup_pass = None
    if n_cases >= 2:
        af = np.array([r[3] for r in rows], dtype=float)
        u = np.array([r[2] for r in rows], dtype=float)
        med = float(np.median(af))
        deep = u[af > med]
        shallow = u[af <= med]
        if len(deep) > 0 and len(shallow) > 0:
            sup_val = float(deep.mean() - shallow.mean())
            sup_pass = bool(sup_val > 0)
        else:
            sup_pass = False

    main = {"name": main_name, "value": mean_u,
            "statistic": {"name": "t of the mean, cases of one day taken together", "value": t} if t is not None else None,
            "threshold": thr}
    supporting = {"name": "deeper-fall half minus shallower half, mean unusual move", "value": sup_val, "passed": sup_pass}

    if n_cases < 30 or n_days < 20:
        status = "not observable"
        decided = (f"The plan's minimum of 30 cases on 20 distinct days is not reached "
                   f"({n_cases} cases on {n_days} days).")
    elif t is None or mean_u is None:
        status = "inconclusive"
        decided = "The day-clustered t could not be computed, so neither the confirm nor the reject rule is met."
    elif mean_u > 0 and t >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "The mean unusual move is positive with t >= 2 and the deeper-fall half beats the shallower half."
        else:
            status = "inconclusive"
            decided = "The mean unusual move is positive with t >= 2 but the supporting check fails, which the plan calls inconclusive."
    elif mean_u < 0 and t <= -2:
        status = "rejected"
        decided = "The mean unusual move is negative with t <= -2 (the price rises more than its drift)."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": supporting,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
