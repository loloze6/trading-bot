import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 6
    BAND = 2.0
    MIN_CASES = 30
    RAW = "debug_info.components.panic.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            close = pd.to_numeric(df["close"], errors="coerce")
            raw = pd.to_numeric(df[RAW], errors="coerce") if RAW in df.columns else pd.Series(np.nan, index=df.index)
            active = fc.notna() & (fc != 0)
            past = close.shift(H)
            fell_price = close < past
            price_known = past.notna() & close.notna()
            # situation: the component's graded fall-x-range value is positive (a fall over the last 24h),
            # and, where the 6-bar price change is computable inside the window, the price did fall
            situation = (raw > 0) & (fell_price | ~price_known)
            on_side = fc > 0  # rebound -> long
            n_active += int(active.sum())
            n_agree += int((active & situation & on_side).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9

    main_name = "mean 6-bar excess return (return minus coin's normal 6-bar drift) over bet cases"
    threshold = "t >= 2 over at least 30 cases pooled (confirm, with positive slope); t <= -2 over at least 30 cases (reject)"
    sup_name = "slope of excess 6-bar return on forecast, grid bars with forecast > 0"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"cases": 0, "active bars": n_active},
            "decided_by": ("Fewer than 90% of bars with a non-zero forecast are bars where the last 24h fell "
                           "(positive panic component and lower close than 6 bars before) with a long forecast"
                           if n_active > 0 else "No bar has a non-zero forecast, so the plan's long bets after a fall never occur"),
            "reading": "Situation taken as a positive raw panic value with a lower close than 6 bars earlier where computable, side long.",
        }

    # ---------- 2. normal drift per coin ----------
    drift = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy()
            n = len(close)
            for p in range(0, n - H, H):
                a, b = close[p], close[p + H]
                if np.isfinite(a) and np.isfinite(b) and a > 0:
                    rets.append(b / a - 1.0)
        drift[coin] = float(np.mean(rets)) if rets else np.nan

    # ---------- 3. cases and supporting regression data ----------
    case_ex = []
    reg_x, reg_y = [], []
    for coin, wins in bars.items():
        d = drift[coin]
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy()
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy()
            n = len(df)

            # bets: rise of the forecast on the long side of at least BAND from its low since the last bet
            bet = np.zeros(n, dtype=bool)
            low = 0.0
            for t in range(n):
                f = fc[t]
                if not np.isfinite(f) or f <= 0:
                    low = 0.0
                    continue
                if f - low >= BAND:
                    bet[t] = True
                    low = f
                else:
                    low = min(low, f)

            # once per 6-bar grid cell: first bet in each cell
            seen = set()
            for t in np.nonzero(bet)[0]:
                cell = t // H
                if cell in seen:
                    continue
                seen.add(cell)
                if t + H >= n:
                    continue
                a, b = close[t], close[t + H]
                if not (np.isfinite(a) and np.isfinite(b) and a > 0 and np.isfinite(d)):
                    continue
                case_ex.append((b / a - 1.0) - d)

            # supporting: grid bars with forecast > 0
            for p in range(0, n - H, H):
                f = fc[p]
                a, b = close[p], close[p + H]
                if np.isfinite(f) and f > 0 and np.isfinite(a) and np.isfinite(b) and a > 0 and np.isfinite(d):
                    reg_x.append(float(f))
                    reg_y.append((b / a - 1.0) - d)

    n_cases = len(case_ex)
    arr = np.asarray(case_ex, dtype=float)
    mean_ex = float(arr.mean()) if n_cases > 0 else None
    t_stat = None
    if n_cases >= 2:
        sd = arr.std(ddof=1)
        if sd > 0:
            t_stat = float(mean_ex / (sd / np.sqrt(n_cases)))

    slope = None
    if len(reg_x) >= 3 and np.ptp(reg_x) > 0:
        slope = float(stats.linregress(reg_x, reg_y).slope)
    slope_pass = None if slope is None else bool(slope > 0)

    counts = {"cases": n_cases, "supporting grid bars with forecast > 0": len(reg_x)}

    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"Only {n_cases} cases pooled across coins, fewer than the plan's minimum of 30."
    elif t_stat is None:
        status = "inconclusive"
        decided = "The t of the mean excess return cannot be computed (zero dispersion), so neither rule is met."
    elif t_stat >= 2 and slope_pass is True:
        status = "confirmed"
        decided = "Mean excess return t >= 2 over at least 30 pooled cases and the supporting slope is positive."
    elif t_stat <= -2:
        status = "rejected"
        decided = "Mean excess return t <= -2 over at least 30 cases."
    elif t_stat >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the supporting slope is not positive (or not computable), which the plan calls inconclusive."
    else:
        status = "inconclusive"
        decided = "t lies between -2 and 2 with at least 30 cases, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_ex,
            "statistic": {"name": "t of the mean", "value": t_stat} if t_stat is not None else None,
            "threshold": threshold,
        },
        "supporting_check": {"name": sup_name, "value": slope, "passed": slope_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": ("A case is the first long bet (forecast rise >= 2 from its low since the last bet, reset at flat) in each "
                    "6-bar grid cell counted from each window's first row, the drift is each coin's mean non-overlapping "
                    "6-bar return over all its windows, and the slope is an ordinary least-squares slope on the grid bars "
                    "with forecast > 0 and a full 6-bar return inside the window."),
    }
