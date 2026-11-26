import numpy as np
import pandas as pd


def measure(bars):
    FC = "forecast"
    RAW = "debug_info.components.down_run.last_history_value"

    # ---------- per-coin drift: mean daily return over all windows (pooled, within windows only)
    drift = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            d = df.sort_values("timestamp")
            c = d["close"].astype(float).values
            if len(c) > 1:
                rets.append(c[1:] / c[:-1] - 1.0)
        drift[coin] = float(np.mean(np.concatenate(rets))) if rets else np.nan

    # ---------- situation check + case collection
    n_active = 0
    n_agree = 0
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df.sort_values("timestamp").reset_index(drop=True)
            c = d["close"].astype(float).values
            fc = pd.to_numeric(d[FC], errors="coerce").fillna(0.0).values
            raw = pd.to_numeric(d[RAW], errors="coerce").values if RAW in d.columns else np.full(len(d), np.nan)
            reg = d["regime"].astype(str).values
            n = len(d)
            for t in range(n):
                if fc[t] != 0:
                    n_active += 1
                    # profile (falling agitated): the detector's own decision, since its vetoes send
                    # every bar outside the profile to 'chop'; detector components are not recorded
                    in_profile = reg[t] == "mean_reversion"
                    run_ok = np.isfinite(raw[t]) and raw[t] >= 1
                    if t >= 2:
                        price_ok = (c[t] > c[t - 1]) and (c[t - 1] < c[t - 2])
                    elif t == 1:
                        price_ok = c[t] > c[t - 1]
                    else:
                        price_ok = True
                    if in_profile and run_ok and price_ok and fc[t] < 0:
                        n_agree += 1
                if fc[t] < 0 and t + 1 < n and np.isfinite(raw[t]) and np.isfinite(drift[coin]):
                    r = c[t + 1] / c[t] - 1.0
                    rows.append((pd.Timestamp(d["timestamp"].iloc[t]).floor("D"), float(raw[t]), r - drift[coin]))

    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.9
    situation = {"agreement": float(agreement), "passed": bool(passed)}

    main_name = "slope of next-day excess return on prior down-run length (forecast < 0)"
    thr = "confirm: slope < 0 with t <= -2 and mean short-side unusual move > 0; reject: slope > 0 with t >= +2, or mean unusual move < 0 with t <= -2"
    reading = ("The profile is checked through the detector's regime (its vetoes send bars outside the falling agitated profile to chop and its "
               "components are not recorded), the up-close-after-down-day from prices; 'cases on the same day are summed' is read as a "
               "day-clustered standard error (scores and deviations summed per day) for the slope t and for the unusual move's t; "
               "fewer than 100 cases or 60 days is reported as not observable.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": situation,
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"cases": len(rows), "distinct days": len(set(r[0] for r in rows)), "active bars": n_active},
            "decided_by": ("Fewer than 90% of bars with a non-zero forecast are short bars in the mean_reversion regime (falling agitated profile) "
                           "with a prior down run >= 1 ending in an up close."),
            "reading": reading,
        }

    cases = pd.DataFrame(rows, columns=["day", "x", "y"])
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0
    counts = {"cases": n_cases, "distinct days": n_days}

    slope = None
    slope_t = None
    mean_u = None
    t_u = None
    if n_cases >= 3 and cases["x"].var() > 0:
        x = cases["x"].values
        y = cases["y"].values
        xc = x - x.mean()
        sxx = float(np.sum(xc ** 2))
        slope = float(np.sum(xc * (y - y.mean())) / sxx)
        intercept = y.mean() - slope * x.mean()
        e = y - intercept - slope * x
        score = pd.Series(xc * e).groupby(cases["day"].values).sum().values
        G = len(score)
        corr = G / (G - 1) if G > 1 else 1.0
        var_b = corr * float(np.sum(score ** 2)) / sxx ** 2
        slope_t = float(slope / np.sqrt(var_b)) if var_b > 0 else 0.0
    if n_cases >= 2:
        u = -cases["y"].values
        mean_u = float(np.mean(u))
        dev = pd.Series(u - mean_u).groupby(cases["day"].values).sum().values
        se = np.sqrt(float(np.sum(dev ** 2))) / n_cases
        G = len(dev)
        if G > 1:
            se *= np.sqrt(G / (G - 1))
        t_u = float(mean_u / se) if se > 0 else 0.0

    support_passed = None if mean_u is None else bool(mean_u > 0)
    supporting = {"name": "mean short-side unusual move (drift removed, sign flipped)", "value": mean_u,
                  "passed": support_passed, "t": t_u}
    main = {"name": main_name, "value": slope,
            "statistic": None if slope_t is None else {"name": "slope t (day-clustered)", "value": slope_t},
            "threshold": thr}

    if n_cases < 100 or n_days < 60 or slope_t is None:
        status = "not observable"
        decided = f"The plan's minimum of 100 cases on at least 60 distinct days is not reached ({n_cases} cases on {n_days} days)."
    elif (slope > 0 and slope_t >= 2) or (mean_u is not None and mean_u < 0 and t_u <= -2):
        status = "rejected"
        if slope > 0 and slope_t >= 2:
            decided = "Reject rule: the slope is positive with t >= +2."
        else:
            decided = "Reject rule: the mean short-side unusual move is below 0 with t <= -2."
    elif slope < 0 and slope_t <= -2 and support_passed:
        status = "confirmed"
        decided = "Confirm rule: the slope is negative with t <= -2 and the mean short-side unusual move is above 0."
    else:
        status = "inconclusive"
        if slope_t <= -2:
            decided = "Inconclusive rule: slope t <= -2 but the mean short-side unusual move is not above 0."
        else:
            decided = "Inconclusive rule: the slope t lies between -2 and +2."

    return {
        "status": status,
        "situation_check": situation,
        "main_measure": main,
        "supporting_check": supporting,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
