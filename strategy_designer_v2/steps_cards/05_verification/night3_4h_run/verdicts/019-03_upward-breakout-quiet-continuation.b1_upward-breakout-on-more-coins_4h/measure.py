import numpy as np
import pandas as pd


def measure(bars):
    H = 18
    BAND = 2.0
    MIN_CASES = 30
    RAW = "debug_info.components.nr_breakout.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            close = pd.to_numeric(df["close"], errors="coerce").values
            high = pd.to_numeric(df["high"], errors="coerce")
            prior_high = high.shift(1).rolling(12, min_periods=12).max().values
            price_break = close > prior_high
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce").values
            else:
                raw = np.full(len(df), np.nan)
            situation = np.where(np.isnan(raw), price_break, raw > 0)
            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc > 0)).sum())

    if n_active == 0:
        agreement = None
        passed = False
    else:
        agreement = n_agree / n_active
        passed = bool(agreement >= 0.9)

    main_name = "mean unusual 18-bar move of breakout bets (return minus coin's mean 18-bar return)"
    threshold = "confirm t >= 2 over >= 30 cases with upper-minus-lower > 0; reject t <= -2 over >= 30 cases"
    sup_name = "mean unusual move of upper half minus lower half (split at median signal-bar forecast)"

    if agreement is not None and not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"cases": 0},
            "decided_by": "Fewer than 90% of the bars with a non-zero forecast are long forecasts on bars whose close "
                          "clears the prior 12-bar high (positive breakout component), as the plan's situation requires.",
            "reading": "Situation taken as a positive raw nr_breakout value (or, where unrecorded, close above the prior "
                       "12-bar high within the window) with forecast > 0.",
        }

    # ---------- 2. criterion ----------
    case_ret = []
    case_coin = []
    case_fc = []
    drift = {}
    for coin, wins in bars.items():
        grid_rets = []
        coin_cases = []
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            close = pd.to_numeric(df["close"], errors="coerce").values
            n = len(df)
            # coin's normal drift: non-overlapping grid 0, H, 2H, ...
            for p in range(0, n - H, H):
                a, b = close[p], close[p + H]
                if np.isfinite(a) and np.isfinite(b) and a > 0:
                    grid_rets.append(b / a - 1.0)
            # bets: rise of the long forecast of at least BAND from its lowest level since last bet
            base = 0.0
            bets = []
            for t in range(n):
                f = fc[t]
                if f <= 0:
                    base = 0.0
                    continue
                base = min(base, f)
                if f - base >= BAND:
                    bets.append(t)
                    base = f
            # once per 18-bar grid cell: first bet in each cell
            seen = set()
            for t in bets:
                cell = t // H
                if cell in seen:
                    continue
                seen.add(cell)
                if t + H < n:
                    a, b = close[t], close[t + H]
                    if np.isfinite(a) and np.isfinite(b) and a > 0:
                        coin_cases.append((b / a - 1.0, float(fc[t])))
        drift[coin] = float(np.mean(grid_rets)) if grid_rets else np.nan
        for r, f in coin_cases:
            if np.isfinite(drift[coin]):
                case_ret.append(r - drift[coin])
                case_coin.append(coin)
                case_fc.append(f)

    um = np.array(case_ret, dtype=float)
    fcs = np.array(case_fc, dtype=float)
    n_cases = int(len(um))

    mean_um = float(np.mean(um)) if n_cases > 0 else None
    t_stat = None
    if n_cases > 1:
        sd = float(np.std(um, ddof=1))
        if sd > 0:
            t_stat = float(mean_um / (sd / np.sqrt(n_cases)))

    diff = None
    n_up = n_lo = 0
    if n_cases > 1:
        med = float(np.median(fcs))
        up = um[fcs > med]
        lo = um[fcs <= med]
        n_up, n_lo = int(len(up)), int(len(lo))
        if n_up > 0 and n_lo > 0:
            diff = float(np.mean(up) - np.mean(lo))
    sup_pass = None if diff is None else bool(diff > 0)

    if n_cases < MIN_CASES:
        status = "not observable"
        decided_by = f"Only {n_cases} cases, fewer than the plan's minimum of 30."
    elif t_stat is not None and t_stat >= 2 and sup_pass:
        status = "confirmed"
        decided_by = "The mean unusual move has t >= 2 over at least 30 cases and the upper-minus-lower difference is above 0."
    elif t_stat is not None and t_stat <= -2:
        status = "rejected"
        decided_by = "The mean unusual move has t <= -2 over at least 30 cases."
    elif t_stat is not None and t_stat >= 2:
        status = "inconclusive"
        decided_by = "t >= 2 but the upper-minus-lower difference is at or below 0, which the plan calls inconclusive."
    else:
        status = "inconclusive"
        decided_by = "The t of the mean unusual move lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": bool(passed)},
        "main_measure": {
            "name": main_name,
            "value": mean_um,
            "statistic": None if t_stat is None else {"name": "t of the mean", "value": t_stat},
            "threshold": threshold,
        },
        "supporting_check": {"name": sup_name, "value": diff, "passed": sup_pass},
        "counts": {"cases": n_cases, "upper half cases": n_up, "lower half cases": n_lo},
        "decided_by": decided_by,
        "reading": "A case is the first bet (long forecast rising >= 2 points from its lowest level since the last bet, "
                   "reset to 0 when flat) in each 18-bar grid cell counted from each window's first row, dropped if "
                   "18 bars do not remain in the window; the drift is the coin's mean return on the non-overlapping "
                   "18-bar grid of all its windows; the median split puts cases with forecast above the median in "
                   "the upper half and those at or below it in the lower half.",
    }
