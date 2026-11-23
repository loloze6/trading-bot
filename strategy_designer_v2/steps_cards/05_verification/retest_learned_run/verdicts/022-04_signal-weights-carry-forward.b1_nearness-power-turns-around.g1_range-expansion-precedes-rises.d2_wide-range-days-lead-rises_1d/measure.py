import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    RAW = "debug_info.components.range_excess.last_history_value"

    # ---------- 1. Situation check ----------
    # Fidelity: situation = today's range above its 30-day mean range (ratio - 1 > 0),
    # i.e. raw compression value (1 - ratio) < 0; expected side: long (outcome is a rise).
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            rng = (pd.to_numeric(df["high"], errors="coerce")
                   - pd.to_numeric(df["low"], errors="coerce"))
            ratio_px = rng / rng.rolling(30, min_periods=30).mean()
            raw_px = 1.0 - ratio_px
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
                raw = raw.where(raw.notna(), raw_px)
            else:
                raw = raw_px
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            agree = active & (raw < 0) & (fc > 0)
            n_agree += int(agree.sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "OLS slope of excess 5-bar return on forecast (forecast > 0 grid cases, pooled)"
    main_thr = "slope t >= 2 confirms (with mean excess t >= 1 and >= 200 cases); slope t <= -2 rejects"
    sup_name = "mean excess 5-bar return of the same cases, ordinary t >= 1"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None,
                             "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "agreeing bars": int(n_agree)},
            "decided_by": ("Fewer than 90% of bars with a non-zero forecast are long bars on which "
                           "today's high-low range exceeds its 30-day mean range, as the Fidelity states."),
            "reading": "Situation taken as raw compression value below 0 (range ratio above 1), side long; raw value recomputed from prices only where not recorded.",
        }

    # ---------- 2. Criterion ----------
    xs, ys = [], []
    for coin, wins in bars.items():
        grid_rets = []
        grid_fc = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            n = len(df)
            for p in range(0, n - H, H):
                c0, c1 = close[p], close[p + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                grid_rets.append(c1 / c0 - 1.0)
                grid_fc.append(fc[p])
        if not grid_rets:
            continue
        grid_rets = np.asarray(grid_rets, float)
        grid_fc = np.asarray(grid_fc, float)
        drift = float(np.mean(grid_rets))
        sel = np.isfinite(grid_fc) & (grid_fc > 0)
        xs.extend(grid_fc[sel].tolist())
        ys.extend((grid_rets[sel] - drift).tolist())

    x = np.asarray(xs, float)
    y = np.asarray(ys, float)
    n_cases = int(len(x))
    counts = {"grid cases with forecast > 0": n_cases}

    slope = slope_t = None
    if n_cases >= 3 and np.std(x) > 0:
        lr = stats.linregress(x, y)
        slope = float(lr.slope)
        slope_t = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    mean_ex = mean_t = None
    if n_cases >= 2:
        mean_ex = float(np.mean(y))
        sd = float(np.std(y, ddof=1))
        mean_t = float(mean_ex / (sd / np.sqrt(n_cases))) if sd > 0 else None
    sup_pass = None if mean_t is None else bool(mean_t >= 1.0)

    reading = ("Grid per window at positions 0,5,10,... with the 5-bar return inside the window; "
               "normal drift = mean 5-bar return over all grid cells of all the coin's windows; "
               "the plan's 'fewer than 200 cases' rule is reported as 'not observable' per the workflow's minimum-count rule.")

    if n_cases < 200:
        status = "not observable"
        decided = f"Only {n_cases} grid cases with forecast > 0, below the plan's minimum of 200."
    elif slope_t is None:
        status = "inconclusive"
        decided = "The slope t could not be computed (no variation in the forecast), so neither rule is met."
    elif slope_t >= 2 and sup_pass:
        status = "confirmed"
        decided = "Slope t >= 2, mean excess return t >= 1, with at least 200 cases: the confirm rule."
    elif slope_t <= -2:
        status = "rejected"
        decided = "Slope t <= -2 with at least 200 cases: the reject rule."
    elif slope_t >= 2:
        status = "inconclusive"
        decided = "Slope t >= 2 but the mean excess return t is below 1: inconclusive per the plan."
    else:
        status = "inconclusive"
        decided = "Slope t between -2 and 2: inconclusive per the plan."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": slope,
                         "statistic": None if slope_t is None else {"name": "OLS slope t", "value": slope_t},
                         "threshold": main_thr},
        "supporting_check": {"name": sup_name, "value": mean_t, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
