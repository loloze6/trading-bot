import numpy as np
import pandas as pd


def measure(bars):
    H = 20
    BAND = 2.0
    RAW = "debug_info.components.fall30.last_history_value"

    def _ts(df):
        return pd.to_datetime(df["timestamp"], utc=True, errors="coerce")

    # ---------------- 1. situation check ----------------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            close = pd.to_numeric(df["close"], errors="coerce")
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            # where the component is not recorded, recompute the 30-bar return from prices (same window only)
            recomputed = (close / close.shift(30) - 1.0) * 100.0
            raw = raw.where(raw.notna(), recomputed).values
            active = fc != 0
            situ = (raw < 0) & (fc < 0)
            n_active += int(active.sum())
            n_agree += int((active & situ).sum())

    if n_active == 0:
        agreement = None
    else:
        agreement = n_agree / n_active

    main_name = "mean unusual 20-bar move of short cases, before costs"
    threshold = "confirm: mean > 0 with t >= 2 and depth check passes; reject: mean < 0 with t <= -2"
    sup_name = "deepest third by |forecast| has a higher mean unusual move than shallowest third"
    reading = ("Situation = recorded fall30 raw value (30-bar return, recomputed from closes where missing) below 0 "
               "with a negative forecast; a case is the first bet (short-side forecast deepening by >= 2 points from its "
               "lowest depth since the last bet, reset at flat) in each 20-bar grid cell of each window, dropped if its "
               "20-bar return leaves the window; drift = mean of a coin's non-overlapping 20-bar returns over all its "
               "windows; t uses a day-clustered standard error with D/(D-1) correction; thirds split by rank of |forecast|; "
               "the plan's 'fewer than 30 cases or 30 distinct days' is applied as 'not observable'.")

    if agreement is not None and agreement < 0.9:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"cases": 0, "distinct days": 0},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are short bars with a negative "
                           "30-bar return, as the plan's situation requires."),
            "reading": reading,
        }

    # ---------------- 2. criterion ----------------
    cases = []  # (coin, day, unusual move, |forecast|)
    for coin, wins in bars.items():
        # normal drift of the coin: non-overlapping 20-bar returns over all its windows
        grid_rets = []
        per_window = []
        for w in sorted(wins.keys(), key=lambda s: (len(str(s)), str(s))):
            df = wins[w]
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            n = len(df)
            for p in range(0, n - H, H):
                r = close[p + H] / close[p] - 1.0
                if np.isfinite(r):
                    grid_rets.append(r)
            per_window.append(df)
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))

        for df in per_window:
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            ts = _ts(df)
            n = len(df)
            ref = 0.0
            bet_bars = []
            for i in range(n):
                f = fc[i]
                if f >= 0:
                    ref = 0.0
                    continue
                d = -f
                if d - ref >= BAND - 1e-12:
                    bet_bars.append(i)
                    ref = d
                else:
                    ref = min(ref, d)
            seen_cells = set()
            for i in bet_bars:
                cell = i // H
                if cell in seen_cells:
                    continue
                seen_cells.add(cell)
                if i + H >= n:
                    continue
                r = close[i + H] / close[i] - 1.0
                if not np.isfinite(r):
                    continue
                unusual = -(r - drift)  # short direction
                day = ts.iloc[i]
                day = day.strftime("%Y-%m-%d") if pd.notna(day) else str(i)
                cases.append((coin, day, float(unusual), float(abs(fc[i]))))

    n_cases = len(cases)
    days = sorted(set(c[1] for c in cases))
    n_days = len(days)
    counts = {"cases": int(n_cases), "distinct days": int(n_days)}
    sit = {"agreement": None if agreement is None else float(agreement),
           "passed": True if agreement is not None else None}

    mean_val = float(np.mean([c[2] for c in cases])) if n_cases > 0 else None

    t_val = None
    if n_cases > 1 and n_days > 1:
        x = np.array([c[2] for c in cases])
        m = x.mean()
        dev = pd.Series(x - m).groupby([c[1] for c in cases]).sum().values
        D = len(dev)
        var_m = (dev ** 2).sum() / (n_cases ** 2) * (D / (D - 1.0))
        se = np.sqrt(var_m)
        t_val = float(m / se) if se > 0 else None

    sup_val = None
    sup_pass = None
    if n_cases >= 3:
        order = sorted(range(n_cases), key=lambda k: (cases[k][3], cases[k][0], cases[k][1]))
        parts = np.array_split(np.array(order), 3)
        shallow = np.mean([cases[k][2] for k in parts[0]])
        deep = np.mean([cases[k][2] for k in parts[2]])
        sup_val = float(deep - shallow)
        sup_pass = bool(deep > shallow)

    main = {"name": main_name, "value": mean_val,
            "statistic": None if t_val is None else {"name": "t of the mean, cases summed per day", "value": t_val},
            "threshold": threshold}
    sup = {"name": sup_name, "value": sup_val, "passed": sup_pass}

    if n_cases < 30 or n_days < 30:
        status = "not observable"
        decided = (f"The plan's minimum of 30 cases and 30 distinct days is not reached "
                   f"({n_cases} cases, {n_days} days).")
    elif t_val is None:
        status = "inconclusive"
        decided = "The t could not be computed (zero standard error), so neither confirm nor reject is met."
    elif mean_val > 0 and t_val >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "The mean unusual move is positive with t >= 2 and the deepest third beats the shallowest third."
        else:
            status = "inconclusive"
            decided = "The mean unusual move is positive with t >= 2 but the depth check fails, which the plan calls inconclusive."
    elif mean_val < 0 and t_val <= -2:
        status = "rejected"
        decided = "The mean unusual move is negative with t <= -2 (the coin rises more than its drift after the slide)."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2 (or its sign disagrees with the mean), which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": sit,
        "main_measure": main,
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
