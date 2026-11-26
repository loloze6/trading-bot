import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    RAW = "debug_info.components.dist_above_sma20.last_history_value"
    PROFILE_REGIME = "unknown"  # the only regime with a strategy: the rising agitated profile (not vetoed to chop)

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            fc = pd.to_numeric(d["forecast"], errors="coerce")
            close = pd.to_numeric(d["close"], errors="coerce")
            if RAW in d.columns:
                raw = pd.to_numeric(d[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=d.index)
            # fallback: recompute the percent distance from the 20-bar SMA inside the window
            sma = close.rolling(20, min_periods=20).mean()
            recomputed = (close / sma - 1.0) * 100.0
            dist = raw.where(raw.notna(), recomputed)
            regime = d["regime"].astype(str) if "regime" in d.columns else pd.Series("", index=d.index)
            active = fc.notna() & (fc != 0)
            situ = (dist > 0) & (regime == PROFILE_REGIME) & (fc < 0)
            n_active += int(active.sum())
            n_agree += int((active & situ).sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = True if agreement is None else bool(agreement >= 0.9)

    main_name = "t of the OLS slope of 5-bar excess return (vs normal drift) on abs(forecast), short grid cases"
    threshold = "confirm: slope < 0 with t <= -2 and mean short unusual move > 0; reject: slope > 0 with t >= +2; else inconclusive"
    sup_name = "mean unusual move in the short direction (minus excess return)"
    reading = ("The rising agitated profile is read from the recorded regime (the only regime with a strategy, "
               "'unknown', i.e. not vetoed to chop) since the detector's components are not recorded, the distance "
               "from last_history_value (recomputed from in-window prices where missing), the normal drift as each "
               "coin's mean 5-bar return on the non-overlapping grid of all its windows, and the plan's 'fewer than "
               "30 independent short cases' minimum is treated as a minimum count giving 'not observable'.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on short side": int(n_agree)},
            "decided_by": ("Fewer than 90% of active bars are short bars with the close above its 20-day SMA inside "
                           "the rising agitated profile, so the config does not do what the Fidelity says."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    xs, ys = [], []
    for coin, wins in bars.items():
        grid_rets = []
        cases = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").values
            fc = pd.to_numeric(d["forecast"], errors="coerce").values
            n = len(d)
            for t in range(0, n, H):
                if t + H >= n:
                    break
                c0, c1 = close[t], close[t + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                grid_rets.append(r)
                if np.isfinite(fc[t]) and fc[t] < 0:
                    cases.append((abs(fc[t]), r))
        if not grid_rets or not cases:
            continue
        drift = float(np.mean(grid_rets))
        for a, r in cases:
            xs.append(a)
            ys.append(r - drift)

    xs = np.asarray(xs, dtype=float)
    ys = np.asarray(ys, dtype=float)
    n_cases = int(len(xs))

    slope = None
    t_stat = None
    if n_cases >= 3 and np.std(xs) > 0:
        lr = stats.linregress(xs, ys)
        slope = float(lr.slope)
        if lr.stderr is not None and np.isfinite(lr.stderr) and lr.stderr > 0:
            t_stat = float(lr.slope / lr.stderr)
    mean_short = float(np.mean(-ys)) if n_cases > 0 else None
    sup_passed = None if mean_short is None else bool(mean_short > 0)

    counts = {"independent short cases": n_cases}
    sit = {"agreement": None if agreement is None else float(agreement), "passed": True}

    def out(status, decided):
        return {
            "status": status,
            "situation_check": sit,
            "main_measure": {
                "name": main_name,
                "value": t_stat,
                "statistic": None if t_stat is None else {"name": "OLS slope t", "value": t_stat},
                "threshold": threshold,
            },
            "supporting_check": {"name": sup_name, "value": mean_short, "passed": sup_passed},
            "counts": counts,
            "decided_by": decided,
            "reading": reading,
        }

    if n_cases < 30:
        return out("not observable", f"Fewer than 30 independent short cases ({n_cases}).")
    if t_stat is None or slope is None:
        return out("inconclusive", "The slope's t cannot be computed (no spread in abs(forecast)), so |t| < 2 is not exceeded.")
    if slope < 0 and t_stat <= -2:
        if mean_short is not None and mean_short > 0:
            return out("confirmed", "The slope is negative with t <= -2 and the mean unusual move in the short direction is positive.")
        return out("inconclusive", "The slope has t <= -2 but the mean unusual move in the short direction is at or below 0.")
    if slope > 0 and t_stat >= 2:
        return out("rejected", "The slope is positive with t >= +2: a larger distance is followed by a further rise versus drift.")
    return out("inconclusive", "The slope's |t| is below 2.")
