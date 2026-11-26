import numpy as np
import pandas as pd


def measure(bars):
    H = 7
    BAND = 2.0
    MIN_CASES = 30
    RAW = "debug_info.components.scaled_fall_7d.last_history_value"

    def as_float(s):
        return pd.to_numeric(s, errors="coerce").astype(float)

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.sort_values("timestamp").reset_index(drop=True)
            f = as_float(d["forecast"]).fillna(0.0).values
            close = as_float(d["close"]).values
            ret7 = pd.Series(close).pct_change(H).values  # inside the window only
            if RAW in d.columns:
                raw = as_float(d[RAW]).values
            else:
                raw = np.full(len(d), np.nan)
            # the fall: raw scaled 7-day return < 0; recomputed from prices where not recorded
            fall_val = np.where(np.isnan(raw), ret7, raw)
            fall = np.nan_to_num(fall_val, nan=0.0) < 0
            # the choppy-agitated profile: the regime not vetoed to chop, i.e. the "unknown" regime holding the strategy
            profile = d["regime"].astype(str).values == "unknown"
            active = f != 0
            agree = active & profile & fall & (f < 0)
            n_active += int(active.sum())
            n_agree += int(agree.sum())

    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "mean short-direction unusual 7-bar move per case"
    threshold = "confirm: mean > 0 with day-clustered t >= 2 and check passes; reject: mean < 0 with t <= -2"
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "cases": 0},
            "decided_by": ("fewer than 90% of the active bars are short bars in the choppy-agitated profile "
                           "('unknown' regime) after a 7-day fall, as the Fidelity requires"
                           if n_active > 0 else "the record has no active bar, so the forecast never takes the plan's short side"),
            "reading": "the profile is read as regime == 'unknown' (the regime the vetoes leave as choppy agitated); the fall as the raw scaled 7-day return < 0.",
        }

    # ---------- 2. criterion ----------
    cases = []  # (coin, day, ret7fwd, absf)
    drift = {}
    for coin, wins in bars.items():
        grid_rets = []
        prepared = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.sort_values("timestamp").reset_index(drop=True)
            close = as_float(d["close"]).values
            n = len(d)
            for p in range(0, n - H, H):
                if np.isfinite(close[p]) and np.isfinite(close[p + H]) and close[p] > 0:
                    grid_rets.append(close[p + H] / close[p] - 1.0)
            prepared.append(d)
        drift[coin] = float(np.mean(grid_rets)) if grid_rets else np.nan

        for d in prepared:
            f = as_float(d["forecast"]).fillna(0.0).values
            close = as_float(d["close"]).values
            ts = pd.to_datetime(d["timestamp"], utc=True)
            n = len(d)
            # bets on the short side
            bet = np.zeros(n, dtype=bool)
            ref = 0.0
            prev_short = False
            for i in range(n):
                if f[i] < 0:
                    mag = -f[i]
                    if not prev_short:
                        ref = 0.0
                    if mag - ref >= BAND:
                        bet[i] = True
                        ref = mag
                    else:
                        ref = min(ref, mag)
                    prev_short = True
                else:
                    prev_short = False
                    ref = 0.0
            # once per 7-bar grid cell: first bet in the cell
            for start in range(0, n, H):
                idx = np.where(bet[start:start + H])[0]
                if len(idx) == 0:
                    continue
                t = start + idx[0]
                if t + H >= n:
                    continue
                c0, c1 = close[t], close[t + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 <= 0:
                    continue
                cases.append((coin, ts.iloc[t].floor("D"), c1 / c0 - 1.0, abs(f[t])))

    rows = [(c, day, -(r - drift[c]), a) for (c, day, r, a) in cases if np.isfinite(drift.get(c, np.nan))]
    n_cases = len(rows)
    days = sorted(set(r[1] for r in rows))
    n_days = len(days)
    counts = {"cases": int(n_cases), "days": int(n_days)}

    reading = ("profile = regime 'unknown', fall = raw scaled 7-day return < 0; a case is the first short bet "
               "(rise of |forecast| on the short side >= 2 from its low since the last bet) in each 7-bar grid cell "
               "of a window; t uses day-clustered errors (deviations summed per UTC day, G/(G-1) correction); "
               "the larger half is |forecast| strictly above the median, the smaller half at or below it; "
               "the plan's 30-case minimum gives 'not observable'.")

    if n_cases == 0:
        return {
            "status": "not observable",
            "situation_check": {"agreement": float(agreement), "passed": True},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": {"name": "larger minus smaller |forecast| half mean unusual move", "value": None, "passed": None},
            "counts": counts,
            "decided_by": "fewer than the plan's minimum of 30 cases (none)",
            "reading": reading,
        }

    u = np.array([r[2] for r in rows], dtype=float)
    a = np.array([r[3] for r in rows], dtype=float)
    dayk = pd.Series([r[1] for r in rows])
    mean_u = float(u.mean())
    dev = pd.Series(u - mean_u)
    per_day = dev.groupby(dayk.values).sum().values
    G = len(per_day)
    t_stat = None
    if G > 1:
        var_mean = (per_day ** 2).sum() / (n_cases ** 2) * G / (G - 1)
        if var_mean > 0:
            t_stat = float(mean_u / np.sqrt(var_mean))

    med = float(np.median(a))
    hi = u[a > med]
    lo = u[a <= med]
    if len(hi) > 0 and len(lo) > 0:
        diff = float(hi.mean() - lo.mean())
        check_pass = bool(diff > 0)
    else:
        diff = None
        check_pass = False

    main = {"name": main_name, "value": mean_u,
            "statistic": {"name": "t of the mean, cases of one day together", "value": t_stat} if t_stat is not None else None,
            "threshold": threshold}
    support = {"name": "mean unusual move, larger minus smaller |forecast| half", "value": diff, "passed": check_pass}

    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"only {n_cases} cases, fewer than the plan's minimum of 30"
    elif t_stat is None:
        status = "inconclusive"
        decided = "the t cannot be computed, so neither the confirm nor the reject rule is met"
    elif mean_u > 0 and t_stat >= 2:
        if check_pass:
            status = "confirmed"
            decided = "mean short-direction unusual move > 0 with t >= 2 and the larger-|forecast| half beats the smaller"
        else:
            status = "inconclusive"
            decided = "the main measure meets the confirm rule but the supporting check fails"
    elif mean_u < 0 and t_stat <= -2:
        status = "rejected"
        decided = "mean short-direction unusual move < 0 with t <= -2"
    else:
        status = "inconclusive"
        decided = "the t lies between -2 and 2 (or the mean's sign disagrees with it)"

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": main,
        "supporting_check": support,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
