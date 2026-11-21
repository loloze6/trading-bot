import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 20
    FC = "forecast"
    RAW = "debug_info.components.ret60.last_history_value"

    # ---------- 1. Situation check: sign of the 60-day return = sign of forecast ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            if FC not in df.columns or "close" not in df.columns:
                continue
            fc = pd.to_numeric(df[FC], errors="coerce")
            close = pd.to_numeric(df["close"], errors="coerce")
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            # where the raw value is missing, recompute the 60-bar return inside the window
            recomputed = close / close.shift(60) - 1.0
            raw = raw.where(raw.notna(), recomputed)
            active = fc.notna() & (fc != 0) & raw.notna()
            n_active += int(active.sum())
            n_agree += int((np.sign(fc[active]) == np.sign(raw[active])).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "t of mean of forecast/10 x (20-bar return minus coin's normal 20-bar drift), non-overlapping grid"
    threshold = "confirm t >= 2 over at least 300 cases with supporting check passed; reject t <= -2 over at least 300 cases"
    sup_name = "mean unusual move in forecast's direction, larger minus smaller half of abs(forecast)"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"cases": 0},
            "decided_by": (
                "The plan's situation is a long after a 60-day rise and a short after a 60-day fall, "
                f"but only {agreement:.3f} of the active bars have a forecast sign equal to the 60-day return's sign (below 0.90)."
            ),
            "reading": "Agreement is the share of non-zero-forecast bars whose forecast sign equals the sign of the recorded 60-bar return (recomputed from closes inside the window where not recorded).",
        }

    # ---------- 2. Grid cases ----------
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df[FC], errors="coerce").values
            n = len(df)
            for t in range(0, n - H, H):
                c0, c1 = close[t], close[t + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                rows.append((coin, w, fc[t], c1 / c0 - 1.0))
    cases = pd.DataFrame(rows, columns=["coin", "window", "fc", "ret"])

    # coin's normal 20-bar drift: mean over all its windows' grid returns
    if len(cases):
        drift = cases.groupby("coin")["ret"].mean()
        cases["unusual"] = cases["ret"] - cases["coin"].map(drift)
    else:
        cases["unusual"] = []
    cases = cases[cases["fc"].notna() & cases["unusual"].notna()].copy()
    cases["val"] = cases["fc"] / 10.0 * cases["unusual"]
    n_cases = int(len(cases))

    mean_val = float(cases["val"].mean()) if n_cases > 0 else None
    t_val = None
    if n_cases > 1:
        sd = cases["val"].std(ddof=1)
        if sd > 0:
            t_val = float(mean_val / (sd / np.sqrt(n_cases)))

    # ---------- supporting check ----------
    sup = cases[cases["fc"] != 0].copy()
    sup_val = None
    sup_pass = None
    if len(sup) >= 2:
        sup["absfc"] = sup["fc"].abs()
        sup["dirmove"] = np.sign(sup["fc"]) * sup["unusual"]
        med = sup["absfc"].median()
        large = sup.loc[sup["absfc"] > med, "dirmove"]
        small = sup.loc[sup["absfc"] <= med, "dirmove"]
        if len(large) > 0 and len(small) > 0:
            sup_val = float(large.mean() - small.mean())
            sup_pass = bool(sup_val > 0)

    reading = ("All grid points (positions 0, 20, 40, ... of each window with a close 20 bars later) are cases, zero forecasts included in the main mean; "
               "the supporting split excludes zero-forecast cases (no direction) and puts abs(forecast) > median in the larger half, <= median in the smaller half; "
               "fewer than 300 cases is treated as not observable per the minimum-count rule.")

    # ---------- decision ----------
    if n_cases < 300:
        status = "not observable"
        decided = f"Only {n_cases} grid cases, below the plan's minimum of 300."
    elif t_val is None:
        status = "inconclusive"
        decided = "The main measure's t could not be computed (no variation), so neither confirm nor reject rule is met."
    elif t_val >= 2 and sup_pass is True:
        status = "confirmed"
        decided = "Main-measure t >= 2 over at least 300 cases and the larger-minus-smaller difference is > 0."
    elif t_val <= -2:
        status = "rejected"
        decided = "Main-measure t <= -2 over at least 300 cases."
    elif t_val >= 2:
        status = "inconclusive"
        decided = "Main-measure t >= 2 but the supporting check failed, which the plan calls inconclusive."
    else:
        status = "inconclusive"
        decided = "Main-measure t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_val,
            "statistic": {"name": "t of the mean", "value": t_val} if t_val is not None else None,
            "threshold": threshold,
        },
        "supporting_check": {"name": sup_name, "value": sup_val, "passed": sup_pass},
        "counts": {"cases": n_cases},
        "decided_by": decided,
        "reading": reading,
    }
