import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    BAND = 2.0
    CASE_LEVEL = -5.0
    MIN_CASES = 30
    MIN_GRID = 100
    RAW = "debug_info.components.resistance.last_history_value"

    # ---------- 1. situation check ----------
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
            # situation: a 90-day swing-high level sits above the close (raw N/(1+D) > 0); expected side short
            agree = active & (raw > 0) & (f < 0)
            n_agree += int(agree.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {
                "name": "t of slope of drift-adjusted 5-bar return on forecast (forecast < 0, grid bars)",
                "value": None, "statistic": None,
                "threshold": "confirm if t >= 2 with supporting check; reject if t <= -2",
            },
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are short bars with a swing-high "
                           "level above the close (raw component > 0), as the Fidelity's situation and side require."),
            "reading": "Situation taken as the raw component being positive (a swing-high level above the close) and the side as a negative forecast.",
        }

    # ---------- 2. drift per coin: mean non-overlapping 5-bar return over all windows ----------
    drift = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            for i in range(0, len(c) - H, H):
                if np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] > 0:
                    rets.append(c[i + H] / c[i] - 1.0)
        drift[coin] = float(np.mean(rets)) if rets else np.nan

    # ---------- 3. main measure and cases ----------
    xs, ys = [], []
    case_moves = []
    for coin, wins in bars.items():
        d = drift.get(coin, np.nan)
        if not np.isfinite(d):
            continue
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            f = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            n = len(c)

            # grid regression sample
            for i in range(0, n - H, H):
                if np.isfinite(f[i]) and f[i] < 0 and np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] > 0:
                    xs.append(f[i])
                    ys.append(c[i + H] / c[i] - 1.0 - d)

            # bets on the short side (rise of |forecast| of at least the band from its lowest since last bet)
            is_bet = np.zeros(n, dtype=bool)
            ref = 0.0
            for i in range(n):
                fi = f[i]
                if not np.isfinite(fi) or fi >= 0:
                    ref = 0.0
                    continue
                m = -fi
                if m - ref >= BAND:
                    is_bet[i] = True
                    ref = m
                else:
                    ref = min(ref, m)

            # one case per grid cell: first bet in the cell with forecast <= -5
            for start in range(0, n, H):
                for i in range(start, min(start + H, n)):
                    if is_bet[i] and f[i] <= CASE_LEVEL:
                        if i + H < n and np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] > 0:
                            r = c[i + H] / c[i] - 1.0
                            case_moves.append(-(r - d))
                        break

    n_grid = len(xs)
    n_cases = len(case_moves)

    slope, t_slope = None, None
    if n_grid >= 3 and np.std(xs) > 0:
        lr = stats.linregress(np.asarray(xs), np.asarray(ys))
        slope = float(lr.slope)
        t_slope = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    mean_case = float(np.mean(case_moves)) if n_cases > 0 else None
    check_passed = (mean_case > 0) if mean_case is not None else None

    counts = {
        "cases with forecast at -5 or below": int(n_cases),
        "grid bars with a non-zero forecast": int(n_grid),
    }

    if n_cases < MIN_CASES or n_grid < MIN_GRID:
        status = "not observable"
        miss = []
        if n_cases < MIN_CASES:
            miss.append(f"fewer than 30 cases with forecast at -5 or below ({n_cases})")
        if n_grid < MIN_GRID:
            miss.append(f"fewer than 100 grid bars with a non-zero forecast ({n_grid})")
        decided = "Minimum count not reached: " + " and ".join(miss) + "."
    elif t_slope is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif t_slope >= 2 and check_passed:
        status = "confirmed"
        decided = "The slope's t is 2 or more and the cases' mean unusual short move is above 0."
    elif t_slope >= 2:
        status = "inconclusive"
        decided = "The slope's t is 2 or more but the supporting check fails, which the plan calls inconclusive."
    elif t_slope <= -2:
        status = "rejected"
        decided = "The slope's t is -2 or less: stronger levels are followed by rises relative to drift."
    else:
        status = "inconclusive"
        decided = "The slope's t is between -2 and +2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "slope of drift-adjusted 5-bar return on forecast (forecast < 0, grid bars)",
            "value": slope,
            "statistic": {"name": "OLS slope t", "value": t_slope} if t_slope is not None else None,
            "threshold": "confirm if t >= 2 with the supporting check passing; reject if t <= -2",
        },
        "supporting_check": {
            "name": "mean unusual 5-bar move in short direction of cases (forecast <= -5)",
            "value": mean_case,
            "passed": None if check_passed is None else bool(check_passed),
        },
        "counts": counts,
        "decided_by": decided,
        "reading": ("Cases are short-side bets (a rise of |forecast| of at least 2 points from its lowest since the last bet) "
                    "with forecast <= -5, the first one per 5-bar grid cell, measured from that bar's close over 5 bars within "
                    "the window; the regression uses grid bars (positions 0,5,10,...) with forecast < 0 and an OLS fit with "
                    "intercept; drift is each coin's mean non-overlapping 5-bar return over all its windows."),
    }
