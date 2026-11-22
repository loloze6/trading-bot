import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 84
    RAW = "debug_info.components.fall_depth.last_history_value"

    # ---------- 1. Situation check: a 24-hour (6-bar) fall, expected side long ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            fc = pd.to_numeric(d["forecast"], errors="coerce")
            close = pd.to_numeric(d["close"], errors="coerce")
            ret6 = close / close.shift(6) - 1.0
            if RAW in d.columns:
                raw = pd.to_numeric(d[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=d.index)
            # Raw value where recorded; recompute the sign from prices otherwise.
            fall = pd.Series(np.where(raw.notna(), raw < 0, ret6 < 0), index=d.index)
            fall_known = raw.notna() | ret6.notna()
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            n_agree += int((active & fall_known & fall.astype(bool) & (fc > 0)).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.90)

    main_name = "pooled OLS slope of 84-bar excess return (return minus coin's normal drift) on forecast"
    thr = "slope t >= 2 confirms (with supporting check), t <= -2 rejects, at least 200 cases"
    sup_name = "mean unusual move of cases with forecast > 0"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are bars where the last 6-bar "
                           "return fell with a long forecast, as the plan's situation requires."
                           if n_active > 0 else
                           "The forecast is never non-zero, so the plan's long-after-a-fall situation never appears."),
            "reading": "The situation is a negative raw component value (a 24-hour fall), recomputed from the 6-bar price return where the raw value is missing; the side is long.",
        }

    # ---------- 2. Criterion ----------
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").values
            fc = pd.to_numeric(d["forecast"], errors="coerce").values
            n = len(d)
            for t in range(0, n, H):
                if t + H >= n:
                    break
                c0, c1 = close[t], close[t + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                rows.append((coin, c1 / c0 - 1.0, fc[t]))
    s = pd.DataFrame(rows, columns=["coin", "ret", "fc"])

    if len(s) > 0:
        drift = s.groupby("coin")["ret"].transform("mean")
        s["excess"] = s["ret"] - drift
    else:
        s["excess"] = []
    s = s.dropna(subset=["excess", "fc"])

    n_cases = int(len(s))
    pos = s[s["fc"] > 0]
    n_pos = int(len(pos))

    slope = None
    tval = None
    if n_cases >= 3 and s["fc"].nunique() > 1:
        res = stats.linregress(s["fc"].values.astype(float), s["excess"].values.astype(float))
        slope = float(res.slope)
        tval = float(res.slope / res.stderr) if res.stderr and res.stderr > 0 else None

    sup_val = float(pos["excess"].mean()) if n_pos > 0 else None
    sup_pass = (bool(sup_val > 0) if sup_val is not None else None)

    counts = {"cases": n_cases, "cases with forecast above 0": n_pos}

    if n_cases < 200:
        status = "not observable"
        decided = f"Only {n_cases} cases, fewer than the plan's minimum of 200."
    elif tval is None:
        status = "inconclusive"
        decided = "The slope's t cannot be computed (the forecast does not vary over the cases), which meets neither the confirm nor the reject rule."
    elif tval >= 2 and sup_pass:
        status = "confirmed"
        decided = "The slope's t is 2 or more, the cases with forecast above 0 have a mean unusual move above 0, with at least 200 cases."
    elif tval <= -2:
        status = "rejected"
        decided = "The slope's t is -2 or less, with at least 200 cases."
    elif tval >= 2:
        status = "inconclusive"
        decided = "The slope's t is 2 or more but the mean unusual move of the cases with forecast above 0 is not above 0."
    else:
        status = "inconclusive"
        decided = "The slope's t is between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": slope,
            "statistic": ({"name": "OLS slope t", "value": tval} if tval is not None else None),
            "threshold": thr,
        },
        "supporting_check": {"name": sup_name, "value": sup_val, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": ("The 200-case minimum is read as the number of pooled grid samples in the regression. Each coin's normal drift is its mean 84-bar return over the grid samples of all its windows. A grid bar whose 84-bar end falls outside its window is left out."),
    }
