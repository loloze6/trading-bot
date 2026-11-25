import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    RAW = "debug_info.components.range_bottom.last_history_value"
    PROFILE_REGIME = "unknown"  # the only regime with a strategy: the choppy calm profile (vetoes send the rest to "chop")

    def raw_position(df):
        # recorded raw range position where present; otherwise recomputed from prices (sign only matters):
        # close relative to the middle of the 20-bar high-low range, current bar included
        hh = df["high"].rolling(20, min_periods=20).max()
        ll = df["low"].rolling(20, min_periods=20).min()
        recomputed = df["close"] - (hh + ll) / 2.0
        if RAW in df.columns:
            rec = pd.to_numeric(df[RAW], errors="coerce")
            return rec.where(rec.notna(), recomputed)
        return recomputed

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            pos = raw_position(df)
            in_profile = df["regime"].astype(str) == PROFILE_REGIME
            situation = in_profile & (pos < 0)
            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc > 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9

    main_name = "OLS slope of excess 5-bar forward return on forecast (profile bars, non-overlapping grid, pooled)"
    threshold = "confirm: slope > 0 with t >= 2 and supporting check passes; reject: slope < 0 with t <= -2"
    reading = ("Profile bars are bars with regime 'unknown' (the config's only active regime, i.e. choppy calm); "
               "the coin's mean 5-bar return is taken on the non-overlapping grid of all its bars over all windows; "
               "the regression uses all profile grid cases including forecast 0; the plan's 'fewer than 50 grid cases "
               "with forecast above 0' is applied as a minimum count giving 'not observable'.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of bars with a non-zero forecast are choppy-calm (regime 'unknown') bars "
                           "with the close below the middle of its 20-day range and a long forecast."
                           if n_active > 0 else "No active bars: the forecast is never non-zero."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    xs, ys = [], []
    for coin, wins in bars.items():
        # coin's normal drift: mean 5-bar return on the non-overlapping grid of all its windows
        all_r = []
        cases = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            reg = df["regime"].astype(str).values
            n = len(df)
            for t in range(0, n, H):
                if t + H >= n:
                    break
                c0, c1 = close[t], close[t + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                all_r.append(r)
                if reg[t] == PROFILE_REGIME and np.isfinite(fc[t]):
                    cases.append((fc[t], r))
        if not all_r:
            continue
        drift = float(np.mean(all_r))
        for f, r in cases:
            xs.append(float(f))
            ys.append(r - drift)

    xs = np.array(xs, dtype=float)
    ys = np.array(ys, dtype=float)
    n_cases = int(len(xs))
    pos_mask = xs > 0
    n_pos = int(pos_mask.sum())

    slope, tval = None, None
    if n_cases >= 3 and np.std(xs) > 0:
        lr = stats.linregress(xs, ys)
        slope = float(lr.slope)
        tval = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    sup_val = float(np.mean(ys[pos_mask])) if n_pos > 0 else None
    sup_pass = (sup_val > 0) if sup_val is not None else None

    counts = {"grid cases with forecast above 0": n_pos, "profile grid cases": n_cases}
    main = {"name": main_name, "value": slope,
            "statistic": {"name": "t of OLS slope", "value": tval} if tval is not None else None,
            "threshold": threshold}
    supporting = {"name": "mean excess 5-bar return of grid cases with forecast > 0",
                  "value": sup_val, "passed": sup_pass}

    if n_pos < 50:
        status = "not observable"
        decided = f"Only {n_pos} grid cases with forecast above 0, fewer than the plan's minimum of 50."
    elif slope is None or tval is None:
        status = "inconclusive"
        decided = "The slope or its t could not be computed (no variation in the forecast), meeting neither rule."
    elif slope > 0 and tval >= 2 and sup_pass:
        status = "confirmed"
        decided = "The slope is positive with t >= 2 and the mean excess return of forecast > 0 cases is positive."
    elif slope > 0 and tval >= 2:
        status = "inconclusive"
        decided = "The slope is positive with t >= 2 but the supporting check failed: inconclusive by the plan."
    elif slope < 0 and tval <= -2:
        status = "rejected"
        decided = "The slope is negative with t <= -2."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": supporting,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
