import json
import ast
import numpy as np
import pandas as pd
from scipy import stats


def _component_series(df, cid, field):
    """Return a float Series of a strategy component's recorded value (NaN where not recorded)."""
    flat = f"debug_info.components.{cid}.{field}"
    if flat in df.columns:
        return pd.to_numeric(df[flat], errors="coerce")
    if "debug_info.components" in df.columns:
        out = []
        for cell in df["debug_info.components"].tolist():
            val = np.nan
            d = cell
            if isinstance(d, str):
                try:
                    d = json.loads(d)
                except Exception:
                    try:
                        d = ast.literal_eval(d)
                    except Exception:
                        d = None
            if isinstance(d, dict):
                c = d.get(cid)
                if isinstance(c, dict) and field in c:
                    try:
                        val = float(c[field])
                    except Exception:
                        val = np.nan
            out.append(val)
        return pd.Series(out, index=df.index, dtype=float)
    return pd.Series(np.nan, index=df.index, dtype=float)


def measure(bars):
    H = 30
    MIN_CASES = 20
    LOOKBACK = 365

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            high = pd.to_numeric(df["high"], errors="coerce")
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            # highest high of the prior bars available in this window (at most 365), current bar excluded
            prior_high = high.shift(1).rolling(LOOKBACK, min_periods=1).max()
            # close above the prior high is necessary for a 365-bar break; first bar cannot be refuted
            in_sit = (close > prior_high) | prior_high.isna()
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            n_agree += int((active & in_sit & (fc > 0)).sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = True if agreement is None else bool(agreement >= 0.9)

    main_name = "pooled OLS slope of 30-bar excess return on vol_ratio post_pipeline_value at break bars"
    threshold = "confirm: slope > 0 with t >= 2 on >= 20 cases; reject: slope < 0 with t <= -2 on >= 20 cases"
    reading = ("The situation is checked as a necessary condition, close above the highest high of the prior bars "
               "available inside the window (at most 365, the window's first bar counted as consistent) with a "
               "positive forecast, since the 365-bar history is not recorded; a break bar is a 'trending' regime bar "
               "whose previous row in the same window is not 'trending' (a window's first row is not a case), and the "
               "coin's mean 30-bar return is taken on the non-overlapping grid (positions 0, 30, 60, ...) of all its windows pooled.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"cases": None},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars whose close is above "
                           "the prior high, so the config does not trade only the plan's breakout situation on the long side."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    xs, ys = [], []
    for coin, wins in bars.items():
        # coin mean 30-bar return over all windows (non-overlapping grid)
        grid_rets = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy()
            n = len(close)
            for p in range(0, n - H, H):
                c0, c1 = close[p], close[p + H]
                if np.isfinite(c0) and np.isfinite(c1) and c0 != 0:
                    grid_rets.append(c1 / c0 - 1.0)
        if len(grid_rets) == 0:
            continue
        coin_mean = float(np.mean(grid_rets))

        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy()
            regime = df["regime"].astype(str).to_numpy()
            vr = _component_series(df, "vol_ratio", "post_pipeline_value").to_numpy()
            n = len(df)
            last_kept = None
            for t in range(1, n):
                if regime[t] != "trending" or regime[t - 1] == "trending":
                    continue
                if t + H > n - 1:
                    continue
                if last_kept is not None and t - last_kept < H:
                    continue
                c0, c1, x = close[t], close[t + H], vr[t]
                if not (np.isfinite(c0) and np.isfinite(c1) and np.isfinite(x)) or c0 == 0:
                    continue
                last_kept = t
                xs.append(float(x))
                ys.append(c1 / c0 - 1.0 - coin_mean)

    n_cases = len(xs)
    counts = {"cases": n_cases}
    sit = {"agreement": None if agreement is None else float(agreement), "passed": passed}

    if n_cases < MIN_CASES:
        return {
            "status": "not observable",
            "situation_check": sit,
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": counts,
            "decided_by": f"Only {n_cases} independent break cases, fewer than the plan's minimum of 20.",
            "reading": reading,
        }

    x = np.asarray(xs)
    y = np.asarray(ys)
    if np.std(x) == 0:
        return {
            "status": "inconclusive",
            "situation_check": sit,
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": counts,
            "decided_by": "The forecast does not vary across cases, so no slope can be estimated; neither rule is met.",
            "reading": reading,
        }
    res = stats.linregress(x, y)
    slope = float(res.slope)
    tval = float(slope / res.stderr) if res.stderr and res.stderr > 0 else float("nan")

    if slope > 0 and np.isfinite(tval) and tval >= 2:
        status = "confirmed"
        decided = f"The slope is positive with t = {tval:.2f} >= 2 on {n_cases} cases (>= 20): the confirm rule."
    elif slope < 0 and np.isfinite(tval) and tval <= -2:
        status = "rejected"
        decided = f"The slope is negative with t = {tval:.2f} <= -2 on {n_cases} cases (>= 20): the reject rule."
    else:
        status = "inconclusive"
        decided = f"t = {tval:.2f} lies between -2 and 2 on {n_cases} cases: the inconclusive rule."

    return {
        "status": status,
        "situation_check": sit,
        "main_measure": {"name": main_name, "value": slope,
                         "statistic": {"name": "OLS slope t", "value": tval},
                         "threshold": threshold},
        "supporting_check": None,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
