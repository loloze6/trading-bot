import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 72
    BAND = 2.0
    PERIOD = 720
    MIN_CASES = 30

    def depth_series(close):
        hi = close.rolling(PERIOD, min_periods=PERIOD).max()
        return (close - hi) / hi * 100.0

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            dep = depth_series(close)
            active = (fc != 0) & dep.notna()
            n_active += int(active.sum())
            n_agree += int((active & (dep <= -20.0) & (fc > 0)).sum())
    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars checked": int(n_active)},
            "decided_by": ("Fewer than 90 % of the bars with a non-zero forecast are long bars at least 20 % "
                           "below the 720-bar closing high, as the plan's situation requires"
                           if n_active > 0 else "No active bar with a computable depth was found to check the plan's situation"),
            "reading": "Depth is the close vs the highest of the last 720 closes (current bar included) within each window; "
                       "bars with fewer than 720 closes of window history are left out of the check.",
        }

    # ---------- 2. cases ----------
    case_rows = []
    for coin, wins in bars.items():
        # normal drift: mean 72-bar return on the grid over all windows of the coin
        grid_rets = []
        per_window = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            n = len(close)
            for p in range(0, n - H, H):
                c0, c1 = close[p], close[p + H]
                if np.isfinite(c0) and np.isfinite(c1) and c0 > 0:
                    grid_rets.append(c1 / c0 - 1.0)
            per_window.append(df)
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))

        for df in per_window:
            close_s = pd.to_numeric(df["close"], errors="coerce")
            close = close_s.values
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            dep = depth_series(close_s).values
            n = len(close)
            # bets: rise of the long forecast of >= BAND from its lowest level since last bet
            base = 0.0
            prev = 0.0
            bet_pos = []
            for i in range(n):
                f = fc[i]
                if f > 0:
                    if prev <= 0:
                        base = 0.0
                    base = min(base, f)
                    if f - base >= BAND:
                        bet_pos.append(i)
                        base = f
                else:
                    base = 0.0
                prev = f
            seen = set()
            for i in bet_pos:
                cell = i // H
                if cell in seen:
                    continue
                seen.add(cell)
                if i + H >= n:
                    continue
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1) and c0 > 0):
                    continue
                r = c1 / c0 - 1.0
                case_rows.append((r - drift, dep[i]))

    unusual = np.array([c[0] for c in case_rows], dtype=float)
    depths = np.array([c[1] for c in case_rows], dtype=float)
    n_cases = int(len(unusual))

    mean_u = float(np.mean(unusual)) if n_cases > 0 else None
    if n_cases >= 2:
        sd = float(np.std(unusual, ddof=1))
        t_u = float(mean_u / (sd / np.sqrt(n_cases))) if sd > 0 else None
    else:
        t_u = None

    # supporting check
    ok = np.isfinite(depths)
    sup_value = None
    sup_t = None
    sup_pass = None
    n_deep = n_shallow = 0
    if ok.sum() >= 2:
        u_ok = unusual[ok]
        d_ok = depths[ok]
        med = float(np.median(d_ok))
        deep = u_ok[d_ok < med]
        shallow = u_ok[d_ok >= med]
        n_deep, n_shallow = int(len(deep)), int(len(shallow))
        if n_deep >= 1 and n_shallow >= 1:
            sup_value = float(np.mean(deep) - np.mean(shallow))
            sup_pass = bool(sup_value > 0)
            if n_deep >= 2 and n_shallow >= 2:
                tt = stats.ttest_ind(deep, shallow, equal_var=False)
                if np.isfinite(tt.statistic):
                    sup_t = float(tt.statistic)

    # ---------- 3. decision ----------
    if n_cases < MIN_CASES:
        status = "not observable"
        decided_by = f"Only {n_cases} cases, fewer than the plan's minimum of 30."
    elif t_u is None:
        status = "inconclusive"
        decided_by = "The main t could not be computed (no spread in the unusual moves)."
    elif mean_u > 0 and t_u >= 2:
        if sup_pass:
            status = "confirmed"
            decided_by = "Mean unusual move above 0 with t >= 2 over at least 30 cases, and the deeper half's mean exceeds the shallower half's."
        else:
            status = "inconclusive"
            decided_by = "Main t of 2 or more but the depth check failed (deeper half not above shallower half)."
    elif mean_u < 0 and t_u <= -2:
        status = "rejected"
        decided_by = "Mean unusual move below 0 with t <= -2 over at least 30 cases."
    else:
        status = "inconclusive"
        decided_by = "Main t between -2 and 2 over at least 30 cases."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": passed},
        "main_measure": {
            "name": "mean 72-bar unusual move of the long cases (return minus coin's normal 72-bar drift)",
            "value": mean_u,
            "statistic": {"name": "t of the mean", "value": t_u} if t_u is not None else None,
            "threshold": "confirm: mean > 0 with t >= 2 over >= 30 cases; reject: mean < 0 with t <= -2 over >= 30 cases",
        },
        "supporting_check": {
            "name": "deeper-half minus shallower-half mean unusual move (Welch difference > 0)",
            "value": sup_value,
            "passed": sup_pass,
        },
        "counts": {
            "cases": n_cases,
            "deeper half cases": n_deep,
            "shallower half cases": n_shallow,
        },
        "decided_by": decided_by,
        "reading": ("Bets are long forecast rises of >= 2 points from the lowest level since the last bet, the first per 72-bar grid cell "
                    "of each window counted from its first row; depth uses the 720 closes including the current bar within the window, "
                    "cases or bars without 720 closes of history are left out of the depth measures; the deeper half is depth strictly "
                    "below the median and the shallower half the rest; the check passes on the sign of the difference (Welch t reported "
                    "as supporting information only)."),
        "supporting_welch_t": sup_t,
    }
