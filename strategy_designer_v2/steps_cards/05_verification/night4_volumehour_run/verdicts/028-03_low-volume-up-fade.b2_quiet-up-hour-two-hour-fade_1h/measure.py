import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 2
    BAND = 2.0
    RAW = "debug_info.components.rise.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            reg = df["regime"].astype(str).values
            raw = (pd.to_numeric(df[RAW], errors="coerce").values
                   if RAW in df.columns else np.full(len(df), np.nan))
            active = f != 0
            # situation: volume ratio regime (detector's decision) and a rise on the latest bar
            situ = (reg == "mean_reversion") & np.nan_to_num(raw > 0, nan=False)
            n_active += int(active.sum())
            n_agree += int((active & situ & (f < 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    reading = ("Situation bars are bars with regime 'mean_reversion' (the recorded detector decision for the "
               "720-bar volume ratio between 0.67 and 1.5) whose raw 'rise' value is above 0, expected side short; "
               "a case is the first short bet (forecast falling at least 2 points below its least-negative level "
               "since the last bet, reset at flat or side change) in each 2-bar grid cell from each window's first row, "
               "and the unusual move is -(r - drift) with drift the coin's mean non-overlapping 2-bar return pooled "
               "over all its windows, following the workflow's 'minus drift, in the signal direction' and the reject "
               "rule's 'beyond drift'.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": "mean unusual 2-bar move in the short direction on short bets",
                             "value": None, "statistic": None,
                             "threshold": "t >= 2 to confirm, t <= -2 to reject, over at least 30 cases"},
            "supporting_check": None,
            "counts": {"cases": None, "active_bars": n_active},
            "decided_by": ("Fewer than 90% of non-zero forecast bars are short forecasts on quiet-volume "
                           "(mean_reversion regime) rising bars, as the Fidelity's situation and side require."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    moves = []
    sizes = []
    for coin, wins in bars.items():
        # coin drift: non-overlapping 2-bar returns, all windows pooled
        rets = []
        for w, df in wins.items():
            c = pd.to_numeric(df["close"], errors="coerce").values
            idx = np.arange(0, len(c) - H, H)
            r = c[idx + H] / c[idx] - 1.0
            rets.append(r[np.isfinite(r)])
        rets = np.concatenate(rets) if rets else np.array([])
        if len(rets) == 0:
            continue
        drift = float(np.mean(rets))

        for w, df in wins.items():
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            c = pd.to_numeric(df["close"], errors="coerce").values
            n = len(f)
            bet = np.zeros(n, dtype=bool)
            ref = 0.0
            for i in range(n):
                if f[i] >= 0:
                    ref = 0.0
                    continue
                s = -f[i]
                if s - ref >= BAND:
                    bet[i] = True
                    ref = s
                else:
                    ref = min(ref, s)
            for start in range(0, n, H):
                cell = np.where(bet[start:start + H])[0]
                if len(cell) == 0:
                    continue
                t = start + int(cell[0])
                if t + H >= n:
                    continue
                r = c[t + H] / c[t] - 1.0
                if not np.isfinite(r):
                    continue
                moves.append(-(r - drift))
                sizes.append(abs(f[t]))

    moves = np.array(moves, dtype=float)
    sizes = np.array(sizes, dtype=float)
    n_cases = int(len(moves))

    mean_move = float(np.mean(moves)) if n_cases > 0 else None
    t_stat = None
    if n_cases > 1:
        sd = float(np.std(moves, ddof=1))
        t_stat = float(mean_move / (sd / np.sqrt(n_cases))) if sd > 0 else 0.0
    slope = None
    if n_cases > 2 and np.std(sizes) > 0:
        slope = float(stats.linregress(sizes, moves).slope)

    slope_pass = None if slope is None else bool(slope > 0)

    if n_cases < 30:
        status = "not observable"
        decided = f"Fewer than 30 cases in total ({n_cases}), the plan's minimum count."
    elif t_stat is not None and mean_move > 0 and t_stat >= 2 and slope_pass:
        status = "confirmed"
        decided = "Mean unusual move positive with t >= 2 over at least 30 cases, and the slope on |forecast| above 0."
    elif t_stat is not None and mean_move < 0 and t_stat <= -2:
        status = "rejected"
        decided = "Mean unusual move negative with t <= -2 over at least 30 cases: quiet-volume rises keep extending beyond drift."
    elif t_stat is not None and t_stat >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the supporting slope is not above 0."
    else:
        status = "inconclusive"
        decided = "t between -2 and 2 over at least 30 cases."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": "mean unusual 2-bar move in the short direction on short bets",
                         "value": mean_move,
                         "statistic": None if t_stat is None else {"name": "t of the mean", "value": t_stat},
                         "threshold": "positive with t >= 2 to confirm, negative with t <= -2 to reject, over at least 30 cases"},
        "supporting_check": {"name": "OLS slope of unusual move on |forecast|",
                             "value": slope, "passed": slope_pass},
        "counts": {"cases": n_cases},
        "decided_by": decided,
        "reading": reading,
    }
