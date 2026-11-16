import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 24
    RAW = "debug_info.components.below_long_ma.last_history_value"

    # ---------- 1. Situation check ----------
    # The situation is "close below its SMA(200)" (raw percent distance < 0).
    # The expected side is short (forecast < 0).
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if "forecast" not in df.columns:
                continue
            f = pd.to_numeric(df["forecast"], errors="coerce")
            raw = (pd.to_numeric(df[RAW], errors="coerce")
                   if RAW in df.columns else pd.Series(np.nan, index=df.index))
            active = f.notna() & (f != 0)
            n_active += int(active.sum())
            n_agree += int((active & (raw < 0) & (f < 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = ("OLS slope of 24-bar excess forward return on forecast, "
                 "non-overlapping 24-bar blocks pooled")
    main_thr = ("confirm if slope t >= 2 (with fall share > 50%); "
                "reject if slope t <= -2")
    reading = ("Non-overlapping blocks are the bars at positions 0, 24, 48, ... of each window, "
               "pooled over all windows into one OLS with the ordinary slope t; the excess return "
               "subtracts the mean 24-bar forward return of all bars of that window; the fall share "
               "uses all bars with forecast < 0 (not only grid bars); the block count is the number "
               "of grid bars with forecast < 0 and a valid forward return.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None,
                             "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are short bars "
                           "with the close below its SMA(200), so the config does not trade "
                           "the plan's situation on its side."),
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    grid_x, grid_y = [], []
    short_ex = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            f = pd.to_numeric(df["forecast"], errors="coerce")
            fwd = close.shift(-H) / close - 1.0
            mean_fwd = fwd.mean()
            if not np.isfinite(mean_fwd):
                continue
            ex = fwd - mean_fwd
            ok = ex.notna() & f.notna()
            # Supporting check: all bars with forecast < 0.
            sel = ok & (f < 0)
            short_ex.extend(ex[sel].tolist())
            # Main measure: non-overlapping grid.
            pos = np.arange(0, len(df), H)
            g_ok = ok.iloc[pos].values
            grid_x.extend(f.iloc[pos].values[g_ok].tolist())
            grid_y.extend(ex.iloc[pos].values[g_ok].tolist())

    x = np.asarray(grid_x, dtype=float)
    y = np.asarray(grid_y, dtype=float)
    n_blocks_short = int((x < 0).sum())

    slope = None
    t_slope = None
    if len(x) >= 3 and np.std(x) > 0:
        res = stats.linregress(x, y)
        slope = float(res.slope)
        if res.stderr is not None and res.stderr > 0:
            t_slope = float(res.slope / res.stderr)

    short_ex = np.asarray(short_ex, dtype=float)
    fall_share = float(np.mean(short_ex < 0)) if len(short_ex) > 0 else None
    fall_ok = (fall_share > 0.5) if fall_share is not None else None

    counts = {
        "non-overlapping 24-bar blocks with forecast < 0": n_blocks_short,
        "non-overlapping 24-bar blocks": int(len(x)),
        "bars with forecast < 0": int(len(short_ex)),
    }

    if n_blocks_short < 200:
        status = "inconclusive"
        decided = "Fewer than 200 non-overlapping 24-bar blocks have forecast < 0, so the result is inconclusive."
    elif t_slope is None:
        status = "inconclusive"
        decided = "The slope t could not be computed, so it is not outside -2 to 2 and the result is inconclusive."
    elif t_slope >= 2 and fall_ok:
        status = "confirmed"
        decided = "Slope t >= 2 across the pooled windows and the short-bar fall share is above 50%: confirm."
    elif t_slope <= -2:
        status = "rejected"
        decided = "Slope t <= -2: price rises after the close sits below the average, reject."
    elif t_slope >= 2:
        status = "inconclusive"
        decided = "Confirm-level slope t but the short-bar fall share is not above 50%: inconclusive."
    else:
        status = "inconclusive"
        decided = "Slope t lies between -2 and 2: inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": slope,
            "statistic": ({"name": "OLS slope t", "value": t_slope}
                          if t_slope is not None else None),
            "threshold": main_thr,
        },
        "supporting_check": {
            "name": "share of forecast<0 bars followed by negative 24-bar excess return, vs 50%",
            "value": fall_share,
            "passed": (bool(fall_ok) if fall_ok is not None else None),
        },
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
