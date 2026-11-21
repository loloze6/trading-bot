import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 24
    BAND = 2.0
    RAW = "debug_info.components.drop_multiple.last_history_value"

    # ---------- 1. Situation check: a 24-bar drop (raw < 0), expected side long ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float)
            recomputed = close / close.shift(H) - 1.0
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
                raw = raw.where(raw.notna(), recomputed)
            else:
                raw = recomputed
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            active = fc != 0
            situation = raw < 0
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc > 0)).sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = True if agreement is None else bool(agreement >= 0.9)

    main_name = "mean strength minus 1 of 24-bar long cases"
    threshold = ("confirm: > 0 with t >= 2 over >= 30 cases and Spearman > 0; "
                 "reject: < 0 with t <= -2 over >= 30 cases")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None,
                             "threshold": threshold},
            "supporting_check": None,
            "counts": {"cases": 0},
            "decided_by": ("Fewer than 90% of active bars are bars where the 24-bar return is a drop "
                           "with a long (positive) forecast, as the plan's situation requires."),
            "reading": "none",
        }

    # ---------- 2. Cases and strength ----------
    case_fc = []
    case_unusual = []
    case_strength = []
    for coin, wins in bars.items():
        # coin's normal drift and usual move: non-overlapping 24-bar returns, all windows
        grid_rets = []
        for w, df in wins.items():
            c = df["close"].astype(float).to_numpy()
            idx = np.arange(0, len(c) - H, H)
            if len(idx):
                r = c[idx + H] / c[idx] - 1.0
                grid_rets.extend(list(r[np.isfinite(r)]))
        grid_rets = np.asarray(grid_rets, dtype=float)
        if len(grid_rets) < 2:
            continue
        drift = float(np.mean(grid_rets))
        usual = float(np.std(grid_rets, ddof=1))
        if not np.isfinite(usual) or usual <= 0:
            continue

        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float).to_numpy()
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).to_numpy()
            n = len(df)
            # bets on the long side: rise of the forecast of >= band from its lowest level since last bet
            low = 0.0
            bet = np.zeros(n, dtype=bool)
            for t in range(n):
                f = fc[t]
                if f <= 0:
                    low = 0.0
                    continue
                if f - low >= BAND:
                    bet[t] = True
                    low = f
                else:
                    low = min(low, f)
            seen_cells = set()
            for t in np.nonzero(bet)[0]:
                cell = t // H
                if cell in seen_cells:
                    continue
                seen_cells.add(cell)
                if t + H >= n:
                    continue
                r = c[t + H] / c[t] - 1.0
                if not np.isfinite(r):
                    continue
                unusual = r - drift  # long direction
                case_fc.append(float(fc[t]))
                case_unusual.append(float(unusual))
                case_strength.append(float(unusual / usual))

    n_cases = len(case_strength)
    s = np.asarray(case_strength, dtype=float)
    value = None
    tval = None
    if n_cases >= 1:
        value = float(np.mean(s) - 1.0)
    if n_cases >= 2:
        sd = float(np.std(s - 1.0, ddof=1))
        if sd > 0:
            tval = float(value / (sd / np.sqrt(n_cases)))
    rho = None
    if n_cases >= 3:
        rr = stats.spearmanr(case_fc, case_unusual).correlation
        if rr is not None and np.isfinite(rr):
            rho = float(rr)
    rho_pass = None if rho is None else bool(rho > 0)

    # ---------- 3. Decision ----------
    if n_cases < 30:
        status = "not observable"
        decided = f"Only {n_cases} cases over all coins and windows, fewer than the plan's minimum of 30."
    elif value is not None and tval is not None and value > 0 and tval >= 2:
        if rho_pass:
            status = "confirmed"
            decided = "Mean strength minus 1 is above 0 with t >= 2 over at least 30 cases, and the Spearman correlation is above 0."
        else:
            status = "inconclusive"
            decided = "A confirming main measure with a Spearman correlation at or below 0 (or undefined) is inconclusive."
    elif value is not None and tval is not None and value < 0 and tval <= -2:
        status = "rejected"
        decided = "Mean strength minus 1 is below 0 with t <= -2 over at least 30 cases."
    else:
        status = "inconclusive"
        decided = "The t of mean strength minus 1 lies between -2 and 2 (or is undefined), which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": bool(passed)},
        "main_measure": {
            "name": main_name,
            "value": value,
            "statistic": None if tval is None else {"name": "t of the mean", "value": tval},
            "threshold": threshold,
        },
        "supporting_check": {"name": "Spearman of case forecast vs unusual move", "value": rho,
                             "passed": rho_pass},
        "counts": {"cases": int(n_cases)},
        "decided_by": decided,
        "reading": ("Cases are long bets (forecast rises of at least 2 points from its lowest level since the last bet, "
                    "reset at 0 after a flat), the first per 24-bar grid cell from each window's first row, kept only "
                    "if 24 bars follow in the window; drift and usual move are the mean and sample std of each coin's "
                    "non-overlapping 24-bar returns pooled over its windows; the t is the ordinary t of the mean of "
                    "strength minus 1 over all cases pooled across coins."),
    }
