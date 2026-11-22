import numpy as np
import pandas as pd


def measure(bars):
    H = 6
    BAND = 2.0
    RAW = "debug_info.components.surge_rise.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce").values
            else:
                raw = np.full(len(df), np.nan)
            active = f != 0
            n_active += int(active.sum())
            # situation: a rising hour (raw volume-weighted scaled return > 0), long side
            situ = np.where(np.isnan(raw), False, raw > 0)
            n_agree += int((active & situ & (f > 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": "t of the mean unusual 6-bar move of long signals",
                             "value": None, "statistic": None,
                             "threshold": "confirm t >= 2 with positive mean; reject t <= -2 with negative mean"},
            "supporting_check": None,
            "counts": {"cases": 0, "active bars": int(n_active)},
            "decided_by": "Fewer than 90 % of the bars with a non-zero forecast are rising hours (raw surge_rise value > 0) "
                          "with a long forecast, so the config does not do what the Fidelity's situation and long side say.",
            "reading": "The situation is read as the raw component value being positive (a rising hour, graded by volume) "
                       "with forecast > 0; bars without a recorded raw value count as outside the situation.",
        }

    # ---------- 2. criterion ----------
    # normal drift per coin: mean 6-bar return on non-overlapping grid over all windows
    drift = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            c = pd.to_numeric(df["close"], errors="coerce").values
            n = len(c)
            for p in range(0, n - H, H):
                a, b = c[p], c[p + H]
                if np.isfinite(a) and np.isfinite(b) and a > 0:
                    rets.append(b / a - 1.0)
        drift[coin] = float(np.mean(rets)) if rets else np.nan

    unusual = []
    fc_at = []
    for coin, wins in bars.items():
        d = drift[coin]
        if not np.isfinite(d):
            continue
        for w, df in wins.items():
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            c = pd.to_numeric(df["close"], errors="coerce").values
            n = len(f)
            # bets: rise of the long forecast of >= BAND from its lowest level since last bet
            low = 0.0
            bet = np.zeros(n, dtype=bool)
            for t in range(n):
                x = f[t]
                if x <= 0:
                    low = 0.0
                    continue
                if x - low >= BAND:
                    bet[t] = True
                    low = x
                else:
                    low = min(low, x)
            # once per 6-bar grid cell
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
                unusual.append((b / a - 1.0) - d)  # long direction
                fc_at.append(f[t])

    unusual = np.array(unusual, dtype=float)
    fc_at = np.array(fc_at, dtype=float)
    n_cases = int(len(unusual))

    mean_u = float(np.mean(unusual)) if n_cases > 0 else None
    t_stat = None
    if n_cases > 1:
        sd = float(np.std(unusual, ddof=1))
        t_stat = float(mean_u / (sd / np.sqrt(n_cases))) if sd > 0 else None

    sup_val = None
    n_up = n_lo = 0
    if n_cases > 0:
        med = float(np.median(fc_at))
        up = unusual[fc_at > med]
        lo = unusual[fc_at <= med]
        n_up, n_lo = int(len(up)), int(len(lo))
        if n_up > 0 and n_lo > 0:
            sup_val = float(np.mean(up) - np.mean(lo))
    sup_pass = None if sup_val is None else bool(sup_val > 0)

    if n_cases < 30:
        status = "not observable"
        decided = f"Only {n_cases} cases in total, fewer than the plan's minimum of 30."
    elif t_stat is None:
        status = "inconclusive"
        decided = "The t of the mean unusual move cannot be computed (zero spread), so it meets neither the confirm nor the reject rule."
    elif mean_u > 0 and t_stat >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "The mean unusual 6-bar move is positive with t >= 2 and the upper-minus-lower forecast half difference is above 0."
        else:
            status = "inconclusive"
            decided = "t >= 2 but the supporting check (upper half minus lower half) is at or below 0 or not computable, which the plan calls inconclusive."
    elif mean_u < 0 and t_stat <= -2:
        status = "rejected"
        decided = "The mean unusual 6-bar move is negative with t <= -2."
    else:
        status = "inconclusive"
        decided = "The t of the mean unusual 6-bar move lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "mean unusual 6-bar move of long signals (return minus coin's normal 6-bar drift)",
            "value": mean_u,
            "statistic": None if t_stat is None else {"name": "t of the mean", "value": t_stat},
            "threshold": "confirm: mean > 0 with t >= 2 (and supporting check > 0); reject: mean < 0 with t <= -2",
        },
        "supporting_check": {
            "name": "mean unusual move of upper forecast half minus lower half",
            "value": sup_val,
            "passed": sup_pass,
        },
        "counts": {"cases in total": n_cases, "upper half cases": n_up, "lower half cases": n_lo},
        "decided_by": decided,
        "reading": "A case is the first bet bar (long forecast rising >= 2 points from its lowest level since the last bet, "
                   "reset to 0 when flat) in each 6-bar grid cell counted from each window's first row, cases whose 6-bar "
                   "return would leave the window are dropped, the drift is the coin's mean 6-bar return on the same grid "
                   "over all windows, and the median split puts forecasts above the median in the upper half and those at "
                   "or below it in the lower half.",
    }
