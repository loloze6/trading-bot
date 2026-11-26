import numpy as np
import pandas as pd


def measure(bars):
    H = 10
    BAND = 2.0
    MIN_DAYS = 30
    RAW_RISE = "debug_info.components.rise_in_std.last_history_value"

    # ---------------- 1. situation check ----------------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            # fallback from prices: the sign of the 1-bar return (same sign as return / 30-day std)
            prev = np.concatenate([[np.nan], close[:-1]])
            price_ret = close / prev - 1.0
            if RAW_RISE in df.columns:
                raw = pd.to_numeric(df[RAW_RISE], errors="coerce").to_numpy(dtype=float)
                rise_val = np.where(np.isfinite(raw), raw, price_ret)
            else:
                rise_val = price_ret
            active = np.isfinite(fc) & (fc != 0)
            n_active += int(active.sum())
            situ = np.isfinite(rise_val) & (rise_val > 0)
            n_agree += int((active & situ & (fc > 0)).sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = True if agreement is None else bool(agreement >= 0.9)

    main_name = "mean unusual 10-bar move after long bets (forecast rise >= 2), once per 10-bar grid cell"
    threshold = "confirm: mean > 0 with t >= 2 and supporting check passes; reject: mean < 0 with t <= -2"
    sup_name = "mean unusual move above median forecast minus below median"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on long side": int(n_agree)},
            "decided_by": "Fewer than 90% of the bars with a non-zero forecast are rise days "
                          "(1-day vol-scaled return > 0) with a long forecast, as the Fidelity's situation and side require.",
            "reading": "The situation is a rise day (raw rise_in_std > 0, else the 1-bar close return > 0) on the long side.",
        }

    # ---------------- 2. criterion ----------------
    cases = []  # (coin, day, forecast, raw return)
    drift = {}
    for coin, wins in bars.items():
        grid_rets = []
        coin_cases = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            ts = pd.to_datetime(df["timestamp"], utc=True)
            days = ts.dt.floor("D").to_numpy()
            n = len(df)
            # normal drift grid: positions 0, H, 2H, ...
            for p in range(0, n - H, H):
                r = close[p + H] / close[p] - 1.0
                if np.isfinite(r):
                    grid_rets.append(r)
            # bets on the long side
            ref = 0.0
            taken_cells = set()
            for t in range(n):
                f = fc[t]
                if not np.isfinite(f) or f <= 0:
                    ref = 0.0
                    continue
                if f - ref >= BAND:
                    ref = f
                    cell = t // H
                    if cell not in taken_cells:
                        taken_cells.add(cell)
                        if t + H < n:
                            r = close[t + H] / close[t] - 1.0
                            if np.isfinite(r):
                                coin_cases.append((coin, days[t], float(f), float(r)))
                else:
                    ref = min(ref, f)
        drift[coin] = float(np.mean(grid_rets)) if grid_rets else np.nan
        for c in coin_cases:
            if np.isfinite(drift[coin]):
                cases.append((c[0], c[1], c[2], c[3] - drift[coin]))

    n_cases = len(cases)
    case_days = sorted(set(c[1] for c in cases))
    n_days = len(case_days)

    mean_u = None
    t_stat = None
    sup_val = None
    sup_pass = None
    if n_cases > 0:
        x = np.array([c[3] for c in cases], dtype=float)
        f_arr = np.array([c[2] for c in cases], dtype=float)
        d_arr = np.array([c[1] for c in cases])
        mean_u = float(x.mean())
        dev = x - mean_u
        sums = pd.Series(dev).groupby(pd.Series(d_arr)).sum().to_numpy()
        D = len(sums)
        if D > 1:
            var = (D / (D - 1.0)) * float(np.sum(sums ** 2)) / (n_cases ** 2)
            se = np.sqrt(var)
            t_stat = float(mean_u / se) if se > 0 else None
        med = float(np.median(f_arr))
        hi = x[f_arr > med]
        lo = x[f_arr < med]
        if len(hi) > 0 and len(lo) > 0:
            sup_val = float(hi.mean() - lo.mean())
            sup_pass = bool(sup_val > 0)
        else:
            sup_val = None
            sup_pass = False

    if n_days < MIN_DAYS:
        status = "not observable"
        decided = f"Fewer than {MIN_DAYS} distinct case days over all coins and windows ({n_days})."
    elif t_stat is None:
        status = "inconclusive"
        decided = "The t of the mean unusual move could not be computed, so neither confirm nor reject is met."
    elif mean_u > 0 and t_stat >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "The mean unusual move is positive with a t of 2 or more and the supporting check passes."
        else:
            status = "inconclusive"
            decided = "A t of 2 or more with the supporting check failing is inconclusive."
    elif mean_u < 0 and t_stat <= -2:
        status = "rejected"
        decided = "The mean unusual move is negative with a t of -2 or less."
    else:
        status = "inconclusive"
        decided = "The t is between -2 and 2, which is inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": (float(agreement) if agreement is not None else None), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_u,
            "statistic": ({"name": "t of the mean, cases of one day taken together", "value": t_stat}
                          if t_stat is not None else None),
            "threshold": threshold,
        },
        "supporting_check": {"name": sup_name, "value": sup_val, "passed": sup_pass},
        "counts": {"distinct case days": int(n_days), "cases": int(n_cases)},
        "decided_by": decided,
        "reading": ("Bets are tracked per window from 0 at its first bar, the first bet in each 10-bar grid cell "
                    "(counted from the window's first row) is the case and cases without 10 bars ahead in the window "
                    "are dropped, cases equal to the median forecast are left out of both halves, and the day-clustered "
                    "t uses the D/(D-1) correction so it equals the ordinary t with one case per day."),
    }
