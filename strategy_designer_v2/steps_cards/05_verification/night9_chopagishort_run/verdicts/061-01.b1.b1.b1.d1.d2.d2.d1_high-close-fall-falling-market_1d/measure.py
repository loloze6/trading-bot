import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    BAND = 2.0
    FCOL = "forecast"
    LHV = "debug_info.components.fall5.last_history_value"

    # ---------- scale of PriceEvolutionComponent (percent vs fraction) ----------
    ratios = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            if LHV not in df.columns:
                continue
            c = df["close"].astype(float).reset_index(drop=True)
            r5 = c / c.shift(5) - 1.0
            lhv = pd.to_numeric(df[LHV], errors="coerce").reset_index(drop=True)
            m = lhv.notna() & r5.notna() & (r5.abs() > 1e-6)
            if m.any():
                ratios.extend((lhv[m] / r5[m]).tolist())
    scale = 100.0
    if len(ratios) >= 10:
        med = float(np.median(ratios))
        if np.isfinite(med) and med > 0:
            scale = 100.0 if abs(med - 100.0) < abs(med - 1.0) else 1.0

    # ---------- situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df.reset_index(drop=True)
            c = d["close"].astype(float)
            hi = d["high"].astype(float)
            lo = d["low"].astype(float)
            rng = hi - lo
            cl = (c - lo) / rng.where(rng > 0)
            pe5 = (c / c.shift(5) - 1.0) * scale
            if LHV in d.columns:
                lhv = pd.to_numeric(d[LHV], errors="coerce")
                pe5 = lhv.where(lhv.notna(), pe5)
            pe60 = (c / c.shift(60) - 1.0) * scale
            f = pd.to_numeric(d[FCOL], errors="coerce").fillna(0.0)
            active = f != 0
            known = cl.notna() & pe5.notna() & pe60.notna()
            sit = (cl >= 0.75) & (pe5 < 0) & (pe60 < -10)
            sel = active & known
            n_active += int(sel.sum())
            n_agree += int((sel & sit & (f < 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9

    reading = ("The 5-day return is the recorded fall5 raw value where present (else recomputed from closes), "
               "the falling profile is the 60-bar return below -10 % recomputed inside each window, and active bars whose "
               "60-bar return cannot be computed (first 60 bars of a window) are left out of the agreement; a case is the "
               "first short bet (rise of the short forecast by >= 2 points from its low since the last bet) in each 5-bar "
               "grid cell counted from the window's first row, cases whose 5-bar return leaves the window are dropped, the "
               "day-clustered t uses the G/(G-1) correction, and fewer than 30 distinct case days gives 'not observable'.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars checked": int(n_active)},
            "decided_by": ("Fewer than 90 % of active bars are short bars with close location >= 0.75, a negative "
                           "5-day return and a 60-bar return below -10 %." if n_active > 0 else
                           "No active bar with a computable situation was found."),
            "reading": reading,
        }

    # ---------- drift per coin ----------
    drift = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            c = df["close"].astype(float).to_numpy()
            for i in range(0, len(c) - H, H):
                if c[i] > 0 and np.isfinite(c[i]) and np.isfinite(c[i + H]):
                    rets.append(c[i + H] / c[i] - 1.0)
        drift[coin] = float(np.mean(rets)) if rets else np.nan

    # ---------- cases ----------
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df.reset_index(drop=True)
            c = d["close"].astype(float).to_numpy()
            f = pd.to_numeric(d[FCOL], errors="coerce").fillna(0.0).to_numpy()
            ts = pd.to_datetime(d["timestamp"], utc=True)
            n = len(d)
            bet = np.zeros(n, dtype=bool)
            ref = 0.0
            for i in range(n):
                s = -f[i] if f[i] < 0 else 0.0
                if s <= 0:
                    ref = 0.0
                    continue
                ref = min(ref, s)
                if s - ref >= BAND:
                    bet[i] = True
                    ref = s
            for start in range(0, n, H):
                idx = [i for i in range(start, min(start + H, n)) if bet[i]]
                if not idx:
                    continue
                t = idx[0]
                if t + H >= n:
                    continue
                if not (np.isfinite(c[t]) and np.isfinite(c[t + H]) and c[t] > 0):
                    continue
                dr = drift.get(coin, np.nan)
                if not np.isfinite(dr):
                    continue
                r = c[t + H] / c[t] - 1.0
                u = -(r - dr)
                rows.append({"day": ts.iloc[t].strftime("%Y-%m-%d"), "u": u, "size": abs(f[t])})

    cases = pd.DataFrame(rows, columns=["day", "u", "size"])
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0
    counts = {"cases": n_cases, "distinct days with cases": n_days}

    mean_u = float(cases["u"].mean()) if n_cases else None
    t_val = None
    if n_cases >= 2 and n_days >= 2:
        dev = cases["u"] - mean_u
        D = dev.groupby(cases["day"]).sum()
        G = len(D)
        var = (G / (G - 1)) * float((D ** 2).sum()) / (n_cases ** 2)
        se = np.sqrt(var)
        t_val = float(mean_u / se) if se > 0 else None
    slope = None
    if n_cases >= 3 and cases["size"].nunique() > 1:
        slope = float(stats.linregress(cases["size"].to_numpy(), cases["u"].to_numpy()).slope)

    main = {
        "name": "mean short-direction unusual 5-bar move over cases",
        "value": mean_u,
        "statistic": {"name": "t of the mean, cases of one day summed", "value": t_val} if t_val is not None else None,
        "threshold": "confirm: mean > 0 with t >= 2 and slope > 0; reject: mean < 0 with t <= -2",
    }
    sc_passed = None if slope is None else bool(slope > 0)
    supporting = {"name": "OLS slope of unusual move on |forecast|", "value": slope, "passed": sc_passed}

    if n_days < 30:
        status = "not observable"
        decided = f"Cases fall on {n_days} distinct days, below the plan's minimum of 30."
    elif t_val is None:
        status = "inconclusive"
        decided = "The t of the mean could not be computed, so neither the confirm nor the reject rule is met."
    elif mean_u > 0 and t_val >= 2 and sc_passed:
        status = "confirmed"
        decided = "The mean short-direction unusual move is above 0 with t >= 2 and the slope is above 0."
    elif mean_u < 0 and t_val <= -2:
        status = "rejected"
        decided = "The mean short-direction unusual move is below 0 with t <= -2."
    elif t_val >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the slope is at or below 0 (or undefined), which the plan calls inconclusive."
    else:
        status = "inconclusive"
        decided = "t lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": supporting,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
