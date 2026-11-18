import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    RAW = "debug_info.components.vol_rise.last_history_value"

    # ---------- 1. situation check ----------
    # Situation: a volatility-scaled up move times the volume ratio (raw value > 0, long side).
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            if "forecast" not in df.columns:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            close = pd.to_numeric(df["close"], errors="coerce")
            ret1 = close / close.shift(1) - 1.0
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            # Where the raw value is not recorded, take the sign of the bar's return
            # (the volume ratio is always positive).
            sit = np.where(raw.notna(), raw > 0, ret1 > 0)
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            n_agree += int((active & pd.Series(sit, index=df.index) & (fc > 0)).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.90)

    main_name = "mean excess 5-bar forward return of cases with forecast >= 2 (vs coin mean on the same grid)"
    threshold = "confirm if t >= 2 and supporting difference > 0; reject if t <= -2; at least 30 cases"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "cases": None},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars on an up day "
                           "(positive volume-weighted scaled return), the plan's adapted situation and side."),
            "reading": "The situation is read as a positive raw component value (up day, volume ratio always positive) with a positive forecast.",
        }

    # ---------- 2. criterion ----------
    case_rows = []  # (coin, forecast, fwd return)
    coin_grid_rets = {}
    for coin, wins in bars.items():
        all_rets = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            n = len(df)
            for t in range(0, n, H):
                if t + H >= n:
                    break
                c0, c1 = close[t], close[t + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                all_rets.append(r)
                if np.isfinite(fc[t]) and fc[t] >= 2:
                    case_rows.append((coin, fc[t], r))
        coin_grid_rets[coin] = float(np.mean(all_rets)) if all_rets else np.nan

    excess = []
    fcs = []
    for coin, f, r in case_rows:
        m = coin_grid_rets.get(coin, np.nan)
        if np.isfinite(m):
            excess.append(r - m)
            fcs.append(f)
    excess = np.array(excess, dtype=float)
    fcs = np.array(fcs, dtype=float)
    n_cases = int(len(excess))

    mean_ex = float(np.mean(excess)) if n_cases > 0 else None
    t_stat = None
    if n_cases >= 2:
        sd = float(np.std(excess, ddof=1))
        if sd > 0:
            t_stat = float(mean_ex / (sd / np.sqrt(n_cases)))

    diff = None
    n_above = n_below = 0
    if n_cases > 0:
        med = float(np.median(fcs))
        above = excess[fcs > med]
        below = excess[fcs < med]
        n_above, n_below = int(len(above)), int(len(below))
        if n_above > 0 and n_below > 0:
            diff = float(np.mean(above) - np.mean(below))
    sup_passed = None if diff is None else bool(diff > 0)

    if n_cases < 30:
        status = "not observable"
        decided = f"Only {n_cases} cases with forecast >= 2 across all coins and windows, fewer than the plan's minimum of 30."
    elif t_stat is None:
        status = "inconclusive"
        decided = "The t of the mean excess return could not be computed (zero dispersion), so neither the confirm nor the reject rule is met."
    elif t_stat >= 2 and sup_passed is True:
        status = "confirmed"
        decided = "The mean excess 5-bar return has t >= 2 and the above-median minus below-median difference is above 0."
    elif t_stat <= -2:
        status = "rejected"
        decided = "The mean excess 5-bar return has t <= -2: large heavy-volume rises are given back."
    elif t_stat >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the supporting difference is not above 0, which the plan calls inconclusive."
    else:
        status = "inconclusive"
        decided = "t lies between -2 and 2, which the plan calls inconclusive whatever the supporting check shows."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_ex,
            "statistic": None if t_stat is None else {"name": "t of the mean", "value": t_stat},
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "mean excess of cases above median forecast minus below median",
            "value": diff,
            "passed": sup_passed,
        },
        "counts": {
            "cases": n_cases,
            "cases above median forecast": n_above,
            "cases below median forecast": n_below,
            "active bars": int(n_active),
        },
        "decided_by": decided,
        "reading": ("The coin's mean is taken over every grid bar with a full 5-bar return in all its windows, cases are grid bars "
                    "with forecast >= 2 and a full return inside the window, cases equal to the median forecast are left out of "
                    "the supporting split, and fewer than 30 cases gives 'not observable' as the workflow requires."),
    }
