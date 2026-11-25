import numpy as np
import pandas as pd


def measure(bars):
    H = 3
    BAND = 2.0
    RNG_COL = "debug_info.components.wide_range.last_history_value"

    def frame(df):
        d = df.copy()
        d["timestamp"] = pd.to_datetime(d["timestamp"], utc=True)
        d = d.sort_values("timestamp").reset_index(drop=True)
        d["forecast"] = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0)
        return d

    # ---------- 1. situation check ----------
    n_active_eval = 0
    n_agree = 0
    n_active_total = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = frame(df)
            c = d["close"].astype(float)
            ret1 = c.pct_change()
            std30 = ret1.rolling(30, min_periods=30).std(ddof=1)
            rng_re = ((d["high"].astype(float) - d["low"].astype(float)) / c) / std30
            if RNG_COL in d.columns:
                rec = pd.to_numeric(d[RNG_COL], errors="coerce")
                rng = rec.where(rec.notna(), rng_re)
            else:
                rng = rng_re
            evo = (c / c.shift(60) - 1.0) * 100.0
            active = d["forecast"] != 0
            n_active_total += int(active.sum())
            evaluable = active & rng.notna() & evo.notna()
            n_active_eval += int(evaluable.sum())
            sit = (rng >= 2.0 - 1e-9) & (evo < -10.0) & (d["forecast"] < 0)
            n_agree += int((evaluable & sit).sum())

    if n_active_eval > 0:
        agreement = n_agree / n_active_eval
        passed = agreement >= 0.9
    else:
        agreement = None
        passed = True

    reading_parts = [
        "The situation is a range/30-day-return-std ratio of at least 2.0 (recorded raw value, else recomputed) with a 60-bar price change below -10 % on a short forecast, judged on the active bars where the 60-bar change can be computed inside the window",
        "a case is the first short bet (rise of |forecast| of at least 2 from its lowest level since the last bet) in each 3-bar grid cell of a window, its return taken from that bar's close",
        "the drift is the coin's mean 3-bar return on the grid of all its windows",
        "the t sums the deviations per UTC day with a D/(D-1) correction",
        "the wider half is |forecast| above the case median, the narrower half at or below it",
        "the plan's minimum of 30 cases and 30 distinct days is applied as 'not observable'",
    ]
    reading = "; ".join(reading_parts) + "."

    main_name = "mean unusual 3-bar move in the short direction"
    main_thr = "confirm: mean > 0 with t >= 2 (and supporting check passes); reject: t <= -2"
    sup_name = "mean unusual move of wider half minus narrower half (split at median |forecast|)"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"cases": None, "distinct days": None},
            "decided_by": "Fewer than 90 % of the active bars are wide-range (ratio >= 2) days in a falling market (60-bar change below -10 %) with a short forecast, so the config does not trade the plan's situation on its side.",
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    cases = []  # (coin, day, unusual, absf)
    for coin, wins in bars.items():
        grid_rets = []
        coin_cases = []
        for w, df in wins.items():
            d = frame(df)
            c = d["close"].astype(float).values
            f = d["forecast"].values
            n = len(d)
            for i in range(0, n - H, H):
                if np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] > 0:
                    grid_rets.append(c[i + H] / c[i] - 1.0)
            # short bets
            ref = 0.0
            bets = np.zeros(n, dtype=bool)
            for i in range(n):
                s = -f[i] if f[i] < 0 else 0.0
                if s <= 0:
                    ref = 0.0
                    continue
                if s - ref >= BAND - 1e-12:
                    bets[i] = True
                    ref = s
                else:
                    ref = min(ref, s)
            seen = set()
            for i in np.where(bets)[0]:
                cell = i // H
                if cell in seen:
                    continue
                seen.add(cell)
                if i + H < n and np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] > 0:
                    r = c[i + H] / c[i] - 1.0
                    day = d["timestamp"].iloc[i].strftime("%Y-%m-%d")
                    coin_cases.append((coin, day, r, abs(f[i])))
        drift = float(np.mean(grid_rets)) if grid_rets else np.nan
        for coin_, day, r, af in coin_cases:
            if np.isfinite(drift):
                cases.append((coin_, day, -r + drift, af))

    n_cases = len(cases)
    days = sorted(set(x[1] for x in cases))
    n_days = len(days)
    counts = {"cases": n_cases, "distinct days": n_days}

    mean_u = None
    t = None
    if n_cases > 0:
        u = np.array([x[2] for x in cases])
        mean_u = float(u.mean())
        if n_days > 1:
            dev = pd.Series(u - mean_u).groupby([x[1] for x in cases]).sum().values
            se = np.sqrt(n_days / (n_days - 1) * np.sum(dev ** 2)) / n_cases
            t = float(mean_u / se) if se > 0 else None

    sup_val = None
    sup_pass = None
    if n_cases > 0:
        af = np.array([x[3] for x in cases])
        u = np.array([x[2] for x in cases])
        med = np.median(af)
        wide = af > med
        narrow = ~wide
        if wide.sum() > 0 and narrow.sum() > 0:
            sup_val = float(u[wide].mean() - u[narrow].mean())
            sup_pass = bool(sup_val > 0)
        else:
            sup_pass = False

    if n_cases < 30 or n_days < 30:
        status = "not observable"
        decided = f"The plan's minimum of 30 cases and 30 distinct days is not reached ({n_cases} cases on {n_days} days)."
    elif t is None:
        status = "inconclusive"
        decided = "The t of the mean unusual move cannot be computed, so neither the confirm nor the reject rule is met."
    elif mean_u > 0 and t >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "The mean unusual move is positive with t of 2 or more and the wider half beats the narrower half (confirm rule)."
        else:
            status = "inconclusive"
            decided = "The mean unusual move has a confirming t but the supporting check fails (inconclusive rule)."
    elif t <= -2:
        status = "rejected"
        decided = "The mean unusual move has t of -2 or less: the price rebounds relative to its drift after wide days (reject rule)."
    else:
        status = "inconclusive"
        decided = "The t of the mean unusual move lies between -2 and 2 (inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": bool(passed)},
        "main_measure": {
            "name": main_name,
            "value": mean_u,
            "statistic": None if t is None else {"name": "t of the mean, same-day cases summed", "value": t},
            "threshold": main_thr,
        },
        "supporting_check": {"name": sup_name, "value": sup_val, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
