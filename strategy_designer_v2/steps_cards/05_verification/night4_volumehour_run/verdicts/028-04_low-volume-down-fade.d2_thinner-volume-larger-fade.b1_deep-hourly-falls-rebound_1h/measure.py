import numpy as np
import pandas as pd


def measure(bars):
    H = 3
    BAND = 2.0
    RAW = "debug_info.components.fall_depth.last_history_value"

    # ---------- 1. Situation check: an hour's fall (raw scaled return < 0), long side ----------
    n_active = 0
    n_agree = 0
    for coin in bars:
        for w in bars[coin]:
            df = bars[coin][w]
            if "forecast" not in df.columns:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            raw = pd.to_numeric(df[RAW], errors="coerce") if RAW in df.columns else pd.Series(np.nan, index=df.index)
            mask = fc.notna() & (fc != 0) & raw.notna()
            n_active += int(mask.sum())
            n_agree += int((mask & (raw < 0) & (fc > 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.90)
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": "Fewer than 90% of the bars with a non-zero forecast are falling hours (raw mean-abs-scaled return < 0) with a long (positive) forecast, as the plan's Fidelity requires.",
            "reading": "none",
        }

    # ---------- 2. Criterion ----------
    case_moves = []
    case_fc = []
    case_coin = []
    for coin in bars:
        # normal 3-bar drift: mean of non-overlapping grid returns over all windows of the coin
        drift_rets = []
        for w in bars[coin]:
            c = pd.to_numeric(bars[coin][w]["close"], errors="coerce").to_numpy(dtype=float)
            for p in range(0, len(c) - H, H):
                if np.isfinite(c[p]) and np.isfinite(c[p + H]) and c[p] != 0:
                    drift_rets.append(c[p + H] / c[p] - 1.0)
        drift = float(np.mean(drift_rets)) if drift_rets else np.nan

        for w in bars[coin]:
            df = bars[coin][w]
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            f = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            n = len(df)
            # bets: rise of the long forecast of >= BAND from its lowest level since the last bet
            low = 0.0
            bet = np.zeros(n, dtype=bool)
            for i in range(n):
                fi = f[i]
                if not np.isfinite(fi) or fi <= 0:
                    low = 0.0
                    continue
                if fi - low >= BAND:
                    bet[i] = True
                    low = fi
                else:
                    low = min(low, fi)
            # once per 3-bar grid cell
            for start in range(0, n, H):
                idx = np.where(bet[start:start + H])[0]
                if len(idx) == 0:
                    continue
                t = start + int(idx[0])
                if t + H >= n:
                    continue
                if not (np.isfinite(c[t]) and np.isfinite(c[t + H]) and c[t] != 0 and np.isfinite(drift)):
                    continue
                r = c[t + H] / c[t] - 1.0
                case_moves.append(r - drift)
                case_fc.append(f[t])
                case_coin.append(coin)

    moves = np.asarray(case_moves, dtype=float)
    fcs = np.asarray(case_fc, dtype=float)
    n_cases = int(len(moves))
    counts = {"non-overlapping cases across both coins": n_cases}
    for coin in bars:
        counts["cases " + str(coin)] = int(sum(1 for x in case_coin if x == coin))

    mean = float(np.mean(moves)) if n_cases > 0 else None
    t = None
    if n_cases > 1:
        sd = float(np.std(moves, ddof=1))
        t = float(mean / (sd / np.sqrt(n_cases))) if sd > 0 else None

    sup_val = None
    sup_pass = None
    if n_cases >= 3:
        order = np.argsort(fcs, kind="mergesort")
        groups = np.array_split(order, 3)
        sup_val = float(np.mean(moves[groups[2]]) - np.mean(moves[groups[0]]))
        sup_pass = bool(sup_val > 0)

    reading = ("Cases are the first bet (long-forecast rise of >= 2 points from its lowest level since the last bet, "
               "reset at 0) in each 3-bar grid cell of each window, counted as the plan's non-overlapping cases; "
               "drift is each coin's mean non-overlapping 3-bar return over all its windows; terciles are equal-count "
               "splits of the pooled cases ranked by forecast at the signal bar.")

    main = {
        "name": "mean unusual 3-bar move after long bets, both coins",
        "value": mean,
        "statistic": {"name": "t of the mean", "value": t} if t is not None else None,
        "threshold": "confirm: mean > 0 with t >= 2 and top-minus-bottom tercile > 0; reject: mean < 0 with t <= -2",
    }
    support = {"name": "top tercile minus bottom tercile mean unusual move", "value": sup_val, "passed": sup_pass}

    if n_cases < 100:
        status = "not observable"
        decided = "Fewer than the plan's minimum of 100 non-overlapping cases across both coins."
    elif t is None:
        status = "inconclusive"
        decided = "The t of the mean cannot be computed (zero dispersion), so neither confirm nor reject rule is met."
    elif mean > 0 and t >= 2 and sup_pass:
        status = "confirmed"
        decided = "The mean unusual move is positive with t >= 2 and the top tercile beats the bottom tercile."
    elif mean < 0 and t <= -2:
        status = "rejected"
        decided = "The mean unusual move is negative with t <= -2."
    elif t >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the top tercile does not beat the bottom tercile, which the plan calls inconclusive."
    else:
        status = "inconclusive"
        decided = "t lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": support,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
