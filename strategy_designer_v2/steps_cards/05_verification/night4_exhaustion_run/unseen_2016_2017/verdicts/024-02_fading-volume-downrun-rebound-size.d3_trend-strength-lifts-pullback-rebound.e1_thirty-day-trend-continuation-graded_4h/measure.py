import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 18
    RAW = "debug_info.components.rise30d.last_history_value"

    # ---------- 1. Situation check: 180-bar return > 0, long side ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            close = pd.to_numeric(df["close"], errors="coerce")
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            # fall back to the price-based 180-bar return where the raw value is missing
            recomputed = close / close.shift(180) - 1.0
            raw = raw.where(raw.notna(), recomputed)
            active = fc.notna() & (fc != 0)
            situation = raw.notna() & (raw > 0)
            agree = active & situation & (fc > 0)
            n_active += int(active.sum())
            n_agree += int(agree.sum())

    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.90

    main_name = "pooled OLS slope of 18-bar excess forward return on forecast (grid cells)"
    threshold = "confirm: slope > 0 with t >= 2; reject: slope < 0 with t <= -2; otherwise inconclusive"
    reading = ("Situation bars are those with the recorded 180-bar return (recomputed from closes where missing) "
               "above 0 and a positive forecast; the coin's normal drift is the mean of its non-overlapping 18-bar "
               "grid returns over all its windows; all grid cells with a valid forward return and forecast enter the "
               "regression (forecast 0 included); the slope's t is the ordinary OLS t; the plan's minimum counts, "
               "when not reached, give 'not observable'.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "agreeing active bars": int(n_agree)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are bars with a positive 30-day "
                           "return and a long forecast, so the config does not do what the plan's situation says."),
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    rows = []
    for coin, wins in bars.items():
        coin_rows = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy()
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy()
            n = len(df)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                coin_rows.append((c1 / c0 - 1.0, fc[i]))
        if not coin_rows:
            continue
        rets = np.array([r for r, _ in coin_rows], dtype=float)
        drift = float(np.mean(rets))
        for r, f in coin_rows:
            if np.isfinite(f):
                rows.append((r - drift, float(f)))

    total_cells = len(rows)
    y = np.array([r for r, _ in rows], dtype=float)
    x = np.array([f for _, f in rows], dtype=float)
    pos_cells = int(np.sum(x > 0)) if total_cells else 0
    counts = {"grid cells with forecast > 0": pos_cells, "grid cells in total": int(total_cells)}

    slope = None
    tval = None
    if total_cells >= 3 and np.ptp(x) > 0:
        lr = stats.linregress(x, y)
        slope = float(lr.slope)
        tval = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    main = {"name": main_name, "value": slope,
            "statistic": ({"name": "OLS slope t", "value": tval} if tval is not None else None),
            "threshold": threshold}

    if pos_cells < 100 or total_cells < 500:
        missing = []
        if pos_cells < 100:
            missing.append(f"grid cells with forecast > 0 = {pos_cells} < 100")
        if total_cells < 500:
            missing.append(f"grid cells in total = {total_cells} < 500")
        status = "not observable"
        decided = "The plan's minimum count is not reached: " + "; ".join(missing) + "."
    elif slope is None or tval is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed (no variation in the forecast), so neither rule is met."
    elif slope > 0 and tval >= 2:
        status = "confirmed"
        decided = "The slope is positive with t >= 2: excess 3-day returns grow with the forecast's size."
    elif slope < 0 and tval <= -2:
        status = "rejected"
        decided = "The slope is negative with t <= -2: larger 30-day rises are followed by smaller-than-drift 3-day returns."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": None,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
