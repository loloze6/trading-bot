import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 7
    MIN_CASES = 30
    RAW = "debug_info.components.fall30.last_history_value"
    POST = "debug_info.components.fall30.post_pipeline_value"

    # ---------- 1. Situation check ----------
    # Situation: choppy agitated profile (the detector's regime "unknown", the only
    # regime not vetoed to chop) and a 30-day fall (raw 30-bar return < 0); side: short.
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            active = fc.notna() & (fc != 0)
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            # recompute the 30-bar percent return from prices where the record lacks it
            close = pd.to_numeric(df["close"], errors="coerce")
            ret30 = (close / close.shift(30) - 1.0) * 100.0
            raw = raw.where(raw.notna(), ret30)
            profile = df["regime"].astype(str) == "unknown"
            situ = profile & (raw < 0) & (fc < 0)
            n_active += int(active.sum())
            n_agree += int((active & situ).sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = True if agreement is None else bool(agreement >= 0.9)

    main_name = "OLS slope of 7-bar forward return minus coin drift on fall30 post_pipeline_value"
    threshold = "confirm: slope > 0 with t >= 2 and mean short unusual move > 0; reject: slope < 0 with t <= -2"
    reading = ("The choppy agitated profile is read from the recorded regime ('unknown', the only regime the "
               "detector does not veto to chop) and the fall from the raw 30-bar return (recomputed from closes "
               "where missing); cases are grid bars (positions 0,7,14,... of each window, forward return inside the "
               "window) with forecast < 0, regressed on fall30's post_pipeline_value, with each coin's drift as the "
               "mean 7-bar return on the same grid over all its windows; the plan's 30-case minimum gives "
               "'not observable' when unmet.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "independent grid cases with a forecast below 0": None},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are short bars in the choppy "
                           "agitated profile after a 30-day fall."),
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    xs, ys = [], []
    for coin, wins in bars.items():
        grid_rets = []
        grid_rows = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            if POST in df.columns:
                post = pd.to_numeric(df[POST], errors="coerce").values
            else:
                post = np.full(len(df), np.nan)
            n = len(df)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                grid_rets.append(r)
                grid_rows.append((r, fc[i], post[i]))
        if not grid_rets:
            continue
        drift = float(np.mean(grid_rets))
        for r, f, p in grid_rows:
            if np.isfinite(f) and f < 0 and np.isfinite(p):
                xs.append(float(p))
                ys.append(r - drift)

    n_cases = len(xs)
    counts = {"independent grid cases with a forecast below 0": int(n_cases)}
    sit = {"agreement": None if agreement is None else float(agreement), "passed": True}

    if n_cases < MIN_CASES:
        return {
            "status": "not observable",
            "situation_check": sit,
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": {"name": "mean short unusual move (minus excess return)", "value": None,
                                 "passed": None},
            "counts": counts,
            "decided_by": f"Only {n_cases} independent grid cases with a forecast below 0, under the plan's minimum of 30.",
            "reading": reading,
        }

    x = np.array(xs)
    y = np.array(ys)
    sup_val = float(np.mean(-y))
    sup_pass = bool(sup_val > 0)

    if np.std(x) == 0:
        slope, t = None, None
    else:
        lr = stats.linregress(x, y)
        slope = float(lr.slope)
        t = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else (
            float(np.sign(lr.slope) * np.inf) if lr.slope != 0 else 0.0)

    if slope is None:
        status = "inconclusive"
        decided = "The forecast does not vary across the cases, so no slope can be measured; neither rule is met."
    elif slope > 0 and t >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "The slope is above 0 with t >= 2 and the mean short unusual move is above 0 (confirm rule)."
        else:
            status = "inconclusive"
            decided = "The slope confirms (above 0, t >= 2) but the supporting check's mean short unusual move is not above 0."
    elif slope < 0 and t <= -2:
        status = "rejected"
        decided = "The slope is below 0 with t <= -2: deeper falls are followed by excess rises (reject rule)."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and 2 (inconclusive rule)."

    return {
        "status": status,
        "situation_check": sit,
        "main_measure": {"name": main_name, "value": slope,
                         "statistic": None if t is None else {"name": "ordinary OLS slope t", "value": t},
                         "threshold": threshold},
        "supporting_check": {"name": "mean short unusual move (minus excess return)", "value": sup_val,
                             "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
