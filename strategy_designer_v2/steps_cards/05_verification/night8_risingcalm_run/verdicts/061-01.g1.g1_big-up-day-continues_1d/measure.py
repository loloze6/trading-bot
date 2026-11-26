import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    BAND = 2.0
    RAW = "debug_info.components.day_move_swing.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            close = pd.to_numeric(df["close"], errors="coerce")
            day_ret = close / close.shift(1) - 1.0  # inside the window only
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
                raw = raw.where(raw.notna(), day_ret)  # fall back to the price when not recorded
            else:
                raw = day_ret
            active = fc.notna() & (fc != 0) & raw.notna()
            situation = raw > 0          # a one-day rise (graded); zero on down days
            agree = active & situation & (fc > 0)  # expected side: long
            n_active += int(active.sum())
            n_agree += int(agree.sum())

    if n_active == 0:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None, "passed": False},
            "main_measure": {"name": "mean unusual 5-bar move after a case", "value": None,
                             "statistic": None,
                             "threshold": "confirm: mean > 0 with t >= 2; reject: mean < 0 with t <= -2"},
            "supporting_check": None,
            "counts": {"cases": 0},
            "decided_by": "No bar has a non-zero forecast, so no case can be observed.",
            "reading": "none",
        }

    agreement = n_agree / n_active
    if agreement < 0.9:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active_bars": n_active},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are up days "
                           "(raw day-return in swing units > 0) with a long forecast, as the Fidelity's situation requires."),
            "reading": "none",
        }

    # ---------- 2. criterion ----------
    cases = []  # (coin, day, return, forecast)
    for coin, wins in bars.items():
        # normal drift: mean 5-bar return on the non-overlapping grid of all windows of the coin
        grid_rets = []
        coin_cases = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            close = pd.to_numeric(df["close"], errors="coerce").values
            ts = pd.to_datetime(df["timestamp"], utc=True)
            n = len(df)
            for p in range(0, n - H, H):
                if np.isfinite(close[p]) and np.isfinite(close[p + H]) and close[p] != 0:
                    grid_rets.append(close[p + H] / close[p] - 1.0)
            # bets: long-side rises of the forecast of at least the band
            base = 0.0
            bet = np.zeros(n, dtype=bool)
            for i in range(n):
                f = fc[i]
                if f <= 0:
                    base = 0.0
                    continue
                if f - base >= BAND:
                    bet[i] = True
                    base = f
                else:
                    base = min(base, f)
            # once per 5-bar grid cell: the first bet in the cell
            for start in range(0, n, H):
                idx = [i for i in range(start, min(start + H, n)) if bet[i]]
                if not idx:
                    continue
                i = idx[0]
                if i + H >= n:
                    continue
                if not (np.isfinite(close[i]) and np.isfinite(close[i + H])) or close[i] == 0:
                    continue
                r = close[i + H] / close[i] - 1.0
                coin_cases.append((coin, ts.iloc[i].date(), r, float(fc[i])))
        if not grid_rets:
            continue
        drift = float(np.mean(grid_rets))
        for c, d, r, f in coin_cases:
            cases.append((c, d, r - drift, f))

    n_cases = len(cases)
    n_days = len(set(c[1] for c in cases))
    counts = {"cases": n_cases, "days": n_days}
    threshold = "confirm: mean > 0 with t >= 2 and supporting check passes; reject: mean < 0 with t <= -2; fewer than 100 cases: not decided"
    reading = ("A case is the first long-side bet (forecast rise of >= 2 points from its lowest level since the last bet, reset at 0) "
               "in each 5-bar grid cell of a window, its return taken from that bar's close; the median split puts forecasts "
               "above the median in the upper half and the rest in the lower half; the day-pooled t uses the clustered "
               "standard error with a D/(D-1) correction; fewer than 100 cases is reported as not observable.")

    if n_cases == 0:
        return {
            "status": "not observable",
            "situation_check": {"agreement": float(agreement), "passed": True},
            "main_measure": {"name": "mean unusual 5-bar move after a case", "value": None,
                             "statistic": None, "threshold": threshold},
            "supporting_check": {"name": "upper-half minus lower-half mean unusual move (median forecast split)",
                                 "value": None, "passed": None},
            "counts": counts,
            "decided_by": "The plan's minimum of 100 cases is not reached (0 cases).",
            "reading": reading,
        }

    u = np.array([c[2] for c in cases], dtype=float)
    f = np.array([c[3] for c in cases], dtype=float)
    days = [c[1] for c in cases]
    m = float(u.mean())
    dev = pd.Series(u - m).groupby(pd.Series(days)).sum().values
    D = len(dev)
    t = None
    if D > 1:
        se = np.sqrt(np.sum(dev ** 2) * D / (D - 1)) / n_cases
        if se > 0:
            t = float(m / se)

    med = float(np.median(f))
    up = u[f > med]
    lo = u[f <= med]
    if len(up) > 0 and len(lo) > 0:
        diff = float(up.mean() - lo.mean())
        sup_pass = bool(diff > 0)
    else:
        diff = None
        sup_pass = False

    main = {"name": "mean unusual 5-bar move after a case",
            "value": m,
            "statistic": {"name": "t of the mean, same-day cases pooled", "value": t} if t is not None else None,
            "threshold": threshold}
    sup = {"name": "upper-half minus lower-half mean unusual move (median forecast split)",
           "value": diff, "passed": sup_pass}

    if n_cases < 100:
        status = "not observable"
        decided = f"The plan's minimum of 100 cases is not reached ({n_cases} cases)."
    elif t is not None and m > 0 and t >= 2 and sup_pass:
        status = "confirmed"
        decided = "The mean unusual move is above 0 with t >= 2 and the upper half beats the lower half (confirm rule)."
    elif t is not None and m < 0 and t <= -2:
        status = "rejected"
        decided = "The mean unusual move is below 0 with t <= -2 (reject rule)."
    elif t is not None and t >= 2 and not sup_pass:
        status = "inconclusive"
        decided = "t >= 2 but the supporting check fails, which the plan calls inconclusive."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2 (or cannot be computed), which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": main,
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
