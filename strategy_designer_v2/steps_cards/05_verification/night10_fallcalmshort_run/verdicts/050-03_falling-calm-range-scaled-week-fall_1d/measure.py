import numpy as np
import pandas as pd


def measure(bars):
    RAW = "debug_info.components.scaled_fall.last_history_value"
    H = 3
    MIN_CASES = 100
    MIN_DAYS = 60

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            fc = pd.to_numeric(d["forecast"], errors="coerce")
            active = fc.notna() & (fc != 0)
            if not active.any():
                continue
            close = pd.to_numeric(d["close"], errors="coerce")
            # 7-day return sign: from the component's raw value where recorded, else from prices
            ret7 = close / close.shift(7) - 1.0
            if RAW in d.columns:
                raw = pd.to_numeric(d[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=d.index)
            fell = pd.Series(np.where(raw.notna(), raw < 0, ret7 < 0), index=d.index).astype(bool)
            # falling calm profile: the regime detector leaves "unknown" (the strategy's regime)
            # only when neither veto (trend >= -10, swing > 0.5) fires
            calm_fall = d["regime"].astype(str) == "unknown"
            short = fc < 0
            situ = fell & calm_fall & short
            n_active += int(active.sum())
            n_agree += int((situ & active).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.90)

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are short bars after a 7-day fall "
                           "in the falling calm profile (regime 'unknown'), so the config does not do what the "
                           "Fidelity says." if n_active > 0 else
                           "The record has no bar with a non-zero forecast, so the plan's short-after-fall situation "
                           "cannot be matched."),
            "reading": "The falling calm profile is read from the recorded regime ('unknown' = no veto fired) and the "
                       "7-day fall from the sign of the component's raw value (prices where it is not recorded).",
        }

    # ---------- 2. Criterion ----------
    # normal 3-bar drift per coin: mean over the non-overlapping grid of all its windows
    drift = {}
    grid_rows = []
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").values
            fc = pd.to_numeric(d["forecast"], errors="coerce").values
            ts = pd.to_datetime(d["timestamp"], utc=True)
            n = len(d)
            for i in range(0, n - H, H):
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                rets.append(r)
                grid_rows.append((coin, r, fc[i], ts.iloc[i].normalize()))
        drift[coin] = float(np.mean(rets)) if rets else np.nan

    cases = [(coin, r, f, day) for coin, r, f, day in grid_rows
             if np.isfinite(f) and f < 0 and np.isfinite(drift.get(coin, np.nan))]
    n_cases = len(cases)
    days = [c[3] for c in cases]
    n_days = len(set(days))
    counts = {"grid cases": int(n_cases), "distinct days": int(n_days)}

    mean_val = None
    t_val = None
    slope = None
    if n_cases > 0:
        x = np.array([-(r - drift[coin]) for coin, r, f, day in cases], dtype=float)
        absf = np.array([abs(f) for coin, r, f, day in cases], dtype=float)
        mean_val = float(np.mean(x))
        # t with the cases of one day taken together (day-clustered standard error)
        dev = pd.Series(x - mean_val).groupby(pd.Series(days)).sum().values
        D = len(dev)
        if D > 1:
            var = (D / (D - 1.0)) * np.sum(dev ** 2) / (n_cases ** 2)
            se = np.sqrt(var)
            t_val = float(mean_val / se) if se > 0 else None
        if n_cases > 1 and np.var(absf) > 0:
            slope = float(np.polyfit(absf, x, 1)[0])

    main = {
        "name": "mean short-direction 3-bar unusual move on forecast<0 grid cases",
        "value": mean_val,
        "statistic": {"name": "t of the mean, cases of one day taken together",
                      "value": t_val} if t_val is not None else None,
        "threshold": "confirm: mean > 0 with t >= 2 (and slope > 0); reject: mean < 0 with t <= -2",
    }
    slope_pass = None if slope is None else bool(slope > 0)
    support = {"name": "OLS slope of unusual move on |forecast|", "value": slope, "passed": slope_pass}

    reading = ("All coins and windows present in the record are used; the drift is each coin's mean 3-bar return on "
               "the non-overlapping grid of all its windows; the per-day t uses day-summed deviations with a "
               "D/(D-1) correction; the falling calm profile is read from the recorded regime 'unknown'.")

    if n_cases < MIN_CASES or n_days < MIN_DAYS:
        return {
            "status": "not observable",
            "situation_check": {"agreement": agreement, "passed": True},
            "main_measure": main,
            "supporting_check": support,
            "counts": counts,
            "decided_by": f"The plan needs at least {MIN_CASES} grid cases on at least {MIN_DAYS} distinct days; "
                          f"the record has {n_cases} cases on {n_days} days.",
            "reading": reading,
        }

    if mean_val is not None and t_val is not None and mean_val > 0 and t_val >= 2 and slope_pass:
        status = "confirmed"
        decided = "The mean unusual move is above 0 with t >= 2 and the slope on |forecast| is above 0 (confirm rule)."
    elif mean_val is not None and t_val is not None and mean_val < 0 and t_val <= -2:
        status = "rejected"
        decided = "The mean unusual move is below 0 with t <= -2, a reversal after scaled falls (reject rule)."
    else:
        status = "inconclusive"
        if mean_val is not None and t_val is not None and mean_val > 0 and t_val >= 2:
            decided = "The main t is >= 2 but the supporting slope is at or below 0 (inconclusive rule)."
        else:
            decided = "The main t lies between -2 and 2 (inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": support,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
