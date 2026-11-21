import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    RAW = "debug_info.components.composite.last_history_value"
    MIN_CASES = 100

    # ---------- 1. Situation check: forecast side must follow the composite score's sign ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            f = pd.to_numeric(df["forecast"], errors="coerce")
            raw = pd.to_numeric(df[RAW], errors="coerce") if RAW in df.columns else pd.Series(np.nan, index=df.index)
            active = f.notna() & (f != 0)
            n_active += int(active.sum())
            agree = active & raw.notna() & (np.sign(raw) == np.sign(f)) & (raw != 0)
            n_agree += int(agree.sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "mean of forecast/10 x (5-day return - coin's mean 5-day return), non-overlapping grid"
    threshold = "confirm: mean > 0 with t >= 2; reject: mean < 0 with t <= -2; otherwise inconclusive; at least 100 cases"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"cases with a non-zero forecast": None},
            "decided_by": (
                f"Only {agreement:.1%} of the {n_active} bars with a non-zero forecast have the sign of the composite "
                "score (long when positive, short when negative), below the 90 % the plan's situation requires."
            ),
            "reading": "The plan's situation is read as: long on bars where the raw composite score is positive, short where it is negative.",
        }

    # ---------- 2. Criterion ----------
    # coin's mean 5-day return over all its windows, on the non-overlapping grid
    coin_grid = {}
    coin_mean = {}
    for coin, wins in bars.items():
        rows = []
        all_r = []
        for w, df in wins.items():
            if df is None or len(df) <= H:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            f = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            n = len(df)
            for p in range(0, n - H, H):
                c0, c1 = close[p], close[p + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                all_r.append(r)
                rows.append((f[p], r))
        coin_grid[coin] = rows
        coin_mean[coin] = float(np.mean(all_r)) if all_r else np.nan

    vals = []
    for coin, rows in coin_grid.items():
        m = coin_mean[coin]
        if not np.isfinite(m):
            continue
        for fv, r in rows:
            if np.isfinite(fv) and fv != 0:
                vals.append(fv / 10.0 * (r - m))

    vals = np.asarray(vals, dtype=float)
    n_cases = int(len(vals))
    mean = float(vals.mean()) if n_cases > 0 else None
    if n_cases > 1:
        sd = float(vals.std(ddof=1))
        t = float(mean / (sd / np.sqrt(n_cases))) if sd > 0 else (0.0 if mean == 0 else float(np.sign(mean) * np.inf))
    else:
        t = None

    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"Only {n_cases} non-overlapping 5-bar cases with a non-zero forecast, below the plan's minimum of 100."
    elif mean > 0 and t >= 2:
        status = "confirmed"
        decided = f"The mean is above 0 with t = {t:.2f} >= 2 over {n_cases} cases (confirm rule; the plan has no supporting check)."
    elif mean < 0 and t <= -2:
        status = "rejected"
        decided = f"The mean is below 0 with t = {t:.2f} <= -2 over {n_cases} cases (reject rule)."
    else:
        status = "inconclusive"
        decided = f"t = {t:.2f} lies between -2 and 2 over {n_cases} cases (inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean,
            "statistic": {"name": "t of the mean", "value": t} if t is not None and np.isfinite(t) else None,
            "threshold": threshold,
        },
        "supporting_check": None,
        "counts": {"cases with a non-zero forecast": n_cases},
        "decided_by": decided,
        "reading": (
            "Situation read as long when the raw composite score is positive and short when negative; grid positions "
            "0, 5, 10, ... of each window with a full 5-bar return inside the window; the coin's mean 5-day return is "
            "the mean over all its windows' grid returns (all grid bars, active or not); the 100-case minimum is applied "
            "as 'not observable'."
        ),
    }
