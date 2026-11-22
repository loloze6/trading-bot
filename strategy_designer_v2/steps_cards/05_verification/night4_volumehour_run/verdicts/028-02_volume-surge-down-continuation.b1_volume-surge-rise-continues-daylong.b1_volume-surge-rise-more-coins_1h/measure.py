import numpy as np
import pandas as pd


def measure(bars):
    RAW = "debug_info.components.vol_move.last_history_value"
    H = 24
    BAND = 2.0
    MIN_CASES = 30

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce").to_numpy(dtype=float)
            else:
                raw = np.full(len(df), np.nan)
            ret = np.full(len(df), np.nan)
            if len(df) > 1:
                ret[1:] = close[1:] / close[:-1] - 1.0
            active = np.isfinite(fc) & (fc != 0)
            # situation: the rise-times-volume product is positive (a rise on volume),
            # and the hour's own return is a rise where it can be computed inside the window
            rise_ok = np.where(np.isfinite(ret), ret > 0, True)
            situ = np.isfinite(raw) & (raw > 0) & rise_ok
            agree = active & situ & (fc > 0)
            n_active += int(active.sum())
            n_agree += int(agree.sum())

    if n_active > 0:
        agreement = n_agree / n_active
        passed = agreement >= 0.9
    else:
        agreement = None
        passed = True

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "agreeing bars": int(n_agree)},
            "decided_by": "Fewer than 90% of the bars with a non-zero forecast are long bars on an hour "
                          "with a positive rise-times-volume product and a rising close, as the Fidelity's situation requires.",
            "reading": "Situation taken as raw component value > 0 and the hour's close-to-close return > 0 (where "
                       "computable within the window), expected side long.",
        }

    # ---------- 2. criterion ----------
    unusual = []
    case_fc = []
    per_coin_cases = {}
    for coin, wins in bars.items():
        # normal 24-bar drift over all windows (non-overlapping grid from each window's first row)
        grid_rets = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            for s in range(0, len(close) - H, H):
                r = close[s + H] / close[s] - 1.0
                if np.isfinite(r):
                    grid_rets.append(r)
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))

        nc = 0
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            n = len(fc)
            # bets: a rise of the long forecast of at least BAND from its lowest level since last bet
            bet = np.zeros(n, dtype=bool)
            low = 0.0
            for i in range(n):
                f = fc[i]
                if not np.isfinite(f) or f <= 0:
                    low = 0.0
                    continue
                if f - low >= BAND:
                    bet[i] = True
                    low = f
                else:
                    low = min(low, f)
            # once per 24-bar grid cell: the first bet of the cell
            for s in range(0, n, H):
                idx = np.nonzero(bet[s:s + H])[0]
                if len(idx) == 0:
                    continue
                t = s + int(idx[0])
                if t + H >= n:
                    continue
                r = close[t + H] / close[t] - 1.0
                if not np.isfinite(r):
                    continue
                unusual.append(r - drift)  # long side
                case_fc.append(fc[t])
                nc += 1
        per_coin_cases[coin] = nc

    unusual = np.asarray(unusual, dtype=float)
    case_fc = np.asarray(case_fc, dtype=float)
    n_cases = int(len(unusual))

    mean_u = float(np.mean(unusual)) if n_cases > 0 else None
    t_u = None
    if n_cases > 1:
        sd = float(np.std(unusual, ddof=1))
        if sd > 0:
            t_u = float(mean_u / (sd / np.sqrt(n_cases)))

    sup_val = None
    sup_pass = None
    n_top = n_bot = 0
    if n_cases > 0:
        med = float(np.median(case_fc))
        top = unusual[case_fc > med]
        bot = unusual[case_fc <= med]
        n_top, n_bot = int(len(top)), int(len(bot))
        if n_top > 0 and n_bot > 0:
            sup_val = float(np.mean(top) - np.mean(bot))
            sup_pass = bool(sup_val > 0)
        else:
            sup_pass = False

    counts = {"cases": n_cases, "top half cases": n_top, "bottom half cases": n_bot}
    for c, k in per_coin_cases.items():
        counts["cases " + str(c)] = int(k)

    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"Only {n_cases} cases, fewer than the plan's minimum of 30."
    elif t_u is not None and mean_u > 0 and t_u >= 2 and sup_pass:
        status = "confirmed"
        decided = "The mean unusual move is positive with t >= 2 on at least 30 cases and the top-minus-bottom half difference is above 0."
    elif t_u is not None and mean_u < 0 and t_u <= -2:
        status = "rejected"
        decided = "The mean unusual move is negative with t <= -2 on at least 30 cases."
    elif t_u is not None and t_u >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the supporting check (top minus bottom half) is not above 0."
    else:
        status = "inconclusive"
        decided = "The t of the mean unusual move is between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": True},
        "main_measure": {
            "name": "mean unusual 24-bar move after a forecast rise of at least 2 points",
            "value": mean_u,
            "statistic": None if t_u is None else {"name": "t of the mean", "value": t_u},
            "threshold": "positive with t >= 2 on at least 30 cases to confirm; negative with t <= -2 on at least 30 cases to reject",
        },
        "supporting_check": {
            "name": "top-half minus bottom-half mean unusual move, split at median forecast",
            "value": sup_val,
            "passed": sup_pass,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": "Cases are the first bet bar (forecast rise >= 2 from its lowest positive level since the last bet, "
                   "reset at 0) in each 24-bar cell counted from each window's first row, with returns only inside the window; "
                   "drift is the coin's mean non-overlapping 24-bar return over all its windows; the median split puts "
                   "cases above the median forecast in the top half and the rest in the bottom half.",
    }
