import numpy as np
import pandas as pd


def measure(bars):
    H = 18
    BAND = 2.0
    MIN_CASES = 30
    RAW = "debug_info.components.down_streak.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            f = pd.to_numeric(df["forecast"], errors="coerce")
            close = pd.to_numeric(df["close"], errors="coerce")
            down_close = (close < close.shift(1))
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
                situ = pd.Series(np.where(raw.notna(), raw > 0, down_close), index=df.index).astype(bool)
            else:
                situ = down_close.astype(bool)
            active = f.notna() & (f != 0)
            n_active += int(active.sum())
            n_agree += int((active & situ & (f > 0)).sum())

    if n_active == 0:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None, "passed": False},
            "main_measure": {"name": "mean unusual 18-bar move of long cases, pooled",
                             "value": None, "statistic": None,
                             "threshold": "t >= 2 to confirm, t <= -2 to reject, over at least 30 independent cases"},
            "supporting_check": None,
            "counts": {"independent cases": 0},
            "decided_by": "No bar has a non-zero forecast, so there are fewer than 30 independent cases.",
            "reading": "With no active bar the situation check is vacuous and no case exists.",
        }

    agreement = n_agree / n_active
    if agreement < 0.9:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": "mean unusual 18-bar move of long cases, pooled",
                             "value": None, "statistic": None,
                             "threshold": "t >= 2 to confirm, t <= -2 to reject, over at least 30 independent cases"},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of active bars are long bars inside a running down-close streak "
                           "(raw streak loss > 0), so the forecast does not follow the plan's situation and side."),
            "reading": "Situation = raw streak value > 0 (down close from prices where the raw value is missing), side long.",
        }

    # ---------- 2. criterion ----------
    case_moves = []
    case_fc = []
    for coin, wins in bars.items():
        # coin drift: mean of non-overlapping 18-bar returns over all windows
        grid_rets = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            for p in range(0, len(c) - H, H):
                a, b = c[p], c[p + H]
                if np.isfinite(a) and np.isfinite(b) and a > 0:
                    grid_rets.append(b / a - 1.0)
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))

        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            f = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            n = len(df)
            # long bets: rise of forecast >= band from its lowest long level since last bet
            ref = 0.0
            bet = np.zeros(n, dtype=bool)
            for i in range(n):
                fi = f[i]
                if not np.isfinite(fi) or fi <= 0:
                    ref = 0.0
                    continue
                if fi - ref >= BAND:
                    bet[i] = True
                    ref = fi
                else:
                    ref = min(ref, fi)
            # one case per grid cell: the first bet of the cell
            for start in range(0, n, H):
                idx = np.where(bet[start:start + H])[0]
                if len(idx) == 0:
                    continue
                t = start + int(idx[0])
                if t + H >= n:
                    continue
                a, b = c[t], c[t + H]
                if not (np.isfinite(a) and np.isfinite(b) and a > 0):
                    continue
                case_moves.append((b / a - 1.0) - drift)
                case_fc.append(f[t])

    moves = np.array(case_moves, dtype=float)
    fcs = np.array(case_fc, dtype=float)
    n_cases = int(len(moves))

    mean_mv = float(np.mean(moves)) if n_cases > 0 else None
    tstat = None
    if n_cases > 1:
        sd = float(np.std(moves, ddof=1))
        tstat = float(mean_mv / (sd / np.sqrt(n_cases))) if sd > 0 else None

    sup_val = None
    sup_pass = None
    if n_cases > 1:
        med = float(np.median(fcs))
        up = moves[fcs > med]
        lo = moves[fcs <= med]
        if len(up) > 0 and len(lo) > 0:
            sup_val = float(np.mean(up) - np.mean(lo))
            sup_pass = bool(sup_val > 0)
        else:
            sup_pass = False

    main = {"name": "mean unusual 18-bar move of long cases, pooled over coins",
            "value": mean_mv,
            "statistic": {"name": "t of the mean", "value": tstat} if tstat is not None else None,
            "threshold": "t >= 2 to confirm, t <= -2 to reject, over at least 30 independent cases"}
    supporting = {"name": "upper-half minus lower-half mean unusual move (split at median forecast)",
                  "value": sup_val, "passed": sup_pass}

    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"Only {n_cases} independent cases, fewer than the plan's minimum of 30."
    elif tstat is not None and tstat >= 2 and sup_pass:
        status = "confirmed"
        decided = "t >= 2 over at least 30 independent cases and the upper-half minus lower-half difference is above 0."
    elif tstat is not None and tstat <= -2:
        status = "rejected"
        decided = "t <= -2 over at least 30 independent cases."
    elif tstat is not None and tstat >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the upper-half minus lower-half difference is not above 0."
    else:
        status = "inconclusive"
        decided = "t is between -2 and 2 over at least 30 independent cases."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": main,
        "supporting_check": supporting,
        "counts": {"independent cases": n_cases},
        "decided_by": decided,
        "reading": ("A case is the first long bet (forecast rise >= 2 from its lowest long level since the last bet) "
                    "in each 18-bar grid cell of a window, dropped if its 18-bar return leaves the window; the drift is "
                    "the coin's mean grid 18-bar return over all windows; the upper half is forecast strictly above "
                    "the median and the lower half the rest."),
    }
