import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    RAW = "debug_info.components.support_break.last_history_value"

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            raw = (pd.to_numeric(df[RAW], errors="coerce") if RAW in df.columns
                   else pd.Series(np.nan, index=df.index))
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            # Situation: close below a touched support level (raw depth x touches > 0); expected side long.
            agree = active & raw.notna() & (raw > 0) & (fc > 0)
            n_agree += int(agree.sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "mean unusual 5-bar return of the top-fifth forecast cases"
    threshold = "confirm: mean > 0 with t >= 2; reject: mean < 0 with t <= -2; at least 30 top-fifth cases"
    reading = ("Bars with a missing raw component value count as not in the situation; the top fifth is the "
               "grid cases whose forecast is at or above the 80th percentile of all positive-forecast grid cases "
               "pooled over coins and windows (ties included); the coin's mean 5-bar return is taken over all "
               "non-overlapping 5-bar grid returns of all its windows; cases without a full 5-bar return inside "
               "their window are left out.")

    if n_active > 0 and not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on long side": int(n_agree)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars where the close is "
                           "below a touched support level (raw component > 0), as the plan's situation requires."),
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    drift = {}
    cases = []  # (coin, forecast, ret)
    for coin, wins in bars.items():
        all_rets = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(d["forecast"], errors="coerce").to_numpy(dtype=float)
            n = len(d)
            for i in range(0, n, H):
                j = i + H
                if j >= n:
                    break
                c0, c1 = close[i], close[j]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                all_rets.append(r)
                if np.isfinite(fc[i]) and fc[i] > 0:
                    cases.append((coin, float(fc[i]), float(r)))
        drift[coin] = float(np.mean(all_rets)) if all_rets else np.nan

    n_cases = len(cases)
    if n_cases > 0:
        fcs = np.array([c[1] for c in cases])
        cut = float(np.quantile(fcs, 0.8))
        top = [c for c in cases if c[1] >= cut and np.isfinite(drift.get(c[0], np.nan))]
    else:
        top = []
    unusual = np.array([c[2] - drift[c[0]] for c in top], dtype=float)
    n_top = int(len(unusual))

    mean_u = float(np.mean(unusual)) if n_top > 0 else None
    t = None
    if n_top > 1:
        sd = float(np.std(unusual, ddof=1))
        if sd > 0:
            t = float(mean_u / (sd / np.sqrt(n_top)))

    counts = {"positive-forecast grid cases": int(n_cases), "top-fifth cases": n_top}
    sc = {"agreement": (float(agreement) if agreement is not None else None), "passed": passed}
    stat = {"name": "t of the mean", "value": t} if t is not None else None
    mm = {"name": main_name, "value": mean_u, "statistic": stat, "threshold": threshold}

    if n_top < 30:
        status = "not observable"
        decided = f"Only {n_top} top-fifth cases, fewer than the plan's minimum of 30."
    elif t is not None and mean_u > 0 and t >= 2:
        status = "confirmed"
        decided = "The mean unusual 5-bar return of the top-fifth cases is above 0 with t >= 2 on at least 30 cases."
    elif t is not None and mean_u < 0 and t <= -2:
        status = "rejected"
        decided = "The mean unusual 5-bar return of the top-fifth cases is below 0 with t <= -2 on at least 30 cases."
    else:
        status = "inconclusive"
        decided = "The t of the mean unusual 5-bar return of the top-fifth cases lies between -2 and 2."

    return {
        "status": status,
        "situation_check": sc,
        "main_measure": mm,
        "supporting_check": None,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
