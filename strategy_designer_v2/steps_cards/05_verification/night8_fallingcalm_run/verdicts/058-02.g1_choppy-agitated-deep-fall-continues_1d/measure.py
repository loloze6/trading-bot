import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    RAW = "debug_info.components.scaled_fall.last_history_value"
    PROFILE_REGIME = "unknown"  # the only regime with a strategy: no veto fired = choppy agitated

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            reg = df["regime"].astype(str).values
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce").values
            else:
                raw = np.full(len(df), np.nan)
            active = fc != 0
            in_profile = reg == PROFILE_REGIME
            fell = np.where(np.isnan(raw), False, raw < 0)
            situation = in_profile & fell
            agree = active & situation & (fc < 0)
            n_active += int(active.sum())
            n_agree += int(agree.sum())

    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on short side": int(n_agree)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are short bars in the choppy "
                           "agitated profile (regime 'unknown') with a 30-day fall (raw scaled return < 0)"
                           if n_active > 0 else "The record has no bar with a non-zero forecast."),
            "reading": "The profile is read from the regime column (regime 'unknown', no veto fired) and the fall from the sign of the raw scaled 30-day return.",
        }

    # ---------- 2. criterion ----------
    xs, ys = [], []
    for coin, wins in bars.items():
        grid_rows = []
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
                grid_rows.append((c1 / c0 - 1.0, fc[i]))
        if not grid_rows:
            continue
        rets = np.array([r for r, _ in grid_rows], dtype=float)
        fcs = np.array([f for _, f in grid_rows], dtype=float)
        hold = float(np.mean(rets))
        sel = np.isfinite(fcs) & (fcs < 0)
        xs.extend(fcs[sel].tolist())
        ys.extend((rets[sel] - hold).tolist())

    x = np.array(xs, dtype=float)
    y = np.array(ys, dtype=float)
    n_cases = int(len(x))
    counts = {"grid bars with forecast < 0": n_cases}

    slope = None
    t_slope = None
    if n_cases >= 3 and np.std(x) > 0:
        lr = stats.linregress(x, y)
        slope = float(lr.slope)
        t_slope = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None
    mean_ex = float(np.mean(y)) if n_cases > 0 else None
    check_pass = bool(mean_ex < 0) if mean_ex is not None else None

    main = {
        "name": "pooled OLS slope of 5-day excess return on forecast (grid bars, forecast < 0)",
        "value": slope,
        "statistic": {"name": "OLS slope t", "value": t_slope} if t_slope is not None else None,
        "threshold": "confirm: slope > 0 with t >= 2 and mean excess < 0; reject: slope < 0 with t <= -2",
    }
    support = {"name": "mean 5-day excess return on the same bars below 0", "value": mean_ex, "passed": check_pass}
    reading = ("The profile is read from the regime column (regime 'unknown', no veto fired) and the fall from the sign "
               "of the raw scaled 30-day return; holding is the coin's mean 5-day return over its non-overlapping grid "
               "of all windows, and the plan's minimum of 30 grid bars is applied as 'not observable'.")

    if n_cases < 30:
        status = "not observable"
        decided = "Fewer than 30 grid bars with forecast < 0 (the plan's minimum count) were recorded."
    elif t_slope is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed (no variation in the forecast), so neither confirm nor reject is met."
    elif slope > 0 and t_slope >= 2 and check_pass:
        status = "confirmed"
        decided = "The slope is positive with t >= 2 and the mean excess return is below 0 (confirm rule)."
    elif slope < 0 and t_slope <= -2:
        status = "rejected"
        decided = "The slope is negative with t <= -2 (reject rule)."
    elif slope > 0 and t_slope >= 2:
        status = "inconclusive"
        decided = "The slope confirms (t >= 2) but the supporting check fails (mean excess not below 0)."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and 2 (inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": support,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
