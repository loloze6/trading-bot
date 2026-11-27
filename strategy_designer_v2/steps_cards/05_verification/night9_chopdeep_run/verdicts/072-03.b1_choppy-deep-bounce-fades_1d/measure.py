import numpy as np
import pandas as pd


def _to_day(ts):
    s = pd.Series(ts)
    if np.issubdtype(s.dtype, np.number):
        mx = s.abs().max()
        unit = "ms" if mx > 1e11 else "s"
        d = pd.to_datetime(s, unit=unit, utc=True)
    else:
        d = pd.to_datetime(s, utc=True)
    return d.dt.floor("D").dt.strftime("%Y-%m-%d").values


def _short_bets(fc, band=2.0):
    """Short-side bets: a fall of the forecast of at least `band` from its least
    negative level on the short side since the last bet (from 0 after flat / side change)."""
    n = len(fc)
    bets = np.zeros(n, dtype=bool)
    ref = 0.0
    for i in range(n):
        f = fc[i]
        if not np.isfinite(f) or f >= 0:
            ref = 0.0
            continue
        if f <= ref - band:
            bets[i] = True
            ref = f
        else:
            ref = max(ref, f)
    return bets


def measure(bars):
    H = 10
    BAND = 2.0
    fc_col = "forecast"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin in sorted(bars.keys()):
        for w in sorted(bars[coin].keys()):
            df = bars[coin][w]
            if df is None or len(df) == 0:
                continue
            close = df["close"].astype(float).values
            fc = df[fc_col].astype(float).values
            regime = df["regime"].astype(str).values
            prev = np.r_[np.nan, close[:-1]]
            up = close / prev - 1.0 > 0
            # first bar of a window: prior close not in record -> rely on the detector's decision
            first_ok = np.zeros(len(df), dtype=bool)
            first_ok[0] = regime[0] == "mean_reversion"
            up_day = np.where(np.isfinite(prev), up, first_ok)
            choppy = regime != "chop"
            situation = up_day & choppy
            active = np.isfinite(fc) & (fc != 0)
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc < 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "mean unusual move over 10 bars after short bets, short direction"
    threshold = "mean > 0 with t >= 2 confirms (with deeper-minus-shallower > 0); mean < 0 with t <= -2 rejects"
    reading_base = (
        "Up day computed from consecutive closes (first window bar from the recorded regime) and the choppy profile "
        "taken as the recorded regime not being 'chop'; a case is the first short bet in each 10-bar cell of a "
        "window's grid, the per-day clustered t uses a D/(D-1) correction, the deeper half is |forecast| strictly "
        "above the median, and the plan's minimum-count clause is reported as 'not observable'."
    )

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "agreeing bars": int(n_agree)},
            "decided_by": "Fewer than 90% of the bars with a nonzero forecast are short bets on up days inside the "
                          "choppy profile, so the config does not do what the plan's Fidelity says.",
            "reading": reading_base,
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin in sorted(bars.keys()):
        grid_rets = []
        coin_cases = []
        for w in sorted(bars[coin].keys()):
            df = bars[coin][w]
            if df is None or len(df) == 0:
                continue
            close = df["close"].astype(float).values
            fc = df[fc_col].astype(float).values
            days = _to_day(df["timestamp"].values)
            n = len(df)
            for p in range(0, n - H, H):
                r = close[p + H] / close[p] - 1.0
                if np.isfinite(r):
                    grid_rets.append(r)
            bets = _short_bets(fc, BAND)
            for c0 in range(0, n, H):
                idx = np.where(bets[c0:c0 + H])[0]
                if len(idx) == 0:
                    continue
                t = c0 + int(idx[0])
                if t + H >= n:
                    continue
                r = close[t + H] / close[t] - 1.0
                if not np.isfinite(r):
                    continue
                coin_cases.append((days[t], r, abs(fc[t])))
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))
        for d, r, a in coin_cases:
            rows.append({"day": d, "u": -(r - drift), "absf": a})

    cases = pd.DataFrame(rows, columns=["day", "u", "absf"])
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0
    counts = {"cases": n_cases, "distinct days": n_days}

    mean_u = float(cases["u"].mean()) if n_cases else None
    t_val = None
    if n_cases >= 2 and n_days >= 2:
        dev = cases["u"] - cases["u"].mean()
        s = dev.groupby(cases["day"]).sum().values
        var = (np.sum(s ** 2) / n_cases ** 2) * n_days / (n_days - 1)
        se = np.sqrt(var)
        t_val = float(mean_u / se) if se > 0 else None

    diff = None
    if n_cases >= 2:
        med = cases["absf"].median()
        deep = cases.loc[cases["absf"] > med, "u"]
        shallow = cases.loc[cases["absf"] <= med, "u"]
        if len(deep) > 0 and len(shallow) > 0:
            diff = float(deep.mean() - shallow.mean())
    sup_pass = None if diff is None else bool(diff > 0)

    main = {"name": main_name, "value": mean_u,
            "statistic": None if t_val is None else {"name": "t of the mean, cases summed per day", "value": t_val},
            "threshold": threshold}
    support = {"name": "deeper-minus-shallower mean unusual move (median |forecast| split)",
               "value": diff, "passed": sup_pass}

    if n_cases < 50 or n_days < 30:
        status = "not observable"
        decided = (f"Minimum counts not reached: {n_cases} cases (need 50) on {n_days} distinct days (need 30).")
    elif t_val is None or mean_u is None:
        status = "inconclusive"
        decided = "The t could not be computed, so neither the confirm nor the reject rule is met."
    elif mean_u > 0 and t_val >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "The mean unusual move is positive with t >= 2 and the deeper-minus-shallower difference is above 0."
        else:
            status = "inconclusive"
            decided = "A confirming t whose deeper-minus-shallower difference is 0 or below is inconclusive."
    elif mean_u < 0 and t_val <= -2:
        status = "rejected"
        decided = "The mean unusual move is negative with t <= -2: the coin rises more than its drift after deep up-day closes."
    else:
        status = "inconclusive"
        decided = "The main measure's t lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": support,
        "counts": counts,
        "decided_by": decided,
        "reading": reading_base,
    }
