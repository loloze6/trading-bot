import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    RAW = "debug_info.components.fall_in_swings.last_history_value"

    # ---------- 1. Situation check ----------
    # Situation: a 5-day fall in swing units (raw value < 0), inside the choppy profile.
    # The choppy profile is regime "unknown"; the "chop" regime has no strategy.
    # Expected side: short, so the forecast should be < 0.
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            close = pd.to_numeric(df["close"], errors="coerce")

            # Use the recorded raw value. Where it is missing, rebuild its sign
            # from the 5-bar return, which has the same sign.
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            ret5 = close / close.shift(H) - 1.0
            raw_sign = np.sign(raw.where(raw.notna(), ret5))

            regime = df["regime"].astype(str)
            active = fc.notna() & (fc != 0)
            situ = (regime == "unknown") & (raw_sign < 0) & (fc < 0)
            n_active += int(active.sum())
            n_agree += int((active & situ).sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "mean short-direction 5-bar unusual move (return minus drift) on grid cases with forecast < 0"
    threshold_txt = ("confirm: mean > 0 with t >= 2 and larger-half minus smaller-half > 0; "
                     "reject: mean < 0 with t <= -2; at least 30 cases on at least 30 distinct days")
    sup_name = "mean unusual move of larger-|forecast| half minus smaller half"

    if not passed:
        if n_active == 0:
            decided = "No bar has a non-zero forecast, so the test cannot show the plan's short, choppy-market situation."
        else:
            decided = ("Fewer than 90% of the active bars are short bars in the choppy profile (regime 'unknown') "
                       "after a 5-day fall, as the plan's Fidelity requires.")
        return {
            "status": "mismatch",
            "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold_txt},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": decided,
            "reading": "Choppy profile read as regime 'unknown', the only regime with a strategy in the config.",
        }

    # ---------- 2. Criterion ----------
    case_rows = []
    for coin, wins in bars.items():
        grid_rets = []
        coin_cases = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            ts = pd.to_datetime(df["timestamp"], utc=True)
            n = len(df)
            # Non-overlapping grid, counted from the window's first row.
            for i in range(0, n, H):
                if i + H >= n:
                    break
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                grid_rets.append(r)
                if np.isfinite(fc[i]) and fc[i] < 0:
                    coin_cases.append((r, fc[i], ts.iloc[i].normalize()))
        if len(grid_rets) == 0:
            continue
        # Normal drift: the coin's mean 5-bar grid return over all its windows.
        drift = float(np.mean(grid_rets))
        for r, f, day in coin_cases:
            case_rows.append({"u": -(r - drift), "absf": abs(f), "day": day})

    cases = pd.DataFrame(case_rows, columns=["u", "absf", "day"])
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases > 0 else 0

    mean_u = float(cases["u"].mean()) if n_cases > 0 else None
    t_val = None
    if n_cases > 1 and n_days > 1:
        dev = cases["u"] - mean_u
        g = dev.groupby(cases["day"]).sum().values
        G = len(g)
        var = (G / (G - 1.0)) * np.sum(g ** 2) / (n_cases ** 2)
        se = np.sqrt(var)
        t_val = float(mean_u / se) if se > 0 else None

    diff = None
    sup_passed = None
    if n_cases >= 2:
        med = cases["absf"].median()
        large = cases.loc[cases["absf"] > med, "u"]
        small = cases.loc[cases["absf"] <= med, "u"]
        if len(large) > 0 and len(small) > 0:
            diff = float(large.mean() - small.mean())
            sup_passed = bool(diff > 0)
        else:
            sup_passed = False

    if n_cases < 30 or n_days < 30:
        status = "not observable"
        decided = (f"The plan's minimum of 30 cases on 30 distinct days is not reached "
                   f"({n_cases} cases on {n_days} days).")
    elif t_val is None:
        status = "inconclusive"
        decided = "The clustered t cannot be computed, so neither the confirm nor the reject rule is met."
    elif mean_u > 0 and t_val >= 2 and diff is not None and diff > 0:
        status = "confirmed"
        decided = "The main mean is above 0 with t >= 2 and the larger-half minus smaller-half difference is above 0."
    elif mean_u < 0 and t_val <= -2:
        status = "rejected"
        decided = "The main mean is below 0 with t <= -2: after choppy-market falls, prices rise more than the coin's drift."
    elif t_val >= 2:
        status = "inconclusive"
        decided = "The main t is >= 2 but the larger-half minus smaller-half difference is at or below 0."
    else:
        status = "inconclusive"
        decided = "The main t is between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_u,
            "statistic": None if t_val is None else {"name": "t of the mean, clustered by day", "value": t_val},
            "threshold": threshold_txt,
        },
        "supporting_check": {"name": sup_name, "value": diff, "passed": sup_passed},
        "counts": {"cases": n_cases, "distinct days": n_days},
        "decided_by": decided,
        "reading": ("Choppy profile read as regime 'unknown'; cases are grid bars (0, 5, 10, ... of each window) "
                    "with forecast < 0 and a full 5-bar forward return inside the window; drift is each coin's mean "
                    "5-bar grid return over all its windows; the clustered t uses day sums of deviations with a "
                    "G/(G-1) correction; the larger half is |forecast| above the median, the smaller half at or below it."),
    }
