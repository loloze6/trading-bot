import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 18
    BAND = 2.0
    BRK_N = 12
    RET_N = 180
    MIN_CASES = 30

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = df["close"].astype(float)
            low = df["low"].astype(float)
            fc = df["forecast"].astype(float)
            prior_low = low.shift(1).rolling(BRK_N, min_periods=BRK_N).min()
            ret180 = close / close.shift(RET_N) - 1.0
            computable = prior_low.notna() & ret180.notna()
            sit_calc = (close < prior_low) & (ret180 > 0)
            if "regime" in df.columns:
                sit_fallback = df["regime"].astype(str) == "trending"
            else:
                sit_fallback = pd.Series(False, index=df.index)
            sit = np.where(computable, sit_calc, sit_fallback)
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            n_agree += int((active & pd.Series(sit, index=df.index) & (fc < 0)).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed_sit = n_active > 0 and agreement >= 0.90

    reading = ("The situation is recomputed per window as close below the minimum low of the 12 prior bars and "
               "close/close 180 bars earlier minus 1 above 0, using the recorded regime only on a window's first bars "
               "where that history is not in the record; a case is the first short bet (rise of the short forecast's size "
               "by at least 2 points from its smallest size since the last bet, from 0 after flat or a side change) in each "
               "18-bar grid cell from each window's first row, the drift is the coin's mean 18-bar return on that grid over "
               "all its windows, and the supporting check passes when the narrower-minus-wider mean difference is above 0.")

    main_name = "mean short-side unusual 18-bar move per case, before costs"
    main_thr = "mean > 0 with t >= 2 over at least 30 cases to confirm; mean < 0 with t <= -2 over at least 30 cases to reject"

    if not passed_sit:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "cases": 0},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are short bars of the plan's situation "
                           "(close below the prior 12-bar low while the 180-bar return is positive)."),
            "reading": reading,
        }

    # ---------- 2. drift per coin ----------
    drift = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            c = df["close"].astype(float).values
            for p in range(0, len(c) - H, H):
                if np.isfinite(c[p]) and np.isfinite(c[p + H]) and c[p] > 0:
                    rets.append(c[p + H] / c[p] - 1.0)
        drift[coin] = float(np.mean(rets)) if rets else np.nan

    # ---------- 3. cases ----------
    case_moves = []
    case_fc = []
    for coin, wins in bars.items():
        d = drift.get(coin, np.nan)
        if not np.isfinite(d):
            continue
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            c = df["close"].astype(float).values
            f = df["forecast"].astype(float).fillna(0.0).values
            n = len(df)
            lowest = 0.0
            on_short = False
            used_cells = set()
            for t in range(n):
                ft = f[t]
                if ft >= 0:
                    on_short = False
                    lowest = 0.0
                    continue
                mag = -ft
                if not on_short:
                    on_short = True
                    lowest = 0.0
                lowest = min(lowest, mag)
                if mag - lowest >= BAND - 1e-12:
                    lowest = mag
                    cell = t // H
                    if cell in used_cells:
                        continue
                    used_cells.add(cell)
                    if t + H < n and np.isfinite(c[t]) and np.isfinite(c[t + H]) and c[t] > 0:
                        r = c[t + H] / c[t] - 1.0
                        case_moves.append(-(r - d))
                        case_fc.append(ft)

    moves = np.asarray(case_moves, dtype=float)
    fcs = np.asarray(case_fc, dtype=float)
    n_cases = int(len(moves))

    mean = float(np.mean(moves)) if n_cases > 0 else None
    tstat = None
    if n_cases > 1:
        sd = float(np.std(moves, ddof=1))
        tstat = float(mean / (sd / np.sqrt(n_cases))) if sd > 0 else 0.0

    # supporting check
    supp_val = None
    supp_pass = None
    n_narrow = n_wide = 0
    if n_cases > 0:
        med = float(np.median(fcs))
        narrow = moves[fcs <= med]
        wide = moves[fcs > med]
        n_narrow, n_wide = int(len(narrow)), int(len(wide))
        if n_narrow > 0 and n_wide > 0:
            supp_val = float(np.mean(narrow) - np.mean(wide))
            supp_pass = bool(supp_val > 0)
        else:
            supp_pass = False

    counts = {"cases": n_cases, "narrower half cases": n_narrow, "wider half cases": n_wide}

    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"Fewer than 30 cases ({n_cases}), the plan's minimum count, so the data could not show the idea."
    elif tstat is not None and mean > 0 and tstat >= 2:
        if supp_pass:
            status = "confirmed"
            decided = "The mean short-side unusual move is above 0 with t >= 2 over at least 30 cases and the narrower half beats the wider half."
        else:
            status = "inconclusive"
            decided = "A confirming t (>= 2, mean above 0) whose supporting check fails (narrower minus wider not above 0)."
    elif tstat is not None and mean < 0 and tstat <= -2:
        status = "rejected"
        decided = "The mean short-side unusual move is below 0 with t <= -2 over at least 30 cases."
    else:
        status = "inconclusive"
        decided = "The t of the mean short-side unusual move lies between -2 and 2 with at least 30 cases."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean,
            "statistic": {"name": "t of the mean", "value": tstat} if tstat is not None else None,
            "threshold": main_thr,
        },
        "supporting_check": {
            "name": "mean unusual move, narrower half minus wider half (Welch difference > 0)",
            "value": supp_val,
            "passed": supp_pass,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
