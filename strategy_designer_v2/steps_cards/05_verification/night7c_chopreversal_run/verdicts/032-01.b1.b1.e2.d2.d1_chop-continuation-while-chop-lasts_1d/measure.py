import numpy as np
import pandas as pd


def measure(bars):
    H = 7
    ER_N = 30
    ER_THR = 0.3

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df.sort_values("timestamp").reset_index(drop=True)
            c = pd.to_numeric(d["close"], errors="coerce")
            f = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0)
            net = (c - c.shift(ER_N)).abs()
            path = c.diff().abs().rolling(ER_N, min_periods=ER_N).sum()
            er = net / path.replace(0, np.nan)
            p7 = c / c.shift(7) - 1.0
            p30 = c / c.shift(30) - 1.0
            computable = er.notna() & p7.notna() & p30.notna()
            situ = (er < ER_THR) & (((p7 > 0) & (p30 > 0)) | ((p7 < 0) & (p30 < 0)))
            side = np.sign(p7)
            active = (f != 0) & computable
            agree = active & situ & (np.sign(f) == side)
            n_active += int(active.sum())
            n_agree += int(agree.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    reading = ("The 30-bar efficiency ratio, 7- and 30-bar returns are recomputed from closes inside each window, "
               "bars without 30 prior bars in the window are left out of the agreement; a case is a grid bar "
               "(positions 0,7,14,... of each window) with non-zero forecast and a 7-bar forward return inside the "
               "window, the coin's mean 7-bar return is the mean over all its windows' grid returns, the t is the "
               "weighted mean over a day-clustered standard error (weighted deviations summed per day), and the "
               "supporting check splits cases into |forecast| above the median versus at or below it, comparing "
               "unweighted mean signed excess returns.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars checked": int(n_active)},
            "decided_by": ("Fewer than 90% of active bars are bars where the 30-bar efficiency ratio is below 0.3 "
                           "with 7- and 30-bar returns of the same sign and the forecast on that sign's side."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin, wins in bars.items():
        grid_rets = []
        cand = []
        for w, df in wins.items():
            d = df.sort_values("timestamp").reset_index(drop=True)
            c = pd.to_numeric(d["close"], errors="coerce").values
            f = pd.to_numeric(d["forecast"], errors="coerce").values
            ts = pd.to_datetime(d["timestamp"], utc=True)
            n = len(d)
            for i in range(0, n, H):
                if i + H >= n:
                    continue
                if not (np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] > 0):
                    continue
                r = c[i + H] / c[i] - 1.0
                grid_rets.append(r)
                if np.isfinite(f[i]) and f[i] != 0:
                    cand.append((ts.iloc[i].floor("D"), r, f[i]))
        if not grid_rets:
            continue
        mu = float(np.mean(grid_rets))
        for day, r, fv in cand:
            rows.append({"day": day, "x": (r - mu) * np.sign(fv), "w": abs(fv)})

    cases = pd.DataFrame(rows, columns=["day", "x", "w"])
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0

    m = None
    t = None
    if n_cases > 0 and cases["w"].sum() > 0:
        W = cases["w"].sum()
        m = float((cases["w"] * cases["x"]).sum() / W)
        cases["dev"] = cases["w"] * (cases["x"] - m)
        s = cases.groupby("day")["dev"].sum().values
        G = len(s)
        if G > 1:
            se = np.sqrt(G / (G - 1) * np.sum(s ** 2)) / W
            t = float(m / se) if se > 0 else None

    supp = None
    if n_cases >= 2:
        med = cases["w"].median()
        up = cases.loc[cases["w"] > med, "x"]
        lo = cases.loc[cases["w"] <= med, "x"]
        if len(up) > 0 and len(lo) > 0:
            supp = float(up.mean() - lo.mean())
    supp_pass = None if supp is None else bool(supp > 0)

    if n_cases < 50:
        status = "not observable"
        decided = f"The plan's minimum of 50 cases is not reached ({n_cases} cases)."
    elif m is None or t is None:
        status = "inconclusive"
        decided = "The weighted mean or its t could not be computed, so neither confirm nor reject is met."
    elif m > 0 and t >= 2 and supp_pass:
        status = "confirmed"
        decided = "The weighted mean is positive with t >= 2 and the upper-minus-lower half difference is above 0."
    elif m < 0 and t <= -2:
        status = "rejected"
        decided = "The weighted mean is negative with t <= -2."
    elif t >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the supporting check is at or below 0 (or missing), which the plan calls inconclusive."
    else:
        status = "inconclusive"
        decided = "t lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "|forecast|-weighted mean signed 7-bar excess return",
            "value": m,
            "statistic": None if t is None else {"name": "t of the weighted mean, cases summed per day", "value": t},
            "threshold": "confirm: positive with t >= 2 and supporting check > 0; reject: negative with t <= -2",
        },
        "supporting_check": {
            "name": "upper-half minus lower-half mean signed excess return (split at median |forecast|)",
            "value": supp,
            "passed": supp_pass,
        },
        "counts": {"cases": n_cases, "days": n_days},
        "decided_by": decided,
        "reading": reading,
    }
