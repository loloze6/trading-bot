import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 3
    DEPTH_COL = "debug_info.components.depth.last_history_value"
    MIN_CASES = 50

    # ---------- 1. Situation check ----------
    # Situation (Fidelity): falling, calm profile (the detector's non-vetoed regime "unknown"),
    # with the close below its 20-day high (raw depth < 0); expected side: short (a fall).
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            reg = df["regime"].astype(str).values if "regime" in df.columns else np.array([""] * len(df))
            if DEPTH_COL in df.columns:
                depth = pd.to_numeric(df[DEPTH_COL], errors="coerce").values
            else:
                depth = np.full(len(df), np.nan)
            active = fc != 0
            in_profile = reg == "unknown"
            below_high = np.where(np.isnan(depth), False, depth < 0)
            situation = in_profile & below_high & (fc < 0)
            n_active += int(active.sum())
            n_agree += int((active & situation).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "OLS slope of coin-excess 3-bar forward return on forecast (before costs)"
    threshold = "confirm: slope > 0 with t >= 2 and check passes; reject: slope < 0 with t <= -2"
    sup_name = "mean excess 3-bar return of deepest third minus shallowest third (< 0 passes)"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "independent cases": 0},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are short bars inside the falling, "
                           "calm profile with the close below its 20-day high, so the config does not do what the "
                           "Fidelity says."),
            "reading": "The profile is read from the recorded regime (\"unknown\" = not vetoed by the trend or swing "
                       "rules) and the depth from its raw recorded value.",
        }

    # ---------- 2. Criterion ----------
    rows = []  # (coin, forecast, fwd return)
    coin_grid_returns = {}
    for coin, wins in bars.items():
        allret = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            n = len(df)
            for i in range(0, n - H, H):
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 <= 0:
                    continue
                r = c1 / c0 - 1.0
                allret.append(r)
                f = fc[i]
                if np.isfinite(f) and f != 0:
                    rows.append((coin, float(f), r))
        coin_grid_returns[coin] = allret

    coin_mean = {c: (float(np.mean(v)) if len(v) else np.nan) for c, v in coin_grid_returns.items()}
    cases = [(c, f, r - coin_mean[c]) for c, f, r in rows if np.isfinite(coin_mean.get(c, np.nan))]
    n_cases = len(cases)
    counts = {"independent cases": int(n_cases), "active bars": int(n_active)}

    reading = ("The profile is read from the recorded regime (\"unknown\" = not vetoed) and the depth from its raw "
               "value; cases are grid bars 0,3,6,... of each window with a non-zero forecast and a full 3-bar return "
               "in the window, the coin's mean is over all its grid bars in all windows, and the thirds are the "
               "floor(n/3) most negative and floor(n/3) least negative forecasts.")

    if n_cases < MIN_CASES:
        return {
            "status": "not observable",
            "situation_check": {"agreement": agreement, "passed": True},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": {"name": sup_name, "value": None, "passed": None},
            "counts": counts,
            "decided_by": f"Fewer than {MIN_CASES} independent cases ({n_cases}): the plan's minimum count is not reached.",
            "reading": reading,
        }

    f_arr = np.array([c[1] for c in cases])
    e_arr = np.array([c[2] for c in cases])

    if np.ptp(f_arr) == 0:
        slope, t_val = None, None
    else:
        lr = stats.linregress(f_arr, e_arr)
        slope = float(lr.slope)
        t_val = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    order = np.argsort(f_arr, kind="mergesort")
    k = n_cases // 3
    deep = e_arr[order[:k]]
    shallow = e_arr[order[-k:]]
    diff = float(np.mean(deep) - np.mean(shallow)) if k > 0 else None
    sup_pass = bool(diff is not None and diff < 0)

    if slope is None or t_val is None:
        status = "inconclusive"
        decided = "The slope or its t cannot be computed, so neither the confirm nor the reject rule is met."
    elif slope > 0 and t_val >= 2 and sup_pass:
        status = "confirmed"
        decided = "The slope is positive with t >= 2 and the deepest third minus the shallowest third is below 0."
    elif slope < 0 and t_val <= -2:
        status = "rejected"
        decided = "The slope is negative with t <= -2: deeper closes are followed by smaller falls or rebounds."
    elif slope > 0 and t_val >= 2:
        status = "inconclusive"
        decided = "The slope is positive with t >= 2 but the deepest-minus-shallowest difference is not below 0."
    else:
        status = "inconclusive"
        decided = "The slope has |t| < 2."

    counts["cases per third"] = int(k)

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": slope,
            "statistic": {"name": "OLS slope t", "value": t_val} if t_val is not None else None,
            "threshold": threshold,
        },
        "supporting_check": {"name": sup_name, "value": diff, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
