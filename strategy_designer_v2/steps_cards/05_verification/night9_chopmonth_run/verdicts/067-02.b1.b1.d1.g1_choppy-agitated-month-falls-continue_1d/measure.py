import numpy as np
import pandas as pd


def measure(bars):
    H = 7
    RAW = "debug_info.components.month_fall.last_history_value"

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            # Where the component is not recorded, recompute the 30-bar return from prices (inside the window).
            px_ret = (close / close.shift(30) - 1.0) * 100.0
            raw = raw.where(raw.notna(), px_ret)
            regime = df["regime"].astype(str) if "regime" in df.columns else pd.Series("", index=df.index)
            # Choppy agitated: the detector's non-chop regime ("unknown", the only regime with a strategy).
            choppy_agitated = regime == "unknown"
            month_fall = raw < 0
            active = fc != 0
            agree = active & choppy_agitated & month_fall & (fc < 0)
            n_active += int(active.sum())
            n_agree += int(agree.sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9

    main_name = "mean unusual move per case, short direction, 7 bars"
    threshold = "confirm: mean > 0 with t >= 2 and deeper-minus-shallower > 0; reject: mean < 0 with t <= -2"
    reading = ("Choppy agitated is read as the detector's 'unknown' regime (the only regime with a strategy) and the month "
               "fall as the raw 30-bar return < 0 (from prices where not recorded); the coin's mean 7-bar return is taken on "
               "the same non-overlapping grid over all its windows; t clusters cases by UTC day (deviations summed per day); "
               "the median split puts forecasts <= median in the deeper half and > median in the shallower half.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "agreeing bars": int(n_agree)},
            "decided_by": ("No active bars in the record." if agreement is None else
                           "Fewer than 90% of the bars with a non-zero forecast are short bars in a choppy agitated "
                           "regime with the close below its close 30 bars earlier."),
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            ts = pd.to_datetime(df["timestamp"], utc=True)
            n = len(df)
            for i in range(0, n - H, H):
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 <= 0:
                    continue
                rows.append({"coin": coin, "day": ts.iloc[i].floor("D"),
                             "r": c1 / c0 - 1.0, "fc": fc[i]})
    allg = pd.DataFrame(rows, columns=["coin", "day", "r", "fc"])
    if len(allg):
        drift = allg.groupby("coin")["r"].mean()
        cases = allg[allg["fc"] < 0].copy()
        cases["u"] = -(cases["r"] - cases["coin"].map(drift))
    else:
        cases = pd.DataFrame(columns=["coin", "day", "r", "fc", "u"])

    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0
    counts = {"cases": n_cases, "days": n_days}

    mean_u = float(cases["u"].mean()) if n_cases else None
    t_val = None
    if n_cases >= 2:
        dev = cases["u"] - mean_u
        s_day = dev.groupby(cases["day"]).sum()
        se = np.sqrt(float((s_day ** 2).sum())) / n_cases
        if n_days > 1:
            se *= np.sqrt(n_days / (n_days - 1.0))
        t_val = float(mean_u / se) if se > 0 else None

    diff = None
    sup_passed = None
    if n_cases >= 2:
        med = float(cases["fc"].median())
        deep = cases[cases["fc"] <= med]["u"]
        shallow = cases[cases["fc"] > med]["u"]
        if len(deep) and len(shallow):
            diff = float(deep.mean() - shallow.mean())
            sup_passed = bool(diff > 0)
        else:
            sup_passed = False

    main = {"name": main_name, "value": mean_u,
            "statistic": None if t_val is None else {"name": "t of the mean, cases clustered by day", "value": t_val},
            "threshold": threshold}
    sup = {"name": "deeper-half minus shallower-half mean unusual move", "value": diff, "passed": sup_passed}

    if n_cases < 30:
        status = "not observable"
        decided = f"Fewer than 30 cases ({n_cases}), the plan's minimum count."
    elif t_val is None:
        status = "inconclusive"
        decided = "The t could not be computed (zero standard error), so neither confirm nor reject is met."
    elif mean_u > 0 and t_val >= 2 and sup_passed:
        status = "confirmed"
        decided = "Mean unusual move above 0 with t >= 2 and the deeper half's move larger than the shallower half's."
    elif mean_u < 0 and t_val <= -2:
        status = "rejected"
        decided = "Mean unusual move below 0 with t <= -2: the coin rises more than its drift after its month-long falls."
    elif t_val >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the deeper half does not show the larger move, which the plan calls inconclusive."
    else:
        status = "inconclusive"
        decided = "t lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": main,
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
