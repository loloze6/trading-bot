import numpy as np
import pandas as pd


def measure(bars):
    H = 7
    ER_P = 30
    ER_MAX = 0.3

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    n_unverifiable = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").astype(float)
            fc = pd.to_numeric(d["forecast"], errors="coerce")
            absdiff = close.diff().abs()
            path = absdiff.rolling(ER_P, min_periods=ER_P).sum()
            net = (close - close.shift(ER_P)).abs()
            er = net / path
            ret30 = close / close.shift(ER_P) - 1.0
            ret7 = close / close.shift(H) - 1.0
            active = fc.notna() & (fc != 0)
            computable = er.notna() & ret30.notna() & ret7.notna()
            n_unverifiable += int((active & ~computable).sum())
            act = active & computable
            in_sit = (er < ER_MAX) & (np.sign(ret30) == np.sign(ret7)) & (ret7 != 0)
            side_ok = np.sign(fc) == np.sign(ret7)
            n_active += int(act.sum())
            n_agree += int((act & in_sit & side_ok).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9

    reading = ("Situation computed from closes (30-day efficiency ratio = |close[t]-close[t-30]| / sum of the 30 "
               "absolute daily changes, below 0.3, with the 7- and 30-day returns of the same sign, expected side = "
               "sign of the 7-day return), active bars lacking 30 bars of in-window history left out of the agreement "
               f"({n_unverifiable} such bars); grid = rows 0,7,14,... of each window; normal drift = the coin's mean "
               "7-bar return on that grid over all its windows; t = mean over a day-clustered standard error "
               "(deviations summed per day); top/bottom half = the floor(n/2) cases with the largest / smallest "
               "|forecast| (middle case dropped when n is odd); fewer than 30 distinct case days is treated as the "
               "plan's minimum count (not observable).")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars checked": n_active},
            "decided_by": ("Fewer than 90% of the active bars are bars where the 30-day efficiency ratio is below 0.3 "
                           "with the 7- and 30-day returns of the same sign and the forecast on the 7-day return's side."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    cases = []  # (coin, day, fwd, sign, absf)
    grid_rets = {}
    for coin, wins in bars.items():
        grid_rets[coin] = []
        for w, df in wins.items():
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").astype(float).values
            fc = pd.to_numeric(d["forecast"], errors="coerce").values
            ts = pd.to_datetime(d["timestamp"], utc=True)
            n = len(d)
            for i in range(0, n, H):
                if i + H >= n:
                    continue
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                grid_rets[coin].append(r)
                f = fc[i]
                if np.isfinite(f) and f != 0:
                    cases.append((coin, ts.iloc[i].normalize(), r, float(np.sign(f)), abs(float(f))))

    drift = {c: (float(np.mean(v)) if len(v) else np.nan) for c, v in grid_rets.items()}
    rows = []
    for coin, day, r, s, a in cases:
        if np.isfinite(drift[coin]):
            rows.append((coin, day, (r - drift[coin]) * s, a))
    cdf = pd.DataFrame(rows, columns=["coin", "day", "u", "absf"])
    n_cases = int(len(cdf))
    n_days = int(cdf["day"].nunique()) if n_cases else 0

    mean_u = None
    t = None
    if n_cases > 0:
        mean_u = float(cdf["u"].mean())
        if n_days > 1:
            dev = cdf["u"] - mean_u
            S = dev.groupby(cdf["day"]).sum().values
            se = np.sqrt(np.sum(S ** 2)) / n_cases * np.sqrt(n_days / (n_days - 1))
            t = float(mean_u / se) if se > 0 else None

    diff = None
    sup_pass = None
    if n_cases >= 2:
        srt = cdf.sort_values("absf", ascending=False, kind="mergesort").reset_index(drop=True)
        k = n_cases // 2
        top = srt["u"].iloc[:k]
        bot = srt["u"].iloc[n_cases - k:]
        diff = float(top.mean() - bot.mean())
        sup_pass = bool(diff > 0)

    counts = {"cases": n_cases, "distinct case days": n_days}
    main = {
        "name": "mean signed 7-bar unusual move (forward return minus coin's normal drift)",
        "value": mean_u,
        "statistic": {"name": "t of the mean, cases of the same day pooled", "value": t} if t is not None else None,
        "threshold": "confirm: mean > 0 with t >= 2 and supporting check passing; reject: mean < 0 with t <= -2",
    }
    sup = {"name": "mean unusual move, top half minus bottom half of |forecast|", "value": diff, "passed": sup_pass}

    if n_days < 30:
        status = "not observable"
        decided = f"Only {n_days} distinct case days, fewer than the plan's minimum of 30."
    elif t is None:
        status = "inconclusive"
        decided = "The t of the mean unusual move could not be computed, so neither confirm nor reject is met."
    elif mean_u > 0 and t >= 2 and sup_pass:
        status = "confirmed"
        decided = "The mean unusual move is positive with t >= 2 and the top half of |forecast| beats the bottom half."
    elif mean_u < 0 and t <= -2:
        status = "rejected"
        decided = "The mean unusual move is negative with t <= -2: the move reverses instead of continuing."
    elif mean_u > 0 and t >= 2:
        status = "inconclusive"
        decided = "A confirm-level t without the supporting check passing."
    else:
        status = "inconclusive"
        decided = "The t of the mean unusual move lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
