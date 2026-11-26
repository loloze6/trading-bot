import numpy as np
import pandas as pd


def measure(bars):
    LHV = "debug_info.components.flatness.last_history_value"
    PPV = "debug_info.components.flatness.post_pipeline_value"
    SIT_LEVEL = 0.8  # smallness 1/(1+|r|/s20) >= 0.8  <=>  |r|/s20 <= 0.25
    TOL = 1e-9

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    case_frames = []
    coin_drift = {}

    for coin, windows in bars.items():
        all_rets = []
        per_window = []
        for wname in sorted(windows.keys(), key=lambda w: (len(str(w)), str(w))):
            df = windows[wname]
            if df is None or len(df) == 0:
                continue
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)

            # Raw smallness from the record, recomputed from prices where missing
            r = close / close.shift(1) - 1.0
            s = r.rolling(20, min_periods=20).std(ddof=1)
            recomputed = 1.0 / (1.0 + (r.abs() / s.replace(0.0, np.nan)))
            if LHV in df.columns:
                raw = pd.to_numeric(df[LHV], errors="coerce")
                raw = raw.where(raw.notna(), recomputed)
            else:
                raw = recomputed

            active = fc != 0
            in_sit = raw >= SIT_LEVEL - TOL
            agree = active & in_sit & (fc < 0)
            n_active += int(active.sum())
            n_agree += int(agree.sum())

            # next-bar return inside the window
            fwd = close.shift(-1) / close - 1.0
            all_rets.append(fwd.dropna())

            ppv = (pd.to_numeric(df[PPV], errors="coerce")
                   if PPV in df.columns else pd.Series(np.nan, index=df.index))
            day = pd.to_datetime(df["timestamp"], utc=True).dt.floor("D")
            per_window.append(pd.DataFrame({
                "coin": coin, "day": day, "fwd": fwd,
                "fc": fc, "ppv": ppv,
            }))
        if all_rets:
            allr = pd.concat(all_rets)
            coin_drift[coin] = float(allr.mean()) if len(allr) else np.nan
        for f in per_window:
            case_frames.append(f)

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed_sit = agreement is not None and agreement >= 0.9

    main_name = "mean drift-adjusted next-day return of short cases"
    threshold = "confirm: mean < 0 with t <= -2 (and check passes); reject: mean > 0 with t >= +2"
    reading = ("Every bar with forecast < 0 is a case (the plan's own case definition), the drift is the coin's "
               "mean next-bar return over all its windows, the day-clustered t sums deviations per UTC day with a "
               "D/(D-1) correction, the halves are the n//2 cases with largest and smallest |post_pipeline_value| "
               "(middle case dropped if odd), and the plan's 'fewer than 200 cases' is treated as the minimum count "
               "giving 'not observable'.")

    if not passed_sit:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "cases": None},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are short bars on a day whose "
                           "smallness 1/(1+|r|/s20) is at least 0.8, as the Fidelity's situation and short side require."
                           if n_active > 0 else "The record has no bar with a non-zero forecast."),
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    data = pd.concat(case_frames, ignore_index=True) if case_frames else pd.DataFrame(
        columns=["coin", "day", "fwd", "fc", "ppv"])
    data["drift"] = data["coin"].map(coin_drift)
    cases = data[(data["fc"] < 0) & data["fwd"].notna() & data["drift"].notna()].copy()
    cases["adj"] = cases["fwd"] - cases["drift"]
    n = int(len(cases))
    n_days = int(cases["day"].nunique()) if n else 0

    mean_adj = float(cases["adj"].mean()) if n else None
    t_val = None
    if n >= 2 and n_days >= 2:
        dev = cases["adj"] - mean_adj
        S = dev.groupby(cases["day"]).sum()
        D = len(S)
        var = (D / (D - 1.0)) * float((S ** 2).sum()) / (n ** 2)
        if var > 0:
            t_val = float(mean_adj / np.sqrt(var))

    # supporting check
    sc = cases[cases["ppv"].notna()].copy()
    sc["absp"] = sc["ppv"].abs()
    sc = sc.sort_values("absp", kind="mergesort").reset_index(drop=True)
    half = len(sc) // 2
    sup_value = None
    sup_pass = None
    if half >= 1:
        bottom = sc.iloc[:half]["adj"].mean()
        top = sc.iloc[len(sc) - half:]["adj"].mean()
        sup_value = float(top - bottom)
        sup_pass = bool(top < bottom)
    supporting = {"name": "mean adj. return, top half minus bottom half of |flatness|",
                  "value": sup_value, "passed": sup_pass}

    counts = {"cases": n, "days with cases": n_days}

    if n < 200:
        status = "not observable"
        decided = f"Only {n} cases, fewer than the plan's minimum of 200."
    elif t_val is None:
        status = "inconclusive"
        decided = "The t of the main measure could not be computed, so neither confirm nor reject is met."
    elif mean_adj < 0 and t_val <= -2:
        if sup_pass:
            status = "confirmed"
            decided = "The mean drift-adjusted next-day return is negative with t <= -2 and the top half of flatness is below the bottom half."
        else:
            status = "inconclusive"
            decided = "A confirm-strength main result (negative, t <= -2) with a failed supporting check is inconclusive."
    elif mean_adj > 0 and t_val >= 2:
        status = "rejected"
        decided = "The mean drift-adjusted next-day return is positive with t >= +2."
    else:
        status = "inconclusive"
        decided = "The t of the mean drift-adjusted next-day return lies between -2 and +2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {"name": main_name, "value": mean_adj,
                         "statistic": ({"name": "t of the mean, cases pooled by day", "value": t_val}
                                       if t_val is not None else None),
                         "threshold": threshold},
        "supporting_check": supporting,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
