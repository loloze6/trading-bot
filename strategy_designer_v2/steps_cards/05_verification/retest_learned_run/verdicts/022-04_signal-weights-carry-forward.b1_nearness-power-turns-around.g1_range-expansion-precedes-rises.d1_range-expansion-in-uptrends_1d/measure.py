import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    RET_PERIOD = 20
    COMP = "debug_info.components.range_mult.last_history_value"

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float).values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            n = len(df)
            ret20 = np.full(n, np.nan)
            if n > RET_PERIOD:
                ret20[RET_PERIOD:] = close[RET_PERIOD:] / close[:-RET_PERIOD] - 1.0
            regime = df["regime"].astype(str).values if "regime" in df.columns else np.array([""] * n)
            # Uptrend: recomputed 20-bar return > 0; on the first 20 bars of a window
            # (no in-window history) fall back to the detector's recorded regime.
            uptrend = np.where(np.isnan(ret20), regime == "trending", ret20 > 0)
            if COMP in df.columns:
                comp = pd.to_numeric(df[COMP], errors="coerce").values
            else:
                comp = np.full(n, np.nan)
            comp_ok = np.isfinite(comp) & (comp > 0)
            active = np.isfinite(fc) & (fc != 0)
            agree = active & uptrend & comp_ok & (fc > 0)
            n_active += int(active.sum())
            n_agree += int(agree.sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)
    situation_check = {"agreement": agreement, "passed": passed}

    main_name = "pooled OLS slope of 5-bar excess return on forecast, trending grid bars"
    main_thr = "slope t >= 2 confirms (with top-minus-bottom third > 0); t <= -2 rejects"
    sup_name = "mean excess 5-bar return, top third minus bottom third of forecasts"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": situation_check,
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of active (non-zero forecast) bars are long bars with a positive "
                           "20-day return and a positive range ratio, as the plan's Fidelity requires."),
            "reading": "On the first 20 bars of a window the 20-day return cannot be recomputed in-window, so the recorded regime is used there.",
        }

    # ---------- 2. Criterion ----------
    xs, ys = [], []
    for coin, wins in bars.items():
        # normal drift: mean non-overlapping 5-bar return over all the coin's windows
        all_r = []
        per_win = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float).values
            n = len(df)
            grid = np.arange(0, n - H, H)
            r = close[grid + H] / close[grid] - 1.0 if len(grid) else np.array([])
            all_r.extend([v for v in r if np.isfinite(v)])
            per_win.append((df, grid, r))
        if len(all_r) == 0:
            continue
        drift = float(np.mean(all_r))
        for df, grid, r in per_win:
            if len(grid) == 0:
                continue
            reg = df["regime"].astype(str).values[grid]
            fc = pd.to_numeric(df["forecast"], errors="coerce").values[grid]
            m = (reg == "trending") & np.isfinite(fc) & np.isfinite(r)
            xs.extend(fc[m].tolist())
            ys.extend((r[m] - drift).tolist())

    x = np.array(xs, dtype=float)
    y = np.array(ys, dtype=float)
    n_cases = int(len(x))

    slope = None
    t_slope = None
    if n_cases >= 3 and np.std(x) > 0:
        lr = stats.linregress(x, y)
        slope = float(lr.slope)
        t_slope = float(lr.slope / lr.stderr) if lr.stderr > 0 else None

    diff = None
    k = n_cases // 3
    if k >= 1:
        order = np.argsort(x, kind="mergesort")
        bottom = y[order[:k]]
        top = y[order[-k:]]
        diff = float(top.mean() - bottom.mean())
    sup_passed = None if diff is None else bool(diff > 0)

    counts = {"trending-regime grid cases": n_cases}

    if n_cases < 100:
        status = "not observable"
        decided_by = f"Only {n_cases} trending-regime grid cases, below the plan's minimum of 100."
    elif t_slope is None:
        status = "inconclusive"
        decided_by = "The slope's t could not be computed (no variation in the forecast), so neither confirm nor reject rule is met."
    elif t_slope >= 2 and sup_passed:
        status = "confirmed"
        decided_by = "The slope's t is 2 or more and the top-minus-bottom-third difference is above 0."
    elif t_slope <= -2:
        status = "rejected"
        decided_by = "The slope's t is -2 or less."
    elif t_slope >= 2:
        status = "inconclusive"
        decided_by = "The slope's t is 2 or more but the top-minus-bottom-third difference is at or below 0."
    else:
        status = "inconclusive"
        decided_by = "The slope's t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": situation_check,
        "main_measure": {
            "name": main_name,
            "value": slope,
            "statistic": None if t_slope is None else {"name": "OLS slope t", "value": t_slope},
            "threshold": main_thr,
        },
        "supporting_check": {"name": sup_name, "value": diff, "passed": sup_passed},
        "counts": counts,
        "decided_by": decided_by,
        "reading": ("Trending cases are grid bars (positions 0,5,10,... of each window with a full 5-bar forward return) whose recorded regime is 'trending', "
                    "thirds are equal-count groups of floor(n/3) cases by forecast rank, the drift is the coin's mean non-overlapping 5-bar return over all its windows, "
                    "and on a window's first 20 bars the situation check uses the recorded regime since the 20-day return cannot be recomputed in-window."),
    }
