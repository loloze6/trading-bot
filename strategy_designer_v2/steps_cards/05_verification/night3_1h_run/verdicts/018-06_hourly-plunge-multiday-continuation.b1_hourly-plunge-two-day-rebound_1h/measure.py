import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 48
    BAND = 2.0
    RAW = "debug_info.components.drop24.last_history_value"

    # ---------- 1. situation check: a 24-bar drop -> long forecast ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            close = pd.to_numeric(df["close"], errors="coerce")
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            recomputed = close / close.shift(24) - 1.0
            raw = raw.where(raw.notna(), recomputed)
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            agree = active & (raw < 0) & (fc > 0)
            n_agree += int(agree.sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "mean 48-bar excess return over coin drift at forecast-rise cases"
    threshold = "confirm: mean > 0 with t >= 2 and Spearman > 0; reject: mean < 0 with t <= -2; at least 30 cases"
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"cases": 0, "active bars": n_active},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are bars with a negative "
                           "24-bar return and a positive (long) forecast, as the plan's situation requires."),
            "reading": "The situation is taken as a negative 24-bar return (drops only, graded), on the long side.",
        }

    # ---------- 2. criterion ----------
    excess_all = []
    fc_all = []
    for coin, wins in bars.items():
        # coin drift: mean non-overlapping 48-bar return over all windows
        grid_rets = []
        for w, df in wins.items():
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            n = len(close)
            for p in range(0, n - H, H):
                c0, c1 = close[p], close[p + H]
                if np.isfinite(c0) and np.isfinite(c1) and c0 != 0:
                    grid_rets.append(c1 / c0 - 1.0)
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))

        for w, df in wins.items():
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).to_numpy(dtype=float)
            n = len(close)
            ref = 0.0
            seen_cells = set()
            for i in range(n):
                f = fc[i]
                if f <= 0:
                    ref = 0.0
                    continue
                if f - ref >= BAND:
                    ref = f
                    cell = i // H
                    if cell in seen_cells:
                        continue
                    seen_cells.add(cell)
                    if i + H < n:
                        c0, c1 = close[i], close[i + H]
                        if np.isfinite(c0) and np.isfinite(c1) and c0 != 0:
                            excess_all.append(c1 / c0 - 1.0 - drift)
                            fc_all.append(f)
                else:
                    ref = min(ref, f)

    n_cases = len(excess_all)
    ex = np.asarray(excess_all, dtype=float)
    fa = np.asarray(fc_all, dtype=float)

    mean_ex = float(ex.mean()) if n_cases > 0 else None
    t_val = None
    if n_cases > 1:
        sd = float(ex.std(ddof=1))
        t_val = float(mean_ex / (sd / np.sqrt(n_cases))) if sd > 0 else None
    rho = None
    if n_cases > 2 and np.std(fa) > 0 and np.std(ex) > 0:
        r = stats.spearmanr(fa, ex).correlation
        rho = float(r) if np.isfinite(r) else None
    sup_pass = (rho > 0) if rho is not None else None

    if n_cases < 30:
        status = "not observable"
        decided = f"Only {n_cases} cases over all coins and windows, fewer than the plan's minimum of 30."
    elif t_val is not None and mean_ex > 0 and t_val >= 2 and rho is not None and rho > 0:
        status = "confirmed"
        decided = "The mean excess return is above 0 with t >= 2 and the Spearman correlation is above 0."
    elif t_val is not None and mean_ex < 0 and t_val <= -2:
        status = "rejected"
        decided = "The mean excess return is below 0 with t <= -2."
    elif t_val is not None and t_val >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the Spearman correlation is 0 or less (or undefined), which the plan calls inconclusive."
    else:
        status = "inconclusive"
        decided = "The t of the mean excess return lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_ex,
            "statistic": {"name": "t of the mean", "value": t_val} if t_val is not None else None,
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "Spearman(forecast at case, 48-bar excess return) > 0",
            "value": rho,
            "passed": sup_pass,
        },
        "counts": {"cases": n_cases},
        "decided_by": decided,
        "reading": ("A case is a bet bar (forecast rising >= 2 points above its lowest positive level since the last bet, "
                    "reset to 0 after a flat bar), the first in each 48-bar grid cell counted from the window's first row, "
                    "kept only when 48 bars remain in the window; the drift is the coin's mean over grid 48-bar returns of all its windows."),
    }
