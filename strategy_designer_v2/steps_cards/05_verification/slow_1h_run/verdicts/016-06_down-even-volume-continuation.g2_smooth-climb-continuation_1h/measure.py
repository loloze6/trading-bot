import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 72
    FC_COL = "debug_info.components.er72.post_pipeline_value"

    # ---------- 1. Situation check: rise over 72 bars (ret72 > 0) -> long ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float).values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            reg = df["regime"].astype(str).values
            n = len(df)
            ret72 = np.full(n, np.nan)
            if n > H:
                ret72[H:] = close[H:] / close[:-H] - 1.0
            for i in range(n):
                f = fc[i]
                if not np.isfinite(f) or f == 0:
                    continue
                n_active += 1
                if np.isfinite(ret72[i]):
                    in_sit = ret72[i] > 0
                else:
                    # first 72 bars of a window: prior prices not recorded,
                    # use the detector's own decision of the same rule
                    in_sit = reg[i] == "trending"
                if in_sit and f > 0:
                    n_agree += 1
    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    reading = ("The coin's mean 72-bar return is the mean of the forward 72-bar returns on every grid bar "
               "(positions 0, 72, 144, ... of each window, all regimes) over all its windows; the slope's t is the "
               "OLS slope over its standard error with the pooled trending grid cases; the top and bottom thirds are "
               "the floor(n/3) highest and lowest forecasts by sort order; the plan's 'fewer than 100 independent "
               "trending grid cases' is treated as the minimum count (not observable); for the situation check, "
               "ret72 is recomputed from closes and, on a window's first 72 bars where it cannot be, the recorded "
               "regime is used.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": "OLS slope of forward 72-bar excess return on er72 forecast",
                             "value": None, "statistic": None,
                             "threshold": "t >= 2 confirms, t <= -2 rejects"},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of bars with a nonzero forecast are long bars where the 72-bar "
                           "price change is above 0, as the plan's situation requires."),
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    xs, ys_raw, coins_of = [], [], []
    coin_means = {}
    for coin, wins in bars.items():
        all_fwd = []
        rows = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float).values
            n = len(df)
            reg = df["regime"].astype(str).values
            fcv = (pd.to_numeric(df[FC_COL], errors="coerce").values
                   if FC_COL in df.columns else np.full(n, np.nan))
            for i in range(0, n, H):
                if i + H >= n:
                    break
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                fwd = c1 / c0 - 1.0
                all_fwd.append(fwd)
                if reg[i] == "trending" and np.isfinite(fcv[i]):
                    rows.append((fcv[i], fwd))
        if len(all_fwd) == 0:
            continue
        m = float(np.mean(all_fwd))
        coin_means[coin] = m
        for f, r in rows:
            xs.append(f)
            ys_raw.append(r - m)
            coins_of.append(coin)

    x = np.asarray(xs, dtype=float)
    y = np.asarray(ys_raw, dtype=float)
    n_cases = int(len(x))
    counts = {"independent trending grid cases": n_cases}

    main = {"name": "OLS slope of forward 72-bar excess return on er72 forecast (pooled trending grid bars)",
            "value": None, "statistic": None,
            "threshold": "slope t >= 2 confirms (with top-minus-bottom third > 0); t <= -2 rejects"}

    if n_cases < 100:
        return {
            "status": "not observable",
            "situation_check": {"agreement": float(agreement), "passed": True},
            "main_measure": main,
            "supporting_check": {"name": "top-third minus bottom-third mean excess return",
                                 "value": None, "passed": None},
            "counts": counts,
            "decided_by": f"Only {n_cases} independent trending grid cases, below the plan's minimum of 100.",
            "reading": reading,
        }

    if np.std(x) > 0:
        lr = stats.linregress(x, y)
        slope = float(lr.slope)
        t = float(lr.slope / lr.stderr) if lr.stderr > 0 else float("nan")
    else:
        slope, t = float("nan"), float("nan")
    main["value"] = slope if np.isfinite(slope) else None
    main["statistic"] = {"name": "OLS slope t", "value": t if np.isfinite(t) else None}

    order = np.argsort(x, kind="mergesort")
    k = n_cases // 3
    bottom = y[order[:k]]
    top = y[order[n_cases - k:]]
    diff = float(np.mean(top) - np.mean(bottom)) if k > 0 else float("nan")
    sup_pass = bool(np.isfinite(diff) and diff > 0)
    supporting = {"name": "top-third minus bottom-third mean forward 72-bar excess return",
                  "value": diff if np.isfinite(diff) else None, "passed": sup_pass}
    counts["top third cases"] = int(k)
    counts["bottom third cases"] = int(k)

    if np.isfinite(t) and t >= 2 and sup_pass:
        status = "confirmed"
        decided = f"Slope t = {t:.2f} >= 2 and top-minus-bottom third = {diff:.5f} > 0 meet the confirm rule."
    elif np.isfinite(t) and t <= -2:
        status = "rejected"
        decided = f"Slope t = {t:.2f} <= -2 meets the reject rule (smoother climbs continue less)."
    elif np.isfinite(t) and t >= 2:
        status = "inconclusive"
        decided = f"Slope t = {t:.2f} >= 2 but top-minus-bottom third = {diff:.5f} <= 0, inconclusive per the plan."
    else:
        status = "inconclusive"
        decided = f"Slope t = {t:.2f} lies between -2 and 2, inconclusive per the plan."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": main,
        "supporting_check": supporting,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
