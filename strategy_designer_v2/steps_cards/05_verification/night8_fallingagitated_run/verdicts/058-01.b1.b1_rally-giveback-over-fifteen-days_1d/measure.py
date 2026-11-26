import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 15
    RAW = "debug_info.components.scaled_rise.last_history_value"

    # ---------- 1. situation check: active bars must be 3-day rises, on the short side ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            close = pd.to_numeric(df["close"], errors="coerce")
            ret3 = close / close.shift(3) - 1.0
            raw = pd.to_numeric(df[RAW], errors="coerce") if RAW in df.columns else pd.Series(np.nan, index=df.index)
            active = fc.notna() & (fc != 0)
            for i in np.where(active.values)[0]:
                n_active += 1
                r = raw.iloc[i]
                if pd.notna(r):
                    rise = r > 0
                else:
                    r3 = ret3.iloc[i]
                    rise = bool(pd.notna(r3) and r3 > 0)
                if rise and fc.iloc[i] < 0:
                    n_agree += 1
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "OLS slope of 15-bar return minus normal drift on forecast (grid bars, forecast < 0)"
    thr = "slope > 0 with t >= 2 on >= 30 cases confirms; slope < 0 with t <= -2 on >= 30 cases rejects"
    sup_name = "mean share given back, top half of |forecast| minus bottom half"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "agreeing bars": int(n_agree)},
            "decided_by": ("fewer than 90% of the bars with a non-zero forecast are short positions after a 3-day rise "
                           "(positive scaled 3-day return), as the plan's situation requires"
                           if n_active > 0 else "the record holds no bar with a non-zero forecast"),
            "reading": "the situation is a positive raw scaled 3-day return (or positive 3-day price return where the raw value is missing) with a negative forecast; the profile is the code's and is not re-checked",
        }

    # ---------- 2. criterion ----------
    # normal drift per coin: mean of non-overlapping 15-bar returns over all windows
    drift = {}
    rows = []
    for coin, wins in bars.items():
        allret = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            n = len(df)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                if not (np.isfinite(close[i]) and np.isfinite(close[i + H]) and close[i] > 0):
                    continue
                r = close[i + H] / close[i] - 1.0
                allret.append(r)
                if np.isfinite(fc[i]) and fc[i] < 0:
                    rise3 = np.nan
                    if i >= 3 and np.isfinite(close[i - 3]) and close[i - 3] > 0:
                        rise3 = close[i] / close[i - 3] - 1.0
                    rows.append((coin, fc[i], r, rise3))
        drift[coin] = float(np.mean(allret)) if allret else np.nan

    cases = pd.DataFrame(rows, columns=["coin", "f", "r", "rise3"])
    if len(cases):
        cases["d"] = cases["coin"].map(drift)
        cases["y"] = cases["r"] - cases["d"]
        cases = cases[np.isfinite(cases["y"]) & np.isfinite(cases["f"])]
    n_cases = int(len(cases))

    slope = None
    tval = None
    if n_cases >= 3 and cases["f"].nunique() > 1:
        lr = stats.linregress(cases["f"].values, cases["y"].values)
        slope = float(lr.slope)
        tval = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    # supporting check
    sup_val = None
    sup_pass = None
    if n_cases > 0:
        s = cases[np.isfinite(cases["rise3"]) & (cases["rise3"] > 0)].copy()
        s["share"] = -s["r"] / s["rise3"]
        s["af"] = s["f"].abs()
        s = s.sort_values("af", kind="mergesort").reset_index(drop=True)
        k = len(s) // 2
        if k >= 1:
            bottom = s.iloc[:k]["share"].mean()
            top = s.iloc[len(s) - k:]["share"].mean()
            sup_val = float(top - bottom)
            sup_pass = bool(sup_val > 0)

    reading = ("cases are grid bars (0,15,30,... of each window) with forecast < 0 and a 15-bar return inside the window; "
               "drift is the coin's mean non-overlapping 15-bar return over all its windows; slope t is the OLS slope over its standard error; "
               "the share check keeps cases with a positive 3-day price rise ending at the signal bar and splits them by |forecast| rank into lower and upper n//2 (middle case dropped if odd); "
               "the plan's 'fewer than 30 cases' is applied as the minimum count, giving 'not observable'.")

    out = {
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": slope,
                         "statistic": ({"name": "OLS slope t", "value": tval} if tval is not None else None),
                         "threshold": thr},
        "supporting_check": {"name": sup_name, "value": sup_val, "passed": sup_pass},
        "counts": {"cases": n_cases},
        "reading": reading,
    }

    if n_cases < 30:
        out["status"] = "not observable"
        out["decided_by"] = f"only {n_cases} cases, below the plan's minimum of 30"
        return out
    if tval is None:
        out["status"] = "inconclusive"
        out["decided_by"] = "the slope's t could not be computed, so neither the confirm nor the reject rule is met"
        return out
    if slope > 0 and tval >= 2:
        if sup_pass:
            out["status"] = "confirmed"
            out["decided_by"] = "the slope is positive with t >= 2 on at least 30 cases and the share given back is larger in the top half of |forecast|"
        else:
            out["status"] = "inconclusive"
            out["decided_by"] = "the slope confirms (t >= 2 on at least 30 cases) but the share-given-back check fails"
        return out
    if slope < 0 and tval <= -2:
        out["status"] = "rejected"
        out["decided_by"] = "the slope is negative with t <= -2 on at least 30 cases"
        return out
    out["status"] = "inconclusive"
    out["decided_by"] = "the slope's t is between -2 and 2 on at least 30 cases"
    return out
