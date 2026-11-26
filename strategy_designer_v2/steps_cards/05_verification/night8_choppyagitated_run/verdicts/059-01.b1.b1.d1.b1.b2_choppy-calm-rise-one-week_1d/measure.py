import numpy as np
import pandas as pd


def measure(bars):
    H = 7
    RAW = "debug_info.components.scaled_rise.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce")
            fc = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0)
            ret7 = close / close.shift(H) - 1.0
            if RAW in d.columns:
                raw = pd.to_numeric(d[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=d.index)
            rise = np.where(raw.notna(), raw > 0, ret7 > 0)
            calm = d["regime"].astype(str).values == "unknown"
            active = fc.values != 0
            situ = rise & calm & (fc.values > 0)
            n_active += int(active.sum())
            n_agree += int((active & situ).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)
    situation_check = {"agreement": agreement, "passed": passed}

    main_name = "clustered-by-day t of the slope of next-7-bar excess return on forecast (forecast > 0, 7-bar grid)"
    threshold = "confirm: slope t >= 2 and mean excess > 0; reject: slope t <= -2, or mean excess < 0 with t <= -2"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": situation_check,
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": "Fewer than 90% of the bars with a non-zero forecast are long bars after a 7-day rise in the choppy calm profile (regime 'unknown'), as the Fidelity's situation and side require.",
            "reading": "The choppy calm profile is read as the detector's default regime 'unknown' (no chop veto fired), and the rise as a positive raw scaled_rise value (or a positive 7-day close return where it is not recorded).",
        }

    # ---------- 2. criterion ----------
    rows = []
    drift_parts = {}
    for coin, wins in bars.items():
        allr = []
        for w, df in wins.items():
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").values
            fc = pd.to_numeric(d["forecast"], errors="coerce").values
            ts = pd.to_datetime(d["timestamp"], utc=True)
            n = len(d)
            for i in range(0, n, H):
                if i + H >= n:
                    continue
                r = close[i + H] / close[i] - 1.0
                if not np.isfinite(r):
                    continue
                allr.append(r)
                if np.isfinite(fc[i]) and fc[i] > 0:
                    rows.append((coin, ts.iloc[i].floor("D"), float(fc[i]), float(r)))
        drift_parts[coin] = float(np.mean(allr)) if len(allr) else np.nan

    cases = pd.DataFrame(rows, columns=["coin", "day", "f", "r"])
    if len(cases):
        cases["drift"] = cases["coin"].map(drift_parts)
        cases["y"] = cases["r"] - cases["drift"]
        cases = cases.dropna(subset=["y", "f"])
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0
    counts = {"grid cases with forecast > 0": n_cases, "distinct days": n_days}

    slope = None
    t_slope = None
    mean_ex = None
    t_mean = None
    if n_cases >= 3 and n_days >= 2:
        y = cases["y"].values
        X = np.column_stack([np.ones(n_cases), cases["f"].values])
        XtX = X.T @ X
        if np.linalg.matrix_rank(XtX) == 2:
            bread = np.linalg.inv(XtX)
            beta = bread @ X.T @ y
            u = y - X @ beta
            groups = cases["day"].values
            meat = np.zeros((2, 2))
            sc = pd.DataFrame(X * u[:, None], columns=["a", "b"])
            sc["g"] = groups
            S = sc.groupby("g")[["a", "b"]].sum().values
            for s in S:
                meat += np.outer(s, s)
            G = S.shape[0]
            c = (G / (G - 1)) * ((n_cases - 1) / (n_cases - 2))
            V = c * bread @ meat @ bread
            slope = float(beta[1])
            se = float(np.sqrt(V[1, 1])) if V[1, 1] > 0 else np.nan
            t_slope = float(slope / se) if np.isfinite(se) and se > 0 else None
        mean_ex = float(np.mean(y))
        dev = pd.Series(y - mean_ex).groupby(cases["day"].values).sum().values
        G = len(dev)
        se_m = np.sqrt(np.sum(dev ** 2) * G / (G - 1)) / n_cases
        t_mean = float(mean_ex / se_m) if se_m > 0 else None
    elif n_cases > 0:
        mean_ex = float(cases["y"].mean())

    sup_passed = None if mean_ex is None else bool(mean_ex > 0)

    if n_cases < 100 or n_days < 50:
        status = "not observable"
        decided = f"Minimum counts not reached: {n_cases} grid cases with forecast > 0 (need 100) and {n_days} distinct days (need 50)."
    elif t_slope is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif t_slope >= 2 and mean_ex is not None and mean_ex > 0:
        status = "confirmed"
        decided = "Confirm rule met: the slope's t is 2 or more and the mean excess return is above 0."
    elif t_slope <= -2:
        status = "rejected"
        decided = "Reject rule met: the slope's t is -2 or less."
    elif mean_ex is not None and mean_ex < 0 and t_mean is not None and t_mean <= -2:
        status = "rejected"
        decided = "Reject rule met: the mean excess return is below 0 with a t of -2 or less."
    elif t_slope >= 2:
        status = "inconclusive"
        decided = "The slope's t is 2 or more but the mean excess return is not above 0, so the supporting check fails: inconclusive."
    else:
        status = "inconclusive"
        decided = "Inconclusive rule: the slope's t is between -2 and 2 and the mean excess return is not below 0 with t <= -2."

    return {
        "status": status,
        "situation_check": situation_check,
        "main_measure": {
            "name": main_name,
            "value": t_slope,
            "statistic": None if t_slope is None else {"name": "OLS slope t, standard errors clustered by day", "value": t_slope},
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "mean excess 7-bar return over cases with forecast > 0",
            "value": mean_ex,
            "passed": sup_passed,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": "The slope is from an OLS with intercept whose t uses day-clustered (CR1) standard errors, the normal drift is each coin's mean 7-bar return on the non-overlapping grid of all its windows, the reject rule's mean-excess t is the day-clustered t of the mean, and the plan's 'inconclusive with too few cases' is reported as 'not observable' as the workflow requires.",
    }
