import numpy as np
import pandas as pd


def measure(bars):
    # ---------- helpers ----------
    def _day(ts):
        t = pd.to_datetime(ts, utc=True, errors="coerce")
        return t.dt.floor("D")

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    case_rows = []  # (coin, day, next_ret, forecast)
    coin_rets = {}

    for coin, wins in bars.items():
        all_rets = []
        per_coin_cases = []
        for wname, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.copy()
            if "timestamp" in df.columns:
                df = df.sort_values("timestamp")
            df = df.reset_index(drop=True)
            high = pd.to_numeric(df["high"], errors="coerce")
            low = pd.to_numeric(df["low"], errors="coerce")
            close = pd.to_numeric(df["close"], errors="coerce")
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            regime = df["regime"].astype(str) if "regime" in df.columns else pd.Series([""] * len(df))

            rng = high - low
            # width: day's range / mean bar range of last 20 bars, today included
            mean_rng = rng.rolling(20, min_periods=20).mean()
            width = rng / mean_rng
            # close location within the day's range, from the low
            loc = (close - low) / rng.where(rng > 0)

            # profile (falling agitated) cannot be rebuilt from in-window prices
            # (365-bar volatility percentile, 60-bar evolution): taken from the
            # detector's decision, which is mean_reversion only when no chop veto fired.
            profile_ok = regime == "mean_reversion"
            width_ok = (width >= 1.0) | width.isna()  # not computable in-window: rely on regime
            loc_ok = loc > 0.5
            situation = profile_ok & width_ok & loc_ok.fillna(False)

            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc < 0)).sum())

            # next-bar returns inside the window
            nxt = close.shift(-1) / close - 1.0
            all_rets.append(nxt.dropna().values)
            days = _day(df["timestamp"]) if "timestamp" in df.columns else pd.Series([pd.NaT] * len(df))
            m = (fc < 0) & nxt.notna()
            for i in np.where(m.values)[0]:
                per_coin_cases.append((coin, days.iloc[i], float(nxt.iloc[i]), float(fc.iloc[i])))
        allr = np.concatenate(all_rets) if all_rets else np.array([])
        coin_rets[coin] = float(np.mean(allr)) if len(allr) else np.nan
        case_rows.extend(per_coin_cases)

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = True if agreement is None else bool(agreement >= 0.9)

    main_name = "mean next-day unusual move on short cases (short side, coin drift removed)"
    thr = "confirm: mean > 0 with day-clustered t >= 2 and supporting check passed; reject: mean < 0 with t <= -2"
    reading = ("Profile (falling agitated) taken from the recorded regime since its 365-bar/60-bar inputs cannot be "
               "rebuilt inside windows, width = high-low range over the mean high-low range of the last 20 bars "
               "(today included, regime trusted where fewer than 20 in-window bars), loc > 0.5 from prices; "
               "clustered t uses per-day summed deviations with a G/(G-1) correction; upper half is |forecast| above "
               "the median, lower half the rest; the plan's 30 case-day minimum gives 'not observable'.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "case-days": None},
            "decided_by": ("Fewer than 90% of the bars with a nonzero forecast are short bars in the plan's situation "
                           "(falling agitated profile, range >= 20-day mean range, close above mid-range)."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    cases = pd.DataFrame(case_rows, columns=["coin", "day", "ret", "fc"])
    if len(cases):
        cases["mu"] = cases["coin"].map(coin_rets)
        cases["u"] = -(cases["ret"] - cases["mu"])
        cases = cases.dropna(subset=["u", "day"])
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0

    mean_u = float(cases["u"].mean()) if n_cases else None
    t_val = None
    if n_cases and n_days >= 2:
        dev = cases["u"] - mean_u
        S = dev.groupby(cases["day"]).sum().values
        G = len(S)
        var = (G / (G - 1.0)) * np.sum(S ** 2) / (n_cases ** 2)
        if var > 0:
            t_val = float(mean_u / np.sqrt(var))

    sup_val = None
    sup_pass = None
    if n_cases >= 2:
        a = cases["fc"].abs()
        med = float(a.median())
        up = cases.loc[a > med, "u"]
        lo = cases.loc[a <= med, "u"]
        if len(up) and len(lo):
            sup_val = float(up.mean() - lo.mean())
            sup_pass = bool(sup_val > 0)

    counts = {"case-days": n_days, "cases": n_cases}

    if n_days < 30:
        status = "not observable"
        decided = f"Only {n_days} case-days, below the plan's minimum of 30 case-days."
    elif t_val is None:
        status = "inconclusive"
        decided = "The day-clustered t could not be computed, so neither the confirm nor the reject rule is met."
    elif mean_u > 0 and t_val >= 2 and sup_pass is True:
        status = "confirmed"
        decided = "The mean unusual move is positive with t >= 2 and the upper-minus-lower half difference is above 0."
    elif mean_u < 0 and t_val <= -2:
        status = "rejected"
        decided = "The mean unusual move is negative with t <= -2."
    elif t_val >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the supporting check failed, which the plan calls inconclusive."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_u,
            "statistic": None if t_val is None else {"name": "t of the mean, cases of one day taken together", "value": t_val},
            "threshold": thr,
        },
        "supporting_check": {
            "name": "mean unusual move, upper |forecast| half minus lower half",
            "value": sup_val,
            "passed": sup_pass,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
