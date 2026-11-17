import numpy as np
import pandas as pd
from scipy import stats


def _component_series(df, comp_id, field="last_history_value"):
    """Return the recorded value of a strategy component as a float Series (NaN where not recorded)."""
    flat = f"debug_info.components.{comp_id}.{field}"
    if flat in df.columns:
        return pd.to_numeric(df[flat], errors="coerce")
    if "debug_info.components" in df.columns:
        def _get(x):
            if isinstance(x, dict):
                c = x.get(comp_id)
                if isinstance(c, dict):
                    v = c.get(field)
                    try:
                        return float(v)
                    except (TypeError, ValueError):
                        return np.nan
            return np.nan
        return df["debug_info.components"].apply(_get).astype(float)
    return pd.Series(np.nan, index=df.index, dtype=float)


def measure(bars):
    H = 30
    MIN_CASES = 30

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).to_numpy(dtype=float)
            regime = df["regime"].astype(str).to_numpy()
            n = len(df)
            # Necessary price condition: close above every prior in-window close (at most 365 back).
            above_prior = np.zeros(n, dtype=bool)
            for i in range(n):
                lo = max(0, i - 365)
                if i == 0:
                    above_prior[i] = True  # no in-window history to contradict it
                else:
                    prior = close[lo:i]
                    prior = prior[~np.isnan(prior)]
                    above_prior[i] = (not np.isnan(close[i])) and (prior.size == 0 or close[i] > prior.max())
            situation = above_prior & (regime == "trending")
            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc > 0)).sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.90

    reading = ("Situation bars are bars whose close exceeds every prior in-window close (up to 365 back) and whose "
               "recorded regime is 'trending' (the 365-close high itself needs warm-up history not in the record), "
               "expected side long; breakout bars for cases are regime 'trending' with a recorded volratio, a selected "
               "bar without close[t+30] in its window is not a case; the coin's mean 30-bar return is pooled over the "
               "non-overlapping grid (positions 0, 30, 60, ...) of all its windows; the top third is the ceil(n/3) "
               "cases with the largest volume ratio; the OLS t uses the usual slope standard error with n-2 df; "
               "fewer than 30 cases is reported as 'not observable' per the workflow's minimum-count rule.")

    main_name = "pooled OLS slope of 30-bar excess return on breakout volume ratio"
    threshold = "t >= 2 with >= 30 cases (and top-third mean excess > 0) confirms; t <= -2 with >= 30 cases rejects"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": n_active, "active bars in situation on long side": n_agree},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars where the close is above "
                           "the prior 365-close high, so the config does not trade the plan's breakout situation."),
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    xs, ys = [], []
    for coin, wins in bars.items():
        # coin's mean 30-bar return over all windows, non-overlapping grid
        grid_rets = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            for i in range(0, len(c) - H, H):
                r = c[i + H] / c[i] - 1.0
                if np.isfinite(r):
                    grid_rets.append(r)
        if len(grid_rets) == 0:
            continue
        coin_mean = float(np.mean(grid_rets))

        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            regime = df["regime"].astype(str).to_numpy()
            vr = _component_series(df, "volratio", "last_history_value").to_numpy(dtype=float)
            n = len(df)
            last = -10 ** 9
            for i in range(n):
                if regime[i] != "trending":
                    continue
                if i - last < H:
                    continue
                last = i
                if i + H >= n:
                    continue
                r = c[i + H] / c[i] - 1.0
                if not np.isfinite(r) or not np.isfinite(vr[i]):
                    continue
                xs.append(float(vr[i]))
                ys.append(float(r - coin_mean))

    x = np.asarray(xs, dtype=float)
    y = np.asarray(ys, dtype=float)
    n_cases = int(len(x))
    counts = {"non-overlapping breakout cases": n_cases}

    slope = None
    t_val = None
    if n_cases >= 3 and np.var(x) > 0:
        res = stats.linregress(x, y)
        slope = float(res.slope)
        t_val = float(res.slope / res.stderr) if res.stderr and res.stderr > 0 else None

    top_mean = None
    sup_pass = None
    if n_cases >= 1:
        k = int(np.ceil(n_cases / 3.0))
        order = np.argsort(-x, kind="mergesort")
        top_mean = float(np.mean(y[order[:k]]))
        sup_pass = bool(top_mean > 0)
        counts["top-third cases"] = k

    main = {
        "name": main_name,
        "value": slope,
        "statistic": ({"name": "OLS slope t", "value": t_val} if t_val is not None else None),
        "threshold": threshold,
    }
    supporting = {"name": "mean excess 30-bar return of top third by volume ratio > 0",
                  "value": top_mean, "passed": sup_pass}

    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"Only {n_cases} non-overlapping breakout cases, fewer than the plan's minimum of 30."
    elif t_val is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed (no variation in volume ratio), so neither rule is met."
    elif t_val >= 2 and sup_pass:
        status = "confirmed"
        decided = "The slope's t is 2 or more with at least 30 cases and the top-third mean excess return is above zero."
    elif t_val >= 2:
        status = "inconclusive"
        decided = "The slope's t is 2 or more but the top-third mean excess return is not above zero."
    elif t_val <= -2:
        status = "rejected"
        decided = "The slope's t is -2 or less with at least 30 cases: heavier breakout volume goes with smaller 30-bar returns."
    else:
        status = "inconclusive"
        decided = "The slope's t is between -2 and 2 with at least 30 cases."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": supporting,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
