import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    LOOKBACK = 60
    BAND = 2.0
    MIN_HALF = 30
    MIN_ALL = 60

    def _sorted(df):
        df = df.copy()
        if "timestamp" in df.columns:
            df = df.sort_values("timestamp", kind="mergesort")
        return df.reset_index(drop=True)

    # ---------- 1. situation check ----------
    n_active_checked = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = _sorted(df)
            if len(df) == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce")
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            prior_high = close.shift(1).rolling(LOOKBACK, min_periods=LOOKBACK).max()
            computable = prior_high.notna() & close.notna()
            active = (fc != 0) & computable
            situation = close > prior_high
            agree = active & situation & (fc > 0)
            n_active_checked += int(active.sum())
            n_agree += int(agree.sum())

    agreement = (n_agree / n_active_checked) if n_active_checked > 0 else None
    passed = agreement is not None and agreement >= 0.9

    reading_parts = [
        "the breakout situation is recomputed inside each window as close above the max of the prior 60 recorded closes, so only active bars with 60 prior bars in their window enter the agreement share, and the expected side is long",
    ]

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": False},
            "main_measure": {
                "name": "mean unusual 5-day move, upper minus lower forecast half",
                "value": None,
                "statistic": None,
                "threshold": "Welch t >= 2 confirms (with overall mean > 0), t <= -2 rejects",
            },
            "supporting_check": None,
            "counts": {"active bars checked": int(n_active_checked)},
            "decided_by": ("no active bars could be checked against the plan's situation"
                           if agreement is None else
                           "fewer than 90% of active bars are long bets on bars whose close is above the prior 60-day closing high"),
            "reading": "; ".join(reading_parts) + ".",
        }

    # ---------- 2. criterion ----------
    case_fc = []
    case_um = []
    for coin, wins in bars.items():
        # normal drift: mean 5-bar return on the non-overlapping grid of all windows
        grid_rets = []
        prepared = {}
        for w, df in wins.items():
            df = _sorted(df)
            prepared[w] = df
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            n = len(close)
            for i in range(0, n - H, H):
                a, b = close[i], close[i + H]
                if np.isfinite(a) and np.isfinite(b) and a > 0:
                    grid_rets.append(b / a - 1.0)
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))

        for w, df in prepared.items():
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).to_numpy(dtype=float)
            n = len(df)
            # bets: a rise of the long forecast of at least the band from its lowest level since the last bet
            is_bet = np.zeros(n, dtype=bool)
            low = 0.0
            for t in range(n):
                f = fc[t]
                if f <= 0:
                    low = 0.0
                    continue
                if f - low >= BAND:
                    is_bet[t] = True
                    low = f
                else:
                    low = min(low, f)
            # one case per grid cell: the first bet in the cell
            for start in range(0, n, H):
                idx = np.nonzero(is_bet[start:start + H])[0]
                if len(idx) == 0:
                    continue
                t = start + int(idx[0])
                if t + H >= n:
                    continue
                a, b = close[t], close[t + H]
                if not (np.isfinite(a) and np.isfinite(b) and a > 0):
                    continue
                case_fc.append(float(fc[t]))
                case_um.append(float(b / a - 1.0 - drift))

    n_all = len(case_um)
    order = sorted(range(n_all), key=lambda i: (case_fc[i], i))
    half = n_all // 2
    lower_idx = order[:half]
    upper_idx = order[n_all - half:] if half > 0 else []
    lower = np.array([case_um[i] for i in lower_idx], dtype=float)
    upper = np.array([case_um[i] for i in upper_idx], dtype=float)
    um_all = np.array(case_um, dtype=float)

    reading_parts.append(
        "a case is the first long bet (a forecast rise of at least 2 points from its lowest long level since the last bet) in each 5-bar grid cell of a window, its 5-bar return taken from that bet's close inside the window; the halves are the cases ranked by forecast, the lower n//2 against the upper n//2 (the middle case dropped when n is odd)"
    )
    reading = "; ".join(reading_parts) + "."

    counts = {"cases in upper half": int(len(upper)),
              "cases in lower half": int(len(lower)),
              "cases in all": int(n_all)}

    mean_all = float(np.mean(um_all)) if n_all > 0 else None
    diff = float(np.mean(upper) - np.mean(lower)) if len(upper) > 0 and len(lower) > 0 else None
    t_val = None
    if len(upper) >= 2 and len(lower) >= 2:
        r = stats.ttest_ind(upper, lower, equal_var=False)
        t_val = float(r.statistic) if np.isfinite(r.statistic) else None

    supp_passed = None if mean_all is None else bool(mean_all > 0)

    main = {
        "name": "mean unusual 5-day move, upper minus lower forecast half",
        "value": diff,
        "statistic": None if t_val is None else {"name": "Welch t", "value": t_val},
        "threshold": "Welch t >= 2 confirms (with overall mean unusual move > 0); t <= -2 rejects; otherwise inconclusive",
    }
    supporting = {"name": "mean unusual move over all cases above 0",
                  "value": mean_all, "passed": supp_passed}

    if len(upper) < MIN_HALF or len(lower) < MIN_HALF or n_all < MIN_ALL:
        status = "not observable"
        decided_by = (f"the plan's minimum of {MIN_HALF} cases in each half and {MIN_ALL} in all is not reached "
                      f"({len(upper)} upper, {len(lower)} lower, {n_all} in all)")
    elif t_val is None:
        status = "inconclusive"
        decided_by = "the Welch t could not be computed, so neither the confirm nor the reject rule is met"
    elif t_val >= 2 and supp_passed:
        status = "confirmed"
        decided_by = "the upper-minus-lower difference has Welch t >= 2 and the mean unusual move over all cases is above 0"
    elif t_val >= 2:
        status = "inconclusive"
        decided_by = "a confirming Welch t >= 2 but the overall mean unusual move is not above 0, which the plan calls inconclusive"
    elif t_val <= -2:
        status = "rejected"
        decided_by = "the upper-minus-lower difference has Welch t <= -2: tighter ranges are followed by smaller rises"
    else:
        status = "inconclusive"
        decided_by = "the Welch t lies between -2 and 2, which the plan calls inconclusive"

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": main,
        "supporting_check": supporting,
        "counts": counts,
        "decided_by": decided_by,
        "reading": reading,
    }
