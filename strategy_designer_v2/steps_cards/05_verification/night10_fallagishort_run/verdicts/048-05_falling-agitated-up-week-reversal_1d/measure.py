import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 3
    LHV = "debug_info.components.scaled_week.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = df["close"].astype(float)
            fc = df["forecast"].astype(float).fillna(0.0)
            regime = df["regime"].astype(str)

            # up week: 7-day return > 0 (from prices; where not computable, the recorded
            # raw scaled week, whose sign is the sign of the 7-day return)
            r7 = close / close.shift(7) - 1.0
            sw = df[LHV].astype(float) if LHV in df.columns else pd.Series(np.nan, index=df.index)
            up_week = pd.Series(np.where(r7.notna(), r7 > 0, sw > 0), index=df.index)

            # falling: 60-day price evolution (percent) below -10, where computable
            r60 = (close / close.shift(60) - 1.0) * 100.0
            falling_ok = pd.Series(np.where(r60.notna(), r60 < -10.0, True), index=df.index)

            # agitated (vol percentile > 0.5 over 365 bars) cannot be rebuilt inside a ~120-bar
            # window: the detector's recorded decision carries the vetoes
            in_regime = regime == "mean_reversion"

            situation = in_regime & up_week.astype(bool) & falling_ok.astype(bool)
            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc < 0)).sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "t of the slope of y (3-day return minus coin mean) on |forecast|, grid bars with forecast < 0"
    threshold = "confirm: t <= -2 and mean y < 0; reject: t >= +2 and mean y > 0; fewer than 50 cases: not decidable"
    reading = ("Profile on each bar is read from the recorded regime (the 365-bar volatility percentile cannot be "
               "rebuilt inside a window) plus the 7-day return > 0 and the 60-day percent move < -10 where computable; "
               "the coin's mean 3-day return is the mean over the same non-overlapping grid of all its windows; "
               "fewer than 50 cases is reported as not observable.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": n_active, "cases (grid bars with forecast < 0)": None},
            "decided_by": ("Fewer than 90% of the active bars are short bars inside the falling-agitated profile "
                           "after an up week (7-day return > 0)" if n_active > 0 else
                           "The book never takes a position, so the plan's short-after-up-week situation is never traded"),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    xs, ys = [], []
    for coin, wins in bars.items():
        grid_rows = []
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = df["close"].astype(float).values
            fc = df["forecast"].astype(float).values
            n = len(df)
            for i in range(0, n, H):
                if i + H < n and np.isfinite(close[i]) and np.isfinite(close[i + H]) and close[i] > 0:
                    grid_rows.append((close[i + H] / close[i] - 1.0, fc[i]))
        if not grid_rows:
            continue
        rets = np.array([g[0] for g in grid_rows])
        fcs = np.array([g[1] for g in grid_rows])
        coin_mean = float(np.mean(rets))
        sel = np.isfinite(fcs) & (fcs < 0)
        ys.extend((rets[sel] - coin_mean).tolist())
        xs.extend(np.abs(fcs[sel]).tolist())

    x = np.array(xs, dtype=float)
    y = np.array(ys, dtype=float)
    n_cases = int(len(y))
    mean_y = float(np.mean(y)) if n_cases > 0 else None

    t_slope = None
    slope = None
    if n_cases >= 3 and np.std(x) > 0:
        lr = stats.linregress(x, y)
        slope = float(lr.slope)
        t_slope = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    support_passed = (mean_y < 0) if mean_y is not None else None
    counts = {"active bars": n_active, "cases (grid bars with forecast < 0)": n_cases}

    if n_cases < 50:
        status = "not observable"
        decided_by = f"Only {n_cases} cases (grid bars with forecast < 0), below the plan's minimum of 50."
    elif t_slope is None:
        status = "inconclusive"
        decided_by = "The slope's t cannot be computed (no spread in |forecast|), so the result meets neither rule."
    elif t_slope <= -2 and mean_y < 0:
        status = "confirmed"
        decided_by = "The slope's t is -2 or lower and the mean y is below 0 (confirm rule)."
    elif t_slope >= 2 and mean_y > 0:
        status = "rejected"
        decided_by = "The slope's t is +2 or higher and the mean y is above 0 (reject rule)."
    else:
        status = "inconclusive"
        decided_by = "With at least 50 cases, the slope's t and the mean y meet neither the confirm nor the reject rule."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": t_slope,
            "statistic": ({"name": "OLS slope t", "value": t_slope} if t_slope is not None else None),
            "threshold": threshold,
        },
        "supporting_check": {"name": "mean y below 0", "value": mean_y,
                             "passed": (bool(support_passed) if support_passed is not None else None)},
        "counts": counts,
        "decided_by": decided_by,
        "reading": reading,
    }
